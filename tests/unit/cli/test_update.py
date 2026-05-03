"""tests/unit/cli/test_update.py"""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import Install, ManifestStore


def test_update_check_reports_drift(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="oldsha", installed_at=datetime.now(timezone.utc), files=[],
    ))
    store.save(m)
    with patch("agent_forge.github.resolve_plugin_sha", return_value="newsha"):
        runner = CliRunner()
        result = runner.invoke(main, ["update", "--check"])
    assert result.exit_code == 0
    assert "writing@kilocode" in result.output
    assert "oldsha" in result.output
    assert "newsha" in result.output


def test_update_skips_pinned(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="oldsha", installed_at=datetime.now(timezone.utc),
        pinned=True, pin_target="v1.0.0", files=[],
    ))
    store.save(m)
    with patch("agent_forge.github.resolve_plugin_sha", return_value="newsha"):
        runner = CliRunner()
        result = runner.invoke(main, ["update", "--check"])
    assert "pinned" in result.output.lower()


def test_update_reports_up_to_date(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="samesha", installed_at=datetime.now(timezone.utc), files=[],
    ))
    store.save(m)
    with patch("agent_forge.github.resolve_plugin_sha", return_value="samesha"):
        runner = CliRunner()
        result = runner.invoke(main, ["update", "--check"])
    assert result.exit_code == 0
    assert "up-to-date" in result.output.lower()
