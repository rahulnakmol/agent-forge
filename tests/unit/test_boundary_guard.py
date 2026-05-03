"""Boundary guard — proves the deployable boundary is enforced.

This is the lone real test in Phase 0; it guarantees that as we add install
scripts and marketplace.json files in later phases, none of them sneak paths
under tests/, docs/, or scripts/agent_forge/.
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
FORBIDDEN_PATHS = re.compile(r"\b(tests/|docs/|scripts/agent_forge/)")


def _install_scripts() -> list[Path]:
    return list((REPO / "scripts").glob("install-*.sh"))


@pytest.mark.parametrize(
    "script",
    _install_scripts() or [pytest.param(None, id="no-install-scripts-yet")],
)
def test_installer_does_not_reach_outside_plugins(script: Path | None) -> None:
    """Install scripts may only read from plugins/ — never tests/, docs/, or internal scripts."""
    if script is None:
        pytest.skip("No install scripts present yet; will activate in Phase 2.")
    body = script.read_text()
    for lineno, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if FORBIDDEN_PATHS.search(line):
            pytest.fail(
                f"{script.name}:{lineno} reads from non-shippable path: {stripped}"
            )


def test_marketplace_only_declares_plugins() -> None:
    """marketplace.json sources must all be ./plugins/<name>."""
    mp = REPO / ".claude-plugin" / "marketplace.json"
    if not mp.exists():
        pytest.skip("marketplace.json not present yet; will activate in Phase 1.")
    data = json.loads(mp.read_text())
    for plugin in data.get("plugins", []):
        source = plugin.get("source", "")
        assert source.startswith("./plugins/") or source.startswith("plugins/"), (
            f"Plugin {plugin.get('name')} sources outside plugins/: {source}"
        )
