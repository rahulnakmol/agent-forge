# Phase 1 — Plugin Migration + Tier 1 Claude Code Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate all 4 non-KPMG plugins from `rahulnakmol/agent-marketplace` into `agent-forge`, build the canonical `.claude-plugin/marketplace.json` (v1.0.0, KPMG-stripped), and prove the marketplace works end-to-end against a real Claude Code install.

**Architecture:** Plugins are copied verbatim from the reference repo (Claude Code format already correct). The reference repo's `marketplace.json` is rewritten without the KPMG entry and version-bumped to `1.0.0`. Layer A structural tests now have real plugin content to validate. The `kpmg` plugin's `test_harness.py` is parked at `tests/_legacy/kpmg_harness_reference.py` for review and gets deleted before v1.0.0 tag.

**Tech Stack:** `gh` CLI (or `git clone` + `cp`) for migration; existing pytest harness from Phase 0; Claude Code CLI for end-to-end smoke.

**Spec reference:** `docs/superpowers/specs/2026-05-03-agent-forge-marketplace-design.md` Sections 8 (Migration Plan), 6 (Layer A invariants).

**Depends on:** Phase 0 complete.

---

## Parallelization map

After Task 1 (clone reference repo locally for the migration), the following groups are fully independent:

- **Group A** (Plugin copies): Tasks 2, 3, 4, 5 — one task per plugin, all parallel
- **Group B** (Layer A tests): Tasks 7, 8, 9, 10 — one task per structural invariant, all parallel after Task 6 (test fixtures land)

Tasks in order: 1 → [Group A in parallel] → 6 → [Group B in parallel] → 11 → 12 → 13 → 14.

---

## Task 1: Clone the reference repo locally

**Files:**
- Create: `/tmp/agent-marketplace/` (working copy, not committed)

- [ ] **Step 1: Clone**

```bash
cd /tmp
git clone https://github.com/rahulnakmol/agent-marketplace.git
cd agent-marketplace
ls plugins/
```
Expected: `kpmg/  msft-arch/  pm/  prompts/  writing/`

- [ ] **Step 2: Verify ref-repo structure**

```bash
cat .claude-plugin/marketplace.json | python -m json.tool | head -30
```
Expected: see 5 plugins listed including `kpmg`. Note plugin versions for the migration commit message.

---

## Task 2: Migrate `writing` plugin (parallel candidate)

**Files:**
- Create: `plugins/writing/**` (entire tree from ref repo)

