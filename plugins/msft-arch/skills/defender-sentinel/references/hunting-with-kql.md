# Sentinel Hunting with KQL

Reference for `/defender-sentinel`. KQL fundamentals belong to `/observability-architect`. This file covers hunting-grade KQL: patterns, query standards, watchlist usage, and bookmark-to-incident promotion.

---

## What Hunting Is

Hunting is proactive, analyst-driven threat investigation. Unlike analytics rules (which run continuously and fire alerts), hunting queries are run on demand or on a schedule by a SOC analyst looking for threat behaviour that has not yet triggered an alert.

Effective hunting requires:
- High-quality data connectors (CEF, Syslog, Azure Activity, Entra ID, Defender XDR advanced hunting tables)
- Familiarity with the MITRE ATT&CK technique catalogue for the environment's attack surface
- Version-controlled queries in Git (treat them like code; apply the same review process as application code)

---

## Hunting Query Standards

Every hunting query in the library must include:

```kusto
// === HUNTING QUERY ===
// Name:        [Human-readable name]
// MITRE:       [Tactic] | [Technique ID] - [Technique Name]
// Description: [What the query hunts for; why this pattern indicates compromise]
// Data sources: [Tables queried]
// version:     1.0
// author:      [Team/person]
// ===================
```

After adding the header, write the query. Every query must:
1. Filter to a bounded time window using `ago()` (default 7 days for proactive hunts; 30 days for retroactive hunts)
2. Apply entity projection so results can be promoted to bookmarks (AccountName, IPAddress, HostName, ResourceId must be explicit columns)
3. Use `summarize` to aggregate over time rather than returning raw event rows (raw rows exhaust the portal result limit)
4. Include a result filter that surfaces only anomalous or suspicious entries (not a full table dump)

---

## Hunting Query Patterns

### Pattern 1: Sensitive Azure ARM Operations (Credential Access / Privilege Escalation)

Maps to: MITRE T1078 (Valid Accounts), T1098 (Account Manipulation), T1552 (Unsecured Credentials).

```kusto
// === HUNTING QUERY ===
// Name:        AzureActivity: Sensitive ARM Operations by Principal
// MITRE:       Privilege Escalation | T1078 - Valid Accounts
// Description: Identifies principals performing high-risk ARM operations
//              (snapshot writes, NSG rewrites, storage key enumeration)
//              that may indicate credential abuse or insider threat.
// Data sources: AzureActivity
// version:     1.0
// ===================
let lookback = 14d;
let alertThreshold = 5;
let SensitiveOps = dynamic([
    "microsoft.compute/snapshots/write",
    "microsoft.network/networksecuritygroups/write",
    "microsoft.storage/storageaccounts/listkeys/action",
    "microsoft.authorization/roleassignments/write"
]);
let SensitiveActivity = AzureActivity
| where TimeGenerated > ago(lookback)
| where OperationNameValue in~ (SensitiveOps) or OperationNameValue hassuffix "listkeys/action"
| where ActivityStatusValue =~ "Success";
SensitiveActivity
| summarize
    OperationCount = count(),
    Operations = make_set(OperationNameValue, 10),
    Resources = make_set(ResourceId, 10),
    StartTime = min(TimeGenerated),
    EndTime = max(TimeGenerated)
    by CallerIpAddress, Caller, SubscriptionId
| where OperationCount >= alertThreshold
| extend
    Name = tostring(split(Caller, '@', 0)[0]),
    UPNSuffix = tostring(split(Caller, '@', 1)[0])
| project TimeGenerated = EndTime, Caller, Name, UPNSuffix, CallerIpAddress,
    OperationCount, Operations, SubscriptionId, StartTime, EndTime
```

### Pattern 2: Threat Intelligence IP Match Against CEF Logs (Command and Control)

Maps to: MITRE T1071 (Application Layer Protocol), T1048 (Exfiltration Over Alternative Protocol).

