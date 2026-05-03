"""tests/unit/test_frontmatter.py"""

import pytest
from agent_forge.frontmatter import parse_frontmatter, render_frontmatter


def test_parses_basic_frontmatter() -> None:
    text = "---\nname: humanize\ndescription: Make text feel human\n---\n\nBody here."
    fm, body = parse_frontmatter(text)
    assert fm == {"name": "humanize", "description": "Make text feel human"}
    assert body == "Body here."


def test_returns_empty_dict_when_no_frontmatter() -> None:
    fm, body = parse_frontmatter("Just a body, no frontmatter.")
    assert fm == {}
    assert body == "Just a body, no frontmatter."


def test_renders_frontmatter_back() -> None:
    fm = {"name": "x", "description": "y"}
    body = "Content"
    rendered = render_frontmatter(fm, body)
    parsed_fm, parsed_body = parse_frontmatter(rendered)
    assert parsed_fm == fm
    assert parsed_body == body


def test_handles_lists_in_frontmatter() -> None:
    text = "---\nname: x\ntools: [bash, edit, view]\n---\n\nBody"
    fm, _ = parse_frontmatter(text)
    assert fm["tools"] == ["bash", "edit", "view"]
