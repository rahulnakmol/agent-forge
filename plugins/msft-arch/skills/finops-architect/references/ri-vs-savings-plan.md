# Reserved Instances vs Savings Plans: Decision Reference

Read `standards/references/operations/finops-framework.md` for the high-level comparison table. This file contains the detailed break-even math, decision tree rationale, trade-in flows, and quarterly review cadence.

---

## Core Difference

**Reserved Instances (RIs)** lock you into a specific VM family, size series, and Azure region (or region group with instance size flexibility enabled). In exchange they offer the highest discount rate: up to 60% over pay-as-you-go for a 3-year commitment.

**Savings Plans** lock you into a minimum hourly spend commitment (e.g. $5.00/hr) but apply that discount across any eligible compute (Virtual Machines, App Service, Functions Premium, Container Apps, Container Instances, Dedicated Hosts, Spring Apps Enterprise) in any region. Lower maximum discount than RIs (~35–55%) but far more flexibility.

The Microsoft guidance as of 2025: right-size first, then buy commitments. Discounts reduce rates, not waste. A commitment on an over-provisioned resource is a discount on waste.

---

## Decision Tree

```text
Step 0: Right-size first.
        Run 30-day baseline. P95 consumption < current SKU? Downsize before buying any commitment.

Step 1: What is the workload's usage pattern?

  > 60% of hours running at consistent capacity
  ├── Yes → proceed to Step 2
  └── No  → workload is bursty or unpredictable
             ├── Usage > 40% of hours → Savings Plan at P50 baseline; on-demand for burst
             └── Usage < 40% of hours → on-demand only (dev/test, experimental, batch)

Step 2: Is the compute configuration stable?

  VM family and region will NOT change in the commitment term?
  ├── Yes → Reserved Instance
  │         Term: 1-year if project runway < 2 years; 3-year for long-lived infrastructure
  │         Size flexibility: enable instance size flexibility within the family
  │         Scope: shared (billing account) for large estates; single-subscription for isolated workloads
  └── No  → Compute Savings Plan
             Reason: migrating VM families, containerising, moving regions, or evolving service mix
             Term: 1-year; review for 3-year when footprint stabilises

Step 3: Any licence considerations?

  Windows Server or SQL Server?
  └── Yes → Apply Azure Hybrid Benefit FIRST (up to 40% additional saving on licence costs)
             Then apply RI or Savings Plan on top for compute costs

  SQL Database / PostgreSQL / MySQL / Cosmos DB / Azure SQL MI?
  └── Yes → Savings Plan for Databases (1-year; covers infrastructure + software IP for eligible services)
             Note: this is separate from Compute Savings Plan

Step 4: Dev/Test environments

  Subscription under Visual Studio / MSDN or Azure Dev/Test offer?
  └── Yes → Dev/Test pricing already discounted; RIs provide marginal additional benefit
             Consider RI only if dev environment runs 24/7 (CI agents, shared dev databases)
             Otherwise: use Spot Instances for batch CI; on-demand for interactive dev

Step 5: Batch / interruptible workloads

  Can the workload tolerate eviction (seconds' notice)?
  └── Yes → Azure Spot Instances (up to 90% discount vs PAYG; no commitment required)
             Always pair with on-demand fallback pool
             Never use Spot for production stateful workloads
```

---

## Break-Even Math

### 1-Year Reserved Instance: Example: D4s v5 (4 vCPU, 16 GiB) in East US

| Metric | Value |
|--------|-------|
| Pay-as-you-go rate | ~$0.192/hr |
| 1-year RI upfront price | ~$1,005 (all-upfront) |
| Effective RI hourly rate | $1,005 / 8,760 hrs = ~$0.115/hr |
| Hourly saving | $0.192 − $0.115 = $0.077/hr |
| Break-even (hours) | $1,005 / $0.077 ≈ 13,052 hrs ≈ 6.1 months |
| Net saving at 12 months (100% utilisation) | ~$675 (~35%) |
| Net saving at 12 months (70% utilisation) | ~$258 (~13%) |

**Rule**: If the VM will run at least 60% of the time for the full 12 months, the 1-year RI pays off. Below 60% utilisation, on-demand is cheaper than wasting committed capacity.

### 3-Year Reserved Instance: same VM family

| Metric | Value |
|--------|-------|
| 3-year RI upfront price | ~$1,580 (all-upfront) |
| Effective hourly rate | ~$0.060/hr |
| Discount vs PAYG | ~69% |
| Break-even | ~8,125 hrs ≈ 11 months |
| Net saving at 36 months (100% utilisation) | ~$4,400 (~55% total) |

