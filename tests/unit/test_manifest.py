"""tests/unit/test_manifest.py"""

from datetime import datetime, timezone
from pathlib import Path

from agent_forge.manifest import Install, Manifest, ManifestStore, OperationLogEntry


def test_empty_manifest_initialized(tmp_path: Path) -> None:
    store = ManifestStore(tmp_path / "manifest.json")
    m = store.load()
    assert m.schema_version == 1
    assert m.installs == []
    assert m.operation_log == []


def test_round_trip(tmp_path: Path) -> None:
    store = ManifestStore(tmp_path / "manifest.json")
    m = store.load()
    install = Install(
        id="writing@kilocode",
        plugin="writing",
        scope="plugin",
        scope_path=None,
        tier="kilocode",
        installed_sha="abc123",
        installed_tag=None,
        pinned=False,
        pin_target=None,
        installed_at=datetime.now(timezone.utc),
        files=["/tmp/x"],
    )
    m.installs.append(install)
    m.operation_log.append(OperationLogEntry(
        ts=datetime.now(timezone.utc), op="install", id="writing@kilocode", sha="abc123",
    ))
    store.save(m)
    reloaded = store.load()
    assert len(reloaded.installs) == 1
    assert reloaded.installs[0].id == "writing@kilocode"
    assert len(reloaded.operation_log) == 1


def test_locking_prevents_concurrent_writes(tmp_path: Path) -> None:
    """Two stores writing simultaneously must serialize."""
    import threading
    store_a = ManifestStore(tmp_path / "manifest.json")
    store_b = ManifestStore(tmp_path / "manifest.json")
    errors = []

    def write(store: ManifestStore, plugin_id: str) -> None:
        try:
            with store.lock():
                m = store.load()
                m.operation_log.append(OperationLogEntry(
                    ts=datetime.now(timezone.utc), op="install", id=plugin_id, sha="x",
                ))
                store.save(m)
        except Exception as e:
            errors.append(e)

    t1 = threading.Thread(target=write, args=(store_a, "a"))
    t2 = threading.Thread(target=write, args=(store_b, "b"))
    t1.start(); t2.start(); t1.join(); t2.join()
    assert not errors
    final = store_a.load()
    assert len(final.operation_log) == 2  # both writes succeeded


def test_id_format() -> None:
    install = Install(
        id="msft-arch/skills/azure-architect@codex-cli",
        plugin="msft-arch",
        scope="skill",
        scope_path="skills/azure-architect",
        tier="codex-cli",
        installed_sha="x",
        installed_tag=None,
        pinned=False,
        pin_target=None,
        installed_at=datetime.now(timezone.utc),
        files=[],
    )
    assert install.scope == "skill"
