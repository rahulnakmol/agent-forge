"""tests/unit/translators/test_crush.py"""

from pathlib import Path

from agent_forge.translators import get_translator

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_crush_translator_registered() -> None:
    t = get_translator("crush")
    assert t.tier == "2"


def test_translate_skill_copies(ephemeral_home: Path) -> None:
    t = get_translator("crush")
    src = REPO / "plugins/writing/skills/humanize"
    dest = ephemeral_home / ".claude/skills/writing/humanize"
    t.translate_skill(src, dest)
    assert (dest / "SKILL.md").exists()
