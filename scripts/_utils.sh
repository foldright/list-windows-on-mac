#!/bin/bash

log_and_run() {
  # about CI env var
  #   https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
  if [[ -t 1 || true = "${GITHUB_ACTIONS:-}" ]]; then
    printf '\e[1;33;44m%s\e[0m\n' "run command(PWD: $PWD): $*"
  else
    printf '%s\n' "run command(PWD: $PWD): $*"
  fi

  time "$@"
}
