# Microsoft Graph SDK: .NET (v5+)

Microsoft Graph SDK > raw HTTP, except for batch beyond SDK support. The .NET SDK (`Microsoft.Graph` 5.x, built on Kiota) provides typed access to Graph, default retry middleware, automatic batch splitting, and integration with `Azure.Identity` token credentials. Pick the SDK first, drop to raw HTTP only with documented justification.

---

## Package layout

| Package | Purpose |
|---|---|
| `Microsoft.Graph` (v5+) | Generated typed client for Graph v1.0 |
| `Microsoft.Graph.Beta` | Generated typed client for Graph beta. ADR required to use in production |
| `Azure.Identity` | Token credentials (DefaultAzureCredential, ManagedIdentityCredential, ClientCertificateCredential) |
| `Microsoft.Identity.Web` | ASP.NET Core integration; controllers and Razor pages use `[AuthorizeForScopes]` |
| `Microsoft.Identity.Web.GraphServiceClient` | Bridge that wires `GraphServiceClient` into the ASP.NET DI container with on-behalf-of support |

`Microsoft.Identity.Web.MicrosoftGraph` is the legacy bridge; new code uses `Microsoft.Identity.Web.GraphServiceClient`.

---

## Picking a credential

Apply the identity decision tree first, then map to credential:

| Caller | Credential | Notes |
|---|---|---|
| Azure-hosted compute, system-assigned MI | `ManagedIdentityCredential` (no client_id) or `DefaultAzureCredential` | Default for App Service / Functions / Container Apps |
| Azure-hosted compute, user-assigned MI | `ManagedIdentityCredential(clientId)` or `DefaultAzureCredential` with `ManagedIdentityClientId` | Required for shared MI across resources |
| GitHub Actions, AKS, on-prem | `WorkloadIdentityCredential` | Requires federated credential on the Entra app |
| Local dev | `AzureCliCredential` (chained via `DefaultAzureCredential`) | `az login` on the developer's box |
| Daemon with cert (last resort) | `ClientCertificateCredential` | Cert in Key Vault, pulled at startup |
| Web app, user context | `OnBehalfOfCredential` or `Microsoft.Identity.Web` integration | OBO when calling Graph from a web API |

```csharp
// Azure-hosted, application permission, system-assigned MI
var credential = new DefaultAzureCredential();
var graphClient = new GraphServiceClient(credential,
    new[] { "https://graph.microsoft.com/.default" });
```

```csharp
// User-assigned MI: pass the client_id
var credential = new ManagedIdentityCredential(
    Environment.GetEnvironmentVariable("AZURE_MI_CLIENT_ID"));
var graphClient = new GraphServiceClient(credential,
    new[] { "https://graph.microsoft.com/.default" });
```

```csharp
// GitHub Actions via Workload Identity Federation
var credential = new WorkloadIdentityCredential();
var graphClient = new GraphServiceClient(credential,
    new[] { "https://graph.microsoft.com/.default" });
```

For application permissions, scope is always `https://graph.microsoft.com/.default`. The actual permissions come from what the tenant admin consented to on the app registration.

---

## ASP.NET Core integration (delegated, OBO)

```csharp
// Program.cs
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"))
        .EnableTokenAcquisitionToCallDownstreamApi()
            .AddMicrosoftGraph(builder.Configuration.GetSection("DownstreamApi"))
            .AddInMemoryTokenCaches();

// Controller
[ApiController]
[Route("api/[controller]")]
[Authorize]
[RequiredScope("access_as_user")]
public class CalendarController(GraphServiceClient graph) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var view = await graph.Me.CalendarView
            .GetAsync(rc =>
            {
                rc.QueryParameters.StartDateTime = DateTime.UtcNow.ToString("o");
                rc.QueryParameters.EndDateTime   = DateTime.UtcNow.AddDays(1).ToString("o");
                rc.QueryParameters.Select        = new[] { "subject", "start", "end" };
            });
        return Ok(view?.Value);
    }
}
```

---

## Page iteration

For list operations that return paged results, use `PageIterator` rather than manual `@odata.nextLink` chasing:

