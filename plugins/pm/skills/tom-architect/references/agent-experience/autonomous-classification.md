---
category: "agent-experience"
loading_priority: 2
tokens_estimate: 1300
keywords: [autonomous, classification, scoring, decision-framework, human-in-the-loop, copilot-assist, rpa, automation-level, risk-assessment]
version: "1.0"
last_updated: "2026-03-23"
---

# Autonomous Classification — Decision Framework for AI Autonomy Level

## Overview

A structured scoring framework to classify the appropriate AI autonomy level for each TOM process. This framework is referenced by the AI Augmentation Framework and should be applied during TOM process analysis to determine the right balance of human and AI involvement.

---

## Scoring Criteria

Each criterion is scored 0-5. Total score determines the autonomy classification.

### Criterion 1: Data Availability

> Is the data needed for AI inference accessible, structured, and clean?

| Score | Description | Example |
|---|---|---|
| 0 | No digital data; paper-based or verbal | Verbal approvals, handwritten forms |
| 1 | Unstructured data in emails/documents | Contract terms scattered across emails |
| 2 | Data in multiple disconnected systems | Customer data in CRM + ERP + spreadsheets |
| 3 | Data in one system but needs cleansing | D365 data with quality issues |
| 4 | Clean structured data in D365/Dataverse | Well-maintained master data in D365 |
| 5 | Rich labeled data with historical outcomes | 3+ years of invoice matching outcomes |

### Criterion 2: Decision Complexity

> Is the decision logic rule-based or does it require human judgment?

| Score | Description | Example |
|---|---|---|
| 0 | Deep expertise, creative judgment, negotiation | Executive strategy, complex negotiations |
| 1 | Multi-factor analysis with high ambiguity | Investment decisions, legal interpretations |
| 2 | Guidelines exist but require interpretation | Performance evaluation, vendor selection |
| 3 | Mostly rule-based with occasional edge cases | Credit approval with clear thresholds |
| 4 | Rule-based with defined exception handling | Invoice 3-way matching |
| 5 | Fully deterministic lookup or calculation | Tax rate lookup, currency conversion |

### Criterion 3: Regulatory Constraint

> Does regulation require human involvement?

| Score | Description | Example |
|---|---|---|
| 0 | Regulation mandates human accountability | Audit sign-off, SOX controls |
| 1 | Regulation requires human review of AI output | Medical device approval, safety-critical |
| 2 | Industry best practice recommends oversight | Financial reporting, HR termination |
| 3 | Organizational policy requires approval | Procurement above threshold |
| 4 | Minimal regulatory concern | Internal process optimization |
| 5 | No regulatory or compliance constraint | Office supply ordering |

### Criterion 4: Error Tolerance

> What is the cost of an incorrect AI decision?

| Score | Description | Example |
|---|---|---|
| 0 | Irreversible financial/legal/safety harm | Incorrect regulatory filing, safety incident |
| 1 | Significant customer impact or rework | Wrong shipment to major customer |
| 2 | Costly but detectable and correctable | Mis-posted journal entry (reversible) |
| 3 | Minor rework, easily reversible | Incorrect categorization of expense |
| 4 | Low impact, self-correcting next cycle | Minor scheduling inefficiency |
| 5 | Inconsequential | Internal notification routing |

### Criterion 5: Volume/Frequency

> Is the process high-volume enough to justify AI investment?

| Score | Description | Example |
|---|---|---|
| 0 | Rare (< 1 per month) | Annual strategy review |
| 1 | Infrequent (1-5 per month) | Quarterly board report |
| 2 | Periodic (weekly) | Weekly cash position report |
| 3 | Daily (10-50 per day) | Daily journal postings |
| 4 | High volume (50-500 per day) | Invoice processing |
| 5 | Very high volume (> 500 per day) | Transaction matching, email triage |

---

## Classification Thresholds

| Total Score | Classification | Autonomy Level | Governance Model |
|---|---|---|---|
| **20-25** | Fully Autonomous Agent | AI executes independently; human monitors exceptions | Dashboard monitoring; weekly exception review; quarterly model validation |
| **14-19** | Human-in-the-Loop Agent | AI prepares and recommends; human approves critical step | Approval workflow with SLA; escalation on timeout; audit trail |
| **8-13** | Copilot Assist | AI suggests within human workflow; human decides | User feedback loop; periodic accuracy review; opt-in/opt-out |
| **4-7** | RPA (Rule-Based Automation) | Automated execution of deterministic rules | Standard flow monitoring; error queue; version control |
| **0-3** | Human Only | No automation; human performs fully | Training investment; UX optimization; process simplification |

