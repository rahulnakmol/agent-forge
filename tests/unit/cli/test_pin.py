"""tests/unit/cli/test_pin.py"""

from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import Install, ManifestStore


def test_pin_sets_pinned_flag(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="x", installed_at=datetime.now(timezone.utc), files=[],
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["pin", "writing@kilocode", "v1.0.0"])
    assert result.exit_code == 0
    m = store.load()
    assert m.installs[0].pinned is True
    assert m.installs[0].pin_target == "v1.0.0"


def test_unpin_clears_pinned_flag(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="x", installed_at=datetime.now(timezone.utc),
        pinned=True, pin_target="v1.0.0", files=[],
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["unpin", "writing@kilocode"])
    assert result.exit_code == 0
    m = store.load()
    assert m.installs[0].pinned is False
    assert m.installs[0].pin_target is None
