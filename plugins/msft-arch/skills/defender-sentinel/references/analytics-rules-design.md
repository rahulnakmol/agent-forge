# Sentinel Analytics Rules: Design Guide

Reference for `/defender-sentinel`. MITRE ATT&CK technique mapping belongs to `mitre-attack-mapping.md`.

---

## Rule Type Selection

### Decision Matrix

| Rule type | When to use | Latency | Notes |
|---|---|---|---|
| **Microsoft security** | Alerts from external Microsoft services (Defender for Cloud, Entra ID Protection, Defender for Identity) need to become Sentinel incidents | Near-real-time | Disabled automatically when Defender XDR connector is enabled; Defender XDR creates incidents instead |
| **Scheduled** | Correlation across multiple tables, statistical analysis, lookback > 1 minute, aggregation over a time window | 5 min to hours (configurable) | Most common type; start here |
| **NRT (near-real-time)** | Single-event detections where sub-minute latency is critical (one Key Vault purge = alert, one privileged role assignment = alert) | ~1 minute | Cannot use all scheduled-rule features (no alert threshold, no query scheduling); limited to 30 events per run before truncation |
| **Fusion** | Multistage attack correlation (correlates signals from multiple sources into a single incident representing a kill chain) | Minutes to hours | Enable the built-in Fusion rule; it is self-managed. Improve quality by adding MITRE tactic/technique mapping to all custom scheduled rules |
| **UEBA (Anomaly)** | Detecting deviations from normal user/entity behavior baselines | Hours (observation period required) | Writes to `Anomalies` table; does not generate incidents directly. Use as enrichment in scheduled rules or hunting queries |
| **ML behavior analytics** | Detecting anomalous SSH and RDP login behavior (built-in ML templates) | Hours | Limited number of templates; cannot be customised; enable only after analytics rule baseline is stable |

**Build order:** Microsoft security rules first (zero authoring) → scheduled query rules (content hub OOTB + custom) → NRT rules for critical single-event detections → Fusion (auto-enabled) → UEBA after baseline stable → ML anomaly templates last as enrichment.

---

## Scheduled Rules: Authoring Standards

Every scheduled analytics rule must include all of the following:

1. **Name:** `<Source>: <Threat Behavior> (<MITRE Tactic>)`. Example: `AzureActivity: Bulk Role Assignment by Single Principal (Privilege Escalation)`.
2. **Description:** 2-3 sentences explaining what the rule detects, why it indicates a threat, and what the analyst should investigate.
3. **MITRE ATT&CK tactic:** at least one tactic from the ATT&CK Enterprise framework (required for Fusion quality).
4. **MITRE ATT&CK technique:** at least one technique ID (for example, T1078 for Valid Accounts, T1098 for Account Manipulation). Sub-technique is optional but preferred.
5. **Severity:** Critical, High, Medium, or Low. See severity guide below.
6. **Entity mapping:** map query result columns to Sentinel entity types (AccountEntity, HostEntity, IPEntity, etc.). Entity mapping enables the investigation graph and UEBA enrichment.
7. **Custom details (optional):** surface key fields from the raw event directly in the alert detail without requiring the analyst to open the raw log.
8. **Alert grouping:** group alerts into incidents by entity (AccountName, IPAddress) within a time window. This prevents incident flooding when a single attacker triggers many alerts.

### Severity Guide

| Severity | When to assign |
|---|---|
| **Critical** | Active exploitation in progress, data exfiltration, account takeover confirmed |
| **High** | Strong indicator of attack (unusual privilege escalation, impossible travel, credential harvesting), requires same-day investigation |
| **Medium** | Suspicious but explainable by legitimate activity (bulk downloads, off-hours access); requires investigation within 48 hours |
| **Low** | Informational, possible false positive, or policy violation not constituting an active threat; review in weekly triage |

---

## Scheduled Rule: KQL Template

Adapt this structure for every new scheduled rule.

