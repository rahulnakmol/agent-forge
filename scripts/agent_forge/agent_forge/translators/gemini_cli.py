"""Google Gemini CLI translator (Tier 1b — git-URL native install)."""

import shutil
from pathlib import Path

from agent_forge.translators import register


class GeminiCliTranslator:
    name = "gemini-cli"
    tier = "1b"

    def detect(self) -> bool:
        return bool(shutil.which("gemini"))

    def install_command(self, repo: str, skill: str | None = None) -> str:
        if skill:
            return f"gemini skills install github:{repo}#{skill}"
        return f"gemini skills install github:{repo}"

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


register(GeminiCliTranslator())
