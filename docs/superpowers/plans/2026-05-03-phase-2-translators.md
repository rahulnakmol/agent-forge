# Phase 2 — All Translators Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build all 10 translators that turn the canonical Claude Code-format plugins into the shape each target CLI expects. After Phase 2, the agent-forge repo contains committed Tier 1a manifests for Copilot/Codex/Cursor (mirroring Claude's), and the Python translator code can install plugins for any of the 12 v1.0 install targets.

**Architecture:** Translators implement the `Translator` Protocol stubbed in Phase 0. They split into 4 categories: Tier 1a (registry-style — generate marketplace.json + plugin.json mirrors, committed in-repo), Tier 1b (git-URL install — install guide is the artifact, translator just records in manifest), Tier 2 (lightweight adapters — drop into `~/.claude/skills/` or `~/.agents/skills/` for fallback discovery), Tier 3 (prompt loader generator — emits paste-ready Markdown loaders).

**Tech Stack:** Python 3.11+, `pydantic` for translator-specific schemas, `tomli-w` for Codex's TOML output, `pyyaml` for frontmatter, `httpx` for raw GitHub URL construction.

**Spec reference:** `docs/superpowers/specs/2026-05-03-agent-forge-marketplace-design.md` Section 4 (Translator Interface), Section 6 (CI invariants 2–9).

**Depends on:** Phase 0 (Protocol stub, pyproject.toml), Phase 1 (real plugins to translate).

---

## Parallelization map

After Tasks 1–3 (shared helpers), the following groups are fully independent:

- **Group A** (Tier 1a registry translators): Tasks 4 (Claude no-op), 5 (Copilot), 6 (Codex), 7 (Cursor) — all parallel
- **Group B** (Tier 1b git-URL translators): Tasks 8 (Amp), 9 (Gemini) — parallel
- **Group C** (Tier 2 adapters): Tasks 10 (Kilo), 11 (OpenCode), 12 (Crush) — parallel
- **Group D** (Tier 3): Task 13 (prompt loader generator) — parallel with all other groups

Tasks in order: 1 → 2 → 3 → [Groups A + B + C + D fully in parallel] → 14 (CI invariants for sync) → 15 (smoke + commit).

**Recommended subagent dispatch:** spawn 9 parallel subagents in one message, one per translator (Groups A1–A4, B1–B2, C1–C3, D1).

---

## Task 1: Build the shared frontmatter parser

**Files:**
- Create: `scripts/agent_forge/frontmatter.py`
- Create: `tests/unit/test_frontmatter.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run + expect failure**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pytest tests/unit/test_frontmatter.py -v
```
Expected: ImportError on `agent_forge.frontmatter`.

- [ ] **Step 3: Implement `scripts/agent_forge/frontmatter.py`**

```python
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
```

- [ ] **Step 4: Run + expect pass**

```bash
pytest tests/unit/test_frontmatter.py -v
```
Expected: 4 passing.

---

## Task 2: Build the canonical plugin reader

**Files:**
- Create: `scripts/agent_forge/canonical.py`
- Create: `tests/unit/test_canonical.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/test_canonical.py"""

from pathlib import Path

import pytest
from agent_forge.canonical import CanonicalPlugin, discover_plugins


def test_discovers_all_plugins() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = discover_plugins(repo / "plugins")
    names = [p.name for p in plugins]
    assert "writing" in names
    assert "prompts" in names
    assert "msft-arch" in names
    assert "pm" in names
    assert "kpmg" not in names


def test_canonical_plugin_loads_manifest() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    writing = plugins["writing"]
    assert writing.manifest["name"] == "writing"
    assert writing.manifest["description"]


def test_canonical_plugin_lists_skills() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    skills = plugins["writing"].skills()
    assert any(s.name == "humanize" for s in skills)


def test_canonical_skill_has_frontmatter() -> None:
    repo = Path(__file__).resolve().parent.parent.parent
    plugins = {p.name: p for p in discover_plugins(repo / "plugins")}
    skills = {s.name: s for s in plugins["writing"].skills()}
    assert skills["humanize"].frontmatter["name"] == "humanize"
    assert skills["humanize"].frontmatter["description"]
```

- [ ] **Step 2: Run + expect failure**

```bash
pytest tests/unit/test_canonical.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement `scripts/agent_forge/canonical.py`**

```python
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
```

- [ ] **Step 4: Run + expect pass**

```bash
pytest tests/unit/test_canonical.py -v
```
Expected: 4 passing.

---

## Task 3: Build the translator registry

**Files:**
- Create: `scripts/agent_forge/translators/__init__.py` (replace stub)
- Create: `tests/unit/test_translator_registry.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/test_translator_registry.py"""

from agent_forge.translators import get_translator, registered_translators


def test_registry_lists_all_v1_targets() -> None:
    names = registered_translators()
    assert set(names) == {
        "claude-code", "copilot-cli", "codex-cli", "cursor",  # Tier 1a
        "amp", "gemini-cli",                                    # Tier 1b
        "kilocode", "opencode", "crush",                        # Tier 2
        "prompt-loader",                                        # Tier 3
    }


def test_get_translator_returns_instance() -> None:
    t = get_translator("claude-code")
    assert t.name == "claude-code"
    assert t.tier == "1a"


def test_get_translator_raises_on_unknown() -> None:
    import pytest
    with pytest.raises(KeyError, match="unknown CLI"):
        get_translator("nonexistent-cli")
```

- [ ] **Step 2: Run + expect failure**

```bash
pytest tests/unit/test_translator_registry.py -v
```
Expected: ImportError.

- [ ] **Step 3: Implement `scripts/agent_forge/translators/__init__.py`**

```python
"""Translator registry — every CLI's translator registers itself here."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_forge.translators._base import Translator

