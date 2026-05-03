"""Integration test: install/update/remove lifecycle for cursor."""

import subprocess
import pytest

pytestmark = pytest.mark.requires_docker

CLI = "cursor"
IMAGE = f"agent-forge-test:{CLI}"
DOCKERFILE = f"tests/integration/dockerfiles/{CLI}.Dockerfile"


def _build_image() -> None:
    subprocess.run(
        ["docker", "build", "-t", IMAGE, "-f", DOCKERFILE, "."],
        check=True,
        timeout=300,
    )


def _docker_run(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "run", "--rm", IMAGE, *cmd],
        capture_output=True, text=True, timeout=120,
    )


@pytest.mark.slow
def test_cursor_install_lifecycle() -> None:
    _build_image()
    # Install writing plugin
    r = _docker_run("agent-forge", "install", "writing", "--tier", CLI)
    assert r.returncode == 0, f"install failed: {r.stderr}"
    # Check list shows the install
    r = _docker_run("agent-forge", "list")
    assert r.returncode == 0
    assert "writing" in r.stdout
    # Update check
    r = _docker_run("agent-forge", "update", "--check")
    assert r.returncode == 0
    # Remove
    r = _docker_run("agent-forge", "remove", f"writing@{CLI}")
    assert r.returncode == 0
    # Verify removed
    r = _docker_run("agent-forge", "list")
    assert "writing" not in r.stdout or "No installs" in r.stdout
