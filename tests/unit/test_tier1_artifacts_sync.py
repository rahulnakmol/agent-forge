"""Verify all Tier 1a generated artifacts are in sync with the canonical source.

If a contributor edits .claude-plugin/marketplace.json or a plugin without
re-running scripts/regenerate-tier1-artifacts.py, this test catches the drift.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_tier1_artifacts_in_sync() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/regenerate-tier1-artifacts.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Tier 1 artifacts drifted from canonical source.\n"
        f"Stdout: {result.stdout}\n"
        f"Run: python scripts/regenerate-tier1-artifacts.py"
    )
