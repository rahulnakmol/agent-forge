# FinOps Framework

**Based on**: FinOps Foundation open-source framework (finops.org) applied to Azure. The framework describes how engineering, finance, and business teams collaborate to maximize cloud value.

---

## The Three Phases: Inform → Optimize → Operate

FinOps is a continuous loop, not a one-time project. Teams cycle through all three phases repeatedly as workloads evolve.

```text
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │   INFORM ──────► OPTIMIZE ──────► OPERATE           │
  │      ▲                                │             │
  │      └────────────────────────────────┘             │
  │                                                     │
  └─────────────────────────────────────────────────────┘
```

### Inform

**Goal**: Visibility. You cannot optimize what you cannot see.

Activities:
- Allocate cloud spend to teams, products, and cost centers via tags.
- Publish daily/weekly cost dashboards to engineering teams, not just finance.
- Establish unit economics: cost per API call, cost per tenant, cost per processed record.
- Identify the top 10 spend drivers by service and resource group each week.
- Set budget alerts in Azure Cost Management for each cost center and environment.

Key metrics:
- Total cloud spend (actual vs budget)
- Cost per environment (production, staging, dev)
- Top 5 resources by cost
- Spend trend (week-over-week, month-over-month)

### Optimize

**Goal**: Efficiency. Right-size, eliminate waste, and shift spend toward reserved capacity where appropriate.

Activities:
- Right-size overprovisioned VMs and App Service Plans using Azure Advisor recommendations.
- Delete unused resources: unattached disks, orphaned NICs, idle App Gateways.
- Move infrequently accessed data to cooler storage tiers (Hot → Cool → Archive).
- Convert pay-as-you-go compute to Reserved Instances or Savings Plans for stable workloads.
- Implement auto-scaling to avoid running at peak capacity 24/7.
- Use Azure Spot Instances for batch, dev, and test workloads.
- Enable Azure Hybrid Benefit for Windows Server and SQL Server licenses.

### Operate

**Goal**: Culture and governance. Make cost accountability a normal part of engineering.

Activities:
- Include cost in sprint reviews: "Feature X cost $0.04 per user interaction."
- Set cost anomaly alerts (Azure Cost Management anomaly detection).
- Run monthly FinOps reviews with tech leads and product owners.
- Define cost thresholds that require approval before deployment (e.g., estimated monthly cost > $5K requires VP sign-off).
- Track cloud efficiency KPIs quarter-over-quarter.
- Enforce tagging compliance via Azure Policy; deny deployments without required tags.

---

## FinOps Capabilities Map

The FinOps Foundation defines the following capabilities. Teams at "Crawl" level implement basics; "Walk" adds automation; "Run" achieves real-time optimization.

| Capability | Crawl | Walk | Run |
|---|---|---|---|
| Cost Allocation | Manual tag reports | Automated tag enforcement via Policy | Showback/chargeback integrated with finance systems |
| Anomaly Detection | Manual cost review | Azure Cost Anomaly Alerts | ML-driven alerts with auto-notification to engineers |
| Budgeting | Subscription-level budgets | Resource group budgets | Per-workload, per-feature budgets with Slack/Teams alerts |
| Unit Economics | Not measured | Cost per user tracked | Cost per transaction used in product decisions |
| Reserved Capacity | Ad-hoc RI purchases | Quarterly RI planning | Automated RI optimization with savings plan mix |
| Waste Elimination | Manual Advisor review | Weekly automated cleanup scripts | Idle resource policies with auto-decommission |
| Rate Optimization | PAYG only | Hybrid Benefit applied | Savings Plans + RI + Spot mix optimized |

---

## Anomaly Detection

Azure Cost Management provides built-in anomaly detection that uses machine learning to identify unexpected cost spikes compared to historical baselines.

Configure anomaly alerts:
1. Azure Cost Management → **Cost Alerts** → **Anomaly Alerts**.
2. Set scope (subscription or resource group).
3. Set notification threshold (e.g., alert when anomaly confidence > 95% and deviation > $100/day).
4. Route alerts to an email group or Azure Monitor action group (→ Teams webhook, PagerDuty).

Engineering response to a cost anomaly:
1. Identify the resource group and resource type driving the spike.
2. Check recent deployments in that scope (deployment history in Azure portal).
3. Check for runaway loops, missing throttling, or autoscale misconfiguration.
4. Tag the root cause in the anomaly alert for FinOps review.

---

## Showback vs Chargeback

| Model | Description | When to Use |
|---|---|---|
| **Showback** | Teams see their cloud costs in a report but are not billed internally | Early FinOps maturity; teams are not yet accountable for cost |
| **Chargeback** | Costs are transferred to the consuming team's budget in the internal accounting system | Mature FinOps; team-level P&L accountability; multiple cost centers |

