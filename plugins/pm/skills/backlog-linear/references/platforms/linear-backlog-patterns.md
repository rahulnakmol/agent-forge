# Linear Backlog Patterns

## Overview

When the user selects Linear as the target platform, the backlog generator creates
issues directly via the Linear MCP tools. This document describes how to structure
backlogs in Linear using projects, sub-issues, labels, and relations.

---

## Structural Mapping

| Backlog Concept     | Linear Construct         | Implementation                         |
|---------------------|--------------------------|----------------------------------------|
| Epic                | Issue + "epic" label     | Top-level issue in the project         |
| Feature             | Sub-issue of Epic        | Child issue with "feature" label       |
| User Story          | Sub-issue of Feature     | Child issue with "user-story" label    |
| Technical Story     | Sub-issue of Feature     | Child issue with "tech-story" label    |
| Risk                | Issue + "risk" label     | Standalone or related to Epic/Feature  |
| Impediment          | Issue + "impediment"     | Standalone issue                       |
| CI Item             | Issue + "ci-item" label  | Standalone issue                       |

---

## Label Taxonomy

Create these labels on the target team if they do not already exist. Use
`create_issue_label` for each missing label.

| Label Name   | Color    | Description                                    |
|-------------|----------|------------------------------------------------|
| epic         | #7C3AED  | Epic-level work item (strategic initiative)    |
| feature      | #2563EB  | Feature-level work item (capability)           |
| user-story   | #059669  | User story (user-facing requirement)           |
| tech-story   | #D97706  | Technical user story (infra/API/migration)     |
| risk         | #DC2626  | Risk item (potential threat to delivery)        |
| impediment   | #E11D48  | Impediment (blocking issue)                    |
| ci-item      | #8B5CF6  | Continuous improvement item                    |

### Label Check Before Creation

Before creating labels, use `list_issue_labels` (filtered by team) to check which
labels already exist. Only create missing labels. Match by exact name (case-insensitive).

---

## Priority Mapping

The PRD uses MoSCoW priority categories. Map them to Linear priority values:

| PRD Priority         | Linear Priority Value | Linear Priority Name | Description          |
|---------------------|----------------------|---------------------|----------------------|
| MH (Must Have)       | 2                    | High                | Critical for release |
| SH (Should Have)     | 3                    | Normal              | Important, not blocking |
| CH (Could Have)      | 4                    | Low                 | Nice to have         |
| WH (Won't Have)      | 0                    | No Priority         | Deferred / out of scope |

When no priority is specified in the PRD, default to priority 3 (Normal).

---

## Parent-Child Hierarchy via parentId

Linear supports sub-issues via the `parentId` field on `save_issue`.

### Creation Order (Critical)

Issues must be created in top-down order because child issues need the parent's ID:

1. Create all Epic-level issues first. Record their returned IDs.
2. Create all Feature-level issues with `parentId` set to their parent Epic's ID.
   Record their returned IDs.
3. Create all User Story and Technical Story issues with `parentId` set to their
   parent Feature's ID.
4. Create Risk, Impediment, and CI Item issues (no parentId unless they are
   sub-issues of an Epic or Feature).

### Example Invocation Sequence

```
Step 1: save_issue(title="Customer Onboarding", labels=["epic"], priority=2, ...)
        -> returns epicId = "abc-123"

Step 2: save_issue(title="Self-Service Registration", labels=["feature"],
                   parentId="abc-123", priority=2, ...)
        -> returns featureId = "def-456"

Step 3: save_issue(title="As a customer, I want to register with email",
                   labels=["user-story"], parentId="def-456", priority=2, ...)
```

---

## Relations: blocks, blockedBy, relatedTo

Linear supports three relation types that can be set on `save_issue`:

| Relation   | Purpose                                          | Usage                        |
|-----------|--------------------------------------------------|------------------------------|
| blocks     | This issue blocks another issue                  | Pass array of issue IDs      |
| blockedBy  | This issue is blocked by another issue           | Pass array of issue IDs      |
| relatedTo  | This issue is related to another issue           | Pass array of issue IDs      |

### When to Use Relations

- **blocks/blockedBy**: Use when the PRD identifies explicit dependencies between
  features or stories (e.g., "Authentication must be complete before Payment
  integration can begin").
- **relatedTo**: Use when cross-referencing finds existing issues that overlap with
  new backlog items.

### Relation Creation Timing

Relations can only reference issues that already exist. Therefore:
1. Create all issues first (in hierarchy order).
2. Then update issues with relations using `save_issue` with the issue ID and
   the relation fields.

---

## Project and Team Selection Workflow

### Step 1: List Available Teams

Call `list_teams` to get all teams. Present the list to the user and ask them to
select the target team.

### Step 2: List Projects for Selected Team

Call `list_projects` with the team filter. Present available projects. The user
can either:
- Select an existing project (recommended for adding to an existing initiative).
- Request creation of a new project (use `save_project` if available).

### Step 3: Confirm Configuration

Before creating any issues, confirm with the user:
- Team name and ID
- Project name and ID
- Label set (which labels exist, which need to be created)

---

## Cross-Referencing Existing Issues

Before creating new issues, check for existing items that may overlap:

### Query Strategy

1. Call `list_issues` with:
   - `team` = selected team ID
   - `project` = selected project ID (if applicable)
   - `state` = open states (Backlog, Todo, In Progress)
2. Compare each planned backlog item title against existing issue titles.
3. Flag matches with similarity above 70%.

### Handling Duplicates

| Scenario               | Action                                              |
|------------------------|-----------------------------------------------------|
| Exact title match      | Skip creation, link as relatedTo                    |
| High similarity (>70%) | Present to user for decision (skip, merge, create)  |
| Partial overlap        | Create new issue, add relatedTo link to existing    |
| No match               | Create new issue                                    |

---

## Issue Description Format

Use markdown in Linear issue descriptions:

### Epic Description Template
```markdown
## Overview
[High-level description of the epic]

## Business Justification
[Why this epic matters]

## Scope
**In scope:**
- [Item 1]
- [Item 2]

**Out of scope:**
- [Exclusion 1]

## Success Metrics
- [KPI 1]
- [KPI 2]
```

### User Story Description Template
```markdown
## User Story
As a **[persona]**, I **[want to]** so that **[benefit]**.

## Context
[Additional context]

## Acceptance Criteria
- [ ] Given [precondition], When [action], Then [result]
- [ ] Given [precondition], When [action], Then [result]

## Notes
[Any additional notes or assumptions]
```

---

## Estimation in Linear

Linear uses a numeric `estimate` field. Map story points directly:

| Story Points | Linear Estimate |
|-------------|----------------|
| 1            | 1              |
| 2            | 2              |
| 3            | 3              |
| 5            | 5              |
| 8            | 8              |
| 13           | 13             |
| 21           | 21             |

Only set estimates on User Story and Technical User Story issues. Epics and
Features do not receive direct estimates (their effort is the sum of child stories).
