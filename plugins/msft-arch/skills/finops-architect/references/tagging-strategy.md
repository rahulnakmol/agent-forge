# Tagging Strategy

Tagging is the foundation of every FinOps capability. You cannot allocate costs, enforce showback, or detect anomalies by team if resources carry no metadata. Tag every resource on day 1, no exceptions.

---

## Mandatory Tags (enforced via Azure Policy: Deny effect)

All five tags below are required on every Azure resource, no exceptions. Resources missing any mandatory tag are non-compliant and blocked from deployment after the policy Deny effect activates.

| Tag Key | Description | Allowed Values / Format |
|---------|-------------|------------------------|
| `cost-center` | Finance cost center code mapped to the resource's owning team or product | `CC-<4-digit code>`, e.g. `CC-1042`, `CC-PROD` |
| `environment` | Deployment environment | `production`, `staging`, `dev`, `sandbox` |
| `owner` | Primary responsible team or individual (for escalation, anomaly triage) | Team name or email: `platform-team`, `jane.doe@contoso.com` |
| `project` | Product or project name the resource belongs to | Lowercase, hyphen-separated: `orders-api`, `identity-service` |
| `expiry` | Date after which the resource should be reviewed for deletion (ISO 8601 date or `never`) | `2027-06-30`, `never` |

---

## Recommended Additional Tags

These are not enforced by policy but are strongly recommended for mature FinOps implementations.

| Tag Key | Description | Example |
|---------|-------------|---------|
| `app` | Application name, for resource groups that host multiple apps | `checkout-service` |
| `tier` | Architectural tier | `frontend`, `api`, `data`, `infra`, `security` |
| `created-by` | Identity or automation that created the resource (useful for debugging orphan resources) | `terraform`, `iac-pipeline`, `john.smith@contoso.com` |
| `criticality` | Business criticality (drives retention and SLA decisions) | `critical`, `high`, `medium`, `low` |
| `data-classification` | Data sensitivity (drives security and compliance controls) | `public`, `internal`, `confidential`, `restricted` |

---

## Tag Naming Convention

- **Lowercase only**: no mixed case, no camelCase.
- **Hyphens as separators**: no underscores, no spaces, no dots.
- **No special characters**: alphanumeric and hyphens only.
- **Max key length**: 512 characters (Azure limit; keep keys under 32 in practice).
- **Max value length**: 256 characters.

---

## Canonical Schema: YAML (for IaC variable files)

Use this schema as the single source of truth in your Terraform variable files. Import it into every module via a `locals` block.

```yaml
# tags.yaml -- checked into the repository root
# All values are required. The CI pipeline validates this file on PR.
mandatory_tags:
  cost_center: "CC-1042"
  environment: "production"          # production | staging | dev | sandbox
  owner: "platform-team"
  project: "orders-platform"
  expiry: "never"                    # ISO 8601 date or "never"

recommended_tags:
  app: "orders-api"
  tier: "api"
  created_by: "terraform"
  criticality: "critical"
  data_classification: "confidential"
```

---

## Terraform Implementation

### Module-level tag merge pattern

Every Terraform module accepts a `tags` variable and merges with module-default tags. This prevents any resource from being deployed without the mandatory set.

```hcl
# variables.tf (in every module)
variable "tags" {
  description = "Mandatory tags that every resource in this module inherits."
  type = object({
    cost_center  = string
    environment  = string
    owner        = string
    project      = string
    expiry       = string
  })
}

variable "extra_tags" {
  description = "Optional additional tags merged on top of mandatory tags."
  type        = map(string)
  default     = {}
}

locals {
  all_tags = merge(
    {
      cost-center = var.tags.cost_center
      environment = var.tags.environment
      owner       = var.tags.owner
      project     = var.tags.project
      expiry      = var.tags.expiry
    },
    var.extra_tags
  )
}

# Usage in every resource block:
# tags = local.all_tags
```

### Root module instantiation

```hcl
# main.tf (root module)
module "app_service" {
  source = "./modules/app-service"

  tags = {
    cost_center = "CC-1042"
    environment = "production"
    owner       = "platform-team"
    project     = "orders-platform"
    expiry      = "never"
  }

  extra_tags = {
    app  = "orders-api"
    tier = "api"
  }
}
```

---

## Azure Policy: Tag Enforcement

### Phase 1: Audit (first 30 days)

Deploy the Audit policy immediately. It logs non-compliant resources without blocking deployments. Use the 30-day window to identify gaps and fix IaC.

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "allOf": [
        { "field": "tags['cost-center']", "exists": "false" },
        { "field": "tags['environment']", "exists": "false" },
        { "field": "tags['owner']", "exists": "false" },
        { "field": "tags['project']", "exists": "false" },
        { "field": "tags['expiry']", "exists": "false" }
      ]
    },
    "then": {
      "effect": "audit"
    }
  }
}
```

### Phase 2: Deny (after 30-day ramp-up)

Switch to Deny effect. Any resource missing one or more mandatory tags fails deployment at the ARM layer, before any infrastructure is created.

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        { "field": "tags['cost-center']", "exists": "false" },
        { "field": "tags['environment']", "exists": "false" },
        { "field": "tags['owner']", "exists": "false" },
        { "field": "tags['project']", "exists": "false" },
        { "field": "tags['expiry']", "exists": "false" }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

### Tag inheritance policy (resource groups → resources)

Resources created via the Azure portal without IaC often miss tags. Tag inheritance copies resource group tags to child resources automatically.

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "field": "tags['cost-center']",
      "exists": "false"
    },
    "then": {
      "effect": "modify",
      "details": {
        "roleDefinitionIds": [
          "/providers/microsoft.authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
        ],
        "operations": [
          {
            "operation": "addOrReplace",
            "field": "tags['cost-center']",
            "value": "[resourceGroup().tags['cost-center']]"
          }
        ]
      }
    }
  }
}
```

---

## Compliance Reporting

Track tag compliance weekly. Chargeback is only appropriate when compliance is above 90%. Below that threshold, finance data is too unreliable for internal billing.

```kql
// Tag compliance report -- run in Azure Resource Graph Explorer
Resources
| where isnotnull(tags)
| extend
    has_cost_center  = isnotnull(tags["cost-center"]),
    has_environment  = isnotnull(tags["environment"]),
    has_owner        = isnotnull(tags["owner"]),
    has_project      = isnotnull(tags["project"]),
    has_expiry       = isnotnull(tags["expiry"])
| extend fully_compliant = (has_cost_center and has_environment and has_owner and has_project and has_expiry)
| summarize
    total_resources    = count(),
    compliant          = countif(fully_compliant),
    non_compliant      = countif(not(fully_compliant))
| extend compliance_pct = round(100.0 * compliant / total_resources, 1)
```

---

## Tag Governance Runbook

1. **Week 0 (IaC)**: Add `tags` variable to every Terraform module. Merge into every `resource` block via `local.all_tags`.
2. **Week 0 (Policy)**: Deploy Audit policy to all subscriptions.
3. **Day 1–30 (Ramp-up)**: Review compliance report weekly. Assign owners to non-compliant resource groups. Fix IaC, not resources manually.
4. **Day 31 (Enforce)**: Switch policy effect to Deny. All new deployments blocked if tags missing.
5. **Monthly (Ongoing)**: Review expiry-tagged resources whose `expiry` date has passed. File decommission request or update date.
6. **Quarterly (Review)**: Validate cost-center codes against the latest finance chart of accounts. Mismatched codes produce incorrect showback reports.
