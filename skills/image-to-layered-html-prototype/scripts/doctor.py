#!/usr/bin/env python3
"""Read-only runtime checks. The shell launcher also handles missing Python."""
import argparse
import importlib
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys

SKILL_ROOT = Path(__file__).resolve().parent.parent


def command(*parts):
    return ' '.join(shlex.quote(str(part)) for part in parts)


def repair_python():
    print('  From: ' + str(SKILL_ROOT))
    print('  ' + command('cd', SKILL_ROOT))
    if sys.prefix == sys.base_prefix:
        print('  ' + command(sys.executable, '-m', 'venv', '.venv'))
        print('  . .venv/bin/activate  # PowerShell: .venv\\Scripts\\Activate.ps1')
    print('  python -m pip install -r requirements.txt')


def repair_browser():
    repo_root = SKILL_ROOT.parent.parent
    repository = (repo_root / 'package-lock.json').is_file() and (repo_root / 'skills').is_dir()
    install_root = repo_root if repository else SKILL_ROOT
    print('  From: ' + str(install_root))
    print('  ' + command('cd', install_root))
    print('  ' + ('npm ci  # repository checkout' if repository else 'npm install  # independently installed skill'))
    print('  ' + command('cd', SKILL_ROOT))
    print('  npx --no-install playwright install chromium')
    print('  Linux shared libraries: npx --no-install playwright install --with-deps chromium')
    print('  Installed Chrome alternative: PLAYWRIGHT_CHANNEL=chrome sh scripts/doctor.sh --scope browser')


def check_python():
    print('[ok] Python ' + platform.python_version() + ' (' + sys.executable + ')')
    missing = False
    for module, package in [('PIL.Image', 'Pillow'), ('yaml', 'PyYAML')]:
        try:
            imported = importlib.import_module(module)
            if module == 'PIL.Image':
                imported.new('RGB', (1, 1)).close()
            else:
                imported.safe_load('doctor: true')
            print('[ok] ' + package + ' import and basic operation')
        except (ImportError, OSError, AttributeError, ValueError) as exc:
            print('[missing] ' + package + ': ' + str(exc).splitlines()[0])
            missing = True
    if missing:
        repair_python()
    return not missing


def run_command(args, timeout=10):
    try:
        return subprocess.run(args, cwd=SKILL_ROOT, text=True, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print('[missing] ' + args[0] + ': ' + str(exc).splitlines()[0])
        return None


def check_browser():
    ready = True
    node = shutil.which('node')
    if not node:
        print('[missing] Node.js 22+. Install the current LTS from https://nodejs.org/en/download')
        ready = False
    else:
        result = run_command([node, '--version'])
        try:
            supported = result is not None and result.returncode == 0 and int(result.stdout.strip().lstrip('v').split('.')[0]) >= 22
        except ValueError:
            supported = False
        if not supported:
            print('[missing] Node.js 22+. Upgrade from https://nodejs.org/en/download')
            ready = False
        else:
            print('[ok] Node.js ' + result.stdout.strip())
    npm = shutil.which('npm')
    npm_result = run_command([npm, '--version']) if npm else None
    if npm_result is None or npm_result.returncode != 0:
        print('[missing] npm. Reinstall Node.js with npm from https://nodejs.org/en/download')
        ready = False
    else:
        print('[ok] npm ' + npm_result.stdout.strip())
    if ready:
        # Resolve from this skill, so a repository workspace and independent installation both work.
        source = """
(async () => {
  const {chromium} = require('playwright');
  const browser = await chromium.launch({headless:true, timeout:15000,
    channel:process.env.PLAYWRIGHT_CHANNEL || undefined});
  try {
    const page = await browser.newPage();
    await page.setContent('<h1>runtime-ready</h1>');
    if (await page.locator('h1').innerText() !== 'runtime-ready') throw new Error('Browser page check failed');
    console.log('Playwright browser ' + browser.version() + ' (' + (process.env.PLAYWRIGHT_CHANNEL || 'chromium') + ')');
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode=1; });
"""
        result = run_command([node, '-e', source], timeout=35)
        if result is not None and result.returncode == 0:
            print('[ok] ' + result.stdout.strip())
        else:
            print('[missing] Playwright module or runnable browser')
            if result is not None:
                detail = (result.stderr or result.stdout).strip().splitlines()
                if detail:
                    print('  ' + detail[0])
            ready = False
    if not ready:
        repair_browser()
    return ready


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['python', 'browser', 'all'], default='all')
    args = parser.parse_args()
    if sys.version_info < (3, 9):
        print('[missing] Python 3.9+. Install from https://www.python.org/downloads/')
        return 1
    print('Skill: ' + str(SKILL_ROOT))
    print('Working directory: ' + os.getcwd())
    checks = []
    if args.scope in ('python', 'all'):
        checks.append(check_python())
    if args.scope in ('browser', 'all'):
        checks.append(check_browser())
    if platform.system() == 'Darwin' and shutil.which('swift'):
        print('[optional] Swift available for Apple Vision OCR; core checks do not require it')
    else:
        print('[optional] Swift/Vision OCR unavailable; pixel-core measurement remains supported')
    print('Environment ready.' if all(checks) else 'Environment incomplete. Apply the relevant repair, then rerun this check.')
    return 0 if all(checks) else 1


if __name__ == '__main__':
    raise SystemExit(main())
