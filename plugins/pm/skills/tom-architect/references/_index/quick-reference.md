---
category: index
loading_priority: 1
tokens_estimate: 4000
keywords:
  - quick reference
  - cheat sheet
  - request patterns
  - TOM layers
  - maturity levels
  - process levels
  - domains
  - emergency links
  - navigation
  - common requests
  - finance transformation
  - GBS
  - AI roadmap
  - executive presentation
version: "1.0"
last_updated: "2026-03-23"
---

# Quick Reference

Top-level navigation, common request patterns, and cheat sheets for the tom-architect skill.

---

## Top 8 Request Patterns

### 1. Build a TOM for Our Finance Transformation

**Request example**: "Build a TOM for our finance transformation" / "Design the target operating model for our R2R process"

**Quick response approach**: Start with domain selection (Finance), identify which L1 processes are in scope, load the relevant domain references (1.1 through 6.2), then systematically walk through each TOM layer.

**References to load**: `domains/finance/1.1-process-taxonomies.md` through `domains/finance/6.2-policies.md`

**What to ask first**: Which L1 processes are in scope? What is the current ERP platform? What is the target platform? Is there a GBS or shared services center? What is the target go-live timeline?

### 2. Assess Our Current Process Maturity

**Request example**: "Assess our current process maturity" / "How mature are our procurement processes?"

**Quick response approach**: Load the maturity framework, identify the domain and L2 processes in scope, then guide through a structured assessment across People, Process, Technology, and Data dimensions.

**References to load**: `methodology/maturity-framework.md`, `domains/{domain}/1.2-maturity-models.md`

**What to ask first**: Which domain(s) are in scope? Do you have existing maturity assessments? What industry are you in (for benchmarking)?

### 3. Map Our Processes to D365 F&O

**Request example**: "Map our processes to D365 F&O" / "Show me how our current processes map to D365 modules"

**Quick response approach**: Load the process taxonomy for the relevant domain, then overlay the D365 module mapping. Show which L3 processes map to which D365 modules and identify gaps requiring extensions or third-party solutions.

**References to load**: `domains/{domain}/1.1-process-taxonomies.md`, `domains/{domain}/4.2-technology-overlay.md`, `domains/{domain}/4.3-app-architecture.md`

**What to ask first**: Which functional domain? Which D365 modules are already licensed? Are there existing customizations or ISV solutions?

### 4. Design the Organizational Structure for a GBS

**Request example**: "Design the organizational structure for a GBS" / "How should we structure our shared services center?"

**Quick response approach**: Load the organization and service delivery references. Design the GBS structure including GPO model, role mapping, FTE sizing, and service delivery model (onshore/nearshore/offshore split).

**References to load**: `domains/{domain}/2.1-process-owners.md`, `domains/{domain}/2.2-role-mapping.md`, `domains/{domain}/2.3-job-profiles.md`, `domains/{domain}/3.1-service-delivery.md`

**What to ask first**: Which functions are in scope for the GBS? How many FTEs currently? What locations are available? What is the target cost reduction?

### 5. Create a Technology Overlay for Our ERP

**Request example**: "Create a technology overlay for our ERP" / "What technology supports each process?"

**Quick response approach**: Load the technology overlay and app architecture references. Build a matrix mapping each L2 process to the enabling technology platform (D365 F&O, D365 SCM, Power Platform, Azure, Fabric, third-party).

**References to load**: `domains/{domain}/4.2-technology-overlay.md`, `domains/{domain}/4.3-app-architecture.md`, `domains/{domain}/4.4-environment-arch.md`

**What to ask first**: What is the current technology landscape? What is the target platform strategy? Are there integration requirements with non-Microsoft systems?

### 6. Define KPIs for Our Procurement Function

**Request example**: "Define KPIs for our procurement function" / "What metrics should we track for P2P?"

**Quick response approach**: Load the KPI and reporting references for the domain. Present the KPI catalog with industry benchmarks, help prioritize, and design the dashboard structure.

**References to load**: `domains/{domain}/5.1-kpis-benchmarks.md`, `domains/{domain}/5.2-reporting-dashboards.md`

**What to ask first**: Which L1/L2 processes? What industry (for benchmarking)? Who is the audience for the KPIs (operational team, management, executive)?

### 7. Build an AI Augmentation Roadmap

**Request example**: "Build an AI augmentation roadmap" / "Where should we apply AI in our finance processes?"