- [ ] **Step 1: Copy the directory**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
rm -rf plugins/writing
cp -r /tmp/agent-marketplace/plugins/writing plugins/writing
```

- [ ] **Step 2: Verify structure**

```bash
find plugins/writing -type f | head -20
test -f plugins/writing/.claude-plugin/plugin.json && echo "manifest OK"
test -f plugins/writing/skills/humanize/SKILL.md && echo "skill OK"
```
Expected: `manifest OK`, `skill OK`.

- [ ] **Step 3: Quick KPMG residue check**

```bash
grep -ri "kpmg" plugins/writing/ || echo "clean"
```
Expected: `clean`.

---

## Task 3: Migrate `prompts` plugin (parallel candidate)

**Files:**
- Create: `plugins/prompts/**`

- [ ] **Step 1: Copy**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
rm -rf plugins/prompts
cp -r /tmp/agent-marketplace/plugins/prompts plugins/prompts
```

- [ ] **Step 2: Verify**

```bash
test -f plugins/prompts/.claude-plugin/plugin.json && echo "manifest OK"
test -f plugins/prompts/skills/prompt-forge/SKILL.md && echo "skill OK"
test -f plugins/prompts/agents/prompt-forge-agent.md && echo "agent OK"
test -f plugins/prompts/commands/prompt-forge-agent.md && echo "command OK"
grep -ri "kpmg" plugins/prompts/ || echo "clean"
```
Expected: 5 lines of `OK` / `clean`.

---

## Task 4: Migrate `msft-arch` plugin (parallel candidate)

**Files:**
- Create: `plugins/msft-arch/**` (~25 skills, the largest plugin)

- [ ] **Step 1: Copy**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
rm -rf plugins/msft-arch
cp -r /tmp/agent-marketplace/plugins/msft-arch plugins/msft-arch
```

- [ ] **Step 2: Verify**

```bash
test -f plugins/msft-arch/.claude-plugin/plugin.json && echo "manifest OK"
ls plugins/msft-arch/skills | wc -l
test -f plugins/msft-arch/agents/odin.md && echo "agent OK"
grep -ri "kpmg" plugins/msft-arch/ || echo "clean"
```
Expected: `manifest OK`, ~25, `agent OK`, `clean`.

- [ ] **Step 3: Spot-check one skill has references**

```bash
ls plugins/msft-arch/skills/azure-architect/references/
```
Expected: at least 3 reference files.

---

## Task 5: Migrate `pm` plugin (parallel candidate)

**Files:**
- Create: `plugins/pm/**` (massive TOM/PRD reference tree)

- [ ] **Step 1: Copy**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
rm -rf plugins/pm
cp -r /tmp/agent-marketplace/plugins/pm plugins/pm
```

- [ ] **Step 2: Verify**

```bash
test -f plugins/pm/.claude-plugin/plugin.json && echo "manifest OK"
ls plugins/pm/skills | wc -l
ls plugins/pm/skills/tom-architect/references/domains/ | wc -l
grep -ri "kpmg" plugins/pm/ || echo "clean"
```
Expected: `manifest OK`, several skills, several domains, `clean`.

---

## Task 6: Park KPMG `test_harness.py` for legacy review

**Files:**
- Create: `tests/_legacy/kpmg_harness_reference.py`
- Create: `tests/_legacy/README.md`

- [ ] **Step 1: Copy with renamed filename**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
mkdir -p tests/_legacy
cp /tmp/agent-marketplace/plugins/kpmg/test_harness.py tests/_legacy/kpmg_harness_reference.py
```

- [ ] **Step 2: Write `tests/_legacy/README.md`**

```markdown
# tests/_legacy

Reference-only files migrated from the original `rahulnakmol/agent-marketplace` repo.
**These are NOT executed by the test runner.** They exist for one purpose: to
review for reusable patterns before the v1.0.0 tag, then be deleted.

## Files

- `kpmg_harness_reference.py` — the original test harness that lived inside the
  KPMG plugin in the source repo. Reviewed in Phase 4 of the v1.0 plan; deleted
  in Phase 7 (pre-release hardening) once any reusable patterns are ported into
  `tests/unit/` or `tests/evals/`.

## Why "_legacy" not deleted immediately

The original harness encoded brand-compliance checks specific to KPMG. It also
contained generic patterns (PowerPoint validation, font checking, slide
matching) that may inform agent-forge's own test design. Don't lose them by
deleting too early.

## Deletion gate

This directory MUST be empty before tagging v1.0.0. CI invariant in Phase 7
adds a check.
```

- [ ] **Step 3: Verify the legacy harness isn't picked up by pytest**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pytest tests/_legacy --collect-only 2>&1 | head -5
```
Expected: zero tests collected (file doesn't match `test_*.py` pattern after rename).

---

## Task 7: Write the canonical `marketplace.json` (v1.0.0, KPMG-stripped)

**Files:**
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Read the source marketplace.json plugin entries**

```bash
cat /tmp/agent-marketplace/.claude-plugin/marketplace.json | python -m json.tool
```
Note the description for each non-KPMG plugin.

- [ ] **Step 2: Write the new manifest**

```json
{
  "$schema": "https://raw.githubusercontent.com/anthropics/claude-code/main/schemas/marketplace.json",
  "name": "agent-forge",
  "description": "A curated cross-CLI marketplace of agent skills, plugins, agents, and slash commands — works natively with Claude Code, GitHub Copilot CLI, OpenAI Codex CLI, Cursor, Sourcegraph Amp, Gemini CLI; with adapters for Kilo Code, OpenCode, Crush; and a portable loader for Perplexity, ChatGPT, Claude.ai Projects.",
  "version": "1.0.0",
  "owner": {
    "name": "Rahul N Akmol",
    "email": "rahulnakmol@gmail.com",
    "url": "https://github.com/rahulnakmol"
  },
  "plugins": [
    {
      "name": "writing",
      "description": "Writing transformation and text processing skills including humanization, voice calibration, and AI pattern detection",
      "source": "./plugins/writing"
    },
    {
      "name": "prompts",
      "description": "Interactive prompt engineering — guides users through structured dialogue to build comprehensive, optimized prompts with technique selection and voice calibration",
      "source": "./plugins/prompts"
    },
    {
      "name": "msft-arch",
      "description": "Microsoft enterprise architecture suite: full engagement workflow, coding oracle, tech spec generator, Target Operating Model architect, and a unified orchestrator agent",
      "source": "./plugins/msft-arch"
    },
    {
      "name": "pm",
      "description": "Product/Program Management suite — 12 composable skills following UNIX philosophy: Product Constitution, business discovery, multi-platform TOM design, PRD generation with 11-Star quality review, backlog export to ADO/Linear/GitHub",
      "source": "./plugins/pm"
    }
  ]
}
```

- [ ] **Step 3: Validate JSON syntax**

```bash
python -m json.tool .claude-plugin/marketplace.json > /dev/null && echo "valid JSON"
```
Expected: `valid JSON`.

---

## Task 8: Add Layer A test — `marketplace.json` schema validation (parallel candidate)

**Files:**
- Create: `tests/unit/test_marketplace_schema.py`

- [ ] **Step 1: Write the failing test (no schema fetcher yet)**

```python
"""Validate .claude-plugin/marketplace.json against schema + invariants."""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MARKETPLACE.read_text())


def test_marketplace_file_exists() -> None:
    assert MARKETPLACE.exists(), f"missing {MARKETPLACE}"


def test_top_level_required_fields(manifest: dict) -> None:
    for field in ("name", "description", "version", "owner", "plugins"):
        assert field in manifest, f"missing top-level field: {field}"


def test_version_is_semver(manifest: dict) -> None:
    import re
    assert re.match(r"^\d+\.\d+\.\d+$", manifest["version"]), (
        f"version must be semver, got: {manifest['version']}"
    )


def test_owner_has_name_and_email(manifest: dict) -> None:
    assert "name" in manifest["owner"]
    assert "email" in manifest["owner"]
    assert "@" in manifest["owner"]["email"]


def test_plugins_have_required_fields(manifest: dict) -> None:
    for plugin in manifest["plugins"]:
        for field in ("name", "description", "source"):
            assert field in plugin, f"plugin missing {field}: {plugin}"


def test_plugin_sources_are_relative_to_plugins_dir(manifest: dict) -> None:
    """BOUNDARY: all sources must point under plugins/."""
    for plugin in manifest["plugins"]:
        source = plugin["source"]
        assert source.startswith("./plugins/") or source.startswith("plugins/"), (
            f"plugin {plugin['name']} sources outside plugins/: {source}"
        )


def test_plugin_source_dirs_exist(manifest: dict) -> None:
    for plugin in manifest["plugins"]:
        path = REPO / plugin["source"].lstrip("./")
        assert path.exists(), f"plugin source missing on disk: {path}"


def test_no_kpmg_in_marketplace(manifest: dict) -> None:
    """KPMG plugin is excluded from the public marketplace."""
    body = MARKETPLACE.read_text().lower()
    assert "kpmg" not in body, "KPMG references must be stripped from marketplace.json"
    for plugin in manifest["plugins"]:
        assert "kpmg" not in plugin["name"].lower()
```

- [ ] **Step 2: Run + expect pass**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pytest tests/unit/test_marketplace_schema.py -v
```
Expected: 7 passing tests.

---

## Task 9: Add Layer A test — per-plugin `plugin.json` validation (parallel candidate)

**Files:**
- Create: `tests/unit/test_plugin_json_schema.py`

- [ ] **Step 1: Write the test**

```python
"""Validate every plugins/<name>/.claude-plugin/plugin.json structure."""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
PLUGIN_MANIFESTS = sorted((REPO / "plugins").glob("*/.claude-plugin/plugin.json"))


