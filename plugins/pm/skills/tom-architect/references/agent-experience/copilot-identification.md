---
category: "agent-experience"
loading_priority: 2
tokens_estimate: 1600
keywords: [copilot, m365-copilot, d365-copilot, copilot-studio, azure-ai-foundry, sales-copilot, customer-service-copilot, finance-copilot, supply-chain-copilot]
version: "1.0"
last_updated: "2026-03-23"
---

# Copilot Identification — Microsoft Copilot Products to TOM Capabilities

## Overview

Maps each Microsoft Copilot product to the TOM processes it augments. For each copilot: target TOM processes, expected efficiency gains, and implementation complexity.

---

## Microsoft 365 Copilot

| Attribute | Detail |
|---|---|
| **Scope** | Cross-cutting productivity layer across all TOM domains |
| **Licensing** | Per-user add-on ($30/user/month as of 2025) |
| **Implementation Complexity** | Low (license activation + data governance readiness) |

| TOM Process Area | Copilot Capability | Expected Impact |
|---|---|---|
| All — document creation | Draft Word documents, Excel analyses, PowerPoint decks from prompts | 30-40% reduction in document creation time |
| All — email communication | Draft, summarize, and prioritize emails in Outlook | 20-30% reduction in email handling time |
| All — meeting management | Meeting summaries, action items, follow-up drafts in Teams | 25% reduction in post-meeting admin |
| All — data analysis | Natural language queries over Excel data, pivot table generation | 40% faster ad-hoc analysis for non-technical users |
| All — knowledge retrieval | Search across SharePoint, OneDrive, Teams, email via Microsoft Graph | 50% reduction in time-to-find-information |
| Governance — compliance | Summarize policy documents, draft compliance responses | 20% faster compliance review cycles |

### Prerequisites for M365 Copilot
- Microsoft Graph data must be properly permissioned (oversharing risk)
- Sensitivity labels applied to sensitive content (Purview)
- SharePoint site hygiene (retire stale content, proper permissions)
- Semantic Index for Copilot must be enabled

---

## D365 Sales Copilot

| Attribute | Detail |
|---|---|
| **Scope** | Sales processes — Lead to Opportunity to Close |
| **Licensing** | Included in D365 Sales Premium; available as Copilot for Sales add-on for non-D365 CRM |
| **Implementation Complexity** | Low-Medium (D365 Sales configuration + Copilot activation) |

| TOM Process | Copilot Capability | Expected Impact |
|---|---|---|
| Lead qualification | AI-scored lead prioritization based on engagement signals | 25% improvement in lead-to-opportunity conversion |
| Opportunity management | Opportunity summaries, deal insights, competitor analysis | 15% reduction in sales cycle length |
| Email engagement | Context-aware email drafting with CRM data | 30% reduction in email composition time |
| Meeting preparation | Pre-meeting briefs combining CRM data, email history, LinkedIn | 20 min saved per customer meeting |
| CRM hygiene | Natural language CRM updates (voice/text to record update) | 50% improvement in CRM data completeness |
| Forecasting | AI-assisted pipeline review and forecast confidence scoring | 20% improvement in forecast accuracy |

---

## D365 Customer Service Copilot

| Attribute | Detail |
|---|---|
| **Scope** | Service processes — Case Management, Knowledge, Omnichannel |
| **Licensing** | Included in D365 Customer Service Premium |
| **Implementation Complexity** | Medium (knowledge base quality is critical for effectiveness) |

| TOM Process | Copilot Capability | Expected Impact |
|---|---|---|
| Case summarization | Auto-generate case summary from conversation history | 30% reduction in case handling time |
| Knowledge search | AI-powered knowledge article suggestions during case handling | 40% improvement in first-contact resolution |
| Response drafting | Draft customer responses using knowledge base and case context | 25% reduction in agent response time |
| Conversation wrap-up | Auto-populate case fields from conversation transcript | 60% reduction in after-call work |
| Sentiment analysis | Real-time customer sentiment tracking during conversation | Proactive escalation of negative interactions |
| Knowledge authoring | Generate knowledge articles from resolved cases | 50% faster knowledge base growth |

### Prerequisites for CS Copilot
- Well-maintained knowledge base (current, tagged, reviewed)
- Omnichannel configured for digital channels
- Case entity properly configured with required fields

---

## D365 Finance Copilot

| Attribute | Detail |
|---|---|
| **Scope** | Finance processes — Collections, Cash Flow, Reporting |
| **Licensing** | Included in D365 Finance |
| **Implementation Complexity** | Low (feature activation in D365 Finance) |

