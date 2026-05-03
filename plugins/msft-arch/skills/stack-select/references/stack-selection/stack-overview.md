---
category: stack-selection
loading_priority: 1
tokens_estimate: 3200
keywords:
  - stack comparison
  - decision tree
  - cost analysis
  - scalability
  - governance
  - licensing
  - stack upgrade
  - combination rules
  - databricks
  - fabric
  - data platform
  - x++
version: "1.0"
last_updated: "2026-03-21"
---

# Stack Selection Overview

## Stack Comparison Matrix

The Microsoft technology estate organizes into four composable stacks. Each stack is additive: Stack B includes everything in Stack A, Stack C includes everything in Stack B, and Stack D combines with any of A, B, or C depending on integration needs.

### Cost Comparison

| Dimension | Stack A (Low-Code) | Stack B (Low-Code + PaaS) | Stack C (Containers) | Stack D (Dynamics 365) |
|---|---|---|---|---|
| Licensing | Per-user Power Platform licenses ($20-$40/user/month); Dataverse capacity-based | Stack A licenses + Azure consumption (pay-as-you-go or reserved) | Stack B costs + AKS cluster compute, container registry | Per-app D365 licenses ($65-$210/user/month) + platform costs from chosen sub-stack; X++ dev for F&O customization |
| Infrastructure | Fully managed by Microsoft; zero infrastructure cost beyond licensing | Moderate; App Service Plans, SQL DTUs, Function consumption units | High; node pool VMs, load balancers, persistent volumes, egress | Fully managed SaaS; infrastructure cost is embedded in license price |
| Development | Low; citizen developers can build. Pro dev cost only for complex customization | Medium; requires pro developers for Azure services, but Power Platform accelerates UI | High; requires container expertise, Kubernetes operators, DevOps engineers | Medium; functional consultants for config, pro devs for plugins and extensions |
| Total 3-Year TCO (100 users) | $150K-$300K | $300K-$600K | $500K-$1M | $400K-$900K (varies heavily by module mix) |

### Complexity Comparison

| Dimension | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Development complexity | Low. Declarative configuration, formula language (Power Fx), visual designers | Medium. Code-based Azure services alongside low-code. Requires API design skills | High. Dockerfile authoring, Kubernetes manifests, Helm charts, service mesh config | Medium. D365 customization model (OOB > Config > Customize > Extend > ISV). X++ for F&O extensions; C# plugins for CE. |
| Operational complexity | Low. Microsoft manages infrastructure, patching, scaling | Medium. Azure resource monitoring, scaling rules, cost management | High. Cluster upgrades, node pool management, container image lifecycle, security patching | Low-Medium. Microsoft manages SaaS infrastructure; ops focus is on data and configuration |
| Governance complexity | Medium. DLP policies, environment strategy, CoE Starter Kit, solution management | High. Azure Policy, RBAC across subscriptions, network security groups, Key Vault | Very High. Pod security policies, network policies, image scanning, runtime security, GitOps | Medium. Security roles, business units, field-level security, audit logging |

### Scalability Comparison

| Dimension | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Concurrent users | Up to 2,000 effective; performance degrades with complex canvas apps beyond this | Up to 50,000 with proper App Service scaling and caching | 50,000+ with horizontal pod autoscaling and cluster autoscaler | Scales with D365 SaaS infrastructure; effectively unlimited for standard operations |
| Data volume | Dataverse: up to 4TB per environment (with capacity add-ons); practical limit ~10M rows per table | Azure SQL: up to 100TB; Cosmos DB: effectively unlimited with partitioning | Same as Stack B for data tier; compute scales independently | CE: Dataverse limits apply; F&O: Azure SQL-backed, scales to enterprise volumes |
| Throughput | API limits: 6,000 requests/5 min per user; Power Automate: 100K actions/day (premium) | Azure Functions: millions of executions/day; Service Bus: millions of messages/day | Limited only by cluster size and node count; KEDA enables event-driven scaling | D365 API limits: 6,000 requests/5 min per user; batch frameworks for bulk operations |

### Time-to-Market

| Dimension | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Weeks to first release | 2-4 weeks | 6-10 weeks | 10-16 weeks | 8-14 weeks (config-heavy); 16-24 weeks (implementation project) |
| Iteration speed | Very fast. Visual designers, instant preview, same-day deployments | Moderate. CI/CD pipelines needed, but infrastructure-as-code accelerates | Slower. Container builds, image scanning, staged rollouts | Moderate. Solution transport through environments, regression testing required |

