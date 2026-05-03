---
category: artifacts
loading_priority: 3
tokens_estimate: 900
keywords:
  - extension guide
  - new artifact
  - template
  - artifact creation
  - spec file
  - customization
  - patterns
version: "1.0"
last_updated: "2026-03-21"
---

# Artifact Extension Guide

This guide explains how to add new artifact types to the artifacts skill. Follow these steps to ensure consistency with existing artifacts and proper integration into the skill's generation pipeline.

## Steps to Define a New Artifact

### Step 1: Create the Spec File

Create a new file named `[artifact-name]-spec.md` in the `references/artifacts/` directory.

Use kebab-case for the file name. Examples:
- `deployment-runbook-spec.md`
- `cost-model-spec.md`
- `governance-matrix-spec.md`

### Step 2: Add YAML Frontmatter

Every spec file must include the following frontmatter fields:

```yaml
---
category: artifacts
loading_priority: 2
tokens_estimate: <estimated token count for the file>
keywords:
  - <keyword 1>
  - <keyword 2>
  - <keyword 3>
version: "1.0"
last_updated: "YYYY-MM-DD"
---
```

- `loading_priority`: Use 1 for the overview catalog, 2 for individual artifact specs, 3 for guides and supplementary material.
- `tokens_estimate`: Approximate token count for the file content. Helps the skill manage context window budget.
- `keywords`: 3-8 terms that help the skill locate this file during reference loading.

### Step 3: Define the Specification

Structure the spec file with the following sections:

1. **Title and purpose**: One-paragraph description of what the artifact captures and when it is generated.
2. **Sheet name(s)**: The Excel sheet name(s) for workbook artifacts.
3. **Column specifications**: For each column, define:
   - Column letter and header name
   - Width (in Excel character units)
   - Data type (text, number, date)
   - Wrap text (yes/no)
   - Data validation dropdown values (if applicable)
   - Color coding rules (if applicable)
   - Format pattern (if applicable, e.g., ID format)
4. **Formatting rules**: Header style, alternating rows, conditional formatting, freeze panes, auto-filter.
5. **Example data rows**: 3-6 representative rows demonstrating realistic content.
6. **xlsx skill invocation pattern**: The exact prompt pattern to invoke the xlsx skill.

### Step 4: Update the Master Catalog

Add the new artifact to the master table in `artifact-overview.md`:
- Artifact Name
- Type (xlsx, docx, pptx)
- Phase Generated
- Dependencies
- Description

Update the dependency graph if the new artifact has upstream or downstream relationships.

### Step 5: Update SKILL.md

Add an inline summary of the new artifact to the Phase 5 (Delivery) section of SKILL.md, so the skill knows to offer it during artifact generation.

### Step 6: Validate

Verify that:
- The spec file loads correctly (frontmatter parses without errors).
- Keywords are specific enough to avoid false matches during reference loading.
- Example data rows are realistic and cover edge cases.
- The xlsx invocation pattern produces a valid workbook when executed.

## Spec File Skeleton Template

```markdown
---
category: artifacts
loading_priority: 2
tokens_estimate: <estimate>
keywords:
  - <keyword>
version: "1.0"
last_updated: "YYYY-MM-DD"
---

# [Artifact Name] Workbook Specification

<One-paragraph description of purpose, phase, and dependencies.>

## Sheet: "[Sheet Name]"

### Column Specifications

#### Column A: [Header] (width: NN)
- <description>
- <format or validation rules>

#### Column B: [Header] (width: NN)
- <description>

<!-- Continue for all columns -->

### Formatting Rules

- **Header row:** Bold, dark blue background (#003366), white text, freeze pane.
- **Alternating row colors:** white (#FFFFFF) / light gray (#F2F2F2).
- **Auto-filter:** Enabled on all columns.
- **Conditional formatting:** <describe rules>.

### Example Data Rows

| Col A | Col B | Col C | ... |
| ----- | ----- | ----- | --- |
| ...   | ...   | ...   | ... |

### xlsx Skill Invocation Pattern

\```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet name: "[Sheet Name]"
- Columns: [list with widths]
- Data validation on [column]: [values]
- Header formatting: bold, #003366 background, white text
- Freeze top row, auto-filter enabled
- Data: [provide rows]
\```
```

## Common Patterns

### Data Validation Dropdowns
Used for columns with a fixed set of allowed values. Define the list in the column spec and reference it in the invocation pattern. Keep lists to 3-8 items for usability.

### Conditional Formatting
Apply background color changes based on cell value. Common uses:
- Priority columns (Critical=Red, High=Orange, Medium=Yellow, Low=Green)
- Status columns (Open=Red, In Progress=Yellow, Closed=Green)
- Type columns (each type gets a distinct color)

### Cross-References
Link entries between artifacts using reference IDs:
- ADR Ref No format: `MS-[TECH]-[PLATFORM]-[PROJECT]-XXX`
- RFR Reference format: `REQ-[XX]-[NNN]`
- Test ID format: `TST-[NNN]`

Cross-references enable traceability across the full artifact set. Always use the exact ID format from the source artifact.

### Summary Sheets
Add a second sheet with SUMIFS/COUNTIFS aggregations when the primary sheet has categorical columns. Include:
- Counts and totals by each dropdown category
- Percentage breakdowns
- Charts (pie for distribution, bar for comparison)
