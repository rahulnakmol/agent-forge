"""tests/unit/test_canonical.py"""

from pathlib import Path

import pytest
from agent_forge.canonical import CanonicalPlugin, discover_plugins


def test_discovers_all_plugins() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = discover_plugins(repo / "plugins")
    names = [p.name for p in plugins]
    assert "writing" in names
    assert "prompts" in names
    assert "msft-arch" in names
    assert "pm" in names
    assert "kpmg" not in names


def test_canonical_plugin_loads_manifest() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    writing = plugins["writing"]
    assert writing.manifest["name"] == "writing"
    assert writing.manifest["description"]


def test_canonical_plugin_lists_skills() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    skills = plugins["writing"].skills()
    assert any(s.name == "humanize" for s in skills)


def test_canonical_skill_has_frontmatter() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    skills = {s.name: s for s in plugins["writing"].skills()}
    assert skills["humanize"].frontmatter["name"] == "humanize"
    assert skills["humanize"].frontmatter["description"]