### Skill Requirements

| Role | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Citizen developer | Primary builder. Power Fx, model-driven design, flow authoring | UI layer via Power Platform; cannot build Azure services | Not applicable | Limited to personalizations and simple workflows |
| Professional developer | PCF controls, plugins, custom connectors | Full-stack: C#/Node.js APIs, Azure Functions, SQL, front-end | Kubernetes, Docker, CI/CD, service mesh, observability | C# plugins, JavaScript web resources, AL (Business Central), X++ for F&O (Visual Studio, Chain of Command extensions) |
| DevOps engineer | Solution pipelines, environment management | Azure DevOps/GitHub Actions, IaC (Bicep/Terraform), monitoring | Advanced: GitOps (Flux/ArgoCD), Helm, cluster operations, security scanning | Solution deployment pipelines, data migration, environment management |
| Functional consultant | Not typically needed | Not typically needed | Not typically needed | Critical: business process mapping, fit-gap analysis, data migration planning |

### Governance Model

| Aspect | Stack A | Stack B | Stack C | Stack D |
|---|---|---|---|---|
| Center of Excellence | CoE Starter Kit; DLP policies; managed environments; tenant-level controls | Azure landing zones; management groups; Azure Policy; cost management | Platform engineering team; cluster policies; namespace isolation; admission controllers | D365 Center of Excellence; release management; regression test suites |
| ALM | Dataverse solutions; environment variables; connection references; Power Platform pipelines | Azure DevOps/GitHub; Bicep/Terraform modules; artifact registries | GitOps repositories; Helm chart versioning; container image promotion | Solution transport; ISV solution management; dual-write configuration management |
| CI/CD | Power Platform Build Tools (Azure DevOps) or GitHub Actions for Power Platform | Standard Azure CI/CD with pipeline stages, gates, approvals | Container-native: build, scan, push, deploy via GitOps or pipeline | LCS (F&O) or Power Platform pipelines (CE); automated testing frameworks |

## Decision Tree

Use this prose-based decision tree to select the right starting stack. Begin at the top and follow the first matching condition.

**Step 1: Does your solution primarily automate standard ERP or CRM business processes?**

If your application centers on financial management, supply chain, manufacturing, sales pipeline, customer service case management, or field service operations, and these processes align closely with Dynamics 365 out-of-the-box capabilities, start with **Stack D**. Stack D provides pre-built industry-standard processes that would take months to build from scratch. Combine Stack D with Stack A, B, or C as needed for custom extensions.

**Step 2: Does your solution require microservices architecture, polyglot runtimes, or more than 50,000 concurrent users?**

If you need to run workloads in multiple programming languages, require fine-grained control over compute resources, need sidecar patterns (service mesh), or anticipate more than 50,000 concurrent users with complex processing, choose **Stack C**. This gives you Kubernetes-grade orchestration on top of all PaaS and low-code capabilities.

**Step 3: Does your solution require custom APIs, external-facing portals with complex identity, high-throughput messaging, or advanced data tier capabilities?**

If you need to build custom RESTful or GraphQL APIs, integrate with external systems beyond Power Platform connector capabilities, handle more than 6,000 API requests per 5 minutes per user, or need advanced database features like geo-replication or multi-model data, choose **Stack B**. This adds Azure PaaS services to your Power Platform foundation.

**Step 4: Your solution can be built entirely within Power Platform.**

If your application serves fewer than 2,000 users, works within Dataverse API limits, uses available connectors for integrations, and does not require custom server-side code, start with **Stack A**. This delivers the fastest time-to-market and lowest TCO.

## Stack Combination Rules

Stacks are designed to be additive and composable:

- **B is a superset of A** (B includes A). Every Stack B architecture uses Power Platform for the UI and workflow layer, adding Azure PaaS for capabilities that exceed Power Platform limits.
- **C is a superset of B** (C includes B includes A). Every Stack C architecture uses Power Platform and Azure PaaS, adding container orchestration for workloads that need it.
- **D combines with A, B, or C**. Dynamics 365 is a horizontal layer. A D365 implementation always pairs with at least Stack A (since D365 CE runs on Dataverse). Complex D365 implementations add Stack B (custom integrations) or Stack C (microservices extending D365).