**Rule**: 3-year RI is only appropriate for infrastructure you are certain will exist and remain stable for 3 years. Financial systems, central identity services, and long-lived databases are typical candidates.

### Compute Savings Plan: same baseline spend

| Metric | Value |
|--------|-------|
| Assumed PAYG baseline | $5.00/hr across mixed compute |
| 1-year Savings Plan hourly commitment | $3.30/hr (approx. 34% discount) |
| 3-year Savings Plan hourly commitment | $2.60/hr (approx. 48% discount) |
| Flexibility | Any VM, App Service, Container Apps, Functions, any region |

Savings Plans are billed hourly. If actual usage is below the committed amount in a given hour, the committed amount is still charged. Overcommitting wastes money; follow the Azure Advisor and Benefit Recommendations API output.

---

## Coverage Strategy

```text
Baseline compute (P50 usage): cover 100% with RI + Savings Plan mix
  └── Stable, region-locked workloads → RI
  └── Mixed or evolving compute       → Savings Plan

Predictable burst (P50 → P95 band): cover with on-demand
  └── Spike capacity is cheaper on-demand than wasting committed hours

Unpredictable spike (above P95): on-demand; scale-in quickly post-spike

Summary rule: commit to P50 baseline; leave P95 and above on-demand.
```

---

## Trade-In Flow (Reservation → Savings Plan)

If a workload changes (VM family migrates, app containerised, region moves), an underutilised RI can be traded in for a Savings Plan.

1. Navigate to **Cost Management → Reservations → your RI** → **Exchange**.
2. Azure calculates the outstanding prorated value of the RI.
3. The minimum Savings Plan commitment is the outstanding amount divided by (24 × remaining days in term).
4. You can increase the commitment above the minimum to cover additional resources.
5. Allow 7 days after the trade-in before purchasing additional commitments (recommendation engine needs time to update).

Trade-in restrictions:
- Spot or on-demand usage does not count toward Savings Plan coverage.
- Products must be in the savings plan eligible list (download via Cost Management → Savings Plans → Price Sheet).
- Savings Plans cannot be traded back into RIs.

---

## Quarterly Review Cadence

| Quarter | Activity |
|---------|----------|
| Q1 | Pull Reservation Recommendations API output for all subscriptions. Compare RI utilisation report. Identify RIs below 70% utilisation for exchange or right-sizing. |
| Q2 | Review Savings Plan utilisation. Expand scope (subscription → shared) if utilisation is low. Assess new workloads for RI/SP candidacy. |
| Q3 | Pre-renewal review for any 1-year RIs expiring in Q4. Evaluate 3-year upgrade for stable workloads. |
| Q4 | Year-end FinOps review. Compare actual cloud spend vs commitment plan. Present savings realised vs wasted commitment. Update the commitment vehicle ADR. |

---

## API Integration: Reservation Recommendations

Use the Benefit Recommendations API to programmatically retrieve savings plan purchase recommendations. The Reservation Recommendations API (under Azure Consumption) covers RI recommendations.

```bash
# Get savings plan benefit recommendations (shared scope, 1-year term, 30-day lookback)
GET https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/providers/Microsoft.CostManagement/benefitRecommendations?api-version=2023-11-01&$filter=properties/lookBackPeriod eq 'Last30Days' and properties/term eq 'P1Y'
```

```bash
# Get RI recommendations via Consumption API (subscription scope)
GET https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Consumption/reservationRecommendations?api-version=2023-05-01&$filter=properties/scope eq 'Single'
```

Allow 7 days after any RI or Savings Plan purchase before calling these APIs again; the recommendation engine needs time to account for the new commitment in its simulations.

---

## Common Mistakes

| Mistake | Consequence | Correct Approach |
|---------|-------------|-----------------|
| Buying RIs before right-sizing | Paying for committed waste | Right-size first; commit second |
| Buying 3-year RIs for experimental workloads | Stranded commitment if workload is decommissioned | 1-year RI for workloads < 2yr runway |
| Buying both Savings Plan and RI for the same resources simultaneously | Double-counting; inflated cost | Allow 7 days between purchases; recommendations account for existing commitments |
| Ignoring Savings Plan utilisation alerts | Underutilised commitment billed at 100% regardless | Configure reservation utilisation alerts at 80% threshold |
| Charging teams for RI waste on shared platforms | Team resentment; incorrect cost accountability | Apply RI benefits at billing account scope; distribute savings via showback, not chargeback |
