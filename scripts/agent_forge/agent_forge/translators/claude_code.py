"""Claude Code translator — mostly a no-op (canonical format)."""

import shutil
from pathlib import Path

from agent_forge.translators import register
from agent_forge.translators._base import Translator


class ClaudeCodeTranslator:
    name = "claude-code"
    tier = "1a"

    def detect(self) -> bool:
        import shutil as sh
        return bool(sh.which("claude")) or Path.home().joinpath(".claude").exists()

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


register(ClaudeCodeTranslator())