Showback is the recommended starting point. Move to chargeback only when:
- Finance has aligned cost center codes with Azure subscriptions or resource groups.
- Engineering teams have budget autonomy and can make spend decisions.
- Tagging compliance is above 90%.

---

## Reserved Instances vs Savings Plans: Decision Matrix

| Commitment | Flexibility | Discount vs PAYG | Best For |
|---|---|---|---|
| **1-Year Reserved Instance** | Specific VM family + region | ~35–40% | Stable, predictable VMs; single-region production |
| **3-Year Reserved Instance** | Specific VM family + region | ~55–60% | Long-lived infrastructure; financial systems |
| **1-Year Compute Savings Plan** | Any VM, App Service, Container Instances in any region | ~30–35% | Mixed or evolving compute footprint |
| **3-Year Compute Savings Plan** | Any VM, App Service, Container Instances in any region | ~50–55% | Large, mature Azure estate |
| **Pay-As-You-Go** | No commitment | Baseline | Dev/test, spiky, short-lived, uncertain workloads |

Rules of thumb:
- Cover at least 70% of your baseline (minimum expected) compute with Reserved Instances or Savings Plans.
- Leave the top 30% on PAYG to absorb traffic spikes without wasting committed capacity.
- Use Savings Plans for compute that migrates between VM families or regions.
- Review RI and Savings Plan coverage quarterly using Azure Cost Management's **Reservation Recommendations** blade.

---

## Tagging Strategy

All Azure resources MUST carry these five mandatory tags. Enforce via Azure Policy (deny deployment if tag is missing).

| Tag Key | Description | Example Values |
|---|---|---|
| `cost-center` | Finance cost center code | `CC-1234`, `PROD-ENG` |
| `environment` | Deployment environment | `production`, `staging`, `dev`, `sandbox` |
| `owner` | Primary responsible team or engineer | `platform-team`, `jane.doe@contoso.com` |
| `project` | Product or project name | `orders-platform`, `identity-service` |
| `expiry` | Date after which the resource should be reviewed for deletion (ISO 8601) | `2026-12-31`, `never` |

Recommended additional tags:
- `app`: application name for multi-app resource groups.
- `tier`: architectural tier (`frontend`, `api`, `data`, `infra`).
- `created-by`: automation or person who created the resource (for debugging).

Tag naming convention: lowercase, hyphen-separated, no spaces.

---

## Azure Cost Management Features

| Feature | Purpose | Where to find it |
|---|---|---|
| **Cost Analysis** | Interactive cost breakdown by service, resource, tag, time period | Cost Management → Cost Analysis |
| **Budgets** | Set spend limits with email/action-group alerts | Cost Management → Budgets |
| **Anomaly Alerts** | ML-based spike detection | Cost Management → Cost Alerts → Anomaly Alerts |
| **Advisor Recommendations** | Right-sizing, reserved capacity, idle resource suggestions | Azure Advisor → Cost |
| **Reservation Recommendations** | RI and Savings Plan purchase recommendations based on usage history | Cost Management → Reservations → Recommendations |
| **Power BI Connector** | Connect Cost Management data to Power BI for custom dashboards | Cost Management → Export → Power BI |
| **Cost Exports** | Scheduled export of cost data to Storage Account for custom ETL | Cost Management → Exports |
| **Azure Policy (Tag Enforcement)** | Deny or audit deployments missing required tags | Policy → Definitions → Tag policies |

---

## Trade-offs and Exceptions

- **Tagging vs deployment speed**: Mandatory tag enforcement via Azure Policy (Deny effect) blocks deployments that lack tags. In fast-moving teams this creates friction. Start with **Audit** effect (log non-compliant resources) for 30 days, then switch to **Deny** after teams have adapted their IaC.
- **Reserved Instances for volatile workloads**: Never buy RIs for workloads you expect to shut down or drastically resize within the commitment period. The break-even for a 1-year RI is typically 6–8 months of usage.
- **Chargeback without budget authority**: Charging a team for cloud spend they cannot control (shared platform costs, central services) breeds resentment. Apply showback for shared services and chargeback only for team-owned resources.
- **Savings Plans vs Reserved Instances**: Savings Plans offer more flexibility but lower discount rates. If your compute footprint is stable and well-understood, RIs give better ROI. If your team is actively migrating to containers or changing VM families, Savings Plans are safer.
- **Unit economics at early stage**: Computing cost-per-user or cost-per-transaction requires instrumentation and is not always worth the engineering time at early product stages. Prioritize tagging and budget alerts first; introduce unit economics when the product has stable usage patterns.
