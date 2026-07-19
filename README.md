# dx-suite

Useful command line utilities for DNAnexus workflows.

## Installation

Install the package into a Python 3.10+ environment:

```bash
pip install -e .
```

For local development and tests:

```bash
pip install -e ".[dev]"
pytest
```

Or use the helper script to create a local virtual environment, install the
development dependencies, and create a starter `.env` file:

```bash
scripts/setup-env.sh
source .venv/bin/activate
```

Local environment values are kept in `.env`, which is ignored by git. Start
from the committed example file:

```bash
cp .env.example .env
source scripts/load-env.sh
```

## CLI

The package installs a `dx-suite` command powered by
[Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/).
DNAnexus API access is provided by `dxpy`, so run commands in an environment
where `dxpy` is installed and authenticated.

### Failed jobs

List failed jobs visible to the current `dxpy` context:

```bash
dx-suite failed-jobs
```

Limit results or scope the lookup to a project:

```bash
dx-suite failed-jobs --project project-xxxx --limit 10
```

The same defaults can come from environment variables, including values loaded
from `.env`:

```bash
DX_PROJECT=project-xxxx
DX_SUITE_FAILED_JOBS_LIMIT=10
```

Emit JSON for scripts:

```bash
dx-suite failed-jobs --json
```

## Development notes

- Keep CLI commands thin: Typer should parse options and render output, while
  DNAnexus API behavior lives in reusable modules under `src/dx_suite`.
- Prefer Rich tables for human-readable output and JSON output for automation.
- Unit tests should mock the `dxpy` boundary rather than requiring live
  DNAnexus credentials.
