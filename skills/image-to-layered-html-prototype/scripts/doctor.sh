#!/bin/sh
# Bootstrap the dependency checker without assuming Python is already installed.
set -u
case "${1-}" in
  -h|--help)
    printf '%s\n' 'Usage: sh scripts/doctor.sh [--scope python|browser|all]' \
      'Read-only checks; all is the default. Missing requirements exit 1; usage errors exit 2.'
    exit 0 ;;
esac
script_dir=${0%/*}
[ "$script_dir" != "$0" ] || script_dir=.
script_dir=$(CDPATH= cd -P "$script_dir" && pwd) || exit 1
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 &&
      "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
    exec "$candidate" "$script_dir/doctor.py" "$@"
  fi
done
printf '%s\n' '[missing] Python 3.9+ (python3 or python on PATH)' \
  'Install Python from https://www.python.org/downloads/ and reopen the terminal.' \
  'On Windows, enable the Python installer PATH option; use Git Bash for this .sh launcher.' \
  "Then run: sh \"$script_dir/doctor.sh\"" >&2
exit 1
