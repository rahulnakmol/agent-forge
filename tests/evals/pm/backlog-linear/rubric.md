Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Linear Context Verification** — Collects team name and project name before creating issues. Calls `list_teams` and `list_projects` to verify they exist. If the project does not exist, confirms with user before creating it. Does not proceed to issue creation with unverified team/project context. Score 5 if team/project verification via MCP calls is described before creation; 1 if issues are created without verifying team and project existence.

2. **Duplicate Detection** — Calls `list_issues` with team ID to retrieve all open issues before creation. Compares backlog titles using fuzzy matching against existing issues. Flags potential duplicates for user decision (skip, update, or create new). Score 5 if duplicate detection is performed before any issue creation; 1 if issues are created without checking for duplicates.

3. **Label Creation for Missing Labels** — Calls `list_issue_labels` to check existing labels, then uses `create_issue_label` for any missing required labels: epic, feature, risk, impediment, ci-item. Does not assume labels exist. Score 5 if label existence check and creation of missing labels are both described; 1 if labels are assumed to exist without checking.

4. **Priority and Field Mapping Accuracy** — Correctly maps: backlog priority 1 → Linear Urgent/High; 2 → Medium; 3 → Low; story points → Linear Estimate field; work item type → Linear Label. Parent-child: captures IDs from `save_issue` calls for parent items and passes them as `parentId` for child items. Score 5 if all field mappings are correct including parentId linking; 1 if priority mapping is wrong or parentId linking is omitted.

5. **Summary Artifact Update** — After creation, updates `{project}/specs/backlog/backlog-summary.md` with: PRD reference, generation date, Linear team/project, item counts by type, story point totals, and Linear issue IDs for all created items. Score 5 if summary update with all required fields including Linear IDs is described; 1 if no summary update is performed.
