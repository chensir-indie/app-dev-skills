import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_collection.py'
spec = importlib.util.spec_from_file_location('check_collection', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'skills/example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\ndescription: Example workflow\n---\n[Guide](guide.md)\n')
        (self.skill / 'guide.md').write_text('Original guidance\n')
        (self.skill / 'LICENSE').write_text('MIT\n')
        (self.skill / 'agents').mkdir()
        (self.skill / 'agents/openai.yaml').write_text('interface:\n  display_name: "Example"\n  short_description: "A reusable example workflow skill"\n  default_prompt: "Use $example for this task."\n')

    def test_standalone_skill_passes(self):
        self.assertEqual(checker.check(self.root), [])

    def test_broken_relative_link_fails(self):
        (self.skill / 'guide.md').unlink()
        self.assertTrue(any('broken link' in e for e in checker.check(self.root)))

    def test_dependency_on_another_skill_is_not_standalone(self):
        (self.skill / 'guide.md').write_text('[Other](../../README.md)')
        (self.root / 'README.md').write_text('Collection')
        self.assertTrue(any('outside skill' in e for e in checker.check(self.root)))

    def test_private_path_and_name_mismatch_fail(self):
        (self.skill / 'SKILL.md').write_text('---\nname: wrong\ndescription: Example\n---\n/Users/private/project\n')
        errors = checker.check(self.root)
        self.assertTrue(any('name mismatch' in e for e in errors))
        self.assertTrue(any('private absolute path' in e for e in errors))

    def test_invalid_invocation_fails(self):
        (self.skill / 'agents/openai.yaml').write_text('interface:\n  default_prompt: "Use $wrong"\n')
        self.assertTrue(any('invocation metadata' in e for e in checker.check(self.root)))


if __name__ == '__main__':
    unittest.main()
