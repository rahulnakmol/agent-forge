# Backlog Generator Framework Overview

## Purpose

The PM Backlog Generator skill transforms a Product Requirements Document (PRD) into
a structured, platform-ready product backlog. It supports three target platforms and
follows a six-phase workflow with progressive disclosure.

---

## Three Platform Modes

### 1. Azure DevOps (ADO) -- SAFe Agile

- Produces a CSV import file and an Excel workbook for bulk import into ADO.
- Uses the SAFe Agile hierarchy: Epic > Feature > User Story / Technical User Story.
- Includes supplementary work item types: Risk, Impediment, Continuous Improvement Item.
- Best for: Enterprise teams using SAFe, regulated industries, organizations with
  existing ADO project structures.

### 2. Linear

- Creates issues directly via Linear MCP tools (save_issue, create_issue_label).
- Uses projects for epic-level grouping and sub-issues for hierarchy.
- Labels encode work item type (epic, feature, user-story, tech-story, risk, etc.).
- Best for: Product-led engineering teams, startups, teams already using Linear for
  sprint planning.

### 3. GitHub

- Creates issues directly via GitHub MCP tools (issue_write, sub_issue_write).
- Uses labels for work item type classification and sub-issues for hierarchy.
- Best for: Open-source projects, teams with GitHub-centric workflows, projects that
  need issue tracking close to the code.

---

## Six-Phase Workflow

### Phase 1: PRD Analysis and Extraction

- Parse the PRD document to extract epics, features, user stories, risks, and
  dependencies.
- Identify technical story candidates from non-functional requirements and
  architectural decisions.
- Map PRD sections to backlog item types (see methodology/prd-to-backlog-decomposition.md).

### Phase 2: Platform Selection and Configuration

- Prompt the user to select a target platform (ADO, Linear, GitHub).
- For Linear: use list_teams and list_projects to select target team and project.
- For GitHub: confirm repository owner and name.
- For ADO: confirm area path and iteration path conventions.

### Phase 3: Cross-Reference Existing Items

- Query the target platform for existing issues that overlap with the new backlog.
- Linear: list_issues filtered by project and state.
- GitHub: search_issues with keyword matching, list_issues with label filters.
- ADO: no live query -- user reviews CSV against existing backlog manually.
- Flag duplicates and partial overlaps for user review.

### Phase 4: Backlog Construction

- Build the hierarchical backlog: Epics > Features > Stories.
- Generate technical stories for infrastructure, API, migration, and observability
  needs not explicitly stated in the PRD.
- Create risk items, impediments, and continuous improvement items.
- Assign priorities, estimates, and metadata per platform conventions.

### Phase 5: Platform-Specific Output

- ADO: Generate CSV file and Excel workbook with five sheets.
- Linear: Create issues via MCP tools in dependency order (parents first).
- GitHub: Create issues via MCP tools in dependency order (parents first).
- All platforms: Generate a markdown summary document.

### Phase 6: Summary and Validation

- Produce a backlog summary report with statistics, priority distribution, and
  estimation totals.
- List all created items with IDs/numbers for traceability.
- Highlight any items that need manual review (duplicates, ambiguous requirements).

---

## When to Use Each Platform

| Criteria                        | ADO              | Linear           | GitHub           |
|---------------------------------|------------------|------------------|------------------|
| Team methodology                | SAFe / Agile     | Kanban / Scrum   | Any              |
| Organization size               | Enterprise       | Startup / SMB    | Any              |
| Compliance requirements         | High             | Low-Medium       | Low-Medium       |
| Integration with code           | Moderate         | Moderate         | High             |
| Existing tool investment        | ADO ecosystem    | Linear ecosystem | GitHub ecosystem |
| Offline / bulk import needed    | Yes (CSV/Excel)  | No (live API)    | No (live API)    |

---

## Cross-Referencing Strategy Overview

Before creating any new backlog items, the skill checks for existing work items on
the target platform. This prevents duplicates and ensures new items are linked to
related existing work.

- **Title similarity**: Compare new item titles against existing open items. Flag
  matches above 70% similarity.
- **Description overlap**: Check for shared keywords between new and existing item
  descriptions.
- **Linking**: When partial overlap is found, create relation links (Linear: relatedTo;
  GitHub: cross-reference in issue body) rather than duplicating.
- **User confirmation**: Always present potential duplicates to the user before
  creating or skipping items.

See methodology/cross-reference-strategy.md for the full strategy.

---

## Progressive Disclosure Model

The skill reveals complexity incrementally:

1. **Level 1 -- Summary**: Show the user a count of items by type and a hierarchical
   tree view before creating anything.
2. **Level 2 -- Detail on demand**: The user can expand any epic or feature to see
   child stories and their fields.
3. **Level 3 -- Full output**: After user confirmation, generate the complete backlog
   with all fields populated.
4. **Level 4 -- Platform creation**: Only after full output review does the skill
   create items on the target platform (Linear/GitHub) or produce the import file (ADO).

This model ensures the user maintains control and can adjust priorities, scope, or
hierarchy before any irreversible platform actions are taken.

---

## File Cross-References

| Topic                          | Reference File                                      |
|--------------------------------|-----------------------------------------------------|
| ADO SAFe work item types       | platforms/ado-safe-backlog.md                       |
| ADO CSV import format          | platforms/ado-csv-import-format.md                  |
| Linear patterns                | platforms/linear-backlog-patterns.md                |
| GitHub patterns                | platforms/github-backlog-patterns.md                |
| PRD decomposition methodology  | methodology/prd-to-backlog-decomposition.md         |
| Technical story generation     | methodology/technical-story-generation.md           |
| Cross-reference strategy       | methodology/cross-reference-strategy.md             |
| Linear MCP tools               | mcp-integration/linear-mcp-reference.md             |
| GitHub MCP tools               | mcp-integration/github-mcp-reference.md             |
| ADO workbook template          | templates/ado-workbook-template.md                  |
| Markdown backlog template      | templates/backlog-markdown-template.md              |
| Summary report template        | templates/backlog-summary-template.md               |
