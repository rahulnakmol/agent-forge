"""tests/unit/cli/test_detect.py"""

from click.testing import CliRunner
from agent_forge.cli import main


def test_detect_outputs_each_cli() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["detect"])
    assert result.exit_code == 0
    for cli in ("claude-code", "copilot-cli", "codex-cli", "cursor", "amp", "gemini-cli", "kilocode", "opencode", "crush"):
        assert cli in result.output
