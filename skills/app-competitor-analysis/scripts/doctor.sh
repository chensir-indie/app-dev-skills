#!/bin/sh
# Read-only preflight for the optional standard-library Python helpers.
set -eu

found_python=false
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    found_python=true
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
      version=$("$candidate" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
      printf '[ok] app-competitor-analysis: %s %s (%s)\n' "$candidate" "$version" "$(command -v "$candidate")"
      printf 'Use %s for the helpers. Core rendering/audits require no pip packages, Node.js or browser download. Optional preview preparation needs Pillow.\n' "$candidate"
      exit 0
    fi
  fi
done

if [ "$found_python" = true ]; then
  printf '%s\n' '[error] Python was found, but no Python 3.9+ interpreter could run.' >&2
else
  printf '%s\n' '[error] Python 3.9+ is missing from PATH (checked python3 and python).' >&2
fi
printf '%s\n' \
  'Install a supported Python 3 from https://www.python.org/downloads/ using your platform instructions.' \
  'Reopen the terminal, confirm python3 --version (or python --version), then rerun sh scripts/doctor.sh.' \
  'This check installs nothing. Evidence research can continue; rendering and ledger audits need Python.' >&2
exit 1
