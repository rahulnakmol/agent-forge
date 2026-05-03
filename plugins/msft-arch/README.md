# Microsoft Architecture Skills

**Your enterprise architecture superpowers for Claude Code.**

A suite of **32 specialist skills across 5 tiers** that turn Claude into a senior Microsoft Solutions Architect. Each skill does one thing exceptionally well, like a UNIX toolchain for enterprise architecture. The orchestrator agent (`agent`) composes them into powerful workflows; vertical specialists build solutions; horizontal architects review them in parallel; authored specialists cover no-upstream domains; Odin (`odin`) acts as your always-available design advisor and conflict resolver.

> **v5.3.0 (Phase 4).** New long-tail specialists: `maui-architect`, `sre-architect`, `dotnet-modernization`, `defender-sentinel`. This is the FINAL phase of the v5 expansion: the plugin is now at 32 skills across 5 tiers. See [the design spec](../../docs/superpowers/specs/2026-05-02-msft-arch-horizontal-tiers-design.md) for the full roadmap.

> **v5.2.0 (Phase 3).** New authored specialists: `microsoft-graph`, `m365-platform`, `accessibility`, `azure-sql-architect`. `data-architect` adds Azure SQL handoff. `docs` adds live-architecture diagrams from Resource Graph (Mermaid-from-RG). 24 to 28 skills.

> **v5.1.0 (Phase 2).** New: `finops-architect`, `observability-architect`, `cicd-architect`, `threat-model`. `identity-architect` and `security-architect` promoted from trigger-based to always-on. Odin gains conflict-resolver mode. The plugin grows from 20 to 24 skills; phases 3-4 will reach 32 total. See [the design spec](../../docs/superpowers/specs/2026-05-02-msft-arch-horizontal-tiers-design.md) for the roadmap.

> **v5.0.0 (Phase 1).** Added `dotnet-architect`, `iac-architect`, `identity-architect`, `security-architect`. Plugin grew from 16 to 20 skills.

> **Progressive disclosure.** Install the full suite but only pay the context cost for what you use. Skills load on demand (~1-2k tokens each), not all at once.

---

## Quick Start

### 1. Install

```bash
# Add the marketplace (one-time setup)
/plugin marketplace add rahulnakmol/agent-marketplace

# Install the architecture suite
/plugin install msft-arch@agent-marketplace
```

### 2. Try It

```
You: /msft-arch:agent Design a customer portal on Azure with D365 CE integration

agent: Orchestrating end-to-end:
  1. discover    -> Gathering your requirements...
  2. stack-select -> Stack D (D365) + B (Azure PaaS) selected
  3. d365-architect -> D365 CE design with portal integration
  4. azure-architect -> Azure PaaS services, identity, networking
  5. [parallel] identity-architect, security-architect, finops-architect, observability-architect (always-on)
  6. odin         -> Conflict resolver (security vs finops findings)
  7. artifacts    -> ADR, Effort, RAID workbooks generated
  8. docs         -> HLD + LLD documentation produced
  9. validate     -> Quality gate passed
```

**That's it.** One command triggered 9 specialist skills working in concert. Each produced focused, high-quality output.

---

## The Skills

### Overview: 5 Tiers, 32 Skills

```
                          agent (orchestrator)
                               |
     +----------+--------------+--------------+------------------+-----------+
     |          |              |              |                  |           |
  PROCESS   VERTICALS    HORIZONTALS    SPECIALISTS            OUTPUT    CROSS-CUT
     |          |              |              |                  |           |
  discover   azure-arch   [always-on]   microsoft-graph       spec        odin
  stack-sel  pp-arch      identity     m365-platform         artifacts   standards
  requirem   d365-arch    security     accessibility           docs
  validate   container-.. finops       azure-sql-arch
             data-arch    observ       maui-architect
             ai-arch      [triggered]  sre-architect
                          dotnet-arch  dotnet-modernization
                          iac-arch     defender-sentinel
                          cicd-arch
                          threat-model
                                  |
                    tom-architect (business)
```

---

### Tier 0: Foundation

| Skill | What It Does |
|-------|-------------|
| **standards** | The shared brain. Canonical source for preferred coding stack, FP paradigm, DDD principles, security checklists, C4 diagram guides. Other skills read from it; zero duplication. |

### Tier 1: Process Skills

These guide you through the engagement lifecycle. Each handles one phase.

| Skill | Superpower | Example |
|-------|-----------|---------|
| **discover** | Structured intake that captures everything an architect needs | `"I need to modernize our legacy ERP"` -> Outputs a discovery brief with constraints, landscape, compliance needs |
| **stack-select** | Choose the right Microsoft stack for your scenario | Presents Stack A/B/C/D decision tree -> Outputs a stack ADR with rationale |
| **requirements** | Turn vague needs into structured requirements | Fit-gap analysis, capability mapping, MOSCOW prioritization -> Requirements register |
| **validate** | Quality gate that catches gaps before delivery | Cross-checks ADRs, requirements traceability, WAF compliance -> Validation report |

