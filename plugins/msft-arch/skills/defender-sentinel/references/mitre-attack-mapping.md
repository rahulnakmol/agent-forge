# MITRE ATT&CK Mapping for Sentinel Analytics Rules

Reference for `/defender-sentinel`. This file covers the required mapping process, technique sets by common Azure data source, and quality gates. The canonical STRIDE-A framework is at `standards/references/security/stride-a-worksheet.md`. Full MITRE technique enumeration by domain is at `threat-model/references/mitre-attack-cloud.md`.

---

## Why MITRE Mapping is Non-Negotiable

Every Sentinel analytics rule must declare at least one MITRE ATT&CK tactic and at least one technique. This is not optional. Three capabilities depend on it:

1. **Fusion correlation:** Fusion uses tactic and technique metadata to correlate related alerts from multiple sources into a single multistage incident. Rules without MITRE mapping produce alerts that Fusion cannot correlate; Fusion quality degrades proportionally to the fraction of unmapped rules.
2. **Coverage visualisation:** the Sentinel MITRE ATT&CK workbook maps active analytics rules against the ATT&CK matrix, showing which techniques are covered and which are blind spots. This is the primary tool for rule gap analysis.
3. **Hunting context:** analysts use the MITRE annotation to understand the threat context of an alert without reading the full rule query. "Privilege Escalation | T1098 Account Manipulation" communicates immediately that the alert is about an attacker modifying account attributes to maintain access.

---

## Tactic and Technique Mapping Reference

Use the ATT&CK Enterprise framework for cloud and on-premises detection. Use the ATT&CK Cloud matrix for Azure-specific techniques.

### Mapping by Azure Data Source

#### Azure Activity (AzureActivity table)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| Bulk role assignments by a single principal | Privilege Escalation | T1098 | Account Manipulation |
| Owner/Contributor role granted to external principal | Privilege Escalation | T1098.001 | Account Manipulation: Additional Cloud Credentials |
| Resource Manager operations from unusual geography | Initial Access | T1078.004 | Valid Accounts: Cloud Accounts |
| Storage account key enumeration | Credential Access | T1552.005 | Unsecured Credentials: Cloud Instance Metadata API |
| Snapshot or disk export | Exfiltration | T1537 | Transfer Data to Cloud Account |
| Resource deletion at scale | Impact | T1485 | Data Destruction |
| Policy modification or diagnostic settings deletion | Defense Evasion | T1562.008 | Impair Defenses: Disable Cloud Logs |
| Unusual resource provisioning (new region, unusual type) | Resource Development | T1583.006 | Acquire Infrastructure: Web Services |

#### Microsoft Entra ID (SigninLogs, AuditLogs)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| Sign-in from impossible travel location | Initial Access | T1078.004 | Valid Accounts: Cloud Accounts |
| Sign-in from anonymising proxy or Tor exit node | Initial Access | T1078.004 | Valid Accounts: Cloud Accounts |
| Mass failed authentication followed by success | Credential Access | T1110.003 | Brute Force: Password Spraying |
| Token refresh from unusual device/OS | Credential Access | T1528 | Steal Application Access Token |
| New service principal credential added | Persistence | T1098.001 | Account Manipulation: Additional Cloud Credentials |
| MFA method modified by attacker | Defense Evasion | T1556.006 | Modify Authentication Process: Multi-Factor Authentication |
| Conditional Access policy disabled | Defense Evasion | T1562 | Impair Defenses |
| New Global Administrator added | Privilege Escalation | T1098 | Account Manipulation |

#### Azure Key Vault (AzureActivity / AzureDiagnostics)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| High-volume secret enumeration | Credential Access | T1555 | Credentials from Password Stores |
| Soft-delete or purge-protection disabled | Defense Evasion | T1562.001 | Impair Defenses: Disable or Modify Tools |
| Access from service principal not expected to query vault | Credential Access | T1555 | Credentials from Password Stores |
| Certificate or key export | Exfiltration | T1552.004 | Unsecured Credentials: Private Keys |

