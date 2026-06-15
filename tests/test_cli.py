import json

from typer.testing import CliRunner

from dx_suite.cli import app
from dx_suite.failed_jobs import FailedJob

runner = CliRunner()


def test_failed_jobs_outputs_json(monkeypatch):
    def fake_get_failed_jobs(project, limit):
        assert project == "project-123"
        assert limit == 3
        return [
            FailedJob(
                job_id="job-123",
                name="qc",
                project="project-123",
                state="failed",
                created="2024-01-01T00:00:00+00:00",
                failure="AppError: bad input",
            )
        ]

    monkeypatch.setattr("dx_suite.cli.get_failed_jobs", fake_get_failed_jobs)

    result = runner.invoke(
        app,
        ["failed-jobs", "--project", "project-123", "--limit", "3", "--json"],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == [
        {
            "job_id": "job-123",
            "name": "qc",
            "project": "project-123",
            "state": "failed",
            "created": "2024-01-01T00:00:00+00:00",
            "failure": "AppError: bad input",
        }
    ]


def test_failed_jobs_outputs_empty_message(monkeypatch):
    monkeypatch.setattr("dx_suite.cli.get_failed_jobs", lambda project, limit: [])

    result = runner.invoke(app, ["failed-jobs"])

    assert result.exit_code == 0
    assert "No failed jobs found." in result.stdout


def test_failed_jobs_reports_lookup_errors(monkeypatch):
    def fake_get_failed_jobs(project, limit):
        raise RuntimeError("not authenticated")

    monkeypatch.setattr("dx_suite.cli.get_failed_jobs", fake_get_failed_jobs)

    result = runner.invoke(app, ["failed-jobs"])

    assert result.exit_code == 1
    assert "Unable to fetch failed jobs" in result.stdout
    assert "not authenticated" in result.stdout