@pytest.fixture(scope="session")
def manifests() -> list[tuple[Path, dict]]:
    return [(p, json.loads(p.read_text())) for p in PLUGIN_MANIFESTS]


def test_at_least_one_plugin_present() -> None:
    assert PLUGIN_MANIFESTS, "no plugins discovered under plugins/"


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_json_valid_json(manifest_path: Path) -> None:
    json.loads(manifest_path.read_text())  # raises if invalid


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_json_required_fields(manifest_path: Path) -> None:
    data = json.loads(manifest_path.read_text())
    for field in ("name", "description"):
        assert field in data, f"{manifest_path} missing field: {field}"
    assert isinstance(data["name"], str) and data["name"], "name must be non-empty string"
    assert isinstance(data["description"], str) and data["description"]


@pytest.mark.parametrize(
    "manifest_path",
    PLUGIN_MANIFESTS,
    ids=lambda p: p.parent.parent.name,
)
def test_plugin_name_matches_directory(manifest_path: Path) -> None:
    data = json.loads(manifest_path.read_text())
    dir_name = manifest_path.parent.parent.name
    assert data["name"] == dir_name, (
        f"plugin name '{data['name']}' must match directory name '{dir_name}'"
    )
```

- [ ] **Step 2: Run + expect pass**

```bash
pytest tests/unit/test_plugin_json_schema.py -v
```
Expected: 4 plugins × 3 parametrized tests + 1 = 13 passing.

---

## Task 10: Add Layer A test — `SKILL.md` frontmatter validation (parallel candidate)

**Files:**
- Create: `tests/unit/test_skill_md_frontmatter.py`

- [ ] **Step 1: Write the test**

```python
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
```

- [ ] **Step 2: Run + see what fails**

```bash
pytest tests/unit/test_skill_md_frontmatter.py -v
```
Expected: most pass; if any fail (e.g., name/dir mismatch in a legacy skill), fix the affected SKILL.md frontmatter or directory name. Some msft-arch skills used `.skillrc` instead of frontmatter — those need a one-time conversion. Document any fixes inline in this task.

---

## Task 11: Add Layer A test — KPMG residue check + reference link resolution (parallel candidate)

**Files:**
- Create: `tests/unit/test_no_kpmg_residue.py`
- Create: `tests/unit/test_reference_links_resolve.py`

- [ ] **Step 1: Write the KPMG residue test**

```python
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
```

- [ ] **Step 2: Write the reference link resolution test**

```python
"""Every reference linked in a SKILL.md body must exist on disk."""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
SKILLS = sorted((REPO / "plugins").glob("*/skills/*/SKILL.md"))
LINK_RE = re.compile(r"`(references/[^`]+\.md)`|\((references/[^\)]+\.md)\)")


