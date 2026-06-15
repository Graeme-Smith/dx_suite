#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "This script must be sourced: source scripts/load-env.sh [path-to-env]" >&2
  exit 1
fi

env_file="${1:-.env}"

if [[ ! -f "${env_file}" ]]; then
  echo "Missing ${env_file}. Copy .env.example to .env and fill in local values." >&2
  return 1
fi

set -a
# shellcheck disable=SC1090
source "${env_file}"
set +a

echo "Loaded environment from ${env_file}"
