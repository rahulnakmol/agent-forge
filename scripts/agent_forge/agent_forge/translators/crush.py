"""Crush translator (Tier 2 — trivial adapter)."""

import shutil
from pathlib import Path

from agent_forge.translators import register


class CrushTranslator:
    name = "crush"
    tier = "2"

    def detect(self) -> bool:
        return bool(shutil.which("crush"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        home = Path.home()
        plugin_name = plugin_root.name
        result: dict[str, Path] = {}
        skills_src = plugin_root / "skills"
        if skills_src.exists():
            for skill_dir in skills_src.iterdir():
                if (skill_dir / "SKILL.md").exists():
                    result[str(skill_dir.relative_to(plugin_root))] = (
                        home / ".claude/skills" / plugin_name / skill_dir.name
                    )
        return result

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(command_md, dest)

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CrushTranslator())
