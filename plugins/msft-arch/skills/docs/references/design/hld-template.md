---
category: design-documentation
loading_priority: 2
tokens_estimate: 2800
keywords:
  - high-level design
  - HLD
  - solution architecture
  - C4 diagram
  - architecture document
  - design template
  - integration architecture
  - data architecture
  - security architecture
version: "1.0"
last_updated: "2026-03-21"
---

# High-Level Design (HLD) Document Template

This reference provides the complete structure and guidance for generating High-Level Design documents. Use the docx skill to produce the final deliverable.

---

## Section 1: Document Control

Every HLD must begin with a document control table.

| Field            | Value                          |
|------------------|--------------------------------|
| Document Title   | [Solution Name]: High-Level Design |
| Version          | 1.0                            |
| Author           | [Architect Name]               |
| Reviewers        | [Reviewer 1], [Reviewer 2]     |
| Approval Status  | Draft / In Review / Approved   |
| Date Created     | [Date]                         |
| Last Updated     | [Date]                         |

### Change History

| Version | Date | Author | Description of Change |
|---------|------|--------|-----------------------|
| 0.1     |      |        | Initial draft         |
| 1.0     |      |        | Approved baseline     |

---

## Section 2: Executive Summary (~1 page)

### Solution Purpose and Business Value
Describe the business problem being solved and the value the solution delivers. Keep this to 2-3 paragraphs aimed at executive stakeholders.

### Key Architectural Decisions (Top 3-5)
Summarize the most significant decisions. Each entry should state the decision, the rationale, and the ADR reference number.

| # | Decision | Rationale | ADR Ref |
|---|----------|-----------|---------|
| 1 |          |           | ADR-001 |
| 2 |          |           | ADR-002 |
| 3 |          |           | ADR-003 |

### Technology Stack Summary
Reference the selected stack (A, B, C, or D) and list the primary technologies. Link to the Technology Stack Summary section for full detail.

### Expected Outcomes and Success Metrics
List 3-5 measurable outcomes with target values (e.g., "Reduce order processing time from 48h to 4h").

---

## Section 3: Solution Overview and Architecture Vision

### Business Context and Problem Statement
Describe the current state, pain points, and drivers for change. Include relevant business process context.

### Solution Scope

| In Scope | Out of Scope |
|----------|--------------|
|          |              |

### Architecture Principles Guiding the Design
List the principles applied (e.g., cloud-native, API-first, security by design, least privilege). For each principle, state how it influences the design.

### Target Operating Model (TOM) Summary
Describe the operational model: who operates the solution, support tiers, change management approach, and DevOps responsibilities.

---

## Section 4: C4 Context Diagram

Include a Mermaid C4 Context diagram showing the solution as a single system boundary with all external interactions. Refer to `c4-diagram-guide.md` for templates.

**Must include:**
- User personas (internal users, external users, administrators)
- Integrated systems (upstream and downstream)
- Data sources consumed
- External APIs and third-party services
- Data flow direction and protocol labels

---

## Section 5: C4 Container Diagram

Include a Mermaid C4 Container diagram showing internal containers. Refer to `c4-diagram-guide.md` for per-stack templates.

### Per-Stack Container Patterns

**Stack A (Power Platform Native):**
- Dataverse (data store)
- Model-driven app (case management / data-heavy UI)
- Canvas app (task-oriented / mobile UI)
- Power Automate (workflow orchestration)
- Power BI (reporting and analytics)

**Stack B (Power Platform + Azure PaaS):**
- All Stack A containers, plus:
- Azure App Service (custom web application)
- Azure Functions (event-driven compute)
- Azure SQL Database (relational data store)
- Azure Service Bus (asynchronous messaging)
- Azure API Management (API gateway)

**Stack C (Containerized / Microservices):**
- All Stack B containers, plus:
- Azure Kubernetes Service (container orchestration)
- Azure Container Apps (serverless containers)
- Azure Container Registry (image store)
- Ingress Controller (traffic routing)

**Stack D (Dynamics 365):**
- D365 Customer Engagement or Finance & Operations modules
- Dataverse (unified data platform)
- Integration middleware (Logic Apps / Service Bus)
- Power Platform for extensions

---

## Section 6: Integration Architecture

### Integration Landscape Diagram
Include a Mermaid flowchart or sequence diagram showing all integration touchpoints.

### Integration Catalog

| # | Source | Target | Protocol | Frequency | Data Format | Direction | Error Handling |
|---|--------|--------|----------|-----------|-------------|-----------|----------------|
| 1 |        |        |          |           |             |           |                |