---

## Worked Examples

### Example 1: Invoice Three-Way Matching

| Criterion | Score | Rationale |
|---|---|---|
| Data availability | 5 | PO, receipt, and invoice data all in D365 F&O with clean structure |
| Decision complexity | 4 | Rule-based matching with defined tolerances; exceptions are well-categorized |
| Regulatory constraint | 4 | No regulation requires human matching; internal policy allows auto-match within tolerance |
| Error tolerance | 3 | Mis-match is detectable in AP review; reversible before payment |
| Volume/frequency | 5 | 500+ invoices per day in large enterprise |
| **Total** | **21** | **Fully Autonomous Agent** |

**Recommendation**: Deploy autonomous matching agent. Auto-approve within tolerance (e.g., < 2% variance). Route exceptions to AP specialist queue. Monitor match rate and exception rate via Power BI dashboard.

**Technology**: Power Automate (cloud flow) + AI Builder (invoice extraction) + D365 F&O (matching engine) + Copilot Studio (exception handler agent)

### Example 2: Annual Performance Review

| Criterion | Score | Rationale |
|---|---|---|
| Data availability | 2 | Performance data in D365 HR but qualitative feedback is in emails, Teams, documents |
| Decision complexity | 1 | Requires nuanced judgment on performance, potential, development needs |
| Regulatory constraint | 2 | HR best practice requires manager accountability; some jurisdictions have notification requirements |
| Error tolerance | 1 | Incorrect rating impacts compensation, morale, legal exposure |
| Volume/frequency | 1 | Once or twice per year per employee |
| **Total** | **7** | **RPA (with Copilot Assist overlay)** |

**Recommendation**: Do not automate the review decision. Use Copilot Assist to help managers draft reviews (M365 Copilot for writing, D365 HR data for context). Use RPA (Power Automate) for the review cycle administration (notifications, reminders, deadline tracking, compilation).

**Technology**: M365 Copilot (review drafting) + Power Automate (cycle management) + D365 HR (performance module)

### Example 3: Demand Forecasting

| Criterion | Score | Rationale |
|---|---|---|
| Data availability | 4 | 3+ years of sales history in D365 SCM; external data (weather, economic indicators) available via APIs |
| Decision complexity | 2 | Statistical models work well for stable demand; new products, promotions, and disruptions require judgment |
| Regulatory constraint | 5 | No regulatory constraint on demand planning |
| Error tolerance | 3 | Over/under-forecast causes inventory cost but is correctable in next planning cycle |
| Volume/frequency | 3 | Daily or weekly planning runs across thousands of SKU-location combinations |
| **Total** | **17** | **Human-in-the-Loop Agent** |

**Recommendation**: Deploy AI-generated forecast as baseline (D365 Planning Optimization + Azure ML custom model for external signals). Demand planner reviews and adjusts AI forecast, especially for new products, promotions, and disrupted categories. AI learns from planner adjustments over time.

**Technology**: D365 SCM (Planning Optimization) + Azure ML (custom forecast model) + Power BI (forecast accuracy dashboard) + Power Automate (planner review workflow)

---

## Application Guidance

### When to Apply This Framework

1. **TOM Process Analysis Phase**: Score every L2/L3 process during TOM design
2. **Technology Overlay Phase**: Use scores to select Microsoft technology per process
3. **Roadmap Prioritization**: Prioritize high-score processes (Fully Autonomous, Human-in-the-Loop) for early waves
4. **Business Case Development**: Use scores to estimate effort and benefit per process

### Score Adjustment Factors

| Factor | Adjustment |
|---|---|
| Process is net-new (no historical data) | Reduce Data Availability by 1-2 |
| Organization has low AI maturity | Start with Copilot Assist even for high scores; graduate to autonomous |
| Process spans multiple departments | Reduce Decision Complexity by 1 (coordination complexity) |
| Process is customer-facing | Reduce Error Tolerance by 1 (brand risk) |
| Strong executive sponsorship | Can attempt higher autonomy earlier |
