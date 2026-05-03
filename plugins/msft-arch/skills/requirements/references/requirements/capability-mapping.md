---
category: requirements
loading_priority: 2
tokens_estimate: 3500
keywords: [capability mapping, stack comparison, Power Platform, Azure PaaS, AKS, containers, Dynamics 365, business process, data storage, integration, AI, security, DevOps, ALM, escalation, boundary]
version: 1.0
last_updated: 2026-03-21
---

# Capability Mapping Matrix

## Purpose

This reference maps requirement types to specific platform capabilities across all four Microsoft stacks. Use it during fit-gap analysis to identify which stack best addresses each capability area, and to understand the escalation boundaries between stacks.

## Stack Legend

| Stack | Label | Primary Platform |
|---|---|---|
| A | Low-Code | Power Platform + Dataverse |
| B | PaaS | Azure PaaS Services |
| C | Containers | AKS + Container Workloads |
| D | D365 | Dynamics 365 Applications |

---

## Business Process Automation

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Simple workflows | Power Automate cloud flows | Logic Apps (Standard) | DAPR workflows | D365 workflows |
| Complex orchestration | Power Automate with child flows | Durable Functions, Logic Apps | Custom orchestrators in containers, Temporal | D365 business process flows |
| Business rules | Dataverse business rules | Azure Functions with rules engine | Custom rules engine in containers | D365 plugins, business rules |
| Scheduled processes | Power Automate scheduled flows | Azure Functions timer triggers, WebJobs | CronJobs in Kubernetes | D365 batch jobs, SysOperation framework |
| Human-in-the-loop | Power Automate approvals | Custom approval UI + Durable Functions | Custom approval service | D365 workflow approvals |
| RPA | Power Automate Desktop flows | N/A (use Stack A) | N/A (use Stack A) | N/A (use Stack A) |

**Boundary Guidance**:
- When Power Automate flows exceed 500 actions or run longer than 30 minutes, escalate to **Stack B** (Logic Apps or Durable Functions)
- When orchestration requires custom retry policies, compensation transactions, or saga patterns, escalate to **Stack B or C**
- When processes are standard ERP/CRM workflows (order-to-cash, procure-to-pay, lead-to-opportunity), prefer **Stack D**

---

## Data Storage and Management

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Relational data | Dataverse | Azure SQL, Azure Database for PostgreSQL | Container-hosted SQL, PostgreSQL | Dataverse, D365 F&O SQL database |
| Document storage | SharePoint, Dataverse file columns | Azure Blob Storage, Data Lake Storage | Container-mounted volumes, MinIO | SharePoint, Dataverse notes/attachments |
| NoSQL / key-value | N/A | Cosmos DB (multiple APIs), Table Storage | MongoDB, Redis, Cassandra in containers | N/A |
| Search | Dataverse Relevance Search | Azure AI Search (Cognitive Search) | Elasticsearch/OpenSearch in containers | D365 Relevance Search |
| Data lake / warehouse | N/A | Azure Synapse Analytics, Data Lake Gen2 | Container-hosted Spark, Trino | Azure Synapse Link for Dataverse/D365 |
| Caching | N/A | Azure Cache for Redis | Redis sidecar, in-memory caches | N/A |
| Data integration | Dataflows (Power Query Online) | Azure Data Factory, Synapse Pipelines | Custom ETL in containers, Airbyte | Dual-write, Virtual Entities, Data Export Service |

**Boundary Guidance**:
- When Dataverse storage exceeds 10 GB or row counts exceed 10 million, evaluate **Stack B** (Azure SQL or Cosmos DB) for the data tier
- When sub-millisecond read latency is required, escalate to **Stack B** (Redis Cache) or **Stack C** (in-process cache)
- When polyglot persistence is needed (relational + document + graph + search), escalate to **Stack B or C**

---

## User Interface

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Data-centric forms | Model-driven apps | Custom web app (React/Angular/Blazor on App Service) | Container-hosted SPA | D365 Unified Interface |
| Custom UI | Canvas apps | Custom web app with full design freedom | Micro-frontends in containers | PCF controls, custom web resources |
| Portal / external users | Power Pages | Custom web app + Azure AD B2C | Container-hosted portal | D365 Customer Self-Service portal |
| Mobile | Power Apps mobile app | Custom PWA or React Native on App Service | Container-hosted mobile BFF | D365 mobile app |
| Embedded analytics | Power BI embedded in apps | Power BI Embedded service, custom charts | Container-hosted BI tools (Metabase, Grafana) | D365 embedded Power BI, analytical workspaces |
| Conversational UI | Copilot Studio | Azure Bot Service + Azure OpenAI | Custom bot in containers | D365 Copilot, Copilot Studio |