### Error Handling and Retry Strategies
Document retry policies (max retries, backoff strategy), dead-letter queue usage, and manual intervention procedures.

### Integration Monitoring Approach
Describe how integration health is monitored: Application Insights, Logic App run history, Service Bus metrics, alert rules.

Refer to `integration-patterns.md` for pattern selection guidance.

---

## Section 7: Data Architecture

### Data Flow Diagram
Include a Mermaid flowchart showing data movement through the solution.

### Storage Strategy

| Data Type | Storage Technology | Rationale | Retention |
|-----------|--------------------|-----------|-----------|
| Transactional | | | |
| Analytical | | | |
| Documents/Blobs | | | |
| Cache | | | |

### Data Lifecycle
Describe creation, transformation, archival, and deletion policies.

### Master Data Management Approach
Identify master data entities, system of record for each, and synchronization strategy.

### Data Migration Strategy
If applicable: source mapping, transformation rules, validation approach, cutover plan.

---

## Section 8: Security Architecture

### Identity and Access Management
- Entra ID configuration (tenant, app registrations, groups)
- B2C/B2B for external users (if applicable)
- Conditional Access policies
- Role-based access control (RBAC) model

### Network Security
- Virtual Network topology
- Private endpoints for PaaS services
- Network Security Groups (NSGs)
- Web Application Firewall (WAF) configuration
- DNS architecture

### Data Protection
- Encryption at rest (service-managed vs. customer-managed keys)
- Encryption in transit (TLS 1.2+ enforcement)
- Azure Key Vault for secrets, certificates, and keys
- Data classification and handling

### Compliance Mapping

| Regulatory Requirement | Control | Implementation | Evidence |
|------------------------|---------|----------------|----------|
|                        |         |                |          |

### Zero Trust Alignment
Map design decisions to Zero Trust principles: verify explicitly, least privilege, assume breach.

---

## Section 9: Infrastructure Topology

### Deployment Topology Diagram
Include a Mermaid diagram showing compute, storage, and networking components per environment.

### High Availability Design
- Region strategy (single region, multi-region, paired regions)
- Availability zone usage
- Load balancing approach

### Disaster Recovery

| Metric | Target | Design Approach |
|--------|--------|-----------------|
| RTO    |        |                 |
| RPO    |        |                 |

### Scaling Strategy
Auto-scaling rules, scaling dimensions (horizontal / vertical), and capacity planning.

**Stack relevance:** Stack A has minimal infrastructure detail (PaaS/SaaS managed). Stack C requires the most extensive infrastructure topology documentation.

---

## Section 10: NFR Alignment Matrix

| NFR Category | Requirement | Design Decision | WAF Pillar | ADR Ref |
|--------------|-------------|-----------------|------------|---------|
| Performance  |             |                 | Performance Efficiency | |
| Scalability  |             |                 | Performance Efficiency | |
| Availability |             |                 | Reliability | |
| Security     |             |                 | Security | |
| Operability  |             |                 | Operational Excellence | |
| Cost         |             |                 | Cost Optimization | |

---

## Section 11: Technology Stack Summary

| Layer | Component | Technology | Version | Purpose | License |
|-------|-----------|------------|---------|---------|---------|
| Presentation | | | | | |
| Application  | | | | | |
| Data         | | | | | |
| Integration  | | | | | |
| Infrastructure | | | | | |

---

## Section 12: Assumptions and Constraints

### Technical Assumptions
List assumptions about the environment, capabilities, and dependencies.

### Business Constraints
List budget, timeline, regulatory, and organizational constraints.

### Dependencies on External Parties
List third-party dependencies with risk assessment.

---

## Section 13: Appendices

### Referenced ADR List

| ADR Ref | Title | Status | Date |
|---------|-------|--------|------|
| ADR-001 |       |        |      |

### Glossary of Terms

| Term | Definition |
|------|------------|
|      |            |

### Reference Links
Link to relevant Microsoft Learn documentation, WAF pillars, and technology-specific guidance.

---

## docx Skill Invocation Pattern

When generating the HLD as a Word document, use the following approach:

1. Create the presentation using the docx skill with the section structure above
2. Apply consistent heading styles (Heading 1 for sections, Heading 2 for subsections)
3. Embed Mermaid diagrams as rendered images where the target format supports it
4. Use the document control table as the first page
5. Include a table of contents after the document control page
6. Apply corporate branding if a template is provided
