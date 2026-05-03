---
category: index
loading_priority: 1
tokens_estimate: 2500
keywords:
  - framework overview
  - TOM summary
  - layer hierarchy
  - progressive disclosure
  - token budget
  - reference loading
  - interconnections
  - layer dependencies
version: "1.0"
last_updated: "2026-03-23"
---

# TOM Framework Overview

One-page summary of the 6-layer Target Operating Model framework, layer interconnections, and reference loading strategy.

---

## Framework at a Glance

```
╔═══════════════════════════════════════════════════════════════╗
║                    BUSINESS STRATEGY                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │  LAYER 6: GOVERNANCE                                    │  ║
║  │  6.1 Security & Controls  │  6.2 Policies               │  ║
║  ├─────────────────────────────────────────────────────────┤  ║
║  │  LAYER 5: DATA & ANALYTICS                              │  ║
║  │  5.1 KPIs  │  5.2 Reporting  │  5.3 MDM                │  ║
║  ├─────────────────────────────────────────────────────────┤  ║
║  │  LAYER 4: TECHNOLOGY                                    │  ║
║  │  4.1 AI  │  4.2 Tech Overlay  │  4.3 App Arch  │ 4.4 Env│ ║
║  ├─────────────────────────────────────────────────────────┤  ║
║  │  LAYER 3: SERVICE                                       │  ║
║  │  3.1 Service Delivery  │  3.2 Service Management        │  ║
║  ├─────────────────────────────────────────────────────────┤  ║
║  │  LAYER 2: ORGANIZATION                                  │  ║
║  │  2.1 GPOs  │  2.2 Role Mapping  │  2.3 Job Profiles     │  ║
║  ├─────────────────────────────────────────────────────────┤  ║
║  │  LAYER 1: PROCESSES                                     │  ║
║  │  1.1 Taxonomies │ 1.2 Maturity │ 1.3 Flows │ 1.4 Practices│║
║  └─────────────────────────────────────────────────────────┘  ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                  TECHNOLOGY IMPLEMENTATION                    ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Layer Interconnections

The six layers are not independent — they form a connected system:

| From Layer | To Layer | Relationship |
|-----------|----------|-------------|
| 1 Processes | 2 Organization | Processes define the roles and structure needed |
| 1 Processes | 4 Technology | Processes define technology requirements |
| 1 Processes | 5 Data & Analytics | Processes generate the data to be measured |
| 1 Processes | 6 Governance | Processes require controls and compliance |
| 2 Organization | 3 Service | Roles determine where and how services are delivered |
| 2 Organization | 5 Data & Analytics | Roles own KPIs and data stewardship |
| 3 Service | 4 Technology | Service model drives technology deployment locations |
| 4 Technology | 5 Data & Analytics | Technology generates and stores data for analytics |
| 4 Technology | 6 Governance | Technology enforces security controls |
| 5 Data & Analytics | 6 Governance | Data governance is part of overall governance |

**Key insight**: Layer 1 (Processes) is the foundation. Every other layer derives from or serves the process layer. Always start TOM design with processes.

---

## Progressive Disclosure Guidance

Load references progressively based on the user's query to stay within token budgets.

### Tier 1 — Always Load (~6,500 tokens)
These provide enough context to understand any TOM request and route to the right detailed references:

| File | Tokens | Purpose |
|------|--------|---------|
| `_index/quick-reference.md` | ~4,000 | Request patterns, legends, navigation |
| `_index/tom-framework-overview.md` | ~2,500 | This file — framework summary, loading strategy |

### Tier 2 — Load Based on Topic (~3,000–4,200 tokens each)
Load when the user's request touches a specific methodology area:

| File | Tokens | Load When |
|------|--------|-----------|
| `methodology/tom-intro.md` | ~3,200 | User asks "what is a TOM?" or needs positioning |
| `methodology/tom-layers.md` | ~4,200 | User needs layer definitions or section details |
| `methodology/maturity-framework.md` | ~2,800 | User asks about maturity or assessment |
| `methodology/process-decomposition.md` | ~3,400 | User asks about process hierarchy or L1–L4 |

### Tier 3 — Load for Specific Domain Work (~2,000–4,000 tokens each)
Load the relevant domain files only when the user is working on a specific domain:

| Pattern | Files to Load |
|---------|--------------|
| Process design | `domains/{domain}/1.1-process-taxonomies.md` + `1.3-process-flows.md` |
| Maturity assessment | `domains/{domain}/1.2-maturity-models.md` |
| Org design | `domains/{domain}/2.1-process-owners.md` + `2.2-role-mapping.md` + `2.3-job-profiles.md` |
| Service model | `domains/{domain}/3.1-service-delivery.md` + `3.2-service-management.md` |
| Technology | `domains/{domain}/4.1-ai-augmentation.md` through `4.4-environment-arch.md` |
| KPIs & data | `domains/{domain}/5.1-kpis-benchmarks.md` through `5.3-mdm-governance.md` |
| Governance | `domains/{domain}/6.1-security-controls.md` + `6.2-policies.md` |

### Tier 4 — Load for Artifact Generation
Load only when generating deliverables:

| File | Tokens | Load When |
|------|--------|-----------|
| `templates/tom-deck-template.md` | ~3,200 | Generating PPTX deck |
| `templates/tom-workbook-template.md` | ~3,200 | Generating XLSX workbook |
| `templates/tom-diagram-templates.md` | ~5,500 | Generating Mermaid diagrams |
| `_index/diagram-patterns.md` | ~2,800 | Quick diagram reference |

---

## Token Budget Strategy

| Scenario | Max Budget | Loading Plan |
|----------|-----------|-------------|
| Simple question | ~10,000 | Tier 1 + one methodology file |
| Domain TOM design | ~25,000 | Tier 1 + Tier 2 (relevant) + Tier 3 (one domain, relevant sections) |
| Full TOM build | ~50,000 | Tier 1 + Tier 2 (all) + Tier 3 (one domain, all sections) |
| Multi-domain TOM | ~80,000 | Tier 1 + Tier 2 (all) + Tier 3 (multiple domains, all sections) |
| Artifact generation | ~15,000 | Tier 1 + relevant Tier 4 template |

**Rule of thumb**: Never load more than one full domain at a time. If the user needs cross-domain work, load one domain, complete it, then move to the next.

---

## Section Numbering Convention

All 18 TOM sections follow a consistent numbering scheme:

```
Section X.Y
  │     │
  │     └── Sub-section within the layer (1, 2, 3, or 4)
  └──────── Layer number (1–6)
```

This numbering is consistent across all six domains. Section 1.1 in Finance is structurally equivalent to Section 1.1 in HR — same methodology, different content.
