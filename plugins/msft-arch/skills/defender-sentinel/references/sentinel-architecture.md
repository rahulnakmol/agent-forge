# Microsoft Sentinel: Workspace Architecture

Reference for `/defender-sentinel`. Log Analytics workspace basics (OTel, App Insights, KQL fundamentals) belong to `/observability-architect`.

---

## What Sentinel Is (SOC Perspective)

Microsoft Sentinel is a cloud-native SIEM + SOAR built on top of a Log Analytics workspace. Every Sentinel instance is a Log Analytics workspace with the `SecurityInsights` solution enabled. This means:

- All data in a Sentinel-enabled workspace is billed at Sentinel pricing, including non-security data (Perf, ContainerLog, etc.)
- Sentinel provides 3 months of free interactive retention (vs. 31 days for a plain Log Analytics workspace)
- KQL queries, saved functions, and Workbooks work identically across Sentinel and Log Analytics because they are the same platform
- Sentinel is migrating from the Azure portal to the Microsoft Defender portal (retirement of Azure portal support: March 31, 2027). Plan the transition timeline accordingly.

---

## Workspace Topology Decision

**Default rule:** start with a single workspace per tenant. Introduce additional workspaces only when a specific requirement makes a single workspace infeasible.

### Decision Tree

```
Does the environment span multiple Azure AD tenants?
  YES: One Sentinel workspace per tenant (tenant-level data sources like Entra ID
       sign-ins cannot cross tenant boundaries without Azure Lighthouse).
  NO: Continue.

Is there a data-residency requirement (data must stay in a specific Azure region)?
  YES: One workspace per region boundary.
  NO: Continue.

Does the security team require strict isolation from Ops data for compliance reasons?
  YES: Separate SOC workspace from Ops workspace. Note: all data in the Sentinel
       workspace is billed at Sentinel pricing; Ops data in that workspace costs more.
  NO: Consider a combined workspace. Benefits: single commit tier, simpler cross-
      data queries, no Lighthouse overhead.

Is this an MSSP managing multiple customer tenants?
  YES: Hub-and-spoke model. Each customer gets their own Sentinel workspace.
       Hub uses Azure Lighthouse to query across customer workspaces.
  NO: Use the simplest model that meets the requirements above.
```

### Single Workspace Model

Best for: single tenant, single SOC team, no regional data residency requirement, combined security + operational data is acceptable.

- One Log Analytics workspace with Sentinel enabled.
- All security data (Defender XDR, Entra ID, Azure Activity, CEF/Syslog, M365) and operational data (App Insights, Perf, ContainerLog) in the same workspace.
- Cost benefit: easier to reach commitment tiers. A workspace ingesting 50 GB/day security + 50 GB/day ops at 100 GB/day combined receives a 50% Sentinel discount vs. two 50 GB/day workspaces each below the first commitment tier.
- Risk: security team sees operational tables. Mitigate with table-level RBAC or resource-context access mode if needed.

### Separate SOC + Ops Workspace (Same Tenant)

Best for: security team must not see operational data (Perf, InsightsMetrics, ContainerLog), or operational data volume is so large that including it in Sentinel would significantly increase Sentinel costs without security benefit.

- One workspace for Sentinel (security data only).
- One workspace for Ops (App Insights, Perf, container logs).
- Security-relevant data from operational sources (application security events, specific structured logs) is forwarded to the Sentinel workspace via a Data Collection Rule (DCR) with a transform that filters to security-relevant rows only.
- Cost note: operational data in a non-Sentinel workspace is billed at standard Log Analytics prices (cheaper than Sentinel pricing). Security data in the Sentinel workspace pays Sentinel prices and gets the 3-month free retention.

### Hub-and-Spoke (Multi-Tenant / MSSP)

Best for: MSSP managing multiple customer tenants, enterprise with multiple Azure AD tenants, or strict per-subsidiary data ownership.

