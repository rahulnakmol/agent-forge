"""Guard: no KPMG strings should appear anywhere under plugins/."""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
PLUGINS = REPO / "plugins"
KPMG_RE = re.compile(r"\bkpmg\b", re.IGNORECASE)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".txt", ".ts", ".js"}


def _text_files() -> list[Path]:
    return [
        p for p in PLUGINS.rglob("*")
        if p.is_file() and p.suffix in TEXT_SUFFIXES
    ]


@pytest.mark.parametrize("path", _text_files(), ids=lambda p: str(p.relative_to(PLUGINS)))
def test_no_kpmg_in_text_file(path: Path) -> None:
    body = path.read_text(errors="replace")
    matches = KPMG_RE.findall(body)
    assert not matches, f"{path} contains KPMG references: {matches[:3]}"


def test_no_kpmg_in_filenames() -> None:
    matches = [p for p in PLUGINS.rglob("*") if KPMG_RE.search(p.name)]
    assert not matches, f"KPMG-named files found: {matches}"


def test_no_kpmg_directory() -> None:
    assert not (PLUGINS / "kpmg").exists(), "plugins/kpmg/ must not exist in agent-forge"
