"""Read the canonical plugin tree under plugins/<name>/."""

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from agent_forge.frontmatter import parse_frontmatter


@dataclass(frozen=True)
class CanonicalSkill:
    plugin_name: str
    name: str
    skill_dir: Path

    @cached_property
    def skill_md(self) -> Path:
        return self.skill_dir / "SKILL.md"

    @cached_property
    def frontmatter(self) -> dict:
        fm, _ = parse_frontmatter(self.skill_md.read_text())
        return fm

    @cached_property
    def body(self) -> str:
        _, body = parse_frontmatter(self.skill_md.read_text())
        return body

    def references(self) -> list[Path]:
        ref_dir = self.skill_dir / "references"
        return sorted(ref_dir.rglob("*.md")) if ref_dir.exists() else []

    def scripts(self) -> list[Path]:
        sd = self.skill_dir / "scripts"
        return sorted(sd.rglob("*")) if sd.exists() else []

    def assets(self) -> list[Path]:
        ad = self.skill_dir / "assets"
        return sorted(ad.rglob("*")) if ad.exists() else []


@dataclass(frozen=True)
class CanonicalAgent:
    plugin_name: str
    name: str
    md_path: Path

    @cached_property
    def frontmatter(self) -> dict:
        fm, _ = parse_frontmatter(self.md_path.read_text())
        return fm

    @cached_property
    def body(self) -> str:
        _, body = parse_frontmatter(self.md_path.read_text())
        return body


@dataclass(frozen=True)
class CanonicalCommand:
    plugin_name: str
    name: str
    md_path: Path


@dataclass(frozen=True)
class CanonicalPlugin:
    plugin_dir: Path

    @property
    def name(self) -> str:
        return self.plugin_dir.name

    @cached_property
    def manifest(self) -> dict:
        return json.loads((self.plugin_dir / ".claude-plugin" / "plugin.json").read_text())

    def skills(self) -> list[CanonicalSkill]:
        skills_dir = self.plugin_dir / "skills"
        if not skills_dir.exists():
            return []
        result = []
        for sd in sorted(skills_dir.iterdir()):
            if (sd / "SKILL.md").exists():
                result.append(CanonicalSkill(self.name, sd.name, sd))
        return result

    def agents(self) -> list[CanonicalAgent]:
        ad = self.plugin_dir / "agents"
        if not ad.exists():
            return []
        return [
            CanonicalAgent(self.name, p.stem, p)
            for p in sorted(ad.glob("*.md"))
        ]

    def commands(self) -> list[CanonicalCommand]:
        cd = self.plugin_dir / "commands"
        if not cd.exists():
            return []
        return [
            CanonicalCommand(self.name, p.stem, p)
            for p in sorted(cd.glob("*.md"))
        ]


def discover_plugins(plugins_dir: Path) -> list[CanonicalPlugin]:
    """All plugins discovered under plugins/<name>/.claude-plugin/plugin.json."""
    if not plugins_dir.exists():
        return []
    return [
        CanonicalPlugin(p.parent.parent)
        for p in sorted(plugins_dir.glob("*/.claude-plugin/plugin.json"))
    ]
