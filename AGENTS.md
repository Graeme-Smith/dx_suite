# AGENTS.md

## Cursor Cloud specific instructions

`dx-suite` is a Python 3.10+ CLI (Typer + Rich, `src/` layout) for DNAnexus
workflows. The DNAnexus API client is `dxpy`. See `README.md` for standard
usage and `pyproject.toml` for dependency/test config.

### Environment
- Dependencies install into a virtualenv at `.venv` (created by the startup
  update script). Activate it before working: `source .venv/bin/activate`
  (or call binaries directly, e.g. `.venv/bin/pytest`, `.venv/bin/dx-suite`).
- The update script guards on `pyproject.toml` existing, because project code
  lives under `src/` and may not be present on a bare `main` checkout.

### Test / run
- Tests: `pytest` (config in `pyproject.toml`: `pythonpath=src`, `testpaths=tests`).
  There is no separate linter; `tests/test_env_setup.py` also `bash -n` lints the
  helper scripts.
- Core command: `dx-suite failed-jobs` (supports `--project/-p`, `--limit/-n`,
  `--json`; defaults also read from `DX_PROJECT` / `DX_SUITE_FAILED_JOBS_LIMIT`).

### Gotchas
- `dx-suite --version` alone exits with "Missing command": the `--version` option
  lives on the Typer callback which requires a subcommand. Read the version from
  `dx_suite.__version__` if you need it programmatically.
- `failed-jobs` calls the live DNAnexus API via `dxpy`. Real use normally needs an
  authenticated `dxpy` (`dx login`, or `DX_SECURITY_CONTEXT`). In this cloud
  sandbox the `api.dnanexus.com` endpoint returns job data even with no local
  auth configured, so the command works out of the box here.
