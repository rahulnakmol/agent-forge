# Backlog Markdown Document Template

## Overview

This template defines the structure of the full backlog markdown document generated
by the PM Backlog Generator skill. The markdown file provides a human-readable view
of the complete backlog with all details.

---

## Document Structure

```markdown
# Product Backlog: {PRD Name}

**Generated**: {date}
**Source PRD**: {prd-file-name}
**Platform Target**: {ADO | Linear | GitHub}

---

## Summary Statistics

{summary statistics table}

---

## Hierarchical Tree View

{collapsible tree of all items}

---

## Epic Details

{detailed cards for each epic and its children}

---

## Risk Register

{all risk items}

---

## Impediments

{all impediment items}

---

## Continuous Improvement Items

{all CI items}

---

## Dependency Diagram

{mermaid diagram}

---

## Cross-Reference Log

{duplicate/overlap findings}
```

---

## Section: Summary Statistics

### Template

```markdown
## Summary Statistics

| Metric                  | Count |
|-------------------------|-------|
| Total Work Items        | {n}   |
| Epics                   | {n}   |
| Features                | {n}   |
| User Stories             | {n}   |
| Technical User Stories   | {n}   |
| Risks                   | {n}   |
| Impediments             | {n}   |
| CI Items                | {n}   |

### Priority Distribution

| Priority       | Count | Percentage |
|---------------|-------|------------|
| 1 (High/MH)   | {n}   | {%}        |
| 2 (Medium/SH)  | {n}   | {%}        |
| 3 (Low/CH)     | {n}   | {%}        |

### Estimation Summary

| Metric                        | Value   |
|-------------------------------|---------|
| Total Story Points            | {n}     |
| Average Points per Story      | {n.n}   |
| Estimated Sprints (at {n} pts/sprint) | {n} |
```

---

## Section: Hierarchical Tree View

### Template

Use collapsible `<details>` sections for each epic to keep the document navigable.

```markdown
## Hierarchical Tree View

<details>
<summary><strong>Epic: {Epic Title}</strong> (Priority: {p}, Features: {n}, Stories: {n})</summary>

- **Feature: {Feature Title}** (Priority: {p}, Stories: {n}, Points: {n})
  - User Story: {Story Title} ({n} pts, Priority {p})
  - User Story: {Story Title} ({n} pts, Priority {p})
  - Tech Story: {Story Title} ({n} pts, Priority {p})
- **Feature: {Feature Title}** (Priority: {p}, Stories: {n}, Points: {n})
  - User Story: {Story Title} ({n} pts, Priority {p})

</details>

<details>
<summary><strong>Epic: {Epic Title}</strong> (Priority: {p}, Features: {n}, Stories: {n})</summary>

- **Feature: {Feature Title}** (Priority: {p}, Stories: {n}, Points: {n})
  - User Story: {Story Title} ({n} pts, Priority {p})

</details>
```

---

## Section: Epic Details (Per-Item Detail Cards)

### Epic Card Template

```markdown
## Epic: {Epic Title}

| Field              | Value                          |
|--------------------|--------------------------------|
| Priority           | {1/2/3}                        |
| Value Area         | {Business/Architectural}       |
| Risk               | {1-High/2-Medium/3-Low}        |
| Target Date        | {YYYY-MM-DD or TBD}            |
| Child Features     | {count}                        |
| Total Story Points | {sum of all child stories}     |

### Description
{Epic description text}

### Expected Benefits
{Expected benefits text}

### Success Metrics
{KPIs and measure indicators}

---
```

### Feature Card Template

```markdown
### Feature: {Feature Title}

| Field              | Value                          |
|--------------------|--------------------------------|
| Parent Epic        | {Epic Title}                   |
| Priority           | {1/2/3}                        |
| Effort             | {hours or points}              |
| Business Value     | {1-100}                        |
| Time Criticality   | {1-100}                        |
| Value Area         | {Business/Architectural}       |
| Child Stories      | {count}                        |
| Story Points       | {sum}                          |

### Description
{Feature description text}

### In Scope
- {scope item 1}
- {scope item 2}

### Out of Scope
- {exclusion 1}

---
```

### User Story Card Template

