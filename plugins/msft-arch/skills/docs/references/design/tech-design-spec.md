---
category: design-documentation
loading_priority: 1
tokens_estimate: 3200
keywords:
  - tech-design-first
  - design.md
  - technical specification
  - implementation tasks
  - coding agent
  - feature spec
  - architecture-first
  - feasibility
  - task generation
  - Kiro
dependencies: [hld-template, lld-template, c4-diagram-guide, stack-overview, artifact-overview]
version: "1.0"
last_updated: "2026-03-21"
---

# Tech-Design-First Specification

This reference defines the tech-design-first specification format for the architecture skills suite. The approach is inspired by [Kiro's feature spec workflow](https://kiro.dev/docs/specs/feature-specs/tech-design-first/) and adapted for Microsoft enterprise architectures across all four stacks.

---

## Overview

The tech-design-first workflow inverts traditional software development. Instead of the conventional flow (requirements --> design --> implementation), it follows:

**Technical Design --> Derive Feasible Requirements --> Generate Implementation Tasks**

This inversion provides a critical guarantee: every requirement is technically feasible because it was derived from a validated architecture, not invented in isolation. The output is a single `design.md` file that serves as the authoritative source of truth for coding agents and development teams.

### Why This Matters for Enterprise Microsoft Solutions

Microsoft enterprise solutions span managed SaaS platforms (D365, Power Platform) through to fully custom container workloads (AKS). Each stack imposes hard constraints: API throttling limits, licensing boundaries, data residency rules, and service-level capabilities. Starting with technical design surfaces these constraints before requirements are locked, preventing the costly cycle of discovering infeasibility during implementation.

---

## When to Use Tech-Design-First

Use this approach when:

- **Rapid prototyping with known stacks**: The user already knows they want Stack B (Azure PaaS) or has existing infrastructure preferences. Start with the architecture, not discovery.
- **Strict non-functional requirements (NFRs)**: Systems with hard latency targets (<200ms P99), throughput requirements (>10K TPS), or compliance mandates (FedRAMP, HIPAA, SOC2) need architecture-first validation.
- **Porting existing architectures**: Converting Visio diagrams, whiteboard sketches, or verbal descriptions into structured specs. The architecture already exists; it just needs formalization.
- **Feasibility exploration under constraints**: "Can we build X using only Power Platform?" or "Can this run within our existing AKS cluster?" Design-first answers these questions before investing in requirements.
- **Strong architectural preferences**: The user or their organization has established patterns, preferred services, or existing landing zones. Start from what exists.
- **Coding agent consumption**: When the output will be consumed by Claude Code or other coding agents, the `design.md` format provides structured, unambiguous implementation guidance.

### When NOT to Use Tech-Design-First

Use the traditional requirements-first approach (see `requirements-gathering.md`) when:

- Business requirements are ambiguous and need stakeholder discovery
- Multiple solution approaches are being evaluated (use fit-gap analysis instead)
- The project is in the Vision phase and strategic alignment is the priority
- Regulatory requirements must be documented before any design work begins

---

## The design.md Specification Format

The skill generates a `design.md` file that serves as the single source of truth for implementation. This file lives in the project repository and is the primary artifact coding agents reference.

### Template

```markdown
# [Feature/Solution Name] - Technical Design

## Overview
[1-2 paragraph description of what this component/feature does and why it exists.
Include the business context and the primary user persona.]

## Architecture

### System Components

| Component | Type | Technology | Responsibility | Stack |
|-----------|------|------------|----------------|-------|
| [Name] | Power App / Azure Function / API / Container / D365 Plugin / Flow / etc. | [Specific Microsoft service and SDK version] | [Single responsibility description] | A / B / C / D |

### Component Interaction Diagram

` ``mermaid
sequenceDiagram
    participant U as User
    participant A as Component A
    participant B as Component B
    participant C as Component C
    U->>A: [Action description]
    A->>B: [Method/endpoint + payload shape]
    B->>C: [Method/endpoint + payload shape]
    C-->>B: [Response shape]
    B-->>A: [Response shape]
    A-->>U: [Result description]
` ``

### Data Flow Diagram

` ``mermaid
flowchart LR
    Source["Data Source"] --> Ingest["Ingestion Layer"]
    Ingest --> Transform["Transformation"]
    Transform --> Store["Data Store"]
    Store --> Present["Presentation Layer"]
` ``

## API Contracts

### [Endpoint Name]
- **Method**: GET / POST / PUT / PATCH / DELETE
- **Path**: `/api/v1/[resource]`
- **Authentication**: Bearer token (Entra ID) / API key / Managed Identity
- **Rate Limit**: [requests/minute]

**Request Schema:**
```typescript
interface [RequestName] {
  field1: string;
  field2: number;
  field3?: boolean;
}
```

**Response Schema:**
```typescript
interface [ResponseName] {
  id: string;
  status: "success" | "error";
  data: {
    // response fields
  };
  metadata: {
    timestamp: string;
    requestId: string;
  };
}
```

**Error Response:**
```json
{
  "type": "https://api.contoso.com/errors/[error-type]",
  "title": "[Human-readable title]",
  "status": 400,
  "detail": "[Specific error description]",
  "instance": "/api/v1/[resource]/[id]"
}
```

## Data Models

` ``mermaid
erDiagram
    ENTITY_A ||--o{ ENTITY_B : "has many"
    ENTITY_A {
        string id PK
        string name
        datetime created_at
        string status
    }
    ENTITY_B {
        string id PK
        string entity_a_id FK
        string description
        decimal amount
    }
` ``

### Entity Definitions

| Entity | Field | Type | Required | Constraints | Notes |
|--------|-------|------|----------|-------------|-------|
| [Name] | [field] | [type] | Yes/No | [PK, FK, unique, index] | [Dataverse/SQL/Cosmos annotation] |

## Process Flows

### [Primary Business Process Name]

` ``mermaid
sequenceDiagram
    actor User
    participant App as Application
    participant API as API Layer
    participant DB as Database
    participant Queue as Message Queue

    User->>App: Initiate action
    App->>API: POST /api/v1/resource
    API->>DB: Validate and persist
    DB-->>API: Confirmation
    API->>Queue: Publish event
    API-->>App: 202 Accepted
    App-->>User: Action submitted

    Note over Queue: Async processing
    Queue->>API: Process event
    API->>DB: Update status
` ``

### Error / Exception Flow

[Mermaid sequence diagram showing error detection, retry, compensation]

### Human-in-the-Loop Flow

[Mermaid sequence diagram showing approval routing, escalation, timeout handling]

## Non-Functional Properties

| Property | Target | Approach |
|----------|--------|----------|
| Response Time | P95 < [X]ms, P99 < [Y]ms | [Caching strategy, query optimization, CDN] |
| Throughput | [N] requests/second | [Scaling approach, partitioning] |
| Availability | [X]% SLA | [Redundancy, failover, health checks] |
| Scalability | [N] concurrent users | [Horizontal/vertical, auto-scale rules] |
| Security | [Standard] | [AuthN/AuthZ, encryption at rest/transit, WAF] |
| Compliance | [Regulation] | [Specific controls, audit logging, data residency] |
| DR/BC | RPO: [X]h, RTO: [Y]h | [Backup strategy, geo-replication, runbook] |

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend | | | |
| API Gateway | | | |
| Application | | | |
| Data | | | |
| Messaging | | | |
| Identity | | | |
| Monitoring | | | |

## Implementation Tasks

| Task ID | Description | Component | Dependencies | Acceptance Criteria | Complexity |
|---------|-------------|-----------|--------------|---------------------|------------|
| TASK-001 | | | None | | V.Simple / Simple / Medium / Complex / V.Complex |
| TASK-002 | | | TASK-001 | | |
| TASK-003 | | | TASK-001 | | |
| TASK-004 | | | TASK-002, TASK-003 | | |
```

---

## Detail Levels

The tech-design-first workflow supports two detail levels. Choose based on the project context.

### High-Level Design First (HLD-First)

**Use when**: Team projects, complex multi-component systems, formal review gates, stakeholder presentations.

**Focus areas**:
- System architecture diagrams (C4 Context and Container levels)
- Component descriptions with responsibilities and boundaries
- Technical patterns and integration approaches
- NFR documentation with quantitative targets
- Cross-cutting concerns (security, monitoring, DR)

**Output**: `design.md` emphasizes architecture overview, component boundaries, and interaction patterns. Implementation tasks are coarse-grained (epics/features level).

**Complements**: HLD Document (docx) generated from `hld-template.md`.

### Low-Level Design First (LLD-First)

**Use when**: Rapid validation, solo development, coding agent consumption, implementation sprints.

**Focus areas**:
- Algorithmic pseudocode for complex logic
- Interface definitions with exact type signatures
- Key data structures and their serialization formats
- Mermaid process diagrams at method-call granularity (see `lld-process-diagrams.md`)
- Error handling paths with specific error codes

**Output**: `design.md` emphasizes API contracts, data models, and process flows. Implementation tasks are fine-grained (story/task level) with specific acceptance criteria.

**Complements**: LLD Document (docx) generated from `lld-template.md`.

---

## Workflow Pipeline

The tech-design-first workflow follows six sequential steps with defined inputs, outputs, and review checkpoints.

### Step 1: Create Feature Spec

**Input**: PRD, user story, feature description, existing architecture diagrams, or verbal description.

**Actions**:
- Extract the core problem statement and desired outcome
- Identify explicit and implicit technical constraints
- Determine target stack (A/B/C/D) or confirm from existing context
- List known NFRs (performance, compliance, availability)

**Output**: Structured feature brief with constraints and stack alignment.

### Step 2: Choose Detail Level

**Input**: Feature brief, project context.

**Decision criteria**:

| Factor | HLD-First | LLD-First |
|--------|-----------|-----------|
| Team size | >3 developers | 1-3 developers or coding agents |
| Review gates | Formal architecture review board | Peer review or self-review |
| Integration complexity | Multiple external systems | Self-contained or few integrations |
| Stakeholder visibility | Executive/management reporting needed | Development team only |
| Implementation timeline | Multi-sprint/quarter | Single sprint |

**Output**: Detail level selection (HLD-first or LLD-first).

### Step 3: Design Phase

**Input**: Feature brief, detail level, stack reference (from `stack-selection/`).

**Actions**:
- Generate `design.md` with architecture section (components, interactions, data flow)
- Create Mermaid diagrams for component interaction and data flow
- Define API contracts with request/response schemas
- Define data models with entity relationships
- Document NFR approach for each target property
- Iterate with user until architecture is validated

**Output**: Validated `design.md` (architecture, API contracts, data models, NFRs).

**Review checkpoint**: User confirms architecture before proceeding.

### Step 4: Requirements Phase

**Input**: Validated `design.md`.

**Actions**:
- Derive functional requirements from each component's responsibility
- Derive integration requirements from each component interaction
- Derive data requirements from each entity definition
- Derive NFR requirements from each non-functional property
- Trace every requirement back to a specific design decision

**Output**: Traceable requirements list appended to or accompanying `design.md`.

**Traceability rule**: Every requirement MUST reference at least one component, API contract, or data model from the design. If a requirement cannot be traced, it indicates either a design gap or an invalid requirement.

### Step 5: Tasks Phase

**Input**: Requirements list, validated `design.md`.

**Actions**:
- Generate ordered implementation tasks with dependency chains
- Assign each task to a specific component from the architecture
- Define acceptance criteria referencing API contracts and data models
- Estimate complexity using the V.Simple/Simple/Medium/Complex/V.Complex scale
- Order tasks to maximize parallel work and minimize blocking

**Output**: Implementation Tasks section populated in `design.md`.

**Ordering principle**: Infrastructure and data layer tasks first, then API/service layer, then UI/integration layer. Cross-cutting tasks (auth, monitoring) run in parallel.

### Step 6: Implementation

**Input**: Complete `design.md`.

**Actions**:
- Coding agents or developers execute tasks in dependency order
- Reference `design.md` as the source of truth for all architecture questions
- Consult API Contracts section for exact interface implementations
- Consult Data Models section for schema definitions
- Consult Process Flows section for business logic
- Update `design.md` if implementation reveals necessary design changes

**Output**: Implemented solution aligned to the validated design.

---

## Per-Stack Design Templates

Each stack has typical component patterns. Use these as starting points when populating the System Components table.

### Stack A (Power Platform / Low-Code)

| Component | Type | Technology | Typical Responsibility |
|-----------|------|------------|----------------------|
| User Interface | Canvas App or Model-Driven App | Power Apps | User interaction, data entry, visualization |
| Business Logic | Cloud Flow | Power Automate | Workflow automation, approval routing, notifications |
| Data Store | Dataverse Table | Microsoft Dataverse | Structured data persistence, security, business rules |
| Reporting | Dashboard / Report | Power BI Embedded | Analytics, KPIs, operational reporting |
| Integration | Custom Connector | Power Platform Connectors | External system communication |
| AI | Copilot | Copilot Studio | Natural language interface, guided assistance |

### Stack B (Azure PaaS + Low-Code)

| Component | Type | Technology | Typical Responsibility |
|-----------|------|------------|----------------------|
| Frontend | SPA / Canvas App | React + Azure Static Web Apps / Power Apps | User interface |
| API Gateway | Gateway | Azure API Management | Routing, throttling, authentication |
| Application API | Function App / App Service | Azure Functions (.NET/Node) / Azure App Service | Business logic, orchestration |
| Data Store (Relational) | Database | Azure SQL Database | Transactional data |
| Data Store (NoSQL) | Database | Azure Cosmos DB | Document/event data, global distribution |
| Messaging | Message Broker | Azure Service Bus / Event Grid | Async communication, event-driven processing |
| Identity | Identity Provider | Microsoft Entra ID | Authentication, authorization, RBAC |
| Monitoring | Observability | Azure Monitor + Application Insights | Logging, metrics, alerting, distributed tracing |

### Stack C (Containers / Microservices)

| Component | Type | Technology | Typical Responsibility |
|-----------|------|------------|----------------------|
| Ingress | Ingress Controller | NGINX / Azure Application Gateway | TLS termination, routing, WAF |
| API Service | Container | AKS Pod (.NET/Go/Node) | API endpoint, request validation |
| Domain Service | Container | AKS Pod | Core business logic, domain operations |
| Worker Service | Container | AKS Pod + KEDA | Background processing, event handling |
| Data Store | Database | Azure SQL / Cosmos DB / PostgreSQL Flex | Persistent data |
| Cache | Cache | Azure Cache for Redis | Session state, query cache, rate limiting |
| Message Broker | Message Bus | Azure Service Bus / RabbitMQ | Inter-service communication |
| Service Mesh | Mesh | Istio / Linkerd | mTLS, traffic management, observability |
| Container Registry | Registry | Azure Container Registry | Image storage, scanning, geo-replication |

### Stack D (Dynamics 365 + Platform)

| Component | Type | Technology | Typical Responsibility |
|-----------|------|------------|----------------------|
| CRM/ERP Application | SaaS Module | D365 Sales / Service / Finance / SCM | Core business process |
| Custom Logic | Plugin / Webhook | D365 Plugin (C#) | Server-side business logic, validation |
| Custom UI | PCF Control / App | Power Apps Component Framework | Extended user experience |
| Integration Layer | Middleware | Azure Integration Services / Dual-Write | D365-to-external system synchronization |
| Data Integration | Sync | Dual-Write / Data Export Service / Synapse Link | Real-time or batch data synchronization |
| Reporting | Analytics | Power BI / Synapse Analytics | Operational and analytical reporting |
| Automation | Workflow | Power Automate / D365 Workflows | Process automation, notifications |

---

## Best Practices

1. **Start with constraints, not features.** List required technologies, performance targets, compliance mandates, and budget limits before designing anything.
2. **Iterate on architecture BEFORE deriving requirements.** The design review checkpoint (Step 3) is mandatory. Never skip to requirements with an unvalidated design.
3. **Use HLD-first for team projects, LLD-first for coding agents.** When the consumer of `design.md` is a coding agent, LLD-first with detailed API contracts and process flows produces better implementation outcomes.
4. **Every requirement traces to a design decision.** Untraceable requirements indicate scope creep or design gaps. Address both before proceeding to tasks.
5. **Implementation tasks reference specific components.** Every task in the Implementation Tasks table must name a component from the System Components table. Orphaned tasks indicate architectural blind spots.
6. **Keep `design.md` current.** When implementation reveals a design change, update `design.md` first, then update affected tasks. The file is a living source of truth, not a frozen document.
7. **Use Mermaid for all diagrams.** Refer to `c4-diagram-guide.md` for C4 model templates and `lld-process-diagrams.md` for implementation-level flow diagrams.
8. **Verify with Microsoft Docs.** Before finalizing technology selections, use the context7 MCP to verify current service capabilities, limits, and pricing. See `mcp-integration.md`.

---

*Cross-references: `hld-template.md`, `lld-template.md`, `lld-process-diagrams.md`, `c4-diagram-guide.md`, `stack-overview.md`, `artifact-overview.md`, `mcp-integration.md`, `sub-agent-orchestration.md`*
