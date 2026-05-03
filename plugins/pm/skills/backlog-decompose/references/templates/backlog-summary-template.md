# Backlog Summary Report Template

## Overview

This template defines the structure of the summary report generated after backlog
creation. The summary provides a concise overview of what was generated, key
statistics, and platform-specific creation details.

---

## Document Structure

```markdown
# Backlog Summary Report

**PRD**: {prd-name}
**Generated**: {YYYY-MM-DD HH:MM}
**Platform**: {ADO | Linear | GitHub}
**Total Items Created**: {count}
```

---

## Section: Backlog Statistics Table

### Template

```markdown
## Backlog Statistics

| Work Item Type              | Count | % of Total |
|-----------------------------|-------|------------|
| Epic                        | {n}   | {%}        |
| Feature                     | {n}   | {%}        |
| User Story                  | {n}   | {%}        |
| Technical User Story        | {n}   | {%}        |
| Risk                        | {n}   | {%}        |
| Impediment                  | {n}   | {%}        |
| Continuous Improvement Item | {n}   | {%}        |
| **Total**                   | **{n}** | **100%** |
```

---

## Section: Priority Distribution

### Template

```markdown
## Priority Distribution

| Priority          | Items | Story Points | % of Items | % of Points |
|-------------------|-------|-------------|------------|-------------|
| 1 - Must Have     | {n}   | {pts}       | {%}        | {%}         |
| 2 - Should Have   | {n}   | {pts}       | {%}        | {%}         |
| 3 - Could Have    | {n}   | {pts}       | {%}        | {%}         |
| **Total**         | **{n}** | **{pts}** | **100%**   | **100%**    |

### Distribution Health Check

- [ ] Must Have items are ~60% of total (actual: {%})
- [ ] Should Have items are ~20% of total (actual: {%})
- [ ] Could Have items are ~20% of total (actual: {%})
- [ ] No single epic contains more than 40% of total points

{If distribution is significantly off, add a warning note:}
> **Warning**: Priority distribution deviates from recommended MoSCoW ratios.
> Consider re-prioritizing items before sprint planning.
```

---

## Section: Estimation Summary

### Template

```markdown
## Estimation Summary

| Metric                              | Value     |
|-------------------------------------|-----------|
| Total Story Points (User Stories)   | {n}       |
| Total Story Points (Tech Stories)   | {n}       |
| Combined Story Points               | {n}       |
| Average Points per User Story       | {n.n}     |
| Average Points per Tech Story       | {n.n}     |
| Largest Story                       | {title} ({n} pts) |
| Smallest Story                      | {title} ({n} pts) |

### Sprint Capacity Planning

| Scenario                    | Velocity | Sprints Needed | Duration   |
|-----------------------------|----------|----------------|------------|
| Conservative (team of 5)    | {n} pts  | {n}            | {n} weeks  |
| Moderate (team of 5)        | {n} pts  | {n}            | {n} weeks  |
| Aggressive (team of 5)      | {n} pts  | {n}            | {n} weeks  |

*Velocity assumptions: Conservative = 20 pts/sprint, Moderate = 30 pts/sprint,
Aggressive = 40 pts/sprint for a team of 5 developers in 2-week sprints.*
```

---

## Section: Platform-Specific Creation Summary

### ADO Template

```markdown
## Platform Output: Azure DevOps

### Generated Files

| File                                    | Path                              |
|-----------------------------------------|-----------------------------------|
| CSV Import File                         | `{path}/backlog-{name}-ado-import.csv` |
| Excel Workbook                          | `{path}/backlog-{name}-ado-workbook.xlsx` |
| Full Backlog (Markdown)                 | `{path}/backlog-{name}-full.md`   |

### Import Instructions

1. Open Azure DevOps and navigate to **Boards > Backlogs**.
2. Click the **...** menu and select **Import Work Items**.
3. Upload the CSV file: `backlog-{name}-ado-import.csv`.
4. Review the field mapping and confirm.
5. Verify parent-child relationships in the backlog view.

### Pre-Import Checklist

- [ ] Area paths exist in the ADO project: `{area-path}`
- [ ] Iteration paths exist: `{iteration-path}`
- [ ] No duplicate titles in the existing backlog
- [ ] CSV file is UTF-8 encoded
```

### Linear Template

```markdown
## Platform Output: Linear

### Created Issues

| Identifier | Type         | Title                              | Priority |
|------------|-------------|-------------------------------------|----------|
| {TEAM-1}   | Epic        | {title}                            | {p}      |
| {TEAM-2}   | Feature     | {title}                            | {p}      |
| {TEAM-3}   | User Story  | {title}                            | {p}      |
| ...        | ...         | ...                                | ...      |

### Creation Statistics

| Metric                | Count |
|-----------------------|-------|
| Issues Created        | {n}   |
| Sub-Issue Links       | {n}   |
| Relations Created     | {n}   |
| Labels Created        | {n}   |
| Skipped (duplicates)  | {n}   |
| Failed                | {n}   |

### Configuration Used

- **Team**: {team-name} ({team-key})
- **Project**: {project-name}
- **Labels**: {list of label names used}

{If there were failures:}
### Failed Items (Require Manual Creation)

| Title                           | Type         | Error                    |
|---------------------------------|-------------|--------------------------|
| {title}                         | {type}      | {error message}          |
```

### GitHub Template

```markdown
## Platform Output: GitHub

### Created Issues

| Number | Type         | Title                              | Priority | Labels        |
|--------|-------------|-------------------------------------|----------|---------------|
| #{n}   | Epic        | {title}                            | {p}      | epic, pri-high|
| #{n}   | Feature     | {title}                            | {p}      | feature, ...  |
| #{n}   | User Story  | {title}                            | {p}      | user-story,...|
| ...    | ...         | ...                                | ...      | ...           |

### Creation Statistics

| Metric                  | Count |
|-------------------------|-------|
| Issues Created          | {n}   |
| Sub-Issue Links Created | {n}   |
| Comments Added          | {n}   |
| Skipped (duplicates)    | {n}   |
| Failed                  | {n}   |

### Configuration Used

- **Repository**: {owner}/{repo}
- **Issue Types**: {enabled/disabled}
- **Labels Used**: {list of label names}

### Quick Links

- [All Epic Issues](https://github.com/{owner}/{repo}/issues?q=label%3Aepic)
- [All Open Backlog Items](https://github.com/{owner}/{repo}/issues?q=is%3Aopen)

{If there were failures:}
### Failed Items (Require Manual Creation)

| Title                           | Type         | Error                    |
|---------------------------------|-------------|--------------------------|
| {title}                         | {type}      | {error message}          |
```

---

## Section: Next Steps

### Template

```markdown
## Recommended Next Steps

1. **Review the backlog** with the product owner and development team.
2. **Refine estimates** during a team estimation session (planning poker).
3. **Prioritize** items within each priority band based on team input.
4. **Assign to sprints** starting with Priority 1 (Must Have) items.
5. **Identify dependencies** and resolve impediments before sprint planning.
6. **Review risks** and assign owners for mitigation plans.
7. **Address CI items** to improve future backlog generation quality.
```

---

## File Output

- **File name**: `backlog-{prd-name}-summary.md`
- **Encoding**: UTF-8
- **Line endings**: LF (Unix-style)