```kusto
// === HUNTING QUERY ===
// Name:        TI: Malicious IP Match in CEF Firewall Logs
// MITRE:       Command and Control | T1071 - Application Layer Protocol
// Description: Joins active threat intelligence IOCs (IP indicators) against
//              CommonSecurityLog (CEF firewall/IDS events) to surface hosts
//              that communicated with known-malicious IPs.
// Data sources: ThreatIntelIndicators, CommonSecurityLog
// version:     1.0
// ===================
let dt_lookBack = 1h;
let ioc_lookBack = 14d;
let IPRegex = '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}';
let IP_Indicators = ThreatIntelIndicators
| extend IndicatorType = replace(@"\[|\]|\"", "", tostring(split(ObservableKey, ":", 0)))
| where IndicatorType in ("ipv4-addr", "ipv6-addr", "network-traffic")
| extend NetworkSourceIP = toupper(ObservableValue)
| where TimeGenerated >= ago(ioc_lookBack)
| where ipv4_is_private(NetworkSourceIP) == false
| summarize LatestIndicatorTime = arg_max(TimeGenerated, *) by Id, ObservableValue
| where IsActive and (ValidUntil > now() or isempty(ValidUntil));
IP_Indicators
| join kind=innerunique (
    CommonSecurityLog
    | where TimeGenerated >= ago(dt_lookBack)
    | extend MessageIP = extract(IPRegex, 0, Message)
    | extend CS_ipEntity = iff(
        (not(ipv4_is_private(SourceIP)) and isnotempty(SourceIP)), SourceIP, DestinationIP)
    | extend CS_ipEntity = iff(
        isempty(CS_ipEntity) and isnotempty(MessageIP), MessageIP, CS_ipEntity)
) on $left.NetworkSourceIP == $right.CS_ipEntity
| where TimeGenerated < ValidUntil
| summarize
    MatchTime = arg_max(TimeGenerated, *)
    by Id, CS_ipEntity
| project MatchTime, SourceIP, DestinationIP, DeviceVendor, DeviceProduct,
    TI_ipEntity = NetworkSourceIP, LogSeverity, DeviceAction, ValidUntil, Confidence
```

### Pattern 3: Ransomware Precursor Activity (Impact)

Maps to: MITRE T1490 (Inhibit System Recovery), T1489 (Service Stop), T1070.001 (Indicator Removal: Clear Windows Event Logs).

```kusto
// === HUNTING QUERY ===
// Name:        MDE: Ransomware Precursor Behaviours
// MITRE:       Impact | T1490 - Inhibit System Recovery
// Description: Aggregates evidence of ransomware precursor commands:
//              shadow copy deletion, backup tampering, service stopping,
//              event log clearing. Multiple signals on the same device
//              within 1 day are high-confidence indicators.
// Data sources: DeviceProcessEvents (Defender for Endpoint)
// version:     1.0
// ===================
let lookback = 1d;
let evidenceThreshold = 2;
DeviceProcessEvents
| where Timestamp > ago(lookback)
| where (
    FileName =~ "vssadmin.exe" and ProcessCommandLine has_any("list shadows", "delete shadows")
    or FileName =~ "fsutil.exe" and ProcessCommandLine has "usn" and ProcessCommandLine has "deletejournal"
    or ProcessCommandLine has "bcdedit" and ProcessCommandLine has_any("recoveryenabled no", "bootstatuspolicy ignoreallfailures")
    or ProcessCommandLine has "wbadmin" and ProcessCommandLine has "delete" and ProcessCommandLine has_any("backup", "catalog")
    or (ProcessCommandLine has "wevtutil" and ProcessCommandLine has "cl")
    or (ProcessCommandLine has "wmic" and ProcessCommandLine has "shadowcopy delete")
)
| extend
    ShadowDelete = iff(ProcessCommandLine has "shadowcopy delete" or (FileName =~ "vssadmin.exe" and ProcessCommandLine has "delete shadows"), 1, 0),
    BcdEdit = iff(ProcessCommandLine has "bcdedit" and ProcessCommandLine has_any("recoveryenabled no", "bootstatuspolicy ignoreallfailures"), 1, 0),
    Wbadmin = iff(ProcessCommandLine has "wbadmin" and ProcessCommandLine has "delete", 1, 0),
    EventLogClear = iff(ProcessCommandLine has "wevtutil" and ProcessCommandLine has "cl", 1, 0)
| summarize
    EvidenceCount = sum(ShadowDelete) + sum(BcdEdit) + sum(Wbadmin) + sum(EventLogClear),
    Commands = make_set(ProcessCommandLine, 20),
    FirstSeen = min(Timestamp),
    LastSeen = max(Timestamp)
    by DeviceId, DeviceName, bin(Timestamp, 6h)
| where EvidenceCount >= evidenceThreshold
| project LastSeen, DeviceName, DeviceId, EvidenceCount, Commands, FirstSeen
| order by EvidenceCount desc
```

