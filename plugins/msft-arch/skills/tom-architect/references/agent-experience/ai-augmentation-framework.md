---
category: "agent-experience"
loading_priority: 1
tokens_estimate: 2400
keywords: [ai-augmentation, autonomous, human-in-the-loop, copilot, rpa, classification, roi, azure-openai, copilot-studio, semantic-kernel]
version: "1.0"
last_updated: "2026-03-23"
---

# AI Augmentation Framework: Cross-Domain Methodology

## Overview

This framework defines how to systematically evaluate every TOM process for AI augmentation potential. It provides a classification taxonomy, decision criteria, and ROI estimation model applicable across all six TOM layers.

---

## AI Augmentation Classification Taxonomy

| Classification | Description | Human Role | Technology Pattern |
|---|---|---|---|
| **Fully Autonomous** | AI agent executes end-to-end without human intervention | Exception monitoring only | Copilot Studio autonomous agent, Azure Functions, Semantic Kernel |
| **Human-in-the-Loop** | AI agent prepares and recommends; human approves critical step | Approve/reject/modify | Copilot Studio with approval gates, Power Automate approvals |
| **Copilot Assist** | AI provides real-time suggestions within human-driven workflow | Primary decision maker with AI support | M365 Copilot, D365 Copilots, Copilot Studio plugins |
| **RPA** | Rule-based automation of repetitive tasks; no AI reasoning | Design and exception handling | Power Automate Desktop, cloud flows |
| **Human Only** | Process requires human judgment, empathy, or regulatory mandate | Full ownership | No AI; optional productivity tools (M365) |

---

## Decision Criteria for Classification

Score each criterion 0-5 for every TOM process:

### 1. Data Availability (0-5)

| Score | Criteria |
|---|---|
| 0 | No structured data exists; process is entirely verbal/paper-based |
| 1 | Some data exists but in unstructured formats (emails, documents) |
| 2 | Data exists in systems but is fragmented across multiple sources |
| 3 | Data is available in one system but needs cleansing/enrichment |
| 4 | Clean, structured data available in D365/Dataverse/Fabric |
| 5 | Rich, labeled historical data with clear input-output mappings |

### 2. Decision Complexity (0-5)

| Score | Criteria |
|---|---|
| 0 | Requires deep domain expertise, negotiation, or creative judgment |
| 1 | Complex multi-factor decisions with significant ambiguity |
| 2 | Moderate complexity; follows guidelines but requires interpretation |
| 3 | Mostly rule-based with occasional edge cases requiring judgment |
| 4 | Rule-based with well-defined exception handling |
| 5 | Fully deterministic; lookup or calculation-based |

### 3. Regulatory Constraint (0-5)

| Score | Criteria |
|---|---|
| 0 | Regulation mandates human decision and accountability (e.g., audit sign-off) |
| 1 | Regulation requires human review of AI-generated output |
| 2 | Industry guidance recommends human oversight |
| 3 | No specific regulation but organizational policy requires approval |
| 4 | Minimal regulatory concern; standard business process |
| 5 | No regulatory or compliance constraint on automation |

### 4. Error Tolerance (0-5)

| Score | Criteria |
|---|---|
| 0 | Error causes irreversible financial/legal/safety harm |
| 1 | Error causes significant rework or customer impact |
| 2 | Error is costly but detectable and correctable within SLA |
| 3 | Error causes minor rework; easily reversible |
| 4 | Error is low-impact; self-correcting in next cycle |
| 5 | Error is inconsequential; no business impact |

### 5. Volume/Frequency (0-5)

| Score | Criteria |
|---|---|
| 0 | Rare (< 1/month); not worth automation investment |
| 1 | Infrequent (1-5/month) |
| 2 | Periodic (weekly) |
| 3 | Daily (10-50 instances/day) |
| 4 | High volume (50-500/day) |
| 5 | Very high volume (> 500/day); automation is essential |

### Classification Thresholds

| Total Score (0-25) | Classification | Recommended Approach |
|---|---|---|
| 20-25 | Fully Autonomous Agent | Deploy autonomous agent; monitor via dashboards; human exception queue |
| 14-19 | Human-in-the-Loop Agent | Agent prepares recommendation; human approves via adaptive card or approval flow |
| 8-13 | Copilot Assist | Embed copilot in user's workflow; suggestions, drafts, summaries |
| 4-7 | RPA | Power Automate desktop/cloud flows for repetitive sub-tasks |
| 0-3 | Human Only | No automation; invest in UX improvement and training |

---

## ROI Estimation Framework

### Cost Model for AI Investment

| Cost Component | Estimation Method |
|---|---|
| Development cost | Complexity tier * rate (Simple: 2-4 weeks, Medium: 4-8 weeks, Complex: 8-16 weeks) |
| Azure AI consumption | Token volume * pricing (Azure OpenAI per-token), compute (Functions/AKS) |
| Copilot licensing | Per-user/month (M365 Copilot ~$30/user/month, D365 Copilot included in premium) |
| Maintenance | 15-20% of development cost per year for model drift, prompt tuning, testing |
| Change management | Training, adoption support (typically 10-15% of total project cost) |