### Tier 2: Stack Specialists

Each specialist is a deep expert in one technology area. They fetch the **latest Microsoft Learn documentation** and validate against **Well-Architected Framework** pillars.

| Skill | Domain | WAF Pillars | Typical Use |
|-------|--------|-------------|-------------|
| **azure-architect** | Azure PaaS/IaaS: App Service, Functions, APIM, Azure SQL, networking, identity | Azure WAF (5 pillars) | `"Design an event-driven order processor on Azure"` |
| **powerplatform-architect** | Power Apps, Power Automate, Copilot Studio, Dataverse, Power Pages | Power Platform WAF (5 pillars) | `"Build a case management app on Power Platform"` |
| **d365-architect** | Dynamics 365 CE, F&O, Business Central, dual-write, ISV | Success by Design | `"Design a D365 F&O implementation for manufacturing"` |
| **container-architect** | AKS, Container Apps, DAPR, GitOps, Flux, service mesh | Azure WAF (container-focused) | `"Containerize our microservices on AKS with GitOps"` |
| **data-architect** | Fabric, Databricks, Power BI, data governance, DuckDB | Fabric WAF | `"Design a lakehouse on Microsoft Fabric"` |
| **ai-architect** | Azure OpenAI, Copilot Studio, agent frameworks, RAG, guardrails | Responsible AI principles | `"Design an AI agent for claims processing"` |

### Tier 3: Horizontal Architects (Phase 1 + Phase 2)

Horizontals run after verticals. Always-on horizontals run for every engagement; triggered horizontals run when specific signals appear.

#### Always-on (Phase 2: all four now always-on)

| Skill | Owns | Notes |
|-------|------|-------|
| **identity-architect** | Entra ID, B2C / External ID, Managed Identity, RBAC, CA, PIM | Promoted to always-on in v5.1.0 |
| **security-architect** | Defender for Cloud, Key Vault, secret scanning, SBOM, OWASP | Promoted to always-on in v5.1.0 |
| **finops-architect** | Cost modeling, budget alerts, tagging, RI/Savings Plans, rightsizing | New in v5.1.0 |
| **observability-architect** | SLOs, dashboards, alert rules, distributed tracing, log retention | New in v5.1.0 |

#### Triggered (signal-based)

| Skill | Trigger Signals |
|-------|----------------|
| **dotnet-architect** | .NET in stack (stack-pinned after azure-architect) |
| **iac-architect** | "deployment", "infrastructure", Terraform, Bicep |
| **cicd-architect** | "deployment pipeline", "release", "CI/CD" |
| **threat-model** | "compliance", "regulated", "PII", or security-architect flags security-sensitive design |

### Tier 3C: Authored Specialists (Phase 3, no-upstream domains)

These four skills cover domains where awesome-copilot has no upstream content. All are authored as original IP in plugin voice. Three are stack-pinned, one is trigger-based.

| Skill | Owns | Routing Mode |
|-------|------|--------------|
| **microsoft-graph** | Graph API patterns, app vs delegated permissions, batch, change notifications, throttling, beta-vs-v1.0 governance, SDKs (.NET v5+, JS v3+) | Stack-pinned: chains after any vertical needing M365 data |
| **m365-platform** | SPFx 1.20+, Microsoft 365 Agents Toolkit (formerly Teams Toolkit), Office.js add-ins, Adaptive Cards Universal Action Model, Graph Connectors, Viva, bundle-size budgets | Stack-pinned: chains after `powerplatform-architect` when SPFx or Teams in scope |
| **accessibility** | WCAG 2.2 AA for Power Apps, Power Pages, Blazor, Office add-ins, Teams; ARIA, keyboard navigation, screen-reader patterns, remediation playbook | Trigger-based: Power Platform UIs, Blazor, or any user-facing UI in scope |
| **azure-sql-architect** | Azure SQL DB / MI / Edge tuning, Hyperscale, Query Store, partitioning, Always Encrypted, audit + ledger, failover groups, connection resilience | Stack-pinned: chains after `data-architect` or `azure-architect` when Azure SQL is the data store |

### Tier 2D: Long-tail Specialists (Phase 4, v5.3.0)

Four new skills for no-upstream domains with deep content. All are authored as original IP in plugin voice.

