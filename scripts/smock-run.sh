#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

logAndRun() {
  echo "run command(PWD: $PWD):"
  echo "$*"
  "$@"
}

logAndRun ./lswin.py
logAndRun python lswin.py -h

logAndRun ./lswin.py --exclude-0-area
logAndRun ./lswin.py --sort-key x --sort-key title
logAndRun ./lswin.py --keep-one-for-same-pid-rect

logAndRun ./lswin.py -Zok x -k title -ky -H
