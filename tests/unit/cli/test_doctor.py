"""tests/unit/cli/test_doctor.py"""

from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import Install, ManifestStore


def test_doctor_detects_missing_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="x", installed_at=datetime.now(timezone.utc),
        files=["/nonexistent/path/file.md"],
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert "missing" in result.output.lower()


def test_doctor_healthy_when_no_installs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    runner = CliRunner()
    result = runner.invoke(main, ["doctor"])
    assert result.exit_code == 0
    assert "healthy" in result.output.lower() or "0" in result.output