| Skill | Owns | Routing Mode |
|-------|------|--------------|
| **maui-architect** | .NET MAUI 9 cross-platform mobile (iOS, Android, Windows, macOS via Mac Catalyst), Shell navigation, CommunityToolkit.Mvvm (source-generated), Blazor Hybrid (70%+ reuse gate), offline-first SQLite + sync, Azure Notification Hubs, Key Vault Code Signing | Trigger-based: "mobile", "cross-platform", "iOS", "Android", "MAUI" |
| **sre-architect** | SLI/SLO/SLA decomposition, error budgets, multi-window multi-burn-rate alerting (Google SRE Workbook), Azure Chaos Studio experiments, blameless postmortems, on-call rotation design, runbook authoring, incident command (ICS), Polly reliability patterns (circuit breakers, bulkheads), toil reduction | Trigger-based: "SLA", "SLO", "SLI", "uptime target", "error budget", "chaos", "on-call" |
| **dotnet-modernization** | .NET Framework 4.x to .NET 8/9 LTS migration, ASP.NET to Core, WCF to gRPC (internal) or HTTP+OpenAPI (external), EF6 to EF Core, Web Forms to Blazor Server, strangler-fig strategy, .NET Upgrade Assistant + GitHub Copilot modernization agent, Windows Container fallback, test-coverage-first prerequisite | Chain-after-discover: fires when "legacy", "modernize", ".NET Framework", "Web Forms", "WCF", "EF6" detected |
| **defender-sentinel** | DEEP Defender for Cloud plan design by resource type (Server, App Service, SQL, Storage, Container, Key Vault, ARM, DNS), regulatory compliance dashboard, secure score, Sentinel workspace topology (single vs hub-and-spoke), data connectors, analytics rules (scheduled/NRT/Fusion/ML/Microsoft security), hunting KQL, SOAR playbooks via Logic Apps, MITRE ATT&CK mapping required on every rule | Explicit-only trigger: "Sentinel", "SOC", "SIEM", "SOAR", "analytics rule", "hunting query", "MITRE" |

### Tier 4: Output Skills

These generate the deliverables.

| Skill | What It Produces |
|-------|-----------------|
| **spec** | Tech specs per epic/story: `spec/design/*.md` with Mermaid C4 diagrams, API contracts, implementation tasks |
| **artifacts** | Excel workbooks: ADR, Effort Estimation, RAID Log, Solution Design, Test Strategy |
| **docs** | HLD + LLD documentation in docx/markdown format |

### Cross-Cutting: Odin

| Mode | Invocation | What It Does |
|------|-----------|-------------|
| **Interactive** | `/msft-arch:odin` | Deep design review, ultrathink mode, enters plan mode for thorough analysis |
| **Advisory** | Auto-invoked by agent at pipeline checkpoints | Read-only lateral thinker: challenges assumptions, proposes alternatives, validates security |
| **Conflict resolver** | Auto-invoked by agent after all horizontals complete | Reads every horizontal's handoff, identifies contradictions, produces a Resolution Memo with one decision per conflict |

### Business Architecture

| Skill | What It Does |
|-------|-------------|
| **tom-architect** | Target Operating Model design: L1-L4 process decomposition, maturity assessments, capability maps across Finance, HR, Procurement, SCM, Cyber, and Sustainability |

---

## By-Scenario Recipes

Four pre-baked pipelines, one per phase, that show which skills fire and why.

### Scenario 1 (Phase 1): Multi-tenant SaaS on Azure

*Build a multi-tenant SaaS on Azure with .NET 9, Entra ID, Terraform, Defender enabled.*

```
discover -> stack-select -> requirements
  -> azure-architect
  -> dotnet-architect (stack-pinned: .NET in stack)
  -> identity-architect (always-on)
  -> security-architect (always-on)
  -> finops-architect (always-on)
  -> observability-architect (always-on)
  -> iac-architect (trigger: "Terraform" mentioned)
  -> odin (conflict resolver)
  -> spec -> artifacts -> docs
  -> validate (Council of Three)
```

Routing note: `dotnet-architect` fires because `.NET 9` appears in requirements (stack-pinned after `azure-architect`). `iac-architect` fires because `Terraform` is explicit. No Phase 2 trigger keywords present, so `cicd-architect` and `threat-model` do not fire.

### Scenario 2 (Phase 2): Production rollout with SLOs and STRIDE-A

*Production rollout plan: SLOs, cost model, STRIDE-A, observability.*

```
discover -> stack-select -> requirements
  -> azure-architect
  -> dotnet-architect (stack-pinned: .NET in stack)
  -> identity-architect (always-on)
  -> security-architect (always-on)
  -> finops-architect (always-on)
  -> observability-architect (always-on)
  -> cicd-architect (trigger: "rollout" / "CI/CD")
  -> threat-model (trigger: "STRIDE-A" explicit)
  -> odin (conflict resolver: security vs finops on logging volume)
  -> spec (with ADRs in spec/decisions/) -> artifacts -> docs
  -> validate (Council of Three)
```

