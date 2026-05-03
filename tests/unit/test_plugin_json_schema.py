"""Validate every plugins/<name>/.claude-plugin/plugin.json structure."""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
PLUGIN_MANIFESTS = sorted((REPO / "plugins").glob("*/.claude-plugin/plugin.json"))


@pytest.fixture(scope="session")
def manifests() -> list[tuple[Path, dict]]:
    return [(p, json.loads(p.read_text())) for p in PLUGIN_MANIFESTS]


def test_at_least_one_plugin_present() -> None:
    assert PLUGIN_MANIFESTS, "no plugins discovered under plugins/"


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_json_valid_json(manifest_path: Path) -> None:
    json.loads(manifest_path.read_text())  # raises if invalid


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_json_required_fields(manifest_path: Path) -> None:
    data = json.loads(manifest_path.read_text())
    for field in ("name", "description"):
        assert field in data, f"{manifest_path} missing field: {field}"
    assert isinstance(data["name"], str) and data["name"], "name must be non-empty string"
    assert isinstance(data["description"], str) and data["description"]


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_name_matches_directory(manifest_path: Path) -> None:
    data = json.loads(manifest_path.read_text())
    dir_name = manifest_path.parent.parent.name
    assert data["name"] == dir_name, (
        f"plugin name '{data['name']}' must match directory name '{dir_name}'"
    )
