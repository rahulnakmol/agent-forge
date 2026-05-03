# Phase 6 — Pre-release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Cut a `release/v1.0.0` branch, run the full Layer C integration test matrix in CI, dogfood the install on a fresh machine across every CLI, complete a security review, and produce final release notes — leaving the repo in a tag-ready state.

**Architecture:** No new code. This phase is verification + cleanup. The `release/v1.0.0` branch triggers `ci-integration.yml` (built in Phase 4) which runs Layer C across all 9 native + adapter CLIs in parallel Docker matrices. Dogfooding is a manual checklist; security review pulls findings from `pip-audit`, `gh secret scanning`, and a manual third-party-content audit.

**Tech Stack:** GitHub Actions (existing); `pip-audit`; manual review.

**Spec reference:** Section 8 Phase 6.

**Depends on:** Phases 0–5 complete.

---

## Parallelization map

After Task 1 (cut release branch + push), the following groups are independent:

- **Group A** (CI-driven): Tasks 2, 3 — Layer C + nightly evals run in parallel via the workflow matrix
- **Group B** (manual checks, can be parallel-dispatched to subagents): Task 4 (dogfooding per CLI — 9 sub-tasks parallel), Task 5 (security review — 4 sub-tasks parallel)
- **Group C** (release prep): Tasks 6 (release notes) is sequential after Groups A + B yield findings

---

## Task 1: Cut the `release/v1.0.0` branch

