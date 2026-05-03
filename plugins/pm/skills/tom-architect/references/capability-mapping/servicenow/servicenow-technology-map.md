---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3400
keywords: [technology-map, servicenow, tom-layers, capability-mapping, itsm, itom, csm, hrsd, app-engine, secops]
version: "1.0"
last_updated: "2026-03-28"
---

# ServiceNow Technology Map — TOM Capabilities to ServiceNow Stack

## Overview

This master mapping connects each TOM design layer to the recommended ServiceNow technology. ServiceNow is a platform-centric enterprise service management solution with deep strength in IT, employee, and customer workflows.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | Flow Designer | Workflow Editor (legacy) | Flow Designer for modern no-code automation; Workflow Editor for legacy compatibility |
| Process mining | ServiceNow Process Mining | Process Optimization | Native process mining for IT and business processes |
| Business rules | Business Rules Engine | Flow Designer (Decision Tables) | Business Rules for server-side logic; Decision Tables for declarative rules |
| Workflow orchestration | Flow Designer + Orchestration | IntegrationHub (cross-system) | Flow Designer for platform workflows; IntegrationHub for external system actions |
| Document processing | Document Intelligence (AI) | Partner OCR solutions | AI-powered document extraction for structured and unstructured documents |
| RPA | ServiceNow RPA (Automation Engine) | RPA Hub (third-party orchestration) | Native RPA for desktop automation; RPA Hub for managing UiPath, AA, Blue Prism |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | ServiceNow CMDB (Departments, Locations, Companies) | HR Service Delivery (Org chart) | CMDB for organizational entities; HRSD for people hierarchy |
| Role management | ServiceNow Access Control (Roles, ACLs, Groups) | Delegated Administration | Role-based access with granular ACL controls |
| Workforce planning | Not native to ServiceNow | Integration with Workday / SuccessFactors | ServiceNow is not an HCM platform; integrates with HR systems |
| Skills & competency | Agent Skills (for routing) | Integration with LMS | Skills-based routing for ITSM/CSM; full competency management via HR integration |
| Collaboration | Virtual Agent + Agent Workspace | Microsoft Teams / Slack integration | Virtual Agent for self-service; Agent Workspace for agent collaboration |
| Identity governance | ServiceNow IRM (Identity Risk Management) | Integration with SailPoint, Saviynt | IRM for access risk; integrate with specialized IGA platforms |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | ITSM (Incident, Request, Agent Workspace) | Now Assist for ITSM | Full ITSM service desk with AI-augmented resolution |
| ITSM | ServiceNow ITSM (Incident, Problem, Change, CMDB) | ITSM Professional/Enterprise | Core ITSM aligned to ITIL 4 practices |
| SLA management | SLA Engine (Definitions, Conditions, Schedules) | Service Level Management module | Configurable SLA tracking with escalation and breach alerts |
| Knowledge management | Knowledge Management (Knowledge Bases, Articles) | AI Search, Now Assist | Structured knowledge with AI-powered search and recommendations |
| Self-service portal | Service Portal + Employee Center | Virtual Agent, Service Catalog | Service Portal for external; Employee Center for internal unified experience |
| Service analytics | Performance Analytics | Reporting, Dashboards | PA for trend analysis and KPIs; native dashboards for operational reporting |

## Layer 4: Technology

### IT Service Management (ITSM)

| TOM Capability | Primary Technology | ITIL Practice | Notes |
|---|---|---|---|
| Incident Management | ITSM Incident | Incident Management | Detect, log, classify, resolve, and close incidents |
| Problem Management | ITSM Problem | Problem Management | Root cause analysis, known errors, workarounds |
| Change Management | ITSM Change | Change Enablement | Normal, standard, emergency change with CAB support |
| Request Fulfillment | ITSM Request + Service Catalog | Service Request Management | Catalog items, record producers, approval workflows |
| Asset Management | ITSM Asset Management (HAM, SAM) | IT Asset Management | Hardware and software asset lifecycle, license compliance |
| CMDB | Configuration Management Database | Configuration Management | CI discovery, relationships, service mapping |
| SLA Management | SLA Definitions + Conditions | Service Level Management | Multi-condition SLAs with escalation rules |
| Release Management | ITSM Release | Release Management | Release planning, deployment tracking, rollback |

### IT Operations Management (ITOM)

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Discovery | ITOM Discovery + Service Mapping | Automated CI discovery and application dependency mapping |
| Event Management | ITOM Event Management | Consolidate events from monitoring tools, correlate to CIs, auto-create incidents |
| Cloud Management | ITOM Cloud Management (Cloud Insights) | Multi-cloud visibility, cost optimization, governance |
| Health Log Analytics | ITOM Health Log Analytics | ML-powered log analysis for anomaly detection and root cause |
| AIOps | ITOM AIOps | Alert correlation, noise reduction, predictive alerting |

