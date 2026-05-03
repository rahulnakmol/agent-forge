---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 1600
keywords: [power-platform, power-automate, power-apps, power-pages, power-bi, copilot-studio, low-code, automation, citizen-developer, coe]
version: "1.0"
last_updated: "2026-03-23"
---

# Power Platform Mapping — Automation & Low-Code Capabilities

## Overview

Maps TOM automation and low-code requirements to Power Platform components. Includes governance patterns via the Center of Excellence (CoE) Starter Kit.

---

## Process Automation — Power Automate

### Cloud Flows

| TOM Pattern | Power Automate Solution | Example |
|---|---|---|
| Approval workflows | Multi-stage approval flows with adaptive cards | Purchase requisition approval chain, leave request |
| System-to-system integration | Automated flows with 1,000+ connectors | D365 to SharePoint document sync, SAP to Dataverse |
| Scheduled batch processing | Scheduled flows with concurrency control | Nightly data reconciliation, weekly report distribution |
| Event-driven reactions | Trigger-based flows (Dataverse, HTTP, Event Grid) | New case auto-assignment, SLA breach escalation |
| Document routing | AI Builder + flow orchestration | Invoice capture, contract extraction, form processing |

### Desktop Flows (RPA)

| TOM Pattern | Desktop Flow Solution | Example |
|---|---|---|
| Legacy system automation | Attended/unattended desktop flows | Mainframe data entry, legacy ERP order processing |
| Screen scraping | UI-based recording with selectors | Extract data from terminal applications |
| File manipulation | Local file and Excel automation | Process CSV exports, transform spreadsheets |
| Hybrid automation | Cloud flow triggers desktop flow | Cloud approval triggers desktop flow for legacy posting |

### Process Mining

| TOM Pattern | Process Mining Solution | Example |
|---|---|---|
| Process discovery | Import event logs, auto-discover process map | Discover actual P2P process variants |
| Conformance checking | Compare actual vs. ideal process | Identify O2C process deviations |
| Bottleneck analysis | Performance analytics on process steps | Find period-close bottlenecks |
| Automation opportunity | Identify high-volume, rule-based steps | Recommend RPA candidates in R2R |

---

## Citizen Applications — Power Apps

### Model-Driven Apps

| TOM Pattern | Model-Driven Approach | Best For |
|---|---|---|
| Data-centric CRUD | Table-driven forms, views, dashboards on Dataverse | Case management, asset tracking, request management |
| Business process guided | Business Process Flows (BPF) | Employee onboarding, incident resolution, loan origination |
| Role-based workspace | App designer with sitemap and security roles | Department-specific views of shared data |

### Canvas Apps

| TOM Pattern | Canvas Approach | Best For |
|---|---|---|
| Mobile-first experience | Responsive canvas app with offline support | Field data collection, time entry, inspections |
| Custom UX | Pixel-perfect design with Power Fx formulas | Executive dashboards, approval interfaces, kiosks |
| Multi-source mashup | Connect to 1,000+ data sources without Dataverse | Ad-hoc reporting, cross-system lookups |
| Embedded in D365 | Canvas app embedded in model-driven form | Custom visualizations within D365 records |

---

## External Portals — Power Pages

| TOM Pattern | Power Pages Solution | Example |
|---|---|---|
| Customer self-service | Authenticated portal with Dataverse tables | Case submission, order tracking, knowledge base |
| Vendor collaboration | External user portal with table permissions | Vendor invoice submission, RFQ response |
| Employee self-service | Internal portal for non-licensed users | Benefits enrollment, IT request submission |
| Community / events | Public site with registration | Event registration, community forums |
| Partner portal | Multi-tenant portal with web roles | Partner deal registration, co-selling |

---

## Analytics — Power BI

| TOM Pattern | Power BI Solution | Example |
|---|---|---|
| Executive dashboards | Power BI service with row-level security | CFO financial dashboard, CEO operational scorecard |
| Embedded analytics | Power BI Embedded in Power Apps / D365 | In-context analytics within business applications |
| Operational reports | Paginated reports (pixel-perfect, printable) | Financial statements, regulatory reports, invoices |
| Self-service analytics | Power BI Desktop with shared datasets | Ad-hoc analysis by business analysts |
| Real-time monitoring | Power BI streaming datasets / DirectLake | Production line monitoring, live sales ticker |

---

## Virtual Agents — Copilot Studio

| TOM Pattern | Copilot Studio Solution | Example |
|---|---|---|
| Customer support bot | Topic-based bot with knowledge base | IT helpdesk, HR FAQ, order status inquiry |
| Process-triggered agent | Autonomous agent triggered by events | Invoice exception handler, SLA breach responder |
| Internal assistant | Enterprise copilot with org knowledge | Employee policy assistant, procurement guide |
| Multi-channel deployment | Deploy to Teams, web, mobile, voice | Omnichannel customer engagement |
| Custom plugin agent | Copilot with API plugins and connectors | Agent that queries ERP, creates records, sends emails |

---

## Governance — Center of Excellence

### CoE Starter Kit Components

| Component | Purpose |
|---|---|
| CoE Core | Inventory of all apps, flows, environments, makers; usage analytics |
| CoE Governance | DLP policy management, compliance workflows, app/flow approval processes |
| CoE Nurture | Maker onboarding, training campaigns, community management |
| CoE Innovation Backlog | Idea submission, prioritization, business justification pipeline |

### Managed Environments

| Capability | Description |
|---|---|
| Sharing limits | Restrict how widely apps and flows can be shared |
| Solution checker enforcement | Require all solutions pass quality checks before import |
| Maker welcome content | Custom onboarding content for new makers |
| Data policies (DLP) | Control which connectors can be used together (business vs. non-business vs. blocked) |
| Pipeline deployment | Managed deployment pipelines for ALM |

### TOM Automation Opportunity Matrix

Use this matrix to identify which TOM processes are candidates for Power Platform solutions:

| Criteria | Score 0 (Low) | Score 1 (Medium) | Score 2 (High) |
|---|---|---|---|
| Manual effort | < 1 hr/week | 1-10 hrs/week | > 10 hrs/week |
| Rule-based logic | Judgment-heavy | Mixed | Fully rule-based |
| Data in M365/Dataverse | External systems only | Partial | Fully accessible |
| Error frequency | Rare | Occasional | Frequent |
| User technical skill | Very low | Moderate | Power user |

**Score >= 7**: Strong Power Platform candidate (citizen-developed)
**Score 4-6**: Power Platform with pro-dev support
**Score < 4**: Consider custom development or third-party solution
