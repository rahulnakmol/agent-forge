"""OpenAI Codex CLI translator (Tier 1a — registry-style native marketplace)."""

import shutil
from pathlib import Path

import tomli_w

from agent_forge.canonical import CanonicalPlugin
from agent_forge.frontmatter import parse_frontmatter
from agent_forge.translators import register


def build_codex_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    return {
        "name": canonical["name"],
        "plugins": [
            {
                "name": p.name,
                "source": {"path": f"./plugins/{p.name}"},
                "policy": {"installation": "interactive", "authentication": "none"},
                "category": "productivity",
            }
            for p in plugins
        ],
    }


def build_codex_plugin_json(plugin: CanonicalPlugin) -> dict:
    pj: dict = {
        "name": plugin.name,
        "version": plugin.manifest.get("version", "1.0.0"),
        "description": plugin.manifest.get("description", ""),
    }
    if (plugin.plugin_dir / "skills").exists():
        pj["skills"] = "skills/"
    if (plugin.plugin_dir / "agents").exists():
        pj["agents"] = "agents/"
    if (plugin.plugin_dir / ".mcp.json").exists():
        pj["mcpServers"] = ".mcp.json"
    return pj


def md_agent_to_toml(agent_md: Path) -> str:
    """Convert a Claude-format agent .md (frontmatter + body) to Codex TOML."""
    fm, body = parse_frontmatter(agent_md.read_text())
    toml_doc: dict = {
        "name": fm.get("name", agent_md.stem),
        "description": fm.get("description", ""),
        "developer_instructions": body.strip(),
    }
    if "model" in fm:
        toml_doc["model"] = fm["model"]
    return tomli_w.dumps(toml_doc)


class CodexCliTranslator:
    name = "codex-cli"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("codex"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(md_agent_to_toml(agent_md))

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CodexCliTranslator())
