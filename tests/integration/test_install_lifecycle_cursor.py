"""Integration test: install/update/remove lifecycle for cursor."""

import subprocess
import pytest

pytestmark = pytest.mark.requires_docker

CLI = "cursor"
IMAGE = f"agent-forge-test:{CLI}"
DOCKERFILE = f"tests/integration/dockerfiles/{CLI}.Dockerfile"
CONTAINER = f"agent-forge-test-{CLI}"


def _build_image() -> None:
    subprocess.run(
        ["docker", "build", "-t", IMAGE, "-f", DOCKERFILE, "."],
        check=True,
        timeout=300,
    )


def _exec(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", CONTAINER, *cmd],
        capture_output=True, text=True, timeout=120,
    )


@pytest.mark.slow
def test_cursor_install_lifecycle() -> None:
    _build_image()
    subprocess.run(
        ["docker", "run", "-d", "--name", CONTAINER, "--rm", IMAGE, "sleep", "300"],
        check=True, timeout=30,
    )
    try:
        r = _exec("agent-forge", "install", "writing", "--tier", CLI)
        assert r.returncode == 0, f"install failed: {r.stderr}"

        r = _exec("agent-forge", "list")
        assert r.returncode == 0
        assert "writing" in r.stdout, f"expected 'writing' in list output: {r.stdout}"

        r = _exec("agent-forge", "update", "--check")
        assert r.returncode == 0

        r = _exec("agent-forge", "remove", f"writing@{CLI}")
        assert r.returncode == 0

        r = _exec("agent-forge", "list")
        assert "writing" not in r.stdout or "No installs" in r.stdout
    finally:
        subprocess.run(["docker", "rm", "-f", CONTAINER], capture_output=True)
