# Strangler Fig Pattern for .NET Modernization

**Applies to**: Any non-trivial .NET Framework codebase (greater than 50K LOC, active WCF contracts, or insufficient test coverage for a safe big-bang rewrite).

**Principle**: Strangler fig over big bang for any non-trivial codebase (greater than 50K LOC).

---

## When to Choose Strangler Fig vs. Big Bang

| Factor | Strangler Fig | Big Bang |
|---|---|---|
| LOC | > 50K | <= 50K |
| Test coverage | Any level (characterization tests added per phase) | High coverage existing |
| Active WCF service contracts | Yes (external consumers) | No external WCF consumers |
| Team size | Any | <= 5 engineers |
| Business continuity | Cannot afford feature freeze | Short feature freeze acceptable |
| Risk tolerance | Low: incremental, reversible | High: all-or-nothing |

Big bang is viable only when ALL of the following hold: codebase < 50K LOC, existing test suite covers critical paths, no active external WCF contracts, and a feature freeze window of 2-6 weeks is acceptable.

---

## Canonical Strangler Fig Sequence for .NET

### Phase 0: Characterization tests (pre-condition, mandatory)

Before touching any project file, establish a characterization test suite that captures the existing behaviour of the legacy app. See `references/test-coverage-first.md` for the approach. No migration work starts until this gate is met.

### Phase 1: Introduce the facade

Deploy a reverse proxy in front of the legacy application. All traffic routes through the facade initially; the legacy app behaves exactly as before. Recommended options:

- **YARP (Yet Another Reverse Proxy)**: .NET-native, hosted on .NET 8/9, configurable via `appsettings.json` or code. Preferred for .NET shops.
- **Azure API Management (APIM)**: preferred when the facade must also handle authentication, rate limiting, or multiple downstream systems.
- **Nginx / Azure Front Door**: valid for simple HTTP routing; lacks .NET-native integration.

YARP minimal setup:

```csharp
// Program.cs (.NET 8/9)
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

var app = builder.Build();
app.MapReverseProxy();
app.Run();
```

```json
// appsettings.json (route legacy by default)
{
  "ReverseProxy": {
    "Routes": {
      "legacy-catchall": {
        "ClusterId": "legacy",
        "Match": { "Path": "{**catch-all}" }
      }
    },
    "Clusters": {
      "legacy": {
        "Destinations": {
          "legacy-app": { "Address": "https://legacy-host/" }
        }
      }
    }
  }
}
```

### Phase 2: Identify the strangler boundary

Choose the first component to migrate. Selection criteria:

- **Low risk, high value**: a bounded context that is well-understood and frequently changed.
- **Minimal cross-cutting dependencies**: avoid components that share in-process state with many others.
- **Well-defined API surface**: endpoints with clear request/response contracts are easier to route.

Typical first candidates: authentication/login flow, a single API controller group, a reporting module.

### Phase 3: Implement the new service

Build the replacement component in .NET 8/9. Delegate the target-state design to `/dotnet-architect`. The new service must:

- Expose the same contract (URL paths, response shape) as the legacy equivalent so the facade routes transparently.
- Pass the characterization tests that cover the legacy component's behaviour.
- Not share the legacy database directly: use a migration adapter or dual-write if schema ownership is contested.

### Phase 4: Incremental traffic routing

Update the facade to route specific paths to the new service. Validate:

1. Canary traffic (1-5%) to the new service, remainder to legacy.
2. Compare response parity (use a shadow-mode proxy or traffic replay).
3. Ramp up to 100% once parity is confirmed.

```json
// appsettings.json (route /api/orders to new service)
{
  "ReverseProxy": {
    "Routes": {
      "new-orders": {
        "ClusterId": "orders-v2",
        "Match": { "Path": "/api/orders/{**catch-all}" }
      },
      "legacy-catchall": {
        "ClusterId": "legacy",
        "Match": { "Path": "{**catch-all}" }
      }
    },
    "Clusters": {
      "orders-v2": {
        "Destinations": {
          "orders-new": { "Address": "https://orders-service/" }
        }
      },
      "legacy": {
        "Destinations": {
          "legacy-app": { "Address": "https://legacy-host/" }
        }
      }
    }
  }
}
```

### Phase 5: Retire the legacy component

Once the new service carries 100% of traffic for a component and monitoring confirms parity:

1. Remove the legacy code for that component (do not leave dead code).
2. Update the facade to remove the legacy route for that path.
3. Update characterization tests to target the new service directly.
4. Repeat Phase 2-5 for the next component.

### Phase 6: Decommission the facade

When all components are migrated and no traffic routes to the legacy app:

1. Update DNS / load balancer to point directly to the new services.
2. Remove the YARP facade.
3. Decommission the legacy app and its infrastructure.

---

## Database Migration During Strangler Fig

The database is frequently the hardest part. Options in order of preference:

1. **New schema, new database**: the new service owns its own schema/database. A dual-write adapter synchronises writes to legacy during the transition window.
2. **Shared database, separate schema**: new service uses a new schema on the same server; legacy and new share via views or stored procedures during transition.
3. **Shared schema**: highest risk; requires careful change compatibility. Avoid if possible.

---

## References

- Azure Architecture Patterns, Strangler Fig: https://learn.microsoft.com/azure/architecture/patterns/strangler-fig
- YARP documentation: https://microsoft.github.io/reverse-proxy/
- Modern Web App pattern (.NET): https://learn.microsoft.com/azure/architecture/web-apps/guides/enterprise-app-patterns/modern-web-app/dotnet/guidance
