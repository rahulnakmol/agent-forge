"""tests/unit/translators/test_kilocode.py"""

from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_kilocode_translator_registered() -> None:
    t = get_translator("kilocode")
    assert t.tier == "2"


def test_target_paths_default_to_claude_skills(ephemeral_home: Path) -> None:
    t = get_translator("kilocode")
    plugin_root = REPO / "plugins/writing"
    paths = t.target_paths(plugin_root)
    for src, dst in paths.items():
        assert ".claude/skills" in str(dst) or ".agents/skills" in str(dst)


def test_translate_skill_copies_directory(ephemeral_home: Path) -> None:
    t = get_translator("kilocode")
    src_skill = REPO / "plugins/writing/skills/humanize"
    dest = ephemeral_home / ".claude/skills/writing/humanize"
    t.translate_skill(src_skill, dest)
    assert (dest / "SKILL.md").exists()
