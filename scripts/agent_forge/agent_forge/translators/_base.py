"""Translator Protocol — stable contract every CLI translator implements.

Phase 2 fills in real method bodies; this stub locks the interface.
"""

from pathlib import Path
from typing import Literal, Protocol


class Translator(Protocol):
    name: str
    tier: Literal["1a", "1b", "2", "3"]

    def detect(self) -> bool:
        """Is this CLI installed on the current machine?"""
        ...

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        """Map source-relative repo paths → absolute on-disk destinations."""
        ...

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        """Copy or rewrite a skill directory into the target's expected shape."""
        ...

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        """Convert Claude Code agent frontmatter to the target's equivalent."""
        ...

    def translate_command(self, command_md: Path, dest: Path) -> None:
        """Convert a slash command to the target's slash-command format."""
        ...

    def post_install_verify(self, plugin: str) -> bool:
        """Optional: invoke the CLI to confirm the plugin loaded."""
        ...
