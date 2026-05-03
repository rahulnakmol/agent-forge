"""Cursor translator (Tier 1a — registry-style native marketplace)."""

import shutil
from pathlib import Path

from agent_forge.canonical import CanonicalPlugin
from agent_forge.translators import register


def build_cursor_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    return {
        "name": canonical["name"],
        "description": canonical["description"],
        "version": canonical["version"],
        "owner": canonical["owner"],
        "plugins": [
            {
                "name": p.name,
                "description": p.manifest.get("description", ""),
                "version": p.manifest.get("version", canonical["version"]),
                "source": f"./plugins/{p.name}",
                "category": "productivity",
            }
            for p in plugins
        ],
    }


def build_cursor_plugin_json(plugin: CanonicalPlugin) -> dict:
    pj: dict = {
        "name": plugin.name,
        "description": plugin.manifest.get("description", ""),
        "version": plugin.manifest.get("version", "1.0.0"),
    }
    if author := plugin.manifest.get("author"):
        pj["author"] = author
    return pj


class CursorTranslator:
    name = "cursor"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("cursor")) or Path(".cursor").exists()

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CursorTranslator())
