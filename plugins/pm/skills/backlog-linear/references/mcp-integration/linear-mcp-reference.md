# Linear MCP Tool Reference

## Overview

This document provides a complete reference for the Linear MCP tools used by the
PM Backlog Generator skill. These tools are invoked via the Linear MCP server
connection to create and query issues in Linear.

---

## Tool: save_issue

### Purpose
Create a new issue or update an existing issue in Linear.

### Parameters

| Parameter    | Type     | Required | Description                                      |
|-------------|----------|----------|--------------------------------------------------|
| title        | string   | Yes      | Issue title (max 255 characters)                 |
| team         | string   | Yes      | Team ID (UUID) -- get from list_teams             |
| project      | string   | No       | Project ID (UUID) -- get from list_projects       |
| description  | string   | No       | Issue description (markdown supported)           |
| priority     | integer  | No       | 0=No priority, 1=Urgent, 2=High, 3=Normal, 4=Low|
| labels       | string[] | No       | Array of label IDs (UUID) -- get from list_issue_labels |
| parentId     | string   | No       | Parent issue ID for sub-issue hierarchy          |
| assignee     | string   | No       | Assignee user ID (UUID) -- get from list_users    |
| estimate     | integer  | No       | Story point estimate (numeric)                   |
| dueDate      | string   | No       | Due date in ISO 8601 format (YYYY-MM-DD)         |
| state        | string   | No       | State ID (UUID) -- get from list_issue_statuses   |
| blocks       | string[] | No       | Array of issue IDs that this issue blocks        |
| blockedBy    | string[] | No       | Array of issue IDs that block this issue         |
| relatedTo    | string[] | No       | Array of issue IDs related to this issue         |
| links        | object[] | No       | Array of link objects {url, label}               |

### Response

Returns the created/updated issue object including:
- `id`: Issue UUID (use for parentId, relations)
- `identifier`: Human-readable identifier (e.g., "TEAM-123")
- `title`: Issue title
- `url`: Direct URL to the issue in Linear

### Usage Notes

1. The `team` parameter is always required, even when specifying a project.
2. The `labels` parameter expects label IDs, not label names. Use
   `list_issue_labels` to get the mapping.
3. When creating sub-issues, the `parentId` must reference an existing issue.
   Create parent issues first.
4. The `state` parameter is optional. If omitted, the issue is created in the
   team's default state (usually "Backlog" or "Triage").
5. Relations (blocks, blockedBy, relatedTo) can only reference existing issues.
   Create all issues first, then add relations in a second pass.

### Example: Create an Epic

```json
{
  "title": "Customer Onboarding Platform",
  "team": "team-uuid-here",
  "project": "project-uuid-here",
  "description": "## Overview\nPlatform for customer self-service onboarding...",
  "priority": 2,
  "labels": ["epic-label-uuid"]
}
```

### Example: Create a User Story as Sub-Issue

```json
{
  "title": "As a customer, I want to register with my email so that I can access the platform",
  "team": "team-uuid-here",
  "project": "project-uuid-here",
  "description": "## User Story\nAs a **customer**, I **want to register**...\n\n## Acceptance Criteria\n- [ ] Given...",
  "priority": 2,
  "labels": ["user-story-label-uuid"],
  "parentId": "parent-feature-uuid",
  "estimate": 5
}
```

---

## Tool: list_issues

### Purpose
Query existing issues with filters. Used for cross-referencing before creating
new issues.

### Parameters

| Parameter | Type   | Required | Description                                       |
|----------|--------|----------|---------------------------------------------------|
| team      | string | No       | Filter by team ID                                 |
| project   | string | No       | Filter by project ID                              |
| state     | string | No       | Filter by state name(s), comma-separated          |
| assignee  | string | No       | Filter by assignee user ID                        |
| label     | string | No       | Filter by label name                              |
| query     | string | No       | Full-text search query                            |
| parentId  | string | No       | Filter by parent issue ID (get sub-issues)        |

### Response

Returns an array of issue objects, each containing:
- `id`: Issue UUID
- `identifier`: Human-readable identifier
- `title`: Issue title
- `description`: Issue description
- `state`: Current state name
- `priority`: Priority value
- `labels`: Array of label objects
- `url`: Direct URL

### Usage Notes

1. Combine filters for precise queries: `team` + `project` + `state`.
2. The `query` parameter performs full-text search on title and description.
3. Use `parentId` to find all sub-issues of a specific issue.
4. Results may be paginated. Handle pagination if the response indicates more
   results are available.
5. For cross-referencing, query with `state` = open states (backlog, todo,
   in_progress) to avoid matching closed/completed items.

---

## Tool: list_teams

### Purpose
Get all teams in the Linear workspace. Used in Phase 2 to let the user select
a target team.

### Parameters

None required.

### Response

Returns an array of team objects:
- `id`: Team UUID (use in save_issue)
- `name`: Team display name
- `key`: Team key prefix (e.g., "ENG", "PROD")

### Usage Notes

1. Present the team list to the user for selection.
2. Store the selected team ID for all subsequent operations.
3. Teams determine the issue identifier prefix and available states.

---

## Tool: list_projects

### Purpose
Get projects, optionally filtered by team. Used in Phase 2 to let the user
select a target project.

