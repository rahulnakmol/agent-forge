# Data Breach Blast-Radius Modeling

Every threat model that involves personal data must quantify the regulatory exposure at design time. This file provides the fine-range reference tables, a blast-radius calculation methodology, and worked examples for GDPR, CCPA, and HIPAA. Treat these calculations as a forcing function for investment decisions: if the mitigation cost is less than the expected fine at any realistic probability, the mitigation is non-negotiable.

---

## GDPR: Article 83 Fine Framework

The EU General Data Protection Regulation imposes a two-tier administrative fine structure at Articles 83(4) and 83(5)/(6).

### Tier 1: Article 83(4), Lower-tier infringements

**Maximum**: EUR 10,000,000 or 2% of total worldwide annual turnover of the preceding financial year, whichever is higher.

Applies to infringements of:
- Controller and processor obligations under Articles 8, 11, 25–39, 42, 43 (privacy by design, DPO obligations, record of processing activities, security of processing under Art. 32)
- Certification body obligations under Articles 42 and 43
- Monitoring body obligations under Article 41(4)

**Relevant for threat modeling:** Article 32 (security of processing): "implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk." Failure to implement appropriate encryption, access controls, or incident detection is a Tier 1 infringement.

### Tier 2: Article 83(5)/(6), Higher-tier infringements

**Maximum**: EUR 20,000,000 or 4% of total worldwide annual turnover of the preceding financial year, whichever is higher.

Applies to infringements of:
- Basic principles of processing, including conditions for consent (Articles 5, 6, 7, 9)
- Data subjects' rights (Articles 12–22)
- Transfers to recipients in third countries or international organisations (Articles 44–49)
- Member State law adoptions under Chapter IX
- Non-compliance with an order by a supervisory authority

**Relevant for threat modeling:** Articles 5 and 32 overlap. Failure to maintain confidentiality, integrity, and availability of personal data is both a Tier 1 and Tier 2 breach risk depending on the supervisory authority's characterisation.

### GDPR Fine Calculation Factors (Article 83(2))

Supervisory authorities weigh these eight factors when setting the actual fine within the tier ceiling:
1. Nature, gravity, and duration of the infringement
2. Intentional or negligent character
3. Actions taken to mitigate damage
4. Degree of responsibility (technical and organisational measures)
5. Prior infringements
6. Degree of cooperation with the supervisory authority
7. Categories of personal data affected (special-category data multiplies severity)
8. How the infringement became known (self-report vs. third-party report vs. investigation)

**Design implication:** A threat model that identifies and mitigates risks before a breach, and documents the decision-making, demonstrates "appropriate technical measures" and substantially reduces fine exposure under factors 4 and 5.

### Recent GDPR Enforcement Reference Points (2023–2025)

| Organisation | Fine (EUR) | Infringement | Art. 83 tier |
|---|---|---|---|
| Meta (Ireland) | 1.2 billion | Cross-border transfer (SCCs inadequate) | 83(5) |
| TikTok (Ireland) | 345 million | Children's data processing | 83(5) |
| LinkedIn (Ireland) | 310 million | Consent basis: targeted advertising | 83(5) |
| Clearview AI (France) | 20 million | Biometric data without legal basis | 83(5) |
| Telecom Italia | 7.6 million | Telemarketing consent failure | 83(5) |
| Austrian Post | 9.5 million | Data subject right to access | 83(5) |

**Note:** The EUR 20M ceiling is not the practical ceiling for large organisations; 4% of global turnover dominates. Meta's EUR 1.2B fine (2023, cross-border transfer) demonstrates that the 4% multiplier is operational.

---

## CCPA / CPRA: California Consumer Privacy Act §1798.155

The California Consumer Privacy Act, as amended by the California Privacy Rights Act (CPRA), establishes a civil penalty structure enforced by the California Privacy Protection Agency (CPPA) and the California Attorney General.

### Civil Penalty Structure

| Violation type | Maximum civil penalty per violation |
|---|---|
| Unintentional CCPA violation | USD 2,500 per violation |
| Intentional CCPA violation | USD 7,500 per violation |
| Any violation involving a consumer under 16 years of age | USD 7,500 per violation (always treated as intentional) |

**"Per violation" interpretation:** The CPPA and courts have applied "per violation" to mean per individual record or per individual affected consumer in enforcement actions. A breach affecting 100,000 records can in theory produce up to USD 750,000,000 in maximum civil penalties (100,000 × USD 7,500). Actual enforcement targets realistic exposure; documented remediation efforts are a significant mitigating factor.

