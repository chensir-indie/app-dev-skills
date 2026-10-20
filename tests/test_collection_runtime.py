"""Exercise collection runtime diagnosis without changing the host installation."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('doctor', ROOT / 'scripts/doctor.py')
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


class DoctorTests(unittest.TestCase):
    def test_missing_packages_and_tools_accumulate_repairs(self):
        def missing(_):
            raise ImportError('no yaml')
        errors = doctor.collection_checks(which=lambda _: None, load=missing)
        self.assertEqual(len(errors), 3)
        self.assertIn('pip install -r', errors[0])
        self.assertTrue(all('https://nodejs.org/' in error for error in errors[1:]))

    def test_old_node_and_failed_npm_are_failures(self):
        runner = Mock(side_effect=[subprocess.CompletedProcess([], 0, 'v20.1.0\n', ''),
                                   subprocess.CompletedProcess([], 1, '', 'broken')])
        errors = doctor.collection_checks(run=runner, which=lambda name: name, load=lambda _: None)
        self.assertEqual(len(errors), 2)
        self.assertIn('too old', errors[0])
        self.assertIn('cannot run', errors[1])

    def test_shell_bootstrap_handles_absent_python(self):
        with tempfile.TemporaryDirectory() as folder:
            for command in ('dirname',):
                os.symlink('/usr/bin/' + command, str(Path(folder) / command))
            result = subprocess.run(['/bin/sh', str(ROOT / 'scripts/doctor.sh')],
                                    env={**os.environ, 'PATH': folder}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Python 3.9+', result.stderr)
        self.assertIn('python.org', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_unknown_skill_is_usage_error(self):
        result = subprocess.run(['sh', str(ROOT / 'scripts/doctor.sh'), '--skill', '../wrong'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
