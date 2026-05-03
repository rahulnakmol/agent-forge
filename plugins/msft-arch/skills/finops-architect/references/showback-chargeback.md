# Showback vs Chargeback

Every organisation must choose how it communicates cloud costs to engineering teams. Showback and chargeback are the two models. The canonical decision table is in `standards/references/operations/finops-framework.md`. This file contains implementation patterns, readiness criteria, and the tooling integration guide.

---

## The Rule

**Showback at minimum; chargeback when org maturity supports it.** Every team sees their cloud costs in a weekly report, no exceptions. Chargeback is added only when three gates are passed (see Readiness Gates below). Never charge teams for shared platform costs they cannot control.

---

## Model Definitions

### Showback

Teams receive a cost report showing their cloud spend. The report is informational; it does not transfer budget or trigger an invoice. The goal is cost awareness: engineers who see their costs tend to make better provisioning decisions.

**Characteristics:**
- No finance system integration required.
- Works with any tagging compliance level (start here; improve tags alongside the showback).
- Low political friction; no team loses budget.
- Effective at "crawl" FinOps maturity.

**Limitation:** Without budget accountability, showback can become ignored over time. Pair it with a monthly FinOps review where engineering leads discuss the report.

### Chargeback

Cloud costs are transferred from a central IT budget to the consuming team's cost center in the internal accounting system. Engineering teams are financially accountable for their spend.

**Characteristics:**
- Requires finance system integration (cost center codes in Azure tags must match the chart of accounts).
- Requires tagging compliance above 90%; unclaimed costs become a political problem.
- Requires engineering teams to have genuine budget authority over their allocated spend.
- Effective at "run" FinOps maturity.

**Limitation:** Charging teams for costs they cannot control (shared services, central platform) destroys trust. Apply chargeback only to team-owned resources; use showback for shared infrastructure.

---

## Readiness Gates for Chargeback

All three gates must be cleared before enabling chargeback. If any gate fails, remain on showback and remediate.

| Gate | Metric | Threshold |
|------|--------|-----------|
| Tagging compliance | % of resources with all 5 mandatory tags | > 90% |
| Budget authority | Engineering team can approve spend decisions for their resources | Confirmed with team lead + finance |
| Finance alignment | Azure cost center codes match the chart of accounts | Validated by finance controller |

Check compliance with the KQL query from `references/tagging-strategy.md`. Run it monthly.

---

## Showback Implementation

### Weekly Cost Report: Azure Cost Management Scheduled Alert

The simplest showback implementation uses Cost Management's built-in scheduled alerts.

1. Navigate to **Cost Management → Cost Analysis**.
2. Create a view filtered by `environment` tag = `production` and grouped by `cost-center` tag.
3. Save the view.
4. **Subscribe → Scheduled alert → Weekly → Monday 08:00 local time**.
5. Add all engineering team leads as recipients.
6. Optionally include a CSV attachment for offline analysis.

The email contains a chart of the saved view and a link to Cost Analysis. Recipients do not need Azure portal access to read the email.

### Power BI Showback Dashboard

For organisations that want interactive drill-down, connect Cost Management to Power BI.

```text
Cost Management → Exports → connect to Power BI Desktop
  └── Dataset: AzureCostManagementConnector
      ├── Dimension: cost-center tag → maps to finance cost center
      ├── Dimension: environment tag → filter to production / staging separately
      ├── Measure: PreTaxCost (actual)
      ├── Measure: PreTaxCost (amortised, use for RI/Savings Plan allocation)
      └── Publish to Power BI Service → share with team leads (no Azure RBAC needed)
```

### Cost Allocation Rules (shared resources)

Some resources serve multiple teams: a shared Log Analytics workspace, a central APIM instance, a hub virtual network. Azure Cost Management cost allocation rules split these costs across tags without changing the invoice.

```text
Cost Management → Cost allocation → + Add rule
  ├── Source: resource group "shared-infra-rg" (Log Analytics workspace)
  ├── Targets: split by tag "project" proportional to ingestion volume
  │             project=orders-platform → 45%
  │             project=identity-service → 30%
  │             project=payments-api → 25%
  └── This split appears in showback reports but not on the invoice
```

Use cost allocation for showback of shared services. Never use direct chargeback for shared services; teams cannot control the costs of a shared resource.

