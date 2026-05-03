# Runbook Authoring Reference

**Used by**: `sre-architect` Steps 7 and 8  
**Store runbooks at**: `docs/runbooks/<alert-name>.md`

---

## Principle

Runbooks are living documents: if not tested in the last 90 days, assume stale. A runbook that has not been exercised since the last infrastructure change, code deployment, or configuration update should be treated as unverified. Schedule quarterly fire-drills and require a merged PR (with updated `last-tested` date) to clear the unverified flag.

---

## Runbook Mandatory Sections

Every runbook must contain all six sections. A runbook missing any section is incomplete and must not be linked from an alert rule.

### 1. Alert Context

- Alert name (exact name as configured in Azure Monitor).
- Alert rule query or metric description.
- Severity (P1 / P2 / P3).
- SLO this alert protects (link to SLO register).
- Expected time-to-respond: P1 = 5 minutes, P2 = 30 minutes, P3 = next business day.

### 2. Triage Steps

Ordered diagnostic steps. Start with the lowest-risk investigation (read-only queries) before any mutating action.

Each step must include:
- The exact command or query to run.
- What a healthy result looks like.
- What an unhealthy result indicates.

KQL example for an availability alert:

```kusto
// 1. Check error rate over last 30 minutes
requests
| where timestamp > ago(30m)
| summarize
    total = count(),
    failed = countif(success == false),
    error_rate = round(todouble(countif(success == false)) / count() * 100, 2)
| project error_rate, failed, total

// 2. Find the failing operations
requests
| where timestamp > ago(30m) and success == false
| summarize count() by name, resultCode
| order by count_ desc
| take 20

// 3. Check exceptions correlated with failures
exceptions
| where timestamp > ago(30m)
| summarize count() by type, outerMessage
| order by count_ desc
| take 10
```

Azure CLI triage:

```bash
# Check App Service health
az webapp show \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --query "{state: state, availabilityState: availabilityState}"

# Check recent deployments (may be root cause)
az webapp deployment list-publishing-credentials \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub>

# Check scaling events
az monitor activity-log list \
  --resource-group <rg> \
  --subscription <sub> \
  --start-time "$(date -u -d '2 hours ago' '+%Y-%m-%dT%H:%M:%SZ')" \
  --query "[?contains(operationName.value, 'autoscale')]"
```

### 3. Mitigation Options

List mitigation actions from safest (no blast radius, reversible) to broadest (service restart, redeploy). Do not skip to the broadest action first.

| Step | Action | Blast radius | Reversible |
|---|---|---|---|
| 1 | Scale out App Service plan by 2 instances | None | Yes (scale back in) |
| 2 | Restart the unhealthy slot only | Single slot | Yes |
| 3 | Swap deployment slot (rollback to last known good) | Full service swap | Yes (swap back) |
| 4 | Restart all instances in the App Service plan | Brief availability impact | Yes |
| 5 | Failover to secondary region | Full traffic shift | Yes (failover back) |

Each action must include the exact command:

```bash
# Scale out (Option 1)
az appservice plan update \
  --name <plan-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --number-of-workers 4

# Slot swap (Option 3)
az webapp deployment slot swap \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --slot staging \
  --target-slot production
```

### 4. Escalation Path

Define who to contact if the runbook steps do not resolve the incident, and when to escalate.

| Condition | Escalate to | Contact method |
|---|---|---|
| Runbook steps exhausted, issue unresolved after 20 minutes | On-call secondary | PagerDuty escalation policy |
| Root cause is in a dependency not owned by this team | Dependency team on-call | Contact list in `docs/teams.md` |
| Data loss suspected | Engineering director | Direct phone (in `docs/escalation-contacts.md`) |
| Security incident suspected | Security team | `security@company.com` + STRIDE-A playbook |

### 5. Rollback Procedure

If the incident was caused or preceded by a deployment:

```bash
# Check deployment history
az webapp deployment list \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --query "[0:5].{id: id, timestamp: lastSuccessEnd, status: status}"

# Rollback via slot swap (preferred: production has last-known-good in staging)
az webapp deployment slot swap \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --slot staging \
  --target-slot production

# Rollback via container tag (if containerized)
az webapp config container set \
  --name <app-name> \
  --resource-group <rg> \
  --subscription <sub> \
  --container-image-name <registry>/<image>:<last-known-good-tag>
```

For IaC-managed resources: trigger a pipeline run pinned to the last known-good git SHA. Do not run `terraform apply` manually against production.

### 6. Post-Incident

After resolving the alert:

1. Confirm the SLO signal has recovered (burn-rate alert has cleared).
2. Create a ticket in the issue tracker for root cause investigation (link: `docs/sre/issue-tracker-url`).
3. If P1 or P2: open a postmortem document from the template in `docs/postmortems/`.
4. Update this runbook if any steps were inaccurate or missing.
5. Update the `last-tested` date in the runbook header.

---

## Runbook Header Template

Every runbook starts with this header:

```markdown
# Runbook: <Alert Name>

| Field | Value |
|---|---|
| Alert name | <exact name in Azure Monitor> |
| Severity | P1 / P2 / P3 |
| SLO | <link to SLO register entry> |
| Last tested | YYYY-MM-DD |
| Last updated | YYYY-MM-DD |
| Owner | <team name> |
| Review due | YYYY-MM-DD (90 days from last-tested) |
| Status | Verified / Unverified (if last-tested > 90 days ago) |
```

Mark a runbook as "Unverified" automatically when the `last-tested` date exceeds 90 days. Use a CI job to scan `docs/runbooks/*.md` headers and open a GitHub Issue for each unverified runbook.

---

## Incident Command Quick Reference

For P1 incidents, the Incident Commander (IC) role is separate from the Operations Lead running the runbook.

**IC responsibilities during active incident:**
1. Assign roles: Operations Lead (runs runbook), Communications Lead (updates stakeholders).
2. Post initial message within 10 minutes: "We are investigating [symptom]. Impact: [description]. Next update in 30 minutes."
3. Post status update every 30 minutes until resolved.
4. Declare resolution: "Incident resolved. Service restored at [HH:MM UTC]. Brief RCA: [one sentence]. Full postmortem within 48 hours."

**IC does not run runbook steps.** IC coordinates, communicates, and makes escalation decisions.

**Incident channel naming**: `#incident-YYYY-MM-DD-<slug>` in Teams or Slack.

**Status page**: update the external status page within 10 minutes of P1 declaration if the incident is customer-impacting.

---

## Quarterly Runbook Review Process

1. 90 days before the `review-due` date: automated CI job opens a GitHub Issue assigned to the runbook owner.
2. Owner schedules a 30-minute fire-drill to execute the runbook against the staging environment or a controlled production scenario.
3. Owner updates the runbook with any corrections.
4. Owner sets `last-tested` to today and `review-due` to today + 90 days.
5. PR merged by a second team member.
6. CI job closes the GitHub Issue.

Runbooks not reviewed within 15 days of the `review-due` date are automatically flagged as "Unverified" in the alert rule description until the review is completed.