**Quick response approach**: Load the AI augmentation reference for the domain. Assess each L3 process for AI potential, classify opportunities (Copilot, custom agents, RPA, ML), and sequence into a phased roadmap (assist, augment, automate, autonomous).

**References to load**: `domains/{domain}/4.1-ai-augmentation.md`, `domains/{domain}/1.4-leading-practices.md`

**What to ask first**: What is the current automation level? Is Microsoft 365 Copilot already deployed? What is the appetite for AI-driven process change? Any regulatory constraints on AI use?

### 8. Generate a TOM Deck for Executive Presentation

**Request example**: "Generate a TOM deck for executive presentation" / "Create slides for our TOM readout"

**Quick response approach**: Load the deck template and diagram templates. Generate a 15-slide PPTX following the standard structure. Use Mermaid diagrams for visualizations and invoke the pptx skill for generation.

**References to load**: `templates/tom-deck-template.md`, `templates/tom-diagram-templates.md`

**What to ask first**: Which domain(s)? Current state or target state focus? Who is the audience (C-suite, steering committee, project team)? What key messages should be emphasized?

---

## Quick Legend

### Maturity Levels (1–5)

| Level | Name | One-liner |
|-------|------|-----------|
| 1 | Initial | Ad-hoc, person-dependent |
| 2 | Managed | Basic processes, some standardization |
| 3 | Defined | Standardized, documented, measured |
| 4 | Quantified | Data-driven, predictive, automated |
| 5 | Optimized | Continuous improvement, AI-augmented |

### Process Levels (L1–L4)

| Level | Name | Granularity | Example |
|-------|------|------------|---------|
| L1 | Value Chain | End-to-end | Record to Report |
| L2 | Process Area | Major grouping | General Ledger |
| L3 | Process | Specific process | Journal Entry Processing |
| L4 | Activity/Task | Individual step | Post journal entry |

### Functional Domains

| Domain | Abbreviation | Primary Platform |
|--------|-------------|-----------------|
| Finance | FIN | D365 F&O |
| Human Resources | HR | D365 HR |
| Procurement | PROC | D365 F&O |
| Supply Chain Management | SCM | D365 SCM |
| Cyber Security | CYBER | Azure Security |
| Sustainability | SUST | D365 Sustainability |

### TOM Layers & Sections

| Layer | Name | Sections |
|-------|------|----------|
| 1 | Processes | 1.1 Taxonomies, 1.2 Maturity, 1.3 Flows, 1.4 Leading Practices |
| 2 | Organization | 2.1 GPOs, 2.2 Role Mapping, 2.3 Job Profiles |
| 3 | Service | 3.1 Delivery Model, 3.2 Service Management |
| 4 | Technology | 4.1 AI Augmentation, 4.2 Tech Overlay, 4.3 App Architecture, 4.4 Environment |
| 5 | Data & Analytics | 5.1 KPIs, 5.2 Reporting, 5.3 MDM |
| 6 | Governance | 6.1 Security & Controls, 6.2 Policies |

---

## Emergency Links

| Resource | URL |
|----------|-----|
| Microsoft Well-Architected Framework | https://learn.microsoft.com/azure/well-architected/ |
| D365 F&O Documentation | https://learn.microsoft.com/dynamics365/finance/ |
| D365 SCM Documentation | https://learn.microsoft.com/dynamics365/supply-chain/ |
| D365 HR Documentation | https://learn.microsoft.com/dynamics365/human-resources/ |
| Power Platform Documentation | https://learn.microsoft.com/power-platform/ |
| Microsoft Fabric Documentation | https://learn.microsoft.com/fabric/ |
| Azure AI Services | https://learn.microsoft.com/azure/ai-services/ |
| APQC Process Classification Framework | https://www.apqc.org/process-frameworks |
| ITIL 4 Foundation | https://www.axelos.com/certifications/itil-service-management/ |

---

## Reference File Loading Strategy

**Always load first** (every request):
- `_index/quick-reference.md` (this file)
- `_index/tom-framework-overview.md`

**Load based on request type**:
- Methodology questions → `methodology/*.md`
- Domain-specific work → `domains/{domain}/*.md`
- Deck/document generation → `templates/*.md`
- Diagram generation → `_index/diagram-patterns.md` or `templates/tom-diagram-templates.md`

**Load on demand** (only when specifically needed):
- Full domain reference files (load the specific section, not all 18)
- Template specifications (only when generating artifacts)