Routing note: `sre-architect` does NOT fire here even though "SLOs" appears, because `sre-architect` is a Phase 4 skill that fires on explicit SLO/error-budget governance requests. `observability-architect` (Phase 2, always-on) covers SLO design at orientation level in this scenario.

### Scenario 3 (Phase 3): M365-integrated case management

*SPFx + Power Apps + Graph + WCAG-AA + Azure SQL.*

```
discover -> stack-select -> requirements
  -> powerplatform-architect (Stack A: Power Apps canvas)
  -> azure-architect (Azure backend)
  -> data-architect -> azure-sql-architect (stack-pinned: Azure SQL is data store)
  -> m365-platform (stack-pinned: SPFx + Teams in scope)
  -> microsoft-graph (stack-pinned: Teams chat = Graph data)
  -> identity-architect (always-on)
  -> security-architect (always-on)
  -> finops-architect (always-on)
  -> observability-architect (always-on)
  -> accessibility (trigger: Power Apps + WCAG mentioned)
  -> threat-model (trigger: regulated + PII implied by case management)
  -> odin (conflict resolver: security vs finops on Graph webhook log retention)
  -> spec -> artifacts -> docs (live-architecture diagram via Mermaid-from-RG)
  -> validate (Council of Three)
```

Routing note: `azure-sql-architect` fires because Azure SQL is the chosen data store (stack-pinned after `data-architect`). `accessibility` fires because Power Apps canvas is a user-facing UI in scope. `defender-sentinel` does NOT fire because the request does not mention Sentinel, SOC, or SIEM explicitly.

### Scenario 4 (Phase 4): Modernize legacy .NET ERP with MAUI mobile + SRE + Sentinel

*Modernize a legacy .NET Framework 4.8 ERP: add MAUI mobile companion + define SRE practice with SLOs + integrate Sentinel SOC.*

```
discover -> dotnet-modernization (chain: ".NET Framework" + "Modernize" detected)
  -> stack-select -> requirements
  -> azure-architect (target hosting)
  -> dotnet-architect (stack-pinned: .NET 9 target)
  -> maui-architect (trigger: "MAUI mobile companion" explicit)
  -> identity-architect (always-on)
  -> security-architect (always-on)
  -> finops-architect (always-on)
  -> observability-architect (always-on)
  -> defender-sentinel (trigger: "Sentinel SOC" + "MITRE" explicit)
  -> sre-architect (trigger: "SLOs" + "error budgets" explicit)
  -> iac-architect (trigger: deployment implicit)
  -> cicd-architect (trigger: rollout implicit)
  -> threat-model (trigger: SOC2 + SOC)
  -> odin (conflict resolver: sre vs finops on log retention; defender-sentinel vs finops on Sentinel ingestion costs)
  -> spec (with ADRs) -> artifacts -> docs
  -> validate (Council of Three)
```

Routing note: `defender-sentinel` triggers only because the user said "Sentinel SOC" and "MITRE ATT&CK-mapped analytics rules". Without those explicit words, `security-architect` (always-on) would cover Defender for Cloud at orientation level instead. `dotnet-modernization` fires immediately after `discover` because `.NET Framework 4.8` + `Modernize` are both present: it chains before `stack-select` to produce the migration strategy brief.

---

## Examples That Wow

### Example 1: Full Enterprise Engagement (5 minutes)

```
You: /msft-arch:agent
     We're building a multi-tenant SaaS for insurance claims processing.
     100k users, SOC2 required, Azure preferred, budget $15k/month.
```

**What happens:**

| Step | Skill | Output |
|------|-------|--------|
| 1 | discover | Discovery brief: Insurance vertical, enterprise scale, SOC2, Azure |
| 2 | stack-select | Stack C (Azure + Containers): ADR explains why AKS over App Service |
| 3 | azure-architect | Azure architecture: AKS, APIM, Azure SQL, Key Vault, Private Endpoints |
| 4 | container-architect | Container design: DAPR sidecars, Flux GitOps, pod security policies |
| 5 | ai-architect | Claims AI agent: Azure OpenAI + RAG for document analysis |
| 6 | [parallel] identity-architect, security-architect, finops-architect, observability-architect | Always-on horizontal reviews |
| 7 | [parallel] iac-architect, threat-model | Triggered by infrastructure + SOC2 compliance signals |
| 8 | odin | Conflict resolver: security vs finops on logging; observability vs finops on cardinality |
| 9 | requirements | 47 requirements with MOSCOW priority, fit-gap for insurance domain |
| 10 | artifacts | 5 Excel workbooks: ADR, Effort, RAID, Solution Design, Test Strategy |
| 11 | docs | HLD (32 pages) + LLD (48 pages) with C4 diagrams |
| 12 | validate | Quality gate: all checks passed |

