---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3400
keywords: [technology-map, sap, tom-layers, capability-mapping, s4hana, successfactors, ariba, btp, analytics-cloud, integration]
version: "1.0"
last_updated: "2026-03-28"
---

# SAP Technology Map — TOM Capabilities to SAP Stack

## Overview

This master mapping connects each TOM design layer to the recommended SAP technology. Use this as the primary lookup when translating a TOM capability requirement into a concrete SAP solution component.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | SAP Build Process Automation | SAP Integration Suite (iFlows) | Build PA for business-user workflows; Integration Suite for system-to-system orchestration |
| Process mining | SAP Signavio Process Intelligence | Celonis integration | Signavio for native SAP process mining; Celonis for multi-system landscapes |
| Business rules | SAP Build Process Automation (Decisions) | S/4HANA BRFplus | Decisions for cloud-native rules; BRFplus for on-stack ABAP rules |
| Workflow orchestration | SAP Build Process Automation (Workflows) | S/4HANA Flexible Workflows | Cloud workflows for cross-system; Flexible Workflows for in-app approvals |
| Document processing | SAP Build Process Automation (Document AI) | SAP AI Services (Doc Information Extraction) | Document AI for invoice/PO extraction; AI Services for custom document types |
| RPA | SAP Build Process Automation (Desktop Agent) | — | Attended and unattended bots for legacy SAP GUI and third-party automation |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | SAP SuccessFactors (Employee Central) | S/4HANA Org Management | EC for cloud-first HR org; S/4HANA for finance/logistics org units |
| Role management | S/4HANA Role-Based Access (PFCG) | SAP Cloud Identity Services, IAG | PFCG for on-stack roles; IAG for cross-system access governance |
| Workforce planning | SuccessFactors Workforce Planning | SAP Analytics Cloud (Planning) | SF for headcount planning; SAC for financial workforce modeling |
| Skills & competency | SuccessFactors (Skills Ontology, Learning) | SAP SuccessFactors Opportunity Marketplace | Skills Ontology for AI-driven skill inference; Opportunity Marketplace for talent mobility |
| Collaboration | SAP Build Work Zone (Advanced Edition) | Microsoft Teams integration | Work Zone for unified launchpad and collaboration; Teams for chat-based collaboration |
| Identity governance | SAP Cloud Identity Services (IAS/IPS) | SAP Access Control (GRC) | IAS for authentication; IPS for provisioning; GRC AC for SoD and access risk |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | SAP Service Cloud | S/4HANA Service Management | Service Cloud for omnichannel customer service; S/4HANA for internal plant maintenance service |
| ITSM | Integration with ServiceNow / ITSM tools | SAP Cloud ALM | SAP Cloud ALM for SAP-centric operations; ServiceNow for enterprise-wide ITSM |
| SLA management | SAP Service Cloud (SLA Engine) | SAP Cloud ALM (monitoring) | Service Cloud for customer SLAs; Cloud ALM for system availability SLAs |
| Knowledge management | SAP Service Cloud Knowledge Base | SAP Enable Now | Service Cloud KB for customer-facing; Enable Now for end-user training content |
| Self-service portal | SAP Build Work Zone (Standard) | SAP Commerce Cloud (Service Portal) | Work Zone for employee self-service; Commerce Cloud for customer self-service |
| Service analytics | SAP Analytics Cloud (embedded) | S/4HANA Embedded Analytics | SAC for cross-module service dashboards; embedded analytics for in-app KPIs |

## Layer 4: Technology

### ERP & HCM

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Enterprise Finance | S/4HANA Cloud (Finance) | GL, AP, AR, Asset Accounting, Cash Mgmt | Universal Journal architecture; real-time financial close |
| Supply Chain Management | S/4HANA Cloud (SCM) | MM, PP, QM, WM/EWM | Integrated supply chain with embedded analytics |
| Manufacturing | S/4HANA Cloud (Manufacturing) | PP, PP/DS, MES integration | Discrete, process, and repetitive manufacturing |
| Procurement | SAP Ariba + S/4HANA Procurement | Sourcing, Contracts, Supplier Mgmt, Buying | Ariba for network-based procurement; S/4HANA for operational purchasing |
| Sales & Distribution | S/4HANA Cloud (Sales) | SD, Billing, ATP | Order-to-cash with advanced ATP and billing |
| Core HR & Payroll | SAP SuccessFactors (Employee Central + EC Payroll) | Core HR, Payroll, Benefits, Time | Cloud HCM suite with localized payroll engines |
| Talent Management | SAP SuccessFactors (Talent) | Recruiting, Onboarding, Performance, Succession | End-to-end talent lifecycle |
| Learning | SAP SuccessFactors Learning | LMS, Compliance Training | Formal and informal learning with compliance tracking |
| Compensation | SAP SuccessFactors Compensation | Salary, Variable Pay, Total Rewards | Compensation planning with calibration |

