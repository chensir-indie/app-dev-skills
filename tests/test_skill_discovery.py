"""Discovery follows the checkout, including newly added or renamed skills."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('collection_doctor_discovery', ROOT / 'scripts/doctor.py')
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


class SkillDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'scripts').mkdir()
        self.skill = self.root / 'skills/new-workflow'
        (self.skill / 'scripts').mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: new-workflow\ndescription: Fixture\n---\n# Fixture\n')
        (self.skill / 'scripts/doctor.sh').write_text('printf "fixture preflight: %s\\n" "$1"\n')

    def test_shell_dispatches_discovered_skill_without_python(self):
        shell = self.root / 'scripts/doctor.sh'
        shutil.copy(ROOT / 'scripts/doctor.sh', shell)
        result = subprocess.run(['/bin/sh', str(shell), '--skill', 'new-workflow', 'proof'],
                                env={**os.environ, 'PATH': ''}, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('fixture preflight: proof', result.stdout)

    def test_all_scope_uses_current_skill_entries(self):
        with patch.object(doctor, 'ROOT', self.root), patch.object(doctor, 'collection_checks', return_value=[]), \
             patch.object(sys, 'argv', ['doctor.py']), patch.object(doctor.subprocess, 'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(doctor.main(), 0)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0], ['sh', str(self.skill / 'scripts/doctor.sh')])

    def test_catalog_json_uses_live_names_and_relative_paths(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/list_skills.py'), '--root', str(self.root), '--json'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(result.stdout)
        self.assertEqual([entry['name'] for entry in entries], ['new-workflow'])
        self.assertEqual(entries[0]['entrypoint'], 'skills/new-workflow/SKILL.md')
        self.assertEqual(entries[0]['doctor'], 'skills/new-workflow/scripts/doctor.sh')

    def test_catalog_fails_instead_of_reporting_an_empty_success(self):
        shutil.rmtree(self.root / 'skills')
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/list_skills.py'), '--root', str(self.root)],
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No skills', result.stderr)

    def test_catalog_and_doctor_ignore_cached_or_hidden_skill_copies(self):
        for name in ('.test-output', '.draft', 'node_modules', 'exports', '__pycache__'):
            cached = self.root / 'skills' / name
            cached.mkdir()
            (cached / 'SKILL.md').write_text('Cached copy, not an installed skill\n')
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/list_skills.py'),
                                 '--root', str(self.root), '--json'],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([entry['name'] for entry in json.loads(result.stdout)], ['new-workflow'])
        with patch.object(doctor, 'ROOT', self.root), patch.object(doctor, 'collection_checks', return_value=[]), \
             patch.object(sys, 'argv', ['doctor.py']), patch.object(doctor.subprocess, 'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(doctor.main(), 0)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0], ['sh', str(self.skill / 'scripts/doctor.sh')])


if __name__ == '__main__':
    unittest.main()
