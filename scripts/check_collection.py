#!/usr/bin/env python3
"""Check skill discovery, portable local links and invocation metadata.

This is a packaging check, not a secrets scanner or visual-quality review.
"""
import re
import sys
from pathlib import Path

import yaml

IGNORED = {'node_modules', '.git', '.venv', '__pycache__', 'exports', '.test-output'}


def documents(root):
    for path in root.rglob('*.md'):
        if not IGNORED.intersection(path.relative_to(root).parts):
            yield path


def check(root):
    root = Path(root).resolve()
    errors = []
    entries = sorted((root / 'skills').glob('*/SKILL.md'))
    if not entries:
        errors.append('No skills discovered')
    for entry in entries:
        skill = entry.parent
        try:
            match = re.match(r'^---\r?\n(.*?)\r?\n---', entry.read_text(), re.S)
            header = yaml.safe_load(match.group(1)) if match else {}
            if not isinstance(header, dict) or header.get('name') != skill.name:
                errors.append(f'{skill.name}: name mismatch')
            if not isinstance(header, dict) or not isinstance(header.get('description'), str) or not header['description'].strip():
                errors.append(f'{skill.name}: missing description')
            metadata = yaml.safe_load((skill / 'agents/openai.yaml').read_text())['interface']
            if not (metadata.get('display_name') and
                    25 <= len(metadata.get('short_description', '')) <= 64 and
                    '$' + skill.name in metadata.get('default_prompt', '')):
                errors.append(f'{skill.name}: invalid invocation metadata')
        except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
            errors.append(f'{skill.name}: invalid invocation metadata/frontmatter: {exc}')
        if not (skill / 'LICENSE').is_file():
            errors.append(f'{skill.name}: missing standalone LICENSE')
    for doc in documents(root):
        text = doc.read_text()
        if re.search(r'/(?:Users|home)/[\w.-]+/', text):
            errors.append(f'{doc.relative_to(root)}: private absolute path')
        owner = next((entry.parent for entry in entries if entry.parent in doc.parents), None)
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'^[a-z][a-z0-9+.-]*:', link, re.I) or link.startswith('#'):
                continue
            target = (doc.parent / link.split('#')[0]).resolve()
            if not target.exists():
                errors.append(f'{doc.relative_to(root)}: broken link {link}')
            if owner and target != owner and owner not in target.parents:
                errors.append(f'{doc.relative_to(root)}: link outside skill {link}')
    return errors


if __name__ == '__main__':
    findings = check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
    if findings:
        print('\n'.join(findings), file=sys.stderr)
        sys.exit(1)
    print('Skill discovery, metadata, standalone links and documentation paths: PASS')
