---
name: backlog-linear
description: >-
  Linear Backlog Exporter: creates Linear issues from platform-neutral
  backlog via MCP. TRIGGER when: user asks to create Linear issues from
  backlog, export backlog to Linear, push work items to Linear, or invokes
  /backlog-linear. Also triggers for: "create Linear issues", "push
  to Linear", "Linear backlog import", "issues in Linear from backlog".
  Creates hierarchical issues with labels, projects, cycles, and
  parent-child relations via Linear MCP server.
  DO NOT TRIGGER for backlog decomposition (use backlog-decompose).
  DO NOT TRIGGER for Azure DevOps export (use backlog-ado) or GitHub
  export (use backlog-github).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Linear Backlog Exporter

**Version**: 1.0 | **Role**: Linear Issue Creation Specialist
**Methodology**: Gather Context > Cross-Reference > Create Issues > Verify

You take platform-neutral backlog files produced by `backlog-decompose` and create issues directly in Linear via the Linear MCP server.

**MCP tools used** (available via Linear MCP server, not listed in allowed-tools):
`list_teams`, `list_projects`, `list_issues`, `list_issue_labels`, `create_issue_label`, `save_issue`

## Prerequisites

- **Platform-neutral backlog** must exist at `{project}/specs/backlog/{epic-name}-backlog.md`
- If no backlog file exists, invoke `/backlog-decompose` first
- **Linear MCP server** must be connected

## Phase 1: Gather Linear Context

Use `AskUserQuestion` to collect:

| Field | Required | Example |
|-------|----------|---------|
| Team name | Yes | `Platform Engineering` |
| Project name | Yes | `Q2 Auth Overhaul` (or create new) |
| Cycle | No | `Sprint 14` |

Then call `list_teams` and `list_projects` to confirm the team and project exist. If the project does not exist, confirm with user before creating it.

## Phase 2: Cross-Reference

Avoid creating duplicate issues:

1. Call `list_issues` with the team ID to retrieve all open issues
2. Compare generated backlog titles against existing issues using fuzzy matching
3. Flag potential duplicates -- ask user: skip, update existing, or create new
4. Call `list_issue_labels` to check for existing labels
5. Create missing labels with `create_issue_label` (e.g., `epic`, `feature`, `risk`, `impediment`, `ci-item`)

## Phase 3: Create Issues

Map backlog items to Linear issue fields:

| Backlog Field | Linear Field |
|---------------|-------------|
| Title | Title |
| Description + AC | Description (Markdown) |
| Priority (1/2/3) | Priority (Urgent/High/Medium/Low/None) |
| Work item type | Label |
| Story points | Estimate |
| Epic/Feature parent | Parent Issue ID |

Execute in order:
1. `save_issue` for all parent-level items (epics, then features) -- capture returned issue IDs
2. `save_issue` for all child items (stories, technical stories) with `parentId` set to parent issue ID
3. `save_issue` for risks, impediments, and CI items with `parentId` set to their linked epic

## Phase 4: Verify and Deliver

1. Confirm creation count matches expected count
2. Provide summary with issue links
3. Update `{project}/specs/backlog/backlog-summary.md` with: PRD reference, generation date, Linear team/project, item counts by type, story point totals, issue IDs for all created items

## Examples

**"Create Linear issues from the authentication backlog"** -> Read `authentication-backlog.md`, collect team/project context, list_issues to check duplicates, create_issue_label for missing labels, save_issue parents first capturing IDs, save_issue children with parentId, update `backlog-summary.md` with Linear issue IDs.

**"Push the full backlog to Linear"** -> Read all `*-backlog.md` files, confirm team and project, cross-reference all existing issues, create labels, create all issues in parent-first order, update `backlog-summary.md`.

## References

- `references/platforms/linear-backlog-patterns.md`
- `references/mcp-integration/linear-mcp-reference.md`

---

*backlog-linear v1.0 | Gather Context > Cross-Reference > Create Issues > Verify*
