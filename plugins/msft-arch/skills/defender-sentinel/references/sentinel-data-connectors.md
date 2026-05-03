# Microsoft Sentinel: Data Connectors

Reference for `/defender-sentinel`. Always verify connector GA vs. preview status via `microsoft_docs_search` before finalising a connector selection; the catalog changes frequently.

---

## Connector Categories

### Category 1: Azure-Native (Service-to-Service, Free to Ingest)

These connectors ingest data that is included in existing licensing or free at the service level. Enable all applicable ones on day 1.

| Connector | Data produced | Tables | Notes |
|---|---|---|---|
| **Azure Activity** | Subscription-level ARM operations | `AzureActivity` | Free ingestion; no additional cost |
| **Microsoft Entra ID** | Sign-in logs, Audit logs, Risky users/sign-ins, Provisioning logs | `SigninLogs`, `AuditLogs`, `AADRiskyUsers`, `ProvisioningLogs` | Requires Entra ID P1 or P2 for some tables |
| **Defender for Cloud** | Defender alerts, security recommendations | `SecurityAlert`, `SecurityRecommendation` | Requires Defender plan enabled; alerts flow automatically when workspace is linked |
| **Azure Key Vault** | Diagnostic logs (AuditEvent) | `AzureDiagnostics` (KeyVault category) | Route via Diagnostic Settings; filter to security-relevant operations |
| **Azure Firewall** | Firewall application rule logs, network rule logs, DNS proxy logs | `AzureDiagnostics` (AzureFirewall category) | High volume; use DCR transform to filter to Deny actions and threat-intelligence-matched flows |

### Category 2: Microsoft 365 (License-Included)

| Connector | Data produced | Tables | Notes |
|---|---|---|---|
| **Microsoft Defender XDR** | Unified XDR incidents covering MDE, MDI, MDO, MCAS | `SecurityAlert`, `SecurityIncident`, Advanced Hunting tables | **Primary connector for M365-licensed tenants.** Replaces individual Microsoft security rules when enabled. Requires Microsoft Defender XDR license. |
| **Microsoft 365 (Office 365 Activity)** | Exchange Online, SharePoint Online, Teams activity | `OfficeActivity` | Included in M365 licensing; enable for all M365 tenants |
| **Microsoft Entra ID Protection** | Risk events, risky users | `AADRiskyUsers`, `AADUserRiskEvents` | Requires Entra ID P2 |

**Note on Defender XDR integration:** when the Defender XDR connector is enabled and Microsoft Sentinel is onboarded to the Defender portal, Microsoft security rules (which create incidents from individual product alerts) are automatically disabled. Defender XDR creates unified incidents instead. This is the preferred architecture for M365-licensed tenants.

### Category 3: Third-Party CEF/Syslog via AMA

The **Azure Monitor Agent (AMA)** replaces the legacy Log Analytics Agent (MMA/OMS) for CEF and Syslog ingestion. Use AMA exclusively for new deployments.

**Architecture:**

```
Security device / appliance
       |  (UDP/TCP port 514)
       v
  Log forwarder Linux VM
  (rsyslog or syslog-ng daemon)
       |  (AMA receives on TCP port 28330 for AMA >= 1.28.11)
       v
  Azure Monitor Agent (AMA)
       |  (HTTPS, Data Collection Rule)
       v
  Microsoft Sentinel workspace
  Tables: Syslog (raw) | CommonSecurityLog (CEF)
```

**Configuration steps:**

1. Install AMA on the log forwarder VM (auto-installed when setting up the data connector in the Sentinel portal, or install manually before creating a DCR).
2. Create a Data Collection Rule (DCR) specifying: source (Syslog facility and minimum severity), destination (Sentinel workspace), and any row-level filters (DCR transforms).
3. Configure the security appliance to forward syslog to the forwarder on port 514 (or a custom port if using a non-standard port; ensure the Syslog daemon configuration matches).
4. CEF messages land in `CommonSecurityLog`; plain Syslog messages land in `Syslog`.

**Test query (post-setup):**

```kusto
CommonSecurityLog
| where TimeGenerated > ago(1d)
| where DeviceVendor == "Cisco"
| where DeviceProduct == "ASA"
| take 10
```

**High-volume sources:** apply DCR transforms to drop low-value rows at ingestion time. A firewall generating 50 GB/day of permit logs for known-safe traffic should be filtered to deny/block events only before the data reaches the Sentinel workspace.

### Category 4: Custom Connectors via Logic Apps and Logs Ingestion API

For SaaS sources, custom applications, and data sources with no native Sentinel connector:

1. **Logic Apps connector (recommended for low/medium volume):** use the `Azure Log Analytics Data Collector` or the newer `Azure Monitor Logs` connector in Logic Apps. Trigger on a schedule or HTTP webhook; transform the payload; post to Sentinel via the Logs Ingestion API.
2. **Logs Ingestion API (recommended for high volume or programmatic ingestion):** REST API that accepts JSON payloads and routes them to a custom table (suffix `_CL`) or a transformed standard table. Requires a Data Collection Endpoint (DCE) and a DCR. Use this for high-volume custom feeds, batch ingestion jobs, and any scenario where a Logic App trigger cadence is too slow.
3. **Codeless Connector Framework (CCF):** for building production-grade connectors that appear in the Sentinel content hub. Uses a declarative JSON definition to describe the connector's authentication, API calls, and schema mapping. Preferred for connectors that will be shared across multiple workspaces or published to the content hub.

**Deprecation notice:** the legacy HTTP Data Collector API is deprecated; it stops being supported after September 14, 2026. Migrate all custom ingestion built on the HTTP Data Collector API to the Logs Ingestion API before that date.

---

## Connector Priority Order

Apply connectors in this sequence to maximise detection value per ingestion dollar spent:

1. Defender XDR (if M365 licensed) or Defender for Cloud + individual Microsoft security connectors
2. Azure Activity
3. Microsoft Entra ID (Sign-in + Audit + Risky users)
4. Microsoft 365 (Office 365 Activity) if M365 tenant
5. Azure Firewall (filter to deny/block events via DCR transform)
6. CEF/AMA for on-premises firewalls, IDS/IPS, network appliances
7. Custom via Logs Ingestion API for SaaS apps not covered by content hub

---

## Cost Governance for Connectors

Before enabling any connector, estimate the daily GB/day ingestion volume:

- Azure Activity: low volume (typically 1-5 GB/day for active subscriptions)
- Entra ID sign-ins: medium volume (depends on user count and app integrations)
- CEF/Syslog from firewalls: highly variable; 10-500 GB/day is common for enterprise firewall fleets

Use the `Usage` table query after 48 hours of ingestion to validate actual volume:

```kusto
Usage
| where TimeGenerated > ago(2d)
| summarize DataGB = sum(Quantity) / 1000 by DataType
| order by DataGB desc
```

Disconnect or route to Basic Logs any connector where the ingestion cost does not justify the detection value. Document the decision in an ADR.
