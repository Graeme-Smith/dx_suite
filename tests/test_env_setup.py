import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_env_scripts_have_valid_bash_syntax():
    for script in ("scripts/setup-env.sh", "scripts/load-env.sh"):
        subprocess.run(
            ["bash", "-n", str(ROOT / script)],
            check=True,
        )


def test_env_example_uses_safe_placeholders():
    env_example = (ROOT / ".env.example").read_text()

    assert "DX_PROJECT=" in env_example
    assert "DX_SUITE_FAILED_JOBS_LIMIT=20" in env_example
    assert "token" not in env_example.lower()
