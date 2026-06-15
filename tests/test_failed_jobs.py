from dx_suite.failed_jobs import get_failed_jobs


class FakeDxpy:
    def __init__(self, jobs):
        self.jobs = jobs
        self.calls = []

    def find_jobs(self, **kwargs):
        self.calls.append(kwargs)
        return self.jobs


def test_get_failed_jobs_queries_failed_jobs_with_project_and_limit():
    dxpy = FakeDxpy(
        [
            {
                "id": "job-123",
                "name": "align reads",
                "project": "project-abc",
                "state": "failed",
                "created": 1_700_000_000_000,
                "failureReason": "AppError",
                "failureMessage": "tool exited 1",
            }
        ]
    )

    jobs = get_failed_jobs(project="project-abc", limit=5, dxpy_module=dxpy)

    assert dxpy.calls == [
        {
            "state": "failed",
            "describe": True,
            "limit": 5,
            "project": "project-abc",
        }
    ]
    assert jobs[0].as_dict() == {
        "job_id": "job-123",
        "name": "align reads",
        "project": "project-abc",
        "state": "failed",
        "created": "2023-11-14T22:13:20+00:00",
        "failure": "AppError: tool exited 1",
    }


def test_get_failed_jobs_supports_wrapped_descriptions():
    dxpy = FakeDxpy(
        [
            {
                "describe": {
                    "$dnanexus_link": "job-456",
                    "project": {"id": "project-def"},
                    "state": "failed",
                    "failure": "ExecutionError",
                }
            }
        ]
    )

    jobs = get_failed_jobs(dxpy_module=dxpy)

    assert jobs[0].job_id == "job-456"
    assert jobs[0].project == "project-def"
    assert jobs[0].failure == "ExecutionError"


def test_get_failed_jobs_requires_positive_limit():
    dxpy = FakeDxpy([])

    try:
        get_failed_jobs(limit=0, dxpy_module=dxpy)
    except ValueError as exc:
        assert str(exc) == "limit must be at least 1"
    else:
        raise AssertionError("expected ValueError")
