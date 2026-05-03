---
category: requirements
loading_priority: 2
tokens_estimate: 3500
keywords: [fit-gap, analysis, OOB, configuration, customization, third-party, ISV, gap resolution, risk assessment, stack selection, scoring, decision escalation]
version: 1.0
last_updated: 2026-03-21
---

# Fit-Gap Analysis Guide

## Purpose

This reference provides a structured methodology for conducting fit-gap analysis against the four Microsoft stacks. It defines classification categories, scoring criteria, gap resolution strategies, and risk assessment guidelines. Use this after requirements gathering to evaluate how well each stack addresses the captured requirements.

## Four-Category Classification

### OOB (Out of Box)

**Definition**: Feature is available natively in the platform with no development or configuration effort. Works immediately upon provisioning.

**Characteristics**:
- No deployment, coding, or significant setup required
- Covered by standard platform licensing
- Fully supported by Microsoft with standard SLAs
- Automatically updated with platform releases

**Examples per Stack**:
- **Stack A (Power Platform)**: Dataverse CRUD operations, basic form layouts, standard connectors, out-of-box security roles
- **Stack B (Azure PaaS)**: Azure AD authentication, Azure SQL geo-replication, App Service auto-scaling, Key Vault secret management
- **Stack C (Containers/AKS)**: Kubernetes pod scheduling, horizontal pod autoscaler, Azure CNI networking, managed identity for pods
- **Stack D (D365)**: Standard D365 Sales opportunity pipeline, D365 F&O general ledger, D365 Customer Service case management

### Config (Configuration)

**Definition**: Feature is available via platform settings, admin console, declarative tools, or no-code builders. No custom code is written.

**Characteristics**:
- Achieved through admin UI, configuration files, or declarative tooling
- May require platform-specific knowledge but not development skills
- Generally survives platform upgrades with minimal rework
- Covered by standard platform support

**Examples per Stack**:
- **Stack A**: Dataverse business rules, Power Automate cloud flow triggers, model-driven app sitemap customization, security role configuration
- **Stack B**: App Service deployment slots, Azure SQL firewall rules, APIM policy expressions, Application Insights alert rules
- **Stack C**: Kubernetes resource limits/requests, ConfigMaps and Secrets, ingress controller routing rules, namespace-level RBAC
- **Stack D**: D365 entity customization (adding fields), business process flow modification, security role adjustment, workflow configuration

### Customization

**Definition**: Requires development effort including code, scripts, plugins, custom components, or extensions. Involves a build-test-deploy lifecycle.

**Characteristics**:
- Requires developers with platform-specific coding skills
- Must be maintained through platform upgrades (potential breaking changes)
- Needs dedicated testing (unit, integration, UAT)
- Increases solution complexity and ongoing maintenance cost