#### Microsoft 365 / Exchange (OfficeActivity table)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| Inbox forwarding rule to external domain | Exfiltration | T1114.003 | Email Collection: Email Forwarding Rule |
| New inbox rule created during anomalous token session | Persistence | T1098 | Account Manipulation |
| Mass email download (PST export, large attachment download) | Collection | T1114.001 | Email Collection: Local Email Collection |
| Mailbox delegation granted to external user | Persistence | T1098 | Account Manipulation |

#### Azure Firewall / CEF Network Logs (CommonSecurityLog)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| Outbound connection to known-malicious IP (TI match) | Command and Control | T1071 | Application Layer Protocol |
| DNS queries to known-malicious domains | Command and Control | T1071.004 | Application Layer Protocol: DNS |
| High-volume outbound data transfer | Exfiltration | T1041 | Exfiltration Over C2 Channel |
| Internal lateral movement (internal IP to internal IP, high port scan) | Lateral Movement | T1021 | Remote Services |
| Port scan pattern from single internal IP | Discovery | T1046 | Network Service Discovery |

#### Defender for Endpoint (DeviceProcessEvents, DeviceNetworkEvents)

| Behaviour to detect | Tactic | Technique ID | Technique |
|---|---|---|---|
| Shadow copy deletion (vssadmin, wmic) | Impact | T1490 | Inhibit System Recovery |
| Event log clearing (wevtutil cl) | Defense Evasion | T1070.001 | Indicator Removal: Clear Windows Event Logs |
| PowerShell download cradles | Execution | T1059.001 | Command and Scripting Interpreter: PowerShell |
| Credential dump (lsass access, mimikatz patterns) | Credential Access | T1003.001 | OS Credential Dumping: LSASS Memory |
| Scheduled task creation for persistence | Persistence | T1053.005 | Scheduled Task/Job: Scheduled Task |
| Registry run key for persistence | Persistence | T1547.001 | Boot or Logon Autostart: Registry Run Keys |

---

## MITRE Coverage Gap Analysis

Use the **Sentinel MITRE ATT&CK workbook** (available in Content Hub: `Microsoft Sentinel MITRE ATT&CK workbook`) to visualise rule coverage:

1. Open the workbook in Sentinel.
2. The matrix highlights tactics and techniques covered by active analytics rules (green) vs. gaps (grey).
3. Sort the gap list by: (a) techniques with highest frequency in known threat actor playbooks for the industry vertical; (b) techniques relevant to the data sources you have connected.
4. Prioritise filling gaps in Initial Access, Privilege Escalation, and Exfiltration tactics first (highest attacker utility in Azure environments).

---

## Mapping Quality Gates

Before publishing any analytics rule (via pull request or Sentinel Repositories):

| Gate | Pass criteria |
|---|---|
| Tactic declared | At least one ATT&CK tactic from the Enterprise matrix |
| Technique declared | At least one technique ID (format: T followed by four digits, optionally dot-separated sub-technique) |
| Technique is relevant | The declared technique matches the attacker behaviour the rule actually detects (not a generic catch-all) |
| Entity mapping present | AccountEntity, IPEntity, or HostEntity is mapped to a result column where the data is available |
| Rule name includes tactic | Convention: `<Source>: <Behavior> (<Tactic>)` |

Rules failing any gate must be revised before merging. Add MITRE-mapping review as an explicit pull-request checklist item in the repository's PR template.

---

## MITRE ATT&CK Resources

- Enterprise Matrix: `https://attack.mitre.org/matrices/enterprise/`
- Cloud Matrix (Azure, AWS, GCP): `https://attack.mitre.org/matrices/enterprise/cloud/`
- MITRE ATLAS (AI/ML adversarial threats): `https://atlas.mitre.org/` (see `/threat-model` skill for AI-specific mapping)
- Navigator (technique heatmap for gap analysis): `https://mitre-attack.github.io/attack-navigator/`