| TOM Process | Copilot Capability | Expected Impact |
|---|---|---|
| Collections management | Collections coordinator copilot — prioritized customer outreach, email drafting | 30% reduction in days sales outstanding (DSO) |
| Cash flow forecasting | AI-powered cash flow predictions using historical patterns | 30% improvement in forecast accuracy |
| Payment prediction | Customer payment behavior prediction | 20% reduction in overdue receivables |
| Bank reconciliation | AI-suggested matching rules for bank statement lines | 40% faster reconciliation |
| Financial narrative | Variance analysis commentary generation | 4 hrs/month saved per financial analyst |

---

## D365 Supply Chain Copilot

| Attribute | Detail |
|---|---|
| **Scope** | SCM processes — Demand Planning, Inventory, Procurement |
| **Licensing** | Included in D365 Supply Chain Management |
| **Implementation Complexity** | Medium (requires clean historical data for prediction accuracy) |

| TOM Process | Copilot Capability | Expected Impact |
|---|---|---|
| Demand planning | AI-assisted demand forecasting with external signals | 25% improvement in forecast accuracy |
| Supply chain disruption | Proactive disruption alerts (weather, news, supplier risk) | Days of advance warning vs. reactive |
| Inventory optimization | AI-recommended safety stock and reorder points | 20% reduction in excess inventory |
| Procurement suggestions | Suggested purchase orders based on demand signals | 30% reduction in stockouts |
| Warehouse operations | Natural language queries on inventory and order status | 15% faster operational decision-making |

---

## Power Platform Copilot

| Attribute | Detail |
|---|---|
| **Scope** | Low-code development — App building, Flow creation, Report design |
| **Licensing** | Included in Power Platform premium licenses |
| **Implementation Complexity** | Low (enabled by default in managed environments) |

| TOM Process | Copilot Capability | Expected Impact |
|---|---|---|
| Citizen app development | Describe app in natural language; Copilot generates canvas/model-driven app | 50% faster app prototyping |
| Automation design | Describe flow in natural language; Copilot generates cloud flow | 40% faster flow creation |
| Report creation | Describe report need; Copilot generates Power BI report | 30% faster initial report design |
| Data modeling | Copilot suggests Dataverse table structures | 25% faster data model design |
| Formula assistance | Power Fx formula suggestions and explanations | 60% reduction in formula debugging time |

---

## Copilot Studio

| Attribute | Detail |
|---|---|
| **Scope** | Custom agent building — per business process or domain |
| **Licensing** | Per-tenant or per-message consumption-based |
| **Implementation Complexity** | Medium-High (agent design, knowledge curation, plugin development, testing) |

| TOM Process | Copilot Studio Capability | Expected Impact |
|---|---|---|
| Any process — custom agent | Build domain-specific agents with topics, knowledge, plugins | Varies by use case; 30-70% process efficiency gain |
| Cross-process orchestration | Autonomous agents triggered by business events | End-to-end automation of multi-step processes |
| External customer engagement | Deploy agents to web, Teams, mobile channels | 40% reduction in Tier 1 support volume |
| Internal employee service | HR, IT, Facilities self-service agents | 50% reduction in internal ticket volume |
| Knowledge management | RAG-based agents over SharePoint, Dataverse, custom sources | 60% faster information retrieval |

---

## Azure AI Foundry

| Attribute | Detail |
|---|---|
| **Scope** | Custom AI models and agents for specialized TOM processes |
| **Licensing** | Consumption-based (Azure OpenAI token pricing, compute) |
| **Implementation Complexity** | High (ML engineering, prompt engineering, RAG architecture, evaluation, MLOps) |

| TOM Process | Azure AI Foundry Capability | Expected Impact |
|---|---|---|
| Specialized document processing | Custom models for domain-specific documents (contracts, regulatory) | 90% extraction accuracy on custom document types |
| Custom classification | Fine-tuned models for industry-specific categorization | Higher accuracy than generic models for niche domains |
| Multi-agent orchestration | Semantic Kernel / AutoGen for complex agent pipelines | End-to-end process automation with multi-step reasoning |
| Custom RAG | Enterprise search over proprietary knowledge with citations | Grounded answers with source attribution |
| Evaluation & testing | AI Foundry evaluation framework for quality, safety, groundedness | Systematic quality assurance for AI outputs |

---

## Copilot Implementation Priority Matrix

| Priority | Copilot | Rationale |
|---|---|---|
| 1 (Quick Win) | M365 Copilot | Broad impact, low implementation effort, immediate productivity gains |
| 2 (Quick Win) | D365 native copilots (Sales, CS, Finance, SCM) | Feature activation on existing D365; no additional build |
| 3 (Medium) | Copilot Studio — FAQ/knowledge agents | High deflection rates; well-understood pattern |
| 4 (Medium) | Power Platform Copilot | Accelerates citizen development; multiplier effect |
| 5 (Strategic) | Copilot Studio — autonomous process agents | High impact but requires careful design, testing, governance |
| 6 (Strategic) | Azure AI Foundry — custom models/agents | Highest complexity; reserve for processes where OOB copilots are insufficient |
