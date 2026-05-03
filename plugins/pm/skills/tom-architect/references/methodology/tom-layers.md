---
category: methodology
loading_priority: 1
tokens_estimate: 4200
keywords:
  - TOM layers
  - processes
  - organization
  - service delivery
  - technology
  - data analytics
  - governance
  - process taxonomies
  - maturity models
  - process flows
  - leading practices
  - global process owners
  - role mapping
  - job profiles
  - service delivery model
  - service management
  - AI augmentation
  - technology overlay
  - application architecture
  - environment architecture
  - KPIs
  - benchmarks
  - reporting dashboards
  - MDM
  - master data management
  - security controls
  - policies
version: "1.0"
last_updated: "2026-03-23"
---

# TOM Layers — Detailed Definition

The Target Operating Model is structured into **6 layers** containing **18 sections** total. Each layer addresses a distinct operational dimension, and together they form a complete blueprint for how an organization operates.

---

## Layer 1: Processes (Sections 1.x)

**Purpose**: Define what work the organization performs and how it is executed — from high-level value chains down to individual tasks.

### Section 1.1 — Process Taxonomies

The hierarchical decomposition of all business processes from L1 (value chain) through L4 (activity/task).

**Key deliverables**:
- L1 end-to-end process catalog (e.g., Record to Report, Order to Cash)
- L2 major process area breakdown
- L3 process definitions with inputs, outputs, and ownership
- L4 activity/task detail with automation flags

**Typical questions answered**: What are our core business processes? How do they decompose? Where are the boundaries between process areas?

### Section 1.2 — Maturity Models

Assessment of current and target process maturity across a 5-level scale, with gap analysis.

**Key deliverables**:
- Current-state maturity scores per L2 process
- Target-state maturity scores per L2 process
- Gap analysis with prioritized improvement actions
- Maturity heatmap visualization

**Typical questions answered**: How mature are our processes today? Where should we invest in improvement? What does "good" look like for our industry?

### Section 1.3 — Role-Based Process Flows

Detailed process flow diagrams showing who does what, in what sequence, using what systems.

**Key deliverables**:
- Swimlane process flows at L3 level
- Role-to-activity mapping
- System touchpoints per activity
- Decision points and exception paths

**Typical questions answered**: Who performs each step? What systems are used? Where are the handoffs and bottlenecks?

### Section 1.4 — Leading Practices

Industry-standard best practices and optimization opportunities for each process area.

**Key deliverables**:
- Leading practice catalog per L2 process
- Current vs leading practice gap assessment
- Automation opportunity register
- Quick win identification

**Typical questions answered**: What do best-in-class organizations do differently? Where can we adopt leading practices? What are the quick wins?

**Interdependencies**: Layer 1 is the foundation — it drives organizational design (Layer 2), service delivery scope (Layer 3), technology requirements (Layer 4), KPI definitions (Layer 5), and control frameworks (Layer 6).

---

## Layer 2: Organization (Sections 2.x)

**Purpose**: Define the people dimension — who performs the work, how they are structured, and what roles they fill.

### Section 2.1 — Global Process Owners (GPOs)

Identification and mandate definition for senior leaders accountable for end-to-end processes.

**Key deliverables**:
- GPO role definitions and mandates
- GPO-to-L1 process mapping
- Accountability matrix (GPO vs functional leaders)
- GPO governance cadence and decision rights

**Typical questions answered**: Who owns each end-to-end process? What authority do GPOs have? How do GPOs interact with functional leaders?

### Section 2.2 — Position-to-Role Mapping & Sizing

Translation of organizational positions into TOM roles, with headcount sizing based on process volumes and automation levels.

**Key deliverables**:
- Position-to-role mapping matrix
- FTE sizing model (volume-based + complexity-adjusted)
- Span of control analysis
- Role rationalization recommendations

**Typical questions answered**: How many people do we need? What roles are required? How does automation change our staffing model?

