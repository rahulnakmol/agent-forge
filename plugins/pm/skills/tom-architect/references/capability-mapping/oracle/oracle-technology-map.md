---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3400
keywords: [technology-map, oracle, tom-layers, capability-mapping, fusion, oic, oci, hcm, erp, scm, cx]
version: "1.0"
last_updated: "2026-03-28"
---

# Oracle Technology Map — TOM Capabilities to Oracle Stack

## Overview

This master mapping connects each TOM design layer to the recommended Oracle technology. Use this as the primary lookup when translating a TOM capability requirement into a concrete Oracle solution component.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | Oracle Integration Cloud (OIC) Process Automation | Oracle APEX Workflows | OIC for enterprise processes; APEX for departmental workflows |
| Process mining | Oracle Process Mining (Fusion) | Celonis integration | Native process mining within Fusion apps |
| Business rules | Oracle Business Rules (SOA Suite) | OIC Decision Models (DMN) | SOA rules for on-prem; OIC DMN for cloud-native decisions |
| Workflow orchestration | Oracle BPM (OIC Process) | Oracle Fusion Approval Workflows | OIC Process for cross-system; Fusion for in-app approvals |
| Document processing | Oracle AI Document Understanding (OCI) | OIC Document Processing | OCI for high-volume extraction; OIC for workflow-embedded processing |
| RPA | Oracle Integration Cloud (RPA capabilities) | Third-party RPA (UiPath, AA) | OIC for basic automation; third-party for complex desktop scenarios |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | Oracle HCM Cloud (Workforce Structures) | Oracle ERP Org Hierarchies | HCM for people org; ERP for financial/legal entity hierarchies |
| Role management | Oracle HCM Cloud (Roles) + Fusion Security | OCI IAM | Fusion RBAC for application roles; OCI IAM for infrastructure |
| Workforce planning | Oracle HCM Strategic Workforce Planning | Oracle EPM Workforce Planning | HCM for talent-driven; EPM for finance-driven headcount planning |
| Skills & competency | Oracle HCM Cloud (Talent Profile, Skills Center) | Oracle Learning Cloud | Skills Center for AI-driven skill management; Learning for development |
| Collaboration | Oracle Content Management | Microsoft Teams / Slack integration | OCM for document collaboration; Teams/Slack for real-time chat |
| Identity governance | Oracle Access Governance (OAG) | OCI IAM Identity Domains | OAG for access reviews and SoD; IAM for authentication/authorization |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | Oracle CX Service (Fusion Service) | Oracle Digital Assistant | Fusion Service for case management; Digital Assistant for self-service |
| ITSM | Integration with ServiceNow / BMC | Oracle Cloud Infrastructure Operations | Oracle partners with ITSM vendors; OCI for infrastructure monitoring |
| SLA management | Oracle CX Service (Entitlements) | Oracle Integration (SLA monitoring) | CX Service for customer SLAs; OIC for cross-system SLA tracking |
| Knowledge management | Oracle Knowledge Management (CX) | Oracle Content Management | Oracle KM for customer-facing articles; OCM for internal knowledge |
| Self-service portal | Oracle Digital Assistant + Oracle Visual Builder | Oracle CX Service Portal | Digital Assistant for conversational; Visual Builder for custom portals |
| Service analytics | Oracle Analytics Cloud (embedded) | Oracle Transactional BI (OTBI) | OAC for advanced analytics; OTBI for operational reporting |

## Layer 4: Technology

### ERP

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| General Ledger | Oracle Fusion ERP Cloud | GL, Subledger Accounting | Multi-GAAP, multi-currency, real-time accounting |
| Accounts Payable | Oracle Fusion ERP Cloud | AP, Expenses | Invoice processing, payment management, expense reporting |
| Accounts Receivable | Oracle Fusion ERP Cloud | AR, Revenue Management | Billing, collections, revenue recognition (ASC 606) |
| Fixed Assets | Oracle Fusion ERP Cloud | FA | Asset lifecycle, depreciation, impairment |
| Cash Management | Oracle Fusion ERP Cloud | Cash Management, Treasury | Bank reconciliation, cash positioning, forecasting |
| Project Management | Oracle Fusion ERP Cloud | Project Portfolio Management | Project costing, billing, resource management |

