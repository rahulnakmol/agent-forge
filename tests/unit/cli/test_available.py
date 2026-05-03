"""tests/unit/cli/test_available.py"""

from click.testing import CliRunner
from agent_forge.cli import main


def test_available_lists_all_canonical_plugins() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["available"])
    assert result.exit_code == 0
    for plugin in ("writing", "prompts", "msft-arch", "pm"):
        assert plugin in result.output
