---
category: templates
loading_priority: 3
tokens_estimate: 3200
keywords:
  - deck template
  - PPTX
  - PowerPoint
  - presentation
  - executive summary
  - TOM deck
  - slides
  - capability map
  - maturity assessment
  - roadmap
  - organizational design
  - service delivery
  - technology overlay
  - AI augmentation
  - KPI framework
version: "1.0"
last_updated: "2026-03-23"
---

# TOM Deck Template — 15-Slide PPTX Specification

Standard presentation template for Target Operating Model deliverables. This specification defines the structure, content, and visual approach for each slide.

---

## Invocation Pattern

To generate the deck using the pptx skill:

```
Use the ms-pptx skill to create a TOM presentation following the template in
references/templates/tom-deck-template.md. Domain: {domain}. Focus: {current/target/both}.
```

---

## Slide Specifications

### Slide 1: Title Slide

- **Title**: "{Domain} Target Operating Model"
- **Subtitle**: "{Client Name} | {Date}"
- **Content**: Project name, version number, confidentiality notice
- **Visual approach**: Clean title with client and firm logos, brand colors
- **Key elements**: Domain name, client name, date, version, "CONFIDENTIAL" watermark if needed

### Slide 2: Executive Summary

- **Title**: "Executive Summary"
- **Content**: 3–5 bullet points summarizing the TOM scope, key findings, and recommendations. Include the headline maturity score (current vs target) and top 3 transformation themes.
- **Visual approach**: Text-heavy with a summary callout box on the right showing key metrics
- **Key elements**: Scope statement, current maturity (overall), target maturity (overall), top 3 themes, timeline summary

### Slide 3: TOM Framework Overview

- **Title**: "Target Operating Model Framework"
- **Content**: The 6-layer framework visual showing all layers and their sections. Brief description of each layer (one line each).
- **Visual approach**: Stacked horizontal bars representing the 6 layers, color-coded. Sections listed within each bar.
- **Key elements**: All 6 layers with section numbers, layer descriptions, visual hierarchy

### Slide 4: Current State Assessment

- **Title**: "Current State Assessment"
- **Content**: Summary of current-state findings across all 6 layers. Key pain points, inefficiencies, and risks identified. Top 5 current-state challenges.
- **Visual approach**: Left side — summary text organized by layer. Right side — spider/radar chart showing current maturity scores by dimension.
- **Key elements**: Current maturity scores, pain point list, risk indicators

### Slide 5: Capability Map

- **Title**: "{Domain} Capability Map"
- **Content**: L1 and L2 process hierarchy for the domain, showing all end-to-end processes and their major process areas.
- **Visual approach**: Mindmap or treemap visualization. Color-code by maturity (red/amber/green) or by transformation scope (in/out of scope).
- **Key elements**: All L1 processes, L2 breakdowns, scope indicators
- **Diagram**: Use capability map Mermaid template from `_index/diagram-patterns.md`

### Slide 6: Maturity Assessment

- **Title**: "Process Maturity Assessment"
- **Content**: Current vs target maturity scores for all L2 processes. Gap analysis highlighting the largest gaps. Dimension breakdown (People, Process, Technology, Data).
- **Visual approach**: Heatmap matrix (rows = L2 processes, columns = dimensions). Quadrant chart overlay showing gap priorities.
- **Key elements**: Maturity heatmap, gap scores, priority classification (Quick Win / Transform / Maintain / Assess)
- **Diagram**: Use maturity assessment Mermaid template

### Slide 7: Process Taxonomy

- **Title**: "Process Taxonomy — {L1 Process Name}"
- **Content**: Detailed decomposition of the primary L1 process showing L2, L3, and representative L4 activities. Automation flags at L4 level.
- **Visual approach**: Hierarchical flowchart (left to right). Color-code L4 activities by automation classification.
- **Key elements**: Process hierarchy, automation flags, system mapping
- **Diagram**: Use process taxonomy Mermaid template
- **Note**: Repeat this slide for each L1 process in scope (insert additional slides as needed)

### Slide 8: Organizational Design

- **Title**: "Target Organizational Design"
- **Content**: GPO model showing end-to-end process ownership. Org chart showing key roles and reporting lines. FTE sizing summary (current vs target). Span of control analysis.
- **Visual approach**: Org chart on the left, FTE summary table on the right. Highlight new roles and eliminated roles.
- **Key elements**: GPO assignments, org chart, FTE counts, new/changed roles