**Boundary Guidance**:
- When Canvas apps exceed 500 controls or require pixel-perfect responsive design across 5+ breakpoints, escalate to **Stack B** (custom web app)
- When the UI requires complex state management, real-time collaboration, or rich animations, escalate to **Stack B or C**
- When the application is a standard CRM/ERP form-based experience, prefer **Stack D** Unified Interface

---

## Integration

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| API consumption | Power Automate connectors (900+), custom connectors | APIM, Logic Apps connectors, HttpClient in Functions | REST/gRPC clients in containers, DAPR service invocation | Dataverse Web API, D365 OData endpoints |
| API exposure | Custom connectors, Dataverse Web API | APIM-fronted APIs, Azure Functions HTTP triggers | Container-hosted APIs with ingress | D365 OData endpoints, custom APIs |
| Event-driven | Dataverse triggers, Power Automate triggers | Event Grid, Service Bus, Event Hubs | DAPR pub/sub, NATS, Kafka in containers | D365 event framework, webhooks, Azure Service Bus plugin |
| Messaging / queues | N/A | Service Bus queues/topics, Storage Queues | RabbitMQ, Kafka, DAPR bindings | Service Bus integration for async patterns |
| File transfer | SharePoint connectors, FTP connector | Azure Blob triggers, SFTP on Blob Storage | Container-hosted SFTP, file watchers | D365 Data Management Framework (DMF) |
| B2B / EDI | N/A | Logic Apps Integration Account (AS2, X12, EDIFACT) | Container-hosted EDI solutions | D365 F&O Electronic Messaging, EDI add-ons |

**Boundary Guidance**:
- When Power Automate connector throughput limits are hit (>100 calls/min for standard connectors), escalate to **Stack B** (Logic Apps or direct API calls)
- When event processing requires guaranteed ordering, exactly-once delivery, or >10,000 events/second, escalate to **Stack B** (Event Hubs + Stream Analytics) or **Stack C** (Kafka)
- When B2B/EDI is required, escalate to **Stack B** (Logic Apps Integration Account) or **Stack D** (D365 F&O EDI)

---

## AI and Analytics

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Pre-built AI models | AI Builder (form processing, object detection, sentiment, prediction) | Azure AI Services (Vision, Language, Speech, Decision) | Container-hosted AI models | D365 Copilot, Customer Insights AI |
| Custom AI / ML | AI Builder custom models | Azure Machine Learning, Azure OpenAI Service | ML model serving in containers (TensorFlow Serving, TorchServe) | D365 AI predictions, Customer Insights custom models |
| Generative AI | Copilot Studio, AI Builder GPT | Azure OpenAI Service (GPT-4, embeddings, DALL-E) | Self-hosted LLMs in containers (vLLM, Ollama) | D365 Copilot features |
| BI and reporting | Power BI (included with many licenses) | Power BI Premium, Azure Synapse Analytics | Grafana, Metabase, Superset in containers | D365 Power BI embedded, analytical workspaces |
| Streaming analytics | N/A | Azure Stream Analytics, Event Hubs + Functions | Flink, Spark Streaming in containers | N/A |
| Data science notebooks | N/A | Azure Machine Learning notebooks, Synapse notebooks | JupyterHub in containers | N/A |

**Boundary Guidance**:
- When AI Builder model types do not cover the use case, escalate to **Stack B** (Azure AI Services or Azure ML)
- When model inference requires GPU acceleration or custom model architectures, escalate to **Stack C** (GPU node pools in AKS)
- When AI features are standard D365 patterns (sales forecasting, customer churn, product recommendations), prefer **Stack D**

---

