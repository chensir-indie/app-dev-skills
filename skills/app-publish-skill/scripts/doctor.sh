#!/bin/sh
# Read-only readiness checks. Never loads environment files or store credentials.
set -eu
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'FAIL: Python 3.9+ is required. Install Python from https://www.python.org/downloads/ and reopen the terminal.' >&2
  exit 1
fi
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then
  printf '%s\n' 'FAIL: Python is older than 3.9 or cannot run. Select Python 3.9+ and rerun this doctor.' >&2
  exit 1
fi
script_dir=${0%/*}
python3 - "$script_dir" "$@" <<'PY'
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description='Read-only skill readiness; not an app release preflight.')
parser.add_argument('script_dir')
parser.add_argument('--project', type=Path)
parser.add_argument('--fastlane-dir', type=Path, help='Directory containing Fastfile, relative to the project root or absolute.')
parser.add_argument('--platform', choices=('ios', 'android'), help='Check only the selected platform; default checks detected platforms.')
parser.add_argument('--timeout-seconds', type=float, default=15, help='Maximum time for each read-only tool check (default: 15).')
args = parser.parse_args()
if args.timeout_seconds <= 0:
    parser.error('--timeout-seconds must be positive')
if args.project is None and (args.fastlane_dir is not None or args.platform is not None):
    parser.error('--fastlane-dir and --platform require --project')
root = Path(args.script_dir).resolve().parent
failures = []
for relative in ('SKILL.md', 'LICENSE', 'README.md', 'README.zh-CN.md',
                 'agents/openai.yaml', 'scripts/release_evidence.py',
                 'references/fastlane-build-testflight.md',
                 'references/fastlane-setup.md',
                 'references/metadata-screenshots.md',
                 'references/acceptance-review-android.md',
                 'references/evidence-contract.md',
                 'references/workspace-adapters.md'):
    path = root / relative
    try:
        path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        failures.append(f'Missing or unreadable package resource {relative}; restore the complete skill folder.')
print(f'PASS: Python {sys.version.split()[0]}; offline helpers use only the standard library.')


def run_check(command, label, cwd, env):
    if shutil.which(command[0]) is None:
        failures.append(f'{label} executable is unavailable. See references/fastlane-setup.md to activate or install the project toolchain.')
        return None
    try:
        result = subprocess.run(command, cwd=str(cwd), env=env, capture_output=True,
                                text=True, timeout=args.timeout_seconds)
    except subprocess.TimeoutExpired:
        failures.append(f'{label} timed out; repair the selected toolchain. See references/fastlane-setup.md.')
        return None
    except OSError:
        failures.append(f'{label} cannot run; repair the selected toolchain. See references/fastlane-setup.md.')
        return None
    if result.returncode:
        failures.append(f'{label} failed; activate the project-pinned Ruby/tools and repair missing dependencies using references/fastlane-setup.md. No installation was attempted.')
        return None
    return result.stdout + '\n' + result.stderr


def version_check(command, label, pattern, cwd, env):
    output = run_check(command, label, cwd, env)
    if output is None:
        return False
    match = re.search(pattern, output, re.I | re.M)
    if not match:
        failures.append(f'{label} did not report a recognizable version; inspect the selected executable locally.')
        return False
    print(f'PASS: {label} {match.group(1)}')
    return match.group(1)


def nearest_gemfile(adapter, project):
    current = adapter.parent
    while True:
        candidate = current / 'Gemfile'
        if candidate.is_file():
            return candidate
        if current == project:
            return None
        current = current.parent


if args.project is not None:
    project = args.project.resolve()
    if not project.is_dir():
        failures.append('Project directory does not exist; pass the app repository root.')
    else:
        if args.fastlane_dir is not None:
            selected = args.fastlane_dir
            selected = (project / selected).resolve() if not selected.is_absolute() else selected.resolve()
            if project not in selected.parents or not (selected / 'Fastfile').is_file():
                failures.append('--fastlane-dir must be inside the project and contain Fastfile.')
                adapters = []
            else:
                adapters = [selected]
        else:
            adapters = [project / relative for relative in ('fastlane', 'ios/fastlane', 'android/fastlane')
                        if (project / relative / 'Fastfile').is_file()]
            if args.platform is not None:
                adapters = [adapter for adapter in adapters
                            if adapter.parent == project or adapter.parent.name == args.platform]
            paired = [adapter for adapter in adapters if nearest_gemfile(adapter, project) is not None]
            adapters = paired or adapters
        if len(adapters) > 1:
            failures.append('Multiple Fastlane adapters match; select the directory containing Fastfile with --fastlane-dir.')
        elif not adapters:
            failures.append('No matching Fastfile found in root/ios/android; inspect the actual entrypoint or use --fastlane-dir. See references/fastlane-setup.md.')
        else:
            adapter = adapters[0]
            env = {**os.environ, 'FASTLANE_SKIP_UPDATE_CHECK': '1', 'FASTLANE_HIDE_CHANGELOG': '1',
                   'FASTLANE_OPT_OUT_USAGE': '1', 'FASTLANE_DISABLE_COLORS': '1',
                   'BUNDLE_AUTO_INSTALL': 'false', 'BUNDLE_VERSION': 'system', 'BUNDLE_FROZEN': 'true'}
            print('PASS: Fastfile entrypoint selected; only tool version/dependency checks will run, no lane.')
            gemfile = nearest_gemfile(adapter, project)
            if gemfile is None:
                # A standalone diagnostic must not activate another project's bundle.
                for key in list(env):
                    if key.startswith(('BUNDLE_', 'BUNDLER_')):
                        del env[key]
                if 'bundler' in env.get('RUBYOPT', '').lower():
                    env.pop('RUBYOPT', None)
            ruby_ok = version_check(['ruby', '--version'], 'Ruby', r'^ruby\s+(\d+(?:\.\d+)+)', adapter.parent, env)
            if gemfile is not None:
                lockfile = gemfile.with_name('Gemfile.lock')
                try:
                    lock = lockfile.read_text(encoding='utf-8')
                except (OSError, UnicodeError):
                    lock = ''
                locked = re.search(r'^BUNDLED WITH\s*\n[ \t]+(\d+(?:\.\d+)+)[ \t]*$', lock, re.M)
                if not locked:
                    failures.append('Gemfile.lock or its BUNDLED WITH version is missing; complete the project setup before this read-only check. See references/fastlane-setup.md.')
                elif ruby_ok:
                    bundler = locked.group(1)
                    env.update({'BUNDLE_GEMFILE': str(gemfile), 'BUNDLER_VERSION': bundler})
                    prefix = ['bundle', '_' + bundler + '_']
                    installed = version_check(prefix + ['--version'], 'Bundler', r'^Bundler version\s+(\d+(?:\.\d+)+)', gemfile.parent, env)
                    if installed and installed != bundler:
                        failures.append('Bundler version differs from Gemfile.lock BUNDLED WITH; activate the exact locked version. See references/fastlane-setup.md.')
                    elif installed:
                        # Local Bundler configuration outranks environment flags. Query only
                        # safety booleans before any command that could install or rewrite locks.
                        probe = '''gem "bundler", ARGV.fetch(0)
require "bundler"
puts JSON.generate({auto_install: !!Bundler.settings[:auto_install], frozen: !!Bundler.frozen_bundle?, version_safe: ["system", ARGV.fetch(0)].include?(Bundler.settings[:version].to_s)})'''
                        output = run_check(['ruby', '-rjson', '-e', probe, bundler], 'Bundler settings safety check', gemfile.parent, env)
                        try:
                            settings = json.loads(output) if output is not None else None
                        except ValueError:
                            settings = None
                        if settings != {'auto_install': False, 'frozen': True, 'version_safe': True}:
                            failures.append('Bundler settings do not guarantee frozen/no-auto-install execution; correct the existing configuration using references/fastlane-setup.md. No dependency or Fastlane command was run.')
                        elif run_check(prefix + ['check', '--dry-run'], 'bundle check --dry-run', gemfile.parent, env) is not None:
                            print('PASS: locked bundle dependencies are locally available (frozen, dry-run).')
                            version_check(prefix + ['exec', 'fastlane', '--version'], 'Fastlane (project bundle)',
                                          r'^fastlane\s+(\d+(?:\.\d+)+)', adapter.parent, env)
            else:
                print('WARN: No ancestor Gemfile; checking the existing standalone Fastlane. Its version is not project-locked; see references/fastlane-setup.md.')
                if ruby_ok:
                    version_check(['fastlane', '--version'], 'Fastlane (standalone)', r'^fastlane\s+(\d+(?:\.\d+)+)', adapter.parent, env)

            framework_bases = []
            current = adapter.parent
            while True:
                framework_bases.append(current)
                if current == project:
                    break
                current = current.parent
            bases = set(framework_bases)
            bases.update(base / platform for base in framework_bases for platform in ('ios', 'android')
                         if (base / platform).is_dir())
            ios = any(list(base.glob('*.xcodeproj')) or list(base.glob('*.xcworkspace')) for base in bases) or (project / 'ios').is_dir()
            android = (project / 'android').is_dir() or any(any((base / name).is_file() for name in ('build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts')) for base in bases)
            if args.platform == 'ios' or (args.platform is None and ios):
                version_check(['xcodebuild', '-version'], 'Xcode', r'^Xcode\s+(\d+(?:\.\d+)+)', adapter.parent, env)
            if args.platform == 'android' or (args.platform is None and android):
                version_check(['java', '-version'], 'Java', r'(?:openjdk|java) version\s+"(\d+(?:\.\d+)+)', adapter.parent, env)
                if not any((base / 'gradlew').is_file() for base in bases):
                    failures.append('Android gradlew is missing; restore the project Gradle wrapper. It was not executed or downloaded.')
                else:
                    print('PASS: Android gradlew is present; Gradle execution/download was not attempted.')
            for base in framework_bases:
                pubspec = base / 'pubspec.yaml'
                if pubspec.is_file():
                    try:
                        is_flutter = re.search(r'^\s*flutter:\s*$', pubspec.read_text(encoding='utf-8'), re.M)
                    except (OSError, UnicodeError):
                        failures.append('pubspec.yaml is unreadable; inspect the app checkout.')
                        is_flutter = False
                    if is_flutter:
                        if shutil.which('flutter') is None:
                            failures.append('Flutter executable is unavailable; activate the app-pinned SDK using references/fastlane-setup.md.')
                        else:
                            print('PASS: Flutter executable is present; SDK bootstrap/version checks belong to project preflight, not this read-only doctor.')
                    break
            for base in framework_bases:
                package = base / 'package.json'
                if not package.is_file():
                    continue
                try:
                    config = json.loads(package.read_text(encoding='utf-8'))
                    dependencies = {**config.get('dependencies', {}), **config.get('devDependencies', {})}
                except (OSError, UnicodeError, ValueError, TypeError, AttributeError):
                    failures.append('package.json is unreadable or invalid; inspect the selected app project.')
                    continue
                if 'react-native' in dependencies or 'expo' in dependencies:
                    version_check(['node', '--version'], 'Node (React Native/Expo)', r'^v(\d+(?:\.\d+)+)', base, env)
                    managers = [name for name, filename in (('npm', 'package-lock.json'), ('yarn', 'yarn.lock'), ('pnpm', 'pnpm-lock.yaml'), ('bun', 'bun.lock'), ('bun', 'bun.lockb')) if (base / filename).is_file()]
                    if len(set(managers)) != 1:
                        print('WARN: React Native/Expo package-manager lock is missing or ambiguous; inspect packageManager and project setup before building.')
                    elif shutil.which(managers[0]) is None:
                        print('WARN: React Native/Expo lockfile package manager is unavailable; activate the project-pinned package manager before building.')
                break
            print('Tool checks do not verify signing, source sync, policies, store baseline, credentials, device behavior or publication authority.')
for failure in failures:
    print('FAIL: ' + failure, file=sys.stderr)
if failures:
    sys.exit(1)
print('PASS: selected readiness checks only. Run the app-owned release preflight before any build/upload.')
PY
