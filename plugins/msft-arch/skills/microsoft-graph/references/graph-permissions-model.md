# Microsoft Graph Permissions Model

Every Graph call carries an access token, and every access token carries scopes. Picking the wrong model (application vs delegated) or the wrong scope (`*.All` when `*.Shared` would do) produces an integration that either fails consent review or accumulates governance debt forever. Application permissions when running as a daemon or service. Delegated when acting on behalf of a user. Never confuse these.

---

## Application vs Delegated: the rule

| Caller context | Permission type | Token flow | Identity backing |
|---|---|---|---|
| Daemon, scheduled job, message-queue worker, server-to-server | Application | Client credentials (OAuth 2.0 v2.0) | Managed Identity (preferred) federated to an Entra app registration; certificate credential as fallback |
| Web app or API acting in the user's name | Delegated | Authorization code with PKCE, then bearer token; or on-behalf-of for downstream APIs | User's signed-in token, MSAL handles acquisition and caching |
| Single-page app (SPA) | Delegated | Authorization code with PKCE in the browser via MSAL.js | Browser session, redirect-based |
| Native desktop or mobile app | Delegated | Interactive flow via MSAL native, broker on Windows | Logged-in user |
| Background processor that occasionally needs user-context data | Hybrid: store refresh token at consent time, exchange later | OBO or refresh-token flow | Original user |

The simplest mental check: "Is there a real human waiting on this call?" If yes, delegated. If no, application. Hybrid daemons that consume queues populated by user actions still call Graph as the application; the user identity is metadata, not the caller.

---

## Granular scopes: the rule

Request the narrowest scope that satisfies the operation. Scopes ending in `.All` are tenant-wide and require admin consent: avoid them when a user-context or shared-resource scope exists.

| Operation | Avoid | Prefer |
|---|---|---|
| Read signed-in user's mailbox | `Mail.ReadWrite`, `Mail.Read.All` | `Mail.Read` |
| Read shared mailboxes the user has access to | `Mail.Read.All` | `Mail.Read.Shared` |
| Read specific SharePoint sites | `Sites.Read.All`, `Sites.ReadWrite.All` | `Sites.Selected` (with site-specific role grant) |
| Read Teams chat for a specific app | `Chat.Read.All` | Resource-Specific Consent (RSC) per chat or team |
| Read user profile basics | `User.Read.All` | `User.Read` (delegated only the signed-in user) |
| Send mail as the signed-in user | `Mail.Send.All` | `Mail.Send` |
| Read a single calendar | `Calendars.ReadWrite.All` | `Calendars.Read.Shared` |

If a scope exists in both application and delegated forms, the application form usually has broader reach (e.g. application `Mail.Read` reads any mailbox in the tenant). Pair the scope with `Sites.Selected`-style narrowing or RSC when the platform supports it.

---

## Sites.Selected: the SharePoint trick

Default `Sites.Read.All` reads every site in the tenant. `Sites.Selected` ships zero access at consent time, and a tenant admin grants per-site permissions to the app via Graph: `POST /sites/{site-id}/permissions`. The roles are `read`, `write`, `owner`. This is the only viable per-site scoping pattern for production multi-tenant apps.

```http
POST https://graph.microsoft.com/v1.0/sites/{site-id}/permissions
Content-Type: application/json

{
  "roles": ["read"],
  "grantedToIdentities": [
    {
      "application": {
        "id": "{app-client-id}",
        "displayName": "My Background Worker"
      }
    }
  ]
}
```

Document in the architecture which sites the app needs and the rotation procedure for the per-site grants.

---

## Resource-Specific Consent (RSC) for Teams

For Teams data, RSC scopes (`ChannelMessage.Read.Group`, `Chat.Read.Chat`, `TeamMember.Read.Group`) require a Teams app manifest and a team owner consent rather than tenant-wide admin consent. RSC is the right pattern for any Teams-bound app that should not have global Teams reach.

Configuration lives in the Teams app manifest under `webApplicationInfo.applicationPermissions`. Ship the manifest with the app: do not request the equivalent `*.All` scope as a fallback.

---

## Consent flows

| Flow | When | Notes |
|---|---|---|
| Admin consent (tenant-wide) | Application permissions, or delegated `*.All` scopes | Use admin consent endpoint or tenant admin grants in the Entra portal |
| User consent | Delegated scopes that do not require admin consent | Most user-mailbox-scoped reads fall here |
| Incremental consent | SPA or web app that adds scopes over time | MSAL handles the additional consent prompt; do not request all scopes at sign-in |
| Pre-authorized scopes (`/.default`) | Daemon apps; web app calling Graph with all pre-approved scopes | Returns whatever the admin has consented to; cannot be filtered |

For multi-tenant apps, the consent screen the customer admin sees is a direct list of the scopes the app declares: minimize aggressively or expect deal-blocking review.

---

## App registration checklist

- [ ] Single-tenant or multi-tenant declared explicitly (do not default to `common`)
- [ ] Redirect URIs match deployed environments only (no localhost in prod registration)
- [ ] Application permissions list is the minimum the daemon needs
- [ ] Delegated permissions list is the minimum the user-context flows need
- [ ] No client secret if Managed Identity or Workload Identity Federation can replace it
- [ ] Certificate credential preferred over client secret when a credential is unavoidable
- [ ] Federated credentials configured for GitHub Actions / AKS / on-premises CI per identity-decision-tree.md
- [ ] Token validation in receiving APIs validates `tid`, `iss`, `aud`
- [ ] Owners list scrubbed; no individual employees as sole owners

---

## Verification queries to run

Use Microsoft Learn MCP to confirm the current scope list before finalizing:

```text
microsoft_docs_search "Microsoft Graph permissions reference {resource name}"
microsoft_docs_search "Sites.Selected SharePoint permissions Graph"
microsoft_docs_search "Resource-specific consent Teams app manifest"
```

Graph permissions ship updates regularly: a scope that used to require `*.All` may now have a narrower form. Verify before recommending.

---

## Trade-offs and exceptions

- **Multi-tenant SaaS**: every additional scope is a friction point at customer sign-up. Build a scope-on-demand model where features unlock as the customer admin grants more.
- **Consent fatigue**: stage consent across the user journey, do not request everything on first sign-in.
- **`/.default` scope**: returns the union of pre-authorized scopes for the app. Useful for daemons, dangerous for delegated flows because it bypasses incremental consent and surfaces every static scope.
- **Resource-specific consent for Chat resources**: still expanding GA coverage; some operations require the broader `*.All` as a fallback.
- **Application permissions in External ID tenants**: Graph application permissions in customer tenants behave differently and have stricter limits. Verify per scenario.
