"""tests/unit/test_judge.py"""

from unittest.mock import MagicMock, patch


def test_judge_returns_float_in_range() -> None:
    fake_response = MagicMock()
    fake_response.content = [MagicMock(text='{"score": 4.2, "reasoning": "Good"}')]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake_response
        from evals._judge import score_against_rubric
        score = score_against_rubric(
            output="Some output text",
            rubric="Rubric criteria here",
            case={"id": "test1", "input": "x"},
            model="claude-haiku-4-5-20251001",
        )
        assert 1.0 <= score <= 5.0


def test_judge_strips_markdown_fences() -> None:
    fake_response = MagicMock()
    fake_response.content = [MagicMock(text='```json\n{"score": 3.5, "reasoning": "Ok"}\n```')]
    with patch("anthropic.Anthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = fake_response
        from evals._judge import score_against_rubric
        score = score_against_rubric(
            output="output", rubric="rubric", case={"id": "x", "input": "y"},
        )
        assert score == 3.5