### Platform & Integration

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Application development | SAP Build Apps (low-code) | Visual drag-and-drop app builder on BTP |
| Pro-code development | SAP Build Code (SAP Business Application Studio) | Full-stack dev with CAP framework and Joule AI assist |
| Extension platform | SAP BTP (Cloud Foundry / Kyma) | Side-by-side extensions; keep S/4HANA core clean |
| Integration platform | SAP Integration Suite (CPI) | Cloud-native iPaaS with 3000+ prebuilt integrations |
| API management | SAP Integration Suite (API Management) | Centralized API gateway, policies, developer portal |
| Event-driven architecture | SAP Event Mesh | CloudEvents-based messaging for event-driven integrations |

### AI & Intelligent Automation

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Generative AI assistant | SAP Joule | Embedded AI copilot across SAP applications |
| Business AI scenarios | SAP Business AI (embedded) | 130+ AI scenarios across S/4HANA, SF, Ariba |
| AI development | SAP AI Core + AI Launchpad (BTP) | Model training, deployment, and management on BTP |
| Machine learning | SAP HANA Cloud (PAL/APL) | In-database ML with Predictive Analysis Library |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Enterprise analytics | SAP Analytics Cloud | SAP Datasphere | SAC for visualization and planning; Datasphere for data fabric |
| KPI dashboards | SAP Analytics Cloud (Stories) | S/4HANA Embedded Analytics (Fiori KPI tiles) | SAC for executive dashboards; Fiori tiles for operational KPIs |
| Planning & budgeting | SAP Analytics Cloud Planning | BPC (legacy) | SAC Planning for unified financial and operational planning |
| Predictive analytics | SAP Analytics Cloud (Smart Predict) | SAP AI Core | Smart Predict for citizen data science; AI Core for advanced ML |
| Data warehousing | SAP Datasphere | SAP BW/4HANA | Datasphere for hybrid data fabric; BW/4HANA for existing BW investments |
| Data integration | SAP Datasphere (Replication Flows) | SAP Integration Suite, SLT | Replication Flows for analytics; Integration Suite for transactional |
| Data governance | SAP Datasphere (Catalog) | SAP Master Data Governance | Catalog for metadata discovery; MDG for master data quality |
| Real-time analytics | S/4HANA Embedded Analytics (CDS Views) | SAC live connection | CDS views for real-time operational reporting directly on HANA |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Access governance | SAP Access Control (GRC) | SAP Cloud Identity Access Governance | GRC AC for SoD analysis and emergency access; IAG for cloud-native access reviews |
| Risk management | SAP Risk Management (GRC) | SAP Process Control | GRC RM for enterprise risk; Process Control for continuous monitoring |
| Compliance management | SAP Process Control (GRC) | S/4HANA Audit Management | Automated control monitoring and compliance reporting |
| Security monitoring | SAP Enterprise Threat Detection | SIEM integration (Sentinel, Splunk) | ETD for SAP-specific threat detection; SIEM for enterprise-wide correlation |
| Data protection | SAP Data Privacy Governance | SAP Information Lifecycle Management | DPG for GDPR/privacy compliance; ILM for data retention |
| Audit & logging | SAP Cloud ALM + S/4HANA Security Audit Log | SAP ETD | Cloud ALM for operations monitoring; SAL for detailed audit trails |

---

## Capability-to-Process Mapping