**Result:** A complete architecture engagement package, ready for stakeholder review.

---

### Example 2: Odin Deep Dive (2 minutes)

```
You: /msft-arch:odin
     Our microservice has 47 endpoints and 12 database tables.
     Response times are degrading. Simplify it.
```

**Odin response:**

```
## Odin Design Review

### Assessment
Your service contains 4 hidden bounded contexts sharing one database.
Cross-context queries cause N+1 problems and lock contention.

### Recommendations
1. MUST-DO: Decompose into 4 services (Claims, Assessment, Payment, Audit)
2. MUST-DO: Each context owns its database (CQRS for reporting)
3. SHOULD-DO: Replace polling with Azure Event Grid for cross-context sync
4. NICE-TO-HAVE: Add read replicas for the Assessment query load

### Proposed Architecture
[C4 Container diagram with 4 services, event bus, separate databases]

### Implementation Plan
Phase 1: Strangler fig. Extract Payment context first (lowest risk)
Phase 2: Extract Audit (write-only, no read dependencies)
Phase 3: Split Claims and Assessment (requires data migration)
```

---

### Example 3: Quick Spec for a User Story (1 minute)

```
You: /msft-arch:spec
     Spec this: As a customer, I want to receive real-time notifications
     when my claim status changes, so I can stay informed without checking.
```

**Generated files:**

```
spec/design/
  claim-notifications-design.md         # Full tech design with components table
  claim-notifications-diagrams.md       # C4 Context, Container, Dynamic diagrams
  claim-notifications-api-contracts.md  # WebSocket + REST API specs
  claim-notifications-tasks.md          # 8 ordered implementation tasks with AC
```

Each file is implementation-ready. A mid-level developer picks it up and builds.

---

### Example 4: Target Operating Model (3 minutes)

```
You: /msft-arch:tom-architect
     Design a Target Operating Model for our Finance function.
     We're moving from SAP to D365 F&O. 2,000 finance users across 12 countries.
```

**Output:**
- L1-L4 process taxonomy for Finance (Record-to-Report, Procure-to-Pay, etc.)
- Maturity assessment across 5 levels with gap analysis
- Capability map showing D365 F&O coverage per L2 process
- Organizational design with GPO overlay and shared services model
- AI augmentation overlay: which processes get copilots vs autonomous agents
- Executive deck (15 slides in PPTX) + detailed workbook (XLSX)

---

### Example 5: Production Rollout Plan (Phase 2 full pipeline)

```
You: /msft-arch:agent
     Production rollout for our SaaS platform.
     Need SLOs, cost model, STRIDE-A threat model, observability stack, CI/CD.
```

**Pipeline:**

```
discover -> stack-select -> requirements
  -> azure-architect -> dotnet-architect (stack-pinned)
  -> [parallel] identity-architect, security-architect, finops-architect, observability-architect (always-on)
  -> [parallel] iac-architect (trigger: infrastructure), cicd-architect (trigger: pipeline), threat-model (trigger: STRIDE-A)
  -> odin (conflict resolver: security vs finops on logging volume)
  -> spec (with ADRs in spec/decisions/) -> artifacts -> docs
  -> validate (Council of Three)
```

---

### Example 6: M365-Integrated Case Management (Phase 3 full pipeline)

```
You: /msft-arch:agent
     Build an M365-integrated case management app for a regulated legal firm.
     SPFx web part embedded in SharePoint Online, Power Apps canvas app for intake,
     Microsoft Graph for Teams chat notifications to caseworkers,
     Azure SQL backend (multi-tenant by firm), WCAG 2.2 AA required.
     2,000 caseworkers, $15k/month budget, SOC2 + HIPAA in scope.
```

**Pipeline:**

```
discover -> stack-select -> requirements
  -> azure-architect -> dotnet-architect (SPFx tooling + Functions for Graph webhooks)
  -> powerplatform-architect (Power Apps canvas)
  -> data-architect -> azure-sql-architect (Phase 3 stack-pinned: Azure SQL is the data store)
  -> m365-platform (Phase 3 stack-pinned: SPFx + Teams chat in scope)
  -> microsoft-graph (Phase 3 stack-pinned: Teams chat = Graph data)
  -> [parallel] identity-architect, security-architect, finops-architect, observability-architect (always-on)
  -> accessibility (Phase 3 trigger: Power Apps + WCAG mentioned)
  -> threat-model (Phase 2 trigger: SOC2 + HIPAA + PII)
  -> odin (conflict resolver: security vs finops on Graph webhook log retention; accessibility vs SPFx bundle budget)
  -> spec -> artifacts -> docs (live-architecture diagram via Mermaid-from-RG)
  -> validate (Council of Three)
```

