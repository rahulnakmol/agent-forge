"""Every reference linked in a SKILL.md body must exist on disk."""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
SKILLS = sorted((REPO / "plugins").glob("*/skills/*/SKILL.md"))
LINK_RE = re.compile(r"`(references/[^`]+\.md)`|\((references/[^\)]+\.md)\)")


def _id(p: Path) -> str:
    return f"{p.parent.parent.parent.name}/{p.parent.name}"


def _is_concrete_path(ref: str) -> bool:
    """Skip wildcard/template references — only check concrete file paths."""
    return not any(c in ref for c in "*{}|")


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_referenced_files_exist(skill_md: Path) -> None:
    body = skill_md.read_text()
    skill_dir = skill_md.parent
    referenced: set[str] = set()
    for match in LINK_RE.finditer(body):
        ref = match.group(1) or match.group(2)
        if _is_concrete_path(ref):
            referenced.add(ref)
    missing = [r for r in referenced if not (skill_dir / r).exists()]
    assert not missing, f"{skill_md} references missing files: {missing}"