```kusto
// Rule: [Rule Name]
// MITRE ATT&CK: [Tactic] | [Technique ID] - [Technique Name]
// Description: [What this detects and why it is suspicious]
// version: 1.0
let lookback = 1d;
let alertThreshold = 5;
AzureActivity
| where TimeGenerated > ago(lookback)
| where OperationNameValue in~ (
    "microsoft.authorization/roleassignments/write",
    "microsoft.authorization/roleassignments/delete"
)
| where ActivityStatusValue =~ "Success"
| summarize
    RoleAssignmentCount = count(),
    TargetResources = make_set(ResourceId, 20),
    Operations = make_set(OperationNameValue),
    StartTime = min(TimeGenerated),
    EndTime = max(TimeGenerated)
    by Caller, CallerIpAddress, SubscriptionId
| where RoleAssignmentCount >= alertThreshold
| extend
    Name = tostring(split(Caller, '@', 0)[0]),
    UPNSuffix = tostring(split(Caller, '@', 1)[0])
| project
    TimeGenerated = EndTime,
    Caller,
    Name,
    UPNSuffix,
    CallerIpAddress,
    RoleAssignmentCount,
    SubscriptionId,
    TargetResources,
    StartTime,
    EndTime
```

**Entity mapping for this rule:**
- `Name` + `UPNSuffix` -> AccountEntity
- `CallerIpAddress` -> IPEntity
- `SubscriptionId` -> AzureResourceEntity

---

## NRT Rules: When and How

NRT rules run every minute and examine the preceding minute of ingested data. Use NRT when:
- A single event is sufficient to generate an alert (no aggregation, no lookback, no threshold)
- The time between event and alert matters (for example, a privileged role assigned to a service account, a Key Vault purge initiated)

NRT rules do NOT support:
- Query scheduling or alert threshold configuration
- Event grouping beyond 30 events per run (generates one alert per event for the first 29; a summary alert for remainder)

NRT rule example (Key Vault purge detection):

```kusto
// Rule: KeyVault: Purge Protection Disable Attempt (Defense Evasion)
// MITRE ATT&CK: Defense Evasion | T1562.001 - Impair Defenses: Disable or Modify Tools
// version: 1.0
AzureActivity
| where OperationNameValue =~ "microsoft.keyvault/vaults/write"
| where ActivityStatusValue =~ "Success"
| where Properties has "softDeleteEnabled" and Properties has "\"false\""
| extend
    VaultName = tostring(split(ResourceId, '/', 8)),
    Caller = tostring(Caller),
    Name = tostring(split(Caller, '@', 0)[0]),
    UPNSuffix = tostring(split(Caller, '@', 1)[0])
| project TimeGenerated, VaultName, Caller, Name, UPNSuffix, CallerIpAddress, ResourceId
```

---

## Analytics Rule: Tuning and False Positive Management

1. **Start in Alert mode, not Incident mode.** Enable a new rule to generate alerts only, not incidents, for the first 72 hours. Review the alert volume and false-positive rate before enabling incident creation.
2. **Use alert grouping.** Group multiple alerts for the same entity (AccountName, IPAddress) within a 24-hour window into a single incident. Prevents analyst fatigue on noisy rules.
3. **Suppress** rules that continue to generate false positives at high rates by adding exclusion conditions (for example, `where Caller !in (_GetWatchlist('AllowedServiceAccounts') | project SearchKey)`).
4. **Document suppressions.** Every suppression (watchlist exclusion, `!in` condition, KQL filter) must have a comment explaining what it excludes and why.
5. **Review monthly.** Analytics rules are code. Schedule a monthly review to retire rules whose signal-to-noise ratio has degraded, update rules for new MITRE techniques, and add rules for newly enabled data sources.

---

## Content Hub: Priority Solution Deployments

Deploy these Content Hub solutions as the analytics rule baseline before authoring custom rules:

| Content Hub solution | Required for |
|---|---|
| Azure Activity | All Azure subscriptions |
| Microsoft Entra ID | All Entra ID tenants |
| Microsoft 365 | M365 tenants |
| Microsoft Defender for Cloud | All Defender-enabled subscriptions |
| Defender for Identity | Entra ID Domain Services / on-premises AD |
| Azure Key Vault | All subscriptions with Key Vault |
| Azure Firewall | All subscriptions with Azure Firewall |
| Network Session Essentials | CEF/Syslog network device data |
| Threat Intelligence | TAXII/TI integrations (see `sentinel-data-connectors.md`) |

After deploying each solution, enable the recommended rule templates. Customise thresholds and lookback periods to match the environment volume before promoting to production.