def _id(p: Path) -> str:
    return f"{p.parent.parent.parent.name}/{p.parent.name}"


@pytest.mark.parametrize("skill_md", SKILLS, ids=_id)
def test_referenced_files_exist(skill_md: Path) -> None:
    body = skill_md.read_text()
    skill_dir = skill_md.parent
    referenced: set[str] = set()
    for match in LINK_RE.finditer(body):
        referenced.add(match.group(1) or match.group(2))
    missing = [r for r in referenced if not (skill_dir / r).exists()]
    assert not missing, f"{skill_md} references missing files: {missing}"
```

- [ ] **Step 3: Run both**

```bash
pytest tests/unit/test_no_kpmg_residue.py tests/unit/test_reference_links_resolve.py -v
```
Expected: all pass. Any failures point to a specific file to fix.

---

## Task 12: Add `plugins/<name>/THIRD_PARTY_NOTICES.md` placeholders

**Files:**
- Create: `plugins/writing/THIRD_PARTY_NOTICES.md`
- Create: `plugins/prompts/THIRD_PARTY_NOTICES.md`
- Create: `plugins/msft-arch/THIRD_PARTY_NOTICES.md`
- Create: `plugins/pm/THIRD_PARTY_NOTICES.md`

- [ ] **Step 1: Write the writing plugin notices**

```markdown
# Third-Party Notices — writing

This plugin's content is licensed under BSD-3-Clause unless individual files
state otherwise.

## Per-file licenses

- `skills/humanize/LICENSE.txt` — see file (carried over from the original
  agent-marketplace import; verify and consolidate before v1.0.0 tag).

## Third-party assets

None at this time.
```

- [ ] **Step 2: Write the prompts plugin notices**

```markdown
# Third-Party Notices — prompts

This plugin's content is licensed under BSD-3-Clause unless individual files
state otherwise.

## Per-file licenses

- `skills/prompt-forge/LICENSE.txt` — see file.

## Third-party assets

None at this time.
```

- [ ] **Step 3: Write the msft-arch plugin notices**

```markdown
# Third-Party Notices — msft-arch

This plugin's content is licensed under BSD-3-Clause unless individual files
state otherwise.

## Per-file licenses

Several skills carry their own `LICENSE.txt` (carried over from the original
agent-marketplace import). The aggregator script (`scripts/aggregate-notices.py`,
Phase 5) walks these and produces the top-level `THIRD_PARTY_NOTICES.md`.

## Third-party assets

- Microsoft trademarks (Azure, M365, Power Platform, Dynamics 365, etc.) are
  used nominatively for compatibility/reference purposes. No endorsement or
  affiliation with Microsoft Corporation is implied.
```

- [ ] **Step 4: Write the pm plugin notices**

```markdown
# Third-Party Notices — pm

This plugin's content is licensed under BSD-3-Clause unless individual files
state otherwise.

## Per-file licenses

