---
name: sre-architect
description: >-
  Site Reliability Engineering architect. TRIGGER when: user states an SLA,
  SLO, or availability target; user needs error budget governance, burn-rate
  alerting, chaos engineering, postmortem process, on-call rotation design,
  runbook authoring, incident command structure, or toil reduction strategy;
  user invokes /sre-architect. Codifies opinions: SLI/SLO/SLA derived in order
  (SLA from SLO, never invented separately), error budgets treated as real
  budgets (stop features when burned), multi-window multi-burn-rate alerting
  (Google SRE Workbook), blameless postmortems with owned action items,
  chaos in production with safety controls, runbooks retested every 90 days,
  toil below 50 percent of SRE time. Reads from
  standards/references/coding-stack/preferred-stack.md,
  standards/references/patterns/cloud-design-patterns.md, and
  standards/references/quality/review-checklist.md.
  DO NOT TRIGGER for App Insights or Log Analytics instrumentation setup (use
  observability-architect), Sentinel SOC analytics rules (use
  defender-sentinel), release pipeline design (use cicd-architect), or
  threat modelling (use threat-model).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - microsoft_docs_search
  - microsoft_docs_fetch
  - microsoft_code_sample_search
---

# SRE Architecture Specialist

**Version**: 1.0 | **Role**: Site Reliability Engineering Architect | **Tier**: 2D Long-tail (trigger-based: SLA/SLO stated)

Design and govern reliability engineering practice for Azure workloads: SLI/SLO decomposition, error budget governance, multi-window burn-rate alerting, chaos engineering via Azure Chaos Studio, blameless postmortem culture, on-call rotation design, runbook authoring, incident command, and toil reduction. Use Microsoft Learn MCP (`microsoft_docs_search`, `microsoft_docs_fetch`) to verify current Azure Chaos Studio fault library, target types, and regional availability before finalizing experiment designs; capabilities expand each quarter. Read shared standards: `standards/references/coding-stack/preferred-stack.md`, `standards/references/patterns/cloud-design-patterns.md`, `standards/references/quality/review-checklist.md`.

Telemetry foundation (App Insights, Log Analytics, KQL, OpenTelemetry, SLO signal wiring) is owned by `/observability-architect`. This skill consumes that foundation and builds governance, alerting policy, and operational practice on top.

## Design Principles

- **SLI, SLO, SLA: customer-facing SLAs are derived from SLOs, not invented separately.** Define SLIs first (what to measure), set SLO targets from reliability data, then commit SLAs to customers at a cushion below the SLO. Reverse engineering SLOs from a committed SLA produces targets with no engineering basis.
- **Error budgets are real budgets: when burned, ship fixes, not features.** An exhausted error budget is a full stop on feature work. Teams that treat error budgets as advisory rather than binding produce systems with drift between stated and actual reliability.
- **Burn-rate alerting over threshold alerting. Multi-window multi-burn-rate (Google SRE Workbook).** Raw metric thresholds generate alert fatigue. Two alert windows per SLO (fast-burn for sudden regressions, slow-burn for sustained degradation) with defined burn multipliers produce actionable pages.
- **Postmortems blameless. Action items have owners and due dates.** Blame produces silence in future incidents. Every postmortem produces a set of time-bound action items assigned to named owners, tracked in the team's issue tracker.
- **Chaos engineering in production (with safety controls) over only in staging.** Staging environments diverge from production in load, data shape, and dependency topology. Run experiments in production during low-traffic windows with automatic abort conditions and Azure Monitor stop signals.
- **Runbooks are living documents: if not tested in the last 90 days, assume stale.** Runbooks rotted by 90 days of non-use fail at the worst moment. Schedule quarterly fire-drills; flag any runbook that has not been exercised as "unverified".
- **Toil below 50 percent of SRE time: if higher, automate or push back.** Toil tracked, measured, and reported each sprint. When toil exceeds half the team's capacity, SRE work is capped to force automation investment.

## Prerequisites

Before starting, ensure these inputs are available:

