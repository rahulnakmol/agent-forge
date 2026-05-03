# Defender for Cloud: Plans by Resource Type

Reference for `/defender-sentinel`. Cross-link to `/security-architect` for baseline orientation (free tier, secure score introduction).

---

## Foundational CSPM (Free, Always-On)

Foundational Cloud Security Posture Management is auto-enabled on every subscription at no cost. It provides:

- Security recommendations against MCSB v1 controls
- Secure score calculation
- Regulatory Compliance dashboard (MCSB, NIST SP 800-53, CIS, ISO 27001, PCI-DSS)
- Asset inventory
- Basic cloud security graph (limited attack path vs. paid CSPM)

**Non-negotiable:** never disable Foundational CSPM. There is no acceptable justification for disabling it on any subscription.

---

## Plan Selection Matrix

### Defender CSPM (Paid Posture Management)

| When to enable | What it adds over free CSPM |
|---|---|
| All production subscriptions | Attack path analysis (full kill-chain from internet exposure to data) |
| Workloads with storage accounts containing sensitive data | DSPM: sensitive data posture management, detects sensitive data in storage and SQL |
| Regulated workloads | Agentless vulnerability scanning (no agent required on VMs) |
| Any workload | Cloud Infrastructure Entitlement Management (CIEM): over-provisioned identities |
| DevOps environments | PR annotations, DevOps security posture (GitHub, Azure DevOps) |

**Pricing model (2025):** per billable resource per month. Confirm current SKU price via `microsoft_docs_search` before quoting.

---

### Defender for Servers

| Plan | When required | Key capabilities |
|---|---|---|
| **P1** | Dev/test VMs, non-production Arc servers | Microsoft Defender for Endpoint integration (MDE); basic threat detection |
| **P2** | All production VMs, Arc servers | P1 + file integrity monitoring (FIM), just-in-time VM access (JIT), agentless vulnerability assessment, Defender for DNS (bundled at no extra charge for new subscriptions) |

**Critical note (August 2023 pricing update):** for new subscriptions, Defender for DNS is included in Servers P2 at no extra charge. Existing Defender for DNS standalone subscribers retain their billing model until they actively switch. Verify current bundle state with `microsoft_docs_search`.

**Resource-level enablement (GA December 2023):** Servers plan can now be overridden at the individual resource level, allowing P2 on critical VMs and P1 on lower-value VMs within the same subscription. Use this capability to optimise cost while maintaining P2 coverage on production workloads.

**Agentless scanning:** Servers P2 includes agentless vulnerability scanning and agentless secret scanning; does not require MMA/AMA on the VM. Enable this for immediate coverage on new VMs before the MDE onboarding completes.

---

### Defender for App Service

| When to enable | Coverage |
|---|---|
| Any subscription with App Service plans (web apps, Function Apps, API Apps) | Threat detection: dangling DNS (subdomain takeover detection), phishing content hosted on App Service, suspicious process execution, suspicious outbound connections, brute-force on admin panels |

**Pricing:** per App Service plan per month. Confirm current price.

**Key detection:** dangling DNS detection is unique to Defender for App Service and catches subdomain takeover attacks that cannot be detected by other plans. Always enable when App Service is in scope.

---

### Defender for Databases (SQL, OSS DBs, Cosmos DB)

| Plan | When to enable |
|---|---|
| **Defender for SQL** | Azure SQL Database, SQL Managed Instance, SQL Server on VMs, SQL Server on Azure Arc |
| **Defender for Open-Source Relational Databases** | PostgreSQL Flexible Server, MySQL Flexible Server, MariaDB |
| **Defender for Cosmos DB** | Azure Cosmos DB accounts |

Defender for SQL detects: anomalous query patterns, SQL injection attempts, access from unusual locations, brute-force on SQL authentication.

**Defender for Databases bundle:** Microsoft offers a Defender for Databases bundle covering all database types in a subscription at a lower per-resource cost than enabling each plan individually. Evaluate the bundle when multiple database types are present.

---

### Defender for Storage

| Feature tier | When to enable |
|---|---|
| **Standard (new plan)** | All production storage accounts; includes activity monitoring, malware scanning on-upload, sensitive data threat detection |
| **Classic (legacy)** | Retain only if already subscribed and not yet migrated; migrate to the new plan proactively |

**Malware scanning on-upload (near-real-time):** scans every blob uploaded across all file types. Critical for accounts that receive user uploads, partner file drops, or automated data pipelines. Per-GB scanning cost applies; size-limit per blob is confirmed via `microsoft_docs_search`.

**Sensitive data exfiltration detection:** detects anomalous access patterns to containers tagged as holding sensitive data. Pairs with DSPM in Defender CSPM.

**SAS token misuse detection:** detects use of SAS tokens from unusual locations or at unusual rates.

---

### Defender for Containers

| When to enable | Coverage |
|---|---|
| Any subscription with AKS clusters | Kubernetes environment hardening (CIS Kubernetes benchmark recommendations), container image vulnerability assessment, runtime threat protection |
| Any subscription with Azure Container Registry (ACR) | Image vulnerability assessment on push and on-pull |
| Any AKS workload | Runtime anomaly detection (suspicious process in container, privilege escalation, container escape attempts) |

**Agentless vs. agent:** Defender for Containers uses both agentless (Kubernetes API) and DaemonSet-based (Defender sensor) protection. The DaemonSet provides runtime threat detection; the agentless component provides posture. Both are needed for full coverage.

**Container image scanning:** enabled automatically on ACR. Findings appear in Defender for Cloud recommendations and in the `ContainerRegistryVulnerabilityAssessment` table.

---

### Defender for Key Vault

| When to enable | Coverage |
|---|---|
| All production Key Vaults | Alerts on: unusual access patterns (high volume of operations, unusual geographic location), access by suspicious principals, attempts to access disabled secrets, attempts to enumerate vault contents |

**Pricing model (2025):** fixed price per vault per month (new model). Existing subscribers on the per-operation legacy model retain their pricing until they actively switch. Confirm current vault pricing via `microsoft_docs_search`.

**Pairing with RBAC:** Defender for Key Vault detects anomalous access; it does not replace the RBAC permission model or soft-delete/purge-protection configuration. Both layers are required. RBAC design belongs to `/security-architect`.

---

### Defender for Resource Manager

| When to enable | Coverage |
|---|---|
| Every production subscription | Detects suspicious ARM operations: unusual subscription-level role assignments, cross-tenant activity, privilege escalation via ARM, suspicious resource creation (crypto-mining VMs, unusual regions) |

**Pricing model (2025):** fixed price per subscription per month (new model). Confirm current price.

**Critical detections:** Defender for Resource Manager is the only plan that monitors the ARM control plane. Without it, attackers can deploy rogue resources, exfiltrate data via ARM APIs, and elevate privileges entirely within blind spots. Enable on every production subscription without exception.

---

### Defender for DNS

| When to enable | Coverage |
|---|---|
| New subscriptions (included in Servers P2) | DNS-layer threat detection: DNS tunnelling (data exfiltration over DNS), communication with malicious domains, DNS hijacking indicators, anomalous DNS query volumes |
| Existing standalone subscribers | Retain until migrated to Servers P2 if the subscription has VMs |
| Subscriptions with no VMs (only PaaS) | Enable as a standalone plan for DNS coverage on resources connected to Azure's default DNS resolvers |

**Scope:** protects all Azure resources connected to Azure's default DNS resolvers, regardless of whether Servers plan is enabled. The DNS protection scope does not change when DNS is bundled with Servers P2; only billing changes.

---

### Defender for APIs

| When to enable | Coverage |
|---|---|
| Any subscription with Azure API Management (APIM) | API endpoint discovery, API risk posture scoring, API-specific threat detection (data exfiltration via API responses, authentication anomalies, unusual parameter values) |

---

### Defender for AI Services

| When to enable | Coverage |
|---|---|
| Any subscription with Azure AI Foundry or Azure OpenAI Service endpoints | Detects prompt injection attempts against AI models, jailbreak attempts, suspicious model invocation patterns, token exfiltration |

**Important:** Defender for AI Services is distinct from Azure AI Content Safety (which is an application-layer guardrail). Both are needed for AI workloads. Content Safety integration is the domain of `/ai-architect` and `/threat-model`.

---

## Cost vs. Coverage Trade-off Framework

When budget constraints require prioritisation, use this sequence:

1. **Always free, always on:** Foundational CSPM, Defender for Resource Manager (subscription cost is low).
2. **Enable first in production:** Defender for Servers P2 (largest attack surface; includes JIT, FIM, DNS), Defender for Storage (upload-path threat vector), Defender for Key Vault (secrets exfiltration detection).
3. **Enable when resource type is present:** Defender for App Service, Defender for SQL, Defender for Containers, Defender for APIs.
4. **Enable when compliance or risk justifies cost:** Defender CSPM (DSPM, agentless scanning, attack path), Defender for AI Services.
5. **Defer to budget discussion:** Defender for Cosmos DB, Defender for OSS databases (if low data-sensitivity or no compliance requirement).

Document all deferrals as accepted risks in an ADR, with a review date.

---

## Log Analytics Workspace Topology for Defender

Defender for Cloud writes findings, alerts, and recommendations to the **Security** and **SecurityAlert** tables in a connected Log Analytics workspace.

- Enable the **Log Analytics workspace agent auto-provisioning** setting in Defender for Cloud to automatically connect new VMs to the workspace.
- Use the **same workspace** for both Defender for Cloud and Sentinel where possible. This simplifies cross-table queries (SecurityAlert joined with Syslog, AzureActivity, etc.) and avoids data duplication.
- If the security team requires a dedicated workspace separate from Ops, configure Defender for Cloud to send alerts to the security workspace, not the ops workspace.

Workspace topology decisions: `sentinel-architecture.md`.