### Pattern 4: MITRE T1078 Behaviour via UEBA

Maps to: MITRE T1078 (Valid Accounts), T1106 (Native API).

```kusto
// === HUNTING QUERY ===
// Name:        UEBA: Valid Account Abuse via BehaviorAnalytics
// MITRE:       Initial Access | T1078 - Valid Accounts
// Description: Surfaces users whose behaviour (access patterns, location,
//              resource usage) has been flagged as anomalous by UEBA,
//              focusing on T1078 technique detections.
// Data sources: BehaviorInfo, BehaviorAnalytics
// version:     1.0
// ===================
BehaviorInfo
| where TimeGenerated > ago(7d)
| where AttackTechniques has "T1078"
| extend AF = parse_json(AdditionalFields)
| extend TableName = tostring(AF.TableName)
| join kind=leftouter (
    BehaviorAnalytics
    | where TimeGenerated > ago(7d)
    | project UsersInsights, DevicesInsights, ActivityInsights, InvestigationPriority, UserPrincipalName
) on UserPrincipalName
| project TimeGenerated, Title, Description, TableName,
    UserPrincipalName, InvestigationPriority, UsersInsights, ActivityInsights
| order by InvestigationPriority desc
```

---

## Bookmark-to-Incident Promotion

When a hunting query returns a suspicious result:

1. Select the row in the Sentinel **Hunting** blade.
2. Create a **Bookmark** for the result. Bookmarks preserve the raw query result with a timestamp and allow annotation.
3. Optionally attach the bookmark to an existing incident (if the result is related to an active investigation) or promote it to a **new incident**.
4. Bookmarks appear in the investigation graph, allowing analysts to visually connect entities across bookmarks and alerts.

Entity columns in the query (AccountName, IPAddress, HostName) are automatically resolved to Sentinel entity objects in the bookmark. This is why entity projection in every query is mandatory.

---

## Query Version Control

Store all hunting queries in Git using one of two methods:

1. **Sentinel Repositories (preferred):** connect the Sentinel workspace to a GitHub or Azure DevOps repository. Hunting queries stored as `.yaml` files (Sentinel ARM format) are deployed and synced automatically. Pull-request review applies the same code-review process as application code changes.
2. **ARM export:** export analytics rules and hunting queries from the portal as ARM templates and commit them to Git. Less automated than Repositories but suitable when the Repositories feature is not available or desired.

Query file naming convention: `<data-source>-<threat-behavior>-<mitre-technique-id>.yaml`. Example: `azureactivity-bulk-role-assignment-T1098.yaml`.

---

## Watchlist Integration in Hunting Queries

Reference watchlists in hunting queries to suppress known-good entities or focus on known-bad entities:

```kusto
// Exclude known-safe service account callers from role assignment hunting
let AllowedCallers = _GetWatchlist('AllowedServiceAccounts') | project SearchKey;
AzureActivity
| where TimeGenerated > ago(14d)
| where OperationNameValue =~ "microsoft.authorization/roleassignments/write"
| where ActivityStatusValue =~ "Success"
| where Caller !in (AllowedCallers)
| summarize count() by Caller, CallerIpAddress, ResourceId
```

Watchlist alias names must be documented in the watchlist design (see `soar-playbooks.md` for watchlist governance).
