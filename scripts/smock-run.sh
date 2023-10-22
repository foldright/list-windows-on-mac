#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

logAndRun() {
  printf '\e[1;33;44m%s\e[0m\n' "run command(PWD: $PWD): $*"
  time "$@"
}

logAndRun ./lswin.py
logAndRun python lswin.py -h

logAndRun ./lswin.py --exclude-0-area --keep-one-for-same-pid-rect
logAndRun ./lswin.py --sort-key x --sort-key title --no-headers

logAndRun ./lswin.py -Zok x -k title -ky -H
