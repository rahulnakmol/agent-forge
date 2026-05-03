"""Tier 3 prompt-loader generator for Perplexity Spaces, ChatGPT custom GPTs,
and Claude.ai Projects."""

from pathlib import Path

from agent_forge.canonical import CanonicalSkill
from agent_forge.translators import register

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

LOADER_TEMPLATE = """---
name: {name}
description: {description}
source: https://github.com/{repo}/tree/{branch}/plugins/{plugin}/skills/{skill}
---

# {name} Skill (loader)

This is a thin loader. The actual skill body and references are fetched on
demand to preserve progressive disclosure (UNIX-style — load only what you need).

**When to invoke this skill:** {description}

**Skill body** (read first when triggered):
{skill_url}

**References** (load only when SKILL.md instructs you to):
{references_block}

**Instructions to the host LLM:** When this skill is triggered, fetch the body
above. Do NOT eagerly fetch references — only retrieve a reference when the
body's instructions explicitly tell you to.
"""


def build_loader_md(skill: CanonicalSkill, repo: str, branch: str = "main") -> str:
    base = f"https://raw.githubusercontent.com/{repo}/{branch}"
    skill_url = f"{base}/plugins/{skill.plugin_name}/skills/{skill.name}/SKILL.md"
    refs = skill.references()
    if refs:
        ref_lines = []
        for r in refs:
            rel = r.relative_to(REPO_ROOT).as_posix()
            ref_lines.append(f"- {r.stem}: {base}/{rel}")
        ref_block = "\n".join(ref_lines)
    else:
        ref_block = "_(no references defined for this skill)_"
    return LOADER_TEMPLATE.format(
        name=skill.frontmatter["name"],
        description=skill.frontmatter["description"],
        repo=repo,
        branch=branch,
        plugin=skill.plugin_name,
        skill=skill.name,
        skill_url=skill_url,
        references_block=ref_block,
    )


class PromptLoaderTranslator:
    name = "prompt-loader"
    tier = "3"

    def detect(self) -> bool:
        return False

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(PromptLoaderTranslator())
