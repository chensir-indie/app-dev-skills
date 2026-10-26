#!/bin/sh
# Diagnose the selected task before invoking a runtime. No installations or writes.
set -eu
scope=workspace
case "$#" in
  0) ;;
  2)
    if [ "$1" != '--scope' ]; then
      printf '%s\n' 'Usage: sh scripts/doctor.sh [--scope instructions|workspace]' >&2
      exit 2
    fi
    scope=$2 ;;
  *)
    printf '%s\n' 'Usage: sh scripts/doctor.sh [--scope instructions|workspace]' >&2
    exit 2 ;;
esac
case "$scope" in
  instructions)
    printf '%s\n' '[ok] iphone-duo-adaptation: reading workflow instructions needs only this POSIX shell.' ;;
  workspace)
    found_runtime=false
    for interpreter in python3 python; do
      if command -v "$interpreter" >/dev/null 2>&1 &&
         "$interpreter" -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
        printf '[ok] iphone-duo-adaptation: Python 3.9+ available as %s; workspace rules use only its standard library.\n' "$interpreter"
        found_runtime=true
        break
      fi
    done
    if [ "$found_runtime" != true ]; then
      printf '%s\n' 'FAIL: Python 3.9+ as python3 or python is required to materialize and check workspace rules.' \
        'Install a supported Python from https://www.python.org/downloads/ and reopen your terminal.' \
        'To read the workflow without Python: sh scripts/doctor.sh --scope instructions' >&2
      exit 1
    fi ;;
  *)
    printf '%s\n' 'Usage: sh scripts/doctor.sh [--scope instructions|workspace]' >&2
    exit 2 ;;
esac
printf '%s\n' 'This preflight does not validate Apple compliance, browsers, HTML quality, UI-framework toolchains, Xcode, simulators or devices.'
