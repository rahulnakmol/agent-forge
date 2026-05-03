"""GitHub Copilot CLI translator (Tier 1a — registry-style native marketplace)."""

import shutil
from pathlib import Path

from agent_forge.canonical import CanonicalPlugin
from agent_forge.translators import register


def build_copilot_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    """Wrap canonical Claude marketplace.json in Copilot's metadata schema."""
    return {
        "name": canonical["name"],
        "owner": canonical["owner"],
        "metadata": {
            "description": canonical["description"],
            "version": canonical["version"],
        },
        "plugins": [
            {
                "name": p.name,
                "description": p.manifest.get("description", ""),
                "version": p.manifest.get("version", canonical["version"]),
                "source": f"./plugins/{p.name}",
            }
            for p in plugins
        ],
    }


def build_copilot_plugin_json(plugin: CanonicalPlugin) -> dict:
    """Generate the per-plugin Copilot manifest at <plugin>/plugin.json."""
    pj: dict = {
        "name": plugin.name,
        "description": plugin.manifest.get("description", ""),
        "version": plugin.manifest.get("version", "1.0.0"),
    }
    if author := plugin.manifest.get("author"):
        pj["author"] = author
    if plugin.manifest.get("license"):
        pj["license"] = plugin.manifest["license"]
    if (plugin.plugin_dir / "skills").exists():
        pj["skills"] = "skills/"
    if (plugin.plugin_dir / "agents").exists():
        pj["agents"] = "agents/"
    if (plugin.plugin_dir / "commands").exists():
        pj["commands"] = "commands/"
    if (plugin.plugin_dir / ".mcp.json").exists():
        pj["mcpServers"] = ".mcp.json"
    return pj


class CopilotCliTranslator:
    name = "copilot-cli"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("copilot"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        """Mirror <name>.md → <name>.agent.md (Copilot's filename convention)."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CopilotCliTranslator())