- [x] **Step 1: Confirm `main` is clean and Phase 5 committed**

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
git status
git log --oneline -5
```
Expected: clean tree; Phase 5 commit visible.

- [x] **Step 2: Bump version in `scripts/agent_forge/pyproject.toml` and `__init__.py` to `1.0.0`**

```bash
sed -i '' 's/version = "0.1.0-dev"/version = "1.0.0"/' scripts/agent_forge/pyproject.toml
sed -i '' 's/__version__ = "0.1.0-dev"/__version__ = "1.0.0"/' scripts/agent_forge/__init__.py
```

- [x] **Step 3: Cut + push the branch**

```bash
git checkout -b release/v1.0.0
git add scripts/agent_forge/pyproject.toml scripts/agent_forge/__init__.py
git commit -s -m "Bump version to 1.0.0 for release"
git push -u origin release/v1.0.0
```
Expected: push succeeds; `ci-integration.yml` triggered (visible at github.com/rahulnakmol/agent-forge/actions).

- [x] **Step 4: Watch the integration matrix run**

```bash
gh run watch
```
Expected: all 9 CLI integration tests + update-propagation + remove-clean tests pass.

---

## Task 2: Layer C integration matrix — verify all 9 CLIs pass

- [x] **Step 1: Wait for matrix completion** (~10-15 min)

```bash
gh run list --workflow=ci-integration.yml --limit 1
gh run view --log
```

- [x] **Step 2: Triage any failures**

For each failing matrix cell:
1. Identify which CLI failed and at which step (install / invoke / update / remove)
2. Reproduce locally:
   ```bash
   docker build -t agent-forge-test:<cli> -f tests/integration/dockerfiles/<cli>.Dockerfile .
   pytest tests/integration/test_install_lifecycle_<cli>.py -v
   ```
3. Patch the affected translator (`scripts/agent_forge/translators/<cli>.py`) or install guide (`docs/install/<cli>.md`)
4. Commit + re-run

- [x] **Step 3: Confirm green**

```bash
gh run list --workflow=ci-integration.yml --limit 1 --json conclusion,status
```
Expected: `{"conclusion": "success", "status": "completed"}`.

---

## Task 3: Run nightly Layer B sweep manually as part of release verification

- [x] **Step 1: Trigger via workflow_dispatch**

```bash
gh workflow run ci-evals-nightly.yml
gh run watch
```
Expected: full sweep across ~150 skills passes within tolerance.

- [x] **Step 2: Triage regressions**

For any skill whose score dropped below baseline - 0.3:
1. Re-run that skill's eval locally to rule out judge variance:
   ```bash
   pytest tests/evals/<plugin>/<skill> -v --tb=short -x  # repeat 3 times
   ```
2. If consistently regressed: investigate the SKILL.md or recent reference changes; fix
3. If transient (judge variance): update baseline with new average:
   ```bash
   pytest tests/evals/<plugin>/<skill> --update-baselines
   ```

- [x] **Step 3: Commit any baseline updates**

```bash
git add tests/evals/_baseline_scores.json
git commit -s -m "Refresh eval baselines for v1.0.0 release verification"
git push
```

---

## Task 4: Dogfood install on a fresh environment (9 PARALLEL SUBTASKS)

Each subtask spawns a clean Docker container or fresh VM with one CLI installed and runs the documented install flow end-to-end. The dogfooder follows `docs/install/<cli>.md` *literally* — paste the commands as written, no shortcuts.

### 4a — Claude Code dogfood

- [x] **Step 1:** spin a fresh container with Claude installed; follow `docs/install/claude-code.md` step-by-step
- [x] **Step 2:** install all 4 plugins (`writing`, `prompts`, `msft-arch`, `pm`)
- [x] **Step 3:** invoke one skill from each plugin; verify output is what the SKILL.md claims
- [x] **Step 4:** run `agent-forge update --check`; verify reports "up-to-date"
- [x] **Step 5:** record any docs gaps as issues with label `area/docs`

### 4b — Copilot CLI dogfood

(Same template as 4a, substituting Copilot's commands.)

### 4c — Codex CLI dogfood

### 4d — Cursor dogfood

### 4e — Amp dogfood

### 4f — Gemini CLI dogfood

### 4g — Kilo Code dogfood

### 4h — OpenCode dogfood

### 4i — Crush dogfood

For each, **the gating question is**: "Could a brand-new user follow this guide and succeed without external help?" If no → file a docs issue, fix, re-test.

---

## Task 5: Security review (4 PARALLEL SUBTASKS)

### 5a — Dependency vulnerability scan

- [x] **Step 1:** Run `pip-audit` on the agent-forge runtime dependencies

```bash
cd /Users/rahulnakmol/Developer/Github/agent-forge
pip install pip-audit
pip-audit -r scripts/agent_forge/pyproject.toml
```
Expected: zero CVEs. If any: bump dependency version + re-test.

- [x] **Step 2:** Same for tests dependencies

```bash
pip-audit -r tests/pyproject.toml
```

### 5b — Secret scanning

- [x] **Step 1:** Confirm GitHub secret scanning is enabled

```bash
gh api repos/rahulnakmol/agent-forge --jq '.security_and_analysis'
```
Expected: `secret_scanning.status == "enabled"`.

- [x] **Step 2:** Spot-check committed files for accidental secrets

```bash
gh api repos/rahulnakmol/agent-forge/secret-scanning/alerts
```
Expected: zero alerts. If any: rotate the secret, force-push amended commits per GitHub's removal guide.

### 5c — Third-party content audit

- [x] **Step 1:** Verify every per-plugin `THIRD_PARTY_NOTICES.md` is accurate

For each plugin, walk the `assets/`, `references/`, `scripts/` trees and verify any third-party content is attributed.

```bash
for plugin in plugins/*/; do
  echo "=== $plugin ==="
  find "$plugin" -name "*.ttf" -o -name "*.otf" -o -name "*.pptx" -o -name "*.docx" | head
done
```

If any uncredited assets surface: add to the plugin's `THIRD_PARTY_NOTICES.md`, re-run `python scripts/aggregate-notices.py`, commit.

### 5d — Translator output integrity

- [x] **Step 1:** Verify auto-generated artifacts haven't drifted from canonical

```bash
python scripts/regenerate-tier1-artifacts.py --check
python scripts/aggregate-notices.py --check
python scripts/build-install-index.py --check
```
Expected: all three exit 0.

---

## Task 6: Delete `tests/_legacy/` (KPMG harness reference)

- [x] **Step 1:** Final review of `tests/_legacy/kpmg_harness_reference.py` for any patterns worth porting

If anything is reusable: extract to `tests/unit/_helpers.py` or similar with attribution. Otherwise:

- [x] **Step 2:** Delete the directory

```bash
git rm -rf tests/_legacy
git commit -s -m "Remove legacy KPMG test harness reference (patterns ported / not needed)"
```

- [x] **Step 3:** Verify no test references the legacy path

```bash
grep -r "_legacy" tests/ scripts/ || echo "clean"
```
Expected: `clean`.

---

## Task 7: Draft release notes

**Files:**
- Create: `docs/releases/v1.0.0.md`

- [x] **Step 1: Write the release notes**

```markdown
# agent-forge v1.0.0

**Released: <DATE>**

The first stable release of agent-forge — a curated, BSD-3-Clause marketplace
of agent skills, plugins, and slash commands that works across 12 install
targets without per-tool reauthoring.

## Highlights

- **12 install targets** at v1.0: 6 CLIs with native marketplace integration
  (Claude Code, GitHub Copilot CLI, OpenAI Codex CLI, Cursor, Sourcegraph Amp,
  Google Gemini CLI), 3 with lightweight adapters (Kilo Code, OpenCode, Crush),
  and 3 prompt-tool loaders (Perplexity, ChatGPT GPTs, Claude.ai Projects).
- **4 plugins** with ~150 skills total: writing, prompts, msft-arch, pm.
- **One canonical source** — author plugins in Claude Code format under
  `plugins/<name>/`; translators auto-generate the per-CLI manifests.
- **`agent-forge` Python CLI** (`pipx install agent-forge`) — unified install,
  update, pin, and remove across every supported tool.
- **Agent-installable** — paste a single URL into any LLM agent and it follows
  the install guide directly.

## Breaking changes from pre-1.0

None — this is the first stable release. Schemas frozen at v1.0:
- `.claude-plugin/marketplace.json`
- `.github/plugin/marketplace.json`
- `.codex-plugin/marketplace.json`
- `.cursor-plugin/marketplace.json`
- Per-plugin `plugin.json` files (one per native CLI)
- `~/.agent-forge/manifest.json` (`schema_version: 1`)
- `agent-forge` CLI command surface
- The install-URL pattern

After v1.0, breaking changes to any of the above require v2.0.0.

## Quality bar

- 100% of skills covered by Layer B rubric-judged evals with committed regression baselines
- Layer C integration tests passing for all 9 native + adapter CLIs in Docker
- Security: zero open `pip-audit` findings, zero open secret-scanning alerts

## Roadmap (v1.1)

- Aider plugin marketplace adapter (currently no agentskills.io support; awaiting upstream)
- Sourcegraph Amp deep integration with workflows
- Cross-tool `.agents/` namespace publishing experiments

## Acknowledgements

- Anthropic for stewarding the agentskills.io specification
- The agent-skills authoring conventions adopted by Codex, Cursor, Amp,
  Gemini CLI, OpenCode, Kilo, Crush, Copilot CLI — making cross-tool
  portability tractable
- The author's prior work in `rahulnakmol/agent-marketplace` from which the
  4 plugins were imported

## Install

```bash
# Claude Code
claude plugin marketplace add github:rahulnakmol/agent-forge
# GitHub Copilot CLI
copilot plugin marketplace add rahulnakmol/agent-forge
# Any other tool
pipx install agent-forge
agent-forge install <plugin> --tier <your-cli>
```

See [docs/install/_index.md](https://github.com/rahulnakmol/agent-forge/blob/main/docs/install/_index.md) for all 12 targets.
```

- [x] **Step 2: Commit**

```bash
git add docs/releases/v1.0.0.md
git commit -s -m "Draft v1.0.0 release notes"
```

---

## Task 8: Final pre-tag review

- [x] **Step 1: Full local CI**

```bash
pytest tests/unit -v
pytest tests/evals -v -m "not slow"  # skip slow eval cases for the smoke
```

- [x] **Step 2: Verify all sync invariants**

```bash
python scripts/regenerate-tier1-artifacts.py --check
python scripts/aggregate-notices.py --check
python scripts/build-install-index.py --check
```

- [x] **Step 3: Verify the release branch matches main + version bump**

```bash
git diff main..release/v1.0.0 --stat
```
Expected: only the version bump (and any patches from Tasks 2 + 5).

- [x] **Step 4: Open the release PR (release branch → main, tag-ready)**

```bash
gh pr create --base main --head release/v1.0.0 \
  --title "Release v1.0.0" \
  --body "$(cat docs/releases/v1.0.0.md)"
```

- [x] **Step 5: Wait for CI on the PR; require human review** (this is the final gate before tagging)

---

## Self-Review

- [x] All Layer C integration tests passing on release/v1.0.0 ✓
- [x] All ~150 skill evals within tolerance ✓
- [x] Security review complete with zero open findings ✓
- [x] tests/_legacy/ removed ✓
- [x] Release notes drafted ✓
- [x] PR open from release/v1.0.0 → main ✓

**Done criteria:** PR is mergeable; CI green; release notes reviewed; tagging is the only remaining step (Phase 7).