```csharp
var firstPage = await graphClient.Users.GetAsync(rc =>
{
    rc.QueryParameters.Select = new[] { "id", "displayName", "mail" };
    rc.QueryParameters.Top    = 100;
});

var pageIterator = PageIterator<User, UserCollectionResponse>
    .CreatePageIterator(graphClient, firstPage, user =>
    {
        // process each user
        Console.WriteLine($"{user.DisplayName} <{user.Mail}>");
        return true; // false to stop
    });

await pageIterator.IterateAsync();
```

The iterator handles `@odata.nextLink` traversal, retry on `429`, and stop signals from the callback.

---

## Batching (auto-split at 20)

```csharp
var batch = new BatchRequestContentCollection(graphClient);

var meReq = graphClient.Me.ToGetRequestInformation();
var calReq = graphClient.Me.CalendarView.ToGetRequestInformation(rc =>
{
    rc.QueryParameters.StartDateTime = DateTime.UtcNow.ToString("o");
    rc.QueryParameters.EndDateTime   = DateTime.UtcNow.AddDays(1).ToString("o");
    rc.QueryParameters.Select        = new[] { "subject", "start", "end" };
});

var meId  = await batch.AddBatchRequestStepAsync(meReq);
var calId = await batch.AddBatchRequestStepAsync(calReq);

var response = await graphClient.Batch.PostAsync(batch);

var me  = await response.GetResponseByIdAsync<User>(meId);
var cal = await response.GetResponseByIdAsync<EventCollectionResponse>(calId);
```

The SDK splits batches over 20 entries automatically.

---

## Retry middleware

Default retry middleware ships with the SDK and honours `Retry-After`. Tune by passing options:

```csharp
var handlers = GraphClientFactory.CreateDefaultHandlers();
var retry = handlers.OfType<RetryHandler>().First();
// Override retry handler options via constructor in custom handler chain

var httpClient = GraphClientFactory.Create(handlers);
var graphClient = new GraphServiceClient(httpClient, credential,
    new[] { "https://graph.microsoft.com/.default" });
```

For a circuit breaker on top of retry, wrap the chain with Polly: place the Polly handler before the SDK retry handler so Polly sees the eventual failure after retries are exhausted.

---

## Beta endpoint

`Microsoft.Graph.Beta` provides the typed client for the beta surface. Reference it as a separate `GraphServiceClient` instance, never alongside the v1.0 client in the same DI scope:

```csharp
using BetaGraph = Microsoft.Graph.Beta;

var betaClient = new BetaGraph.GraphServiceClient(credential,
    new[] { "https://graph.microsoft.com/.default" });

// Beta-only resource: requires ADR
var insights = await betaClient.Me.Analytics.ActivityStatistics.GetAsync();
```

ADR before adoption: see `beta-vs-v1-policy.md`.

---

## Diagnostic patterns

```csharp
try
{
    await graphClient.Me.GetAsync();
}
catch (ODataError ex)
{
    // ex.Error.Code, ex.Error.Message, ex.ResponseStatusCode
    if (ex.ResponseStatusCode == 429)
    {
        // Retry-After header is in ex.ResponseHeaders
    }
    throw;
}
```

The SDK throws `ODataError` for HTTP failures with the parsed `error` envelope. Inspect `Code` for the canonical Graph error code (e.g. `TooManyRequests`, `Forbidden`, `Authorization_RequestDenied`) before deciding to retry, surface, or escalate.

---

## Trade-offs and exceptions

- **Generated client size**: `Microsoft.Graph` v5 is a large package. For trim-sensitive scenarios (Native AOT, container size), consider Kiota-generated lite clients targeting only the resources you need.
- **Beta package volatility**: `Microsoft.Graph.Beta` updates every two weeks. Pin minor versions and review changelogs before upgrading.
- **`Microsoft.Identity.Web.MicrosoftGraph` legacy**: do not start new code on this; migrate to `Microsoft.Identity.Web.GraphServiceClient` when touching that area.
- **Raw HTTP**: acceptable when (a) batch dependency shape exceeds SDK support, (b) using a preview header that the SDK does not pass, (c) custom middleware wraps the entire chain. Document why in the spec.
- **Concurrency**: `GraphServiceClient` is thread-safe and intended to be a singleton or scoped service. Do not new it up per request.
