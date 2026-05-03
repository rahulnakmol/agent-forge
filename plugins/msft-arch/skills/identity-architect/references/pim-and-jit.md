# PIM and Just-in-Time Access

Privileged Identity Management eliminates standing privileged access. The principle: **PIM for any role above Reader on production. Just-in-time elevation, time-bounded.** This file covers PIM for Azure roles vs Entra roles, approval workflows, time-bound eligibility, and audit trail requirements.

---

## What PIM Governs

| Scope | Examples |
|---|---|
| **Entra roles** | Global Administrator, Privileged Role Administrator, Security Administrator, User Administrator, Exchange Administrator |
| **Azure resource roles** | Owner, Contributor, User Access Administrator on subscriptions, RGs, and resources |
| **PIM for Groups** | Just-in-time membership in Entra security groups that carry privileged app permissions |

License required: **Microsoft Entra ID P2** (or Microsoft Entra ID Governance). Included in M365 E5.

---

## Eligibility vs Active Assignment

| Assignment type | Standing access | Use when |
|---|---|---|
| **Eligible** | No (user must activate) | Default for all privileged roles on production |
| **Active (time-bound)** | Yes, until expiry | Break-fix situations; new starters during onboarding window |
| **Active (permanent)** | Yes, indefinitely | Never for privileged roles. Reader on non-prod only if justified. |

The goal: zero permanently active assignments above Reader on production. Every activation creates an audit trail.

---

## PIM for Azure Roles: Configuration

### Set up eligible assignment via Terraform (azurerm_pim_eligible_role_assignment)

```hcl
resource "azurerm_pim_eligible_role_assignment" "prod_contributor" {
  scope              = azurerm_resource_group.prod.id
  role_definition_id = data.azurerm_role_definition.contributor.id
  principal_id       = data.azuread_user.platform_engineer.object_id

  schedule {
    expiration {
      duration_days = 365   # eligible for 1 year; must be renewed
    }
  }

  justification = "Platform engineer: production incident response. PIM eligible only."
}
```

### Configure role settings (activation rules)

In the Entra portal (ID Governance > PIM > Azure Resources > Role Settings), or via Graph API, set per-role:

| Setting | Recommended value |
|---|---|
| Max activation duration | 2–4 hours for Contributor; 1 hour for Owner |
| Require justification | Yes |
| Require approval | Yes for Owner/User Access Admin; optional for Contributor |
| Require MFA on activation | Yes |
| Send notifications | Role admin + user + approver |
| Require ticket information | Yes (link to incident/change ticket) |

---

## PIM for Entra Roles

```powershell
# Assign a user as eligible for Global Administrator via PowerShell
# Requires Microsoft.Graph module

$params = @{
    "@odata.type" = "#microsoft.graph.unifiedRoleEligibilityScheduleRequest"
    action        = "adminAssign"
    principalId   = "user-object-id"
    roleDefinitionId = "62e90394-69f5-4237-9190-012177145e10"  # Global Admin
    directoryScopeId = "/"
    scheduleInfo = @{
        startDateTime = (Get-Date).ToUniversalTime().ToString("o")
        expiration = @{
            type        = "afterDuration"
            duration    = "P365D"
        }
    }
    justification = "Emergency global admin: eligible only, max 1h activation, approval required"
}

New-MgRoleManagementDirectoryRoleEligibilityScheduleRequest -BodyParameter $params
```

---

## Approval Workflow Design

For production Owner and User Access Administrator roles, require at least one approver. Approver choices:
- **Role admin group**: A dedicated PIM approvers security group (2–3 members). Avoid single approver to prevent single point of failure.
- **24-hour window**: Requests expire after 24 hours if not approved. Configure alerts so approvers are notified immediately.
- **Justification + ticket**: Require the requestor to link to an incident or change ticket. Automated alerting on activations without a matching ticket can detect policy violations.

---

## Time-Bounded Eligibility (Preventing "Orphaned" Eligible Assignments)

Eligible assignments should have an end date, at minimum 1 year, reviewed annually:
- Quarterly access reviews via Entra ID Governance (Access Reviews).
- Automated alert when eligible assignment expires and was never activated (may indicate a stale assignment to remove).
- Offboarding checklist: revoke eligible assignments on departure, not just active assignments.

---

## Audit Trail

PIM generates rich audit logs. Forward to Log Analytics:

```bash
az monitor diagnostic-settings create \
  --name pim-audit-to-law \
  --resource /subscriptions/<subId>/providers/microsoft.aadiam \
  --logs '[{"category":"AuditLogs","enabled":true},{"category":"SignInLogs","enabled":true}]' \
  --workspace /subscriptions/<subId>/resourceGroups/ops/providers/Microsoft.OperationalInsights/workspaces/myLAW
```

### KQL: All PIM activations in the last 7 days

```kusto
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName == "Add member to role completed (PIM activation)"
| extend ActivatedRole = tostring(TargetResources[0].displayName)
| extend ActivatedBy   = tostring(InitiatedBy.user.userPrincipalName)
| extend Duration      = tostring(AdditionalDetails[?(@.key == "Duration")].value)
| project TimeGenerated, ActivatedBy, ActivatedRole, Duration, ResultDescription
| order by TimeGenerated desc
```

### KQL: Activations without matching ticket reference

```kusto
AuditLogs
| where OperationName == "Add member to role completed (PIM activation)"
| extend Justification = tostring(AdditionalDetails[?(@.key == "Justification")].value)
| where Justification !matches regex @"[A-Z]+-\d+"   // no ticket pattern e.g. INC-1234
| project TimeGenerated, InitiatedBy, TargetResources, Justification
```

---

## PIM for Groups (Advanced Pattern)

When an Entra security group controls app permissions (e.g., a group that is assigned a custom Dynamics 365 role), use PIM for Groups to apply just-in-time membership:

1. Create the group as a "role-assignable group" in Entra.
2. Configure the group in PIM > Groups.
3. Users activate group membership just-in-time rather than having standing membership.

This pattern is useful for applications that use group claims for authorization and cannot be configured for direct PIM role eligibility.

---

## Common Gaps to Flag in Reviews

| Gap | Risk | Fix |
|---|---|---|
| Active permanent Contributor on production subscription | Standing access = blast radius on account compromise | Convert to PIM eligible; remove permanent assignment |
| PIM configured but no approval on Owner role | Owner elevation is self-service with no oversight | Add approval workflow for Owner and User Access Administrator |
| No access reviews scheduled | Stale eligible assignments accumulate | Configure quarterly access reviews for all production eligible assignments |
| Break-glass accounts in PIM eligible pool | Break-glass must be immediately usable in emergencies | Exclude break-glass from PIM; they have permanent credentials stored offline |
| Activation duration set to 8+ hours | Long activation = reduced audit frequency | Max 4 hours for Contributor; 1 hour for Owner; emergency extensions via re-activation with justification |