### CCPA Data Breach: Private Right of Action (§1798.150)

Distinct from civil penalties, §1798.150 provides a private right of action for consumers whose non-encrypted, non-redacted personal information is exposed by a security breach resulting from the business's failure to implement reasonable security procedures. Statutory damages: USD 100–USD 750 per consumer per incident (or actual damages if greater).

**Design implication:** "Reasonable security procedures" under CCPA maps directly to the Center for Internet Security (CIS) Controls v8 and NIST SP 800-53. A documented STRIDE-A threat model with mitigations aligned to these controls is evidence of reasonable security measures.

### California AG Enforcement Priorities (2024–2025)

The CPPA has signalled enforcement focus on:
- Data minimisation failures (collecting data beyond stated purpose)
- Opt-out mechanism failures (Global Privacy Control not honoured)
- Dark patterns in consent flows
- AI and automated decision-making (CPRA §1798.185(a)(16))

**AI design implication:** Any AI agent that makes automated decisions about consumers (credit, employment, pricing, health) is subject to CPRA §1798.185 opt-out rights. Map to the OWASP ASI Top-10 for AI agents; see `references/owasp-asi-top10.md`.

---

## HIPAA: §160.404 Civil Money Penalties

The Health Insurance Portability and Accountability Act civil money penalty (CMP) structure is established at 45 CFR §160.404 and was last updated by the HITECH Act.

### Four-Tier Penalty Structure

| Tier | Knowledge level | Minimum per violation | Maximum per violation | Annual cap per violation category |
|---|---|---|---|---|
| Tier 1 | Did not know and would not have known with reasonable diligence | USD 100 | USD 50,000 | USD 25,000 |
| Tier 2 | Reasonable cause (not wilful neglect) | USD 1,000 | USD 50,000 | USD 100,000 |
| Tier 3 | Wilful neglect, corrected within 30 days | USD 10,000 | USD 50,000 | USD 250,000 |
| Tier 4 | Wilful neglect, not corrected within 30 days | USD 50,000 | USD 50,000 | USD 1,500,000 |

**Note:** HHS OCR (Office for Civil Rights) interprets "per violation" as per individual whose PHI (Protected Health Information) was improperly disclosed. A breach affecting 50,000 patient records at Tier 3 exposure could reach USD 2.5 billion in maximum penalties (50,000 × USD 50,000) before the annual cap mechanism applies. The annual cap per violation category is USD 1.5M for the most severe tier.

### Breach Notification Rule (45 CFR §164.400–414)

HIPAA requires notification to affected individuals, HHS, and (for breaches ≥ 500 individuals in a state) prominent media within 60 days of discovery. The Breach Notification Rule creates a secondary penalty track; failures to notify are independent violations.

### HHS OCR Settlement Reference Points (2023–2025)

| Organisation | Settlement (USD) | Root cause |
|---|---|---|
| Montefiore Medical Center | 4.75 million | Insider data theft of PHI |
| Premom app / Easy Healthcare | 200,000 | Sharing PHI with third-party analytics without BAA |
| iHealth Solutions | 75,000 | Impermissible disclosure of PHI to unauthorised user |
| New England Dermatology | 300,640 | Disposal of PHI on sticky notes in trash bins |

**Note:** OCR increasingly uses corrective action plans (CAPs) in addition to financial penalties. CAPs mandate periodic risk assessments and technical controls, which directly match the output of a STRIDE-A threat model.

---

## Blast-Radius Calculation Methodology

Use this methodology to populate the blast-radius table required in Step 3b of the Design Process.

### Step 1: Asset Data Classification

For each data store or data flow, classify the data it contains:

| Classification | Examples | Regulatory regimes |
|---|---|---|
| Special-category personal data | Health records, biometric data, racial/ethnic origin, religious beliefs, sexual orientation | GDPR Art. 9, HIPAA, CCPA (sensitive PI) |
| Financial personal data | Credit card numbers, bank account details, credit scores | CCPA, PCI-DSS, GLBA |
| Standard personal data | Name, email, address, phone, IP address, device identifiers | GDPR, CCPA |
| Children's data | Any data of individuals under 13 (COPPA) or under 16 (CCPA / GDPR Art. 8) | COPPA, GDPR, CCPA |
| Proprietary non-personal | Trade secrets, source code, business plans | Contract law / trade secret law |
| Public / non-sensitive | Published content, anonymised aggregates | No regulatory fine risk |

