"""tests/unit/cli/test_remove.py"""

from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner
from agent_forge.cli import main
from agent_forge.manifest import Install, ManifestStore


def test_remove_deletes_files_and_record(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AGENT_FORGE_MANIFEST", str(tmp_path / "m.json"))
    fake_installed = tmp_path / "fake_install.txt"
    fake_installed.write_text("x")
    store = ManifestStore(tmp_path / "m.json")
    m = store.load()
    m.installs.append(Install(
        id="writing@kilocode", plugin="writing", scope="plugin", tier="kilocode",
        installed_sha="x", installed_at=datetime.now(timezone.utc),
        files=[str(fake_installed)],
    ))
    store.save(m)
    runner = CliRunner()
    result = runner.invoke(main, ["remove", "writing@kilocode"])
    assert result.exit_code == 0
    assert not fake_installed.exists()
    m = store.load()
    assert not m.installs