### Section 2.3 — Functional Job Profiles

Detailed job descriptions for each role in the target operating model, including skills, competencies, and career paths.

**Key deliverables**:
- Job profile catalog (one per unique role)
- Skills and competency matrix
- Training needs analysis
- Career progression pathways

**Typical questions answered**: What skills do we need? What does each role look like? How do people grow in the new model?

**Interdependencies**: Layer 2 depends on Layer 1 (processes define what roles are needed) and influences Layer 3 (service delivery determines where roles are located) and Layer 5 (roles drive KPI ownership).

---

## Layer 3: Service (Sections 3.x)

**Purpose**: Define the service delivery model — where work is performed, by whom (internal vs external), and how services are managed.

### Section 3.1 — Service Delivery Model

The strategic design of how services are sourced, located, and delivered.

**Key deliverables**:
- Sourcing strategy per process area (insource / outsource / hybrid / GBS)
- Location strategy (onshore / nearshore / offshore)
- Service catalog with SLAs per service
- Transition roadmap from current to target delivery model

**Typical questions answered**: Should we build a GBS? What should we outsource? Where should work be located? What SLAs should we target?

**Sourcing options**:
| Model | Description | Best For |
|-------|-------------|----------|
| **Insource** | Internal team, internal location | Core strategic processes |
| **Outsource** | Third-party provider | Commodity processes, peak capacity |
| **Hybrid** | Internal team with outsourced augmentation | Complex processes with variable volumes |
| **GBS** | Centralized shared services organization | Standardized, high-volume transactional work |

### Section 3.2 — Service Management Framework

ITIL-aligned service management processes for the operating model.

**Key deliverables**:
- Incident management process
- Change management process
- Service request catalog
- Continuous improvement framework
- Service reporting and governance

**Typical questions answered**: How do we manage service quality? How do we handle incidents? How do we drive continuous improvement?

**Interdependencies**: Layer 3 depends on Layers 1 and 2 (processes and roles define what services exist) and connects to Layer 4 (technology enables service management tooling) and Layer 5 (KPIs measure service performance).

---

## Layer 4: Technology (Sections 4.x)

**Purpose**: Define the technology platforms, AI capabilities, and technical architecture that enable the operating model.

### Section 4.1 — AI Augmentation Overlay

The design of how artificial intelligence enhances processes across all domains.

**Key deliverables**:
- AI opportunity assessment per L3 process
- AI use case catalog (Copilot, custom agents, RPA, ML models)
- Human-in-the-loop vs autonomous decision matrix
- AI maturity roadmap (assist → augment → automate → autonomous)

**Typical questions answered**: Where can AI add value? What level of autonomy is appropriate? How do we sequence AI adoption?

### Section 4.2 — Supporting Technology / Technology Overlay

The mapping of technology platforms to business processes.

**Key deliverables**:
- Technology-to-process mapping matrix
- Platform landscape diagram (D365, Power Platform, Azure, Fabric, M365)
- Integration architecture (APIs, data flows, middleware)
- Technology rationalization recommendations

**Typical questions answered**: Which platform supports which process? Where are the integration points? What should we consolidate?

### Section 4.3 — Application Architecture & Data Flows

Detailed technical architecture showing application components, data flows, and integration patterns.

**Key deliverables**:
- Application component diagram (C4 container level)
- Data flow diagrams (entity-level)
- Integration pattern catalog (sync, async, batch, event-driven)
- API inventory and contract specifications

**Typical questions answered**: How do systems connect? Where does data flow? What integration patterns do we use?

### Section 4.4 — Environment Architecture

Infrastructure and environment design for development, testing, and production.

**Key deliverables**:
- Environment strategy (dev, test, UAT, staging, production)
- Infrastructure architecture (Azure regions, networking, security)
- DevOps pipeline design
- Disaster recovery and business continuity design

