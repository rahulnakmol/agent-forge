---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2800
keywords: [ai-capabilities, servicenow, now-assist, now-intelligence, virtual-agent, ai-agents, predictive-intelligence, ai-search]
version: "1.0"
last_updated: "2026-03-28"
---

# ServiceNow AI Capabilities — TOM Process Categories to ServiceNow AI Features

## Overview

ServiceNow's AI strategy is built around Now Assist (GenAI across the platform), Now Intelligence (predictive ML), Virtual Agent (conversational AI), and AI Agents (autonomous task execution). These capabilities are embedded across ITSM, ITOM, CSM, HRSD, and the platform layer. This reference maps ServiceNow AI capabilities to TOM process categories.

---

## Now Assist — Generative AI Across the Platform

Now Assist brings large language model capabilities to every ServiceNow workflow, available to end users, agents, and developers.

### Now Assist for ITSM

| Capability | Description | TOM Process Category |
|---|---|---|
| Incident Summarization | Auto-summarize incident history, work notes, and resolution for handoffs | IT Service Management |
| Resolution Notes Generation | Generate resolution notes from work notes and activities | IT Service Management |
| Knowledge Article Generation | Draft KB articles from resolved incidents and problem records | IT Service Management |
| Chat Summarization | Summarize Virtual Agent conversations when escalated to live agent | IT Service Management |
| Similar Incident Search | GenAI-enhanced search for similar past incidents with resolution context | IT Service Management |
| Change Risk Assessment | AI-generated risk summaries for change requests | IT Service Management |

### Now Assist for CSM

| Capability | Description | TOM Process Category |
|---|---|---|
| Case Summarization | Summarize customer case history for agent context | Customer Service |
| Reply Generation | Generate customer-facing replies grounded in knowledge base | Customer Service |
| Case Wrap-Up | Auto-populate case fields (category, resolution) at case close | Customer Service |
| Email Response Generation | Draft email responses to customer inquiries | Customer Service |

### Now Assist for HRSD

| Capability | Description | TOM Process Category |
|---|---|---|
| HR Case Summarization | Summarize employee HR case history | Employee Services |
| Knowledge Search (HR) | AI-powered search across HR knowledge bases | Employee Services |
| Employee Chat Assist | Conversational AI for common HR questions (PTO, benefits, policies) | Employee Services |

### Now Assist for Developers

| Capability | Description | TOM Process Category |
|---|---|---|
| Code Generation | Generate server-side scripts, client scripts, and Flow Designer actions | Platform Development |
| Code Explanation | Explain existing scripts and business rules | Platform Development |
| Flow Generation | Generate Flow Designer flows from natural language descriptions | Platform Development |
| Test Generation | Create Automated Test Framework tests from natural language | Platform Development |

---

## Now Intelligence — Predictive AI & ML

| Capability | Module | TOM Process Category | Description |
|---|---|---|---|
| Predictive Intelligence (Classification) | ITSM, CSM, HRSD | IT Service Management, Customer Service | Auto-classify category, subcategory, assignment group, priority |
| Predictive Intelligence (Similarity) | ITSM, CSM | IT Service Management, Customer Service | Find similar records for faster resolution |
| Predictive Intelligence (Regression) | Platform | Cross-functional | Predict numeric outcomes (e.g., resolution time, SLA breach probability) |
| Anomaly Detection | ITOM, Platform | IT Operations | Detect anomalous patterns in metrics, logs, and events |
| Clustering | ITOM Event Management | IT Operations | Group related alerts to reduce noise |
| Agent Recommendations | ITSM Agent Workspace | IT Service Management | Suggest next best actions, knowledge articles, and similar incidents |

---

## Virtual Agent — Conversational AI

| Capability | Description | TOM Process Category |
|---|---|---|
| Pre-built Conversations | Out-of-box conversation topics for ITSM, CSM, HRSD | IT Service Management, Customer Service, Employee Services |
| Custom Topics | Build custom conversation flows with NLU models | Any |
| Multi-Channel | Deploy on ServiceNow Portal, Microsoft Teams, Slack, web chat | Cross-functional |
| Entity Extraction | Extract key entities (date, location, CI name, employee ID) from user input | Cross-functional |
| Live Agent Handoff | Seamless escalation to human agent with conversation context | IT Service Management, Customer Service |
| Proactive Prompts | Trigger conversations based on events (e.g., VPN down, benefit enrollment) | IT Service Management, Employee Services |
| Multi-Language | Support for 15+ languages with NLU models | Cross-functional |

---

## AI Search

| Capability | Description | TOM Process Category |
|---|---|---|
| Federated Search | Search across knowledge bases, catalog items, community, and external sources | Cross-functional |
| Semantic Search | AI-powered semantic understanding (not just keyword matching) | Cross-functional |
| Personalized Results | Results ranked by user role, department, and history | Cross-functional |
| External Source Connectors | Index and search external content (SharePoint, Confluence, web) | Cross-functional |
| AI-Generated Answers | Generate direct answers from knowledge base content (not just links) | Cross-functional |

---

## AI Agents — Autonomous Task Execution

ServiceNow AI Agents go beyond chatbots to autonomously complete multi-step workflows.

