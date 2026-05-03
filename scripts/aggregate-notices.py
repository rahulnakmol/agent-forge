"""Aggregate per-plugin THIRD_PARTY_NOTICES.md files into the top-level one.

Usage:
  python scripts/aggregate-notices.py            # rewrite the file
  python scripts/aggregate-notices.py --check    # exit 1 if drift detected
"""

import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOP_LEVEL = REPO / "THIRD_PARTY_NOTICES.md"

HEADER = """# Third-Party Notices

This file aggregates per-plugin third-party attributions into one place.
Generated automatically by `scripts/aggregate-notices.py` — do not edit by hand.

## Repository license

The agent-forge project is licensed under BSD-3-Clause (see `LICENSE`).

---

"""


def build() -> str:
    body = HEADER
    for plugin_notices in sorted((REPO / "plugins").glob("*/THIRD_PARTY_NOTICES.md")):
        plugin = plugin_notices.parent.name
        body += f"## Plugin: {plugin}\n\n"
        body += plugin_notices.read_text() + "\n\n---\n\n"
    return body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        actual = TOP_LEVEL.read_text() if TOP_LEVEL.exists() else ""
        if actual != expected:
            print("THIRD_PARTY_NOTICES.md drifted from per-plugin sources")
            raise SystemExit(1)
    else:
        TOP_LEVEL.write_text(expected)


if __name__ == "__main__":
    main()