```markdown
#### User Story: {Story Title}

| Field              | Value                          |
|--------------------|--------------------------------|
| Parent Feature     | {Feature Title}                |
| Priority           | {1/2/3}                        |
| Story Points       | {fibonacci number}             |
| Value Area         | {Business/Architectural}       |

**As a** {persona}, **I want to** {action} **so that** {benefit}.

**Acceptance Criteria:**
- [ ] Given {precondition}, When {action}, Then {result}
- [ ] Given {precondition}, When {action}, Then {result}
- [ ] Given {precondition}, When {action}, Then {result}

---
```

### Technical Story Card Template

```markdown
#### Tech Story: {Story Title}

| Field              | Value                          |
|--------------------|--------------------------------|
| Parent Feature     | {Feature Title}                |
| Priority           | {1/2/3}                        |
| Story Points       | {fibonacci number}             |
| Value Area         | Architectural                  |
| Category           | {API/Infra/Security/etc.}      |

**As a** {developer/DevOps/system}, **I want to** {technical action}
**so that** {technical benefit}.

**Acceptance Criteria:**
- [ ] {Technical validation criterion 1}
- [ ] {Technical validation criterion 2}
- [ ] {Technical validation criterion 3}

---
```

---

## Section: Risk Register

### Template

```markdown
## Risk Register

| ID    | Title              | Likelihood | Impact | Assessment | Parent       |
|-------|--------------------|-----------|--------|------------|--------------|
| R-001 | {Risk title}       | {1-5}     | {A-E}  | {1-5}      | {Epic/Feature}|
| R-002 | {Risk title}       | {1-5}     | {A-E}  | {1-5}      | {Epic/Feature}|

### R-001: {Risk Title}

**Business Impact:** {impact description}

**Mitigation Plan:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

---
```

---

## Section: Impediments

### Template

```markdown
## Impediments

| ID      | Title                   | Priority | Resolution Status |
|---------|-------------------------|----------|-------------------|
| IMP-001 | {Impediment title}      | {1/2/3}  | Open              |
| IMP-002 | {Impediment title}      | {1/2/3}  | Open              |

### IMP-001: {Impediment Title}

**Description:** {detailed description}

**Proposed Resolution:** {resolution steps}

**Blocked Items:** {list of affected stories/features}

---
```

---

## Section: Dependency Diagram

### Mermaid Template

```markdown
## Dependency Diagram

```mermaid
graph TD
    E1[Epic: {Title}] --> F1[Feature: {Title}]
    E1 --> F2[Feature: {Title}]
    F1 --> S1[Story: {Title}]
    F1 --> S2[Story: {Title}]
    F2 --> S3[Story: {Title}]

    S1 -->|blocks| S3

    R1[Risk: {Title}] -.->|threatens| F1
    IMP1[Impediment: {Title}] -.->|blocks| S2

    classDef epic fill:#7C3AED,color:#fff
    classDef feature fill:#2563EB,color:#fff
    classDef story fill:#059669,color:#fff
    classDef techStory fill:#D97706,color:#fff
    classDef risk fill:#DC2626,color:#fff
    classDef impediment fill:#E11D48,color:#fff

    class E1 epic
    class F1,F2 feature
    class S1,S3 story
    class S2 techStory
    class R1 risk
    class IMP1 impediment
```
```

### Diagram Rules

1. Include all epics and features as nodes.
2. Include stories only if they have dependency relationships.
3. Use solid arrows for parent-child relationships.
4. Use labeled arrows for `blocks` relationships.
5. Use dashed arrows for risk and impediment associations.
6. Apply the standard color scheme via classDef.
7. Keep the diagram readable: if more than 30 nodes, split into per-epic diagrams.

---

## Section: Cross-Reference Log

### Template

```markdown
## Cross-Reference Log

### Skipped Items (existing duplicates found)

| Planned Item           | Existing Item              | Platform ID | Similarity |
|------------------------|----------------------------|-------------|------------|
| {planned title}        | {existing title}           | {#num/ID}   | {%}        |

### Linked Items (new items related to existing)

| New Item               | Linked To                  | Platform ID | Relation   |
|------------------------|----------------------------|-------------|------------|
| {new title}            | {existing title}           | {#num/ID}   | relatedTo  |

### No Matches (created without cross-references)
- {item title 1}
- {item title 2}
```

---

## File Output

- **File name**: `backlog-{prd-name}-full.md`
- **Encoding**: UTF-8
- **Line endings**: LF (Unix-style)
- **Max line width**: 100 characters (wrap prose, not tables or code blocks)
