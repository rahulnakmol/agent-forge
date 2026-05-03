# Error Budgets Reference

**Used by**: `sre-architect` Step 3  
**Related**: `sli-slo-design.md`, `burn-rate-alerting.md`

---

## Principle

Error budgets are real budgets. When the budget is exhausted, features stop shipping and engineering time shifts to reliability work. Teams that treat error budgets as advisory maintain SLOs on paper while silently degrading in production.

---

## Calculating the Error Budget

```
error_budget_fraction = 1 - SLO_target
error_budget_minutes  = error_budget_fraction * window_minutes
```

Common calculations (28-day window = 40,320 minutes):

| SLO target | Error budget fraction | Error budget (28 days) |
|---|---|---|
| 99.0% | 1.0% | 403.2 minutes (6h 43m) |
| 99.5% | 0.5% | 201.6 minutes (3h 22m) |
| 99.9% | 0.1% | 40.3 minutes |
| 99.95% | 0.05% | 20.2 minutes |
| 99.99% | 0.01% | 4.0 minutes |

Choose SLO targets deliberately. A 99.99% SLO gives only 4 minutes of downtime per month. Any deployment, configuration change, or dependency hiccup consumes it. For most production services, 99.9% is a strong starting point; 99.99% is appropriate only for systems where brief unavailability causes material financial or safety harm.

---

## Error Budget Tracking (KQL)

Store daily error budget consumption in a Log Analytics custom table or derive it from the SLO signal query. Example: track remaining budget percentage.

```kusto
// Compute remaining error budget % over the last 28 days
let slo_target = 0.999;
let window = 28d;
let budget_fraction = 1.0 - slo_target;
let window_minutes = 28.0 * 24.0 * 60.0;
requests
| where timestamp > ago(window)
| summarize
    total = count(),
    failed = countif(success == false)
| extend
    actual_error_rate = todouble(failed) / todouble(total),
    error_budget_consumed_fraction = (todouble(failed) / todouble(total)) / budget_fraction,
    remaining_budget_pct = (1.0 - (todouble(failed) / todouble(total)) / budget_fraction) * 100.0
```

Surface this query as an Azure Workbook panel pinned to the SLO summary dashboard. Update weekly in the team standup review.

---

## Error Budget Governance Tiers

| Budget remaining | Policy | Who owns the decision |
|---|---|---|
| > 50% | Normal velocity. Feature and reliability work proceed in parallel. | Team |
| 25 - 50% | Reliability caution. Each sprint must contain at least one reliability-improving item. Inform engineering manager. | Team lead |
| 10 - 25% | Reliability focus. Non-critical feature work paused. All sprint capacity reviewed by engineering manager. | Engineering manager |
| < 10% | Feature freeze. All available engineering time on reliability. Escalate to engineering leadership with a recovery plan. | Engineering director |
| Exhausted (0%) | Full stop. No new features until budget recovers to 25%+. Post-mortem required if not already done. Communicate SLA risk to account managers. | Engineering leadership |

---

## Error Budget Policy Document

Produce a one-page policy document per service. Store under `docs/sre/error-budget-policy-<service>.md`. Include:

1. Service name and SLO list.
2. Budget governance tiers (copy from above, tuned per service).
3. Review cadence: weekly sprint review + monthly leadership rollup.
4. Named owner: the team lead or SRE responsible for SLO health.
5. Escalation path when budget reaches < 10%.
6. Freeze criteria and unfreeze criteria.

---

## Error Budget and Feature Releases

Link the error budget to the release pipeline (coordinate with `/cicd-architect`):

- Add a budget gate in the CI/CD pipeline: query current remaining budget before allowing deployment to production.
- If budget < 10%: block deployment automatically; require engineering manager override with a justification comment.
- If budget is exhausted: block all deployments except rollbacks and hotfixes.

Example Azure DevOps pipeline gate (PowerShell task):

```powershell
# Query remaining error budget from Log Analytics
$query = @"
requests
| where timestamp > ago(28d)
| summarize total=count(), failed=countif(success==false)
| extend remaining = (1.0 - (todouble(failed)/todouble(total)) / 0.001) * 100.0
| project remaining
"@

$result = Invoke-AzOperationalInsightsQuery -WorkspaceId $env:LA_WORKSPACE_ID -Query $query
$remainingBudget = $result.Results.remaining

if ([double]$remainingBudget -lt 10.0) {
    Write-Error "Error budget below 10% ($remainingBudget%). Deployment blocked. Override required."
    exit 1
}
```

---

## Common Error Budget Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Setting SLO targets without baseline data | SLO is aspirational, not achievable | Measure 30-day baseline before setting targets |
| Treating error budget as a hard 0/1 gate only | Teams game the SLO to avoid the freeze | Use graduated tiers; make 25% the action trigger |
| Not tracking budget consumption rate | Budget exhausts as a surprise | Weekly KQL review + burn-rate alerting |
| Silently excluding incidents | SLO looks healthy while customers suffer | Maintain a public exclusion log; audit quarterly |
| Not linking budget to engineering priorities | Budget exhausts but features keep shipping | Embed budget gate in sprint planning and CI/CD |
| SLO target set by business, not engineering | Engineers own targets they cannot achieve | SLO targets require engineering sign-off |
