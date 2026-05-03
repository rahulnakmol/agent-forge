---
category: "capability-mapping"
loading_priority: 2
tokens_estimate: 2800
keywords: [ai-capabilities, salesforce, agentforce, einstein, trust-layer, data-cloud-ai, generative-ai, predictive-ai]
version: "1.0"
last_updated: "2026-03-28"
---

# Salesforce AI Capabilities — TOM Process Categories to Salesforce AI Features

## Overview

Salesforce AI is built around Agentforce (autonomous AI agents), Einstein AI (predictive and generative), and the Einstein Trust Layer (safe AI with zero data retention). Data Cloud provides the unified data foundation for AI across all Salesforce clouds. This reference maps Salesforce AI capabilities to TOM process categories.

---

## Agentforce — Autonomous AI Agents

Agentforce enables organizations to build, deploy, and manage autonomous AI agents that take action across Salesforce applications.

| Agent | Cloud | TOM Process Category | Description |
|---|---|---|---|
| Einstein SDR Agent | Sales Cloud | Lead-to-Cash | Autonomously qualifies inbound leads, engages via email/chat, books meetings with sales reps |
| Einstein Sales Coach Agent | Sales Cloud | Lead-to-Cash | Simulates buyer objections for rep training, provides deal coaching |
| Einstein Service Agent | Service Cloud | Customer Service | Resolves customer cases autonomously using knowledge base, escalates complex issues to humans |
| Einstein Commerce Agent | Commerce Cloud | Order-to-Cash | Provides personalized shopping assistance, handles product inquiries, facilitates checkout |
| Einstein Marketing Agent | Marketing Cloud | Marketing & Campaigns | Generates campaign briefs, optimizes send times, creates audience segments |
| Einstein Analytics Agent | Tableau / CRM Analytics | Cross-functional | Answers business questions in natural language, generates visualizations on demand |
| Custom Agents | Any Cloud (Agent Builder) | Any | Build custom agents using Agent Builder with topics, actions, and guardrails |

### Agent Builder Components

| Component | Description |
|---|---|
| Topics | Define the agent's scope of responsibility (e.g., "Order Status", "Return Processing") |
| Actions | Map to Salesforce Flows, Apex, APIs, or MuleSoft integrations the agent can execute |
| Guardrails | Policy-based boundaries for agent behavior (e.g., max discount authority, escalation triggers) |
| Instructions | Natural language instructions that shape agent reasoning and responses |
| Testing Center | Simulate agent conversations and validate behavior before deployment |

---

## Einstein AI — Predictive & Generative

### Predictive AI

| Capability | Cloud | TOM Process Category | Description |
|---|---|---|---|
| Lead Scoring | Sales Cloud | Lead-to-Cash | ML-predicted conversion likelihood for lead prioritization |
| Opportunity Scoring | Sales Cloud | Lead-to-Cash | Win probability prediction for pipeline management |
| Forecasting AI | Sales Cloud | Lead-to-Cash | AI-adjusted forecasts based on historical patterns and pipeline signals |
| Case Classification | Service Cloud | Customer Service | Auto-classify case type, priority, and routing based on case content |
| Case Routing | Service Cloud | Customer Service | ML-optimized case assignment to best-fit agent or queue |
| Engagement Scoring | Marketing Cloud | Marketing & Campaigns | Predict contact engagement likelihood for send optimization |
| Next Best Action | Any Cloud | Cross-functional | Strategy-based AI recommendations surfaced in the flow of work |
| Einstein Discovery | CRM Analytics | Cross-functional | No-code predictive modeling and root cause analysis |

### Generative AI

| Capability | Cloud | TOM Process Category | Description |
|---|---|---|---|
| Sales Emails | Sales Cloud | Lead-to-Cash | Generate personalized outreach emails grounded in CRM data |
| Call Summaries | Sales Cloud (Einstein Conversation Insights) | Lead-to-Cash | Auto-summarize sales calls with action items and key moments |
| Case Summaries | Service Cloud | Customer Service | Summarize case history for agent context or customer communication |
| Knowledge Article Generation | Service Cloud | Customer Service | Draft knowledge articles from resolved case data |
| Reply Recommendations | Service Cloud | Customer Service | Generate suggested responses grounded in knowledge base |
| Campaign Content | Marketing Cloud | Marketing & Campaigns | Generate email copy, subject lines, and SMS content |
| Product Descriptions | Commerce Cloud | Order-to-Cash | Auto-generate product descriptions from catalog data |
| Code Generation | Salesforce Platform | Platform Development | Einstein for Developers: generate Apex, LWC, SOQL from prompts |

---

## Einstein Trust Layer

