"""tests/unit/translators/test_cursor.py"""

import json
from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.cursor import (
    build_cursor_marketplace_json,
    build_cursor_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_cursor_translator_registered() -> None:
    t = get_translator("cursor")
    assert t.tier == "1a"


def test_cursor_marketplace_json_shape() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_cursor_marketplace_json(canonical, plugins)
    assert out["name"]
    assert "plugins" in out
    for p in out["plugins"]:
        assert "name" in p


def test_cursor_plugin_json_minimal() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_cursor_plugin_json(plugins["writing"])
    assert pj["name"] == "writing"
