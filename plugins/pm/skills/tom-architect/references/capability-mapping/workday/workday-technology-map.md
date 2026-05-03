---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3200
keywords: [technology-map, workday, tom-layers, capability-mapping, hcm, financials, adaptive-planning, extend, integration]
version: "1.0"
last_updated: "2026-03-28"
---

# Workday Technology Map — TOM Capabilities to Workday Stack

## Overview

This master mapping connects each TOM design layer to the recommended Workday technology. Workday is a cloud-native platform primarily focused on HCM and Financial Management, with strong capabilities in planning, analytics, and workforce management.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | Workday Business Process Framework | Workday Orchestrations | BPF for approval workflows; Orchestrations for multi-step cross-system processes |
| Process mining | Not native to Workday | Partner: Celonis, SAP Signavio | Integrate via Workday APIs or data exports |
| Business rules | Workday Condition Rules + Validation Rules | Calculated Fields | Condition rules for routing/approval logic; Validation rules for data quality |
| Workflow orchestration | Workday Business Process Framework | Workday Orchestrations (API-based) | BPF for human-centric workflows; Orchestrations for system-to-system choreography |
| Document processing | Workday Document Intelligence | Partner OCR solutions | Document Intelligence for invoice and receipt extraction |
| RPA | Not native to Workday | Partner: UiPath, Automation Anywhere | Integrate via Workday APIs; use for legacy system bridging |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | Workday HCM (Supervisory Orgs, Cost Centers, Companies) | Workday Financial Mgmt (Company Hierarchy) | Supervisory Orgs for people hierarchy; Companies for legal entity structure |
| Role management | Workday Security (Domain/Business Process Policies) | Configurable Security Groups | Role-based, user-based, and intersection security groups |
| Workforce planning | Workday Adaptive Planning (Workforce Planning) | Workday Strategic Workforce Planning | Adaptive for headcount modeling; Strategic for skills-based planning |
| Skills & competency | Workday Skills Cloud (Skills Ontology) | Workday Talent Marketplace | Skills Cloud for AI-inferred skills; Talent Marketplace for internal mobility |
| Collaboration | Workday Collaborative Planning (Adaptive) | Slack/Teams integration | Collaborative planning for cross-team input; Slack/Teams for communication |
| Identity governance | Workday Security Administration | Workday Integration (provisioning to IdP) | Workday as authoritative source; provision to Entra ID, Okta, etc. |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | Workday Help (Employee Service Center) | Workday Case Management | Help for self-service; Case Management for HR support tickets |
| ITSM | Not native (HCM/Finance-focused) | ServiceNow integration | Workday is not an ITSM platform; integrate with dedicated tools |
| SLA management | Workday Case Management (SLA tracking) | Custom reporting | Basic SLA tracking within HR case management |
| Knowledge management | Workday Knowledge Base (Help) | Workday Community Knowledge | Knowledge articles for employee self-service |
| Self-service portal | Workday Employee Self-Service | Workday Help | Native self-service for HR, pay, benefits, time, and absence |
| Service analytics | Workday Prism Analytics | Workday People Analytics | Prism for custom analytics; People Analytics for prebuilt HR insights |

## Layer 4: Technology

### HCM

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Core HR | Workday HCM | Worker Management, Org Management, Staffing | Single global worker record, unlimited org hierarchies |
| Compensation | Workday HCM | Compensation, Advanced Compensation | Salary, merit, bonus, stock, total rewards statements |
| Benefits | Workday HCM | Benefits Administration | Open enrollment, life events, carrier integrations |
| Payroll | Workday Payroll | US, Canada, UK, France, Australia + Cloud Connect | Native payroll for select countries; Cloud Connect for third-party payroll |
| Talent Management | Workday HCM | Performance, Goals, Succession, Career Hub | Continuous performance management, talent reviews, succession pools |
| Recruiting | Workday Recruiting | Job Requisitions, Applications, Candidate Pipeline | End-to-end recruiting with CRM capabilities |
| Learning | Workday Learning | Course Catalog, Learning Campaigns, Content | Formal, informal, and external content learning |
| Time Tracking | Workday Time Tracking | Time Entry, Scheduling, Calculations | Configurable time entry with complex calculation rules |
| Absence Management | Workday Absence Management | Leave Plans, Accruals, Compliance | Global absence plans with country-specific compliance |

### Financial Management

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| General Ledger | Workday Financial Management | GL, Worktags, Accounting | Worktag-based accounting (no chart of accounts required) |
| Accounts Payable | Workday Financial Management | Supplier Accounts, Invoice Processing | Automated invoice matching and payment processing |
| Accounts Receivable | Workday Financial Management | Customer Accounts, Billing, Collections | Customer invoicing, installments, dunning |
| Revenue Management | Workday Financial Management | Revenue Recognition | ASC 606 / IFRS 15 automated revenue recognition |
| Grants Management | Workday Financial Management | Grants, Award Lifecycle | Proposal-to-closeout for public sector and higher education |
| Projects | Workday Financial Management | Projects, Project Billing | Project costing, billing, resource management |
| Expenses | Workday Expenses | Expense Reports, Corporate Cards | Mobile expense entry, receipt capture, policy enforcement |
| Procurement | Workday Procurement | Requisitions, POs, Receipts, Supplier Contracts | Procure-to-pay lifecycle within Workday |
| Asset Management | Workday Financial Management | Assets, Depreciation | Asset lifecycle tracking and depreciation schedules |

