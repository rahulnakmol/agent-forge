"""tests/unit/test_aggregate_notices.py"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_third_party_notices_in_sync() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/aggregate-notices.py", "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"THIRD_PARTY_NOTICES.md drifted:\n{result.stdout}"
