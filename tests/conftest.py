"""Shared fixtures: plugin discovery, ephemeral $HOME directories.

Real fixtures populated as plugins migrate (Phase 1) and translators land (Phase 2).
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def plugins_dir(repo_root: Path) -> Path:
    return repo_root / "plugins"


@pytest.fixture(scope="session")
def all_plugin_roots(plugins_dir: Path) -> list[Path]:
    """All plugin directories — empty until Phase 1 migrates plugins."""
    if not plugins_dir.exists():
        return []
    return sorted(p.parent.parent for p in plugins_dir.glob("*/.claude-plugin/plugin.json"))


@pytest.fixture(scope="session")
def all_skill_md_paths(all_plugin_roots: list[Path]) -> list[Path]:
    """All SKILL.md paths across all plugins. Empty until Phase 1."""
    return [s for p in all_plugin_roots for s in p.glob("skills/*/SKILL.md")]


@pytest.fixture
def ephemeral_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set HOME to a fresh tmp dir so install tests don't touch the real one."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    return fake_home
