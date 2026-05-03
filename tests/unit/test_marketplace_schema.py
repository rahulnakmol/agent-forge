"""Validate .claude-plugin/marketplace.json against schema + invariants."""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MARKETPLACE.read_text())


def test_marketplace_file_exists() -> None:
    assert MARKETPLACE.exists(), f"missing {MARKETPLACE}"


def test_top_level_required_fields(manifest: dict) -> None:
    for field in ("name", "description", "version", "owner", "plugins"):
        assert field in manifest, f"missing top-level field: {field}"


def test_version_is_semver(manifest: dict) -> None:
    import re
    assert re.match(r"^\d+\.\d+\.\d+$", manifest["version"]), (
        f"version must be semver, got: {manifest['version']}"
    )


def test_owner_has_name_and_email(manifest: dict) -> None:
    assert "name" in manifest["owner"]
    assert "email" in manifest["owner"]
    assert "@" in manifest["owner"]["email"]


def test_plugins_have_required_fields(manifest: dict) -> None:
    for plugin in manifest["plugins"]:
        for field in ("name", "description", "source"):
            assert field in plugin, f"plugin missing {field}: {plugin}"


def test_plugin_sources_are_relative_to_plugins_dir(manifest: dict) -> None:
    """BOUNDARY: all sources must point under plugins/."""
    for plugin in manifest["plugins"]:
        source = plugin["source"]
        assert source.startswith("./plugins/") or source.startswith("plugins/"), (
            f"plugin {plugin['name']} sources outside plugins/: {source}"
        )


def test_plugin_source_dirs_exist(manifest: dict) -> None:
    for plugin in manifest["plugins"]:
        path = REPO / plugin["source"].lstrip("./")
        assert path.exists(), f"plugin source missing on disk: {path}"


def test_no_kpmg_in_marketplace(manifest: dict) -> None:
    """KPMG plugin is excluded from the public marketplace."""
    body = MARKETPLACE.read_text().lower()
    assert "kpmg" not in body, "KPMG references must be stripped from marketplace.json"
    for plugin in manifest["plugins"]:
        assert "kpmg" not in plugin["name"].lower()