### HCM

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Core HR | Oracle HCM Cloud | Global HR, Workforce Management | Global person model, employment lifecycle, compliance |
| Payroll | Oracle HCM Cloud | Payroll, Global Payroll Interface | Cloud payroll with 30+ country localizations |
| Talent Management | Oracle HCM Cloud | Recruiting, Performance, Succession, Career Dev | End-to-end talent lifecycle with AI recommendations |
| Workforce Management | Oracle HCM Cloud | Time & Labor, Absence Management | Time tracking, scheduling, leave management |
| Learning | Oracle HCM Cloud | Oracle Learning | Formal, informal, and social learning |

### Supply Chain & CX

| TOM Capability | Primary Technology | Module | Notes |
|---|---|---|---|
| Procurement | Oracle SCM Cloud | Procurement, Supplier Portal, Sourcing | Strategic sourcing through operational purchasing |
| Inventory & Warehouse | Oracle SCM Cloud | Inventory Management, WMS | Multi-org inventory with warehouse execution |
| Manufacturing | Oracle SCM Cloud | Manufacturing (Discrete, Process, Mixed-Mode) | Shop floor execution with IoT integration |
| Order Management | Oracle SCM Cloud | Order Management, Global Order Promising | Distributed order orchestration with ATP |
| Sales | Oracle CX Sales | Accounts, Opportunities, Forecasting, CPQ | AI-driven sales with adaptive intelligence |
| Customer Service | Oracle CX Service | Service Requests, Knowledge, Digital Channels | Omnichannel service with AI-assisted resolution |
| Marketing | Oracle CX Marketing (Eloqua, Responsys) | Campaigns, Journeys, ABM | B2B (Eloqua) and B2C (Responsys) marketing automation |
| Commerce | Oracle CX Commerce | B2B, B2C Storefronts | Headless commerce with experience management |

### Platform & Integration

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Integration platform | Oracle Integration Cloud (OIC) | iPaaS with 400+ prebuilt adapters for Oracle and third-party |
| API management | Oracle API Gateway (OCI) | Centralized API management, throttling, analytics |
| Low-code development | Oracle Visual Builder Cloud Service (VBCS) | Extend Fusion apps or build custom applications |
| Application development | Oracle APEX | Low-code for data-centric applications on Oracle Database |
| Event-driven architecture | Oracle Streaming (OCI) + OIC Events | Kafka-compatible streaming for event-driven patterns |
| Infrastructure | Oracle Cloud Infrastructure (OCI) | Compute, networking, storage, containers, Kubernetes (OKE) |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Enterprise analytics | Oracle Analytics Cloud (OAC) | Oracle Fusion Analytics Warehouse (FAW) | OAC for custom analytics; FAW for prebuilt Fusion analytics |
| KPI dashboards | Oracle Fusion Analytics Warehouse | OAC Dashboards, OTBI | FAW for cross-module KPIs; OTBI for transactional reporting |
| Planning & budgeting | Oracle EPM Cloud (Planning) | Oracle EPM Narrative Reporting | EPM for enterprise financial planning and consolidation |
| Predictive analytics | Oracle Analytics Cloud (ML) | OCI Data Science | OAC for citizen data science; OCI DS for advanced ML |
| Data warehousing | Oracle Autonomous Data Warehouse (ADW) | Oracle Exadata Cloud Service | ADW for self-managing cloud DW; Exadata for high-performance |
| Data integration | Oracle Data Integrator (ODI) | OCI Data Integration, GoldenGate | ODI for ELT; GoldenGate for real-time replication |
| Data governance | Oracle Data Catalog (OCI) | Oracle Enterprise Metadata Management | Data Catalog for discovery; OEMM for enterprise metadata |
| Real-time analytics | OCI Streaming + Oracle GoldenGate | OAC Real-Time | GoldenGate for change data capture; Streaming for event analytics |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Access governance | Oracle Access Governance | Oracle Fusion Security Console | OAG for access certification and SoD; Security Console for role management |
| Risk management | Oracle Risk Management Cloud | Oracle GRC (on-prem) | Cloud-native risk assessment and incident management |
| Compliance management | Oracle GRC Cloud | Oracle Financial Reporting Compliance | Automated compliance monitoring and control testing |
| Security monitoring | OCI Security Zones + Cloud Guard | Oracle Data Safe | Cloud Guard for cloud security posture; Data Safe for database security |
| Data protection | Oracle Data Safe | OCI Vault, Database Vault | Data Safe for masking, auditing; Vault for key management |
| Audit & logging | OCI Audit + Logging Analytics | Oracle Fusion Audit Trail | OCI Audit for infrastructure; Fusion Audit for application events |