Common combinations:
- **D + A**: Standard D365 deployment with Power Platform extensions. Most common for mid-market. F&O customization via X++ extensions.
- **D + B**: D365 with custom APIs, advanced integrations, Azure data platform. Common for enterprise. Fabric/Databricks for D365 analytics.
- **D + C**: D365 with microservices for high-scale custom processing. Rare; only for the largest enterprises.
- **A alone**: Departmental apps, process automation, internal portals. Most common starting point.
- **B without D**: Custom line-of-business applications that need APIs or advanced data but not ERP/CRM processes.
- **C without D**: Cloud-native applications, ISV products, high-scale consumer-facing platforms.

**Cross-Stack: Data Platform (Fabric / Databricks)**

Microsoft Fabric and Azure Databricks serve as the data platform layer across all stacks. They are not tied to a single stack but complement any combination:
- **Stack A + Fabric**: Analytics over Dataverse data, Power BI DirectLake dashboards
- **Stack B + Fabric/Databricks**: Data engineering, ML pipelines, enterprise analytics alongside Azure PaaS
- **Stack C + Databricks**: Heavy Spark workloads, ML at scale, streaming analytics alongside containers
- **Stack D + Fabric**: Mirroring D365 data to OneLake, cross-system analytics over ERP/CRM data, Power BI over F&O
- Both platforms use Delta Lake format and can interoperate via OneLake shortcuts

## When to Upgrade Stacks

Monitor these ceiling indicators to know when to escalate to the next stack:

**Stack A ceiling indicators (upgrade to B):**
- Power Automate flow runs consistently hitting daily action limits
- Canvas app performance degrading beyond acceptable thresholds with user growth
- Custom connectors hitting throttling limits or needing capabilities beyond connector framework
- Need for complex computational logic that Power Fx cannot express efficiently
- External integration requirements exceeding available connector catalog
- Data volume approaching Dataverse table row limits with performance impact

**Stack B ceiling indicators (upgrade to C):**
- Azure Functions cold start latency unacceptable for critical paths
- Need to run third-party software that only ships as container images
- Requirement for sidecar patterns (logging agents, security proxies, protocol translators)
- Multiple teams deploying independently and needing namespace-level isolation
- Need for fine-grained resource allocation (CPU/memory per service)
- Polyglot runtime requirements (Java, Python, Go services alongside .NET)

**Upgrade is not always linear.** Sometimes a Stack A application should jump directly to Stack C if the requirements shift dramatically. Always reassess against the decision tree rather than assuming incremental progression.

## Licensing and Cost Implications

**Stack A licensing:**
- Power Apps per-user: $20/user/month (use up to unlimited apps)
- Power Apps per-app: $5/user/app/month (use a single app)
- Power Automate per-user: $15/user/month (unlimited cloud flows)
- Power Automate per-flow: $100/flow/month (unlimited users for that flow)
- Dataverse capacity: 1GB database per 20 per-user licenses; additional at $40/GB/month
- Power Pages: authenticated users at $100/100 users/month

**Stack B additional costs:**
- Azure consumption is usage-based and highly variable
- Reserved instances (1-year or 3-year) save 30-60% on predictable workloads
- Azure SQL: starts at ~$5/month (Basic); production at $150-$1,500/month depending on DTU/vCore tier
- Azure Functions consumption: first 1M executions free; $0.20 per additional million
- App Service: $55-$350/month per instance depending on tier

**Stack C additional costs:**
- AKS cluster: control plane is free; pay only for node VMs
- Node VMs: D-series from $70/month; production clusters typically $500-$3,000/month
- Container Registry: Basic $5/month; Standard $20/month; Premium $50/month
- Egress costs can be significant for high-traffic applications

**Stack D licensing:**
- D365 Sales Professional: $65/user/month; Enterprise: $105/user/month
- D365 Customer Service Professional: $50/user/month; Enterprise: $105/user/month
- D365 Finance: $210/user/month (first user); $30/user/month (subsequent)
- D365 Supply Chain: $210/user/month (first user); $30/user/month (subsequent)
- D365 Business Central Essentials: $70/user/month; Premium: $100/user/month
- Team member licenses: $8/user/month (limited read/write access)

Cost optimization strategies apply across all stacks: right-size early, use dev/test pricing for non-production, leverage Azure Hybrid Benefit for existing Windows Server/SQL licenses, and negotiate Enterprise Agreement pricing for organizations with 500+ users.
