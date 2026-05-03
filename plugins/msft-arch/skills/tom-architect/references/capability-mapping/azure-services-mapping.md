---
category: "capability-mapping"
loading_priority: 3
tokens_estimate: 1600
keywords: [azure, integration, infrastructure, networking, security, monitoring, identity, entra-id, logic-apps, apim, service-bus, event-grid]
version: "1.0"
last_updated: "2026-03-23"
---

# Azure Services Mapping: Infrastructure & Integration

## Overview

Maps TOM environment architecture and integration layer requirements to Azure services. Provides patterns for integrating D365, Power Platform, and custom workloads on Azure.

---

## Integration Layer

| TOM Requirement | Azure Service | When to Use | Key Features |
|---|---|---|---|
| Orchestration & workflow | Azure Logic Apps (Standard) | Multi-step integration workflows, B2B, EDI | 1,000+ connectors, visual designer, built-in retry/error handling, stateful workflows |
| Lightweight event processing | Azure Functions | Event-driven compute, data transformation, API backends | Consumption/Premium plans, durable functions for stateful orchestration, language flexibility (C#, Python, JS, Java) |
| API management | Azure API Management (APIM) | Centralized API gateway for internal and external APIs | Rate limiting, authentication, developer portal, analytics, versioning, policy engine |
| Asynchronous messaging | Azure Service Bus | Reliable message queuing, pub/sub, guaranteed delivery | Queues, topics/subscriptions, sessions, dead-letter, transactions, duplicate detection |
| Event routing | Azure Event Grid | Reactive event-driven architecture, event fan-out | System topics (Azure resource events), custom topics, event domains, push delivery, pull delivery |
| File-based integration | Azure Blob Storage + Event Grid | Batch file exchange, SFTP, legacy file drops | SFTP support (Blob Storage), event triggers on file arrival, lifecycle management |
| EDI / B2B | Azure Logic Apps (B2B) + Integration Account | Trading partner management, EDI X12, EDIFACT | AS2/X12/EDIFACT, partner agreements, maps, schemas, certificates |

### Integration Architecture Patterns

**Pattern: Hub-and-Spoke Integration**
- APIM as central gateway for all APIs
- Logic Apps for orchestration workflows
- Service Bus for decoupled messaging between D365/custom systems
- Event Grid for real-time event distribution

**Pattern: D365 F&O Integration**
- OData APIs (synchronous CRUD)
- Data Management Framework (DMF) recurring integrations (batch file-based)
- Business Events (event-driven push notifications)
- Virtual Entities (real-time read from external Dataverse)
- Dual-Write (bidirectional sync between F&O and Dataverse)

**Pattern: D365 CE / Dataverse Integration**
- Dataverse Web API (REST, synchronous)
- Dataverse connectors in Power Automate / Logic Apps
- Webhooks and Service Endpoints (event-driven push)
- Fabric Link (Dataverse to OneLake for analytics)

---

## Data Storage

| TOM Requirement | Azure Service | When to Use |
|---|---|---|
| Relational (transactional) | Azure SQL Database | Custom app backends, structured transactional data |
| Relational (managed instance) | Azure SQL Managed Instance | Lift-and-shift of SQL Server, cross-database queries |
| NoSQL (document/graph) | Azure Cosmos DB | Global distribution, multi-model (document, graph, key-value, column), low-latency |
| Object / blob storage | Azure Blob Storage | Files, documents, media, backups, data lake raw zone |
| Data lake | Azure Data Lake Storage Gen2 (ADLS) | Large-scale analytics, hierarchical namespace, Hadoop-compatible |
| Cache | Azure Cache for Redis | Session state, application caching, real-time leaderboards |

---

## Identity & Access

| TOM Requirement | Azure Service | When to Use |
|---|---|---|
| Enterprise identity | Microsoft Entra ID | SSO, MFA, conditional access for all M365/D365/Azure apps |
| External identity | Entra External ID (B2C) | Customer and partner authentication (social login, local accounts) |
| Workload identity | Managed Identity (system/user-assigned) | Azure resource-to-resource auth without credentials |
| Privileged access | Entra ID PIM (Privileged Identity Management) | Just-in-time admin access, approval-based role activation |
| Permissions management | Entra Permissions Management | Multi-cloud (Azure, AWS, GCP) permissions discovery and right-sizing |
| Certificate management | Azure Key Vault | Secrets, keys, and certificate lifecycle management |

---

## Networking

| TOM Requirement | Azure Service | When to Use |
|---|---|---|
| Network isolation | Azure Virtual Network (VNet) | Isolate workloads, subnets, NSGs for micro-segmentation |
| Private connectivity | Private Endpoints | Access PaaS services (SQL, Storage, Service Bus) over private IP |
| Hybrid connectivity | ExpressRoute / VPN Gateway | Connect on-premises to Azure; ExpressRoute for dedicated, VPN for internet-based |
| Global load balancing | Azure Front Door | Global HTTP(S) routing, WAF, CDN, SSL offload |
| Regional load balancing | Azure Application Gateway | Regional L7 load balancer, WAF, URL-based routing |
| DNS management | Azure DNS | Public and private DNS zones |
| DDoS protection | Azure DDoS Protection | Volumetric attack mitigation for public-facing services |

---

## Monitoring & Operations

| TOM Requirement | Azure Service | When to Use |
|---|---|---|
| Application monitoring | Application Insights | APM for custom apps (request tracing, dependency mapping, exceptions, performance) |
| Infrastructure monitoring | Azure Monitor | Metrics, alerts, action groups for Azure resources |
| Log aggregation | Log Analytics Workspace | Centralized log collection (KQL queries), integration with Sentinel |
| Workbook dashboards | Azure Monitor Workbooks | Operational dashboards combining metrics, logs, and parameters |
| Cost management | Microsoft Cost Management | Budget alerts, cost analysis, advisor recommendations |
| Service health | Azure Service Health | Planned maintenance notifications, incident tracking |

---

## Security

| TOM Requirement | Azure Service | When to Use |
|---|---|---|
| Secret management | Azure Key Vault | Store secrets, connection strings, certificates, keys |
| SIEM | Microsoft Sentinel | Security event aggregation, detection rules, incident response, SOAR |
| Cloud security posture | Microsoft Defender for Cloud | CSPM, vulnerability assessment, regulatory compliance |
| Endpoint security | Microsoft Defender for Endpoint | EDR, threat detection, automated investigation |
| Email / collaboration security | Microsoft Defender for Office 365 | Anti-phishing, safe attachments, safe links |
| Identity protection | Entra ID Protection | Risk-based conditional access, risky user/sign-in detection |
| Data governance | Microsoft Purview | Data catalog, data lineage, sensitivity labels, compliance controls |
| Compliance management | Microsoft Purview Compliance Manager | GDPR/SOX/HIPAA compliance assessments, improvement actions, compliance score |
| Data loss prevention | Microsoft Purview DLP | Detect and prevent data exfiltration across M365, endpoints, and cloud apps |

---

## TOM Environment Architecture Pattern

### Recommended Azure Landing Zone for D365 + Custom Workloads

```
Management Group Hierarchy:
  Tenant Root Group
    ├── Platform
    │   ├── Identity (Entra ID, PIM)
    │   ├── Management (Monitor, Sentinel, Log Analytics)
    │   └── Connectivity (Hub VNet, ExpressRoute, DNS, Firewall)
    └── Landing Zones
        ├── Corp (D365 integration workloads, internal APIs)
        │   ├── Integration-Prod (Logic Apps, APIM, Service Bus)
        │   ├── Integration-NonProd
        │   ├── Custom-Apps-Prod (AKS, App Service, Functions)
        │   └── Custom-Apps-NonProd
        └── Online (External-facing, Power Pages, B2C)
            ├── External-Prod
            └── External-NonProd
```

### Environment Mapping

| TOM Environment | Azure Implementation |
|---|---|
| Development | Non-prod subscription, dev resource groups, Entra dev tenant or B2C dev |
| Test / QA | Non-prod subscription, separate resource groups, test data |
| Pre-production | Prod-like subscription, production-equivalent configuration |
| Production | Prod subscription, geo-redundancy, backup, DR |
| DR | Paired region, Azure Site Recovery, geo-redundant storage |
