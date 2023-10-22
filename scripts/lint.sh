#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

logAndRun() {
  printf '\e[1;33;44m%s\e[0m\n' "run command(PWD: $PWD): $*"
  time "$@"
}

logAndRun flake8 --count --statistics --show-source --max-complexity=10 --max-line-length=120 ./*.py tests

# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
# https://mypy.readthedocs.io/en/stable/existing_code.html#ignoring-errors-from-certain-modules
logAndRun mypy ./*.py tests

# show --strict mypy info only without fail lint
logAndRun mypy --strict ./*.py tests || true
