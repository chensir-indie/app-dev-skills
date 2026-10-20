#!/bin/sh
# Bootstrap without Node/npm dependencies. Never installs or changes configuration.
set -u
case "$0" in
  */*) doctor_dir=${0%/*} ;;
  *) doctor_dir=. ;;
esac
doctor_root=$(CDPATH= cd "$doctor_dir/.." && pwd -P) || exit 1
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  printf '%s\n' 'Usage: sh scripts/doctor.sh [--scope core]' \
    'Run from any directory; checks Node >=22, npm, packages and a real browser launch.' \
    '--scope core checks the runtime and packages only; it does not certify export readiness.' \
    'PLAYWRIGHT_CHANNEL=chrome selects an already installed Google Chrome.' \
    'Checks only: no automatic installation or machine configuration changes.'
  exit 0
fi
doctor_quote() {
  doctor_value=$1
  printf "'"
  while :; do
    case "$doctor_value" in
      *"'"*)
        doctor_prefix=${doctor_value%%\'*}
        printf '%s%s' "$doctor_prefix" "'\\''"
        doctor_value=${doctor_value#*\'}
        ;;
      *) printf "%s'" "$doctor_value"; break ;;
    esac
  done
}
doctor_failed=0
if ! command -v node >/dev/null 2>&1; then
  printf '%s\n' '[FAIL] Node.js: executable not found.' \
    'Install Node.js 22 or newer with npm: https://nodejs.org/en/download' \
    'Then reopen the terminal/agent so its PATH includes node and npm.'
  doctor_failed=1
else
  doctor_version=$(node --version 2>/dev/null) || doctor_version=unavailable
  doctor_major=${doctor_version#v}
  doctor_major=${doctor_major%%.*}
  case "$doctor_major" in
    ''|*[!0-9]*) doctor_major=0 ;;
  esac
  if [ "$doctor_major" -lt 22 ]; then
    printf '[FAIL] Node.js: %s; requires >=22.\n' "$doctor_version"
    printf '%s\n' 'Install or select Node.js 22+: https://nodejs.org/en/download'
    doctor_failed=1
  else
    printf '[PASS] Node.js: %s\n' "$doctor_version"
  fi
fi
if ! command -v npm >/dev/null 2>&1; then
  printf '%s\n' '[FAIL] npm: executable not found.' \
    'Use a Node.js installation that includes npm: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm'
  doctor_failed=1
elif [ "$doctor_failed" -eq 0 ]; then
  if doctor_npm_version=$(npm --version 2>/dev/null); then
    printf '[PASS] npm: %s\n' "$doctor_npm_version"
  else
    printf '%s\n' '[FAIL] npm: executable exists but cannot run; repair the selected Node.js/npm installation.'
    doctor_failed=1
  fi
else
  printf '%s\n' '[INFO] npm: found; execution check waits for a supported Node.js runtime.'
fi
if [ "$doctor_failed" -ne 0 ]; then
  printf '\nAfter fixing the runtime, run:\n  sh '
  doctor_quote "$doctor_root/scripts/doctor.sh"
  printf '\n'
  exit 1
fi
exec node "$doctor_root/scripts/doctor.mjs" "$@"