- Each tenant (or subsidiary) has its own Sentinel workspace. Data stays within the tenant boundary.
- The hub SOC uses Azure Lighthouse to query across customer/subsidiary workspaces.
- Analytics rules, hunting queries, and playbooks are managed centrally and deployed to each workspace (Sentinel Repositories via CI/CD, or ARM template deployment via Lighthouse).
- Threat intelligence: connect TI feeds to the hub workspace; use cross-workspace queries to correlate IOCs across spokes. Alternatively connect TI to each spoke; more ingestion cost but simpler query architecture.
- Playbooks (Logic Apps) must reside in the same subscription as the workspace that triggers them; plan the Logic Apps resource group structure accordingly.

---

## Ingestion Cost Model

Sentinel pricing has two dimensions: ingestion (per GB/day) and retention (after the 3-month free interactive tier).

### Commitment Tiers (2025 guidance; verify via `microsoft_docs_search`)

| Daily ingestion | Discount vs. pay-as-you-go |
|---|---|
| Pay-as-you-go | Baseline |
| 100 GB/day | ~50% discount |
| 200 GB/day | Higher discount |
| 500 GB/day+ | Evaluate dedicated cluster |

**Dedicated cluster (100 GB/day minimum):** when multiple Sentinel workspaces in the same region collectively ingest 100 GB/day or more, linking them to a Log Analytics dedicated cluster aggregates volume across all workspaces for commitment tier pricing. Cross-workspace queries also run faster within a cluster. Maximum 1000 workspaces per cluster; maximum 2 clusters per region per subscription.

### Cost-reduction Strategies

1. **Basic Logs tier for high-volume, low-query tables:** CEF/Syslog raw device logs, verbose diagnostic logs, and raw network flow records are often needed for compliance archiving but queried infrequently. Ingest them at Basic Logs pricing (significantly cheaper than Analytics Logs). Basic Logs tables support only 8-day interactive retention and limited KQL (no cross-table joins). For longer retention, archive.
2. **Sentinel data lake (lake-only ingestion):** for secondary data not needed for real-time detection. Ingestion and storage at reduced cost; queried via KQL jobs on demand (not in analytics rules).
3. **Data Collection Rule (DCR) transforms:** filter rows and project columns at ingestion time. Drop noisy rows (heartbeat noise, debug-level logs) before they reach the workspace. Apply `where` and `project` transforms in the DCR pipeline.
4. **Separate Ops and security data:** as described above, operational data in a non-Sentinel workspace pays Log Analytics prices, not Sentinel prices.
5. **Review connector ingestion volume monthly:** use the `Usage` table or the Sentinel cost workbook to track GB/day per table and per connector. Disconnect connectors whose volume/cost does not justify their detection value.

---

## Retention Strategy

| Retention tier | Duration | Cost | Use case |
|---|---|---|---|
| Interactive (free) | 90 days (3 months Sentinel bonus) | Included | Active investigation, analytics rules, hunting |
| Interactive (paid) | Up to 2 years | Per GB/month | Compliance: some standards require >90 days accessible retention |
| Archive (long-term) | Up to 12 years | Very low per GB/month | Regulatory requirements (PCI-DSS: 1 year; HIPAA: 6 years; some audit requirements: 7+ years) |
| Table-level retention | Per table | Varies | Set shorter retention on low-value tables (heartbeat: 30 days); longer on high-value tables (SecurityEvent: 1 year) |

**Rules:**
- Set interactive retention to 90 days minimum on all security tables.
- For PCI-DSS: 1 year interactive; archive the rest to 7 years.
- For HIPAA: configure archive to 6 years minimum.
- For general enterprise: 90 days interactive; 1-year archive on security tables is a sensible default.

---

## Deployment as Code

- Provision the Sentinel workspace, analytics rules, data connectors, watchlists, and automation rules via Terraform (using `azurerm_sentinel_*` resources) or ARM/Bicep.
- Use **Sentinel Repositories** (built-in CI/CD) to deploy analytics rules, hunting queries, and watchlists directly from a Git repository. This is the recommended path for analytics rule version control; it enables pull-request review on rule changes.
- Store all Logic Apps (playbooks) as ARM templates in Git. Use the ARM Template Generator to export existing playbooks from the portal to ARM format.
- Infrastructure delivery belongs to `/iac-architect`; this skill defines the configuration; iac-architect delivers it.
