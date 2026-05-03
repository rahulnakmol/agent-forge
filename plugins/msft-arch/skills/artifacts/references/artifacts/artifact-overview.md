---
category: artifacts
loading_priority: 1
tokens_estimate: 1200
keywords:
  - artifact catalog
  - deliverables
  - workbook
  - document
  - presentation
  - dependency graph
  - naming conventions
  - version control
version: "1.0"
last_updated: "2026-03-21"
---

# Artifact Overview: Master Catalog

This document is the single source of truth for every deliverable artifact produced by the artifacts skill. Each artifact has a defined type, the phase in which it is generated, its upstream dependencies, and a brief description.

## Artifact Master Table

| Artifact Name              | Type | Phase Generated       | Dependencies                                | Description                                                      |
| -------------------------- | ---- | --------------------- | ------------------------------------------- | ---------------------------------------------------------------- |
| ADR Workbook               | xlsx | Phase 3 – Design      | Design decisions, stack selection            | Architecture Decision Records with full context and consequences |
| Effort Estimation Workbook | xlsx | Phase 2 – Analysis    | Requirements, user stories, fit-gap results  | Story-point-based effort breakdown by capability and priority     |
| RAID Log                   | xlsx | All Phases             | ADR entries, project context                 | Risks, Assumptions, Issues, and Dependencies tracker             |
| Solution Design Document   | xlsx | Phase 3 – Design      | ADR Workbook, stack selection, NFRs          | Component-level design mapping to Microsoft services             |
| Test Strategy Workbook     | xlsx | Phase 4 – Validation   | Requirements, effort estimation, design      | Test scenarios, acceptance criteria, and automation approach      |
| HLD Document               | docx | Phase 3 – Design      | ADR Workbook, Solution Design Document       | High-Level Design narrative with architecture diagrams           |
| LLD Document               | docx | Phase 3 – Design      | HLD Document, ADR Workbook                   | Low-Level Design with implementation specifications              |
| Architecture Overview      | pptx | Phase 5 – Delivery     | All design artifacts                         | Visual architecture presentation for technical stakeholders      |
| Executive Summary          | pptx | Phase 5 – Delivery     | All artifacts                                | Business-facing summary with costs, timelines, and decisions     |

## Artifact Dependency Graph

The following describes the directed dependency flow between artifacts. An arrow (→) means "feeds into."

```
Requirements (Phase 1)
  ├─→ Effort Estimation Workbook (requirements feed user stories and sizing)
  ├─→ Test Strategy Workbook (requirements define test scenarios)
  └─→ Fit-Gap Analysis
        └─→ Effort Estimation Workbook (fit-gap informs complexity)

Stack Selection (Phase 2)
  └─→ Fit-Gap Analysis
        └─→ Effort Estimation Workbook

Design Decisions (Phase 3)
  └─→ ADR Workbook (each decision becomes an ADR entry)

ADR Workbook
  ├─→ Solution Design Document (ADRs referenced per component)
  ├─→ RAID Log (decisions surface risks and assumptions)
  ├─→ HLD Document (ADRs justify architectural choices)
  └─→ LLD Document (ADRs constrain implementation detail)

Solution Design Document
  ├─→ HLD Document (component mapping drives narrative)
  └─→ LLD Document (component detail feeds specs)

All Phases (continuous)
  └─→ RAID Log (risks, assumptions, issues, dependencies captured throughout)

HLD + LLD + ADR + Effort + Test Strategy
  ├─→ Architecture Overview (pptx)
  └─→ Executive Summary (pptx)
```

## Naming Conventions

All artifacts follow a standardized naming pattern:

```
[Client]_[ArtifactType]_[Project]_[Date]_v[Version].[ext]
```

| Component      | Format                        | Example                |
| -------------- | ----------------------------- | ---------------------- |
| Client         | PascalCase, no spaces         | Contoso                |
| ArtifactType   | PascalCase abbreviation       | ADR, EffortEstimation  |
| Project        | PascalCase, no spaces         | CallCenterAI           |
| Date           | YYYYMMDD                      | 20260321               |
| Version        | Major.Minor                   | v1.0                   |
| Extension      | xlsx, docx, pptx              | .xlsx                  |

**Full examples:**
- `Contoso_ADR_CallCenterAI_20260321_v1.0.xlsx`
- `Contoso_EffortEstimation_CallCenterAI_20260321_v1.0.xlsx`
- `Contoso_HLD_CallCenterAI_20260321_v1.0.docx`
- `Contoso_ArchOverview_CallCenterAI_20260321_v1.0.pptx`

## Version Control Rules

| Version Type | When Applied                              | Example   |
| ------------ | ----------------------------------------- | --------- |
| Major (x.0)  | Initial baseline delivery                 | v1.0      |
| Minor (x.1)  | Incremental updates within same phase     | v1.1      |
| Major bump   | Post-review revision or phase transition  | v2.0      |

- Every artifact starts at **v1.0** when first generated.
- Minor versions (v1.1, v1.2) are applied when rows are added, values updated, or feedback incorporated within the same engagement phase.
- A major version bump (v2.0) occurs when the artifact is formally re-baselined after stakeholder review or when the engagement moves to a new phase requiring structural changes.
- The RAID Log is the only artifact that spans all phases; its version increments continuously.
