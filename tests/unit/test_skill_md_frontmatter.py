"""Every SKILL.md across every plugin must have valid agentskills.io frontmatter."""

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent.parent
SKILLS = sorted((REPO / "plugins").glob("*/skills/*/SKILL.md"))


def _id(p: Path) -> str:
    return f"{p.parent.parent.parent.name}/{p.parent.name}"


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def test_at_least_one_skill_exists() -> None:
    assert SKILLS, "no SKILL.md files discovered"


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_skill_has_frontmatter(skill_md: Path) -> None:
    fm = _parse_frontmatter(skill_md.read_text())
    assert fm, f"{skill_md} missing or malformed frontmatter"


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_skill_has_name_and_description(skill_md: Path) -> None:
    fm = _parse_frontmatter(skill_md.read_text())
    assert "name" in fm, f"{skill_md} missing 'name'"
    assert "description" in fm, f"{skill_md} missing 'description'"
    assert fm["name"], "name must be non-empty"
    assert fm["description"], "description must be non-empty"


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_skill_name_within_64_chars(skill_md: Path) -> None:
    fm = _parse_frontmatter(skill_md.read_text())
    assert len(fm["name"]) <= 64, f"name '{fm['name']}' exceeds 64 chars"


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_skill_name_matches_directory(skill_md: Path) -> None:
    """Skill name in frontmatter must match the directory it lives in."""
    fm = _parse_frontmatter(skill_md.read_text())
    dir_name = skill_md.parent.name
    # Allow normalization (some legacy skills may use slightly different conventions)
    assert fm["name"].lower().replace("-", "").replace("_", "") == \
        dir_name.lower().replace("-", "").replace("_", ""), (
        f"name '{fm['name']}' should match directory '{dir_name}'"
    )
