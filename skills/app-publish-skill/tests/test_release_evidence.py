"""Offline identity checks using synthetic baselines and byte fixtures."""
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'scripts/release_evidence.py'
DOCTOR = ROOT / 'scripts/doctor.sh'
SPEC = importlib.util.spec_from_file_location('release_evidence', TOOL)
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


class ReleaseEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 26, 2, 0, tzinfo=timezone.utc)
        self.baseline = {'bundle_id': 'com.example.app', 'platform': 'ios',
                         'observed_at': self.now.isoformat(), 'public_version': '1.2.9',
                         'latest_uploaded_version': '1.2.9', 'highest_uploaded_build': 90}

    def plan(self, **changes):
        return evidence.make_plan({**self.baseline, **changes}, self.now)

    def test_public_version_patch_increments_with_global_build(self):
        proposal = self.plan()
        self.assertEqual((proposal['candidate_version'], proposal['candidate_build']), ('1.2.10', 91))
        self.assertEqual(proposal['status'], 'PROPOSAL_ONLY')

    def test_active_test_version_reused_with_global_build(self):
        proposal = self.plan(latest_uploaded_version='1.10.0', highest_uploaded_build=250)
        self.assertEqual((proposal['candidate_version'], proposal['candidate_build']), ('1.10.0', 251))

    def test_rejects_stale_and_future_store_reads(self):
        for offset in (timedelta(minutes=-30, seconds=-1), timedelta(seconds=61)):
            with self.subTest(offset=offset), self.assertRaises(evidence.EvidenceError):
                self.plan(observed_at=(self.now + offset).isoformat())

    def test_accepts_exact_freshness_boundaries_and_offset_time(self):
        self.plan(observed_at=(self.now - timedelta(minutes=30)).isoformat())
        self.plan(observed_at=(self.now + timedelta(seconds=60)).isoformat())
        self.plan(observed_at='2026-10-26T10:00:00+08:00')

    def test_missing_fields_do_not_default_to_zero(self):
        for field in evidence.REQUIRED:
            incomplete = dict(self.baseline)
            del incomplete[field]
            with self.subTest(field=field), self.assertRaises(evidence.EvidenceError):
                evidence.make_plan(incomplete, self.now)

    def test_rejects_ambiguous_versions_and_conflicting_store_state(self):
        for version in ('1.2', '1.2.3-beta', '01.2.3', '1.2.3 ', None):
            with self.subTest(version=version), self.assertRaises(evidence.EvidenceError):
                self.plan(latest_uploaded_version=version)
        with self.assertRaises(evidence.EvidenceError):
            self.plan(latest_uploaded_version='1.2.8')

    def test_rejects_invalid_global_build_and_unzoned_timestamp(self):
        for build in (0, -1, '90', 90.0, True, None):
            with self.subTest(build=build), self.assertRaises(evidence.EvidenceError):
                self.plan(highest_uploaded_build=build)
        with self.assertRaises(evidence.EvidenceError):
            self.plan(observed_at='2026-10-26T02:00:00')

    def test_cli_preserves_existing_output_and_hashes_raw_baseline(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'baseline.json'
            output = Path(temp) / 'proposal.json'
            fresh = {**self.baseline, 'observed_at': datetime.now(timezone.utc).isoformat()}
            source.write_text(json.dumps(fresh), encoding='utf-8')
            command = [sys.executable, str(TOOL), 'plan', '--baseline', str(source), '--output', str(output)]
            first = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(output.read_text())['baseline_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
            output.write_text('preserve me')
            second = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_text(), 'preserve me')
            third = subprocess.run(command + ['--overwrite'], text=True, capture_output=True)
            self.assertEqual(third.returncode, 0, third.stderr)

    def test_cli_rejects_duplicate_json_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'baseline.json'
            source.write_text('{"platform":"ios","platform":"android"}')
            result = subprocess.run([sys.executable, str(TOOL), 'plan', '--baseline', str(source),
                                     '--output', str(Path(temp) / 'proposal.json')], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Duplicate', result.stderr)

    def test_artifact_hash_must_match_frozen_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / 'example.ipa'
            artifact.write_bytes(b'synthetic zip identity fixture')
            command = [sys.executable, str(TOOL), 'verify-artifact', '--artifact', str(artifact), '--expected-sha256']
            expected = hashlib.sha256(artifact.read_bytes()).hexdigest()
            matching = subprocess.run(command + [expected], text=True, capture_output=True)
            self.assertEqual(matching.returncode, 0, matching.stderr)
            artifact.write_bytes(b'replaced artifact')
            changed = subprocess.run(command + [expected], text=True, capture_output=True)
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn('mismatch', changed.stderr)

    def test_doctor_missing_python_has_actionable_failure(self):
        result = subprocess.run(['/bin/sh', str(DOCTOR)], env={**os.environ, 'PATH': ''}, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python 3.9+', result.stderr)

    def test_doctor_old_python_has_actionable_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            python = Path(temp) / 'python3'
            python.write_text('#!/bin/sh\nexit 1\n')
            python.chmod(0o755)
            result = subprocess.run(['/bin/sh', str(DOCTOR)], env={**os.environ, 'PATH': temp}, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('older than 3.9', result.stderr)

    def test_doctor_rejects_incomplete_standalone_package(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / 'skill'
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('__pycache__'))
            (package / 'references/metadata-screenshots.md').unlink()
            result = subprocess.run(['/bin/sh', str(package / 'scripts/doctor.sh')],
                                    text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('references/metadata-screenshots.md', result.stderr)


class ProjectDoctorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / 'app'
        self.project.mkdir()
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        (self.bin / 'python3').symlink_to(sys.executable)
        self.log = self.base / 'commands.jsonl'
        self.env = {**os.environ, 'PATH': str(self.bin), 'DOCTOR_TEST_LOG': str(self.log)}
        for name in ('ruby', 'bundle', 'fastlane', 'xcodebuild', 'node', 'flutter', 'java'):
            self.stub(name)

    def stub(self, name, fail_args=(), delay=0, version=None):
        versions = {'ruby': 'ruby 3.3.7', 'bundle': 'Bundler version 2.6.9',
                    'fastlane': 'fastlane 2.228.0', 'xcodebuild': 'Xcode 16.4',
                    'node': 'v22.16.0', 'flutter': 'Flutter 3.32.0', 'java': 'openjdk version "17.0.15"'}
        path = self.bin / name
        path.write_text('#!' + sys.executable + '\n' +
                        'import json, os, sys, time\n' +
                        'from pathlib import Path\n' +
                        'args=sys.argv[1:]\n' +
                        'if args and args[0].startswith("_"): args=args[1:]\n' +
                        'with open(os.environ["DOCTOR_TEST_LOG"], "a") as log:\n' +
                        ' log.write(json.dumps({"tool":' + repr(name) + ',"args":args,"raw_args":sys.argv[1:],"cwd":str(Path.cwd()),"gemfile":os.environ.get("BUNDLE_GEMFILE"),"frozen":os.environ.get("BUNDLE_FROZEN"),"auto_install":os.environ.get("BUNDLE_AUTO_INSTALL"),"bundle_version":os.environ.get("BUNDLE_VERSION"),"bundler_version":os.environ.get("BUNDLER_VERSION")})+"\\n")\n' +
                        'if args == ' + repr(list(fail_args)) + ':\n sys.exit(1)\n' +
                        'time.sleep(' + repr(delay) + ')\n' +
                        'if ' + repr(name) + ' == "ruby" and args[:1] == ["-rjson"]:\n print(json.dumps({"auto_install":os.environ.get("DOCTOR_TEST_AUTO_INSTALL") == "true","frozen":os.environ.get("DOCTOR_TEST_FROZEN", "true") == "true","version_safe":True})); sys.exit(0)\n' +
                        'print("fastlane 2.228.0" if ' + repr(name) + ' == "bundle" and args[:1] == ["exec"] else ' + repr(version or versions[name]) + ')\n')
        path.chmod(0o755)

    def adapter(self, relative='fastlane', gemfile=True):
        adapter = self.project / relative
        adapter.mkdir(parents=True)
        (adapter / 'Fastfile').write_text('lane :beta do\nend\n')
        if gemfile:
            (adapter.parent / 'Gemfile').write_text('source "https://rubygems.org"\ngem "fastlane"\n')
            (adapter.parent / 'Gemfile.lock').write_text('GEM\n  specs:\n    fastlane (2.228.0)\n\nBUNDLED WITH\n   2.6.9\n')
        return adapter

    def doctor(self, *extra):
        return subprocess.run(['/bin/sh', str(DOCTOR), '--project', str(self.project), *extra],
                              env=self.env, text=True, capture_output=True)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_bundle_presence_does_not_mask_unrunnable_project_fastlane(self):
        self.adapter()
        self.stub('bundle', ('exec', 'fastlane', '--version'))
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Fastlane', result.stderr)
        self.assertTrue(any(call['args'] == ['exec', 'fastlane', '--version'] for call in self.calls()))

    def test_missing_bundle_gems_stops_before_fastlane_execution(self):
        self.adapter()
        self.stub('bundle', ('check', '--dry-run'))
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(call['args'] == ['exec', 'fastlane', '--version'] for call in self.calls()))
        self.assertIn('bundle check', result.stderr)

    def test_ios_adapter_uses_its_gemfile_and_frozen_bundle(self):
        adapter = self.adapter('ios/fastlane')
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [call for call in self.calls() if call['tool'] == 'bundle']
        self.assertTrue(any(call['args'] == ['exec', 'fastlane', '--version'] for call in calls))
        self.assertTrue(all(call['cwd'] == str(adapter.parent) for call in calls))
        self.assertTrue(all(call['gemfile'] == str(adapter.parent / 'Gemfile') for call in calls))
        self.assertTrue(all(call['frozen'] == 'true' for call in calls))
        self.assertTrue(all(call['auto_install'] == 'false' for call in calls))
        self.assertTrue(all(call['bundle_version'] == 'system' for call in calls))
        self.assertTrue(all(call['bundler_version'] == '2.6.9' for call in calls))
        self.assertTrue(all(call['raw_args'][0] == '_2.6.9_' for call in calls))

    def test_standalone_fastlane_must_exist_and_run(self):
        self.adapter(gemfile=False)
        (self.bin / 'fastlane').unlink()
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.stub('fastlane')
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('WARN', result.stdout)
        self.assertTrue(any(call['tool'] == 'fastlane' and call['args'] == ['--version'] for call in self.calls()))

    def test_explicit_monorepo_adapter_finds_ancestor_gemfile(self):
        adapter = self.adapter('apps/mobile/ios/fastlane', gemfile=False)
        (self.project / 'Gemfile').write_text('gem "fastlane"\n')
        (self.project / 'Gemfile.lock').write_text('GEM\n\nBUNDLED WITH\n   2.6.9\n')
        result = self.doctor('--fastlane-dir', 'apps/mobile/ios/fastlane')
        self.assertEqual(result.returncode, 0, result.stderr)
        check = next(call for call in self.calls() if call['args'] == ['check', '--dry-run'])
        self.assertEqual(check['gemfile'], str(self.project / 'Gemfile'))
        execution = next(call for call in self.calls() if call['args'] == ['exec', 'fastlane', '--version'])
        self.assertEqual(execution['cwd'], str(adapter.parent))

    def test_ambiguous_adapter_requires_explicit_selection(self):
        self.adapter('ios/fastlane')
        self.adapter('android/fastlane')
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--fastlane-dir', result.stderr)
        self.assertEqual(self.calls(), [])

    def test_native_and_react_native_do_not_require_flutter(self):
        self.adapter()
        (self.project / 'Demo.xcworkspace').mkdir()
        (self.bin / 'flutter').unlink()
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any(call['tool'] == 'xcodebuild' for call in self.calls()))
        (self.project / 'package.json').write_text(json.dumps({'dependencies': {'react-native': '0.79.0'}}))
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any(call['tool'] == 'node' for call in self.calls()))

    def test_unrelated_package_json_does_not_require_node(self):
        self.adapter()
        (self.project / 'package.json').write_text(json.dumps({'dependencies': {'typescript': '5.8.0'}}))
        (self.bin / 'node').unlink()
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_command_timeout_is_a_failure_without_dumping_tool_logs(self):
        self.adapter(gemfile=False)
        self.stub('fastlane', delay=1)
        result = self.doctor('--timeout-seconds', '0.1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('timed out', result.stderr)

    def test_missing_lockfile_cannot_trigger_dependency_resolution(self):
        self.adapter()
        (self.project / 'Gemfile.lock').unlink()
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Gemfile.lock', result.stderr)
        self.assertFalse(any(call['tool'] == 'bundle' for call in self.calls()))

    def test_android_target_checks_java_wrapper_and_skips_ios_toolchain(self):
        self.adapter()
        (self.project / 'ios').mkdir()
        (self.project / 'android').mkdir()
        wrapper = self.project / 'android/gradlew'
        wrapper.write_text('#!/bin/sh\nexit 99\n')
        (self.bin / 'xcodebuild').unlink()
        (self.bin / 'flutter').unlink()
        result = self.doctor('--platform', 'android')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(any(call['tool'] == 'java' for call in self.calls()))
        self.assertFalse(any(call['tool'] == 'xcodebuild' for call in self.calls()))
        wrapper.unlink()
        result = self.doctor('--platform', 'android')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('gradlew', result.stderr)

    def test_local_settings_cannot_enable_install_or_disable_frozen_mode(self):
        self.adapter()
        for key, value in (('DOCTOR_TEST_AUTO_INSTALL', 'true'), ('DOCTOR_TEST_FROZEN', 'false')):
            with self.subTest(setting=key):
                self.env[key] = value
                if self.log.exists():
                    self.log.unlink()
                result = self.doctor()
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(any(call['args'][:1] in (['check'], ['exec']) for call in self.calls()))
                self.assertIn('Bundler settings', result.stderr)
                del self.env[key]

    def test_bundler_version_must_match_lock_exactly(self):
        self.adapter()
        self.stub('bundle', version='Bundler version 2.6.8')
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('differs', result.stderr)
        self.assertFalse(any(call['args'][:1] in (['check'], ['exec']) for call in self.calls()))

    def test_standalone_drops_unrelated_bundle_injection(self):
        self.adapter(gemfile=False)
        self.env.update({'BUNDLE_GEMFILE': '/not-this-project/Gemfile', 'BUNDLER_VERSION': '1.0.0',
                         'BUNDLE_BIN_PATH': '/not-this-project/bundle', 'RUBYOPT': '-rbundler/setup'})
        result = self.doctor()
        self.assertEqual(result.returncode, 0, result.stderr)
        check = next(call for call in self.calls() if call['tool'] == 'fastlane')
        self.assertIsNone(check['gemfile'])
        self.assertIsNone(check['bundler_version'])

    def test_explicit_monorepo_adapter_checks_nearest_app_manifest(self):
        adapter = self.adapter('apps/mobile/ios/fastlane')
        app = adapter.parent.parent
        (app / 'package.json').write_text(json.dumps({'dependencies': {'react-native': '0.79.0'}}))
        (self.bin / 'node').unlink()
        result = self.doctor('--fastlane-dir', 'apps/mobile/ios/fastlane')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Node', result.stderr)
        (app / 'package.json').unlink()
        (app / 'pubspec.yaml').write_text('name: demo\ndependencies:\n  flutter:\n    sdk: flutter\n')
        (self.bin / 'flutter').unlink()
        result = self.doctor('--fastlane-dir', 'apps/mobile/ios/fastlane')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Flutter', result.stderr)
        self.stub('flutter', fail_args=('--version',))
        result = self.doctor('--fastlane-dir', 'apps/mobile/ios/fastlane')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any(call['tool'] == 'flutter' for call in self.calls()))


if __name__ == '__main__':
    unittest.main()
