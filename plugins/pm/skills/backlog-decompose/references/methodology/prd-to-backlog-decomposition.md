# PRD to Backlog Decomposition Methodology

## Overview

This document describes the step-by-step process for decomposing a Product
Requirements Document (PRD) into a structured product backlog. The decomposition
follows a systematic extraction process, mapping PRD sections to specific backlog
item types.

---

## PRD Section to Backlog Item Mapping

| PRD Section                      | Backlog Item Type(s)              |
|----------------------------------|-----------------------------------|
| Section 3: Epic Definition       | Epic                              |
| Section 5: Key Features          | Feature                           |
| Section 4: User Stories           | User Story                        |
| Section 6: Non-Functional Reqs   | Technical User Story              |
| Section 7.3: Risks               | Risk                              |
| Section 3.3: Dependencies        | Impediment                        |
| Section 7: Assumptions           | Continuous Improvement Item       |
| Architectural decisions          | Technical User Story              |
| Process gaps (inferred)          | Continuous Improvement Item       |

---

## Step 1: Epic Extraction (PRD Section 3)

### Process

1. Read PRD Section 3 (Epic Definition or Product Vision / Scope).
2. Identify each major initiative, strategic theme, or capability area.
3. For each identified epic, extract:
   - **Title**: A concise name for the initiative (5-10 words).
   - **Description**: The scope and purpose of the epic, drawn from the PRD text.
   - **Expected Benefits**: Business outcomes the epic will deliver.
   - **Measure Indicators**: KPIs or metrics that indicate success.
4. If the PRD does not have an explicit "Epic Definition" section, derive epics
   from the major functional areas or themes described in the product vision.

### Epic Identification Rules

- Each epic should represent 2-6 months of work (at team level).
- An epic should contain at least 2 features.
- If a single "epic" has more than 8 features, consider splitting it.
- Epics should be independent enough to be prioritized separately.

### Epic Fields to Populate

| Field              | Source                                              |
|--------------------|-----------------------------------------------------|
| Title              | Section 3 heading or initiative name                |
| Description        | Section 3 body text, summarized                     |
| Expected Benefits  | Section 3 "Benefits" or "Value Proposition"         |
| Measure Indicators | Section 3 "Success Metrics" or "KPIs"               |
| Priority           | Derived from MoSCoW in PRD or stakeholder input     |
| Value Area         | "Business" unless purely architectural              |

---

## Step 2: Feature Extraction (PRD Section 5)

### Process

1. Read PRD Section 5 (Key Features or Feature Specifications).
2. For each feature listed, extract:
   - **Title**: Feature name as stated in the PRD.
   - **Description**: What the feature does and who it serves.
   - **Business Drivers**: Why this feature is needed (from business context).
   - **In Scope / Out of Scope**: Boundaries from the PRD.
3. Map each feature to its parent epic based on functional area alignment.

### Feature Identification Rules

- Each feature should be deliverable within a single Program Increment (PI) or
  quarter.
- A feature should decompose into 3-10 user stories.
- If a feature has more than 10 stories, consider splitting it into sub-features.
- Features should be testable and demonstrable independently.

### Feature-to-Epic Assignment

Use these heuristics to assign features to epics:
1. **Explicit mapping**: The PRD may state which epic each feature belongs to.
2. **Functional area**: Group features by the functional domain they serve
   (e.g., "Authentication" features map to the "User Identity" epic).
3. **User persona**: Group features by the primary persona they serve.
4. **Ask the user**: If mapping is ambiguous, present options and ask.

### Feature Fields to Populate

| Field              | Source                                              |
|--------------------|-----------------------------------------------------|
| Title              | Section 5 feature name                              |
| Description        | Section 5 feature description                       |
| Business Drivers   | Section 5 or Section 2 (business context)           |
| In Scope           | Section 5 scope boundaries                          |
| Out of Scope       | Section 5 exclusions                                |
| Priority           | MoSCoW from PRD (mapped to 1/2/3)                   |
| Effort             | Estimate based on complexity (if PRD provides T-shirt sizes) |
| Business Value     | Derived from priority and business impact            |
| Time Criticality   | Derived from deadlines and dependencies              |
| Parent             | Assigned epic title                                  |

---

## Step 3: User Story Extraction (PRD Section 4)

### Process

1. Read PRD Section 4 (User Stories or User Requirements).
2. For each user story, extract:
   - **Title**: "As a [persona], I want to [action] so that [benefit]"
   - **Description**: Additional context beyond the title.
   - **Acceptance Criteria**: Testable conditions in Given/When/Then format.
3. Map each story to its parent feature.

### User Story Quality Checks

Apply the INVEST criteria to each extracted story:

- **I**ndependent: Can be developed and delivered independently.
- **N**egotiable: Details can be refined during sprint planning.
- **V**aluable: Delivers clear value to the user or business.
- **E**stimable: The team can estimate the effort required.
- **S**mall: Can be completed within a single sprint.
- **T**estable: Has clear acceptance criteria.

### Story Splitting Rules

If a story is too large (estimated > 13 story points), split it:

