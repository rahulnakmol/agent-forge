"""agent-forge CLI entry point. Real commands land in Phase 3."""

import click


@click.group()
@click.version_option()
def main() -> None:
    """agent-forge — install agent skills and plugins across CLIs."""


@main.command()
def hello() -> None:
    """Smoke-test command, removed in Phase 3."""
    click.echo("agent-forge skeleton: OK")


if __name__ == "__main__":
    main()
