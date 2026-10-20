"""Actionable dependency failures shared only by this skill's Python tools."""
import importlib
from pathlib import Path
import shlex
import sys


def ensure_python():
    if sys.version_info < (3, 9):
        root = Path(__file__).resolve().parent.parent
        print('Environment error: Python 3.9+ is required. Install from https://www.python.org/downloads/', file=sys.stderr)
        print('Check: sh ' + shlex.quote(str(root / 'scripts/doctor.sh')) + ' --scope python', file=sys.stderr)
        raise SystemExit(2)


def ensure_pillow():
    ensure_python()
    try:
        importlib.import_module('PIL.Image')
    except (ImportError, OSError) as exc:
        root = Path(__file__).resolve().parent.parent
        print('Environment error: Pillow is unavailable in ' + sys.executable, file=sys.stderr)
        print('  ' + str(exc).splitlines()[0], file=sys.stderr)
        print('Check: sh ' + shlex.quote(str(root / 'scripts/doctor.sh')) + ' --scope python', file=sys.stderr)
        print('Repair from ' + str(root) + ':', file=sys.stderr)
        if sys.prefix == sys.base_prefix:
            print('  ' + shlex.quote(sys.executable) + ' -m venv .venv', file=sys.stderr)
            print('  . .venv/bin/activate', file=sys.stderr)
        print('  python -m pip install -r ' + shlex.quote(str(root / 'requirements.txt')), file=sys.stderr)
        raise SystemExit(2) from None
