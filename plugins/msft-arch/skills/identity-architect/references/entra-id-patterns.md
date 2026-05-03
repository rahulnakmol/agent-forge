# Entra ID Patterns

Patterns for workforce tenant application registrations, token validation, and access control. Complements `standards/references/security/identity-decision-tree.md` with implementation depth.

---

## App Registrations vs Enterprise Applications

Every application in Entra has two objects:

| Object | What it is | Where configured |
|---|---|---|
| **App Registration** | The application's identity definition: client ID, redirect URIs, API permissions, app roles, secrets/certs | Home tenant (`Entra ID > App registrations`) |
| **Enterprise Application (Service Principal)** | The instantiation of that app in a specific tenant: user/group assignments, SSO settings, provisioning | Every tenant that consents to the app |

**Single-tenant apps**: Registration and enterprise app live in the same tenant. Straightforward.

**Multi-tenant apps**: Registration in the "home" tenant; enterprise apps created automatically in every tenant that grants consent. Token issuers differ per tenant.

---

## App Roles vs Group Claims

Two patterns for conveying user permissions in tokens:

### App Roles (preferred for API authorization)

Define roles in the app registration manifest:

```json
"appRoles": [
  {
    "allowedMemberTypes": ["User", "Application"],
    "displayName": "Inventory Reader",
    "id": "b1234567-89ab-cdef-0123-456789abcdef",
    "isEnabled": true,
    "value": "Inventory.Read"
  }
]
```

Assign users or groups to roles via the enterprise application. Roles appear in the token as the `roles` claim; no directory read permission is needed by the API.

### Group Claims (use when roles map directly to AD groups)

Configure group claims on the token in the app registration. Drawback: large group memberships can cause token size issues (>200 groups triggers the `_claim_names` overage pattern; your API must fetch group membership via Graph).

**Recommendation**: App roles for API-level authorization. Groups for broad access patterns (e.g., "all marketing users"). Never mix both without documenting the claim resolution order.

---

## Multi-Tenant Token Validation

For multi-tenant apps, accepting tokens from the `common` endpoint without validation is a critical security flaw; any Entra tenant can issue tokens that pass signature verification.

Always validate:
1. **`tid` (tenant ID)**: Must be in your allow-list of known tenants (or your own tenant for single-tenant).
2. **`iss` (issuer)**: Must match `https://login.microsoftonline.com/{tenantId}/v2.0`. The `common` issuer (`https://login.microsoftonline.com/common/v2.0`) is never a valid issuer for a real token; it is only used during the auth flow.

### Microsoft.Identity.Web Configuration (.NET)

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

// appsettings.json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "common",           // multi-tenant: accept tokens from any tenant
    "ClientId": "YOUR_CLIENT_ID",
    "Audience": "api://YOUR_CLIENT_ID"
  }
}
```

For multi-tenant, add an `IssuerValidator` or use the built-in `ValidIssuers` list:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(options =>
    {
        builder.Configuration.Bind("AzureAd", options);
        options.TokenValidationParameters.IssuerValidator = (issuer, token, parameters) =>
        {
            // Extract tid from token, validate against your allowed-tenants store
            var tid = (token as JwtSecurityToken)?.Claims
                .FirstOrDefault(c => c.Type == "tid")?.Value;
            if (tid is null || !_allowedTenants.Contains(tid))
                throw new SecurityTokenInvalidIssuerException("Tenant not allowed");
            return issuer;
        };
    }, jwtOptions => { });
```

---

## Daemon / Service-to-Service (Client Credentials)

Services calling APIs with no user context use the OAuth 2.0 client credentials flow. Grant application permissions (not delegated) on the target API.

```csharp
// Acquire token for a downstream API using Managed Identity + MSAL
var app = ConfidentialClientApplicationBuilder
    .Create(clientId)
    .WithClientSecret(clientSecret)   // or .WithCertificate(cert): prefer cert
    .WithAuthority($"https://login.microsoftonline.com/{tenantId}")
    .Build();

var result = await app.AcquireTokenForClient(
        new[] { "api://target-api/.default" })
    .ExecuteAsync();
```

When running on Azure: use Managed Identity + `DefaultAzureCredential` instead; no secret required. See `managed-identity-deep-dive.md`.

---

## On-Behalf-Of (OBO) Flow

For middle-tier APIs that receive a user token and need to call a downstream API on behalf of the user:

```csharp
// Exchange incoming user token for downstream API token
var result = await _confidentialApp
    .AcquireTokenOnBehalfOf(
        scopes: new[] { "https://graph.microsoft.com/User.Read" },
        userAssertion: new UserAssertion(incomingBearerToken))
    .ExecuteAsync();
```

Requires the middle-tier app registration to have delegated permissions on the downstream API and the `api://` scope exposed by the downstream API to include the OBO grant.

---

## Token Cache Considerations

- In-memory token cache is fine for single-instance apps in dev.
- Production: use a distributed cache (`IDistributedCache` backed by Azure Cache for Redis) via `Microsoft.Identity.Web`'s `AddDistributedTokenCache()`.
- Never cache tokens in cookies or client-side storage.
