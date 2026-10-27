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
        (self.skill / 'scripts').mkdir()
        (self.skill / 'scripts/doctor.sh').write_text('#!/bin/sh\nexit 0\n')
        (self.skill / 'agents').mkdir()
        (self.skill / 'agents/openai.yaml').write_text('interface:\n  display_name: "Example"\n  short_description: "A reusable example workflow skill"\n  default_prompt: "Use $example for this task."\n')
        for name in ('README.md', 'README.zh-CN.md'):
            (self.root / name).write_text('[Example](skills/example/SKILL.md)\n')
            (self.skill / name).write_text('[Workflow](SKILL.md)\n')

    def test_standalone_skill_passes(self):
        self.assertEqual(checker.check(self.root), [])

    def test_standalone_skill_does_not_require_readmes(self):
        for name in ('README.md', 'README.zh-CN.md'):
            (self.skill / name).unlink()
        self.assertEqual(checker.check(self.root), [])

    def test_collection_still_requires_both_readmes(self):
        for name in ('README.md', 'README.zh-CN.md'):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text()
                path.unlink()
                self.assertTrue(any(f'{name}: missing collection README' in e for e in checker.check(self.root)))
                path.write_text(original)

    def test_broken_relative_link_fails(self):
        (self.skill / 'guide.md').unlink()
        self.assertTrue(any('broken link' in e for e in checker.check(self.root)))

    def test_missing_runtime_preflight_fails(self):
        (self.skill / 'scripts/doctor.sh').unlink()
        self.assertTrue(any('runtime preflight' in e for e in checker.check(self.root)))

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

    def test_unregistered_skill_is_not_discoverable_from_both_readmes(self):
        (self.root / 'README.zh-CN.md').write_text('[Guide](skills/example/README.md)\n')
        self.assertTrue(any('README.zh-CN.md' in e and 'SKILL.md' in e for e in checker.check(self.root)))

    def test_required_standalone_files_are_checked_individually(self):
        for name in ('LICENSE', 'scripts/doctor.sh'):
            with self.subTest(name=name):
                path = self.skill / name
                original = path.read_text()
                path.unlink()
                self.assertTrue(any(name in e for e in checker.check(self.root)))
                path.write_text(original)

    def test_orphan_skill_directory_fails_discovery(self):
        (self.root / 'skills/unregistered').mkdir()
        self.assertTrue(any('unregistered' in e and 'SKILL.md' in e for e in checker.check(self.root)))

    def test_invalid_slug_and_duplicate_name_are_reported(self):
        other = self.root / 'skills/Other_skill'
        other.mkdir()
        (other / 'SKILL.md').write_text('---\nname: example\ndescription: Another workflow\n---\n')
        errors = checker.check(self.root)
        self.assertTrue(any('invalid skill directory' in e for e in errors))
        self.assertTrue(any('duplicate skill name' in e for e in errors))

    def test_frontmatter_requires_string_fields_and_unique_yaml_keys(self):
        for header in ('name: 12\ndescription: Example',
                       'name: example\ndescription: [Example]',
                       'name: example\nname: other\ndescription: Example'):
            with self.subTest(header=header):
                (self.skill / 'SKILL.md').write_text('---\n' + header + '\n---\n')
                errors = checker.check(self.root)
                self.assertTrue(any('frontmatter' in e or 'name mismatch' in e or 'description' in e for e in errors))

    def test_metadata_wrong_types_and_partial_invocations_do_not_crash_or_pass(self):
        cases = (
            'interface: []\n',
            'interface:\n  display_name: 123\n  short_description: "A reusable example workflow skill"\n  default_prompt: "Use $example"\n',
            'interface:\n  display_name: Example\n  short_description: 123\n  default_prompt: "Use $example"\n',
            'interface:\n  display_name: Example\n  short_description: "                         "\n  default_prompt: "Use $example"\n',
            'interface:\n  display_name: Example\n  short_description: "A reusable example workflow skill"\n  default_prompt: 123\n',
            'interface:\n  display_name: Example\n  short_description: "A reusable example workflow skill"\n  default_prompt: "Use $example-extra"\n',
        )
        for source in cases:
            with self.subTest(source=source):
                (self.skill / 'agents/openai.yaml').write_text(source)
                self.assertTrue(any('invocation metadata' in e for e in checker.check(self.root)))

    def test_broken_anchor_is_reported_for_same_and_other_markdown_files(self):
        (self.skill / 'guide.md').write_text('# Guide\n[Here](#missing)\n')
        (self.skill / 'README.md').write_text('[Guide](guide.md#absent)\n')
        errors = checker.check(self.root)
        self.assertEqual(sum('broken fragment' in e for e in errors), 2)

    def test_reference_links_and_encoded_angle_bracket_paths_are_checked(self):
        (self.skill / 'guide file.md').write_text('# API &amp; Design\n\n# API &amp; Design\n\n## 中文：环境检查\n')
        (self.skill / 'guide.md').write_text(
            '[First][guide]\n[Second](guide%20file.md#api--design-1)\n'
            '[中文](<guide file.md#中文环境检查>)\n'
            '[guide]: <guide file.md#api--design> "Reference guide"\n')
        self.assertEqual(checker.check(self.root), [])
        (self.skill / 'guide file.md').unlink()
        self.assertEqual(sum('broken link' in e for e in checker.check(self.root)), 3)

    def test_reference_link_cannot_hide_an_outside_skill_dependency(self):
        (self.skill / 'guide.md').write_text('[Outside][ref]\n\n[ref]: ../../README.md\n')
        self.assertTrue(any('outside skill' in e for e in checker.check(self.root)))

    def test_code_examples_do_not_add_links_or_real_heading_fragments(self):
        (self.skill / 'guide.md').write_text(
            '# Real\n\n```md\n# Fake\n[Not a link](missing.md)\n```\n'
            '~~~md\n[Also not a link](absent.md)\n~~~\n'
            '`[Inline example](gone.md)`\n[Real](#real)\n')
        self.assertEqual(checker.check(self.root), [])
        with (self.skill / 'guide.md').open('a') as doc:
            doc.write('[Bad](#fake)\n')
        self.assertTrue(any('broken fragment' in e for e in checker.check(self.root)))

    def test_setext_headings_and_explicit_html_ids_are_resolved(self):
        (self.skill / 'guide.md').write_text(
            'Named section\n=============\n\n<a id="manual-anchor"></a>\n'
            '[Heading](#named-section) [Manual](#manual-anchor)\n')
        self.assertEqual(checker.check(self.root), [])

    def test_readme_registration_uses_real_links_and_accepts_reference_links(self):
        (self.root / 'README.md').write_text(
            '[Example][entry]\n\n[entry]: skills/example/SKILL.md\n')
        self.assertEqual(checker.check(self.root), [])
        (self.root / 'README.md').write_text('```md\n[Example](skills/example/SKILL.md)\n```\n')
        self.assertTrue(any('README.md: missing direct skill entry' in e for e in checker.check(self.root)))

    def test_failures_accumulate_across_frontmatter_metadata_and_navigation(self):
        (self.skill / 'SKILL.md').write_text('---\nname: [broken\n---\n[Guide](gone.md)\n')
        (self.skill / 'agents/openai.yaml').write_text('interface: [broken\n')
        errors = checker.check(self.root)
        for finding in ('invalid frontmatter', 'invalid invocation metadata', 'broken link gone.md'):
            self.assertTrue(any(finding in error for error in errors))

    def test_heading_formatting_and_slug_collisions_are_resolved(self):
        (self.skill / 'guide.md').write_text(
            '# Work *now* with `API`\n# foo\n# foo\n# foo-1\n'
            '[Formatted](#work-now-with-api) [Duplicate](#foo-1) [Collision](#foo-1-1)\n')
        self.assertEqual(checker.check(self.root), [])

    def test_balanced_parentheses_in_local_filenames_and_link_titles(self):
        (self.skill / 'guide (copy).md').write_text('# Copied\n')
        (self.skill / 'guide.md').write_text('[Copy](guide%20(copy).md#copied "Copy guide")\n')
        self.assertEqual(checker.check(self.root), [])
        (self.skill / 'guide (copy).md').unlink()
        self.assertTrue(any('broken link' in e for e in checker.check(self.root)))

    def test_yaml_frontmatter_does_not_create_a_setext_heading(self):
        with (self.skill / 'guide.md').open('w') as doc:
            doc.write('---\ntitle: Metadata\n---\n\n# Visible\n[Wrong](#title-metadata)\n')
        self.assertTrue(any('broken fragment' in e for e in checker.check(self.root)))


if __name__ == '__main__':
    unittest.main()
