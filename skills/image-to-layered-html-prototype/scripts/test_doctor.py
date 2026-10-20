"""Runtime failures should explain a repair before any workflow is attempted."""
from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import doctor
import runtime_support

SCRIPTS = Path(__file__).resolve().parent


class DoctorTests(unittest.TestCase):
    def output(self, operation):
        stream = io.StringIO()
        with redirect_stdout(stream):
            result = operation()
        return result, stream.getvalue()

    def test_launcher_without_python_has_install_guidance(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run(['/bin/sh', str(SCRIPTS / 'doctor.sh')],
                                    env={**os.environ, 'PATH': folder}, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('https://www.python.org/downloads/', result.stderr)
        self.assertIn('doctor.sh', result.stderr)
        self.assertNotIn('not found', result.stderr)

    def test_launcher_rejects_old_python_and_tries_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'python3').write_text('#!/bin/sh\nexit 1\n')
            (root / 'python3').chmod(0o755)
            (root / 'python').symlink_to(sys.executable)
            result = subprocess.run(['/bin/sh', str(SCRIPTS / 'doctor.sh'), '--scope', 'unsupported'],
                                    env={**os.environ, 'PATH': folder}, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)

    def test_help_does_not_require_python(self):
        result = subprocess.run(['/bin/sh', str(SCRIPTS / 'doctor.sh'), '--help'],
                                env={**os.environ, 'PATH': ''}, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('--scope', result.stdout)

    def test_missing_python_packages_suggest_isolated_repair(self):
        with patch.object(doctor.importlib, 'import_module', side_effect=ImportError('missing test dependency')):
            ready, output = self.output(doctor.check_python)
        self.assertFalse(ready)
        self.assertIn('[missing] Pillow', output)
        self.assertIn('[missing] PyYAML', output)
        self.assertIn('-m venv .venv', output)
        self.assertIn('pip install -r requirements.txt', output)

    def test_python_scope_never_checks_browser(self):
        with patch.object(sys, 'argv', ['doctor.py', '--scope', 'python']), \
                patch.object(doctor, 'check_python', return_value=True), \
                patch.object(doctor, 'check_browser') as browser:
            status, output = self.output(doctor.main)
        self.assertEqual(status, 0)
        browser.assert_not_called()
        self.assertIn('Environment ready.', output)

    def test_all_scope_reports_browser_even_when_python_dependencies_fail(self):
        with patch.object(sys, 'argv', ['doctor.py']), \
                patch.object(doctor, 'check_python', return_value=False), \
                patch.object(doctor, 'check_browser', return_value=True) as browser:
            status, _ = self.output(doctor.main)
        self.assertEqual(status, 1)
        browser.assert_called_once_with()

    def test_direct_python_helper_rejects_old_runtime_before_importing_pillow(self):
        stream = io.StringIO()
        with patch.object(runtime_support.sys, 'version_info', (3, 8)), \
                patch.object(runtime_support.importlib, 'import_module') as importer, \
                redirect_stderr(stream), self.assertRaises(SystemExit) as raised:
            runtime_support.ensure_pillow()
        self.assertEqual(raised.exception.code, 2)
        importer.assert_not_called()
        self.assertIn('Python 3.9+', stream.getvalue())
        self.assertIn('doctor.sh', stream.getvalue())

    def test_missing_node_and_npm_returns_repair(self):
        with patch.object(doctor.shutil, 'which', return_value=None):
            ready, output = self.output(doctor.check_browser)
        self.assertFalse(ready)
        self.assertIn('Node.js 22+', output)
        self.assertIn('npm', output)
        self.assertIn('https://nodejs.org/en/download', output)
        self.assertIn('npm ci', output)

    def test_browser_launch_failure_is_not_reported_ready(self):
        results = [subprocess.CompletedProcess([], 0, 'v22.0.0\n', ''),
                   subprocess.CompletedProcess([], 0, '10.0.0\n', ''),
                   subprocess.CompletedProcess([], 1, '', 'Executable does not exist\nextra detail')]
        with patch.object(doctor.shutil, 'which', side_effect=lambda name: '/test/' + name), \
                patch.object(doctor, 'run_command', side_effect=results) as execute:
            ready, output = self.output(doctor.check_browser)
        self.assertFalse(ready)
        self.assertIn('Executable does not exist', output)
        self.assertIn('install chromium', output)
        source = execute.call_args_list[-1].args[0][-1]
        self.assertIn('chromium.launch', source)
        self.assertIn('PLAYWRIGHT_CHANNEL', source)

    def test_independent_skill_uses_own_install_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'standalone-skill'
            root.mkdir()
            with patch.object(doctor, 'SKILL_ROOT', root):
                _, output = self.output(doctor.repair_browser)
        self.assertIn('npm install', output)
        self.assertNotIn('npm ci', output)
        self.assertIn(str(root), output)

    def test_python_cli_without_site_packages_reports_doctor(self):
        result = subprocess.run([sys.executable, '-S', str(SCRIPTS / 'validate_prototype.py'), '--help'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Pillow', result.stderr)
        self.assertIn('doctor.sh', result.stderr)
        self.assertIn('--scope python', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    @unittest.skipUnless(shutil.which('node'), 'Node.js is unavailable in this Python-only runtime')
    def test_browser_cli_missing_module_reports_doctor(self):
        result = subprocess.run(['node', str(SCRIPTS / 'test_dom.cjs'), '/missing-playwright-for-test'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('doctor.sh', result.stderr)
        self.assertIn('--scope browser', result.stderr)
        self.assertNotIn('Require stack', result.stderr)

    @unittest.skipUnless(shutil.which('node'), 'Node.js is unavailable in this Python-only runtime')
    def test_browser_cli_launch_failure_reports_doctor(self):
        with tempfile.TemporaryDirectory() as folder:
            module = Path(folder) / 'browser.cjs'
            module.write_text("module.exports={chromium:{launch:async()=>{throw new Error('Missing browser binary')}}};\n")
            result = subprocess.run(['node', str(SCRIPTS / 'test_dom.cjs'), str(module)],
                                    text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Missing browser binary', result.stderr)
        self.assertIn('doctor.sh', result.stderr)
        self.assertNotIn('at Object.', result.stderr)


if __name__ == '__main__':
    unittest.main()
