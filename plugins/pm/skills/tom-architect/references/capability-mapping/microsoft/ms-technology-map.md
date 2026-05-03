---
category: "capability-mapping"
loading_priority: 1
tokens_estimate: 3200
keywords: [technology-map, microsoft, tom-layers, capability-mapping, d365, azure, power-platform, fabric, copilot, integration]
version: "1.0"
last_updated: "2026-03-23"
---

# Microsoft Technology Map — TOM Capabilities to Microsoft Stack

## Overview

This master mapping connects each TOM design layer to the recommended Microsoft technology. Use this as the primary lookup when translating a TOM capability requirement into a concrete solution component.

---

## Layer 1: Processes

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Process automation | Power Automate (cloud flows, desktop flows) | Azure Logic Apps, Azure Functions | Power Automate for business-user flows; Logic Apps for enterprise integration patterns; Functions for event-driven microservices |
| Process mining | Power Automate Process Mining (Minit) | Celonis integration via connectors | Native process mining in Power Platform; Celonis for advanced multi-system mining |
| Business rules | D365 Business Rules Engine | Power Fx (Power Apps), Azure Functions | D365 rules for entity-level logic; Power Fx for canvas/model-driven apps; Functions for complex orchestration |
| Workflow orchestration | Power Automate (approvals, business process flows) | Azure Durable Functions | BPFs for guided processes in D365/model-driven apps; Durable Functions for long-running stateful workflows |
| Document processing | AI Builder (document processing) | Azure AI Document Intelligence | AI Builder for citizen-developer scenarios; Azure AI for high-volume or custom extraction |
| RPA | Power Automate Desktop | — | Attended and unattended desktop flows for legacy system automation |

## Layer 2: Organization

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Org structure management | D365 Human Resources | Entra ID, Microsoft Teams | D365 HR for formal hierarchy; Entra ID for directory; Teams for operational org |
| Role management | D365 Security Roles | Entra ID Groups, PIM | D365 roles for application RBAC; Entra groups for platform RBAC; PIM for just-in-time privileged access |
| Workforce planning | D365 HR Workforce Planning | Power BI workforce analytics | D365 HR for headcount planning; Power BI for scenario modeling and dashboards |
| Skills & competency | D365 HR (Skills, Certificates) | Viva Learning, LinkedIn Learning | D365 HR for formal skill tracking; Viva for learning journeys |
| Collaboration | Microsoft Teams | SharePoint, Viva Engage | Teams for real-time collaboration; SharePoint for document management; Viva Engage for communities |
| Identity governance | Entra ID Governance | Entra Permissions Management | Lifecycle workflows, access reviews, entitlement management |

## Layer 3: Service

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Service desk | D365 Customer Service | Power Virtual Agents (Copilot Studio) | D365 CS for case management and routing; Copilot Studio for self-service deflection |
| ITSM | Power Platform + ServiceNow connector | D365 Customer Service (internal) | ServiceNow connector for existing ITSM investments; D365 CS for greenfield internal service |
| SLA management | D365 SLA Engine | Power Automate escalations | D365 native SLA tracking with entitlements; Power Automate for custom escalation workflows |
| Knowledge management | D365 Knowledge Base | SharePoint, Copilot Studio | D365 KB for structured articles; SharePoint for document-centric knowledge; Copilot Studio for conversational retrieval |
| Self-service portal | Power Pages | D365 Customer Self-Service Portal | Power Pages for custom external portals; D365 portal template for accelerated deployment |
| Service analytics | Power BI (embedded in D365 CS) | Fabric Real-Time Intelligence | Power BI for operational dashboards; Fabric KQL for real-time service metrics |

## Layer 4: Technology

### ERP & CRM

| TOM Capability | Primary Technology | Tier | Notes |
|---|---|---|---|
| Enterprise Finance & SCM | D365 Finance & Operations | Tier 1 ERP | Multi-entity, multi-currency, manufacturing, warehouse |
| SMB Finance & Operations | D365 Business Central | Tier 2 ERP | Mid-market, rapid deployment, AppSource ecosystem |
| Sales management | D365 Sales | CRM | Lead-to-cash, opportunity management, forecasting |
| Customer service | D365 Customer Service | CRM | Case management, omnichannel, knowledge base |
| Field service | D365 Field Service | CRM | Work orders, scheduling, IoT integration |
| Project management | D365 Project Operations | CRM + ERP bridge | Project-centric delivery, time/expense, resource management |

