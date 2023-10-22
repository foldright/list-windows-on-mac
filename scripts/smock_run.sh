#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/_utils.sh

log_and_run ./lswin.py
log_and_run python3 lswin.py -h

log_and_run ./lswin.py --exclude-0-area --keep-one-for-same-pid-rect
log_and_run ./lswin.py --sort-key x --sort-key title --no-headers

log_and_run python3 lswin.py -Zok x -k title -ky -H

log_and_run ./lswin.py --json
