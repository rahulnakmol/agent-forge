# B2C vs External ID

Decision guide for customer identity (CIAM) on Microsoft's platform. The short version: **External ID for everything new; B2C only for existing deployments or proven capability gaps**.

---

## The Strategic Picture

Azure AD B2C is no longer available for purchase by new customers as of May 1 2025. Microsoft Entra External ID is the strategic CIAM platform; all new investment and features land there. If you are starting a new project, the question is not "B2C or External ID?" The answer is External ID. The question becomes "which External ID capabilities do I need and are they GA?"

---

## Decision Matrix

| Dimension | Entra External ID | Azure AD B2C |
|---|---|---|
| **Strategic direction** | Active investment, new features | Maintenance mode for existing customers |
| **New customer availability** | Yes | No (end of sale May 2025) |
| **Tenant model** | Separate external tenant (not workforce) | Dedicated B2C tenant |
| **User flow complexity** | Built-in user flows; custom extensions via API | Identity Experience Framework (IEF) custom policies: XML-based, full control |
| **Social providers** | Google, Facebook, Apple, OIDC/SAML federation | Same + broader legacy IdP support via IEF |
| **Custom branding** | Company branding API + per-user-flow customization | Custom HTML/CSS/JS page layouts: pixel-perfect control |
| **MFA options** | TOTP, SMS, email OTP, FIDO2/passkeys | TOTP, SMS, email OTP (passkeys via custom extension) |
| **Token customization** | Claims mapping + custom auth extensions (GA) | Custom policies (IEF): full token control |
| **Multi-tenant SaaS isolation** | Per-external-tenant isolation | Requires custom policy for per-org isolation |
| **Pricing** | MAU-based; M2M add-on for client credentials | MAU-based |
| **Microsoft.Identity.Web support** | Full SDK support | Full SDK support |
| **Max user flows per tenant** | 10 | Effectively unlimited via custom policies |

---

## When B2C Is Still the Right Answer

1. **Existing production B2C deployment**: migration is advisable but not urgent. B2C continues to operate; plan a migration window.
2. **Complex multi-step user journeys** that require IEF-level control: step-up authentication mid-flow, complex claims transformations, multi-page custom HTML layouts.
3. **Team already has deep IEF expertise** and the engagement is purely about extending an existing B2C policy.

Do not start new projects on B2C. If a client insists, document the reason in an ADR and revisit at the next architecture review.

---

## External ID User Flow Capabilities (as of Q2 2026)

User flows in External ID handle the most common CIAM patterns without custom policies:

- Sign-up and sign-in (email/password, email OTP, social: Google, Facebook, OIDC/SAML)
- Self-service password reset
- Profile editing
- MFA (TOTP, SMS, email OTP)
- Custom attributes collection at sign-up
- Custom branding per tenant (background, logo, colors, text)
- Token claims customization via custom authentication extensions

**Gaps still exist for edge cases**: use `microsoft_docs_search` to verify current GA status before telling a client that a specific capability is available. External ID releases features frequently; the gap list shrinks each quarter.

---

## Migration Path: B2C to External ID

Microsoft provides an official migration guide. The high-level stages:

1. **Inventory**: Users, app registrations, user flows / custom policies, identity providers, token customizations, custom HTML templates.
2. **Map capabilities**: Identify each B2C feature in use; find the External ID equivalent or confirm a gap.
3. **Create external tenant**: Separate from workforce tenant. Configure branding, user flows, IdPs.
4. **Register applications**: New app registrations in the external tenant. Update redirect URIs.
5. **Migrate users** (if needed): Microsoft Graph API bulk user import with password hash sync or forced reset.
6. **Run parallel**: Keep B2C operational; cut traffic over gradually (traffic splitting at API gateway or DNS level).
7. **Decommission B2C**: After traffic validation, retire the B2C tenant.

**Key consideration**: Password hashes can be migrated from B2C if you export them (requires a B2C custom policy that exposes hashes). Without hash migration, all users reset passwords on first External ID login; plan user communication accordingly.

---

## External ID Custom Authentication Extensions

For scenarios needing token augmentation (add claims from your database at token issuance), use Custom Authentication Extensions: an HTTP endpoint you own that Entra calls during the token issuance event:

```json
// Token issuance start event payload (your extension receives this)
{
  "type": "microsoft.graph.authenticationEvent.tokenIssuanceStart",
  "data": {
    "authenticationContext": {
      "user": { "id": "...", "mail": "..." },
      "clientId": "..."
    }
  }
}

// Your response adds claims
{
  "data": {
    "@odata.type": "microsoft.graph.onTokenIssuanceStartResponseData",
    "actions": [{
      "@odata.type": "microsoft.graph.tokenIssuanceStartAction",
      "claims": {
        "SubscriptionTier": "Premium",
        "TenantSlug": "contoso"
      }
    }]
  }
}
```

This replaces the B2C REST technical profile pattern and works with standard user flows; no IEF required.
