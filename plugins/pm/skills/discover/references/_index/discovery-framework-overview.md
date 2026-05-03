# Discovery Framework Overview

## Purpose

The PM Discovery framework provides a structured approach to understanding business problems before solution design begins. It ensures that Product and Program Managers capture the full context of a problem space, identify all affected stakeholders, and produce actionable documentation that feeds downstream skills (PRD generation, TOM architecture).

## Five Discovery Dimensions

Every discovery engagement explores five dimensions. Not all dimensions carry equal weight in every engagement -- the entry mode and problem type determine emphasis.

### 1. Business Context

Understand the environment in which the problem exists.

- **Industry and market position**: What industry vertical? B2B, B2C, or B2B2C? Market maturity?
- **Business model**: How does the organization generate revenue? Subscription, transactional, consulting?
- **Strategic objectives**: What are the top 3 organizational goals this initiative supports?
- **Competitive landscape**: What alternatives exist? Where does the organization differentiate?
- **Regulatory environment**: Are there compliance requirements that constrain the solution?

### 2. Stakeholder Landscape

Identify every person and group affected by or influencing the outcome.

- **Decision-makers**: Who approves scope, budget, and timeline?
- **Influencers**: Who shapes direction without formal authority?
- **End users**: Who interacts with the system or process daily?
- **Affected parties**: Who is impacted indirectly (downstream teams, customers, partners)?
- **Organizational structure**: Reporting lines, spans of control, cross-functional dependencies

### 3. Problem Definition

Articulate what is broken, missing, or suboptimal.

- **Problem statement**: One sentence capturing the core issue
- **Impact quantification**: Revenue loss, time waste, error rates, customer churn
- **Root cause vs symptom**: Use 5 Whys or Ishikawa to distinguish
- **Scope boundaries**: What is explicitly in scope and out of scope?
- **Prior attempts**: What has been tried before? Why did it fail?

### 4. Constraints & Dependencies

Map everything that limits the solution space.

- **Budget**: Fixed, flexible, or TBD?
- **Timeline**: Hard deadlines (regulatory, contractual) vs aspirational targets
- **Technical constraints**: Existing systems, integration requirements, platform mandates
- **Organizational constraints**: Change capacity, team availability, skill gaps
- **Dependencies**: Other initiatives, third-party vendors, data availability

### 5. Success Criteria

Define what "done" looks like before starting.

- **Measurable outcomes**: KPIs with baselines and targets
- **Qualitative goals**: User satisfaction, process simplification, team morale
- **Acceptance criteria**: What must be true for stakeholders to accept the deliverable?
- **Timeline milestones**: When should intermediate progress be visible?
- **Risk thresholds**: What level of risk is acceptable?

## Two Entry Modes

The discovery framework supports two distinct entry modes that shape how the five dimensions are explored.

### Mode A: SaaS Product Manager

**Context**: Building or enhancing a software product for external users.

| Aspect | Approach |
|--------|----------|
| **Primary focus** | User personas, behaviors, feelings, journeys |
| **Problem framing** | What users want to accomplish and what blocks them |
| **Stakeholder emphasis** | End users, buyer personas, internal product team |
| **Process mapping** | User flows, interaction patterns, feature usage paths |
| **Output** | Business Understanding Document -> hands off to `/pm-prd-generator` |
| **TOM required?** | No |

### Mode B: Consulting Program Manager

**Context**: Decomposing a transformation design for a client organization.

| Aspect | Approach |
|--------|----------|
| **Primary focus** | Business processes, organizational actors, operational flows |
| **Problem framing** | Process inefficiencies, capability gaps, transformation goals |
| **Stakeholder emphasis** | Client executives, business process owners, IT leadership, change management |
| **Process mapping** | BPMN process flows, swimlane diagrams, state machines |
| **Output** | Business Understanding Document -> hands off to `/tom-architect` |
| **TOM required?** | Yes (mandatory next step) |

## Progressive Disclosure Model

Discovery information is gathered and revealed progressively to avoid overwhelming stakeholders and to respect context budget limits.

**Layer 1 -- Surface**: Business problem statement, entry mode, initiative type (captured in Phase 1-2)
**Layer 2 -- Structure**: Stakeholder map, process inventory, constraint register (captured in Phase 3-4)
**Layer 3 -- Detail**: Full persona profiles, detailed process flows, dependency graph (captured in Phase 5-6)
**Layer 4 -- Deliverable**: Complete Business Understanding Document with embedded diagrams (produced in Phase 7)

Each layer builds on the previous. The skill never loads Layer 3 references without first completing Layer 1-2 analysis.

## Relationship to Downstream Skills

| Discovery Output | Downstream Skill | What Gets Handed Off |
|-----------------|-----------------|---------------------|
| Business Understanding Document (Mode A) | `/pm-prd-generator` | Personas, pain points, user journeys, success criteria, recommended epics |
| Business Understanding Document (Mode B) | `/tom-architect` | Process inventory, actor personas, as-is flows, initiative classification, organizational context |
| Process Flow Diagrams | Both | Mermaid diagrams embedded in the Business Understanding Document |