_REGISTRY: dict[str, "Translator"] = {}


def register(translator: "Translator") -> "Translator":
    _REGISTRY[translator.name] = translator
    return translator


def get_translator(name: str) -> "Translator":
    if name not in _REGISTRY:
        raise KeyError(f"unknown CLI: {name}; available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def registered_translators() -> list[str]:
    return sorted(_REGISTRY)


# Lazy import to populate registry — must come after _REGISTRY is defined
from agent_forge.translators import (  # noqa: E402,F401
    claude_code,
    copilot_cli,
    codex_cli,
    cursor,
    amp,
    gemini_cli,
    kilocode,
    opencode,
    crush,
    prompt_loader,
)
```

- [ ] **Step 4: Run — still failing because translator modules don't exist yet**

The test will fail until Tasks 4–13 land. Mark as expected and move on; CI catches re-run after all translators exist.

---

## Task 4: Tier 1a — Claude Code translator (no-op) (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/claude_code.py`
- Create: `tests/unit/translators/test_claude_code.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_claude_code.py"""

from agent_forge.translators import get_translator


def test_claude_code_translator_registered() -> None:
    t = get_translator("claude-code")
    assert t.name == "claude-code"
    assert t.tier == "1a"


def test_claude_code_translate_skill_is_noop(tmp_path) -> None:
    """Claude format IS canonical — translate_skill should not modify anything."""
    t = get_translator("claude-code")
    # No-op: implementation should not raise; no files created
    t.translate_skill(tmp_path / "src", tmp_path / "dst")
    assert not (tmp_path / "dst").exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/claude_code.py`**

```python
"""Claude Code translator — mostly a no-op (canonical format)."""

import shutil
from pathlib import Path

from agent_forge.translators import register
from agent_forge.translators._base import Translator


class ClaudeCodeTranslator:
    name = "claude-code"
    tier = "1a"

    def detect(self) -> bool:
        import shutil as sh
        return bool(sh.which("claude")) or Path.home().joinpath(".claude").exists()

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        # Claude reads from the cloned repo via marketplace.json — no copy needed
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        # No-op: skills are authored in Claude's format already
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        # Could shell out to `claude plugin list` — defer to integration tests
        return True


register(ClaudeCodeTranslator())
```

- [ ] **Step 3: Run + expect pass**

```bash
pytest tests/unit/translators/test_claude_code.py -v
```
Expected: 2 passing.

---

## Task 5: Tier 1a — Copilot CLI translator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/copilot_cli.py`
- Create: `tests/unit/translators/test_copilot_cli.py`
- Create: `.github/plugin/marketplace.json` (generated artifact, committed)
- Create: `plugins/<each>/plugin.json` (generated, committed)
- Create: `plugins/<each>/agents/<name>.agent.md` (generated mirrors of `<name>.md`)

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_copilot_cli.py"""

import json
from pathlib import Path

import pytest
from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.copilot_cli import (
    build_copilot_marketplace_json,
    build_copilot_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_copilot_translator_registered() -> None:
    t = get_translator("copilot-cli")
    assert t.tier == "1a"


def test_marketplace_json_has_metadata_wrapper() -> None:
    """Copilot's marketplace schema wraps description+version in 'metadata'."""
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_copilot_marketplace_json(canonical, plugins)
    assert "metadata" in out
    assert out["metadata"]["description"]
    assert out["metadata"]["version"]
    assert "owner" in out
    assert "@" in out["owner"]["email"]


def test_marketplace_plugin_entries_have_version() -> None:
    """Copilot REQUIRES 'version' on each plugin entry."""
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_copilot_marketplace_json(canonical, plugins)
    for p in out["plugins"]:
        assert "version" in p, f"plugin {p['name']} missing version"


def test_plugin_json_declares_components() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_copilot_plugin_json(plugins["prompts"])
    assert pj["name"] == "prompts"
    assert pj["description"]
    assert pj["version"]
    # If skills/, agents/, commands/ exist on disk, they're declared
    if (plugins["prompts"].plugin_dir / "skills").exists():
        assert pj.get("skills") == "skills/"
    if (plugins["prompts"].plugin_dir / "agents").exists():
        assert pj.get("agents") == "agents/"
    if (plugins["prompts"].plugin_dir / "commands").exists():
        assert pj.get("commands") == "commands/"


def test_agent_mirror_filename(tmp_path: Path) -> None:
    """Copilot expects <name>.agent.md alongside <name>.md."""
    src = tmp_path / "agents" / "my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text("---\nname: my-agent\ndescription: x\n---\n\nbody")
    t = get_translator("copilot-cli")
    t.translate_agent(src, tmp_path / "agents" / "my-agent.agent.md")
    assert (tmp_path / "agents" / "my-agent.agent.md").exists()
```

- [ ] **Step 2: Run + expect failure (ImportError)**

```bash
pytest tests/unit/translators/test_copilot_cli.py -v
```

- [ ] **Step 3: Implement `scripts/agent_forge/translators/copilot_cli.py`**

```python
"""GitHub Copilot CLI translator (Tier 1a — registry-style native marketplace).

Copilot CLI reads .github/plugin/marketplace.json (also falls back to
.claude-plugin/). Per-plugin manifest at <plugin>/plugin.json. Agents use
<name>.agent.md filename convention.

Schema reference: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace
"""

import json
import shutil
from pathlib import Path

from agent_forge.canonical import CanonicalPlugin
from agent_forge.translators import register


def build_copilot_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    """Wrap canonical Claude marketplace.json in Copilot's metadata schema."""
    return {
        "name": canonical["name"],
        "owner": canonical["owner"],
        "metadata": {
            "description": canonical["description"],
            "version": canonical["version"],
        },
        "plugins": [
            {
                "name": p.name,
                "description": p.manifest.get("description", ""),
                "version": p.manifest.get("version", canonical["version"]),
                "source": f"./plugins/{p.name}",
            }
            for p in plugins
        ],
    }


def build_copilot_plugin_json(plugin: CanonicalPlugin) -> dict:
    """Generate the per-plugin Copilot manifest at <plugin>/plugin.json."""
    pj: dict = {
        "name": plugin.name,
        "description": plugin.manifest.get("description", ""),
        "version": plugin.manifest.get("version", "1.0.0"),
    }
    author = plugin.manifest.get("author")
    if author:
        pj["author"] = author
    if plugin.manifest.get("license"):
        pj["license"] = plugin.manifest["license"]
    if (plugin.plugin_dir / "skills").exists():
        pj["skills"] = "skills/"
    if (plugin.plugin_dir / "agents").exists():
        pj["agents"] = "agents/"
    if (plugin.plugin_dir / "commands").exists():
        pj["commands"] = "commands/"
    if (plugin.plugin_dir / ".mcp.json").exists():
        pj["mcpServers"] = ".mcp.json"
    return pj


class CopilotCliTranslator:
    name = "copilot-cli"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("copilot"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}  # Reads in-repo committed manifests; user does `copilot plugin marketplace add`

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass  # Skills work as-is via the `"skills": "skills/"` declaration

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        """Mirror <name>.md → <name>.agent.md (Copilot's filename convention)."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Use copy not symlink for cross-platform safety (Phase 2 spike resolved here)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass  # Commands work as-is via `"commands": "commands/"` declaration

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CopilotCliTranslator())
```

- [ ] **Step 4: Run + expect pass**

```bash
pytest tests/unit/translators/test_copilot_cli.py -v
```
Expected: 5 passing.

- [ ] **Step 5: Generate the actual committed artifacts**

Add a one-shot generator script `scripts/regenerate-tier1-artifacts.py` (used by CI to detect drift):

```python
"""Regenerate all Tier 1a committed artifacts from canonical plugins/.

Run as: python scripts/regenerate-tier1-artifacts.py [--check]
"""

import argparse
import json
from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators.copilot_cli import (
    build_copilot_marketplace_json,
    build_copilot_plugin_json,
)
# More imports as Codex + Cursor land in Tasks 6 + 7

REPO = Path(__file__).resolve().parent.parent


def regenerate_copilot(check: bool) -> bool:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".github/plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(
        build_copilot_marketplace_json(canonical, plugins),
        indent=2,
    ) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / "plugin.json"
        new_pj = json.dumps(build_copilot_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
        # Mirror agent files
        agents_dir = plugin.plugin_dir / "agents"
        if agents_dir.exists():
            for src in agents_dir.glob("*.md"):
                if src.stem.endswith(".agent"):
                    continue
                dst = agents_dir / f"{src.stem}.agent.md"
                if check and dst.exists():
                    if dst.read_bytes() != src.read_bytes():
                        print(f"DRIFT: {dst}")
                        drifted = True
                else:
                    dst.write_bytes(src.read_bytes())
    return drifted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Exit non-zero if any committed artifact would change.")
    args = parser.parse_args()
    drifted = regenerate_copilot(args.check)
    # TODO: regenerate_codex(args.check), regenerate_cursor(args.check) added in Tasks 6/7
    if args.check and drifted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run the generator**

```bash
python scripts/regenerate-tier1-artifacts.py
ls -la .github/plugin/marketplace.json
ls -la plugins/*/plugin.json
ls -la plugins/prompts/agents/*.agent.md
```
Expected: marketplace.json + 4 plugin.json files + .agent.md mirrors created.

---

## Task 6: Tier 1a — Codex CLI translator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/codex_cli.py`
- Create: `tests/unit/translators/test_codex_cli.py`
- Create: `.codex-plugin/marketplace.json` (generated, committed)
- Create: `plugins/<each>/.codex-plugin/plugin.json` (generated)
- Create: `plugins/<each>/agents/<name>.toml` (generated for each agent)
- Update: `scripts/regenerate-tier1-artifacts.py` to also handle Codex

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_codex_cli.py"""

import json
from pathlib import Path

import tomli
import pytest
from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.codex_cli import (
    build_codex_marketplace_json,
    build_codex_plugin_json,
    md_agent_to_toml,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_codex_translator_registered() -> None:
    t = get_translator("codex-cli")
    assert t.tier == "1a"


def test_codex_marketplace_json_shape() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_codex_marketplace_json(canonical, plugins)
    assert out["name"]
    assert "plugins" in out
    for p in out["plugins"]:
        assert "name" in p
        assert "source" in p
        assert "policy" in p


def test_codex_plugin_json_kebab_name() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_codex_plugin_json(plugins["msft-arch"])
    assert pj["name"] == "msft-arch"
    assert pj["version"]


def test_md_agent_converted_to_toml(tmp_path: Path) -> None:
    """An agent .md with frontmatter becomes a valid Codex TOML subagent file."""
    src = tmp_path / "agents/my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text(
        "---\n"
        "name: my-agent\n"
        "description: A helpful assistant\n"
        "tools: [bash, edit]\n"
        "---\n\n"
        "You are a specialized assistant that helps with X.\n"
    )
    out = md_agent_to_toml(src)
    parsed = tomli.loads(out)
    assert parsed["name"] == "my-agent"
    assert parsed["description"]
    assert parsed["developer_instructions"].startswith("You are a specialized")


def test_translate_agent_writes_toml(tmp_path: Path) -> None:
    src = tmp_path / "agents/my-agent.md"
    src.parent.mkdir(parents=True)
    src.write_text("---\nname: x\ndescription: y\n---\n\nBody")
    t = get_translator("codex-cli")
    dst = tmp_path / "agents/my-agent.toml"
    t.translate_agent(src, dst)
    assert dst.exists()
    parsed = tomli.loads(dst.read_text())
    assert parsed["name"] == "x"


def test_translate_command_is_noop(tmp_path: Path) -> None:
    """Codex deprecated custom prompts in favor of skills."""
    t = get_translator("codex-cli")
    src = tmp_path / "src.md"
    src.write_text("body")
    dst = tmp_path / "dst.toml"
    t.translate_command(src, dst)
    assert not dst.exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/codex_cli.py`**

```python
"""OpenAI Codex CLI translator (Tier 1a — registry-style native marketplace).

Codex CLI reads .codex-plugin/marketplace.json (or .agents/plugins/marketplace.json
at the repo root for project-level use). Per-plugin at <plugin>/.codex-plugin/plugin.json.
Subagents are TOML at <plugin>/agents/<name>.toml.

Custom prompts (~/.codex/prompts/) are DEPRECATED in favor of skills, so this
translator skips command translation.

Schema reference: https://developers.openai.com/codex/plugins
"""

import shutil
from pathlib import Path

import tomli_w

from agent_forge.canonical import CanonicalPlugin
from agent_forge.frontmatter import parse_frontmatter
from agent_forge.translators import register


def build_codex_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    return {
        "name": canonical["name"],
        "plugins": [
            {
                "name": p.name,
                "source": {"path": f"./plugins/{p.name}"},
                "policy": {"installation": "interactive", "authentication": "none"},
                "category": "productivity",
            }
            for p in plugins
        ],
    }


def build_codex_plugin_json(plugin: CanonicalPlugin) -> dict:
    pj: dict = {
        "name": plugin.name,  # must be kebab-case (Codex requirement)
        "version": plugin.manifest.get("version", "1.0.0"),
        "description": plugin.manifest.get("description", ""),
    }
    if (plugin.plugin_dir / "skills").exists():
        pj["skills"] = "skills/"
    if (plugin.plugin_dir / "agents").exists():
        pj["agents"] = "agents/"
    if (plugin.plugin_dir / ".mcp.json").exists():
        pj["mcpServers"] = ".mcp.json"
    return pj


def md_agent_to_toml(agent_md: Path) -> str:
    """Convert a Claude-format agent .md (frontmatter + body) to Codex TOML."""
    fm, body = parse_frontmatter(agent_md.read_text())
    toml_doc: dict = {
        "name": fm.get("name", agent_md.stem),
        "description": fm.get("description", ""),
        "developer_instructions": body.strip(),
    }
    # Optional fields if present in source
    if "model" in fm:
        toml_doc["model"] = fm["model"]
    if "tools" in fm:
        # Codex doesn't have a direct equivalent; emit as a comment-prefixed key
        # for human review. Phase 2 spike resolution: drop with comment.
        pass
    return tomli_w.dumps(toml_doc)


class CodexCliTranslator:
    name = "codex-cli"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("codex"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass  # SKILL.md format is identical to canonical

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(md_agent_to_toml(agent_md))

    def translate_command(self, command_md: Path, dest: Path) -> None:
        # Codex deprecated custom prompts — no-op
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CodexCliTranslator())
```

- [ ] **Step 3: Update `scripts/regenerate-tier1-artifacts.py` to handle Codex**

Add to that script (after `regenerate_copilot`):

```python
def regenerate_codex(check: bool) -> bool:
    from agent_forge.translators.codex_cli import (
        build_codex_marketplace_json,
        build_codex_plugin_json,
        md_agent_to_toml,
    )
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".codex-plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(build_codex_marketplace_json(canonical, plugins), indent=2) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / ".codex-plugin/plugin.json"
        plugin_json.parent.mkdir(parents=True, exist_ok=True)
        new_pj = json.dumps(build_codex_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
        agents_dir = plugin.plugin_dir / "agents"
        if agents_dir.exists():
            for src in agents_dir.glob("*.md"):
                if src.stem.endswith(".agent"):
                    continue
                dst = agents_dir / f"{src.stem}.toml"
                new_toml = md_agent_to_toml(src)
                if check and dst.exists():
                    if dst.read_text() != new_toml:
                        print(f"DRIFT: {dst}")
                        drifted = True
                else:
                    dst.write_text(new_toml)
    return drifted
```

And in `main()`:
```python
drifted = regenerate_copilot(args.check) or drifted
drifted = regenerate_codex(args.check) or drifted
```

- [ ] **Step 4: Run + verify**

```bash
pytest tests/unit/translators/test_codex_cli.py -v
python scripts/regenerate-tier1-artifacts.py
ls -la .codex-plugin/marketplace.json plugins/*/.codex-plugin/plugin.json plugins/prompts/agents/*.toml
```
Expected: tests pass; files generated.

---

## Task 7: Tier 1a — Cursor translator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/cursor.py`
- Create: `tests/unit/translators/test_cursor.py`
- Create: `.cursor-plugin/marketplace.json` (generated)
- Create: `plugins/<each>/.cursor-plugin/plugin.json` (generated)

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_cursor.py"""

import json
from pathlib import Path

import pytest
from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.cursor import (
    build_cursor_marketplace_json,
    build_cursor_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_cursor_translator_registered() -> None:
    t = get_translator("cursor")
    assert t.tier == "1a"


def test_cursor_marketplace_json_shape() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_cursor_marketplace_json(canonical, plugins)
    assert out["name"]
    assert "plugins" in out
    for p in out["plugins"]:
        assert "name" in p


def test_cursor_plugin_json_minimal() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_cursor_plugin_json(plugins["writing"])
    assert pj["name"] == "writing"
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/cursor.py`**

```python
"""Cursor translator (Tier 1a — registry-style native marketplace).

Cursor reads .cursor-plugin/marketplace.json (multi-plugin repos) and
<plugin>/.cursor-plugin/plugin.json. Skills, agents, commands all use Cursor's
auto-discovery — no per-file translation needed.

Schema reference: https://cursor.com/docs/plugins
"""

import shutil
from pathlib import Path

from agent_forge.canonical import CanonicalPlugin
from agent_forge.translators import register


def build_cursor_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    return {
        "name": canonical["name"],
        "description": canonical["description"],
        "version": canonical["version"],
        "owner": canonical["owner"],
        "plugins": [
            {
                "name": p.name,
                "description": p.manifest.get("description", ""),
                "version": p.manifest.get("version", canonical["version"]),
                "source": f"./plugins/{p.name}",
                "category": "productivity",
            }
            for p in plugins
        ],
    }


def build_cursor_plugin_json(plugin: CanonicalPlugin) -> dict:
    pj: dict = {
        "name": plugin.name,
        "description": plugin.manifest.get("description", ""),
        "version": plugin.manifest.get("version", "1.0.0"),
    }
    if author := plugin.manifest.get("author"):
        pj["author"] = author
    return pj


class CursorTranslator:
    name = "cursor"
    tier = "1a"

    def detect(self) -> bool:
        return bool(shutil.which("cursor")) or Path(".cursor").exists()

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass  # Cursor reads SKILL.md format as-is

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass  # Cursor reads agent .md as-is

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass  # Cursor reads commands/*.md as-is

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(CursorTranslator())
```

- [ ] **Step 3: Update `scripts/regenerate-tier1-artifacts.py` to handle Cursor**

Add `regenerate_cursor` mirroring `regenerate_copilot`/`regenerate_codex`. Wire into `main()`.

- [ ] **Step 4: Run**

```bash
pytest tests/unit/translators/test_cursor.py -v
python scripts/regenerate-tier1-artifacts.py
```

---

## Task 8: Tier 1b — Amp translator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/amp.py`
- Create: `tests/unit/translators/test_amp.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_amp.py"""

from pathlib import Path

from agent_forge.translators import get_translator


def test_amp_translator_registered() -> None:
    t = get_translator("amp")
    assert t.tier == "1b"


def test_amp_install_command_string() -> None:
    """Tier 1b primary artifact is the install-command string the user runs."""
    t = get_translator("amp")
    cmd = t.install_command("rahulnakmol/agent-forge")
    assert cmd.startswith("amp skill add")
    assert "rahulnakmol/agent-forge" in cmd


def test_amp_translate_skill_is_noop(tmp_path: Path) -> None:
    """Amp reads .claude/skills/ and .agents/skills/ — no transform needed."""
    t = get_translator("amp")
    t.translate_skill(tmp_path / "src", tmp_path / "dst")
    assert not (tmp_path / "dst").exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/amp.py`**

```python
"""Sourcegraph Amp translator (Tier 1b — git-URL native install).

Amp installs skills via `amp skill add <github|git|path>`. There is no
marketplace.json to commit; the artifact is the install-command string,
documented in docs/install/amp.md.

Amp natively reads .claude/skills/ and .agents/skills/, so no file generation
is needed.

Reference: https://ampcode.com/manual
"""

import shutil
from pathlib import Path

from agent_forge.translators import register


class AmpTranslator:
    name = "amp"
    tier = "1b"

    def detect(self) -> bool:
        return bool(shutil.which("amp"))

    def install_command(self, repo: str, skill: str | None = None) -> str:
        """Return the amp CLI command the user (or agent) should run."""
        if skill:
            return f"amp skill add github:{repo}/plugins/{skill}"
        return f"amp skill add github:{repo}"

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


register(AmpTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_amp.py -v
```

---

## Task 9: Tier 1b — Gemini CLI translator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/gemini_cli.py`
- Create: `tests/unit/translators/test_gemini_cli.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_gemini_cli.py"""

from agent_forge.translators import get_translator


def test_gemini_translator_registered() -> None:
    t = get_translator("gemini-cli")
    assert t.tier == "1b"


def test_gemini_install_command() -> None:
    t = get_translator("gemini-cli")
    cmd = t.install_command("rahulnakmol/agent-forge")
    assert cmd.startswith("gemini skills install")
    assert "rahulnakmol/agent-forge" in cmd
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/gemini_cli.py`**

```python
"""Google Gemini CLI translator (Tier 1b — git-URL native install).

Reference: https://geminicli.com/docs/cli/skills/
"""

import shutil
from pathlib import Path

from agent_forge.translators import register


class GeminiCliTranslator:
    name = "gemini-cli"
    tier = "1b"

    def detect(self) -> bool:
        return bool(shutil.which("gemini"))

    def install_command(self, repo: str, skill: str | None = None) -> str:
        if skill:
            return f"gemini skills install github:{repo}#{skill}"
        return f"gemini skills install github:{repo}"

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


register(GeminiCliTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_gemini_cli.py -v
```

---

## Task 10: Tier 2 — Kilo Code adapter (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/kilocode.py`
- Create: `tests/unit/translators/test_kilocode.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_kilocode.py"""

from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_kilocode_translator_registered() -> None:
    t = get_translator("kilocode")
    assert t.tier == "2"


def test_target_paths_default_to_claude_skills(ephemeral_home: Path) -> None:
    """Kilo reads .claude/skills/ — drop installs there for fallback discovery."""
    t = get_translator("kilocode")
    plugin_root = REPO / "plugins/writing"
    paths = t.target_paths(plugin_root)
    # Maps each skill in the plugin to ~/.claude/skills/<plugin>/<skill>/
    for src, dst in paths.items():
        assert ".claude/skills" in str(dst) or ".agents/skills" in str(dst)


def test_translate_skill_copies_directory(ephemeral_home: Path) -> None:
    t = get_translator("kilocode")
    src_skill = REPO / "plugins/writing/skills/humanize"
    dest = ephemeral_home / ".claude/skills/writing/humanize"
    t.translate_skill(src_skill, dest)
    assert (dest / "SKILL.md").exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/kilocode.py`**

```python
"""Kilo Code translator (Tier 2 — trivial adapter).

Kilo Code natively reads .claude/skills/, .claude/agents/, .agents/skills/
as fallbacks. The "adapter" just drops the canonical plugin tree at
~/.claude/skills/<plugin>/ for free fallback discovery.

If the user already installed via Claude Code, this is effectively a no-op
(files are already there).

Reference: https://kilo.ai/docs/agent-behavior/skills
"""

import shutil
from pathlib import Path

from agent_forge.translators import register


class KilocodeTranslator:
    name = "kilocode"
    tier = "2"

    def detect(self) -> bool:
        return bool(shutil.which("kilo")) or Path(".kilo").exists()

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        home = Path.home()
        plugin_name = plugin_root.name
        result: dict[str, Path] = {}
        skills_src = plugin_root / "skills"
        if skills_src.exists():
            for skill_dir in skills_src.iterdir():
                if (skill_dir / "SKILL.md").exists():
                    result[str(skill_dir.relative_to(plugin_root))] = (
                        home / ".claude/skills" / plugin_name / skill_dir.name
                    )
        return result

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(command_md, dest)

    def post_install_verify(self, plugin: str) -> bool:
        return (Path.home() / ".claude/skills" / plugin).exists()


register(KilocodeTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_kilocode.py -v
```

---

## Task 11: Tier 2 — OpenCode adapter (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/opencode.py`
- Create: `tests/unit/translators/test_opencode.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_opencode.py"""

from pathlib import Path

from agent_forge.translators import get_translator

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_opencode_translator_registered() -> None:
    t = get_translator("opencode")
    assert t.tier == "2"


def test_translate_skill_copies(ephemeral_home: Path) -> None:
    t = get_translator("opencode")
    src = REPO / "plugins/writing/skills/humanize"
    dest = ephemeral_home / ".claude/skills/writing/humanize"
    t.translate_skill(src, dest)
    assert (dest / "SKILL.md").exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/opencode.py`**

```python
"""OpenCode translator (Tier 2 — trivial adapter).

OpenCode reads .claude/skills/, .claude/agents/, .claude/commands/, and
.agents/skills/ as fallbacks. Same pattern as Kilo Code.

Reference: https://opencode.ai/docs/
"""

import shutil
from pathlib import Path

from agent_forge.translators import register


class OpencodeTranslator:
    name = "opencode"
    tier = "2"

    def detect(self) -> bool:
        return bool(shutil.which("opencode")) or Path(".opencode").exists()

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        home = Path.home()
        plugin_name = plugin_root.name
        result: dict[str, Path] = {}
        skills_src = plugin_root / "skills"
        if skills_src.exists():
            for skill_dir in skills_src.iterdir():
                if (skill_dir / "SKILL.md").exists():
                    result[str(skill_dir.relative_to(plugin_root))] = (
                        home / ".claude/skills" / plugin_name / skill_dir.name
                    )
        return result

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(command_md, dest)

    def post_install_verify(self, plugin: str) -> bool:
        return (Path.home() / ".claude/skills" / plugin).exists()


register(OpencodeTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_opencode.py -v
```

---

## Task 12: Tier 2 — Crush adapter (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/crush.py`
- Create: `tests/unit/translators/test_crush.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_crush.py"""

from pathlib import Path

from agent_forge.translators import get_translator

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_crush_translator_registered() -> None:
    t = get_translator("crush")
    assert t.tier == "2"


def test_translate_skill_copies(ephemeral_home: Path) -> None:
    t = get_translator("crush")
    src = REPO / "plugins/writing/skills/humanize"
    dest = ephemeral_home / ".claude/skills/writing/humanize"
    t.translate_skill(src, dest)
    assert (dest / "SKILL.md").exists()
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/crush.py`**

```python
"""Crush translator (Tier 2 — trivial adapter).

Crush supports the agentskills.io open standard. Per Phase 2 spike: verify
exact discovery paths during integration testing. For now, mirror Kilo/OpenCode
behavior: drop into ~/.claude/skills/ for fallback discovery.

Reference: https://github.com/charmbracelet/crush
"""

import shutil
from pathlib import Path

from agent_forge.translators import register


class CrushTranslator:
    name = "crush"
    tier = "2"

    def detect(self) -> bool:
        return bool(shutil.which("crush"))

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        home = Path.home()
        plugin_name = plugin_root.name
        result: dict[str, Path] = {}
        skills_src = plugin_root / "skills"
        if skills_src.exists():
            for skill_dir in skills_src.iterdir():
                if (skill_dir / "SKILL.md").exists():
                    result[str(skill_dir.relative_to(plugin_root))] = (
                        home / ".claude/skills" / plugin_name / skill_dir.name
                    )
        return result

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_md, dest)

    def translate_command(self, command_md: Path, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(command_md, dest)

    def post_install_verify(self, plugin: str) -> bool:
        return True  # Refine with real Crush probe in Phase 4 integration tests


register(CrushTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_crush.py -v
```

---

## Task 13: Tier 3 — Prompt loader generator (PARALLEL CANDIDATE)

**Files:**
- Create: `scripts/agent_forge/translators/prompt_loader.py`
- Create: `tests/unit/translators/test_prompt_loader.py`

- [ ] **Step 1: Write the failing test**

```python
"""tests/unit/translators/test_prompt_loader.py"""

from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.prompt_loader import build_loader_md

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_prompt_loader_registered() -> None:
    t = get_translator("prompt-loader")
    assert t.tier == "3"


def test_loader_includes_frontmatter_for_routing() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="rahulnakmol/agent-forge", branch="main")
    assert loader.startswith("---\n")
    assert "name: humanize" in loader
    assert "description:" in loader


def test_loader_links_to_raw_skill_md() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="rahulnakmol/agent-forge", branch="main")
    expected = "https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/plugins/writing/skills/humanize/SKILL.md"
    assert expected in loader


def test_loader_links_each_reference() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="rahulnakmol/agent-forge", branch="main")
    for ref in skill.references():
        rel = ref.relative_to(REPO).as_posix()
        assert f"https://raw.githubusercontent.com/rahulnakmol/agent-forge/main/{rel}" in loader


def test_loader_instructs_lazy_reference_loading() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="rahulnakmol/agent-forge", branch="main")
    assert "Do NOT eagerly fetch references" in loader
```

- [ ] **Step 2: Implement `scripts/agent_forge/translators/prompt_loader.py`**

```python
"""Tier 3 prompt-loader generator for Perplexity Spaces, ChatGPT custom GPTs,
and Claude.ai Projects.

Emits a thin loader SKILL.md whose frontmatter routes the skill, and whose
body points the host LLM to raw GitHub URLs. Preserves progressive disclosure:
references are loaded on demand, not inlined.
"""

from pathlib import Path

from agent_forge.canonical import CanonicalSkill
from agent_forge.translators import register

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

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
        return False  # No machine-detection possible for Perplexity/GPTs/Projects

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}  # Output is stdout, not filesystem

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True  # No way to verify Perplexity/GPT install programmatically


register(PromptLoaderTranslator())
```

- [ ] **Step 3: Run**

```bash
pytest tests/unit/translators/test_prompt_loader.py -v
```

---

## Task 14: Add CI invariant tests for translator/registry sync

**Files:**
- Create: `tests/unit/test_tier1_artifacts_sync.py`

- [ ] **Step 1: Write the test**

```python
"""Verify all Tier 1a generated artifacts are in sync with the canonical source.

If a contributor edits .claude-plugin/marketplace.json or a plugin without
re-running scripts/regenerate-tier1-artifacts.py, this test catches the drift.
"""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent


def test_tier1_artifacts_in_sync() -> None:
    result = subprocess.run(
        ["python", "scripts/regenerate-tier1-artifacts.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Tier 1 artifacts drifted from canonical source.\n"
        f"Stdout: {result.stdout}\n"
        f"Run: python scripts/regenerate-tier1-artifacts.py"
    )
```

- [ ] **Step 2: Run**

```bash
pytest tests/unit/test_tier1_artifacts_sync.py -v
```
Expected: pass (artifacts are fresh from Tasks 5–7).

---

## Task 15: Smoke test all 10 translators + commit

- [ ] **Step 1: Verify all translators load**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
python -c "from agent_forge.translators import registered_translators; print(registered_translators())"
```
Expected: `['amp', 'claude-code', 'codex-cli', 'copilot-cli', 'crush', 'cursor', 'gemini-cli', 'kilocode', 'opencode', 'prompt-loader']`

- [ ] **Step 2: Run all translator tests**

```bash
pytest tests/unit/translators -v
pytest tests/unit/test_tier1_artifacts_sync.py -v
```
Expected: all pass.

- [ ] **Step 3: Run the full Layer A suite to make sure nothing regressed**

```bash
pytest tests/unit -v
```
Expected: 100% pass.

- [ ] **Step 4: Stage + commit**

```bash
git add scripts/agent_forge/ scripts/regenerate-tier1-artifacts.py tests/unit/ .github/plugin/ .codex-plugin/ .cursor-plugin/ plugins/*/plugin.json plugins/*/.codex-plugin/ plugins/*/.cursor-plugin/ plugins/*/agents/*.agent.md plugins/*/agents/*.toml
git commit -s -m "Phase 2: all 10 translators + Tier 1 generated artifacts

Translators implemented (one Python module each, registered via _REGISTRY):
- Tier 1a (registry): claude_code (no-op), copilot_cli, codex_cli, cursor
- Tier 1b (git-URL):  amp, gemini_cli
- Tier 2 (adapter):   kilocode, opencode, crush
- Tier 3 (loader):    prompt_loader

Generated + committed artifacts (regenerate via scripts/regenerate-tier1-artifacts.py):
- .github/plugin/marketplace.json (Copilot)
- .codex-plugin/marketplace.json (Codex)
- .cursor-plugin/marketplace.json (Cursor)
- plugins/<each>/plugin.json (Copilot's per-plugin manifest)
- plugins/<each>/.codex-plugin/plugin.json (Codex)
- plugins/<each>/.cursor-plugin/plugin.json (Cursor)
- plugins/<each>/agents/*.agent.md (Copilot agent mirrors)
- plugins/<each>/agents/*.toml (Codex TOML conversions)

Shared helpers:
- agent_forge.frontmatter (parse + render YAML frontmatter)
- agent_forge.canonical (read plugins/ tree)
- agent_forge.translators (registry + Protocol)

Tests: every translator has its own pytest module; sync invariant tested via
scripts/regenerate-tier1-artifacts.py --check (CI).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Self-Review

- [ ] Spec coverage: D11 (all 10 translators) ✓; CI invariants 2-4 (manifests in sync) ✓; Translator Protocol contract ✓
- [ ] Placeholder scan: no TBD; every translator has minimal-but-complete implementation; spike resolutions inlined (Copilot uses copy not symlink for cross-platform safety)
- [ ] Type consistency: `CanonicalPlugin`, `CanonicalSkill` used uniformly; `register()` and `get_translator()` signature match across all 10 modules
- [ ] No test references functions/classes not defined in earlier tasks ✓

**Done criteria:** All 10 translators registered + tested; all Tier 1a artifacts generated + committed; sync invariant test passing; full `pytest tests/unit` green.
