# Conditional Access Baseline

Eight baseline policies that form the non-negotiable floor for any Entra ID deployment. Deploy all of them before discussing workload-specific policies. Always deploy new policies in **report-only mode first**.

---

## The Eight Baseline Policies

| # | Policy | License | Controls |
|---|---|---|---|
| 1 | Block legacy authentication | Free / P1 | Blocks IMAP, SMTP, POP3, Exchange ActiveSync, and other legacy protocols |
| 2 | MFA for all administrators | P1 | Phishing-resistant MFA (FIDO2 / passkey) for 14+ privileged roles |
| 3 | MFA for all users | P1 | Password + second factor for all sign-ins |
| 4 | MFA for sign-in risk (Medium/High) | P2 | Risk-based step-up (requires Identity Protection) |
| 5 | Require password change for high-risk users | P2 | Compromised credential remediation |
| 6 | Protect security info registration | P1 | Only trusted networks/devices can register MFA methods |
| 7 | Device compliance for sensitive apps | P1 + Intune | Compliant or Hybrid AD joined for apps containing sensitive data |
| 8 | Block unknown/unsupported device platforms | P1 | Block sign-ins from unrecognised OS platforms |

Start with policies 1–3 (available on P1); add 4–5 when P2 is licensed.

---

## Policy 1: Block Legacy Authentication

Legacy auth (Basic Auth, NTLM over modern, older mail clients) does not support MFA; blocking it stops >99% of password spray attacks.

```json
{
  "displayName": "Block Legacy Authentication",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {
    "users": { "includeUsers": ["All"] },
    "applications": { "includeApplications": ["All"] },
    "clientAppTypes": ["exchangeActiveSync", "other"]
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["block"]
  }
}
```

**Exclusions**: Break-glass accounts only. Any other exclusion must be justified and time-limited.

---

## Policy 2: Phishing-Resistant MFA for Admins

Applies to all users assigned privileged directory roles. Requires FIDO2 security key or Windows Hello for Business; TOTP and SMS do not satisfy phishing-resistant MFA.

Roles covered (minimum): Global Administrator, Privileged Role Administrator, Security Administrator, Exchange Administrator, SharePoint Administrator, User Administrator, Billing Administrator, Conditional Access Administrator, Cloud Application Administrator.

---

## Policy 3: MFA for All Users

Requires any second factor (Authenticator push, TOTP, FIDO2, SMS). Applies to all cloud apps. Session persistence on registered devices reduces friction for returning users.

---

## Policy 4: Sign-In Risk MFA (P2)

```json
{
  "displayName": "MFA for Risky Sign-Ins",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {
    "users": { "includeUsers": ["All"] },
    "applications": { "includeApplications": ["All"] },
    "signInRiskLevels": ["high", "medium"]
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["mfa"]
  }
}
```

---

## Policy 7: Device Compliance for Sensitive Apps

```json
{
  "displayName": "Require Compliant Device for Sensitive Apps",
  "state": "enabledForReportingButNotEnforced",
  "conditions": {
    "users": { "includeUsers": ["All"] },
    "applications": {
      "includeApplications": ["<app-id-1>", "<app-id-2>"]
    }
  },
  "grantControls": {
    "operator": "OR",
    "builtInControls": ["compliantDevice", "domainJoinedDevice"]
  }
}
```

---

## Layering for Sensitive Workloads

Beyond the baseline, regulated workloads (PCI-DSS, ISO 27001, healthcare) add:

| Layer | Policy |
|---|---|
| **Azure management** | MFA required for all Azure portal / CLI / PowerShell access (separate from user MFA) |
| **Session controls** | Sign-in frequency: 1 hour for privileged roles; no persistent browser for unmanaged devices |
| **App protection** | Require Intune app protection policies on iOS/Android for Microsoft 365 data |
| **Insider risk** | Block sign-ins for users with elevated Microsoft Purview insider risk score (Purview licence required) |
| **Token binding** | Token protection (preview): binds access tokens to the device; prevents token theft/replay |

---

## Break-Glass Accounts

Every organisation needs at least two break-glass accounts that are excluded from all Conditional Access policies to prevent lockout if MFA infrastructure fails.

Requirements:
- Cloud-only accounts (not synced from on-premises AD)
- Long random passwords (20+ chars), stored in physical safe + separate sealed envelope
- No MFA registered; break-glass exists precisely because MFA may be unavailable
- Excluded only from CA policies; still require password + have strong monitoring/alerts on sign-in
- Access reviewed quarterly; sign-in triggers immediate alerting via Entra diagnostic logs → Log Analytics → alert rule

```bash
# Alert rule: break-glass sign-in
# KQL for Log Analytics alert
SigninLogs
| where UserPrincipalName in ("break-glass-1@contoso.com", "break-glass-2@contoso.com")
| project TimeGenerated, UserPrincipalName, IPAddress, Location, ResultType
```

---

## Report-Only Mode Rollout Process

1. Create policy in `report-only` state.
2. Monitor `Sign-in logs` > `Conditional Access` tab for 1–2 weeks to identify users who would be blocked.
3. Resolve exceptions: add justified exclusion groups, notify affected users.
4. Switch to `On` during a low-traffic window.
5. Monitor for 48 hours post-enforcement; revert to report-only if unexpected blocks appear.

Never skip report-only for a new policy in a production tenant.

---

## Common Misconfigurations

| Mistake | Consequence | Fix |
|---|---|---|
| Enforcing device compliance before Intune enrollment is complete | Mass user lockout | Enforce report-only until Intune coverage > 95% |
| Including break-glass accounts in all-user MFA policy | Lockout during MFA outage | Exclude break-glass from every CA policy by group |
| Blocking legacy auth without identifying service accounts using SMTP relay | Mail flow breaks | Audit SMTP relay usage; migrate to OAuth 2.0 SMTP auth or Modern Auth before blocking |
| Sign-in risk policy on P2 with incomplete Identity Protection configuration | False positives block legit users | Configure named locations (corporate IPs as trusted) before enabling risk policies |
