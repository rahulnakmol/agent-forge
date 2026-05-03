# Azure DevOps SAFe Agile Backlog Reference

## SAFe Hierarchy in Azure DevOps

The SAFe (Scaled Agile Framework) process template in Azure DevOps organizes work
into the following hierarchy:

```
Portfolio Level:  Epic
Program Level:    Feature
Team Level:       User Story / Technical User Story
Supplementary:    Risk, Impediment, Continuous Improvement Item
```

### Parent-Child Relationships

- Epic has children: Feature, Risk
- Feature has children: User Story, Technical User Story, Risk
- User Story and Technical User Story are leaf-level work items (no children)
- Risk can be a child of Epic OR Feature
- Impediment and Continuous Improvement Item are standalone (no parent required)

---

## Work Item Type 1: Epic

### Purpose
Represents a large body of work that can be broken down into multiple features.
Maps to a strategic initiative or a major product capability.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Epic"                                     |
| Title               | String        | Yes      | Concise name of the epic (max 255 chars)   |
| State               | String        | Yes      | "New"                                      |
| Description         | HTML          | Yes      | Rich text describing the epic scope        |
| Expected Benefits   | HTML          | No       | Business outcomes and measurable benefits   |
| Measure Indicators  | HTML          | No       | KPIs and metrics to track success          |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Priority            | Integer       | Yes      | 1 (highest), 2, 3 (lowest)                |
| Risk                | Integer       | No       | 1 = High, 2 = Medium, 3 = Low             |
| Value Area          | String        | No       | "Business" or "Architectural"              |
| Start Date          | DateTime      | No       | YYYY-MM-DD format                          |
| Target Date         | DateTime      | No       | YYYY-MM-DD format                          |
| Tags                | String        | No       | Semicolon-separated list                   |

### Description Template
```html
<h3>Overview</h3>
<p>[High-level description of the epic and its business context]</p>
<h3>Business Justification</h3>
<p>[Why this epic matters to the organization]</p>
<h3>Scope</h3>
<p>[What is included and excluded from this epic]</p>
```

---

## Work Item Type 2: Feature

### Purpose
Represents a service or capability that delivers value to the user. Features are
children of Epics and parents of User Stories.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Feature"                                  |
| Title               | String        | Yes      | Concise feature name (max 255 chars)       |
| State               | String        | Yes      | "New"                                      |
| Description         | HTML          | Yes      | Rich text describing the feature           |
| Business Drivers    | HTML          | No       | Business reasons driving this feature      |
| Critical Value      | HTML          | No       | Value delivered if feature ships on time    |
| In Scope            | HTML          | No       | What is included in this feature           |
| Out of Scope        | HTML          | No       | What is explicitly excluded                |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Priority            | Integer       | Yes      | 1 (highest), 2, 3 (lowest)                |
| Risk                | Integer       | No       | 1 = High, 2 = Medium, 3 = Low             |
| Effort              | Double        | No       | Numeric effort estimate (hours or points)  |
| Business Value      | Integer       | No       | 1-100 scale (relative business value)      |
| Time Criticality    | Integer       | No       | 1-100 scale (urgency)                      |
| Value Area          | String        | No       | "Business" or "Architectural"              |
| Start Date          | DateTime      | No       | YYYY-MM-DD format                          |
| Target Date         | DateTime      | No       | YYYY-MM-DD format                          |
| Parent              | String        | Yes      | Title of parent Epic                       |
| Tags                | String        | No       | Semicolon-separated list                   |

### Description Template
```html
<h3>Feature Description</h3>
<p>[What this feature does and who it serves]</p>
<h3>Business Drivers</h3>
<p>[Business reasons and market context]</p>
<h3>In Scope</h3>
<ul><li>[Capability 1]</li><li>[Capability 2]</li></ul>
<h3>Out of Scope</h3>
<ul><li>[Exclusion 1]</li></ul>
```

---

## Work Item Type 3: User Story