### Customer Service Management (CSM)

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Case Management | CSM Cases + Accounts + Contacts | Customer case lifecycle with account context |
| Omnichannel | CSM Omni-Channel (Phone, Chat, Email, Portal, Social) | Unified agent desktop across all channels |
| Communities | CSM Communities | Customer self-service community with forums and knowledge |
| Field Service | Field Service Management | Work order dispatch, scheduling, mobile app for technicians |
| Customer Portal | CSM Customer Portal (Service Portal) | Branded self-service portal for B2B customers |
| Proactive Service | CSM Proactive Customer Service Operations | Monitor customer products/services and create cases proactively |

### HR Service Delivery (HRSD)

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Employee Center | Employee Center (unified portal) | Single destination for employee services, knowledge, and tasks |
| HR Case Management | HRSD Case Management | Employee inquiries, lifecycle events, sensitive cases |
| Knowledge (HR) | HRSD Knowledge Management | HR policies, FAQs, benefits guides |
| Onboarding/Offboarding | HRSD Lifecycle Events (Enterprise Onboarding) | Guided onboarding journeys with cross-department task orchestration |
| Document Management | HRSD Document Management | Employee document collection, verification, and storage |
| Employee Journey | HRSD Employee Journey Management | Design and manage key employee moments (promotion, relocation, parental leave) |

### App Engine & Platform

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Low-code development | App Engine Studio | Drag-and-drop app builder for custom applications |
| Flow automation | Flow Designer | No-code flow automation with actions, subflows, and triggers |
| Integration | IntegrationHub + Spokes | Prebuilt spokes for common systems (SAP, Workday, Salesforce, Azure, AWS) |
| API management | ServiceNow API (REST/SOAP, Scripted REST) | Build and expose APIs on the ServiceNow platform |
| Mobile | ServiceNow Mobile (Now Mobile, Mobile Agent) | Native mobile apps for self-service and agent workflows |
| UI development | UI Builder + Service Portal | UI Builder for modern workspace experiences; Service Portal for portals |

### Strategic Portfolio Management

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Project Portfolio Management | SPM (Project, Program, Portfolio) | Demand, project, resource, and portfolio management |
| ITBM | SPM (Application Portfolio Management) | Application rationalization, technology roadmaps |
| Innovation Management | SPM Innovation Management | Idea capture, evaluation, and pipeline management |
| Resource Management | SPM Resource Management | Resource capacity planning and allocation |

### Security Operations

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Security Incident Response | SecOps Security Incident Response | SOAR-based incident response with playbooks |
| Vulnerability Response | SecOps Vulnerability Response | Prioritize and remediate vulnerabilities by business impact |
| Threat Intelligence | SecOps Threat Intelligence | Aggregate threat feeds and correlate to CMDB/vulnerabilities |
| Configuration Compliance | SecOps Configuration Compliance | Assess infrastructure against security benchmarks (CIS, DISA) |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Enterprise analytics | Performance Analytics | Reporting, Dashboards | PA for trend KPIs and benchmarks; native reporting for lists and charts |
| KPI dashboards | Performance Analytics Dashboards | Now Mobile dashboards | Configurable KPI widgets with drill-down and trend analysis |
| Predictive analytics | Now Intelligence (Predictive Intelligence) | AI Search | Predictive classification, similarity matching, regression |
| Data integration | IntegrationHub + Data Sources | CMDB data imports, LDAP | IntegrationHub for real-time; data sources for batch imports |
| Data governance | CMDB Health + Data Certification | Service Mapping validation | CMDB Health for CI data quality; Data Certification for periodic review |
| Reporting | Report Builder + Scheduled Reports | Report Designer (advanced) | Native report builder with scheduling and distribution |
| Real-time monitoring | ITOM Event Management + Dashboards | Health Log Analytics | Real-time infrastructure and application monitoring |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Access governance | ServiceNow IRM (Access Risk) | Role-based ACLs, Access Analyzer | IRM for access risk analysis; ACLs for enforcement |
| Risk management | Integrated Risk Management (IRM) | GRC applications | Enterprise risk register, risk assessment, treatment plans |
| Compliance management | IRM Compliance Management | Audit Management | Policy management, control testing, compliance reporting |
| Security monitoring | SecOps + Event Management | SIEM integration (Splunk, Sentinel) | SecOps for security workflow; integrate with SIEM for detection |
| Data protection | Data Classification + Encryption | ServiceNow Edge Encryption | Classify and protect sensitive data on the platform |
| Audit & logging | System Logs + Audit Trail | Transaction Logs | Comprehensive audit trail for all record and configuration changes |

