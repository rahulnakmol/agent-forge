# Testing locally

agent-forge uses a three-layer test harness. Run layers in order: Layer A must pass
before Layer B, and Layer B must pass before tagging a release.

## Prerequisites

```bash
# Create and activate the virtualenv
python -m venv .venv
source .venv/bin/activate

# Install test dependencies
pip install -e "tests/[dev]"
# or
pip install pytest pytest-timeout
```

## Layer A — Unit tests (structural)

Layer A tests check plugin and skill structure, frontmatter validity, manifest
consistency, and artifact sync. They require no API key and complete in seconds.

**Run all unit tests:**
```bash
.venv/bin/pytest tests/unit -v
```

**Run a specific unit test file:**
```bash
.venv/bin/pytest tests/unit/test_skill_md_frontmatter.py -v
```

**What Layer A checks:**
- Every `SKILL.md` has required frontmatter fields (`name`, `description`, `license`, `version`)
- All `plugin.json` files are valid against the JSON schema
- All Tier 1a artifacts (`.claude-plugin/`, `.github/plugin/`, `.codex-plugin/`, `.cursor-plugin/`) are in sync with canonical sources
- No references to internal or proprietary content (e.g., KPMG residue check)
- All `THIRD_PARTY_NOTICES.md` files are in sync

Layer A runs on every PR via `.github/workflows/ci-structural.yml`.

## Layer B — Eval tests (LLM-judged)

Layer B runs each skill against its eval suite (`tests/evals/<plugin>/<skill>/`) and
uses an LLM judge to score outputs against the rubric. Requires `ANTHROPIC_API_KEY`.

**Run evals for a single skill:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/pytest tests/evals/writing/humanize -v
```

**Run evals for a full plugin:**
```bash
.venv/bin/pytest tests/evals/writing -v
```

**Run all evals:**
```bash
.venv/bin/pytest tests/evals -v
```

**Update baselines** (when intentionally improving skill output):
```bash
.venv/bin/pytest tests/evals/writing/humanize --update-baselines
```

This overwrites the stored baseline outputs. Review the diff before committing.

**What Layer B checks:**
- Skill output matches rubric criteria (scored by LLM judge)
- Output scores meet or exceed the stored baseline
- No regressions: if a skill previously scored 0.9, it cannot regress to 0.7

Layer B runs on PRs via `.github/workflows/ci-evals.yml` (requires secret `ANTHROPIC_API_KEY`).
Most contributors only run Layer A locally; CI handles Layer B.

## Layer C — Docker integration tests

Layer C tests the full install lifecycle for each Tier 2 target (Kilo Code, OpenCode,
Crush) using Docker. It verifies that `agent-forge install` correctly places files and
that the target CLI picks them up.

**Build and run the Kilo Code integration test:**
```bash
docker build -f tests/integration/dockerfiles/kilocode.Dockerfile . \
  && .venv/bin/pytest tests/integration/test_install_lifecycle_kilocode.py -v
```

**Run all integration tests:**
```bash
.venv/bin/pytest tests/integration -v
```

Layer C requires Docker to be installed and running. It is slow (2-5 minutes per target).

Layer C runs on release tags via `.github/workflows/ci-integration.yml`.

## Tier 1 artifact sync check

If you modify any plugin or the canonical marketplace, always verify artifacts are in sync:

```bash
python scripts/regenerate-tier1-artifacts.py --check
```

If it exits non-zero, regenerate:
```bash
python scripts/regenerate-tier1-artifacts.py
```

Then commit the updated artifact files along with your plugin changes. The unit test
`tests/unit/test_tier1_artifacts_sync.py` will catch any drift in CI.

## Running the full pre-PR check

Before opening a PR, run:

```bash
# 1. Regenerate artifacts
python scripts/regenerate-tier1-artifacts.py

# 2. Regenerate aggregate notices
python scripts/aggregate-notices.py

# 3. Regenerate install index
python scripts/build-install-index.py

# 4. Run all unit tests
.venv/bin/pytest tests/unit -v
```

All four steps should complete without errors.

## Common issues

**`ModuleNotFoundError` when running pytest:**
```bash
# Make sure you're using the virtualenv
source .venv/bin/activate
pip install -e "tests/[dev]"
```

**Layer B times out:**
```bash
# Increase timeout
.venv/bin/pytest tests/evals/writing/humanize -v --timeout=120
```

**Docker not found for Layer C:**
```bash
# Install Docker: https://docs.docker.com/get-docker/
# Then verify:
docker --version
```