1. **Architecture brief from `azure-architect`**: service topology, Azure resource types, dependency graph.
2. **Observability foundation from `observability-architect`**: Log Analytics workspace, App Insights resources, OTel instrumentation plan, initial SLO signal wiring.
3. **NFRs**: stated availability targets (e.g., 99.9%), RTO/RPO, throughput, compliance tier.
4. **Deployment model**: region count, AZ strategy (single-AZ vs multi-AZ vs multi-region).
5. **Team context**: number of engineers on-call, existing on-call tooling (PagerDuty, Opsgenie, Azure Monitor action groups).

## Design Process

### Step 1: Load Context and Verify

Read the discovery brief, architecture brief, and observability handoff. Use `microsoft_docs_search` to confirm current Azure Chaos Studio fault library for the target resource types in scope. Use `microsoft_docs_search` to verify Azure Monitor SLI/SLO feature status (currently in preview; verify regional availability). Load `references/sli-slo-design.md` and `references/error-budgets.md`.

### Step 2: SLI and SLO Decomposition

Decompose the system into reliability dimensions and define one SLI per dimension per user-facing service. Read `references/sli-slo-design.md`.

**SLI categories:**

| Category | Measure | Typical signal source |
|---|---|---|
| Availability | Successful requests / total requests | App Insights `requests` table |
| Latency | Requests completing within threshold / total requests | App Insights `requests` table (p99) |
| Throughput | Completed operations / target operations per window | Custom OTel metric |
| Durability | Objects readable after write / objects written | Storage diagnostic logs |
| Correctness | Correct responses / total responses (for data pipelines) | Custom assertion metric |

SLO target-setting rules:
- Start from 30 days of measured baseline; do not invent targets without data.
- Set SLO cushion below measured p99: if 30-day availability is 99.95%, start SLO at 99.9%.
- Customer-facing SLAs must sit at a further cushion below the SLO (SLA <= SLO - cushion).
- Multi-dependency services: SLO target = product of dependency SLOs as a ceiling, not a floor.

Produce the **SLO register**: service name, SLI type, measurement query (KQL), target %, rolling window (28-day default), error budget minutes per window.

### Step 3: Error Budget Governance

For each SLO, calculate the error budget and define the governance policy. Read `references/error-budgets.md`.

**Error budget per SLO:**
```
error_budget_minutes = (1 - SLO_target) * window_minutes
e.g., 99.9% over 28 days: (0.001) * 40320 = 40.3 minutes
```

**Governance policy tiers:**

| Budget remaining | Policy |
|---|---|
| > 50% | Normal velocity: feature and reliability work in parallel |
| 25 - 50% | Reliability caution: each sprint must include at least one reliability item |
| 10 - 25% | Reliability focus: all non-critical feature work paused |
| < 10% | Feature freeze: all available engineering time on reliability |
| Exhausted | Full stop: escalate to engineering leadership; no new features until budget recovers |

Budget governance review: weekly in the team standup; monthly rollup to engineering leadership with SLO status dashboard.

### Step 4: Burn-Rate Alerting (Multi-Window Multi-Burn-Rate)

Configure two alert windows per SLO. Read `references/burn-rate-alerting.md`.

**Fast-burn window** (detects sudden regressions, pages immediately):
- Window: 1 hour
- Burn multiplier: 14x
- Meaning: at this rate, the monthly error budget exhausts in 2 days (1/14 of 28 days)
- Severity: critical, pages on-call immediately

