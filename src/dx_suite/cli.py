"""Typer command line interface for dx-suite."""

from __future__ import annotations

import json
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from dx_suite import __version__
from dx_suite.failed_jobs import FailedJob, get_failed_jobs

app = typer.Typer(
    help="Useful DNAnexus command line utilities.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show the dx-suite version and exit."),
    ] = False,
) -> None:
    """Run dx-suite commands."""

    if version:
        console.print(f"dx-suite {__version__}")
        raise typer.Exit()


@app.command("failed-jobs")
def failed_jobs(
    project: Annotated[
        str | None,
        typer.Option(
            "--project",
            "-p",
            envvar="DX_PROJECT",
            help="Restrict results to a DNAnexus project ID.",
        ),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            "-n",
            envvar="DX_SUITE_FAILED_JOBS_LIMIT",
            min=1,
            help="Maximum number of failed jobs to return.",
        ),
    ] = 20,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit machine-readable JSON."),
    ] = False,
) -> None:
    """List failed DNAnexus jobs visible to the current dxpy context."""

    try:
        jobs = get_failed_jobs(project=project, limit=limit)
    except Exception as exc:
        console.print(f"[red]Unable to fetch failed jobs:[/] {exc}")
        raise typer.Exit(code=1) from exc

    if json_output:
        console.print_json(json.dumps([job.as_dict() for job in jobs]))
        return

    _print_failed_jobs_table(jobs)


def _print_failed_jobs_table(jobs: list[FailedJob]) -> None:
    if not jobs:
        console.print("[green]No failed jobs found.[/]")
        return

    table = Table(title="Failed DNAnexus Jobs")
    table.add_column("Job ID", style="bold cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Project", no_wrap=True)
    table.add_column("Created", no_wrap=True)
    table.add_column("Failure", overflow="fold")

    for job in jobs:
        table.add_row(job.job_id, job.name, job.project, job.created, job.failure)

    console.print(table)
