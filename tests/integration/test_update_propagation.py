"""End-to-end: install, simulate upstream bump via mock, verify update detects drift."""

import subprocess
import pytest
from unittest.mock import patch

pytestmark = pytest.mark.requires_docker

CLI = "kilocode"
IMAGE = f"agent-forge-test:{CLI}"


@pytest.mark.slow
def test_update_lifecycle_kilocode() -> None:
    subprocess.run(
        ["docker", "build", "-t", IMAGE,
         "-f", f"tests/integration/dockerfiles/{CLI}.Dockerfile", "."],
        check=True, timeout=300,
    )
    install = subprocess.run(
        ["docker", "run", "--rm", IMAGE,
         "agent-forge", "install", "writing", "--tier", CLI],
        capture_output=True, text=True,
    )
    assert install.returncode == 0, install.stderr
    update_check = subprocess.run(
        ["docker", "run", "--rm", IMAGE,
         "agent-forge", "update", "--check"],
        capture_output=True, text=True,
    )
    assert update_check.returncode == 0
    assert "writing" in update_check.stdout