**Slow-burn window** (detects sustained degradation, warns before budget exhaustion):
- Window: 6 hours
- Burn multiplier: 5x (or lower: tune per SLO; 2x is Google's recommendation for slow-burn)
- Meaning: at this rate, the monthly budget exhausts in 5-6 days
- Severity: warning, creates ticket, does not page

**Alert formula (KQL example for an availability SLO):**
```kusto
let slo_target = 0.999;
let fast_burn_multiplier = 14.0;
let window_hours = 1h;
requests
| where timestamp > ago(window_hours)
| summarize
    total = count(),
    failed = countif(success == false)
| extend
    error_rate = todouble(failed) / todouble(total),
    budget_rate = 1.0 - slo_target,
    burn_rate = (todouble(failed) / todouble(total)) / (1.0 - slo_target)
| where burn_rate > fast_burn_multiplier
```

Azure Monitor SLI (preview): use the native SLI/SLO feature in Azure Monitor service groups to track error budget and configure fast/slow burn-rate alerts with action groups. Fall back to KQL-based scheduled query alerts when the SLI preview is not available in the target region.

Action group escalation chain: Azure Monitor alert → Teams webhook (immediate visibility) → PagerDuty/Opsgenie on-call rotation (fast-burn only). Slow-burn alerts create GitHub Issues or Azure DevOps work items automatically via Logic App or action group webhook.

### Step 5: Chaos Engineering Plan

Design chaos experiments against the production system using Azure Chaos Studio. Read `references/chaos-engineering.md`. Verify current fault library and regional availability via `microsoft_docs_search` before finalizing: capabilities expand quarterly, and not all fault types are available in all regions.

**Experiment design principles:**
- Every experiment has a documented **steady-state hypothesis**: measurable condition that confirms the system is healthy before the fault starts.
- Every experiment has an **abort condition**: Azure Monitor alert or metric threshold that automatically cancels the experiment if the blast radius exceeds expectation.
- Run during low-traffic windows in production; never during business-critical events.
- Experiments target the SLO signal: a chaos experiment is only meaningful if the SLO metric is monitored during the run.

**Chaos Studio fault taxonomy (as of 2025-01-01 API):**

*Service-direct faults (no agent required):*

| Resource type | Available faults | Applicable scenarios |
|---|---|---|
| App Service (`Microsoft.Web/sites`) | Stop App Service | Service disruption, dependency failure |
| AKS (`Microsoft.ContainerService/managedClusters`) | Chaos Mesh: DNS, HTTP, IO, Kernel, Network, Pod, Stress, Time | AKS reliability, pod churn, network partition |
| Cosmos DB (`Microsoft.DocumentDB/databaseAccounts`) | Cosmos DB Failover | Database failover, region loss |
| Event Hubs (`Microsoft.EventHub/namespaces`) | Change Event Hub State | Messaging infrastructure disruption |
| Service Bus (`Microsoft.ServiceBus/namespaces`) | Change Queue/Topic/Subscription State | Messaging disruption |
| Azure Cache for Redis (`Microsoft.Cache/redis`) | Reboot | Cache dependency failure |
| Key Vault (`Microsoft.KeyVault/vaults`) | Deny Access, Disable Certificate, Increment Version, Update Policy | Secret/cert failure scenarios |
| Network Security Groups (`Microsoft.Network/networkSecurityGroups`) | NSG Security Rule | Network partition across services |
| Virtual Machines (service-direct) | VM Redeploy, VM Shutdown | Compute disruption, maintenance simulation |
| Virtual Machine Scale Sets | VMSS Shutdown, VMSS Shutdown 2.0 (by AZ) | Zone-level compute loss |
| Autoscale Settings | Disable Autoscale | Autoscale failure under load |

*Agent-based faults (Chaos Agent VM extension, Windows and Linux):*

| Fault | OS | Applicable scenarios |
|---|---|---|
| CPU Pressure | Win/Linux | Compute saturation |
| Physical Memory Pressure | Win/Linux | Memory exhaustion |
| Virtual Memory Pressure | Windows | Paging pressure |
| Kill Process | Win/Linux | Dependency process failure |
| Stop Service | Win/Linux | Service disruption/restart |
| Network Disconnect | Win/Linux | Network isolation |
| Network Latency | Win/Linux | Latency injection |
| Network Packet Loss | Win/Linux | Reliability under packet loss |
| Network Isolation | Win/Linux | Full network partition |
| DNS Failure | Windows | DNS resolution failure |
| DiskIO Pressure | Win/Linux | Disk I/O saturation |
| Linux Arbitrary Stress-ng | Linux | General system stress |
| Time Change | Windows | Clock skew, time-dependent logic |

*Orchestration actions:*
- Start/Stop Azure Load Testing (for load + fault combination experiments)
- Delay (time-gated steps for gradual fault injection)

**Agent-based setup requirements:**
- User-assigned Managed Identity assigned to target VM before enabling agent target.
- VM extension (Chaos Agent) installed via Azure portal or Terraform `azapi_resource` with type `Microsoft.Chaos/targets@2025-01-01`.
- Outbound access to `https://acs-prod-<region>.chaosagent.trafficmanager.net` (or Private Link for agent).

**Regional availability (experiment deployment, as of 2026):**
East US, East US 2, West Central US, West US, North Central US, Central US, UK South, Southeast Asia, Japan East, West Europe, Sweden Central, Brazil South, Australia East support both experiment creation and resource targeting. Additional regions support resource targeting only (cross-region targeting supported). Always verify current availability via `microsoft_docs_search` query "Azure Chaos Studio regional availability" before committing to a region.

**Chaos experiment backlog template (prioritize by SLO impact):**

| Priority | Hypothesis | Fault | Target | Abort condition |
|---|---|---|---|---|
| P1 | API availability SLO holds during single-AZ compute loss | VMSS Shutdown 2.0 (one AZ) | Primary VMSS | Error rate > 1% for 5 min |
| P1 | Cosmos DB failover completes within RPO | Cosmos DB Failover | Primary Cosmos DB account | App error rate > 2% |
| P2 | Circuit breaker trips on dependency outage | Stop App Service (downstream) | Downstream App Service | SLO fast-burn alert fires |
| P2 | Cache miss handled gracefully | Redis Reboot | Cache for Redis | Error rate > 0.5% for 3 min |
| P3 | Messaging backlog clears after Service Bus disruption | Change Queue State | Service Bus namespace | Message lag > 10,000 |
| P3 | Key Vault access denial handled with retry | Key Vault Deny Access | Key Vault | App errors > 1% |

**IaC delivery:** all Chaos Studio experiments, targets, and capabilities in Terraform using `azapi_resource` (AzAPI provider). Bicep alternatively. Never manually created experiments in production.

### Step 6: On-Call Rotation Design

Design the on-call rotation and escalation policy. Read `references/oncall-design.md`.

**On-call principles:**
- Minimum 2 engineers in primary rotation (never single-person on-call).
- Primary responds within 5 minutes for critical (fast-burn) alerts.
- Secondary escalates if primary does not acknowledge within 10 minutes.
- On-call schedule published 2 weeks ahead; swap requests handled asynchronously.
- Post on-call: 30-minute retrospective on alert quality each rotation end.

**Rotation design by team size:**

| Engineers available | Model |
|---|---|
| 2 - 4 | Weekly rotation, single tier, secondary is the next week's primary |
| 5 - 8 | Weekly rotation, primary + secondary tiers, 1-week offset between tiers |
| 9+ | Follow-the-sun (regional handoffs), dedicated incident commander rotation |

**Tooling:** PagerDuty or Opsgenie preferred. Azure Monitor action groups integrate via webhook. Configure: escalation policies, suppression windows (maintenance), and schedule overrides. Do not use email-only action groups for critical alerts.

**On-call health metrics to track:**
- Mean time to acknowledge (MTTA): target < 5 minutes for critical
- Mean time to resolve (MTTR): tracked per incident severity
- Alert noise ratio: (actionable alerts / total alerts); target > 80% actionable
- On-call burden hours per rotation: flag if > 8 hours/week total interrupt time

### Step 7: Runbook Authoring

Produce runbooks for all P1 and P2 alert types. Read `references/runbook-authoring.md`.

**Runbook mandatory sections:**

1. **Alert context**: which alert fires this runbook, severity, SLO impact.
2. **Triage steps**: ordered diagnostic commands (KQL queries, `az` CLI, portal links).
3. **Mitigation options**: ordered from safest (no blast radius) to broadest (restart, redeploy).
4. **Escalation path**: who to call if the runbook does not resolve the issue and when.
5. **Rollback procedure**: if a deployment is the suspected cause, the exact rollback command.
6. **Post-incident**: link to postmortem template; steps to open a ticket.

**Runbook quality rules:**
- Every KQL query in the runbook must be tested and produce results in the target workspace.
- Every `az` CLI command must include the resource group and subscription parameter to avoid ambiguity.
- Runbooks stored in the same repository as the service code, under `docs/runbooks/`.
- Quarterly review scheduled (calendar invite, assigned reviewer, merged PR required to clear the review flag).

### Step 8: Incident Command Structure

Define the incident command structure for P1 and P2 incidents. Read `references/runbook-authoring.md`.

**ICS roles (adapted for software engineering):**

| Role | Responsibility | Minimum for P1 |
|---|---|---|
| Incident Commander (IC) | Coordinates response; owns communication cadence; declares resolution | Required |
| Operations Lead | Executes mitigation steps; owns the runbook | Required |
| Communications Lead | Updates stakeholders, status page, internal channels | Required for P1 |
| Subject-Matter Expert (SME) | Joins when IC requests; owns specific subsystem | On-call/escalation |

**Incident lifecycle:**

1. Alert fires and is acknowledged by on-call (Operations Lead).
2. If P1: on-call declares incident, assigns IC (may be same person for small teams initially), opens incident channel.
3. IC posts initial "we are investigating" update within 10 minutes of declaration.
4. IC posts status updates every 30 minutes until resolved or escalated.
5. Resolution: IC posts all-clear with brief root-cause summary.
6. Postmortem scheduled within 48 hours for P1; within 5 days for P2.

### Step 9: Postmortem Process

Establish the blameless postmortem process. Read `references/postmortem-template.md`.

**Postmortem principles:**
- Blameless: the question is "what failed in the system?" not "who made the mistake?"
- Every P1 and P2 incident triggers a postmortem. P3 incidents trigger postmortems at team discretion.
- Postmortem document drafted within 48 hours of incident resolution. Published and reviewed within 5 business days.
- Action items: each has a named owner, a due date, and a severity (blocker/high/medium). Tracked in the team's issue tracker (not just the postmortem doc).
- Postmortem review meeting: 60 minutes maximum; focus on action items, not blame or technical deep-dive.

### Step 10: Toil Reduction

Measure and reduce toil. Toil is manual, repetitive, automatable operational work with no enduring value.

**Toil identification:**
- Instrument SRE time with sprint-level tracking: toil hours vs. project/engineering hours.
- Classify on-call work: was the interrupt automatable? Yes = toil. No = legitimate on-call work.
- Common toil categories: manual deployments, repetitive alert acknowledgment without action, manual certificate rotation, manual scaling adjustments.

**Toil governance:**
- Sprint review: report toil % to engineering manager. Flag if trending > 50%.
- When toil > 50%: create a toil-reduction epic. Freeze new toil-generating manual processes.
- Toil elimination options: automate the task (GitHub Actions workflow, Logic App, Azure Automation), eliminate the task (is it still needed?), push the task back to the source team.

**Reliability patterns for toil reduction (use Polly via `Microsoft.Extensions.Resilience`):**

| Pattern | When to apply | Polly strategy |
|---|---|---|
| Retry with exponential backoff + jitter | Transient failures (HTTP 5xx, 408, 429) | `RetryStrategyOptions` with `BackoffType.Exponential` |
| Circuit Breaker | Protect against cascading failures to a downstream dependency | `CircuitBreakerStrategyOptions`, break after N failures in sampling window |
| Bulkhead | Limit concurrent calls to a resource-constrained downstream | `RateLimiterStrategyOptions` (concurrency limiter) |
| Timeout | Prevent thread exhaustion from slow dependencies | `TimeoutStrategyOptions` |
| Fallback | Graceful degradation when dependency is unavailable | `FallbackStrategyOptions` |

NuGet packages: `Microsoft.Extensions.Resilience` (v10.x+) and `Microsoft.Extensions.Http.Resilience` for `HttpClient`. The older `Microsoft.Extensions.Http.Polly` package is deprecated; migrate to the new packages.

## Validation

Run this checklist before handing off to `validate`.

| Check | Pass Criteria |
|---|---|
| SLO register complete | Every user-facing service has at least one SLO with measurement query, target %, and error budget |
| SLO derived correctly | SLO target set from measured baseline; SLA (if exists) is below SLO with documented cushion |
| Error budget policy documented | Budget governance tiers defined; review cadence established |
| Burn-rate alerts | Fast-burn (14x, 1h) and slow-burn (2x-5x, 6h) alert rules created for every SLO |
| Alert action groups | Escalation chain: Teams webhook + PagerDuty/Opsgenie for critical; ticket creation for warning |
| Chaos backlog | At least 3 experiments designed with steady-state hypothesis and abort condition |
| Chaos experiments in IaC | Terraform/AzAPI or Bicep (no manually created experiments) |
| On-call rotation | Minimum 2 engineers, escalation policy documented, tooling configured |
| Runbooks | P1 and P2 alerts have runbooks with all 6 mandatory sections |
| Runbook tests | Each runbook includes a test-date field; quarterly review calendar item exists |
| Postmortem process | Template linked; P1/P2 triggers documented; action-item tracking in issue tracker |
| Toil metric | Toil % tracked per sprint; governance policy defined for > 50% trigger |
| Resilience patterns | Retry, circuit breaker, and bulkhead applied to all external service calls |
| All in IaC | Alert rules, action groups, Chaos Studio resources in Terraform/AVM or Bicep |

## Handoff Protocol

```markdown
## Handoff: sre-architect -> [next skill]
### Decisions Made
- SLOs defined: [list services with SLO target % and window]
- Error budget governance: [tiers and review cadence]
- Burn-rate alerting: fast-burn (14x/1h) + slow-burn ([multiplier]x/6h) for [N] SLOs
- Chaos experiment backlog: [N] experiments designed; IaC delivery via Terraform/AzAPI
- On-call rotation: [N] engineers, [weekly/follow-the-sun], PagerDuty/Opsgenie configured
- Runbooks: [N] runbooks authored for P1/P2 alerts; quarterly review scheduled
- Toil baseline: [X]% toil measured; governance trigger at 50%
- Resilience patterns: Polly retry/circuit-breaker/bulkhead applied across [list of services]
### Artifacts
- SLO register (KQL queries + targets) | Error budget policy doc | Burn-rate alert rules
- Chaos experiment backlog (Terraform) | On-call rotation + escalation policy
- Runbook library (docs/runbooks/) | Postmortem template | Toil tracking spreadsheet
### Open Questions: [items for other skills]
- observability-architect: confirm KQL signal queries produce correct SLI values in target workspace
- cicd-architect: error budget gate in release pipeline (block deployments when budget < 10%)
- iac-architect: Terraform/AzAPI modules for Chaos Studio experiments and Azure Monitor alert rules
- threat-model: incident-response threat scenarios (unauthorized chaos execution, alert suppression attacks)
```

## Sibling Skills

- `/observability-architect`: Phase 2 telemetry foundation; owns SLO signal wiring, App Insights, Log Analytics, KQL query library, and initial burn-rate alert configuration. `sre-architect` consumes that foundation and adds governance, chaos engineering, and operational practice on top. Start with `/observability-architect` if telemetry is not yet in place.
- `/azure-architect`: resilient Azure service selection (multi-AZ, multi-region, Private Endpoints, Managed Identity); `sre-architect` governs the reliability targets for those services.
- `/cicd-architect`: Phase 2 release strategy; error budget gate wiring in release pipelines (stop deployments when budget is exhausted) is a CI/CD concern that references `sre-architect` SLO outputs.
- `/threat-model`: Phase 2; incident-response threat scenarios (unauthorized chaos experiment execution, alert suppression, audit log tampering) are STRIDE-A concerns that reference this skill's on-call and chaos designs.
- `/agent`: pipeline orchestrator; routes to `sre-architect` when SLA/SLO targets are stated in the discovery brief.
