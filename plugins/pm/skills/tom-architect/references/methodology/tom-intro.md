---
category: methodology
loading_priority: 1
tokens_estimate: 3200
keywords:
  - target operating model
  - TOM
  - what is TOM
  - digital transformation
  - business architecture
  - enterprise architecture
  - M&A
  - regulatory change
  - cost optimization
  - cloud migration
  - strategy to execution
  - operating model design
version: "1.0"
last_updated: "2026-03-23"
---

# What Is a Target Operating Model (TOM)?

A Target Operating Model defines the **future-state blueprint** for how an organization delivers value through its people, processes, technology, data, services, and governance. It translates business strategy into an actionable, measurable operational design.

---

## Definition

A TOM is a structured representation of an organization's desired operating state across six interdependent layers. It answers the question: **"How will we operate differently to achieve our strategic objectives?"**

Unlike a current-state assessment (which documents "how we work today"), a TOM defines "how we will work tomorrow" — with enough specificity to drive implementation decisions while remaining flexible enough to adapt to change.

---

## The 6-Layer Framework

The TOM framework is organized into six layers, each addressing a critical dimension of operations:

| Layer | Name | Sections | Core Question |
|-------|------|----------|---------------|
| 1 | **Processes** | 1.1 – 1.4 | What work do we do, and how do we do it? |
| 2 | **Organization** | 2.1 – 2.3 | Who does the work, and how are they structured? |
| 3 | **Service** | 3.1 – 3.2 | Where is the work performed, and who delivers it? |
| 4 | **Technology** | 4.1 – 4.4 | What tools and platforms enable the work? |
| 5 | **Data & Analytics** | 5.1 – 5.3 | How do we measure, report, and govern our data? |
| 6 | **Governance** | 6.1 – 6.2 | How do we ensure compliance, security, and control? |

Each layer contains 2–4 sections (18 sections total), providing granular design specifications.

---

## When to Use a TOM

### Digital Transformation
When migrating from legacy systems to modern platforms (e.g., D365 F&O, SAP S/4HANA), a TOM ensures that business processes are redesigned — not merely replicated — on new technology.

### Mergers & Acquisitions (M&A)
Post-merger integration requires harmonizing operating models from two or more organizations. A TOM provides the target state that drives integration planning, organizational design, and system rationalization.

### Regulatory Change
New regulations (IFRS 17, CSRD, SOX enhancements) require operating model changes across processes, controls, reporting, and governance. A TOM ensures these changes are implemented holistically rather than in silos.

### Cost Optimization
When leadership mandates cost reduction, a TOM identifies optimization opportunities across all six layers — process automation, organizational right-sizing, service delivery model changes, and technology consolidation.

### Cloud Migration
Moving to cloud-based platforms changes not just technology but also how processes are executed, how data flows, how services are managed, and how governance is enforced. A TOM ensures the full operating model is designed for cloud-native operations.

### Global Business Services (GBS) / Shared Services
Establishing or optimizing a GBS center requires a comprehensive operating model that defines which services are centralized, what processes they follow, what technology they use, and how performance is measured.

---

## TOM vs Business Architecture vs Enterprise Architecture

| Dimension | Business Architecture | Target Operating Model | Enterprise Architecture |
|-----------|----------------------|----------------------|------------------------|
| **Scope** | Capabilities, value streams, information maps | Operational design across 6 layers | Technology platforms, integrations, standards |
| **Primary audience** | Strategy & planning teams | Business operations & transformation leads | IT architects & engineering teams |
| **Time horizon** | Strategic (3–5 years) | Tactical (1–3 years) | Technical (6–18 months) |
| **Level of detail** | Abstract — "what we need" | Operational — "how we will work" | Technical — "how we will build" |
| **Key outputs** | Capability maps, value streams | Process designs, org models, KPIs, tech overlays | Solution architectures, data models, API designs |
| **Frameworks** | BIZBOK, Archimate | TOM 6-Layer Framework | TOGAF, Azure WAF, C4 |

### The Bridge Role

The TOM sits between business architecture (strategy) and enterprise architecture (implementation):

```
Business Strategy
        |
        v
Business Architecture  (WHAT capabilities do we need?)
        |
        v
Target Operating Model  (HOW will we operate?)
        |
        v
Enterprise Architecture  (WHAT will we build?)
        |
        v
Solution Implementation  (HOW will we build it?)
```

This positioning makes the TOM the critical translation layer. Without it, business strategy becomes disconnected from technology implementation — leading to systems that technically work but fail to deliver business outcomes.

---

## TOM Design Principles

1. **Strategy-led**: Every design decision traces back to a strategic objective
2. **Process-first**: Technology serves processes, not the other way around
3. **Data-driven**: Decisions are informed by benchmarks, KPIs, and analytics
4. **People-centric**: Organizational design considers change management, skills, and culture
5. **Technology-enabled**: Modern platforms (D365, Power Platform, Azure, Fabric) are leveraged as accelerators
6. **AI-augmented**: Artificial intelligence is embedded across all layers as an accelerator, not an afterthought
7. **Iterative**: The TOM evolves as the organization matures — it is a living design, not a one-time document

---

## Domain Coverage

The TOM framework supports six functional domains, each with full coverage across all 18 sections:

| Domain | Primary L1 Processes | Primary Platform |
|--------|---------------------|-----------------|
| **Finance** | Record to Report, Order to Cash, Procure to Pay | D365 F&O |
| **HR** | Hire to Retire, Talent to Performance, Payroll | D365 HR / SuccessFactors |
| **Procurement** | Source to Contract, Procure to Pay, Supplier Mgmt | D365 F&O / Ariba |
| **Supply Chain** | Plan to Produce, Order to Deliver, Warehouse Mgmt | D365 SCM |
| **Cyber Security** | Identify, Protect, Detect, Respond, Recover | Azure Security / Sentinel |
| **Sustainability** | Measure, Report, Reduce, Offset, Govern | D365 Sustainability / Fabric |

---

## Key Terminology

- **L1–L4**: Process decomposition levels (see `methodology/process-decomposition.md`)
- **Maturity Level 1–5**: Process maturity scale (see `methodology/maturity-framework.md`)
- **Section X.Y**: TOM section identifier (e.g., 1.1 = Process Taxonomies, 4.1 = AI Augmentation)
- **GPO**: Global Process Owner — the senior leader accountable for an end-to-end process
- **GBS**: Global Business Services — centralized shared services organization
- **Technology Overlay**: The mapping of technology platforms to business processes
