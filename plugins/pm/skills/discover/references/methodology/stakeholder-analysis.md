# Stakeholder Analysis Framework

## Purpose

Stakeholder analysis ensures that every person and group affected by or influencing the initiative is identified, categorized, and appropriately engaged. Incomplete stakeholder identification is the single most common cause of initiative failure.

## Stakeholder Identification

### Step 1: Enumerate Stakeholders by Category

| Category | Description | Examples |
|----------|-------------|---------|
| **Decision-makers** | Approve scope, budget, timeline, and go/no-go | CEO, VP Product, Steering Committee |
| **Influencers** | Shape direction without formal authority | Senior engineers, trusted advisors, industry analysts |
| **End Users** | Interact with the system or process daily | Customers, operations staff, field workers |
| **Affected Parties** | Impacted indirectly by the outcome | Downstream teams, partners, compliance officers |
| **Enablers** | Provide resources, access, or capabilities needed | IT infrastructure, data teams, legal, procurement |

### Step 2: Capture Stakeholder Details

For each identified stakeholder, document:

| Field | Description |
|-------|-------------|
| **Name/Role** | Role title (use role, not personal name in discovery artifacts) |
| **Organization** | Team, department, or external entity |
| **Interest** | What they care about regarding this initiative |
| **Influence** | Their ability to affect outcomes (High/Medium/Low) |
| **Impact** | How much the initiative affects them (High/Medium/Low) |
| **Engagement Need** | How they need to be involved (Inform/Consult/Collaborate/Empower) |
| **Communication Preference** | How and how often they want updates |
| **Known Concerns** | Stated objections, risks, or requirements |

## Influence-Interest Matrix

Plot stakeholders on a 2x2 matrix to determine engagement strategy.

```
                    HIGH INTEREST
                         |
    +--------------------|--------------------+
    |                    |                    |
    |   KEEP SATISFIED   |   MANAGE CLOSELY   |
    |                    |                    |
    |  (High influence,  | (High influence,   |
    |   low interest)    |  high interest)    |
    |                    |                    |
HIGH|--------------------+--------------------| HIGH
INFL|                    |                    | INFL
    |                    |                    |
    |   MONITOR          |   KEEP INFORMED    |
    |                    |                    |
    |  (Low influence,   | (Low influence,    |
    |   low interest)    |  high interest)    |
    |                    |                    |
    +--------------------|--------------------+
                         |
                    LOW INTEREST
```

### Engagement Strategies

| Quadrant | Strategy | Actions |
|----------|----------|---------|
| **Manage Closely** | Active partnership | Regular 1:1s, co-design sessions, approval gates |
| **Keep Satisfied** | Proactive updates | Executive summaries, milestone reviews, escalation path |
| **Keep Informed** | Regular communication | Status updates, demos, feedback channels |
| **Monitor** | Minimal engagement | Newsletter, all-hands updates, available on request |

## RACI Matrix for PM Context

Assign each stakeholder a RACI role per major deliverable or decision.

| Role | Definition | Rule |
|------|-----------|------|
| **R** -- Responsible | Does the work | Can be multiple people |
| **A** -- Accountable | Owns the outcome, makes final decision | Exactly one person per item |
| **C** -- Consulted | Provides input before decision | Two-way communication |
| **I** -- Informed | Notified after decision | One-way communication |

### RACI Template

| Deliverable / Decision | Sponsor | PM | Tech Lead | Business Owner | End Users |
|------------------------|---------|-----|-----------|----------------|-----------|
| Problem Statement | A | R | C | C | I |
| Stakeholder Map | I | R/A | C | C | I |
| Process Flows | I | R | C | A | C |
| Initiative Classification | A | R | C | C | I |
| Business Understanding Doc | A | R | C | C | I |
| Handoff to Next Skill | I | R/A | C | I | I |

## Identifying Decision-Makers

### Signals of Real Decision Authority
- Controls budget allocation for this initiative
- Can say "no" and it sticks (veto power)
- Signs off on scope changes
- Is referenced by others as "the person who decides"

### Common Pitfalls
- **Assuming the loudest voice decides**: Vocal participants may be influencers, not decision-makers
- **Missing the shadow org chart**: Informal influence networks often override formal hierarchy
- **Ignoring downstream veto power**: IT security, legal, and compliance can block any initiative
- **Conflating buyer and user**: In B2B, the person who buys is rarely the person who uses

## Stakeholder Analysis by Entry Mode

### Mode A: SaaS Product Context

Focus on:
- **Buyer personas**: Who makes the purchasing decision? What do they value (ROI, ease of adoption, integrations)?
- **User personas**: Who uses the product daily? What is their technical proficiency? What are their workflows?
- **Internal product team**: Product owner, engineering lead, design lead, data/analytics
- **Customer-facing teams**: Sales, customer success, support -- they carry the voice of the customer

### Mode B: Consulting Delivery Context

Focus on:
- **Client steering committee**: Executive sponsors, program director, workstream leads
- **Business process owners**: People who own the processes being transformed
- **IT leadership**: CIO/CTO, enterprise architects, integration team leads
- **Change management**: Communications, training, organizational development
- **External parties**: Consulting partners, system integrators, outsourcing vendors
- **Unions/works councils**: In regulated environments, employee representatives must be consulted

## Stakeholder Register Template

```markdown
## Stakeholder Register

| # | Role | Organization | Influence | Interest | Quadrant | RACI | Engagement |
|---|------|-------------|-----------|----------|----------|------|------------|
| 1 | VP Product | Product | High | High | Manage Closely | A | Weekly 1:1 |
| 2 | Engineering Lead | Engineering | High | Medium | Keep Satisfied | C | Bi-weekly sync |
| 3 | Customer Success Mgr | CS | Low | High | Keep Informed | C | Monthly review |
| 4 | End User (Persona 1) | External | Low | High | Keep Informed | I | User research |
```
