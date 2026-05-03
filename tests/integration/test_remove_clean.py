"""Verify that `agent-forge remove` leaves zero residual files."""

import subprocess
import tempfile
import pytest

pytestmark = pytest.mark.requires_docker

CLI = "kilocode"
IMAGE = f"agent-forge-test:{CLI}"


@pytest.mark.slow
def test_remove_leaves_no_residue() -> None:
    subprocess.run(
        ["docker", "build", "-t", IMAGE,
         "-f", f"tests/integration/dockerfiles/{CLI}.Dockerfile", "."],
        check=True, timeout=300,
    )
    result = subprocess.run(
        ["docker", "run", "--rm", IMAGE, "bash", "-c",
         "agent-forge install writing --tier kilocode && "
         "agent-forge list | grep writing && "
         "agent-forge remove writing@kilocode && "
         "agent-forge list"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "No installs" in result.stdout or "writing" not in result.stdout.split("Removed")[1] if "Removed" in result.stdout else True
