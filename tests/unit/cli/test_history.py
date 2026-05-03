"""tests/unit/cli/test_history.py"""

from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import ManifestStore, OperationLogEntry


def test_history_lists_log_entries(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.operation_log.append(OperationLogEntry(
        ts=datetime.now(timezone.utc), op="install", id="x@kilocode", sha="abc",
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["history"])
    assert result.exit_code == 0
    assert "install" in result.output
    assert "x@kilocode" in result.output