1. **By workflow step**: Break the user journey into individual steps.
2. **By data variation**: Handle different data types or input formats separately.
3. **By business rule**: Extract complex business rules into separate stories.
4. **By interface**: Separate API, UI, and backend work.
5. **By operation**: Split CRUD operations (Create, Read, Update, Delete).

### Acceptance Criteria Extraction

1. Look for explicit acceptance criteria in the PRD.
2. If not explicit, derive from:
   - Functional requirements listed under the feature.
   - Business rules and constraints.
   - Edge cases mentioned in the PRD.
3. Write in Given/When/Then format:
   ```
   Given [precondition/context],
   When [action/trigger],
   Then [expected outcome/result].
   ```
4. Each story should have 3-7 acceptance criteria.

### Story Point Estimation

| Complexity        | Story Points | Description                              |
|-------------------|-------------|------------------------------------------|
| Trivial           | 1           | Simple config change, copy update        |
| Simple            | 2           | Single component, clear requirements     |
| Straightforward   | 3           | Known pattern, moderate complexity       |
| Moderate          | 5           | Multiple components, some unknowns      |
| Complex           | 8           | Significant unknowns, cross-cutting     |
| Very Complex      | 13          | Major unknowns, new technology          |
| Epic-sized        | 21          | Should probably be split further         |

---

## Step 4: Technical Story Generation

Technical stories are NOT directly in the PRD. They are inferred from:
- Non-functional requirements (PRD Section 6)
- Architectural decisions
- Infrastructure needs implied by features
- Integration requirements

See methodology/technical-story-generation.md for the complete generation process.

---

## Step 5: Risk Extraction (PRD Section 7.3)

### Process

1. Read PRD Section 7.3 (Risk Assessment or Risk Register).
2. For each identified risk, extract:
   - **Title**: Concise risk statement.
   - **Description**: Detailed explanation of the risk.
   - **Business Impact**: Consequences if the risk materializes.
   - **Likelihood**: Map to the 1-5 scale.
   - **Impact**: Map to the A-E scale.
3. Calculate Risk Assessment from the Likelihood x Impact matrix.
4. Write a Mitigation Plan for each risk.

### Risk Identification Beyond the PRD

In addition to explicit PRD risks, look for implied risks:

- **Technology risks**: New or unproven technologies mentioned in the PRD.
- **Integration risks**: Third-party dependencies or API integrations.
- **Data risks**: Data migration, data quality, or data volume concerns.
- **Compliance risks**: Regulatory requirements mentioned or implied.
- **Resource risks**: Skills gaps or team capacity constraints.
- **Timeline risks**: Aggressive deadlines or external date dependencies.

### Risk-to-Parent Assignment

- Assign risks to the most specific parent possible:
  - If the risk affects a specific feature, make it a child of that feature.
  - If the risk affects an entire epic, make it a child of that epic.
  - If the risk is project-wide, leave it as a standalone item.

---

## Step 6: Impediment Identification (PRD Section 3.3)

### Process

1. Read PRD Section 3.3 (Dependencies) and Section 7 (Constraints).
2. Identify blocking dependencies:
   - External team dependencies (waiting for API, design, legal review).
   - Third-party vendor dependencies (contracts, SLAs, access provisioning).
   - Infrastructure dependencies (environments, licenses, tools).
3. For each dependency that could block work, create an Impediment.

### Impediment Fields

| Field        | Source                                              |
|-------------|-----------------------------------------------------|
| Title        | Concise description of the blocker                  |
| Description  | What is blocked and why                             |
| Resolution   | Proposed steps to resolve (if known)                |
| Priority     | Based on how many stories it blocks                  |

---

## Step 7: Continuous Improvement Item Generation

### Process

CI items are generated from:
1. **Process gaps**: Assumptions in the PRD that indicate missing processes.
2. **Ambiguities**: Areas where the PRD is unclear and would benefit from
   better requirements gathering.
3. **Technical debt signals**: Workarounds mentioned in the PRD.
4. **Missing capabilities**: Tools or processes needed but not yet in place.

### Examples

- "Establish automated regression test suite for [feature area]"
- "Create runbook for [operational process]"
- "Define SLA monitoring for [third-party integration]"
- "Improve requirements gathering template to capture [missing info]"

---

## Step 8: Hierarchy Building

### Assembly Rules

1. Group all User Stories and Technical Stories under their parent Features.
2. Group all Features under their parent Epics.
3. Attach Risks to their parent Epics or Features.
4. Leave Impediments and CI Items as standalone.
5. Verify every Feature has at least one child story.
6. Verify every Epic has at least one child feature.

### Validation Checks

- [ ] Every story has acceptance criteria
- [ ] Every story has a story point estimate
- [ ] Every feature has a parent epic
- [ ] Every story has a parent feature
- [ ] No orphaned items (except Impediments and CI Items)
- [ ] Story point totals per feature are reasonable (10-50 points)
- [ ] Total backlog size is appropriate for timeline (10-15 points per sprint per dev)
- [ ] Priority distribution follows MoSCoW: ~60% MH, ~20% SH, ~20% CH