### Purpose
Represents a requirement from the user's perspective. User stories are children of
Features and describe functionality that delivers direct user value.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "User Story"                               |
| Title               | String        | Yes      | "As a [persona], I want to [action]"       |
| State               | String        | Yes      | "New"                                      |
| Description         | HTML          | Yes      | Full user story with context               |
| Issues and Assumptions | HTML       | No       | Known issues, assumptions, constraints     |
| Acceptance Criteria | HTML          | Yes      | Testable conditions for story completion   |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Story Points        | Double        | Yes      | Fibonacci: 1, 2, 3, 5, 8, 13, 21          |
| Priority            | Integer       | Yes      | 1 (highest), 2, 3 (lowest)                |
| Risk                | Integer       | No       | 1 = High, 2 = Medium, 3 = Low             |
| Release Number      | String        | No       | Target release identifier                  |
| Completion Date     | DateTime      | No       | Expected completion date                   |
| Value Area          | String        | No       | "Business" or "Architectural"              |
| Parent              | String        | Yes      | Title of parent Feature                    |
| Tags                | String        | No       | Semicolon-separated list                   |

### Title Format
Always use the canonical user story format:
```
As a [persona], I want to [action] so that [benefit]
```

### Description Template
```html
<h3>User Story</h3>
<p>As a <strong>[persona]</strong>, I <strong>[want to]</strong> so that
<strong>[benefit/reason]</strong>.</p>
<h3>Context</h3>
<p>[Additional context about why this story matters]</p>
<h3>Issues and Assumptions</h3>
<ul><li>[Assumption 1]</li></ul>
```

### Acceptance Criteria Template
```html
<h3>Acceptance Criteria</h3>
<ul>
<li><strong>Given</strong> [precondition], <strong>When</strong> [action],
<strong>Then</strong> [expected result]</li>
<li><strong>Given</strong> [precondition], <strong>When</strong> [action],
<strong>Then</strong> [expected result]</li>
</ul>
```

---

## Work Item Type 4: Technical User Story

### Purpose
Represents a technical requirement that does not deliver direct user-facing value
but is necessary for the system to function. Examples: infrastructure setup, API
contract definition, data migration, security hardening, monitoring setup.

### Fields

Identical to User Story with the following differences:

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Technical User Story"                     |
| Title               | String        | Yes      | Technical action description               |
| State               | String        | Yes      | "New"                                      |
| State Reason        | String        | Auto     | "Moved to state New"                       |
| Description         | HTML          | Yes      | Technical details and justification        |
| Acceptance Criteria | HTML          | Yes      | Technical validation criteria              |
| Story Points        | Double        | Yes      | Fibonacci: 1, 2, 3, 5, 8, 13, 21          |
| Priority            | Integer       | Yes      | 1 (highest), 2, 3 (lowest)                |
| Risk                | Integer       | No       | 1 = High, 2 = Medium, 3 = Low             |
| Value Area          | String        | Yes      | "Architectural" (default for tech stories) |
| Parent              | String        | Yes      | Title of parent Feature                    |

### Title Format for Technical Stories
```
As a [developer/DevOps engineer/system], I want to [technical action]
so that [technical benefit]
```

### Common Categories
- Infrastructure provisioning and configuration
- API contract definition and stub creation
- Database schema migration scripts
- Security hardening and authentication setup
- Monitoring, alerting, and observability pipelines
- CI/CD pipeline configuration
- Performance testing and load testing setup
- Third-party integration configuration

---

## Work Item Type 5: Risk

### Purpose
Represents a potential threat to project delivery. Risks can be children of Epics
or Features.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Risk"                                     |
| Title               | String        | Yes      | Concise risk statement                     |
| State               | String        | Yes      | "New"                                      |
| Description         | HTML          | Yes      | Detailed risk description                  |
| Business Impact     | HTML          | Yes      | Impact on business if risk materializes    |
| Likelihood          | Integer       | Yes      | 1 = Very Likely                            |
|                     |               |          | 2 = Likely                                 |
|                     |               |          | 3 = Possible                               |
|                     |               |          | 4 = Unlikely                               |
|                     |               |          | 5 = Very Unlikely                          |
| Impact              | String        | Yes      | A = Severe                                 |
|                     |               |          | B = Significant                            |
|                     |               |          | C = Moderate                               |
|                     |               |          | D = Minor                                  |
|                     |               |          | E = Negligible                             |
| Risk Assessment     | Integer       | Yes      | 1 = High                                   |
|                     |               |          | 2 = Medium High                            |
|                     |               |          | 3 = Medium                                 |
|                     |               |          | 4 = Medium Low                             |
|                     |               |          | 5 = Low                                    |
| Mitigation Plan     | HTML          | Yes      | Steps to mitigate or avoid the risk        |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Priority            | Integer       | No       | 1 (highest), 2, 3 (lowest)                |
| Parent              | String        | No       | Title of parent Epic or Feature            |
| Tags                | String        | No       | Semicolon-separated list                   |