| Feature | Description |
|---|---|
| Zero Data Retention | Customer data sent to LLMs is not stored or used for model training |
| Data Masking | PII and sensitive fields are masked before sending to LLMs |
| Toxicity Detection | Output is screened for harmful, biased, or inappropriate content |
| Prompt Injection Defense | Guards against prompt manipulation and adversarial inputs |
| Audit Trail | Full logging of all AI prompts, responses, and actions for compliance |
| Grounding with Data Cloud | AI responses grounded in customer's own data via RAG, reducing hallucination |
| Citation & Attribution | Generative responses include source references to knowledge articles or records |

---

## Data Cloud AI

| Capability | Description | TOM Process Category |
|---|---|---|
| Unified Customer Profiles | AI-powered identity resolution across all data sources | Cross-functional |
| Calculated Insights | ML-computed metrics on unified profiles (e.g., lifetime value, propensity) | Cross-functional |
| Segmentation AI | AI-assisted audience segmentation based on behavior and attributes | Marketing & Campaigns |
| Activation | Push AI-computed segments to any Salesforce cloud or external channel | Marketing & Campaigns |
| Einstein Copilot (Data Cloud) | Natural language queries against unified data ("Show me high-value customers at risk of churn") | Cross-functional |
| Vector Database | Native vector storage for RAG patterns and semantic search | Platform |
| Data Graphs | Relationship mapping across unified data for agent grounding | Cross-functional |

---

## Prompt Engineering in Salesforce

| Feature | Description |
|---|---|
| Prompt Builder | Low-code tool to create reusable prompt templates with merge fields from CRM data |
| Prompt Templates | Sales Emails, Record Summaries, Field Generation, Flex (custom) template types |
| Grounding | Ground prompts in CRM records, Data Cloud, Knowledge, or Flow outputs |
| Prompt Chaining | Chain multiple prompts together for multi-step reasoning |
| Model Selection | Choose foundation model per prompt (OpenAI, Anthropic, Google, Salesforce xGen) |
| Workspace Testing | Test prompts with real or sample records before deployment |

---

## Process Automation Candidates (AI-Augmented)

| Process | Automation Type | AI Enhancement | Expected Impact |
|---|---|---|---|
| Lead qualification | Agentforce SDR | Autonomous lead engagement, scoring, meeting booking | 50-70% of leads handled without rep involvement |
| Case resolution | Agentforce Service Agent | Autonomous case resolution via knowledge and actions | 30-50% of cases resolved without human agent |
| Email outreach | Generative AI | Personalized email generation grounded in account context | 3x increase in rep email productivity |
| Forecasting | Predictive AI | AI-adjusted forecasts with deal risk signals | 15-25% improvement in forecast accuracy |
| Data entry | Einstein Activity Capture + AI | Auto-log emails, meetings; auto-populate fields | 5+ hours saved per rep per week |
| Customer onboarding | Flow Orchestrator + Agentforce | Guided onboarding with AI-assisted document generation | 40% faster customer time-to-value |
| Campaign optimization | Marketing AI | Send-time optimization, content generation, A/B testing | 20-30% improvement in engagement rates |
| Product discovery | Commerce AI | AI-powered search, recommendations, guided shopping | 15-25% increase in conversion rates |

---

## AI Capability-to-TOM Process Category Mapping

| TOM Process Category | Salesforce AI Capabilities | Maturity |
|---|---|---|
| Lead-to-Cash | Lead scoring, opportunity scoring, SDR Agent, sales emails, call summaries, forecasting AI | High |
| Customer Service | Case classification, routing, Service Agent, case summaries, reply recommendations | High |
| Marketing & Campaigns | Engagement scoring, campaign content generation, Marketing Agent, send-time optimization | High |
| Order-to-Cash | Commerce Agent, product recommendations, product descriptions, order management AI | Medium-High |
| Cross-functional Analytics | Einstein Discovery, Analytics Agent, natural language queries, Data Cloud insights | High |
| Platform & Development | Code generation, Prompt Builder, Agent Builder, Flow automation | High |
| Customer Data Management | Data Cloud identity resolution, calculated insights, segmentation AI | High |
| Field Service | Scheduling optimization, mobile AI assist, predictive maintenance | Medium |

---

## Licensing & AI Considerations

| Aspect | Detail |
|---|---|
| Einstein AI (predictive) | Included in Enterprise and Unlimited editions of Sales/Service Cloud |
| Agentforce | Per-conversation pricing (autonomous agent interactions) |
| Einstein Trust Layer | Included with Einstein AI features |
| Data Cloud | Included (limited) in Enterprise+; full Data Cloud licensed per-profile |
| Prompt Builder | Included in Enterprise+ editions |
| MuleSoft AI | Included with MuleSoft Anypoint subscription |
| Foundation models | Salesforce partners with OpenAI, Anthropic, Google, and offers proprietary xGen models |
| Data privacy | Einstein Trust Layer ensures zero data retention with LLM providers |
| Bring Your Own Model | Supported via Einstein AI Model Builder for custom or third-party models |
