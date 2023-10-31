#!/bin/bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."
source scripts/_utils.sh

readonly proj_py_files=(./*.py tests)

log_and_run flake8 --count --statistics --show-source --max-complexity=10 --max-line-length=120 "${proj_py_files[@]}"

log_and_run isort --line-length=120 --check-only --diff "${proj_py_files[@]}"

# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
# https://mypy.readthedocs.io/en/stable/existing_code.html#ignoring-errors-from-certain-modules
log_and_run mypy "${proj_py_files[@]}"

# show --strict mypy info only without fail lint
log_and_run mypy --strict "${proj_py_files[@]}" || true