### Slide 9: Service Delivery Model

- **Title**: "Service Delivery Model"
- **Content**: Sourcing strategy per L2 process (insource / outsource / hybrid / GBS). Location strategy (onshore / nearshore / offshore). SLA targets for key services.
- **Visual approach**: Matrix with L2 processes as rows and sourcing/location as columns. Pie chart showing FTE distribution by location.
- **Key elements**: Sourcing decisions per process, location split, SLA targets

### Slide 10: Technology Overlay

- **Title**: "Technology Overlay"
- **Content**: Platform-to-process mapping showing which technology supports each L2 process. Integration architecture showing data flows between systems. Key technology decisions and rationale.
- **Visual approach**: C4-style container diagram showing the technology landscape. Process-to-platform mapping table.
- **Key elements**: Platform landscape, process mapping, integration points
- **Diagram**: Use technology overlay Mermaid template

### Slide 11: AI Augmentation

- **Title**: "AI Augmentation Roadmap"
- **Content**: AI opportunity assessment per L2/L3 process. Classification of opportunities (Copilot, custom agents, RPA, ML). Phased roadmap (assist → augment → automate → autonomous). Quick wins vs strategic initiatives.
- **Visual approach**: Timeline / roadmap visual showing AI adoption phases. Matrix of AI use cases by process and AI type.
- **Key elements**: AI use case catalog, adoption phases, ROI estimates

### Slide 12: KPI Framework

- **Title**: "KPI Framework & Benchmarks"
- **Content**: KPI catalog for the domain showing metric name, definition, current performance, industry benchmark, and target. Top 10 KPIs highlighted. KPI ownership assignments.
- **Visual approach**: KPI scorecard table with red/amber/green indicators. Benchmark comparison bar charts for top 5 KPIs.
- **Key elements**: KPI definitions, current vs benchmark vs target, ownership

### Slide 13: Data & Analytics

- **Title**: "Data & Analytics Design"
- **Content**: Master data entity catalog. Data governance model (ownership, stewardship). Dashboard and reporting design overview. Data quality approach.
- **Visual approach**: Entity relationship overview on the left, dashboard mockup on the right.
- **Key elements**: Master data entities, governance roles, dashboard specifications

### Slide 14: Governance

- **Title**: "Governance Framework"
- **Content**: Control framework summary (preventive, detective, corrective). Segregation of duties (SoD) highlights. Policy landscape overview. Compliance mapping (SOX, GDPR, industry-specific).
- **Visual approach**: Control framework matrix. SoD conflict heat indicators. Policy catalog summary table.
- **Key elements**: Control catalog summary, SoD highlights, compliance mapping

### Slide 15: Roadmap & Next Steps

- **Title**: "Transformation Roadmap"
- **Content**: Phased implementation plan (typically 3–4 phases over 18–36 months). Key milestones and dependencies. Resource requirements per phase. Risk summary and mitigation. Immediate next steps (next 30/60/90 days).
- **Visual approach**: Gantt-style timeline with phases, milestones, and workstreams. Traffic light summary of risks.
- **Key elements**: Phase definitions, milestones, resource needs, risks, 30/60/90 day actions

---

## Slide Insertion Rules

- **Multi-L1 scope**: Insert additional Slide 7 copies for each L1 process beyond the first
- **Multi-domain scope**: Insert a domain separator slide before repeating Slides 5–14 for each domain
- **Appendix**: Add appendix slides for detailed process flows, full KPI catalogs, complete RACI matrices, and detailed technology specifications as needed
- **Executive version**: For C-suite audiences, use Slides 1–3, 6, 10, 11, 12, 15 only (8-slide condensed version)

---

## Visual Standards

| Element | Specification |
|---------|--------------|
| Font (titles) | Segoe UI Semibold, 28pt |
| Font (body) | Segoe UI, 14pt |
| Primary color | #1a73e8 (blue) |
| Secondary color | #4285f4 (light blue) |
| Accent colors | #2e7d32 (green), #c62828 (red), #f57c00 (amber) |
| Maturity colors | L1=#c62828, L2=#f57c00, L3=#fdd835, L4=#66bb6a, L5=#2e7d32 |
| Slide dimensions | 16:9 widescreen |
