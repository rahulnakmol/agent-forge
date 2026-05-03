# Epic Decomposition Methodology

## Purpose

Epic decomposition is the process of breaking a business understanding document into discrete, deliverable epics. Each epic becomes a standalone PRD. The decomposition method varies by input mode.

---

## Decomposition Principles

### 1. Each Epic Must Be Independent and Valuable

An epic is not a technical component or a layer of the stack. It is a user-facing capability that delivers business value on its own. If removing an epic makes the product incomplete but still usable, it is correctly scoped.

**Good epic boundaries:**
- User onboarding and registration
- Payment processing
- Reporting dashboard
- Notification management

**Bad epic boundaries (too technical):**
- Database schema setup
- API gateway configuration
- Authentication middleware
- Logging infrastructure

### 2. Epic Sizing Guidelines

| Size | Story Count | Sprint Estimate | Signal |
|------|------------|----------------|--------|
| Small | 3-5 stories | 1 sprint | Single persona, single workflow |
| Medium | 5-10 stories | 2-3 sprints | Multiple personas or branching flows |
| Large | 10-15 stories | 3-5 sprints | Consider splitting |
| Too Large | 15+ stories | 5+ sprints | Must split before PRD generation |

If an epic exceeds 15 stories during drafting, stop and split it. Each resulting sub-epic gets its own PRD.

### 3. The DIVE Test for Epics

Every epic must pass:

| Criterion | Question |
|-----------|----------|
| **D**eliverable | Can this be released independently? |
| **I**ndependent | Can a team work on this without blocking on other epics? |
| **V**aluable | Does a real persona get measurable value from this? |
| **E**stimable | Can the team estimate the effort to build this? |

---

## Mode A: Decomposition from Discovery (SaaS Pipeline)

### Step 1: Extract Recommended Epics

The understanding document from `pm-discovery` contains a "Recommended Epics" section. Start there.

```
Source: {project}/discovery/understanding-doc.md
Section: "Recommended Epics" or "Epic Recommendations"
```

For each recommended epic, extract:
- Epic name and description
- Primary persona(s) affected
- Business value statement
- Key process flows referenced

### Step 2: Validate Against Personas

Cross-reference each epic against the personas section of the understanding document:

- Does every persona have at least one epic that serves them?
- Does every epic serve at least one persona?
- Are persona journeys (behavior, feelings, pain points) reflected in epic scope?

If a persona has no epic coverage, either expand an existing epic or create a new one.

### Step 3: Validate Against Process Flows

Each process flow diagram from discovery should map to at least one epic. If a process flow spans multiple epics, document the dependency.

### Step 4: Order by Business Value

Rank epics using the initiative classification from the understanding document:
1. **Revenue-generating** epics first (new capabilities that drive growth)
2. **Revenue-protecting** epics second (compliance, security, retention)
3. **Efficiency** epics third (cost reduction, automation)
4. **Foundation** epics last (infrastructure, enablement)

---

## Mode B: Decomposition from TOM (Consulting Pipeline)

### Step 1: Extract Capability Gaps

Read the TOM maturity assessment from `tom-architect`:

```
Source: {project}/tom/ artifacts
Key file: Capability register, maturity assessment
```

For each L1/L2 process with a maturity gap (current < target):
- Gap size = target maturity - current maturity
- Priority = gap size * business impact weight

### Step 2: Group Gaps into Epics

Group related capability gaps into epics using these rules:

1. **Same L1 process**: Gaps within the same L1 value chain group naturally
2. **Same persona-role**: Gaps affecting the same operational role group together
3. **Same system boundary**: Gaps that will be addressed by the same technology group together
4. **Dependency chain**: If gap A must close before gap B, they may belong in the same epic (or ordered epics)

### Step 3: Map TOM Processes to Epic Scope

For each epic, document:
- L1-L4 process IDs covered
- Current maturity level(s)
- Target maturity level(s)
- Gap closure actions (from TOM)
- Persona-role mappings (from TOM organizational design)

### Step 4: Order by Maturity Gap Priority

Rank epics by:
1. Largest maturity gaps with highest business impact
2. Dependencies (foundation capabilities before dependent ones)
3. SOW alignment (if the engagement has contractual milestones)
4. Quick wins (small gaps that demonstrate momentum)

---

## Mode C: Standalone Decomposition

### Step 1: Gather Requirements

Use `AskUserQuestion` to collect:
- Business problem statement
- Target users/personas (at least name and role)
- Key capabilities needed
- Known constraints
- Priority guidance

### Step 2: Identify Natural Epic Boundaries

Without upstream artifacts, look for natural boundaries:
- Different user roles (admin vs end-user epics)
- Different workflow stages (setup, core usage, reporting)
- Different integration points (each external system = potential epic boundary)
- Different value propositions (must-have vs nice-to-have capabilities)

### Step 3: Confirm with User

Present the proposed epic list to the user via `AskUserQuestion` before generating PRDs. Include for each:
- Epic name
- 1-2 sentence description
- Primary persona
- Estimated story count (S/M/L)

---

## Epic Dependency Mapping

After decomposition, map dependencies between epics:

```markdown
## Epic Dependencies

| Epic | Depends On | Dependency Type | Notes |
|------|-----------|----------------|-------|
| Payment Processing | User Onboarding | Hard | Cannot process payments without user accounts |
| Reporting Dashboard | Payment Processing | Soft | Can build with mock data, real data later |
| Admin Console | None | Independent | Can be developed in parallel |
```

Dependency types:
- **Hard**: Cannot start until dependency is complete
- **Soft**: Can develop in parallel with stubs/mocks, integrate later
- **Data**: Needs data produced by dependency, but logic is independent

---

## Splitting Oversized Epics

When an epic exceeds 15 stories, split using these strategies:

### By Workflow Stage
- "Order Management" -> "Order Creation" + "Order Fulfillment" + "Order Returns"

### By Persona
- "User Management" -> "Self-Service Registration" (end-user) + "Admin User Management" (admin)

### By Complexity Tier
- "Search" -> "Basic Search" (keyword, filters) + "Advanced Search" (faceted, ML-ranked)

### By Integration
- "Data Import" -> "CSV Import" + "API Integration" + "Real-Time Sync"

### Split Validation
After splitting, verify each resulting sub-epic still passes the DIVE test. If a sub-epic is not independently valuable, the split boundary is wrong.

---

*pm-prd-generator v1.0 | Epic Decomposition Methodology*