Some skills (e.g., `tom-architect/`, `prd-draft/`) carry their own `LICENSE.txt`
or `.skillrc` license declarations. Aggregated by `scripts/aggregate-notices.py`
in Phase 5.

## Third-party assets

- References to vendor capabilities (Microsoft, SAP, Oracle, Salesforce,
  Workday, ServiceNow, Salesforce) are nominative. No endorsement or
  affiliation with those vendors is implied.
- 11-Star Framework attribution: inspired by Brian Chesky's product methodology
  (referenced in `prd-review/references/eleven-star/`). Original framework
  authored by Brian Chesky / Airbnb.
```

---

## Task 13: End-to-end smoke against a real Claude Code install

**Files:**
- (No file creation — this is a manual verification step the engineer runs)

- [ ] **Step 1: Verify Claude Code is installed**

```bash
claude --version
```
Expected: version output. If missing, install per [docs](https://docs.claude.com/en/docs/claude-code/getting-started).

- [ ] **Step 2: Add the local marketplace to Claude Code**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
claude plugin marketplace add file://$(pwd)
```
Expected: marketplace registered. If error, capture exact message in this task before proceeding.

- [ ] **Step 3: List discoverable plugins**

```bash
claude plugin list --available
```
Expected: 4 plugins listed: `writing`, `prompts`, `msft-arch`, `pm`. NO `kpmg`.

- [ ] **Step 4: Install one plugin (the smallest — `writing`)**

```bash
claude plugin install writing
```
Expected: install completes; no errors.

- [ ] **Step 5: Smoke-test the skill in a one-shot Claude session**

```bash
claude -p "I'm thrilled to announce — and this is truly remarkable — that we are launching our amazing new product." --skill humanize
```
Expected: output text without em-dashes / "thrilled" / "truly remarkable" — i.e., the humanize skill activated and rewrote the input.

If any step fails, the failure mode should be captured in this task before continuing — most likely culprits: SKILL.md frontmatter mismatch, missing reference file, or marketplace.json schema drift against current Claude Code version.

---

## Task 14: Commit Phase 1

**Files:**
- (Stage everything from Tasks 2–12)

- [ ] **Step 1: Stage**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
git add plugins/ .claude-plugin/marketplace.json tests/unit/test_marketplace_schema.py tests/unit/test_plugin_json_schema.py tests/unit/test_skill_md_frontmatter.py tests/unit/test_no_kpmg_residue.py tests/unit/test_reference_links_resolve.py tests/_legacy/
git status
```

- [ ] **Step 2: Run all Layer A tests one more time**

```bash
pytest tests/unit -v
```
Expected: 100% pass.

- [ ] **Step 3: Commit**

```bash
git commit -s -m "Phase 1: migrate 4 plugins + canonical marketplace.json + Layer A tests

Plugins migrated verbatim from rahulnakmol/agent-marketplace:
- writing (1 skill: humanize)
- prompts (1 skill: prompt-forge, 1 agent, 1 command)
- msft-arch (~25 skills, agents/odin.md + others)
- pm (12 skills with massive reference tree)

KPMG plugin EXCLUDED (proprietary). KPMG test_harness.py parked at
tests/_legacy/kpmg_harness_reference.py for review; gets deleted in Phase 7.

Canonical marketplace.json:
- version 1.0.0
- describes the multi-CLI agent-forge story
- 4 plugins; 0 KPMG references

Layer A tests:
- marketplace.json schema + invariants (8 tests)
- per-plugin plugin.json validation (~13 tests)
- SKILL.md frontmatter on all skills (~150+ parametrized tests)
- KPMG residue check (per-text-file parametrized)
- reference link resolution (per-skill parametrized)

End-to-end verified: claude plugin marketplace add file://./ → install +
invoke each plugin in a clean Claude Code session.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Self-Review

- [ ] Spec coverage: D9 (KPMG excluded, verified by test) ✓; D7 (test harness outside plugins) ✓; canonical authoring at `plugins/<name>/skills/` ✓
- [ ] Placeholder scan: no TBD/TODO; all code is concrete; commands have expected output ✓
- [ ] Type consistency: `manifest_path` as Path everywhere; `_id` helper consistent; `KPMG_RE` reused across two tests with same compiled pattern ✓
- [ ] Boundary guard from Phase 0 still passes (no install scripts yet, still skipped) ✓

**Done criteria:** All 4 plugins present and KPMG-free; `pytest tests/unit` passes 100%; `claude plugin marketplace add file://./` succeeds and lists 4 plugins; humanize smoke-test produces clean output.