---

## Chargeback Implementation

### Finance System Integration Pattern

```text
Azure Cost Management exports → Storage Account (daily, FOCUS format)
    └── Azure Data Factory / Fabric pipeline
        ├── Parse: resource group → cost-center tag value
        ├── Lookup: cost-center code → internal cost center in ERP
        └── Write: chargeback journal entry to finance system (SAP / Dynamics 365 F&O / NetSuite)
            ├── Debit:  CC-1042 (orders-platform team): actual cloud cost
            └── Credit: IT-CENTRAL (central IT clearing account)
```

### FOCUS Export for Chargeback

Use the FOCUS (FinOps Open Cost and Usage Specification) export format introduced in 2024. FOCUS combines actual and amortised costs in a single standardised schema, reducing ETL complexity.

```bash
# Create a FOCUS-format export via REST API
PUT https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/exports/chargeback-daily-focus?api-version=2025-03-01
Content-Type: application/json
Authorization: Bearer {token}

{
  "properties": {
    "schedule": {
      "status": "Active",
      "recurrence": "Daily",
      "recurrencePeriod": {
        "from": "2025-01-01T00:00:00Z",
        "to": "2030-12-31T00:00:00Z"
      }
    },
    "deliveryInfo": {
      "destination": {
        "resourceId": "/subscriptions/{subscriptionId}/resourceGroups/finops-rg/providers/Microsoft.Storage/storageAccounts/finopsexports",
        "container": "cost-exports",
        "rootFolderPath": "focus/daily"
      }
    },
    "definition": {
      "type": "FocusCost",
      "timeframe": "MonthToDate",
      "dataSet": {
        "granularity": "Daily"
      }
    }
  }
}
```

### Amortised vs Actual Cost for Chargeback

| Cost Type | Use Case |
|-----------|----------|
| Actual cost | Cash flow reporting; matches invoice; RI purchase shows as a spike in the purchase month |
| Amortised cost | Chargeback for Reserved Instances; spreads RI purchase cost evenly across the commitment term; gives teams a stable monthly bill |

For chargeback with RIs or Savings Plans, always use amortised cost. A team that benefits from an RI should see a consistent monthly charge, not a spike in the purchase month.

---

## Shared Cost Models

Not everything can be directly attributed. Use these models for shared infrastructure.

| Model | Mechanism | Best For |
|-------|-----------|----------|
| **Proportional** | Split by a usage metric (ingestion bytes, API calls, CPU hours) | Log Analytics, APIM, shared databases |
| **Fixed-split** | Pre-agreed percentages per team per month | Hub network, DNS, Azure Firewall |
| **Even split** | Divide equally by number of consuming teams | Shared dev tools, management plane services |
| **Ignore** | Do not allocate shared costs below a materiality threshold | Costs < $100/month; not worth the ETL effort |

Document the shared cost model in a FinOps decision record (use `/spec` for ADRs). Revisit quarterly; team compositions and usage proportions change.

---

## Chargeback Governance

Once chargeback is live, the following governance controls are required.

1. **Dispute resolution process**: Define a clear process for teams to dispute incorrect charges (wrong cost-center tag, shared cost over-allocation). Target: resolution within 5 business days.
2. **Retroactive correction policy**: Correct the current month's chargeback only; never restate prior months unless the error exceeds a materiality threshold (e.g. > $1,000 or > 5% of team bill).
3. **Materiality threshold for shared services**: Costs below $200/month per team for shared services are absorbed centrally; not worth the administrative friction.
4. **Monthly reconciliation**: Finance controller reconciles Azure export totals against the sum of all chargeback journal entries. Any delta > 1% triggers investigation.

---

## Transition Roadmap: Showback → Chargeback

| Month | Milestone |
|-------|-----------|
| M1–M2 | Deploy mandatory tags; activate Audit policy; publish first showback report |
| M3 | Fix non-compliant resources; tag compliance > 80%; run first FinOps review with eng leads |
| M4 | Tag compliance > 90%; validate cost-center codes against chart of accounts |
| M5 | Confirm team budget authority with finance and team leads |
| M6 | Enable chargeback for team-owned resources; maintain showback for shared services |
| M7+ | Quarterly review cycle; dispute resolution; annual showback/chargeback model review |