### Risk Assessment Matrix

| Likelihood \ Impact | A (Severe) | B (Significant) | C (Moderate) | D (Minor) | E (Negligible) |
|---------------------|-----------|-----------------|-------------|----------|----------------|
| 1 (Very Likely)     | 1-High    | 1-High          | 2-Med High  | 3-Medium | 4-Med Low      |
| 2 (Likely)          | 1-High    | 2-Med High      | 3-Medium    | 4-Med Low| 5-Low          |
| 3 (Possible)        | 2-Med High| 3-Medium        | 3-Medium    | 4-Med Low| 5-Low          |
| 4 (Unlikely)        | 3-Medium  | 3-Medium        | 4-Med Low   | 5-Low   | 5-Low          |
| 5 (Very Unlikely)   | 3-Medium  | 4-Med Low       | 5-Low       | 5-Low   | 5-Low          |

---

## Work Item Type 6: Impediment

### Purpose
Represents a blocking issue or obstacle that prevents progress. Impediments are
standalone items not tied to the parent-child hierarchy.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Impediment"                               |
| Title               | String        | Yes      | Concise impediment description             |
| State               | String        | Yes      | "New"                                      |
| Reason              | String        | Yes      | "Moved to state New"                       |
| Description (What is being blocked) | HTML | Yes | What work or progress is being blocked     |
| Cause (what is causing the blocker) | HTML | Yes | Root cause of the impediment               |
| Business Impact (Loss of value/Cost of delay) | HTML | No | Quantified cost or value loss from delay |
| Possible Solutions  | HTML          | No       | Potential approaches to resolve             |
| Resolution (What has been done to mitigate) | HTML | No | Actions taken or planned to mitigate    |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Priority            | Integer       | Yes      | 1 (highest), 2, 3 (lowest)                |
| Tags                | String        | No       | Semicolon-separated list                   |

---

## Work Item Type 7: Continuous Improvement Item

### Purpose
Represents a process improvement opportunity identified during backlog creation.
These capture lessons learned, process gaps, or optimization ideas.

### Fields

| Field               | Type          | Required | Allowed Values / Format                    |
|---------------------|---------------|----------|--------------------------------------------|
| Work Item Type      | String        | Yes      | "Continuous Improvement Item"              |
| Title               | String        | Yes      | Improvement opportunity description        |
| State               | String        | Yes      | "New"                                      |
| Description         | HTML          | Yes      | What needs to improve and why              |
| Expected Benefit    | HTML          | No       | Measurable benefit of the improvement      |
| Area                | TreePath      | Yes      | Project\Team area path                     |
| Iteration           | TreePath      | Yes      | Project\Release\Sprint path                |
| Priority            | Integer       | No       | 1 (highest), 2, 3 (lowest)                |
| Tags                | String        | No       | Semicolon-separated list                   |

---

## Area Path Conventions

Area paths organize work by team or functional area:

```
ProjectName                          (root)
ProjectName\Frontend                 (frontend team)
ProjectName\Backend                  (backend team)
ProjectName\Platform                 (platform/infra team)
ProjectName\QA                       (quality assurance)
```

The backlog generator uses the project root area path by default. The user can
specify a team-level area path during Phase 2 configuration.

---

## Iteration Path Conventions

Iteration paths organize work by time:

```
ProjectName                          (root)
ProjectName\Release 1                (release level)
ProjectName\Release 1\Sprint 1       (sprint level)
ProjectName\Release 1\Sprint 2
ProjectName\Release 2
ProjectName\Release 2\Sprint 3
```

New backlog items are assigned to the release-level iteration by default. Sprint
assignment happens during sprint planning, not during backlog generation.

---

## Hierarchy Validation Rules

1. Every Feature MUST have exactly one parent Epic.
2. Every User Story MUST have exactly one parent Feature.
3. Every Technical User Story MUST have exactly one parent Feature.
4. Risks MAY have a parent Epic or Feature, or be standalone.
5. Impediments are always standalone (no parent).
6. Continuous Improvement Items are always standalone (no parent).
7. No circular parent-child relationships.
8. Parent items must be created/imported before their children.
