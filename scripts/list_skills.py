#!/usr/bin/env python3
"""List the current checkout's skill entrypoints without installing anything."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1],
                        help='collection checkout to inspect')
    parser.add_argument('--json', action='store_true', help='emit machine-readable paths')
    args = parser.parse_args()
    root = args.root.resolve()
    entries = []
    for entry in sorted((root / 'skills').glob('*/SKILL.md')):
        # Match check_collection.py's exclusions; cached copies are not skills.
        if entry.parent.name.startswith('.') or entry.parent.name in {'node_modules', '__pycache__', 'exports'}:
            continue
        folder = entry.parent.relative_to(root)
        entries.append({
            'name': entry.parent.name,
            'entrypoint': str(folder / 'SKILL.md'),
            'guide': str(folder / 'README.md'),
            'guide_zh': str(folder / 'README.zh-CN.md'),
            'doctor': str(folder / 'scripts/doctor.sh'),
        })
    if not entries:
        print('No skills discovered under {}'.format(root / 'skills'), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    else:
        for entry in entries:
            print('{}\n  Read: {}\n  Guide: {} | {}\n  Check: sh {}'.format(
                entry['name'], entry['entrypoint'], entry['guide'], entry['guide_zh'], entry['doctor']))
        print('\nPaths are relative to {}. Read the selected SKILL.md before choosing its workflow.'.format(root))
    return 0


if __name__ == '__main__':
    sys.exit(main())
