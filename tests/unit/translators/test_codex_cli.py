"""tests/unit/translators/test_codex_cli.py"""

import json
from pathlib import Path

import tomli
import pytest
from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.codex_cli import (
    build_codex_marketplace_json,
    build_codex_plugin_json,
    md_agent_to_toml,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_codex_translator_registered() -> None:
    t = get_translator("codex-cli")
    assert t.tier == "1a"


def test_codex_marketplace_json_shape() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_codex_marketplace_json(canonical, plugins)
    assert out["name"]
    assert "plugins" in out
    for p in out["plugins"]:
        assert "name" in p
        assert "source" in p
        assert "policy" in p


def test_codex_plugin_json_kebab_name() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_codex_plugin_json(plugins["msft-arch"])
    assert pj["name"] == "msft-arch"
    assert pj["version"]


def test_md_agent_converted_to_toml(tmp_path: Path) -> None:
    src = tmp_path / "agents/my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text(
        "---\n"
        "name: my-agent\n"
        "description: A helpful assistant\n"
        "tools: [bash, edit]\n"
        "---\n\n"
        "You are a specialized assistant that helps with X.\n"
    )
    out = md_agent_to_toml(src)
    parsed = tomli.loads(out)
    assert parsed["name"] == "my-agent"
    assert parsed["description"]
    assert parsed["developer_instructions"].startswith("You are a specialized")


def test_translate_agent_writes_toml(tmp_path: Path) -> None:
    src = tmp_path / "agents/my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text("---\nname: x\ndescription: y\n---\n\nBody")
    t = get_translator("codex-cli")
    dst = tmp_path / "agents/my-agent.toml"
    t.translate_agent(src, dst)
    assert dst.exists()
    parsed = tomli.loads(dst.read_text())
    assert parsed["name"] == "x"


def test_translate_command_is_noop(tmp_path: Path) -> None:
    t = get_translator("codex-cli")
    src = tmp_path / "src.md"
    src.write_text("body")
    dst = tmp_path / "dst.toml"
    t.translate_command(src, dst)
    assert not dst.exists()
