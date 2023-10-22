#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

logAndRun() {
  echo "run command(PWD: $PWD):"
  echo "$*"
  "$@"
}

logAndRun flake8 --count --statistics --show-source --max-complexity=10 --max-line-length=120 *.py tests
