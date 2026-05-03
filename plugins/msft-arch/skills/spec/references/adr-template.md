# ADR-NNNN: [Short, decisive title]

## Status

Proposed | Accepted | Superseded by ADR-NNNN | Deprecated

## Context

What is the issue motivating this decision? Describe the forces at play:
technical, organizational, regulatory. State the decision drivers (cost,
performance, compliance, time-to-market).

Keep this section factual. No advocacy yet.

## Decision

We will [decisive verb] [thing]. State the choice in one or two sentences.

## Consequences

### Positive
- What gets better as a result of this decision

### Negative
- What gets worse, what we accept as the cost

### Neutral
- What changes but is neither better nor worse

## Alternatives Considered

### Alternative 1: [name]

Why we did not choose this alternative, evaluated against the decision drivers above. [One substantive paragraph: address the specific drivers in Context, not generic trade-offs.]

### Alternative 2: [name]

Why we did not choose this alternative, evaluated against the decision drivers above. [One substantive paragraph: address the specific drivers in Context, not generic trade-offs.]

(At least two alternatives. "Do nothing" is a valid alternative if relevant.)

## References

- [Requirements doc, section N.N](relative/path/to/requirements.md#section-anchor)
- [Vendor docs / Microsoft Learn URL](https://learn.microsoft.com/...)
- [Related ADR (predecessor / successor / dependency)](relative/path/to/decisions/NNNN-other-decision.md)

---

## Worked Example

The following is a complete, realistic ADR for an Azure engagement. Every
section is filled substantively so reviewers understand what "good" looks like.

---

# ADR-0001: Use Terraform over Bicep for IaC

## Status

Accepted

## Context

The client is building a net-new Azure estate (five subscriptions across
development, staging, and production) to host a multi-tenant SaaS platform.
The engagement team must choose a single Infrastructure-as-Code (IaC) authoring
language for all Azure resource provisioning.

Two primary candidates emerged during discovery:

- **Terraform (HashiCorp)** with Azure Verified Modules (AVM): a
  provider-agnostic HCL-based tool with a large OSS community, remote state
  management via Azure Blob Storage or Terraform Cloud, and a rich module
  registry.
- **Bicep**: Microsoft's first-party DSL that compiles to ARM JSON. It is
  Azure-only, tightly integrated with the Azure CLI, and eliminates the need
  for a separate state backend.

Decision drivers:

1. **Multi-cloud optionality**: The client has stated a preference to avoid
   full lock-in to a single cloud and wants the ability to provision AWS or GCP
   resources for a data processing tier in 12-18 months.
2. **Team familiarity**: The delivery team has three certified Terraform
   practitioners; no Bicep expertise is present on either the client or vendor
   side.
3. **Module reuse**: The client's central platform team mandates use of the
   Azure Verified Modules (AVM) library. AVM publishes modules for both
   Terraform and Bicep, so neither tool loses points here.
4. **State management**: Bicep is stateless (ARM manages state). Terraform
   requires explicit remote state (Azure Blob Storage with state locking via
   Azure Blob Lease). The added operational surface is non-trivial but well
   understood by the team.
5. **CI/CD integration**: GitHub Actions is the chosen CI/CD platform.
   Both tools have mature GitHub Actions integrations.

## Decision

We will use **Terraform** (OpenTofu-compatible HCL) with the
`hashicorp/azurerm` provider and Azure Verified Modules (AVM) as the
authoritative IaC language for all Azure resource provisioning on this
engagement.

Remote state is stored in an Azure Blob Storage account in the management
subscription with Blob Lease-based state locking. The `iac-architect` skill
owns module structure and pipeline integration details.

## Consequences

### Positive
- Team can begin delivering immediately using existing Terraform expertise,
  with no ramp-up cost on a new language.
- Multi-cloud optionality is preserved; the same toolchain can provision AWS
  or GCP resources when the data processing tier decision is made.
- Terraform plan output in pull requests gives reviewers a precise diff of
  infrastructure changes before merge, improving change-risk visibility.
- AVM modules are available for the target Azure services (App Service, APIM,
  Azure SQL, Key Vault, Virtual Network), so module coverage is not a
  constraint.
- OpenTofu compatibility means the client is not locked to HashiCorp's BSL
  licensing terms.

### Negative
- Remote state introduces an additional Azure resource (Storage Account,
  container, lock mechanism) and an operational concern (state drift, state
  lock release on pipeline failure).
- Bicep's ARM-native type system and what-if preview are marginally more
  precise for Azure-only changes; we forgo that precision.
- The Terraform `azurerm` provider sometimes lags behind the ARM API by weeks
  to months for newly released Azure services. Workarounds (AzAPI provider
  or `azurerm_resource_group_template_deployment`) add complexity when new
  services are required before provider support ships.

### Neutral
- The AVM module selection process is the same regardless of tool. The
  `iac-architect` skill applies the same vetting criteria to either Bicep or
  Terraform AVM modules.
- Azure Policy and RBAC definitions are authored in JSON regardless of the
  IaC layer; this decision does not affect their format.

## Alternatives Considered

### Alternative 1: Bicep

Bicep is Microsoft's first-party DSL for Azure resource management. It is
stateless (ARM manages state directly), has near-zero Azure API lag, and
benefits from first-party tooling in VS Code and the Azure CLI. We chose not
to adopt Bicep because: (a) the delivery team has no Bicep expertise and the
ramp-up timeline conflicts with the Phase 1 delivery date; (b) Bicep is
Azure-only, which forecloses the multi-cloud optionality the client explicitly
requires; and (c) while AVM publishes Bicep modules, the community module
ecosystem for edge cases is substantially smaller than Terraform's. Bicep
remains the recommended choice for pure Azure-only teams with first-party
tooling preference; it is not the right fit for this engagement.

### Alternative 2: Pulumi (TypeScript)

Pulumi allows infrastructure to be authored in general-purpose languages
(TypeScript, Python, Go). This is attractive because the application
development team uses TypeScript, and a unified language could reduce context
switching. We chose not to adopt Pulumi because: (a) the platform team's AVM
mandate requires using published AVM modules, and Pulumi's Azure provider does
not surface AVM modules natively; bridging would require wrapping Bicep or
Terraform modules, negating the advantage; (b) Pulumi's state backend is
either Pulumi Cloud (SaaS, additional cost and data-residency concern) or
self-hosted (significant operational overhead); and (c) the delivery team has
no Pulumi experience, making the ramp-up risk identical to Bicep without the
AVM alignment benefit.

## References

- [Azure Verified Modules: Terraform module library](https://aka.ms/avm)
- [Terraform azurerm provider changelog and Azure API lag tracker](https://github.com/hashicorp/terraform-provider-azurerm/blob/main/CHANGELOG.md)
- [OpenTofu compatibility statement](https://opentofu.org/docs/intro/migration/terraform/)
- [Microsoft Learn: Choose an IaC tool for Azure](https://learn.microsoft.com/en-us/azure/developer/terraform/overview)
- Engagement requirements doc: `docs/discovery/phase1-nfrs.md`, section 4.3 (Multi-cloud optionality)
- Related ADRs: ADR-0003 (Managed Identity for service-to-service auth, which affects how Terraform configures Managed Identity on each resource)
