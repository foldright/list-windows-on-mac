#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/_utils.sh

log_and_run flake8 --count --statistics --show-source --max-complexity=10 --max-line-length=120 ./*.py tests

# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
# https://mypy.readthedocs.io/en/stable/existing_code.html#ignoring-errors-from-certain-modules
log_and_run mypy ./*.py tests

# show --strict mypy info only without fail lint
log_and_run mypy --strict ./*.py tests || true
