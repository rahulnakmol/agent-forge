"""YAML frontmatter parsing and rendering for SKILL.md / agent .md files."""

import yaml


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) — empty dict if no frontmatter."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm = yaml.safe_load(text[4:end]) or {}
    body = text[end + 5:].lstrip("\n")
    return fm, body


def render_frontmatter(fm: dict, body: str) -> str:
    """Reverse of parse_frontmatter."""
    if not fm:
        return body
    yaml_block = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False).strip()
    return f"---\n{yaml_block}\n---\n\n{body}"
