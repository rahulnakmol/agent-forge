# Defender for Cloud: Secure Score and MCSB Compliance Dashboard

Reference for `/defender-sentinel`. Orientation on what secure score is belongs to `/security-architect`.

---

## Secure Score in Production

Secure score is a percentage representing the ratio of healthy resources to total resources across all active MCSB controls. A score of 80% or above is the production target.

**How score is calculated:**

```
Secure Score = (Points earned across all controls) / (Max points available)
```

Each MCSB control has a maximum point value. Controls in the "critical" category carry higher point weights. Remediating a Critical-weight control has more score impact than remediating a Low-weight one.

**Important:** secure score reflects posture at the control level, not the alert level. A resource can have no active alerts and still reduce the score if a recommendation is unaddressed (for example, an NSG without inbound deny rule, or a storage account with public access enabled).

---

## Microsoft Cloud Security Benchmark (MCSB)

MCSB v1 is the GA baseline as of March 2023. MCSB v2 is in preview. Monitor MCSB v2 controls as leading indicators; do not wait for GA to start gap analysis.

**MCSB control domains (v1):**

| Domain | ID prefix | Examples |
|---|---|---|
| Network Security | NS | NS-1: Establish network segmentation boundaries; NS-8: Detect and disable insecure services |
| Identity Management | IM | IM-1: Use centralised identity and authentication system; IM-3: Manage application identities securely |
| Privileged Access | PA | PA-1: Separate and limit highly privileged/administrative users; PA-7: Follow JEA principles |
| Data Protection | DP | DP-1: Discover, classify and label sensitive data; DP-3: Encrypt sensitive data in transit |
| Asset Management | AM | AM-2: Use only approved services; AM-3: Ensure security of asset lifecycle management |
| Logging and Threat Detection | LT | LT-1: Enable threat detection capabilities; LT-4: Enable network logging for security investigation |
| Incident Response | IR | IR-2: Preparation and planning of incident response; IR-3: Detection and analysis |
| Posture and Vulnerability Management | PV | PV-1: Run automated vulnerability scanning tools; PV-3: Establish secure configurations for compute |
| Endpoint Security | ES | ES-1: Use Endpoint Detection and Response (EDR) |
| Backup and Recovery | BR | BR-1: Ensure regular automated backups |
| DevOps Security | DS | DS-1: Conduct threat modeling; DS-5: Conduct static application security testing |
| Governance and Strategy | GS | GS-1: Align organizational roles, responsibilities and accountabilities |

**Non-negotiable:** use MCSB as the baseline. Do not author custom security policies from scratch. MCSB controls map automatically to NIST SP 800-53 Rev 5, CIS Controls v8, ISO 27001:2013, PCI-DSS 3.2.1, and SOC 2. Enable the relevant compliance standard in the Regulatory Compliance dashboard and let the mapping run automatically.

---

## Regulatory Compliance Dashboard

Enable the Regulatory Compliance dashboard on day 1. Steps:

1. In Defender for Cloud, navigate to **Regulatory Compliance**.
2. The MCSB standard is auto-applied. Add the workload-specific standard: NIST SP 800-53, PCI DSS, ISO 27001, CIS Azure Foundations Benchmark.
3. For regulated workloads (HIPAA, FedRAMP, CMMC), add the specific standard. Availability varies by Azure Government vs. commercial cloud region.
4. Export the compliance report (PDF or CSV) on a cadence that matches the audit cycle (monthly for active audits; quarterly for ongoing governance).

**Continuous compliance export:** configure the **Continuous Export** feature in Defender for Cloud to stream regulatory compliance data to a Log Analytics workspace or Event Hub. Use Log Analytics to build a Workbook tracking compliance posture over time.

---

## Secure Score: Operations

### Finding Backlog Prioritisation

Export the full recommendation list and sort by:

1. **Severity** (Critical first, then High, Medium, Low)
2. **Score impact** (highest point weight first within each severity tier)
3. **Resource count affected** (fixes that apply across many resources)

Assign an owner and sprint/milestone to every Critical and High finding before the workload goes to production. Document Medium and Low findings in the backlog with a review date (30-day for Medium, quarterly for Low). Accept-risk decisions for any finding require an ADR.

### Exemptions

Exemptions are legitimate but must be time-bound and documented. Use the built-in exemption workflow (Waived or Mitigated). Exemptions without expiry dates and justification text are a governance anti-pattern. Require manager or CISO approval for any Critical-severity exemption.

### Governance Rules

Use Defender for Cloud **Governance rules** to automate owner assignment and due-date escalation for recommendations. Configure rules by resource type or by tag (for example, `env=production` resources escalate to the SecOps team; `env=dev` resources escalate to the development team).

---

## Secure Score as a KPI

Track secure score as an SLO-like metric:

- **Baseline:** capture score at first enablement.
- **Target:** 80%+ for production workloads within 60 days of enablement.
- **Regression alert:** configure an Azure Monitor alert rule on the `Microsoft.Security/secureScores` metric to fire if score drops more than 5 percentage points within a 7-day window.
- **Trend workbook:** build an Azure Workbook (or Sentinel Workbook) that charts secure score over time, broken down by control domain, using the Continuous Export data in Log Analytics.

---

## MCSB vs. Custom Policies: Decision Rule

| Scenario | Recommendation |
|---|---|
| Standard enterprise cloud workload | MCSB only. Do not author custom policies duplicating MCSB controls. |
| Regulated workload (PCI-DSS, HIPAA, FedRAMP) | MCSB + applicable built-in compliance standard. Add custom policies only for controls not covered by MCSB or the compliance standard. |
| Organisation-specific guardrails (naming, tagging, allowed regions) | Custom Azure Policy definitions; do not conflate these with security posture. Apply via Azure Policy Initiative, not Defender for Cloud recommendations. |
| Customer-specific security standard (not a public regulation) | Map the customer standard to MCSB controls first. Author custom policies only for the gap (controls in the customer standard that have no MCSB equivalent). |

**Principle:** start with MCSB. Add specificity only where a gap exists. Custom baselines that duplicate MCSB controls create maintenance burden without security value.
