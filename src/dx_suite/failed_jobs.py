"""Helpers for finding and displaying failed DNAnexus jobs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class FailedJob:
    """Normalized failed job details for CLI output."""

    job_id: str
    name: str
    project: str
    state: str
    created: str
    failure: str

    def as_dict(self) -> dict[str, str]:
        return {
            "job_id": self.job_id,
            "name": self.name,
            "project": self.project,
            "state": self.state,
            "created": self.created,
            "failure": self.failure,
        }


def get_failed_jobs(
    *,
    project: str | None = None,
    limit: int = 20,
    dxpy_module: Any | None = None,
) -> list[FailedJob]:
    """Return failed jobs visible to the current DNAnexus auth context."""

    if limit < 1:
        raise ValueError("limit must be at least 1")

    dxpy = dxpy_module or _load_dxpy()
    kwargs: dict[str, Any] = {
        "state": "failed",
        "describe": True,
        "limit": limit,
    }
    if project:
        kwargs["project"] = project

    return [_normalize_failed_job(job) for job in dxpy.find_jobs(**kwargs)]


def _load_dxpy() -> Any:
    try:
        return import_module("dxpy")
    except ImportError as exc:
        raise RuntimeError(
            "dxpy is not installed. Install this project with `pip install -e .`."
        ) from exc


def _normalize_failed_job(job: dict[str, Any]) -> FailedJob:
    describe = _unwrap_description(job)

    return FailedJob(
        job_id=_first_text(describe, "id", "job", "$dnanexus_link"),
        name=_first_text(describe, "name", default="-"),
        project=_format_link(describe.get("project")),
        state=_first_text(describe, "state", default="failed"),
        created=_format_timestamp(describe.get("created")),
        failure=_format_failure(describe),
    )


def _unwrap_description(job: dict[str, Any]) -> dict[str, Any]:
    if isinstance(job.get("describe"), dict):
        return job["describe"]
    if isinstance(job.get("description"), dict):
        return job["description"]
    return job


def _first_text(source: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = source.get(key)
        if value not in (None, ""):
            return _format_link(value)
    return default


def _format_link(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("id") or value.get("$dnanexus_link") or value.get("name") or "-")
    if value in (None, ""):
        return "-"
    return str(value)


def _format_timestamp(value: Any) -> str:
    if value in (None, ""):
        return "-"
    if isinstance(value, (int, float)):
        timestamp = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(timestamp, tz=UTC).isoformat(timespec="seconds")
    return str(value)


def _format_failure(describe: dict[str, Any]) -> str:
    reason = _first_text(describe, "failureReason", "failure", "failureMessage")
    message = _first_text(describe, "error", "message")

    if reason and message and message != reason:
        return f"{reason}: {message}"
    return reason or message or "-"
