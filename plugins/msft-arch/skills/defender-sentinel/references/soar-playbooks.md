# Sentinel SOAR: Automation Rules, Playbooks, and Watchlists

Reference for `/defender-sentinel`.

---

## Design Principle: Decouple Trigger from Logic

**Non-negotiable:** define the trigger in an automation rule; define the response logic in a Logic Apps playbook. Never hard-wire a playbook directly to an analytics rule.

**Why:**
- A single automation rule can trigger the same playbook for multiple analytics rules (or all rules matching a severity filter), without copying the playbook.
- The automation rule is a lightweight, portal-managed object. The playbook is a Logic App with its own versioning, deployment pipeline, and ARM template. Keeping them separate allows independent deployment.
- Automation rules can also perform simple triage actions (assign owner, set severity, add tasks, close incident) without invoking a playbook at all, reducing Logic Apps execution costs.

---

## Automation Rules

Automation rules are evaluation-ordered rules applied to incidents or alerts when specific conditions are met. They execute synchronously and in the configured order.

### Common Automation Rule Patterns

**Pattern 1: Triage automation (no playbook)**

Conditions: Incident severity = High AND Analytics rule name contains "AzureActivity"
Actions:
1. Assign owner to `soc-lead@contoso.com`
2. Add tag `AzureActivity`
3. Add task: "Review AzureActivity for correlated events in the same subscription within the past 24 hours"

**Pattern 2: Playbook trigger on specific incident type**

Conditions: Analytics rule name = "AzureActivity: Bulk Role Assignment by Single Principal (Privilege Escalation)"
Actions:
1. Run playbook: `Notify-Teams-PrivilegeEscalation`
2. Run playbook: `Enrich-AccountInfo`

**Pattern 3: Auto-close low-fidelity informational alerts**

Conditions: Incident severity = Informational AND Analytics rule name contains "Heartbeat"
Actions:
1. Change status: Closed
2. Set closing classification: False Positive
3. Add comment: "Auto-closed by automation rule: informational heartbeat alert"

**Pattern 4: Time-limited suppression during maintenance windows**

Conditions: (configure to match the maintenance window time range)
Actions:
1. Change status: Closed
2. Set closing classification: True Positive (suppress during maintenance)

**Note:** automation rules support a "Stop evaluating subsequent rules" action that short-circuits further rule evaluation for a matched incident.

---

## SOAR Playbooks via Logic Apps

Playbooks are Logic Apps Standard or Consumption workflows triggered by Sentinel. Use the Microsoft Sentinel Logic Apps connectors (incident trigger, alert trigger, entity trigger).

### Playbook Design Principles

1. **One playbook = one responsibility.** A playbook that enriches an account, notifies Teams, blocks the account, and files a ticket is four playbooks that happen to share a trigger. Split them. Compose them with automation rules.
2. **Idempotent actions.** Any playbook that modifies external state (blocks a user, isolates an endpoint) must be idempotent: running it twice on the same incident must not cause double actions (block an already-blocked user).
3. **Human-in-the-loop for high-impact actions.** Playbooks that isolate endpoints, disable accounts, or revoke certificates must include an approval step (Teams Adaptive Card or email approval) before executing the destructive action.
4. **Error handling.** Every connector action must have a failure path configured. Log failures to a custom Log Analytics table or send a Teams notification. Silent failures in automated playbooks are a SOC anti-pattern.
5. **Deployment via ARM template.** Export the Logic App as an ARM template and store in Git. Parameter files per environment (dev/staging/prod). Deploy via IaC pipeline.

### Common Playbook Library

| Playbook name | Trigger | Actions | Human-in-loop? |
|---|---|---|---|
| `Notify-Teams-Incident` | Any incident (severity High/Critical) | Post adaptive card to SOC Teams channel with incident details, entity list, and direct link | No |
| `Enrich-AccountInfo` | Any incident with AccountEntity | Lookup user in Entra ID (display name, job title, manager, last sign-in, risk score); add as incident comment | No |
| `Block-EntraUser` | Incident type: Account Compromise (after analyst confirmation) | Set Entra ID user risk to high; disable sign-in; revoke all refresh tokens | Yes (Teams approval step) |
| `Isolate-MDE-Endpoint` | Incident type: Ransomware Precursor or Malware Execution | Call Defender for Endpoint API to isolate device from network | Yes (Teams approval step) |
| `Open-ServiceNow-Incident` | Any Critical incident | Create ServiceNow incident with Sentinel incident ID, title, severity, and entity list; add ServiceNow ticket ID as Sentinel comment | No |
| `Add-TI-Block-to-Watchlist` | Hunting bookmark with malicious IP confirmed | Append IP to `BlockListIPs` watchlist CSV and update the Sentinel watchlist | No |

