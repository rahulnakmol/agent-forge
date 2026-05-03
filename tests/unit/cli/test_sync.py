"""tests/unit/cli/test_sync.py"""

from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import Install, ManifestStore


def test_sync_empty_reports_nothing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    runner = CliRunner()
    result = runner.invoke(main, ["sync"])
    assert result.exit_code == 0
    assert "Nothing" in result.output


def test_sync_with_installs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="oldsha", installed_at=datetime.now(timezone.utc), files=[],
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["sync"])
    assert result.exit_code == 0
    assert "Synced" in result.output
