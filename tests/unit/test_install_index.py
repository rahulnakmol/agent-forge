"""tests/unit/test_install_index.py"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_install_index_in_sync() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build-install-index.py", "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout
