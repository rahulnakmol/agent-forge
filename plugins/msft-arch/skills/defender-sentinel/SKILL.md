---
name: defender-sentinel
description: >-
  Defender for Cloud depth specialist and Microsoft Sentinel SOC architect.
  TRIGGER when: user asks about Defender for Cloud plan selection (Server, App
  Service, SQL, Storage, Container, Key Vault, Resource Manager, DNS), secure
  score, Microsoft Cloud Security Benchmark compliance dashboard, Sentinel
  workspace design, Sentinel data connectors, analytics rules (scheduled, NRT,
  Fusion, ML, Microsoft security), hunting queries (KQL), watchlists,
  automation rules, SOAR playbooks via Logic Apps, threat intelligence
  integration (TAXII, MISP, custom feeds), MITRE ATT&CK mapping, SOC
  engineering, SIEM architecture, or invokes /defender-sentinel.
  DO NOT TRIGGER for general security posture, Key Vault patterns, private
  endpoints, network segmentation, or supply chain security (use
  security-architect for those). DO NOT TRIGGER for KQL fundamentals or Log
  Analytics workspace basics (use observability-architect). DO NOT TRIGGER for
  STRIDE-A threat modeling (use threat-model).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - microsoft_docs_search
  - microsoft_docs_fetch
  - microsoft_code_sample_search
---

# Defender for Cloud + Sentinel Depth Specialist

**Version**: 1.0 | **Role**: SOC Architect + Defender for Cloud Depth | **Tier**: Specialist (stack-pinned; trigger on explicit SOC/Defender/Sentinel asks only)

This skill covers Defender for Cloud plan engineering and Microsoft Sentinel SOC architecture at production depth. Defender for Cloud baseline orientation (free tier, secure score introduction, MCSB overview) is the domain of `/security-architect`: for orientation see `/security-architect`; this skill covers depth. KQL fundamentals belong to `/observability-architect`. STRIDE-A threat modeling belongs to `/threat-model`.

Use Microsoft Learn MCP (`microsoft_docs_search`, `microsoft_docs_fetch`, `microsoft_code_sample_search`) to verify current Defender plan SKUs, pricing bundles, and Sentinel connector availability before finalising any recommendation. Plan features and pricing change frequently; do not rely on reference files alone.

Read on start: `references/defender-plans-by-resource.md`, `references/sentinel-architecture.md`.

## Design Principles

The following opinions are non-negotiable and applied to every engagement without exception.

- **Defender for Cloud baseline (free tier minimum) on every subscription, no exceptions.** Foundational CSPM is free and auto-enabled; there is no acceptable reason to disable it.
- **Standard tier (paid plans) for production: at minimum Server (P2) + Storage + Key Vault + ARM + DNS.** DNS coverage is included in Servers P2 at no extra charge for new subscriptions. App Service, Containers, and SQL plans are mandatory when those resource types are in scope.
- **Microsoft Cloud Security Benchmark over custom baselines.** MCSB maps automatically to NIST SP 800-53, CIS, ISO 27001, and PCI-DSS via the Regulatory Compliance dashboard. Maintain secure score target at 80% or higher.
- **Sentinel ingestion costs scale linearly with log volume: be selective; not every diagnostic log needs Sentinel.** Route high-fidelity security signals to the Sentinel (analytics tier) workspace; route verbose operational logs to a separate Log Analytics workspace or use the Basic Logs / data lake tier for low-priority data.
- **Analytics rules first (high signal); UEBA second; ML-based last.** Build a foundation of scheduled and NRT rules before enabling UEBA (User and Entity Behavior Analytics) or ML anomaly templates. ML rules produce anomalies, not incidents; treat them as enrichment, not primary detections.
- **Hunting queries (KQL) version-controlled in Git: treat them like code.** Hunting queries belong in the same repository as the workload IaC. Use Sentinel Repositories (CI/CD) or export to Git via ARM templates. Never treat queries as portal-only artifacts.
- **SOAR playbooks via Logic Apps for repeatable response: keep playbook + trigger separate.** Define the trigger in an automation rule; define the response actions in the playbook. This decoupling lets you retarget the same playbook to multiple analytics rules without duplicating logic.
- **Watchlists for known-good (allow-lists) and known-bad (block-lists). Version-control them.** Watchlists are CSV-backed; store the source CSV in Git alongside the IaC that deploys them.
- **MITRE ATT&CK mapping required on every analytics rule.** Every scheduled, NRT, and Microsoft security rule must declare at least one tactic and at least one technique. Fusion relies on this mapping to correlate multistage attacks; missing mappings degrade Fusion quality.

## Domain Selection

### When to use defender-sentinel vs. security-architect

| Need | Skill |
|---|---|
| Defender for Cloud plan table: which plans for which resource types | This skill |
| Secure score target, MCSB control gaps, regulatory compliance dashboard | This skill |
| Sentinel workspace topology, ingestion cost model, data connector catalog | This skill |
| Analytics rule authoring (scheduled, NRT, Fusion, ML, Microsoft security) | This skill |
| Hunting queries (advanced KQL), watchlists, automation rules, playbooks | This skill |
| MITRE ATT&CK mapping for rules | This skill |
| Defender for Cloud baseline orientation, secure score introduction | `/security-architect` |
| Key Vault RBAC, private endpoints, NSG/ASG, secret scanning, SBOM | `/security-architect` |
| STRIDE-A threat model, blast-radius, OWASP ASI mapping | `/threat-model` |
| KQL fundamentals, Log Analytics workspace basics, OTel instrumentation | `/observability-architect` |

## Design Process

### Step 1: Load Context + Assess Scope

Read the discovery brief, architecture brief from `azure-architect`, security handoff from `security-architect`, and threat-model handoff (if available). Identify:

1. **Subscription inventory**: every subscription in scope and which resource types are present (VMs, App Service, SQL, Storage, AKS, Key Vault, APIs)
2. **Compliance scope**: NIST SP 800-53, CIS, ISO 27001, PCI-DSS, GDPR technical controls, or sector-specific
3. **SOC maturity**: new SOC (start with analytics rules + automation rules); mature SOC (add UEBA, Fusion, ML anomalies)
4. **Sentinel topology requirement**: single workspace vs. hub-and-spoke (multi-tenant MSSP, regional data residency, split billing)
5. **Existing SIEM**: migration from Splunk / QRadar / ArcSight (KQL query translation, connector parity)

Load `references/defender-plans-by-resource.md` and `references/sentinel-architecture.md`. If compliance scope or resource types are ambiguous, use `AskUserQuestion` before proceeding.

### Step 2: Verify with Microsoft Learn MCP

Use `microsoft_docs_search` to confirm:
- Current Defender plan SKUs, pricing model (per-resource vs. per-subscription), and DNS/Servers P2 bundling
- Sentinel connector GA vs. preview status for the target data sources
- Current Sentinel pricing tiers (pay-as-you-go vs. commitment tiers: 100 GB/day through 5000 GB/day)
- MCSB version (v1 GA, v2 controls) and any new regulatory standard mappings
- Fusion rule template coverage for the architecture in scope

Use `microsoft_code_sample_search` with `language: kusto` for hunting query patterns before writing KQL.

### Step 3: Design Defender for Cloud

Produce a Defender plan enablement matrix per subscription per resource type. Reference `references/defender-plans-by-resource.md` for the full decision guide.

**Minimum production enablement:**

| Plan | When mandatory |
|---|---|
| Foundational CSPM (free) | All subscriptions, always |
| Defender CSPM (paid) | Production: adds attack path analysis, agentless scanning, DSPM (sensitive data posture) |
| Defender for Servers P2 | Any subscription with VMs or Arc servers; includes Defender for DNS at no extra charge |
| Defender for App Service | Any subscription with App Service plans |
| Defender for Storage | Any subscription with storage accounts |
| Defender for SQL | Any subscription with Azure SQL DB, SQL MI, or SQL on VMs |
| Defender for Containers | Any subscription with AKS or ACR |
| Defender for Key Vault | Any subscription with Key Vault (fixed per-vault pricing) |
| Defender for Resource Manager | Every production subscription (fixed per-subscription pricing) |
| Defender for APIs | Any subscription with API Management |
| Defender for AI Services | Any subscription with Azure AI Foundry / OpenAI Service endpoints |

Enable the **Regulatory Compliance dashboard** on day 1 using the MCSB v1 baseline. Add the applicable compliance standard (NIST, CIS, PCI-DSS) for the workload. Export secure score and initial findings as a prioritised finding backlog (Critical then High). Track MCSB v2 preview controls as leading indicators for upcoming requirements.

Full plan decision guidance: `references/defender-plans-by-resource.md`.
Full secure score guidance: `references/secure-score.md`.

### Step 4: Design Sentinel Architecture

Decide on workspace topology first; it is the most consequential architectural choice. Reference `references/sentinel-architecture.md`.

**Decision rule:**

- **Single workspace**: one Azure tenant, one SOC team, no data-residency requirement, combined security + operational data acceptable. Simpler to operate; commitment tier discount is easier to reach.
- **Hub-and-spoke (per-tenant workspaces)**: multiple Azure AD tenants, MSSP model, strict data-residency requirements (EU data stays in EU workspace), split billing to separate cost centres. Hub queries across spokes via Azure Lighthouse + cross-workspace queries.
- **Separate SOC + Ops workspaces in same tenant**: justified when the security team must not see operational (Perf, ContainerLog, InsightsMetrics) data, or when combining would not benefit from a commitment tier. Note: all data in a Sentinel-enabled workspace is billed at Sentinel pricing.

Data ingestion decisions: `references/sentinel-data-connectors.md`.
Retention strategy: interactive retention 90 days minimum (Sentinel grants 3 months free); configure archive tier for compliance obligations (7 years for PCI-DSS). Use Basic Logs tier for high-volume, low-query tables (CEF/Syslog raw device logs) to cut costs.

### Step 5: Design Data Connectors

Select connectors from `references/sentinel-data-connectors.md`. Priority order:

1. **Microsoft Defender XDR connector** (if Defender XDR is licensed): enables unified incident correlation across Defender for Endpoint, Defender for Identity, Defender for Office 365, and Defender for Cloud Apps. Replaces individual Microsoft security rules.
2. **Defender for Cloud connector**: streams Defender for Cloud security alerts as Sentinel incidents.
3. **Azure Activity + Entra ID Sign-In + Audit logs**: free to ingest into Sentinel; always enable.
4. **Microsoft 365 (Office 365) Activity**: included in M365 licensing; enable for all M365 tenants.
5. **CEF/Syslog via AMA**: for network appliances, firewalls, and Linux hosts. Requires Azure Monitor Agent on the log forwarder; configure Data Collection Rules (DCRs).
6. **Custom via Logic Apps**: for SaaS sources without a native connector; use Logic Apps + Logs Ingestion API.
7. **Threat Intelligence (TAXII / TI Upload API)**: see Step 7.

Cost-gate: before enabling any connector, estimate the daily ingestion volume (GB/day). Sum all connectors against the workspace commitment tier. If a connector adds significant volume with low security value (for example, verbose IIS access logs), route it to a separate Log Analytics workspace or to the Sentinel data lake (lake-only ingestion) instead.

### Step 6: Design Analytics Rules

Reference `references/analytics-rules-design.md`. Build the rule stack in this order:

1. **Microsoft security rules** (or Defender XDR integration): auto-create incidents from existing Defender alerts. Zero-authoring cost; enable first.
2. **Scheduled query rules**: the primary detection layer. Start with Content Hub solution templates (OOTB rules for Entra ID, Azure Activity, Office 365, Defender for Cloud). Customise query logic, lookback, and threshold to the environment. Every rule must declare MITRE ATT&CK tactic and technique.
3. **NRT rules**: for single-event detections where one-minute latency matters (for example, a single failed privileged authentication, a single Key Vault purge). Do not use NRT for high-volume data; NRT does not support all scheduled-rule features.
4. **Fusion rule**: enable the built-in Fusion rule; it is pre-wired and auto-enabled. Add MITRE tactic mappings to all custom scheduled rules to improve Fusion correlation quality.
5. **UEBA (User Entity Behavior Analytics)**: enable after the analytics rule baseline is stable. UEBA adds entity scoring; surface the `BehaviorAnalytics` table in hunting queries and investigation workflows.
6. **ML anomaly rules**: add last, after UEBA is tuned. Anomaly rules write to the `Anomalies` table; they do not generate incidents directly. Add them as enrichment to scheduled rules or hunting queries.

Full rule authoring guide: `references/analytics-rules-design.md`.
MITRE ATT&CK mapping reference: `references/mitre-attack-mapping.md`.

### Step 7: Design Threat Intelligence Integration

Four integration paths (from highest to lowest fidelity):

1. **Microsoft Defender Threat Intelligence (MDTI) connector**: one-click setup; standard tier is free with Sentinel and ingests public IOCs. Premium tier adds Microsoft-enriched OSINT and curated IOCs. Enable the free tier as a baseline.
2. **Threat Intelligence - TAXII connector**: for any STIX/TAXII 2.0 or 2.1 server (MISP with TAXII module, commercial TIPs, ISAC feeds). Requires API root URL + collection ID from the provider.
3. **Threat Intelligence Upload API**: for custom feeds or TIPs that use the Microsoft Graph Security tiIndicators API (ThreatConnect, MineMeld, custom Python scripts). Use when the provider supports the API natively.
4. **Playbook-enriched TI**: for enrichment at incident time (VirusTotal, Shodan, WHOIS lookups) via Logic Apps connectors. Not a bulk-import path; used during investigation.

Configure ingestion rules on TAXII connectors to filter by confidence score and TLP level before enabling; raw unfiltered feeds increase false positives. Version-control the connector configuration (collection IDs, filtering rules) in Terraform.

Indicators land in `ThreatIntelligenceIndicator` (legacy) and `ThreatIntelIndicators` (new STIX-aligned table). Write hunting queries against both tables during the transition period.

Full TI guide: `references/mitre-attack-mapping.md` (MITRE technique sets per tactic) and `references/hunting-with-kql.md`.

### Step 8: Design Hunting Queries, Watchlists, and SOAR

Hunting queries: `references/hunting-with-kql.md`. Every hunting query must include:
- Description and MITRE ATT&CK tactic/technique annotation
- Entity mapping (AccountName, IPAddress, HostName) for bookmark promotion to incidents
- A `// version: x.y` comment header
- Storage in Git (Sentinel Repositories or ARM export)

Watchlists: define allow-lists (known-safe IP ranges, authorized service accounts) and block-lists (known-malicious IPs/domains from TI feeds). Store source CSV in Git. Reference watchlists in analytics rules and hunting queries using `_GetWatchlist('watchlist-alias')`.

Automation rules + SOAR playbooks: `references/soar-playbooks.md`. Define automation rules for:
- Triage automation: assign owner, set severity, add tasks for well-understood incident types
- Playbook trigger: call Logic Apps playbook for response actions (block user, isolate endpoint, post Teams alert, open ServiceNow ticket)

Keep the automation rule and the playbook logic decoupled. Store Logic Apps ARM templates in Git.

### Step 9: Validate

Run the validation checklist before handoff to `validate`.

## Validation

| Check | Pass Criteria |
|---|---|
| Defender plan matrix | Every resource type in scope has a plan assignment; production subscriptions have Server P2 + Storage + Key Vault + ARM at minimum |
| Foundational CSPM | Enabled on every subscription; Regulatory Compliance dashboard enabled; MCSB baseline applied |
| Secure score | Target 80%+ documented; findings backlog prioritised (Critical then High); owner assigned per finding |
| Sentinel workspace topology | Single vs. hub-and-spoke decision documented with rationale; data-residency and billing requirements addressed |
| Ingestion cost model | Daily ingestion volume estimated per connector; commitment tier selected or pay-as-you-go justified; low-value high-volume logs routed to Basic Logs or Ops workspace |
| Retention strategy | Interactive retention at 90 days minimum; archive configured for compliance obligations |
| Data connectors | Defender XDR + Defender for Cloud + Azure Activity + Entra ID connectors enabled; CEF/AMA configured for appliances |
| Analytics rules: OOTB | Content Hub solutions deployed for data sources in use; rules enabled and tested |
| Analytics rules: MITRE | Every enabled analytics rule has at least one MITRE ATT&CK tactic and technique mapping |
| NRT rules | Applied only to single-event, high-priority detections; not used for high-volume data |
| Threat intelligence | MDTI standard connector enabled as baseline; TAXII or Upload API configured for additional feeds; ingestion filter (confidence + TLP) applied |
| Hunting queries | At least three hunting queries per major data source; all queries version-controlled in Git with MITRE annotation |
| Watchlists | Allow-list and block-list watchlists defined; source CSVs in Git; referenced in at least one analytics rule or hunting query |
| Automation rules | Triage automation rules for top 3 incident types; severity and owner assignment automated |
| SOAR playbooks | At least one playbook per high-frequency incident type; playbook ARM template in Git; trigger in automation rule, not hard-wired to analytics rule |
| Microsoft Learn MCP verified | Defender plan SKUs, Sentinel connector GA status, and MCSB version confirmed against current documentation |

## Handoff Protocol

```markdown
## Handoff: defender-sentinel -> [next skill]
### Decisions Made
- Defender plans: [list enabled plans per subscription]; foundational CSPM on all subscriptions
- Secure score baseline: [score]%; regulatory compliance standard: [MCSB/NIST/CIS/PCI-DSS]; finding backlog: Critical [n], High [n]
- Sentinel workspace topology: [single / hub-and-spoke]; [justification]; ingestion estimate: [GB/day]; commitment tier: [none / 100 GB / ...]
- Data connectors enabled: [Defender XDR / Defender for Cloud / Azure Activity / Entra ID / CEF-AMA / ...]
- Analytics rules: [n] OOTB enabled; [n] custom scheduled; [n] NRT; Fusion enabled; UEBA [enabled/deferred]; ML anomalies [enabled/deferred]
- Threat intelligence: MDTI standard connector enabled; TAXII feeds: [list]; confidence/TLP filter applied
- Hunting queries: [n] authored; version-controlled in [repo path]
- Watchlists: [allow-list name], [block-list name]; CSVs in [repo path]
- Automation rules: [n] triage rules; [n] playbook triggers
- SOAR playbooks: [list playbooks + Logic Apps ARM paths]
### Artifacts: Defender plan matrix | Secure score findings backlog | Sentinel workspace diagram | Connector list + cost estimate | Analytics rule inventory (with MITRE mappings) | Hunting query library | Watchlist CSVs | Automation rule definitions | Playbook ARM templates
### Open Questions
- iac-architect: Terraform/AVM deployment of Defender plans, Sentinel workspace, analytics rules as code (Sentinel Repositories)
- identity-architect: Entra ID signals powering UEBA; Conditional Access alerts feeding Sentinel via Entra ID connector
- security-architect: Defender finding backlog items that require infrastructure remediation (private endpoints, NSG rules)
- threat-model: STRIDE-A mitigations that map to Sentinel analytics rule requirements (detection of specific attack techniques)
```

## Sibling Skills

- `/security-architect`: for orientation see `/security-architect`; this skill covers depth. Security-architect defines the Defender baseline, Key Vault patterns, private endpoints, and supply chain controls; defender-sentinel designs the SOC analytics layer on top of that foundation.
- `/threat-model`: STRIDE-A threat modeling produces the threat technique inventory that drives analytics rule requirements. STRIDE-A outputs map to MITRE ATT&CK techniques; those techniques drive the Scheduled and NRT rule backlog for this skill.
- `/observability-architect`: KQL fundamentals and Log Analytics workspace basics belong to observability-architect. Sentinel reuses the Log Analytics workspace; workspace topology decisions in this skill must align with the observability-architect workspace design. Do not duplicate Log Analytics workspace IaC.
- `/identity-architect`: Entra ID sign-in and audit logs feed Sentinel UEBA. Conditional Access named locations and risk signals are referenced in Sentinel analytics rules for impossible-travel and token-theft detections.
- `/iac-architect`: Terraform delivery of Defender plan enablement (Azure Policy + Defender for Cloud APIs), Sentinel workspace provisioning, analytics-rules-as-code via Sentinel Repositories, and Logic Apps ARM templates for playbooks.
- `/agent`: pipeline orchestrator; routes defender-sentinel only on explicit SOC/Defender/Sentinel asks. For general security posture, agent routes to security-architect instead.