**Typical questions answered**: How many environments do we need? How do we deploy changes? What is our DR strategy?

**Interdependencies**: Layer 4 is enabled by Layers 1–3 (business requirements drive technology decisions) and enables Layer 5 (technology generates the data for analytics) and Layer 6 (technology enforces governance controls).

---

## Layer 5: Data & Analytics (Sections 5.x)

**Purpose**: Define how the organization measures performance, manages master data, and derives insights.

### Section 5.1 — KPIs Linked to Benchmarks

Performance indicators tied to industry benchmarks and strategic objectives.

**Key deliverables**:
- KPI catalog per L2 process area
- Industry benchmark comparisons (APQC, Hackett, Gartner)
- KPI ownership matrix (linked to GPOs and roles)
- Target-setting methodology

**Typical questions answered**: How do we measure success? How do we compare to peers? Who owns each metric?

### Section 5.2 — Reporting Packages & Dashboards

Operational and executive reporting design.

**Key deliverables**:
- Dashboard specification per stakeholder group
- Report catalog with frequency, audience, and content
- Data visualization standards
- Power BI / Fabric dashboard templates

**Typical questions answered**: What reports do we need? Who sees what? How often? What does the executive dashboard look like?

### Section 5.3 — MDM Design & Governance

Master data management strategy and governance framework.

**Key deliverables**:
- Master data entity catalog (customer, vendor, product, employee, chart of accounts)
- Data ownership and stewardship model
- Data quality rules and validation
- MDM architecture (golden record, match/merge, distribution)

**Typical questions answered**: Who owns master data? How do we ensure data quality? What is our golden record strategy?

**Interdependencies**: Layer 5 depends on all preceding layers (processes generate data, people own data, services consume data, technology stores data) and informs Layer 6 (data governance is part of overall governance).

---

## Layer 6: Governance (Sections 6.x)

**Purpose**: Define the control framework, security posture, and policy landscape that ensures compliance and risk management.

### Section 6.1 — Security & Controls

Internal controls, segregation of duties, and security design.

**Key deliverables**:
- Control catalog per L3 process (preventive, detective, corrective)
- Segregation of duties (SoD) matrix
- Security role design (aligned to Layer 2 roles)
- Audit trail and logging requirements

**Typical questions answered**: What controls do we need? How do we enforce SoD? How do we ensure auditability?

### Section 6.2 — Policies

Organizational policies that govern the operating model.

**Key deliverables**:
- Policy catalog (operational, financial, data, technology, HR)
- Policy-to-process mapping
- Compliance requirement mapping (SOX, GDPR, industry-specific)
- Policy review and update cadence

**Typical questions answered**: What policies govern our operations? How do we ensure compliance? How often do we review policies?

**Interdependencies**: Layer 6 is the capstone — it applies governance across all other layers, ensuring that processes are controlled, people are authorized, services are compliant, technology is secure, and data is governed.

---

## Layer Interaction Model

```
┌─────────────────────────────────────────────┐
│  Layer 6: Governance                        │  ← Applies across all layers
│  (Security, Controls, Policies)             │
├─────────────────────────────────────────────┤
│  Layer 5: Data & Analytics                  │  ← Measures all layers
│  (KPIs, Dashboards, MDM)                    │
├─────────────────────────────────────────────┤
│  Layer 4: Technology                        │  ← Enables all layers
│  (AI, Platforms, Architecture, Environments)│
├─────────────────────────────────────────────┤
│  Layer 3: Service                           │  ← Delivers processes via org
│  (Delivery Model, Service Management)       │
├─────────────────────────────────────────────┤
│  Layer 2: Organization                      │  ← Executes processes
│  (GPOs, Roles, Job Profiles)                │
├─────────────────────────────────────────────┤
│  Layer 1: Processes                         │  ← Foundation
│  (Taxonomies, Maturity, Flows, Practices)   │
└─────────────────────────────────────────────┘
```
