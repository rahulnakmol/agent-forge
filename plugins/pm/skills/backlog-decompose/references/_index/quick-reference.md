# Backlog Generator Quick Reference

## Workflow Phases at a Glance

| Phase | Name                    | Key Action                                      |
|-------|-------------------------|------------------------------------------------|
| 1     | PRD Analysis            | Parse PRD, extract epics/features/stories      |
| 2     | Platform Selection      | Choose ADO, Linear, or GitHub; configure target |
| 3     | Cross-Reference         | Check for existing issues, flag duplicates      |
| 4     | Backlog Construction    | Build hierarchy, generate tech stories, risks   |
| 5     | Platform Output         | Create items or generate import files           |
| 6     | Summary & Validation    | Report statistics, list created items           |

---

## Platform Modes

| Mode   | Output Format         | Creation Method         | Hierarchy Mechanism     |
|--------|-----------------------|-------------------------|-------------------------|
| ADO    | CSV + Excel workbook  | Manual import           | Parent column in CSV    |
| Linear | Live issue creation   | save_issue MCP tool     | parentId field          |
| GitHub | Live issue creation   | issue_write MCP tool    | sub_issue_write tool    |

---

## Work Item Types

| Type                       | ADO WIT                   | Linear Label    | GitHub Label    |
|----------------------------|---------------------------|-----------------|-----------------|
| Epic                       | Epic                      | epic            | epic            |
| Feature                    | Feature                   | feature         | feature         |
| User Story                 | User Story                | user-story      | user-story      |
| Technical User Story       | Technical User Story      | tech-story      | tech-story      |
| Risk                       | Risk                      | risk            | risk            |
| Impediment                 | Impediment                | impediment      | impediment      |
| Continuous Improvement     | Continuous Improvement    | ci-item         | ci-item         |

---

## ADO Field Mapping Quick Reference

| Field               | Applies To                | Values / Format                        |
|---------------------|---------------------------|----------------------------------------|
| Priority            | All                       | 1, 2, 3                               |
| Risk                | Epic, Feature, Story      | 1-High, 2-Medium, 3-Low               |
| Value Area          | Epic, Feature, Story      | Business, Architectural                |
| Story Points        | User Story, Tech Story    | Fibonacci: 1, 2, 3, 5, 8, 13, 21     |
| Effort              | Feature                   | Numeric (hours)                        |
| Business Value      | Feature                   | 1-100 scale                            |
| Time Criticality    | Feature                   | 1-100 scale                            |
| Likelihood (Risk)   | Risk                      | 1=Very Likely .. 5=Very Unlikely       |
| Impact (Risk)       | Risk                      | A=Severe .. E=Negligible               |
| Risk Assessment     | Risk                      | 1=High .. 5=Low                        |
| State               | All                       | New (always for new items)             |

---

## Linear MCP Tool Quick Reference

| Tool                | Purpose                           | Key Parameters                      |
|---------------------|-----------------------------------|-------------------------------------|
| list_teams          | Get available teams               | (none)                              |
| list_projects       | Get projects for a team           | team                                |
| list_issues         | Query existing issues             | team, project, state, label, query  |
| get_issue           | Get issue details                 | issueId, includeRelations           |
| save_issue          | Create or update issue            | title, team, project, description,  |
|                     |                                   | priority, labels, parentId,         |
|                     |                                   | estimate, dueDate, state            |
| create_issue_label  | Create a new label                | name, color, description, teamId    |

### Linear Priority Mapping

| PRD Priority | Linear Priority Value | Linear Priority Name |
|-------------|----------------------|---------------------|
| MH (Must Have)   | 2                | High                |
| SH (Should Have) | 3                | Normal              |
| CH (Could Have)  | 4                | Low                 |

---

## GitHub MCP Tool Quick Reference

| Tool              | Purpose                        | Key Parameters                       |
|-------------------|--------------------------------|--------------------------------------|
| issue_write       | Create issue                   | method=create, owner, repo, title,   |
|                   |                                | body, labels, assignees, type        |
| issue_read        | Get issue details              | method=get, owner, repo, issue_number|
| list_issues       | List repo issues               | owner, repo, state=OPEN, labels      |
| search_issues     | Search issues by query         | query, owner, repo                   |
| sub_issue_write   | Add sub-issue relationship     | method=add, owner, repo,             |
|                   |                                | issue_number, sub_issue_id           |
| list_issue_types  | Get org issue types            | owner                                |
| add_issue_comment | Add comment to issue           | owner, repo, issue_number, body      |

---

## File Naming and Output Paths

### ADO Output Files
- CSV: `backlog-{prd-name}-ado-import.csv`
- Excel: `backlog-{prd-name}-ado-workbook.xlsx`

### Markdown Output Files
- Full backlog: `backlog-{prd-name}-full.md`
- Summary: `backlog-{prd-name}-summary.md`

### Output Directory
All files are written to the current working directory unless the user specifies
an alternative path.

---

## PRD Section to Backlog Type Mapping

| PRD Section               | Backlog Item Type              |
|---------------------------|-------------------------------|
| Section 3 (Epic Def)      | Epic                          |
| Section 5 (Key Features)  | Feature                       |
| Section 4 (User Stories)  | User Story                    |
| Section 7.3 (Risks)       | Risk                          |
| Section 3.3 (Dependencies)| Impediment                    |
| Non-functional / Arch     | Technical User Story          |
| Process gaps / Assumptions| Continuous Improvement Item   |
