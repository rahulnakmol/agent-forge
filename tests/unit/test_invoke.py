"""tests/unit/test_invoke.py"""

from unittest.mock import MagicMock, patch


def test_invoke_skill_uses_claude_api() -> None:
    fake = MagicMock()
    fake.content = [MagicMock(text="Skill output here")]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake
        from evals._invoke import invoke_skill
        result = invoke_skill(
            skill_body="You are a humanizer skill.",
            user_input="Make this human: AI text here.",
            context="casual blog post",
        )
        assert result == "Skill output here"


def test_invoke_skill_prepends_context() -> None:
    fake = MagicMock()
    fake.content = [MagicMock(text="Result")]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake
        from evals._invoke import invoke_skill
        invoke_skill("system", "input text", context="blog")
        call_args = mock_client.return_value.messages.create.call_args
        user_msg = call_args[1]["messages"][0]["content"]
        assert "Context: blog" in user_msg
        assert "input text" in user_msg
