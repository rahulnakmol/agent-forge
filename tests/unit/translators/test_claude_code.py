"""tests/unit/translators/test_claude_code.py"""

from agent_forge.translators import get_translator


def test_claude_code_translator_registered() -> None:
    t = get_translator("claude-code")
    assert t.name == "claude-code"
    assert t.tier == "1a"


def test_claude_code_translate_skill_is_noop(tmp_path) -> None:
    """Claude format IS canonical — translate_skill should not modify anything."""
    t = get_translator("claude-code")
    t.translate_skill(tmp_path / "src", tmp_path / "dst")
    assert not (tmp_path / "dst").exists()
