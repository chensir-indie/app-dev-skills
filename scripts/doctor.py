#!/usr/bin/env python3
"""Read-only collection preflight; skill-specific checks stay in each skill."""
import argparse
import importlib
from pathlib import Path
import shutil
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def collection_checks(run=subprocess.run, which=shutil.which, load=importlib.import_module):
    failures = []
    try:
        load('yaml')
        print('PASS: PyYAML imports in {}'.format(sys.executable), flush=True)
    except ImportError:
        requirements = ROOT / 'skills/image-to-layered-html-prototype/requirements.txt'
        failures.append('PyYAML is missing in {}. From {}, activate .venv, then run: python -m pip install -r {}'.format(sys.executable, ROOT, shlex.quote(str(requirements))))
    for name in ('node', 'npm'):
        executable = which(name)
        if not executable:
            failures.append('{} is missing. Install Node.js 22+ with npm: https://nodejs.org/en/download ; reopen the terminal.'.format(name))
            continue
        try:
            result = run([executable, '--version'], capture_output=True, text=True, timeout=10)
            version = result.stdout.strip()
            if result.returncode or not version:
                raise ValueError('version command failed')
            if name == 'node' and int(version.lstrip('v').split('.')[0]) < 22:
                failures.append('Node.js {} is too old; install Node.js 22+: https://nodejs.org/en/download'.format(version))
            else:
                print('PASS: {} {}'.format(name, version), flush=True)
        except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
            failures.append('{} cannot run ({}). Repair the installation and reopen the terminal.'.format(name, exc))
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=('all', 'collection'), default='all',
                        help='all: collection plus all skill runtimes; collection: metadata tooling only')
    args = parser.parse_args()
    print('Repository: {}\nWorking directory: {}'.format(ROOT, Path.cwd()), flush=True)
    print('Collection runtime: Python {}'.format(sys.version.split()[0]), flush=True)
    failures = collection_checks()
    if args.scope == 'all':
        # Match check_collection.py's exclusions; never execute cached copies.
        entries = [entry for entry in sorted((ROOT / 'skills').glob('*/SKILL.md'))
                   if not entry.parent.name.startswith('.')
                   and entry.parent.name not in {'node_modules', '__pycache__', 'exports'}]
        if not entries:
            failures.append('No skills discovered under {}/skills.'.format(ROOT))
        for skill_entry in entries:
            skill = skill_entry.parent.name
            print('\nChecking {}:'.format(skill), flush=True)
            entry = skill_entry.parent / 'scripts/doctor.sh'
            try:
                result = subprocess.run(['sh', str(entry)], cwd=str(entry.parent.parent), timeout=60)
                if result.returncode:
                    failures.append('{} preflight failed; follow its repair instructions above.'.format(skill))
            except (OSError, subprocess.TimeoutExpired) as exc:
                failures.append('{} preflight could not finish: {}'.format(skill, exc))
    for failure in failures:
        print('FAIL: ' + failure, file=sys.stderr)
    if failures:
        print('Fix the failed checks, rerun the same doctor command, then retry your task. Setup: docs/runtime.md', file=sys.stderr)
        return 1
    print('\nPASS: selected runtime checks. This does not validate artifacts or visual quality.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
