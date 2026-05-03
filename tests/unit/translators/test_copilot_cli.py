"""tests/unit/translators/test_copilot_cli.py"""

import json
from pathlib import Path

import pytest
from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.copilot_cli import (
    build_copilot_marketplace_json,
    build_copilot_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_copilot_translator_registered() -> None:
    t = get_translator("copilot-cli")
    assert t.tier == "1a"


def test_marketplace_json_has_metadata_wrapper() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_copilot_marketplace_json(canonical, plugins)
    assert "metadata" in out
    assert out["metadata"]["description"]
    assert out["metadata"]["version"]
    assert "owner" in out
    assert "@" in out["owner"]["email"]


def test_marketplace_plugin_entries_have_version() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_copilot_marketplace_json(canonical, plugins)
    for p in out["plugins"]:
        assert "version" in p, f"plugin {p['name']} missing version"


def test_plugin_json_declares_components() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_copilot_plugin_json(plugins["prompts"])
    assert pj["name"] == "prompts"
    assert pj["description"]
    assert pj["version"]
    if (plugins["prompts"].plugin_dir / "skills").exists():
        assert pj.get("skills") == "skills/"
    if (plugins["prompts"].plugin_dir / "agents").exists():
        assert pj.get("agents") == "agents/"
    if (plugins["prompts"].plugin_dir / "commands").exists():
        assert pj.get("commands") == "commands/"


def test_agent_mirror_filename(tmp_path: Path) -> None:
    src = tmp_path / "agents" / "my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text("---\nname: my-agent\ndescription: x\n---\n\nbody")
    t = get_translator("copilot-cli")
    t.translate_agent(src, tmp_path / "agents" / "my-agent.agent.md")
    assert (tmp_path / "agents" / "my-agent.agent.md").exists()