### Low-Code & Integration

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Citizen applications | Power Apps (model-driven for data, canvas for UX) | Model-driven for CRUD on Dataverse; canvas for custom UX and mobile |
| External portals | Power Pages | Authenticated and anonymous external-facing sites |
| Integration platform | Azure Integration Services | Logic Apps (orchestration), APIM (API management), Service Bus (messaging), Event Grid (events) |
| API management | Azure API Management | Centralized API gateway, developer portal, throttling, analytics |
| Event-driven architecture | Azure Event Grid + Service Bus | Event Grid for reactive events; Service Bus for reliable messaging |

### AI & Intelligent Automation

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Generative AI | Azure OpenAI Service | GPT-4o, GPT-o3, embeddings, fine-tuning |
| Custom agents | Copilot Studio | No-code/low-code agent builder with plugin extensibility |
| AI orchestration | Azure AI Foundry (Semantic Kernel) | Custom model orchestration, RAG patterns, multi-agent |
| Machine learning | Azure Machine Learning | MLOps, training, deployment, responsible AI |
| Cognitive services | Azure AI Services | Vision, speech, language, decision |

### Infrastructure

| TOM Capability | Primary Technology | Notes |
|---|---|---|
| Container orchestration | Azure Kubernetes Service (AKS) | Enterprise Kubernetes for microservices |
| Serverless containers | Azure Container Apps | Event-driven containerized apps without K8s management |
| Serverless compute | Azure Functions | Event-driven, consumption-based compute |
| Virtual machines | Azure Virtual Machines | IaaS for lift-and-shift or specialized workloads |

## Layer 5: Data & Analytics

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Enterprise analytics | Microsoft Fabric | Power BI Premium | Fabric for unified analytics; Power BI Premium for report-centric orgs |
| KPI dashboards | Power BI (DirectLake over Fabric Lakehouse) | Power BI (Import/DirectQuery) | DirectLake for best performance; Import for offline; DirectQuery for real-time |
| Operational reporting | Power BI Paginated Reports | SSRS (legacy) | Paginated for pixel-perfect, printable reports |
| Data engineering | Fabric Spark Notebooks | Azure Databricks | Fabric Spark for unified platform; Databricks for advanced ML/engineering |
| Data warehousing | Fabric Data Warehouse (T-SQL) | Azure Synapse (legacy) | Fabric DW for new workloads; Synapse for existing investments |
| MDM | Profisee on Azure | Informatica MDM, Fabric OneLake | Profisee for active MDM; OneLake for passive data virtualization |
| Data governance | Microsoft Purview | Fabric lineage, Unity Catalog | Purview for enterprise-wide cataloging and classification |
| Real-time analytics | Fabric Real-Time Intelligence (KQL) | Azure Data Explorer | Fabric RTI for streaming analytics; ADX for dedicated clusters |
| Data ingestion | Fabric Data Factory | Azure Data Factory | Fabric DF for OneLake-native; ADF for Azure-native pipelines |
| D365 data access | Fabric Mirroring (D365 to OneLake) | Synapse Link, Data Export Service | Mirroring preferred for near-real-time replication |

## Layer 6: Governance

| TOM Capability | Primary Technology | Secondary / Alternative | Notes |
|---|---|---|---|
| Security monitoring | Microsoft Sentinel | Defender for Cloud | Sentinel for SIEM; Defender for CSPM |
| Threat protection | Microsoft Defender (Endpoint, Identity, O365) | Third-party EDR | Defender suite for comprehensive XDR |
| Identity security | Entra ID (Conditional Access, MFA) | Entra Permissions Management | Conditional Access for adaptive policies; Permissions Management for CIEM |
| Compliance management | Microsoft Purview Compliance Manager | — | Compliance assessments, regulatory templates, improvement actions |
| Data classification | Microsoft Purview Information Protection | — | Sensitivity labels, DLP policies, encryption |
| Policy enforcement | Azure Policy | Intune (device), Conditional Access (identity) | Azure Policy for resource governance; Intune for endpoint; CA for access |
| Audit & logging | Azure Monitor + Log Analytics | Microsoft 365 Audit Log | Centralized log aggregation and analysis |

---

## Decision Matrix Summary

| Decision Factor | Recommended Approach |
|---|---|
| Process is within D365 standard capability | Use OOB D365 module — avoid custom build |
| Process needs citizen-developer automation | Power Platform (Power Apps + Power Automate) |
| Process requires enterprise integration | Azure Integration Services (Logic Apps + APIM + Service Bus) |
| Process involves AI/ML augmentation | Azure OpenAI + Copilot Studio for agent layer |
| Analytics need spans multiple data sources | Microsoft Fabric unified lakehouse |
| Reporting is operational and paginated | Power BI Paginated Reports |
| Security/compliance requirement | Microsoft Purview + Sentinel + Defender |
| External user portal needed | Power Pages or D365 Portal template |
| High-throughput event processing | Event Grid + Service Bus + Functions |
| Custom container workloads | AKS (complex) or Container Apps (simple) |