### Parameters

| Parameter | Type   | Required | Description                        |
|----------|--------|----------|------------------------------------|
| team      | string | No       | Filter by team ID                  |

### Response

Returns an array of project objects:
- `id`: Project UUID (use in save_issue)
- `name`: Project display name
- `state`: Project state (planned, started, completed, etc.)

### Usage Notes

1. Filter by the selected team to show relevant projects.
2. Only show projects in "planned" or "started" state.
3. If no suitable project exists, the user may choose to create one.
4. Projects are optional in Linear -- issues can exist without a project.

---

## Tool: get_issue

### Purpose
Get full details of a specific issue, optionally including relations. Used for
deep cross-reference checks.

### Parameters

| Parameter         | Type    | Required | Description                          |
|-------------------|---------|----------|--------------------------------------|
| issueId           | string  | Yes      | Issue ID or identifier (e.g., "ENG-123") |
| includeRelations  | boolean | No       | Include related issues in response   |

### Response

Returns the full issue object including:
- All standard fields (title, description, state, priority, etc.)
- `children`: Array of sub-issues (if any)
- `relations`: Array of related issues (if includeRelations=true)
- `comments`: Recent comments
- `attachments`: Attached files

### Usage Notes

1. Use `includeRelations=true` when checking for existing links.
2. Check the `children` array to understand existing hierarchy.
3. Read `comments` for additional context on the issue.

---

## Tool: create_issue_label

### Purpose
Create a new label on a team. Used to set up the label taxonomy before creating
issues.

### Parameters

| Parameter   | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| name        | string | Yes      | Label name (e.g., "epic", "user-story")  |
| color       | string | No       | Hex color code (e.g., "#7C3AED")         |
| description | string | No       | Label description                        |
| teamId      | string | No       | Team ID (scope label to a specific team) |

### Response

Returns the created label object:
- `id`: Label UUID (use in save_issue labels array)
- `name`: Label name
- `color`: Label color

### Usage Notes

1. Check existing labels first with `list_issue_labels` before creating.
2. If `teamId` is omitted, the label is created as a workspace-level label.
3. Team-level labels are preferred for backlog generation to avoid polluting
   the workspace-level label list.

---

## Invocation Sequence for Backlog Creation

### Phase 2: Platform Configuration

```
1. list_teams()
   -> User selects team -> store teamId

2. list_projects(team=teamId)
   -> User selects project -> store projectId

3. list_issue_labels(team=teamId)
   -> Check which labels exist
   -> For each missing label: create_issue_label(name, color, teamId)
   -> Store label ID mapping: {"epic": "uuid1", "feature": "uuid2", ...}

4. list_issue_statuses(team=teamId)
   -> Identify the "Backlog" or "Triage" state -> store default stateId
```

### Phase 3: Cross-Reference

```
5. list_issues(team=teamId, project=projectId, state="backlog,todo,in_progress")
   -> Store existing issues for comparison

6. For each planned backlog item:
   -> Compare title against existing issues
   -> Flag duplicates and overlaps
   -> Present to user for review
```

### Phase 5: Issue Creation

```
7. For each Epic (in priority order):
   save_issue(title, team=teamId, project=projectId, labels=[epicLabelId],
              priority, description)
   -> Store returned ID as epicId

8. For each Feature (grouped by parent Epic):
   save_issue(title, team=teamId, project=projectId, labels=[featureLabelId],
              priority, description, parentId=epicId)
   -> Store returned ID as featureId

9. For each User Story / Tech Story (grouped by parent Feature):
   save_issue(title, team=teamId, project=projectId,
              labels=[storyLabelId], priority, description,
              parentId=featureId, estimate=storyPoints)

10. For each Risk / Impediment / CI Item:
    save_issue(title, team=teamId, project=projectId,
               labels=[typeLabelId], priority, description)

11. For items with relations (from PRD dependencies):
    save_issue(id=existingIssueId, blocks=[...], blockedBy=[...], relatedTo=[...])
```

---

## Error Handling Patterns

### Common Errors and Recovery

| Error                          | Cause                              | Recovery                           |
|-------------------------------|------------------------------------|------------------------------------|
| "Team not found"              | Invalid team ID                    | Re-run list_teams, re-select      |
| "Project not found"           | Invalid project ID                 | Re-run list_projects, re-select   |
| "Label not found"             | Label ID does not exist            | Re-create label, update ID map    |
| "Parent issue not found"      | parentId references missing issue  | Verify parent was created first   |
| "Rate limited"                | Too many API calls                 | Wait and retry with backoff       |
| "Permission denied"           | Insufficient access                | Ask user to check permissions     |

### Retry Strategy

1. On rate limit errors: wait 2 seconds, then retry.
2. On transient errors (500, timeout): retry up to 3 times with exponential backoff.
3. On permanent errors (400, 403, 404): do not retry; log the error and continue
   with the next item.
4. After all items are processed, report any failures in the summary.

### Partial Failure Handling

If some issues fail to create:
1. Continue creating remaining issues.
2. Skip child issues whose parent failed (they cannot be linked).
3. Report all failures with details in the backlog summary.
4. Provide a list of items that need manual creation.
