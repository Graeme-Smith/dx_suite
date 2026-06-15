#!/usr/bin/env bash
set -euo pipefail

python_cmd="${PYTHON:-python3}"

"${python_cmd}" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Fill in any local values before running commands."
fi

echo "Environment ready. Activate it with: source .venv/bin/activate"
