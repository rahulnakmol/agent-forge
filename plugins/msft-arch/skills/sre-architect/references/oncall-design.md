# On-Call Rotation Design Reference

**Used by**: `sre-architect` Step 6  
**Tooling**: PagerDuty or Opsgenie (preferred); Azure Monitor action groups as the alert entry point

---

## Principles

- Minimum 2 engineers in primary rotation. Single-person on-call is a safety and sustainability risk.
- Primary responds within 5 minutes for critical (fast-burn) alerts.
- Secondary escalates automatically if primary does not acknowledge within 10 minutes.
- On-call schedule published 2 weeks ahead. Swap requests handled asynchronously via tooling.
- Post-rotation retrospective: 30 minutes each rotation end to review alert quality.

---

## Rotation Models by Team Size

### 2 - 4 Engineers

**Model**: weekly rotation, single tier, secondary is next week's primary.

```
Week 1: Alice (primary)  Bob (secondary)
Week 2: Bob (primary)    Alice (secondary)
Week 3: Charlie (primary) Alice (secondary)
...
```

Constraints: with only 2 engineers, on-call burden is heavy. Prioritize toil reduction and automation to reduce interrupt load. Track on-call burden hours; if either engineer exceeds 8 hours/week of interrupt time, escalate to hire or redistribute.

### 5 - 8 Engineers

**Model**: weekly rotation, primary and secondary tiers, 1-week offset between tiers.

```
Week 1: Alice (P), Bob (S)
Week 2: Charlie (P), Alice (S)
Week 3: Bob (P), Charlie (S)
...
```

Secondary escalation policy: auto-page secondary if primary does not acknowledge in 10 minutes.

### 9+ Engineers

**Model**: follow-the-sun with regional handoffs. Dedicated incident commander (IC) rotation if SLO tier requires it.

```
APAC shift (00:00 - 08:00 UTC): 2-engineer rotation
EMEA shift (08:00 - 16:00 UTC): 2-engineer rotation
Americas shift (16:00 - 00:00 UTC): 2-engineer rotation
```

Handoff process: 15-minute overlap between shifts. Outgoing on-call posts a handoff note to the incident channel: open alerts, ongoing investigations, context.

---

## On-Call Tooling Configuration

### PagerDuty Setup

1. **Service**: one PagerDuty service per Azure workload or bounded context.
2. **Escalation policy**: primary paged first; auto-escalate to secondary after 10 minutes; auto-escalate to engineering manager after 30 minutes unacknowledged.
3. **Schedule**: weekly rotation. Configuring via Terraform PagerDuty provider is preferred over manual portal setup.
4. **Azure Monitor integration**: configure Azure Monitor action group with PagerDuty webhook. Set the PagerDuty service integration key as a Key Vault secret; reference in action group via Key Vault reference (do not hardcode in Terraform state).

### Opsgenie Setup

1. **Team**: create a team per service or bounded context.
2. **Rotation**: weekly rotation configured in the team schedule.
3. **Escalation**: primary -> secondary (10 min) -> manager (30 min).
4. **Azure Monitor integration**: use the Opsgenie Azure Monitor integration. Configure via Terraform `opsgenie_integration` resource.

### Azure Monitor Action Groups

Action groups are the Azure-native alert entry point. Configure:

```hcl
resource "azurerm_monitor_action_group" "oncall_critical" {
  name                = "oncall-critical"
  resource_group_name = var.resource_group_name
  short_name          = "oncall-crit"

  webhook_receiver {
    name                    = "pagerduty"
    service_uri             = var.pagerduty_webhook_url
    use_common_alert_schema = true
  }

  microsoft_teams_receiver {
    name    = "teams-incident-channel"
    channel_webhook = var.teams_webhook_url
  }
}

resource "azurerm_monitor_action_group" "oncall_warning" {
  name                = "oncall-warning"
  resource_group_name = var.resource_group_name
  short_name          = "oncall-warn"

  webhook_receiver {
    name                    = "create-ticket"
    service_uri             = var.ticket-creation-webhook
    use_common_alert_schema = true
  }

  microsoft_teams_receiver {
    name    = "teams-sre-channel"
    channel_webhook = var.teams_sre_webhook_url
  }
}
```

**Critical action group**: Teams webhook + PagerDuty/Opsgenie. Used for fast-burn alerts.  
**Warning action group**: Teams webhook + ticket creation. Used for slow-burn alerts. No phone page.  
Never use email-only action groups for critical alerts.

---

## On-Call Health Metrics

Track these metrics per rotation. Report monthly to engineering management.

| Metric | Target | Alert if |
|---|---|---|
| Mean time to acknowledge (MTTA) | < 5 minutes for P1 | > 10 minutes |
| Mean time to resolve (MTTR) | < 60 min for P1, < 4h for P2 | Trending upward 3 rotations |
| Alert noise ratio | > 80% actionable | < 60% actionable |
| On-call interrupt hours per rotation | < 8 hours/week | > 8 hours/week for 2 consecutive rotations |
| Repeat alerts (same root cause > 1x) | 0 repeat P1 per window | Any repeat P1 |

**Alert noise ratio**: (alerts that required action / total alerts). An alert that fired but required no action is noise. Noise ratio below 80% triggers an alert quality review.

---

## On-Call Compensation and Sustainability

Define compensation policy before the first rotation:
- On-call stipend per rotation (per company policy).
- Time-off after a heavy rotation (incidents consuming > 6 hours of interrupt time): recommend 1 day of recovery time per 6 hours of night-time interrupt.
- Hard limits: no engineer on-call for more than 2 consecutive weeks without a break.
- Escalation right: on-call engineer may escalate to the engineering manager at any time without requiring justification.

---

## Maintenance Windows and Suppression

For planned maintenance (deployments, infrastructure changes):

1. Create a maintenance window in PagerDuty/Opsgenie (suppresses alerts for the window duration).
2. Notify stakeholders 24 hours before the window.
3. Have the on-call engineer actively monitoring during the window (maintenance window suppresses pages, not monitoring).
4. Close the maintenance window as soon as the work completes. Never leave a maintenance window open "just in case."

---

## On-Call Runbook Checklist

Every on-call rotation starts with this 5-minute onboarding check:

- [ ] Confirm access to Azure portal, Log Analytics workspace, App Insights.
- [ ] Confirm PagerDuty/Opsgenie app is installed on phone and notifications are enabled.
- [ ] Review open alerts and ongoing investigations from the previous rotation's handoff note.
- [ ] Confirm all P1 alert runbooks are marked "Verified" (last-tested < 90 days).
- [ ] Confirm escalation contacts are up to date in `docs/escalation-contacts.md`.

Every on-call rotation ends with this 5-minute offboarding and 30-minute retrospective:

- [ ] Post handoff note to the incident channel: open alerts, ongoing investigations, context.
- [ ] Log on-call burden hours for the rotation.
- [ ] Retrospective: review alert quality (noise ratio), any stale runbooks encountered, any toil patterns observed.
- [ ] Open tickets for any toil items identified during the rotation.
