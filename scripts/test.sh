#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/_utils.sh

log_and_run python3 -m pytest -v tests