---

## ITIL Process-to-ServiceNow Module Mapping

| ITIL 4 Practice | ServiceNow Module | Key Features |
|---|---|---|
| Incident Management | ITSM Incident | Auto-assignment, major incident workflows, parent-child incidents |
| Problem Management | ITSM Problem | Root cause analysis, known error database, problem tasks |
| Change Enablement | ITSM Change | Risk assessment, CAB workbench, conflict detection, deployment windows |
| Service Request Management | ITSM Service Catalog + Request | Catalog items, record producers, approval policies |
| Knowledge Management | Knowledge Management | Article lifecycle, feedback, versioning, AI search |
| Service Level Management | SLA Engine | SLA definitions, OLA, underpinning contracts |
| Configuration Management | CMDB | CI classes, relationships, discovery, reconciliation |
| IT Asset Management | HAM + SAM | Hardware lifecycle, software license compliance, normalization |
| Service Desk | Agent Workspace | Unified agent experience, AI-assisted resolution |
| Monitoring and Event Management | ITOM Event Management | Alert consolidation, correlation rules, auto-remediation |
| Release Management | ITSM Release | Release planning, build, test, deploy tracking |
| Continual Improvement | Continual Improvement Management | Improvement register, ROI tracking |

## ServiceNow Implementation Methodology

| Phase | Key Activities | ServiceNow Tools |
|---|---|---|
| Align | Executive alignment, business case, stakeholder mapping | ServiceNow Impact, Customer Success |
| Plan | Scope, architecture, data strategy, governance | Platform Architecture, Instance Strategy |
| Build | Configuration, development, integration, data migration | App Engine Studio, Flow Designer, IntegrationHub |
| Validate | Testing (unit, SIT, UAT, performance), training | Automated Test Framework (ATF), Knowledge |
| Deploy | Go-live, data cutover, change management | Update Sets, Application Repository |
| Operate | Monitoring, continuous improvement, upgrades | Performance Analytics, Instance Health, Now Support |

## Integration Patterns

| Pattern | ServiceNow Technology | Use Case |
|---|---|---|
| API-based (sync) | REST/SOAP APIs + Scripted REST | Real-time data exchange with external systems |
| Event-driven (async) | IntegrationHub Events + Flow Triggers | React to external events (e.g., monitoring alert, HR system change) |
| Spoke-based (prebuilt) | IntegrationHub Spokes | Prebuilt connectors for SAP, Workday, Azure, AWS, Jira, Slack |
| File-based (batch) | Import Sets + Transform Maps | Bulk data imports from CSV, XML, JDBC sources |
| Mid Server | MID Server (on-prem agent) | Secure connectivity to on-premises systems and infrastructure |
| CMDB integration | Discovery + Service Mapping | Automated infrastructure and application topology discovery |

## Licensing & Editions

| Edition | Scope | Typical Use Case |
|---|---|---|
| ITSM Standard | Incident, Problem, Change, Request, SLA | Basic ITSM aligned to ITIL |
| ITSM Professional | Standard + Virtual Agent, Predictive Intelligence, Performance Analytics | AI-enhanced ITSM |
| ITSM Enterprise | Professional + Workforce Optimization, Process Mining, Continual Improvement | Full ITSM transformation |
| ITOM Visibility | Discovery, Service Mapping, CMDB | Infrastructure visibility and CMDB population |
| ITOM Health | Visibility + Event Management, Health Log Analytics, AIOps | Proactive IT operations |
| CSM | Case Management, Omni-Channel, Communities, Knowledge | Customer service management |
| HRSD | Employee Center, Case Management, Knowledge, Lifecycle Events | HR service delivery |
| App Engine | App Engine Studio, Flow Designer, IntegrationHub | Custom application development |
| IRM / GRC | Risk, Compliance, Audit, Policy | Governance, risk, and compliance |
| SecOps | Security Incident Response, Vulnerability Response | Security operations and response |

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| IT service management (ITSM) | ServiceNow ITSM — incident, problem, change, request |
| IT operations monitoring | ServiceNow ITOM — discovery, events, AIOps, cloud management |
| Customer service (B2B) | ServiceNow CSM — case management, omnichannel, communities |
| Employee service experience | ServiceNow HRSD — Employee Center, case management, lifecycle events |
| Custom enterprise workflows | App Engine Studio + Flow Designer |
| Enterprise integration | IntegrationHub with prebuilt Spokes |
| Security operations | ServiceNow SecOps — incident response, vulnerability management |
| Risk and compliance | ServiceNow IRM — risk register, compliance, audit management |
| Project and portfolio management | ServiceNow SPM — demand, project, resource, portfolio |
| AI-augmented service | Now Assist + Virtual Agent + Predictive Intelligence |
