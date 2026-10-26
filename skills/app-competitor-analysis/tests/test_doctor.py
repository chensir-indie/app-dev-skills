"""Exercise interpreter discovery and early failure without modifying the host."""
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCTOR = ROOT / 'scripts/doctor.sh'


@unittest.skipUnless(Path('/bin/sh').exists(), 'doctor.sh needs a POSIX shell')
class DoctorTests(unittest.TestCase):
    def old_python(self, path):
        path.write_text(
            '#!/bin/sh\nexec ' + shlex.quote(sys.executable) +
            ' -c \'import sys; sys.version_info = (3, 8, 0); exec(sys.argv[1])\' "$2"\n'
        )
        path.chmod(0o755)

    def run_doctor(self, path):
        return subprocess.run(
            ['/bin/sh', str(DOCTOR)], cwd=path,
            env={**os.environ, 'PATH': str(path)},
            text=True, capture_output=True, check=False,
        )

    def test_missing_python_has_install_and_retry_guidance(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_doctor(folder)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing from PATH', result.stderr)
        self.assertIn('https://www.python.org/downloads/', result.stderr)
        self.assertIn('sh scripts/doctor.sh', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_unsupported_python_fails_without_claiming_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            binary = Path(folder) / 'python3'
            self.old_python(binary)
            result = self.run_doctor(folder)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no Python 3.9+ interpreter could run', result.stderr)
        self.assertNotIn('[ok]', result.stdout)

    def test_python_fallback_is_usable_after_an_unsupported_python3(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            unsupported = path / 'python3'
            self.old_python(unsupported)
            (path / 'python').symlink_to(sys.executable)
            result = self.run_doctor(folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Use python for the helpers.', result.stdout)
        self.assertEqual(result.stderr, '')

    def test_compatible_python3_succeeds_without_node_or_pip(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'python3').symlink_to(sys.executable)
            result = self.run_doctor(folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Use python3 for the helpers.', result.stdout)

    def test_public_helpers_reject_old_python_before_loading_dependencies(self):
        for name in ('audit_evidence.py', 'audit_acquisition.py', 'render_reports.py'):
            with self.subTest(name=name):
                script = ROOT / 'scripts' / name
                result = subprocess.run(
                    [sys.executable, '-c',
                     'import runpy, sys; sys.version_info = (3, 8, 0); '
                     'runpy.run_path(sys.argv[1], run_name="__main__")', str(script)],
                    text=True, capture_output=True, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Python 3.9+ is required', result.stderr)
                self.assertIn('doctor.sh', result.stderr)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