| L1 Business Process | Primary SAP Module | Platform |
|---|---|---|
| Record to Report | S/4HANA FI/CO | S/4HANA Cloud |
| Procure to Pay | SAP Ariba + S/4HANA MM | Ariba / S/4HANA |
| Order to Cash | S/4HANA SD + Billing | S/4HANA Cloud |
| Plan to Produce | S/4HANA PP + Digital Manufacturing | S/4HANA Cloud |
| Hire to Retire | SuccessFactors (EC + Talent Suite) | SuccessFactors |
| Source to Contract | SAP Ariba Sourcing + Contracts | Ariba |
| Lead to Cash | SAP Sales Cloud + S/4HANA SD | SAP CX / S/4HANA |
| Issue to Resolution | SAP Service Cloud | SAP CX |
| Treasury & Cash Mgmt | S/4HANA Treasury | S/4HANA Cloud |
| Asset Management | S/4HANA Asset Management | S/4HANA Cloud |

## SAP Activate Methodology Phases

| Phase | Key Activities | SAP Tools |
|---|---|---|
| Discover | Scope definition, value mapping, fit-to-standard | SAP Signavio Process Navigator, SAP Model Company |
| Prepare | Project setup, governance, environment provisioning | SAP Cloud ALM, S/4HANA Starter System |
| Explore | Fit-to-standard workshops, delta requirements, process confirmation | SAP Best Practices, Signavio, Fiori Test Tenant |
| Realize | Configuration, build, test (string/integration/UAT) | SAP Cloud ALM (test management), SAP Build |
| Deploy | Data migration, cutover, go-live, hypercare | SAP Cloud ALM (deploy management), Migration Cockpit |
| Run | Operations, continuous improvement, innovation cycles | SAP Cloud ALM, SAP for Me, SAP Learning Hub |

## Integration Patterns

| Pattern | SAP Technology | Use Case |
|---|---|---|
| API-based (sync) | SAP Integration Suite (API Mgmt + CPI) | Real-time data retrieval and updates |
| Event-driven (async) | SAP Event Mesh + Integration Suite | Publish-subscribe for business events (e.g., sales order created) |
| File-based (batch) | SAP Integration Suite (SFTP adapter) | Legacy system file transfers, bank statement imports |
| Data replication | SAP Datasphere Replication / SLT | Near-real-time data replication to analytics layer |
| Prebuilt integration | SAP Integration Suite (prebuilt content) | 3000+ prebuilt iFlows for common SAP-to-SAP and SAP-to-third-party |
| Business Network | SAP Business Network (Ariba Network) | B2B procurement, supply chain collaboration |
| B2B / EDI | SAP Integration Suite (B2B Add-on) | EDI/cXML exchange with trading partners |

## Licensing & Editions

| Edition | Scope | Typical Use Case |
|---|---|---|
| S/4HANA Cloud Public Edition | Multi-tenant SaaS, quarterly updates | New implementations, standard processes, rapid deployment |
| S/4HANA Cloud Private Edition | Single-tenant, managed cloud, customer-controlled upgrades | Complex industries, heavy customization, migration from ECC |
| RISE with SAP | Bundle: S/4HANA Cloud + BTP + Business Network + ALM | Full transformation package with commercial simplification |
| GROW with SAP | Bundle: S/4HANA Cloud PE + BTP + community | Mid-market and subsidiaries, fast adoption |
| SAP BTP | Consumption-based or subscription | Extension, integration, analytics, AI development |
| SuccessFactors | Per-employee-per-month (PEPM) | HCM suite, modules licensed independently |
| SAP Ariba | Network-based + module licensing | Strategic and operational procurement |

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| Process is within S/4HANA standard scope | Use SAP Best Practice process — fit-to-standard |
| Process needs citizen-developer automation | SAP Build Process Automation + Build Apps |
| Process requires enterprise integration | SAP Integration Suite (CPI + API Management + Event Mesh) |
| Process involves AI/ML augmentation | SAP Joule + Business AI embedded scenarios |
| Analytics spans multiple data sources | SAP Datasphere (data fabric) + SAP Analytics Cloud |
| Procurement involves supplier collaboration | SAP Ariba + SAP Business Network |
| HCM requirement (cloud-first) | SAP SuccessFactors full suite |
| Security/compliance/GRC requirement | SAP GRC suite (Access Control, Risk Management, Process Control) |
| External portal / launchpad needed | SAP Build Work Zone (Advanced Edition) |