### Benefit Model

| Benefit Category | Measurement |
|---|---|
| Time saved | Hours/week * FTE cost * processes automated |
| Error reduction | Current error rate * cost-per-error * improvement % |
| Faster cycle time | Days saved per cycle * financial impact of acceleration |
| Capacity unlocked | FTEs freed for higher-value work * value differential |
| Customer satisfaction | NPS/CSAT improvement * customer lifetime value impact |

### ROI Formula

```
ROI = (Annual Benefits - Annual Costs) / Total Investment
Payback Period = Total Investment / (Monthly Benefits - Monthly Costs)
Target: ROI > 150% within 18 months; Payback < 12 months
```

---

## Domain-Specific AI Augmentation Examples

### Finance

| Process | Classification | AI Technique | Microsoft Technology | Expected Impact |
|---|---|---|---|---|
| Invoice matching (3-way) | Fully Autonomous | Document extraction + rule matching | AI Builder + Power Automate | 80% straight-through processing |
| Anomaly detection in journals | Human-in-the-Loop | Outlier detection on GL postings | Azure ML + Power BI | 60% reduction in audit findings |
| Cash flow forecasting | Copilot Assist | Time-series forecasting | D365 Finance Copilot (built-in) | 30% improvement in forecast accuracy |
| Period-close task coordination | Human-in-the-Loop | Agent orchestrates close tasks, flags blockers | Copilot Studio + Power Automate | 2-day reduction in close cycle |
| Expense report audit | Fully Autonomous | Policy compliance check + receipt OCR | AI Builder + Power Automate | 90% auto-approved; 10% flagged for review |
| Financial narrative generation | Copilot Assist | LLM-generated variance commentary | Azure OpenAI + Power BI | 4 hrs/month saved per analyst |

### Human Resources

| Process | Classification | AI Technique | Microsoft Technology | Expected Impact |
|---|---|---|---|---|
| Resume screening | Human-in-the-Loop | NLP-based skill matching and ranking | Azure OpenAI + Copilot Studio | 70% reduction in screening time |
| Attrition prediction | Copilot Assist | Classification model on HR data | Azure ML + Power BI | 6-month early warning; 15% retention improvement |
| Employee FAQ / policy queries | Fully Autonomous | RAG over HR policy documents | Copilot Studio + SharePoint | 50% reduction in HR ticket volume |
| Performance review drafting | Copilot Assist | LLM-generated review summaries | M365 Copilot | 2 hrs saved per manager per cycle |
| Onboarding task orchestration | Fully Autonomous | Multi-step agent (IT, HR, Facilities) | Copilot Studio autonomous agent | 3-day reduction in time-to-productivity |

### Procurement

| Process | Classification | AI Technique | Microsoft Technology | Expected Impact |
|---|---|---|---|---|
| Spend analysis & categorization | Fully Autonomous | NLP classification of spend data | Azure OpenAI + Fabric | 95% auto-categorization accuracy |
| Contract clause extraction | Human-in-the-Loop | Document intelligence + NER | Azure AI Document Intelligence | 80% reduction in manual review |
| Supplier risk monitoring | Copilot Assist | News/financial data monitoring | Azure OpenAI + Copilot Studio | Real-time risk alerts vs. quarterly manual review |
| Purchase order matching | Fully Autonomous | Rule-based + ML for exceptions | Power Automate + AI Builder | 85% straight-through processing |

### Supply Chain Management

| Process | Classification | AI Technique | Microsoft Technology | Expected Impact |
|---|---|---|---|---|
| Demand forecasting | Copilot Assist | Time-series + causal ML models | D365 SCM Copilot + Azure ML | 25% improvement in forecast accuracy |
| Route optimization | Fully Autonomous | Optimization algorithms | Azure Functions + custom ML | 15% reduction in transportation cost |
| Quality defect prediction | Human-in-the-Loop | Anomaly detection on sensor data | Azure IoT Hub + Azure ML | 30% reduction in scrap rate |
| Inventory replenishment | Fully Autonomous | Dynamic reorder point calculation | D365 Planning Optimization + ML | 20% reduction in stockouts |

---

## Implementation Prioritization

### Quick Wins (< 4 weeks, high impact)
- Employee/customer FAQ bots (Copilot Studio + SharePoint RAG)
- Document extraction (AI Builder pre-built models)
- Email drafting and summarization (M365 Copilot, license only)

### Medium-Term (4-12 weeks)
- Invoice processing automation (AI Builder + Power Automate)
- Autonomous period-close orchestration agents
- Spend categorization and analysis

### Strategic Initiatives (12+ weeks)
- Multi-agent orchestration for end-to-end processes
- Custom ML models for demand forecasting / risk prediction
- Enterprise knowledge graph for cross-domain copilot
