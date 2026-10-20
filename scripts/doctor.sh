#!/bin/sh
# Bootstrap without Node, npm, or third-party Python packages.
set -eu
script_dir=${0%/*}
[ "$script_dir" != "$0" ] || script_dir=.
script_dir=$(CDPATH= cd -- "$script_dir" && pwd)
if [ "${1:-}" = "--skill" ]; then
  skill_name=${2:-}
  case "$skill_name" in
    ''|*[!a-z0-9-]*|-*|*-)
      echo 'Usage: sh scripts/doctor.sh --skill <skill-name> [skill options]' >&2
      exit 2 ;;
  esac
  skill_dir="$script_dir/../skills/$skill_name"
  if [ ! -f "$skill_dir/SKILL.md" ] || [ ! -f "$skill_dir/scripts/doctor.sh" ]; then
    printf 'Unknown or incomplete skill: %s. Inspect skills/*/SKILL.md or run python3 scripts/list_skills.py.\n' "$skill_name" >&2
    exit 2
  fi
  shift 2
  exec /bin/sh "$skill_dir/scripts/doctor.sh" "$@"
fi
for interpreter in python3; do
  if command -v "$interpreter" >/dev/null 2>&1 &&
     "$interpreter" -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
    exec "$interpreter" "$script_dir/doctor.py" "$@"
  fi
done
echo 'FAIL: Python 3.9+ as python3 is required for collection checks. Install Python from https://www.python.org/downloads/ and reopen your terminal.' >&2
echo 'For only one skill, run: sh scripts/doctor.sh --skill <skill-name>' >&2
echo "See $script_dir/../docs/runtime.md for virtual-environment setup and platform guidance." >&2
exit 1
