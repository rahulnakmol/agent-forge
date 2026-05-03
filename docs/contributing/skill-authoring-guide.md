# Skill authoring guide

This guide covers everything you need to write a high-quality skill for agent-forge.
Skills are the atomic unit of the marketplace: one skill, one domain, one purpose.

## SKILL.md frontmatter spec

Every skill starts with YAML frontmatter. All fields except `allowed-tools` are required.

```yaml
---
name: skill-name          # string, kebab-case, max 30 chars, must match directory name
description: >
  Multi-line trigger description. This is the most important field.
  Claude Code reads this to decide whether to route a user request to your skill.
  Include: explicit trigger phrases ("when the user says X"), use cases, and
  any conditions where the skill should NOT be used.
license: BSD-3-Clause     # or "Complete terms in LICENSE.txt" if a separate file exists
version: 1.0.0            # semver, start at 1.0.0
allowed-tools:            # list of Claude Code tools this skill may use (optional)
  - Read                  # include only tools the skill actually needs
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---
```

**`description` field best practices:**
- Start with the trigger phrase: "This skill should be used when the user..."
- Include synonyms users might say: "humanize", "make this human", "remove AI patterns"
- Specify scope: what the skill does AND what it does NOT do
- Keep it under 300 words — longer descriptions dilute routing accuracy

**`allowed-tools` guidance:**
- Omit the field entirely if your skill is prose-only (no file I/O)
- Never request `Bash` unless the skill genuinely executes scripts
- Request only what you need — principle of least privilege

## Progressive disclosure pattern

Skills should be written so a capable LLM can execute them using only `SKILL.md`.
Supporting files in subdirectories extend capability without requiring them.

```
skills/<skill-name>/
  SKILL.md                  ← core skill, standalone-complete
  LICENSE.txt               ← required for all skills
  references/               ← reference documents (optional)
    style-guide.md          ← referenced from SKILL.md body
    voice-profiles.json     ← data the skill reads via Read tool
  scripts/                  ← executable helpers (optional)
    analyze-patterns.py     ← invoked via Bash tool
    score-output.py
  assets/                   ← static files (optional)
    sample-input.txt        ← example inputs for testing
    rubric-template.md
```

**References:** Documents the skill reads during execution. Reference them in
SKILL.md with: `See [voice profiles](./references/voice-profiles.json)`. The skill
uses the `Read` tool to load them on demand.

**Scripts:** Python or shell scripts the skill executes via the `Bash` tool. Keep
scripts focused: one script, one analysis. Scripts must work with Python 3.9+.

**Assets:** Static files the skill may reference (examples, templates, data). Assets
are read-only — never write to `assets/`.

## Naming conventions

| Item | Convention | Max length | Example |
|---|---|---|---|
| Plugin name | kebab-case | 30 chars | `msft-arch` |
| Skill name | kebab-case | 30 chars | `humanize`, `prompt-forge` |
| Skill directory | same as skill name | 30 chars | `skills/humanize/` |
| Reference files | kebab-case with extension | — | `voice-profiles.json` |
| Script files | kebab-case with extension | — | `analyze-patterns.py` |

**Do not use:** CamelCase, snake_case, spaces, dots (except in extensions).

## Eval requirements

Every skill **must** include an eval suite in `tests/evals/<plugin>/<skill>/`.
This is a hard requirement — PRs without evals will not be merged.

### Required files

**`inputs.json`** — array of test cases:
```json
[
  {
    "id": "case-identifier",
    "description": "What this case tests",
    "user_message": "The exact message a user would send",
    "expected_behavior": "What the skill output should achieve (not exact text)"
  }
]
```

Minimum 3 inputs per skill. Cover: happy path, edge case, and at least one
case where the skill should decline or handle gracefully.

**`rubric.md`** — evaluation criteria:
```markdown
# Eval Rubric: <skill-name>

## Criteria

| Criterion | Weight | Pass condition |
|---|---|---|
| <Criterion 1> | N% | <Observable, measurable condition> |
| <Criterion 2> | N% | <Observable, measurable condition> |

## Scoring

- Pass: weighted average ≥ 0.8
- Fail: any criterion below 0.5

## Notes

<Any special instructions for the LLM judge evaluating outputs>
```

Weights must sum to 100%. Criteria must be observable (an LLM judge can evaluate them).

## Worked examples

### Example 1: Prose-only skill (no supporting files)

The simplest skill type — instructions embedded entirely in SKILL.md.

```
skills/summarize/
  SKILL.md
  LICENSE.txt
```

`SKILL.md` body structure:
```markdown
# Summarize

Reduce any text to its essential points without losing meaning.

## When to use

Apply when the user asks to "summarize", "TL;DR", "give me the key points", or
"shorten this".

## Output format

Return a bulleted list of 3-7 key points, each ≤ 20 words.

## Quality bar

Each bullet should be independently meaningful without requiring the original context.
```

### Example 2: Skill with `scripts/`

A skill that executes a Python script to analyze input before responding.

```
skills/analyze-tone/
  SKILL.md
  LICENSE.txt
  scripts/
    tone-detector.py
```

In `SKILL.md`, reference and invoke the script:
```markdown
## Analysis phase

Before rewriting, run the tone detector:

```bash
python skills/analyze-tone/scripts/tone-detector.py --input "{user_text}"
```

Use the output to calibrate your rewrite. The detector returns a JSON object
with `formality`, `sentiment`, and `ai_probability` scores.
```

The script should accept `--input` and return JSON to stdout.

### Example 3: Skill with `assets/`

A skill that uses a reference dataset and example assets.

```
skills/voice-calibrate/
  SKILL.md
  LICENSE.txt
  references/
    regional-voices.json
  assets/
    sample-oxford.txt
    sample-sanfrancisco.txt
```

In `SKILL.md`, reference assets for calibration:
```markdown
## Voice calibration

Read the regional voice profiles:

```
Read: skills/voice-calibrate/references/regional-voices.json
```

For each requested voice shortcode, load the corresponding sample from `assets/`
to calibrate your output against a known-good example.
```

Assets give the skill grounding data without requiring external fetches.

## Common mistakes to avoid

1. **Vague description field** — "This skill helps with writing" routes nothing. Be specific.
2. **Requesting tools you don't use** — adds surface area without benefit.
3. **Skipping evals** — the CI gate will reject your PR.
4. **Hardcoding paths** — use relative paths from the skill directory, not absolute paths.
5. **Scripts with external dependencies** — scripts must run with stdlib only (or document deps explicitly).
