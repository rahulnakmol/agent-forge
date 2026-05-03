# Postmortem Template

**Used by**: `sre-architect` Step 9  
**Store at**: `docs/postmortems/YYYY-MM-DD-<incident-slug>.md`

---

## Principles

- **Blameless**: the question is "what failed in the system?" not "who made the mistake?" Blame produces silence in future incidents.
- **Time-bound**: draft within 48 hours of resolution; reviewed and published within 5 business days.
- **Action-oriented**: every postmortem produces action items with owners and due dates tracked in the issue tracker.
- **Mandatory triggers**: P1 incidents always produce a postmortem. P2 incidents produce a postmortem. P3 incidents produce a postmortem at team discretion.

---

## Template

Copy this template to `docs/postmortems/YYYY-MM-DD-<slug>.md` immediately after incident resolution.

```markdown
# Postmortem: <Incident title>

**Date**: YYYY-MM-DD  
**Severity**: P1 / P2 / P3  
**Duration**: HH:MM (detection to resolution)  
**Author(s)**: <names>  
**Status**: Draft / In Review / Published  
**Issue tracker**: <link to tracking issue>

---

## Impact Summary

- **User impact**: What did users experience? What features were unavailable or degraded?
- **Duration**: When did the impact start? When was it resolved?
- **Scope**: How many users, requests, or data records were affected?
- **SLO impact**: Did the incident consume error budget? How much? Is the SLO at risk for the current window?

---

## Timeline

All times in UTC.

| Time (UTC) | Event |
|---|---|
| HH:MM | [DETECTION] Alert fired / user report received |
| HH:MM | [ACKNOWLEDGE] On-call acknowledged alert |
| HH:MM | [INCIDENT DECLARED] Incident channel opened; IC assigned |
| HH:MM | [DIAGNOSIS] Root cause identified: [brief description] |
| HH:MM | [MITIGATION] Mitigation applied: [brief description] |
| HH:MM | [RESOLUTION] Service restored to normal; monitoring confirmed |
| HH:MM | [ALL-CLEAR] IC posted resolution notice |

---

## Root Cause

Describe the technical root cause without attributing blame to individuals.

- What component failed or behaved unexpectedly?
- What triggered the failure (deployment, traffic spike, dependency outage, configuration change)?
- What conditions allowed the failure to propagate?

---

## Detection

- How was the incident detected? (Alert, user report, health check)
- Was detection timely? If not, what gap exists in observability?
- Time from impact start to detection: HH:MM

---

## Resolution

- What steps resolved the incident?
- Was the runbook followed? Was it accurate?
- Was the resolution a mitigation (workaround) or a fix (root cause addressed)?

---

## Contributing Factors

List conditions that contributed to the incident or its impact. Do not list people.

- [ ] Missing alert or monitoring gap
- [ ] Insufficient test coverage (chaos experiment or integration test would have caught this)
- [ ] Runbook absent or stale
- [ ] Deployment without canary or feature flag
- [ ] Dependency SLO not accounted for
- [ ] Insufficient error handling in code (missing circuit breaker, retry, fallback)
- [ ] Configuration drift between environments
- [ ] Other: [describe]

---

## What Went Well

- [List things that worked as expected during the incident: alerting, communication, on-call response, tooling]

---

## Action Items

Track all action items in the team issue tracker. Each item in this table must correspond to an open issue/ticket at the time of postmortem publication.

| # | Action | Owner | Due date | Severity | Issue link |
|---|---|---|---|---|---|
| 1 | | | YYYY-MM-DD | Blocker / High / Medium | |
| 2 | | | YYYY-MM-DD | | |

Action item severity:
- **Blocker**: must be resolved before the next production deployment.
- **High**: must be resolved within 2 sprints.
- **Medium**: must be resolved within the current quarter.

---

## Lessons Learned

2-3 sentences on the key takeaway from this incident for the team and for the system design.

---

## SLO Impact Log

| SLO | Target | Budget consumed this incident | Running budget remaining (window) |
|---|---|---|---|
| orders-api availability | 99.9% | X minutes | Y% |
```

---

## Postmortem Review Meeting

- Duration: 60 minutes maximum.
- Attendees: IC, Operations Lead, and any engineers who worked the incident. Engineering manager optional but encouraged for P1.
- Agenda:
  1. Timeline walk-through (15 min): confirm the timeline is accurate.
  2. Root cause review (10 min): confirm technical understanding.
  3. Action items (25 min): review, assign owners, set due dates. Every item must have a single named owner.
  4. Process improvements (10 min): what would have made this incident shorter or less impactful?

Rules for the meeting:
- No blame. If a person's name appears in the discussion of root cause, reframe to the system condition ("the deployment gate did not exist" not "Alex deployed without testing").
- Action items are recorded in the tracker before the meeting ends. "We'll figure it out later" items do not get tracked.

---

## Postmortem Publication

- Published postmortems live in `docs/postmortems/` in the repository.
- For customer-impacting incidents: the SLO/SLA team reviews whether a summary should be shared with customers or posted to a status page.
- Postmortem index maintained at `docs/postmortems/README.md` (table of incidents, date, severity, link).

---

## Escalation: Repeat Incidents

If the same root cause produces two P1 incidents within a single SLO window:
1. Escalate to engineering director.
2. Create a reliability epic in the issue tracker.
3. Hold the error budget freeze (see `error-budgets.md`) until the reliability epic is resolved.
