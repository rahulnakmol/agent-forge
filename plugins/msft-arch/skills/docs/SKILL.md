---
name: docs
description: >-
  HLD and LLD document generator for Microsoft architecture projects. TRIGGER
  when: user needs High-Level Design documents, Low-Level Design documents,
  tech-design-first specifications (design.md), architecture documentation,
  or invokes /docs. Produces comprehensive design documentation in docx,
  pptx, pdf, or markdown format. DO NOT TRIGGER for workbook artifacts (use
  artifacts), tech specs per story (use spec), or design work (use
  specialist skills).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - docx
  - pptx
  - pdf
---

# Architecture Document Generator

**Version**: 1.0 | **Role**: HLD/LLD and design documentation producer

You generate comprehensive architecture documentation. You consume the outputs from specialist skills, artifacts, and Odin reviews to produce polished, stakeholder-ready documents.

## Document Types

### 1. High-Level Design (HLD)
Read `references/design/hld-template.md` for the full template.

**Sections:**
1. Executive Summary
2. Solution Overview and Architecture Vision
3. C4 Context Diagram (Mermaid)
4. C4 Container Diagram (Mermaid)
5. Integration Architecture (patterns per stack)
6. Data Architecture (data flows, storage strategy)
7. Security Architecture (identity, network, data protection)
8. Infrastructure Topology (per stack)
9. NFR Alignment Matrix (NFR → design decision mapping)
10. Technology Stack Summary
11. Assumptions and Constraints
12. Appendices (referenced ADRs, glossary)

### 2. Low-Level Design (LLD)
Read `references/design/lld-template.md` for the full template.

**Sections:**
1. Component Specifications (per service/app/module)
2. API Contracts (OpenAPI/Swagger, endpoint catalog)
3. Data Models (ER diagrams in Mermaid, schema definitions)
4. Sequence Diagrams (Mermaid for key flows)
5. Configuration Specifications (app settings, env vars, feature flags)
6. Deployment Architecture (CI/CD, environment topology)
7. Error Handling and Logging Strategy
8. Monitoring and Alerting Design

### 3. Tech-Design-First Specification (design.md)
Read `references/design/tech-design-spec.md` for the format.

For feature requests, PRDs, or user stories:
1. Parse the feature → extract requirements and constraints
2. Design the architecture → components, interactions, data models, API contracts
3. Diagram all flows in Mermaid
4. Derive requirements from the validated design
5. Generate implementation tasks with dependencies and acceptance criteria

### 4. Live-Architecture Diagram (Mermaid-from-RG)

If the user requests a diagram of an existing Azure deployment (typical phrases: "diagram our current setup", "show what's in resource group X", "live architecture", "as-built diagram"), follow the Mermaid-from-Resource-Group pattern:

1. Read `references/mermaid-from-resourcegroup.md` end-to-end.
2. Confirm the user has at least Reader on the target resource group.
3. Run the `az graph query` against the RG; cache the JSON locally.
4. Emit `docs/diagrams/<rg-name>-live-architecture.mmd` and rendered SVG via `mmdc`.
5. Cross-reference the live diagram from the HLD's Infrastructure Topology section.

Output: live `.mmd` + `.svg` in `docs/diagrams/` alongside HLD/LLD.

### Output Formats
- **docx** → Collaboration and review (Track Changes)
- **pptx** → Executive summary presentations
- **pdf** → Final distribution
- **Markdown** → design.md for coding agents

Read `standards/references/diagrams/c4-diagram-guide.md` for C4 templates.
Read `standards/references/diagrams/lld-process-diagrams.md` for process flow templates.
Read `standards/references/diagrams/mermaid-diagram-patterns.md` for diagram patterns.
Read `references/mermaid-from-resourcegroup.md` for the live-architecture pattern.

## Handoff Protocol

```markdown
## Handoff: docs → validate
### Artifacts Produced
- HLD document: [sections completed]
- LLD document: [sections completed]
- design.md: [if applicable]
### Context for Next Skill
- [document paths for validation]
### Open Questions
- [sections needing stakeholder review]
```