### Step 2: Estimate Records at Risk

For each asset, estimate the number of records that would be exposed in a breach:
- **Worst case**: entire data store (DDoS / ransomware / insider threat)
- **Likely case**: a realistic subset based on the most probable attack vector (e.g., a single tenant's data for a multi-tenant breach)

### Step 3: Calculate Maximum Regulatory Exposure

Apply the per-record maximum fine from each applicable regulation:

```text
GDPR Tier 2 max exposure    = min(EUR 20M, 4% of global annual turnover)
GDPR per-record (practical) = total records exposed / avg. fine amount per prior case

CCPA intentional            = records at risk × USD 7,500
CCPA private right of action= records at risk × USD 750 (practical ceiling)

HIPAA Tier 4                = records at risk × USD 50,000 (before annual cap)
HIPAA annual cap            = USD 1,500,000 per violation category (practical ceiling for any single incident)
```

### Step 4: Assign Risk Tier

| Tier | GDPR exposure | CCPA exposure | HIPAA exposure | Design implication |
|---|---|---|---|---|
| **Critical** | > EUR 5M or near the 4% turnover ceiling | > USD 50M | > USD 500K | All mitigations for this asset are non-negotiable; block deployment if unmitigated |
| **High** | EUR 1M – EUR 5M | USD 5M – USD 50M | USD 100K – USD 500K | Mitigations required in current sprint; architecture review gate |
| **Medium** | EUR 100K – EUR 1M | USD 500K – USD 5M | USD 10K – USD 100K | Mitigations within 30 days; document accepted residual risk in ADR |
| **Low** | < EUR 100K | < USD 500K | < USD 10K | Backlog; standard operational controls |

### Worked Blast-Radius Example: Multi-tenant SaaS with Azure Cosmos DB

**Architecture:** Multi-tenant SaaS processing customer contact data (standard personal data) and medical appointment records (PHI) for healthcare organisations. Cosmos DB stores both datasets with tenant-partitioned containers.

**Scenario:** A cross-tenant IDOR vulnerability in the API allows Tenant A to query Tenant B's appointment records. Records at risk: 10,000 appointment records, each containing patient name, DOB, appointment reason (PHI).

| Asset | Data classification | Records at risk | GDPR max | CCPA max | HIPAA max | Risk tier |
|---|---|---|---|---|---|---|
| Cosmos DB: appointment records | PHI + standard personal data (GDPR Art. 9 special category for appointment reason) | 10,000 | EUR 20M (or 4% turnover) | USD 75M (10,000 × USD 7,500) | USD 500M before cap; USD 1.5M cap per category | **Critical** |
| Cosmos DB: contact data only | Standard personal data | 50,000 | EUR 20M (or 4% turnover) | USD 375M (50,000 × USD 7,500) | Not PHI; HIPAA N/A | **Critical** |

**Design implication:** The IDOR mitigation (tenant-scoped authorization on every data access method, validated by integration tests with cross-tenant caller) is non-negotiable. The mitigation cost (2 engineering sprints) is orders of magnitude below the Critical-tier exposure.

---

## Microsoft Defender for Cloud: Regulatory Compliance Integration

Microsoft Defender for Cloud's Regulatory Compliance dashboard (as of 2025) maps Azure controls to the following frameworks relevant to blast-radius modeling:

| Framework | Status in Defender for Cloud |
|---|---|
| EU GDPR 2016/679 | GA: Azure, AWS, GCP |
| California Consumer Privacy Act (CCPA) | GA: AWS, GCP; Azure under standard MCSB mapping |
| HIPAA | GA: Azure |
| EU AI Act (2024/1689) | Preview: Azure, AWS, GCP (added July 2025) |
| NIST SP 800-53 R5.1.1 | GA: multicloud |
| PCI-DSS v4.0.1 | GA: multicloud |

Use `microsoft_docs_search` with query "Defender for Cloud regulatory compliance standards" to confirm current GA/preview status and new frameworks before finalising compliance scope with the customer.

**Entra Agent ID (November 2025):** For AI agent architectures, Microsoft Entra Agent ID (GA November 2025) provides agent-specific Conditional Access and risk management. Agent identity is now a first-class audit subject under GDPR's accountability principle (Art. 5(2)); agent actions must be attributable and auditable.