**Phase 3 specialists each produce a structured handoff:**

- `microsoft-graph`: app vs delegated decision per call site, beta-vs-v1.0 ADR, throttling/retry strategy, $select fields per query
- `m365-platform`: SPFx version target, Teams app type (tab/bot/extension), bundle budget breakdown
- `accessibility`: WCAG 2.2 AA conformance status per UI surface, remediation backlog
- `azure-sql-architect`: tier (Hyperscale > Premium for >1TB), partition strategy (tenant), Always Encrypted columns, failover group config

---

### Example 7: Stack Specialist Direct Access (30 seconds)

You don't have to go through the full pipeline. Call specialists directly:

```
You: /msft-arch:azure-architect
     Design the networking and identity architecture for a multi-region
     Azure deployment with private endpoints and hub-spoke topology.
```

```
You: /msft-arch:finops-architect
     Review the Azure architecture above for cost optimization.
     Budget is $8k/month. Flag anything that will exceed that.
```

```
You: /msft-arch:observability-architect
     Design SLOs and dashboards for a claims processing API.
     P99 latency target: 500ms. Availability target: 99.9%.
```

```
You: /msft-arch:threat-model
     Run STRIDE-A on the claims processor architecture.
     Scope: SOC2 Type II and HIPAA BAA required.
```

Each specialist fetches the latest from **Microsoft Learn** and validates against the **Well-Architected Framework**.

---

## Skill Reference Card

Quick reference for which skill to invoke directly:

| I want to... | Invoke |
|--------------|--------|
| Start a full architecture engagement | `/msft-arch:agent` |
| Get a deep design review | `/msft-arch:odin` |
| Generate specs for a user story | `/msft-arch:spec` |
| Design Azure infrastructure | `/msft-arch:azure-architect` |
| Architect a .NET implementation | `/msft-arch:dotnet-architect` |
| Design Terraform / IaC for Azure | `/msft-arch:iac-architect` |
| Design Entra ID / B2C / Managed Identity | `/msft-arch:identity-architect` |
| Define security controls (Defender, Key Vault, SBOM) | `/msft-arch:security-architect` |
| Model costs and rightsizing | `/msft-arch:finops-architect` |
| Design SLOs, dashboards, and observability | `/msft-arch:observability-architect` |
| Design CI/CD pipelines and release strategy | `/msft-arch:cicd-architect` |
| Run STRIDE-A and compliance controls | `/msft-arch:threat-model` |
| Integrate Microsoft Graph (mail, Teams, SharePoint, OneDrive) | `/msft-arch:microsoft-graph` |
| Build SPFx, Teams app, or Office add-in | `/msft-arch:m365-platform` |
| Achieve WCAG 2.2 AA on Power Apps, Blazor, Office, or Teams UI | `/msft-arch:accessibility` |
| Tune Azure SQL (Hyperscale, partitioning, Always Encrypted, failover groups) | `/msft-arch:azure-sql-architect` |
| Design .NET MAUI cross-platform mobile (iOS, Android, Windows, macOS) | `/msft-arch:maui-architect` |
| Define SRE practice: SLOs, error budgets, chaos engineering, on-call | `/msft-arch:sre-architect` |
| Migrate .NET Framework to .NET 8/9 (strangler-fig, WCF, EF6, Web Forms) | `/msft-arch:dotnet-modernization` |
| Design Defender for Cloud plans, Sentinel SOC, analytics rules, MITRE | `/msft-arch:defender-sentinel` |
| Build on Power Platform | `/msft-arch:powerplatform-architect` |
| Implement Dynamics 365 | `/msft-arch:d365-architect` |
| Containerize with AKS | `/msft-arch:container-architect` |
| Design a data platform | `/msft-arch:data-architect` |
| Build an AI agent or copilot | `/msft-arch:ai-architect` |
| Design a Target Operating Model | `/msft-arch:tom-architect` |
| Generate architecture workbooks | `/msft-arch:artifacts` |
| Produce HLD/LLD documents | `/msft-arch:docs` |
| Start a new engagement discovery | `/msft-arch:discover` |
| Choose the right technology stack | `/msft-arch:stack-select` |
| Gather and prioritize requirements | `/msft-arch:requirements` |
| Validate architecture deliverables | `/msft-arch:validate` |

---

## How It Works

### The UNIX Philosophy

Each skill does **one thing well**:

```
discover     = "gather context"       (like `find`)
stack-select = "choose technology"    (like `which`)
azure-arch   = "design for Azure"     (like `gcc`)
odin         = "think deeply"         (like `lint`)
spec         = "generate specs"       (like `make`)
validate     = "verify quality"       (like `test`)
agent        = "compose the pipeline" (like `bash`)
```

The orchestrator (`agent`) pipes them together. Each skill's output becomes the next skill's input via a structured **handoff protocol**.

### Progressive Disclosure (Pay Only for What You Use)

| Layer | When Loaded | Cost |
|-------|------------|------|
| **Skill names** | Plugin install | ~100 tokens per skill (~2.4k total) |
| **Full SKILL.md** | You invoke a skill | ~1-2k tokens per skill |
| **Reference files** | Skill reads on demand | Variable (only relevant files loaded) |

Compare: the old monolithic skill loaded ~5k tokens on activation + up to 30k in references. The new architecture loads ~1.5k per specialist + only the references that skill needs.

### Handoff Protocol

Skills pass context to each other via structured handoff blocks:

```markdown
## Handoff: stack-select -> azure-architect
### Decisions Made
- Stack B selected (Low-code + Azure PaaS)
- Compliance: GDPR + SOX
### Context for Next Skill
- Organization: Enterprise (8,000 users)
- Region: EU West + EU North
### Open Questions
- Data residency requirements per country?
```

The orchestrator preserves full context across the pipeline. Nothing is lost between skills.

### Always-on vs. Triggered Horizontals

Phase 2 routing model:

```
After every vertical:
  -> [always-on] identity-architect, security-architect, finops-architect, observability-architect

After signal detection:
  -> [triggered] iac-architect (infrastructure signals)
  -> [triggered] cicd-architect (pipeline signals)
  -> [triggered] threat-model (compliance signals)

Stack-pinned:
  -> dotnet-architect (after azure-architect when .NET in stack)

After all horizontals:
  -> odin (conflict resolver)
```

### Microsoft Learn Integration

Every stack specialist skill uses the **Microsoft Learn MCP** to verify:
- Current service capabilities and limits
- Latest pricing and SKU options
- Best practices and reference architectures
- Code samples and quickstarts

This ensures recommendations are always current, not based on stale training data.

---

## Preferred Technology Stack

The skills recommend these technologies (in priority order). You can override with your own choices.

| # | Technology | Use For |
|---|-----------|---------|
| 1 | **.NET C# (LTS)** | Enterprise APIs, backend services, D365 plugins |
| 2 | **TypeScript + Bun** | Agent development, scripting, automation |
| 3 | **TanStack + React** | Frontend UI (motion-driven, agentic experiences) |
| 4 | **Python (typed)** | Data engineering, ML, analytics |
| 5 | **Go** | System programming, infrastructure tools |
| 6 | **X++** | D365 F&O customization only |
| 7 | **Azure SQL / PostgreSQL** | Enterprise OLTP |
| 8 | **DuckDB / SQLite** | Embedded OLAP, local-first apps |
| 9 | **Microsoft Fabric** | Enterprise data engineering + analytics |
| 10 | **Power BI** | ALL visualizations |
| 11 | **Terraform** | ALL Azure IaC (no ARM templates) |
| 12 | **Kubernetes (AKS)** | Container orchestration |

---

## Tips for Power Users

### Tip 1: Combine Odin with Any Specialist

```
You: /msft-arch:odin
     Review the output from azure-architect above.
     Is there a simpler way to achieve the same NFRs?
```

Odin challenges complexity and finds elegant alternatives.

### Tip 2: Skip the Pipeline for Quick Tasks

Don't need the full engagement? Go direct:

```
You: /msft-arch:spec
     Create specs for: US-042 - Add multi-currency support to invoicing
```

### Tip 3: AWS to Azure Conversion

```
You: /msft-arch:azure-architect
     Convert this AWS architecture to Azure-native:
     EC2 + ALB, Lambda, DynamoDB, SQS, SNS, Cognito, CloudFormation, S3
```

The specialist maps every service, identifies Azure-native advantages, and generates Terraform IaC.

### Tip 4: Odin as Your Coding Mentor

```
You: /msft-arch:odin
     This C# service has 15 classes, scattered validation,
     and uses exceptions for flow control. Show me the functional way.
```

Odin will refactor to immutable records, Result types, pure functions, and railway-oriented programming.

### Tip 5: Business + Tech in One Flow

```
You: /msft-arch:agent
     Our finance team wants to transform their operating model
     and move to D365 F&O. Start with the TOM, then design the solution.
```

agent will sequence: `tom-architect` (operating model) -> `odin` (review) -> `d365-architect` (D365 design) -> `artifacts` (workbooks) -> `docs` (documentation).