### Playbook ARM Template Pattern

Logic Apps deploy as ARM templates. Key elements for Sentinel integration:

```json
{
  "type": "Microsoft.Logic/workflows",
  "name": "[parameters('PlaybookName')]",
  "properties": {
    "definition": {
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "triggers": {
        "Microsoft_Sentinel_incident": {
          "type": "ApiConnectionWebhook",
          "inputs": {
            "host": {
              "connection": { "name": "@parameters('$connections')['azuresentinel']['connectionId']" }
            },
            "path": "/incident-creation"
          }
        }
      }
    }
  }
}
```

Use the ARM Template Generator to export existing playbooks from the portal:
`https://techcommunity.microsoft.com/t5/microsoft-sentinel-blog/export-microsoft-sentinel-playbooks-or-azure-logic-apps-with/ba-p/3275898`

---

## Watchlists

Watchlists are CSV-backed reference tables queried from KQL in analytics rules and hunting queries using `_GetWatchlist('alias')`.

### Watchlist Governance Rules

1. **Version-control the source CSV in Git.** The CSV file is the authoritative source; the Sentinel watchlist is the deployed artifact. Use the same discipline as IaC: Git is truth.
2. **One watchlist per semantic category.** Do not combine allow-list and block-list data in the same watchlist.
3. **Document the schema** (column names and types) in the CSV header row and in a companion `README.md` in the same Git directory.
4. **Automate updates for dynamic lists.** Block-list watchlists sourced from threat intelligence feeds should be updated automatically via a Logic Apps playbook or Azure Function (not manually).
5. **Review allow-lists quarterly.** Stale allow-list entries (service accounts that no longer exist, IP ranges that have been decommissioned) generate false negatives. Schedule a quarterly review.

### Standard Watchlist Catalog

| Watchlist alias | Purpose | Source | Update cadence |
|---|---|---|---|
| `AllowedServiceAccounts` | UPNs of service accounts that are expected to perform privileged ARM operations; excluded from role-assignment hunting queries | AD/Entra ID group export | Monthly |
| `AllowedAdminIPs` | IP ranges of corporate VPN and trusted admin workstations; excluded from impossible-travel and anomalous-location rules | Network team | Quarterly |
| `BlockListIPs` | IP addresses confirmed as malicious from threat intelligence feeds or SOC investigation | TI connector + manual SOC additions | Daily (automated from TI) |
| `BlockListDomains` | DNS domains confirmed malicious; used in DNS hunting queries | TI connector + manual SOC additions | Daily (automated from TI) |
| `HighValueAssets` | Resource IDs of crown-jewel assets (Key Vaults holding production secrets, databases with PII, storage accounts with financial data); used to elevate alert severity when these assets are involved | Architecture team | Per-deployment |
| `SensitiveRoles` | Azure RBAC role names considered high-privilege for the organisation (Owner, Contributor on production subscriptions, Key Vault Administrator); used in privilege-escalation detection rules | Security team | Per-policy change |

### Referencing Watchlists in KQL

```kusto
// Check if an IP is in the block list
let BlockedIPs = _GetWatchlist('BlockListIPs') | project SearchKey;
CommonSecurityLog
| where TimeGenerated > ago(1d)
| where SourceIP in (BlockedIPs) or DestinationIP in (BlockedIPs)
| project TimeGenerated, SourceIP, DestinationIP, DeviceVendor, DeviceAction

// Elevate severity when a high-value asset is involved
let HighValueAssets = _GetWatchlist('HighValueAssets') | project ResourceId = SearchKey;
AzureActivity
| where TimeGenerated > ago(1d)
| where OperationNameValue hassuffix "delete"
| where ActivityStatusValue =~ "Success"
| join kind=inner (HighValueAssets) on ResourceId
| project TimeGenerated, ResourceId, Caller, OperationNameValue
```

---

## SOAR Testing

Before deploying playbooks to production:

1. Test against a Sentinel **test incident** (create a synthetic incident manually).
2. Verify the playbook run history in the Logic Apps blade; check every action's input and output.
3. Test the approval path: confirm the Teams Adaptive Card renders correctly and both Approve and Reject paths execute correctly.
4. Test failure paths: temporarily misconfigure a connector to confirm the error notification fires.
5. Test idempotency: run the playbook twice on the same incident; confirm no duplicate actions occur.

Document the test results in a pull-request comment before merging the ARM template to the main branch.