## Security and Identity

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Authentication | Entra ID (SSO, MFA) | Entra ID + Azure AD B2C for external users | Workload identity, Entra ID integration | Entra ID, D365 security |
| Authorization | Dataverse security roles, business units, teams | Azure RBAC, custom RBAC in application code | Kubernetes RBAC, pod security policies, OPA/Gatekeeper | D365 security roles, business units, field-level security |
| Network security | Managed connectors DLP policies | Private endpoints, VNet integration, NSGs, WAF, Azure Firewall | Network policies (Calico/Cilium), service mesh mTLS, ingress WAF | Managed by Microsoft (SaaS model) |
| Secret management | Environment variables (limited) | Azure Key Vault | Kubernetes Secrets, external secret operators, Key Vault CSI driver | D365 Key Vault integration |
| Encryption | Platform-managed encryption | Customer-managed keys, double encryption, Azure Confidential Computing | Encryption at pod level, Key Vault integration | Platform-managed encryption, customer-managed keys |
| DLP / data protection | Power Platform DLP policies | Microsoft Purview, Azure Information Protection | Custom DLP in application code | D365 DLP, Microsoft Purview |
| Threat detection | N/A | Microsoft Defender for Cloud, Sentinel | Defender for Containers, Falco in AKS | Defender for Cloud Apps |

**Boundary Guidance**:
- When DLP policies in Power Platform are insufficient for sensitive workloads, escalate to **Stack B** (Azure-level network and data controls)
- When zero-trust network segmentation with pod-level policies is required, escalate to **Stack C**
- When regulatory compliance requires full infrastructure control and audit, escalate to **Stack B or C**

---

## DevOps and ALM

| Capability | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Source control | Solution export/import, Power Platform CLI | Git (Azure Repos / GitHub) | Git (Azure Repos / GitHub) | Solution export/import, D365 solution management |
| CI/CD pipelines | Power Platform pipelines, managed environments | Azure DevOps Pipelines, GitHub Actions | GitOps (Flux, ArgoCD), GitHub Actions, Azure DevOps | Azure DevOps + D365 tools, LCS (F&O), AL pipelines (BC) |
| IaC | N/A (platform-managed) | ARM templates, Bicep, Terraform | Helm charts, Kustomize, Terraform (AKS infra) | N/A (SaaS-managed) |
| Environment management | Power Platform environments (dev/test/prod) | Azure subscriptions, resource groups, deployment slots | Kubernetes namespaces, cluster-per-environment | D365 environments, LCS environments (F&O) |
| Testing | Power Apps Test Studio, Test Engine | Azure Load Testing, custom test frameworks | Container-based test runners, chaos engineering (Chaos Mesh) | EasyRep, RSAT (F&O), custom test frameworks |
| Monitoring | Power Platform admin analytics | Application Insights, Azure Monitor, Log Analytics | Prometheus + Grafana, Azure Monitor for containers, OpenTelemetry | D365 telemetry, Application Insights integration |

**Boundary Guidance**:
- When Power Platform ALM requires branching strategies, PR reviews, or automated quality gates beyond solution checker, escalate to **Stack B** patterns (Git-based ALM with Power Platform CLI)
- When deployment requires blue-green, canary, or progressive rollout strategies, escalate to **Stack C** (Kubernetes deployment strategies, Flux/ArgoCD)
- When the solution includes both D365 and custom components, use a **hybrid ALM** approach combining D365 solution management with Azure DevOps pipelines

---

## Cross-Stack Escalation Summary

| Trigger Condition | From | To | Reason |
|---|---|---|---|
| Data volume > 10M rows or > 10 GB | Stack A | Stack B | Dataverse storage/performance limits |
| Concurrent users > 2,000 on custom UI | Stack A | Stack B | Canvas app performance limits |
| Flow complexity > 500 actions | Stack A | Stack B | Power Automate complexity limits |
| Need for private networking | Stack A | Stack B | Power Platform runs on shared infrastructure |
| Need for polyglot languages or runtimes | Stack B | Stack C | PaaS supports limited runtime stacks |
| Need for GPU workloads | Stack B | Stack C | GPU node pools in AKS |
| Sub-10ms latency requirements | Stack B | Stack C | Container co-location and custom networking |
| Standard ERP/CRM processes | Stack A/B/C | Stack D | D365 provides OOB business applications |
| ISV ecosystem for industry verticals | Stack A/B/C | Stack D | D365 AppSource has mature industry solutions |

Use this escalation summary during fit-gap analysis to determine whether a requirement pushes the solution beyond the current stack's capabilities and into the next tier.