| Agent Type | Description | TOM Process Category |
|---|---|---|
| Incident Auto-Resolution | Autonomously resolve common incidents (password reset, access request, software install) | IT Service Management |
| Request Fulfillment Agent | Complete service catalog requests without human intervention | IT Service Management |
| Alert Remediation Agent | Automatically remediate infrastructure alerts using runbook automation | IT Operations |
| Case Resolution Agent | Resolve customer cases using knowledge base, then verify with customer | Customer Service |
| HR Request Agent | Handle routine HR requests (employment verification, policy questions) | Employee Services |
| Change Automation Agent | Auto-approve low-risk standard changes and schedule deployment | IT Service Management |

### Agent Architecture

| Component | Description |
|---|---|
| Reasoning Engine | LLM-based reasoning to determine the right sequence of actions |
| Action Framework | Connect to Flow Designer actions, IntegrationHub spokes, and APIs |
| Guardrails | Configurable boundaries: max actions per session, approval thresholds, escalation triggers |
| Observability | Full audit trail of agent reasoning, actions taken, and outcomes |
| Human-in-the-Loop | Configurable checkpoints where agents pause for human approval |
| Continuous Learning | Agent performance tracked; low-confidence actions flagged for review |

---

## Performance Analytics (AI-Enhanced)

| Capability | Description | TOM Process Category |
|---|---|---|
| KPI Scorecards | Automated KPI tracking with targets and thresholds | Cross-functional |
| Trend Analysis | ML-driven trend detection and forecasting for KPIs | Cross-functional |
| Benchmarking | Compare performance against ServiceNow customer benchmarks | IT Service Management |
| Anomaly Alerts | Proactive alerts when KPIs deviate from expected ranges | Cross-functional |
| Interactive Dashboards | Drill-down dashboards with time-series analysis | Cross-functional |
| Data Collection | Automated data collection and aggregation for analytics | Cross-functional |

---

## Document Intelligence

| Capability | Description | TOM Process Category |
|---|---|---|
| Document Extraction | Extract structured data from unstructured documents (invoices, contracts, forms) | Cross-functional |
| Classification | Auto-classify document types for routing and processing | Cross-functional |
| Verification | AI-assisted document verification against business rules | Cross-functional |
| Integration | Feed extracted data into workflows via Flow Designer | Cross-functional |

---

## Process Automation Candidates (AI-Augmented)

| Process | Automation Type | AI Enhancement | Expected Impact |
|---|---|---|---|
| Incident resolution (L1) | AI Agent + Virtual Agent | Auto-classification, similar incident matching, auto-resolution | 40-60% of L1 incidents resolved without human |
| Service request fulfillment | AI Agent + Flow Designer | Auto-approval, automated provisioning, status updates | 50-70% of requests fulfilled automatically |
| Password reset | Virtual Agent + Flow Designer | Conversational authentication, automated reset | 90%+ automated with zero agent touch |
| Change management | Predictive + Flow | Risk prediction, auto-approval (standard), conflict detection | 30% reduction in change-related incidents |
| Knowledge management | Now Assist (GenAI) | Auto-generate articles from resolved incidents, keep articles fresh | 3x increase in KB article creation |
| Customer case resolution | AI Agent + Knowledge | Auto-resolve via knowledge, sentiment detection, escalation | 30-40% of cases resolved autonomously |
| Employee onboarding | HRSD + Flow Designer + Virtual Agent | Guided onboarding, document collection, cross-system provisioning | 60% reduction in onboarding tasks for HR |
| Security incident response | SecOps + Flow Designer | Alert enrichment, playbook automation, threat correlation | 50% reduction in mean time to respond |

---

## AI Capability-to-TOM Process Category Mapping

| TOM Process Category | ServiceNow AI Capabilities | Maturity |
|---|---|---|
| IT Service Management | Predictive classification, incident summarization, auto-resolution agents, Virtual Agent, similar incidents | High |
| IT Operations | AIOps (alert correlation, noise reduction), anomaly detection, Health Log Analytics, remediation agents | High |
| Customer Service | Case summarization, reply generation, case resolution agents, sentiment analysis | High |
| Employee Services | HR chat assist, case summarization, knowledge search, onboarding agents | Medium-High |
| Security Operations | Threat intelligence correlation, playbook automation, vulnerability prioritization | Medium-High |
| Change Management | Change risk prediction, conflict detection, auto-approval agents | Medium-High |
| Knowledge Management | Article generation, AI Search, semantic search, federated search | High |
| Platform Development | Code generation, flow generation, test generation, code explanation | Medium-High |
| Portfolio Management | Demand forecasting, resource optimization | Medium |
| Risk & Compliance | Risk scoring, control effectiveness prediction, audit recommendations | Medium |

---

## Licensing & AI Considerations

| Aspect | Detail |
|---|---|
| Now Assist | Add-on to ITSM, CSM, HRSD, and Creator (per-user or per-interaction pricing) |
| Now Intelligence (Predictive) | Included in ITSM Professional and above; available as add-on for other products |
| Virtual Agent | Included in ITSM Professional and above; available as add-on |
| AI Search | Included in ITSM Professional and above |
| AI Agents | Included with Now Assist subscription (consumption-based for autonomous interactions) |
| Performance Analytics | Included in Professional and above editions |
| Domain-specific LLMs | ServiceNow fine-tunes models on IT, customer service, and HR domains |
| Data privacy | Now Assist processes data within ServiceNow's trust boundary; customer data not used for model training |
| Foundation models | ServiceNow uses proprietary models and partners with select LLM providers |
| Responsible AI | ServiceNow AI governance: transparency, fairness, human oversight, data protection |