**Examples per Stack**:
- **Stack A**: PCF controls, custom connectors with C# code, Power Apps component libraries, Canvas app complex logic
- **Stack B**: Azure Functions with custom business logic, custom APIs on App Service, Logic Apps custom connectors, Durable Functions orchestrations
- **Stack C**: Custom microservices, DAPR state stores with custom serialization, sidecar containers, custom Kubernetes operators
- **Stack D**: D365 plugins (C#), JavaScript web resources, custom D365 forms with TypeScript, AL extensions for Business Central

### Third Party

**Definition**: Not available natively in the platform. Requires an ISV solution, marketplace app, partner-built component, or external SaaS integration.

**Characteristics**:
- Introduces vendor dependency beyond Microsoft
- Additional licensing cost and procurement process
- Support split between Microsoft and the third-party vendor
- Integration complexity varies by solution maturity

**Examples per Stack**:
- **Stack A**: AppSource apps for Power Platform, third-party PDF generation, external e-signature integration (DocuSign, Adobe Sign)
- **Stack B**: Third-party monitoring tools (Datadog, Splunk), ISV API gateways, specialized AI/ML platforms
- **Stack C**: Service mesh (Istio/Linkerd), external secret managers (HashiCorp Vault), third-party container registries
- **Stack D**: D365 AppSource ISV solutions, third-party EDI providers, specialized industry vertical add-ons

---

## Scoring Matrix

### Coverage Scoring Per Requirement

| Score | Label | Meaning |
|---|---|---|
| 4 | OOB | Fully met out of box |
| 3 | Config | Met via configuration, no code |
| 2 | Customization | Requires development effort |
| 1 | Third Party | Requires external solution |
| 0 | Not Feasible | Cannot be met within this stack |

### Stack-Level Scoring

Calculate the **weighted fit score** per stack:

```
Stack Fit Score = SUM(Requirement_Priority_Weight * Fit_Score) / SUM(Requirement_Priority_Weight * 4)
```

Where `Requirement_Priority_Weight` is:
- **Must Have (MoSCoW M)**: Weight = 3
- **Should Have (MoSCoW S)**: Weight = 2
- **Could Have (MoSCoW C)**: Weight = 1
- **Won't Have (MoSCoW W)**: Weight = 0 (excluded from scoring)

A Stack Fit Score above **0.75** indicates strong alignment. Below **0.50** signals significant gaps.

### Stack-Specific Coverage Patterns

**Stack A (Power Platform)**: strong OOB/Config coverage for:
- Simple CRUD applications, approval workflows, basic reporting
- Standard business processes with fewer than 20 entities
- Citizen developer scenarios, rapid prototyping

**Stack B (Azure PaaS)**: fills gaps where Power Platform reaches limits:
- High-volume data processing, complex integrations, custom APIs
- Advanced security requirements (private endpoints, WAF, custom encryption)
- Complex business logic beyond low-code expression capabilities

**Stack C (Containers/AKS)**: addresses scenarios beyond PaaS:
- Polyglot microservices, legacy app modernization (lift-and-shift)
- Workloads requiring fine-grained infrastructure control
- Multi-cloud or hybrid-cloud portability requirements

**Stack D (D365)**: strong OOB/Config/ISV coverage for:
- Standard ERP processes (finance, supply chain, manufacturing)
- Standard CRM processes (sales, service, marketing)
- Industry-specific solutions with ISV ecosystem support

---

## Gap Resolution Strategies

When a requirement cannot be met OOB or via Config, apply the following resolution strategies in order of preference:

### 1. Accept Gap (Defer)
- **When**: Requirement is low priority (Could Have) and does not block go-live
- **Action**: Document the gap, add to future phase backlog
- **Risk**: Stakeholder dissatisfaction if expectation is not managed

### 2. Workaround (Alternative Approach)
- **When**: Requirement can be approximated using existing platform capabilities in a non-standard way
- **Action**: Document the workaround, its limitations, and conditions for revisiting
- **Risk**: Workarounds may be fragile, hard to maintain, or confusing to users

### 3. Customize (Build)
- **When**: Requirement is Must Have or Should Have and no workaround exists within the platform
- **Action**: Estimate development effort, add to sprint backlog, design for upgrade resilience
- **Risk**: Ongoing maintenance, upgrade compatibility, developer dependency

### 4. Procure (Buy ISV/Third Party)
- **When**: A mature ISV solution exists that meets the requirement with acceptable licensing cost
- **Action**: Evaluate ISV maturity (reviews, customer base, support SLA), negotiate licensing, plan integration
- **Risk**: Vendor lock-in, licensing cost escalation, support gaps

### 5. Hybrid (Platform + Custom)
- **When**: Requirement spans platform capabilities and custom code. Part can be met OOB, part requires development.
- **Action**: Maximize platform coverage, minimize custom code surface area
- **Risk**: Complexity at the boundary between platform and custom components

---

## Risk Assessment Per Gap Category

| Category | Risk Level | Key Risks | Mitigation |
|---|---|---|---|
| OOB | Low | Platform changes could alter behavior | Monitor release notes, use preview environments |
| Config | Low-Medium | Configuration drift across environments; upgrade may reset settings | Use solution packaging, ALM pipelines, config-as-code |
| Customization | Medium-High | Maintenance burden; upgrade breaking changes; developer turnover | Automated testing, coding standards, documentation, CI/CD |
| Third Party | Medium | Vendor dependency; licensing cost changes; support quality; EOL risk | Multi-vendor evaluation, contractual SLA, exit strategy |

---

## Decision Escalation Criteria

A gap should trigger **reconsideration of the stack selection** when any of the following conditions are met:

1. **Volume threshold**: More than 30% of Must Have requirements fall into Customization or Third Party categories for the selected stack
2. **Cost threshold**: Estimated customization cost exceeds 40% of the total project budget
3. **Timeline threshold**: Customization effort pushes go-live beyond the acceptable timeline by more than 25%
4. **Risk threshold**: Three or more Must Have requirements are scored "Not Feasible" (0) for the selected stack
5. **Architectural threshold**: A single requirement forces an architectural pattern that conflicts with the stack's design philosophy (e.g., requiring sub-millisecond latency on Stack A)

When escalation criteria are met, conduct a **stack reassessment workshop** with the architecture review board before proceeding.

---

## Output Format

Document fit-gap results using the following table format:

```markdown
| Req ID | Requirement | Priority | Stack | Fit-Gap | Gap Resolution | Risk | Notes |
|---|---|---|---|---|---|---|---|
| REQ-BP-001 | Order approval workflow | Must Have | A | OOB | N/A | Low | Power Automate approval flow |
| REQ-INT-003 | SAP integration (IDoc) | Must Have | B | Customization | Build | Medium-High | Logic Apps SAP connector + custom mapping |
| REQ-DAT-005 | 500M row analytics | Should Have | B | Config | N/A | Low-Medium | Azure Synapse serverless SQL pool |
| REQ-SEC-002 | HIPAA compliance | Must Have | B | Config | N/A | Low-Medium | Azure compliance controls + BAA |
| REQ-UX-004 | Offline mobile | Could Have | A | Third Party | Procure | Medium | Evaluate Resco or custom PWA |
```

### Summary Metrics

After completing the fit-gap table, calculate and present:

- **Total requirements analyzed**: Count
- **OOB coverage**: Percentage of requirements met OOB
- **Config coverage**: Percentage met via configuration
- **Customization needed**: Percentage requiring development
- **Third Party needed**: Percentage requiring ISV solutions
- **Not Feasible**: Percentage that cannot be met
- **Overall Stack Fit Score**: Weighted score per formula above
- **Escalation triggered**: Yes/No with explanation
