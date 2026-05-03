"""tests/unit/translators/test_gemini_cli.py"""

from agent_forge.translators import get_translator


def test_gemini_translator_registered() -> None:
    t = get_translator("gemini-cli")
    assert t.tier == "1b"


def test_gemini_install_command() -> None:
    t = get_translator("gemini-cli")
    cmd = t.install_command("rahulnakmol/agent-forge")
    assert cmd.startswith("gemini skills install")
    assert "rahulnakmol/agent-forge" in cmd