---

## Architecture

```
plugins/msft-arch/
  .claude-plugin/plugin.json

  agents/
    agent.md                    # Orchestrator (pipeline composer)
    odin.md                     # Read-only advisory agent + conflict resolver

  commands/
    agent.md                    # /agent shortcut
    odin.md                     # /odin shortcut
    discover.md                 # /discover shortcut
    design.md                   # /design shortcut (full pipeline)

  skills/
    standards/                  # Shared knowledge foundation
    discover/                   # Engagement discovery
    stack-select/               # Stack selection gate
    requirements/               # Requirements gathering
    validate/                   # Quality gate (Council of Three)
    azure-architect/            # Azure specialist
    powerplatform-architect/    # Power Platform specialist
    d365-architect/             # Dynamics 365 specialist
    container-architect/        # Container/AKS specialist
    data-architect/             # Data platform specialist
    ai-architect/               # AI/Copilot/Agent specialist
    dotnet-architect/           # .NET implementation specialist
    iac-architect/              # Terraform / IaC specialist
    identity-architect/         # Identity and access specialist
    security-architect/         # Security controls specialist
    finops-architect/           # Cost optimization specialist (v5.1.0)
    observability-architect/    # SLO and observability specialist (v5.1.0)
    cicd-architect/             # CI/CD pipeline specialist (v5.1.0)
    threat-model/               # STRIDE-A threat modeling (v5.1.0)
    microsoft-graph/            # Graph API patterns and SDK (v5.2.0)
    m365-platform/              # SPFx, Teams, Office, Viva, Graph Connectors (v5.2.0)
    accessibility/              # WCAG 2.2 AA application + remediation (v5.2.0)
    azure-sql-architect/        # Azure SQL platform tuning (v5.2.0)
    maui-architect/             # .NET MAUI cross-platform mobile (v5.3.0)
    sre-architect/              # SRE: SLOs, error budgets, chaos (v5.3.0)
    dotnet-modernization/       # .NET Framework -> .NET 8/9 migration (v5.3.0)
    defender-sentinel/          # Deep Defender for Cloud + Sentinel SOC (v5.3.0)
    spec/                       # Tech spec generator
    artifacts/                  # Workbook generator
    docs/                       # Document generator
    odin/                       # Design advisor (interactive mode)
    tom-architect/              # Target Operating Model
```

---

## Cross-Plugin Dependencies

For full functionality, also install:

| Dependency | What It Adds |
|-----------|-------------|
| `writing` | `humanize` skill for voice calibration in generated documents |

```bash
/plugin install writing@agent-marketplace
```

---

## Version History

| Version | Date | Highlights |
|---------|------|-----------|
| **5.3.0** | 2026-05-03 | Phase 4 long-tail specialists: maui-architect, sre-architect, dotnet-modernization, defender-sentinel. Final Routing Decision Table covers all 32 skills. FINAL phase of the v5 expansion: 28 to 32 skills. |
| **5.2.0** | 2026-05-03 | Phase 3 authored specialists: microsoft-graph, m365-platform, accessibility, azure-sql-architect. data-architect adds Azure SQL handoff. docs adds Mermaid-from-Resource-Group live-architecture pattern. Original IP across 32 authored files; no upstream content ported. 24 to 28 skills. |
| **5.1.0** | 2026-05-02 | Phase 2 horizontals: finops-architect, observability-architect, cicd-architect, threat-model. identity-architect and security-architect promoted to always-on. Odin gains conflict-resolver mode. 20 to 24 skills. |
| **5.0.0** | 2026-05-02 | Horizontal architect tier (Phase 1): dotnet-architect, iac-architect, identity-architect, security-architect. azure-architect carved out (~30% shrinkage) with quick-reference handoffs. 9 new standards reference packs. Orchestrator gains stack-pinned + trigger-based routing. Inspired by [github/awesome-copilot](https://github.com/github/awesome-copilot) (MIT), content authored fresh in plugin voice. |
| 4.0.0 | 2026-03-28 | UNIX philosophy refactoring: 16 specialist skills, pipeline orchestration, handoff protocol, MS Learn MCP integration, WAF validation per specialist, ai-architect, shared standards foundation |
| 3.0.0 | 2026-03-21 | Stack selection, 5 artifact workbooks, tech-design-first specs, FP/DDD paradigm, odin mode |
| 2.0.0 | 2025-11-09 | Context-optimized progressive loading, 85-95% context reduction |
| 1.0.0 | 2025-09-01 | Initial release with WAF frameworks and delivery methodology |

---

## License

BSD 3-Clause License. See [LICENSE.txt](skills/odin/LICENSE.txt) in each skill directory for individual terms.