---

## Oracle Implementation Methodology (Oracle Unified Method — OUM)

| Phase | Key Activities | Oracle Tools |
|---|---|---|
| Envision | Business case, scope, success metrics | Oracle Value Realization |
| Architect | Solution design, integration architecture, data strategy | Oracle Cloud Reference Architecture |
| Build | Configuration, extension development, data migration design | Oracle Visual Builder, OIC, FBDI |
| Validate | Testing (SIT, UAT, performance), training | Oracle Test Lab, Oracle Guided Learning |
| Transition | Cutover, go-live, hypercare | Oracle Cloud Provisioning, Oracle Support |
| Optimize | Continuous improvement, quarterly updates, adoption | Oracle Cloud Customer Connect, Release Readiness |

## Integration Patterns

| Pattern | Oracle Technology | Use Case |
|---|---|---|
| API-based (sync) | OIC REST/SOAP Adapters + API Gateway | Real-time data retrieval and updates |
| Event-driven (async) | OIC Events + OCI Streaming | Business event notification (e.g., PO approved) |
| File-based (batch) | OIC FTP Adapter + FBDI (File-Based Data Import) | Bulk data loads, legacy system integration |
| Data replication | Oracle GoldenGate | Real-time data replication for analytics or DR |
| Prebuilt integration | OIC Recipes and Accelerators | 400+ prebuilt integration patterns for common scenarios |
| B2B / EDI | Oracle B2B (OIC) | EDI document exchange with trading partners |

## Licensing & Editions

| Edition | Scope | Typical Use Case |
|---|---|---|
| Oracle Fusion Cloud ERP | SaaS, quarterly updates | Full finance and project management suite |
| Oracle Fusion Cloud HCM | SaaS, quarterly updates | Complete HR suite with country localizations |
| Oracle Fusion Cloud SCM | SaaS, quarterly updates | End-to-end supply chain management |
| Oracle CX Cloud | SaaS, modular licensing | Sales, Service, Marketing, Commerce (licensed separately) |
| Oracle EPM Cloud | SaaS, modular licensing | Planning, Consolidation, Narrative Reporting, Tax |
| OCI | Consumption-based (universal credits) | Infrastructure, AI services, data platform |
| Oracle Integration Cloud (OIC) | Subscription (messages/connections) | Integration and process automation |

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| Process is within Fusion Cloud standard capability | Use OOB Fusion module — configure, do not customize |
| Process needs citizen-developer application | Oracle APEX or Visual Builder Cloud Service |
| Process requires enterprise integration | Oracle Integration Cloud (OIC) with prebuilt adapters |
| Process involves AI/ML augmentation | Oracle AI embedded in Fusion + OCI AI Services |
| Analytics spans multiple Fusion modules | Oracle Fusion Analytics Warehouse (prebuilt) |
| Analytics requires custom data sources | Oracle Analytics Cloud + Autonomous Data Warehouse |
| Financial planning and consolidation needed | Oracle EPM Cloud |
| High-performance database workloads | Oracle Autonomous Database (ADW/ATP) |
| Security/compliance requirement | OCI Cloud Guard + Data Safe + Access Governance |