### Planning

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Financial Planning | Workday Adaptive Planning | Revenue, Expense, Capital, Cash Flow | Driver-based financial planning with unlimited scenarios |
| Workforce Planning | Workday Adaptive Planning | Headcount, Compensation Modeling | Integrated with HCM actuals for plan-vs-actual |
| Operational Planning | Workday Adaptive Planning | Sales Planning, Demand Planning, Custom | Flexible modeling engine for any planning domain |
| Consolidation | Workday Financial Management | Consolidation, Intercompany | Multi-entity consolidation with intercompany elimination |
| Reporting & Close | Workday Financial Management | Financial Reporting, Close Management | Composite reports, close task management |

### Platform & Extension

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Custom applications | Workday Extend | Build custom apps on the Workday platform with Workday objects |
| Custom objects | Workday Extend (Custom Objects) | Create custom business objects with relationships to core objects |
| Orchestrations | Workday Orchestrations | Multi-step processes that call Workday and external APIs |
| Custom reports | Workday Report Writer | Matrix, composite, and advanced reports with calculated fields |
| Dashboards | Workday Dashboards | Configurable dashboards with worklets and scorecards |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Enterprise analytics | Workday Prism Analytics | Workday People Analytics | Prism for custom multi-source analytics; People Analytics for prebuilt HR |
| KPI dashboards | Workday Dashboards + Scorecards | Workday Adaptive Planning dashboards | Native dashboards for operational KPIs; Adaptive for planning KPIs |
| Predictive analytics | Workday Illuminate (ML) | Workday Adaptive Planning (predictive) | Illuminate for embedded predictions; Adaptive for forecast modeling |
| Data integration (analytics) | Workday Prism Analytics (Data Hub) | Third-party BI (Tableau, Power BI) via APIs | Prism Data Hub for bringing external data into Workday analytics |
| People analytics | Workday People Analytics | Workday Prism Analytics | Prebuilt dashboards for retention, diversity, compensation, talent |
| Financial analytics | Workday Financial Reporting | Workday Prism Analytics, Adaptive dashboards | Native reports for financial statements; Prism for custom |
| Data governance | Workday Data Governance (audit, security) | Workday Prism data lineage | Native audit trail; security-enforced data access |
| Benchmarking | Workday Benchmarking | — | Anonymous peer benchmarking across Workday customer base |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Access governance | Workday Security (Configurable Security Groups) | Workday Audit Trail | Role-based, user-based, intersection security; full change audit |
| Compliance management | Workday Compliance (regulatory updates) | Country-specific compliance packs | Workday delivers regulatory updates in biannual releases |
| Data protection | Workday Data Privacy (masking, consent) | Workday Document Retention | Data masking for sensitive fields; consent management for GDPR |
| Security monitoring | Workday Security Dashboard + Sign-On Reports | SIEM integration via API | Monitor access patterns, failed sign-ons, policy changes |
| Audit & logging | Workday Audit Trail | Workday Custom Reports (audit) | Complete audit trail of all configuration and data changes |
| Segregation of duties | Workday SoD Analysis | Business Process Policy controls | Identify and remediate conflicting access across security groups |

---

## Workday Launch Methodology

| Phase | Key Activities | Workday Tools |
|---|---|---|
| Plan | Scope, governance, team formation, tenant strategy | Workday Community, Deployment Guide |
| Architect | Solution design, integration design, data strategy | Workday Architect Toolkit, Configuration Workbooks |
| Configure & Prototype | System configuration, business process design, prototype | Workday Tenant, Configuration tools |
| Test | End-to-end testing, parallel payroll, UAT | Workday Testing tools, Automated Testing |
| Deploy | Data conversion, cutover, go-live | Workday Data Migration, EIB, Launch Cockpit |
| Production Support | Hypercare, stabilization, continuous improvement | Workday Community, Support Cases, Release Management |

## Integration Patterns

| Pattern | Workday Technology | Use Case |
|---|---|---|
| API-based (sync) | Workday REST/SOAP APIs (WQL, RaaS) | Real-time data retrieval and updates |
| File-based (batch) | Enterprise Interface Builder (EIB) | Scheduled data imports/exports (CSV, XML) |
| Studio integrations | Workday Studio | Complex multi-step integrations with transformations |
| Cloud connectors | Workday Integration Cloud (Packaged Connectors) | Prebuilt connectors for benefits, payroll, banking |
| Middleware | Workday + MuleSoft / Dell Boomi / Workato | Enterprise integration hub pattern |
| Event-driven | Workday Business Process Events + Orchestrations | Trigger external actions on business events (e.g., hire, terminate) |

## Licensing & Editions

| Edition | Scope | Typical Use Case |
|---|---|---|
| Workday HCM | Per-employee pricing | Core HR, talent, learning, time, absence, recruiting |
| Workday Payroll | Per-employee (add-on) | Native payroll for supported countries |
| Workday Financial Management | Per-revenue or per-transaction | GL, AP, AR, procurement, expenses, projects, assets |
| Workday Adaptive Planning | Per-user + per-model | Financial, workforce, and operational planning |
| Workday Prism Analytics | Per-employee or per-user (add-on) | Multi-source analytics beyond core Workday reporting |
| Workday Extend | Included (with limits) / add-on | Custom apps and objects on the Workday platform |
| Workday Peakon Employee Voice | Per-employee (add-on) | Continuous employee listening and engagement surveys |

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| Core HR and talent management | Workday HCM — single global worker record |
| Payroll (supported countries) | Workday Payroll for native; Cloud Connect for third-party |
| Financial management (mid-large enterprise) | Workday Financial Management with worktag architecture |
| Financial and workforce planning | Workday Adaptive Planning with HCM integration |
| Custom HR/Finance application | Workday Extend for platform-native apps |
| Enterprise integration | Workday Integration Cloud + middleware (MuleSoft/Boomi) |
| Advanced people analytics | Workday People Analytics + Prism Analytics |
| Employee engagement measurement | Workday Peakon Employee Voice |
| Self-service employee experience | Workday Help + Employee Self-Service |
