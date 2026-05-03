# Microsoft Graph SDK: JavaScript / TypeScript

`@microsoft/microsoft-graph-client` (v3+) is the JavaScript SDK. Pair with `@azure/msal-browser` for SPA scenarios, `@azure/msal-node` for Node.js server-side (or `@azure/identity` for Azure-hosted Node), and `@microsoft/microsoft-graph-types` for type definitions. Microsoft Graph SDK > raw `fetch`, except for batch beyond SDK support.

---

## Package layout

| Package | Purpose |
|---|---|
| `@microsoft/microsoft-graph-client` | Graph SDK client, middleware chain, batch helpers |
| `@microsoft/microsoft-graph-types` | TypeScript definitions for v1.0 resources |
| `@microsoft/microsoft-graph-types-beta` | TypeScript definitions for beta. ADR required to use in production |
| `@azure/msal-browser` | Browser SPA token acquisition |
| `@azure/msal-node` | Node.js token acquisition (web app, daemon, OBO) |
| `@azure/identity` | Token credentials (preferred for Azure-hosted Node, includes Workload Identity) |

The Microsoft Graph Toolkit (`@microsoft/mgt-*`) is deprecated: retirement begins September 2025, full retirement August 2026. New web UIs should use the SDK directly or other supported components.

---

## Picking a credential

| Caller | Library | Pattern |
|---|---|---|
| Azure-hosted Node app, MI | `@azure/identity` | `DefaultAzureCredential` or `ManagedIdentityCredential` |
| GitHub Actions / outside Azure | `@azure/identity` | `WorkloadIdentityCredential` |
| Node web app, user context | `@azure/msal-node` | `ConfidentialClientApplication` with auth code or OBO |
| Daemon with cert (last resort) | `@azure/msal-node` or `@azure/identity` | `ClientCertificateCredential` |
| Browser SPA | `@azure/msal-browser` | `PublicClientApplication`, redirect or popup flow |
| Local dev | `@azure/identity` | `AzureCliCredential` chained via `DefaultAzureCredential` |

---

## Browser SPA + SDK

```typescript
import { PublicClientApplication, InteractionType } from "@azure/msal-browser";
import { Client } from "@microsoft/microsoft-graph-client";
import { AuthCodeMSALBrowserAuthenticationProvider } from "@microsoft/microsoft-graph-client/authProviders/authCodeMsalBrowser";

const msal = new PublicClientApplication({
  auth: {
    clientId: import.meta.env.VITE_CLIENT_ID,
    authority: `https://login.microsoftonline.com/${import.meta.env.VITE_TENANT_ID}`,
    redirectUri: window.location.origin
  },
  cache: { cacheLocation: "sessionStorage" }
});

await msal.initialize();

const account = msal.getAllAccounts()[0];
const authProvider = new AuthCodeMSALBrowserAuthenticationProvider(msal, {
  account,
  scopes: ["User.Read", "Mail.Read"],
  interactionType: InteractionType.Redirect
});

const client = Client.initWithMiddleware({ authProvider });
const me = await client.api("/me").select(["id", "displayName", "mail"]).get();
```

Scopes are delegated and incremental: do not request the full set on first sign-in. Stage consent as features unlock.

---

## Server-side Node + Azure.Identity

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { Client } from "@microsoft/microsoft-graph-client";
import { TokenCredentialAuthenticationProvider } from "@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials";
import "isomorphic-fetch";

const credential = new DefaultAzureCredential();
const authProvider = new TokenCredentialAuthenticationProvider(credential, {
  scopes: ["https://graph.microsoft.com/.default"]
});

const client = Client.initWithMiddleware({ authProvider });
const users = await client
  .api("/users")
  .select("id,displayName,mail")
  .top(100)
  .get();
```

`/.default` returns the union of pre-authorized application permissions: do not list scopes per call for daemons.

---

## Page iteration

```typescript
import { PageIterator, PageIteratorCallback } from "@microsoft/microsoft-graph-client";

const response = await client.api("/users").select("id,displayName,mail").top(100).get();

const callback: PageIteratorCallback = (user) => {
  // process; return false to stop
  console.log(`${user.displayName} <${user.mail}>`);
  return true;
};

const iterator = new PageIterator(client, response, callback);
await iterator.iterate();
```

The iterator chases `@odata.nextLink`, applies retry-on-429, and respects the callback's stop signal.

---

## Batching

```typescript
const batchPayload = {
  requests: [
    { id: "1", method: "GET", url: "/me" },
    { id: "2", method: "GET", url: "/me/calendarView?startDateTime=2026-05-03T00:00:00Z&endDateTime=2026-05-04T00:00:00Z&$select=subject,start,end" },
    { id: "3", method: "GET", url: "/me/messages?$top=10&$select=subject,from,receivedDateTime" }
  ]
};

const response = await client.api("/$batch").post(batchPayload);

for (const r of response.responses) {
  if (r.status === 429) {
    // surface r.headers["Retry-After"]
    continue;
  }
  if (r.status >= 400) {
    // log r.body.error
    continue;
  }
  // r.body is the entity
}
```

The SDK does not auto-split batches in JS as of v3.x: cap your batch at 20 entries per `$batch` POST.

---

## React hooks pattern

For React apps using MSAL.js, lift the SDK client into a context and expose a hook:

```typescript
// graphContext.tsx
import { createContext, useContext, useMemo, ReactNode } from "react";
import { useMsal } from "@azure/msal-react";
import { Client } from "@microsoft/microsoft-graph-client";
import { AuthCodeMSALBrowserAuthenticationProvider } from "@microsoft/microsoft-graph-client/authProviders/authCodeMsalBrowser";
import { InteractionType } from "@azure/msal-browser";

const GraphCtx = createContext<Client | null>(null);

export function GraphProvider({ children, scopes }: { children: ReactNode; scopes: string[] }) {
  const { instance, accounts } = useMsal();

  const client = useMemo(() => {
    if (accounts.length === 0) return null;
    const provider = new AuthCodeMSALBrowserAuthenticationProvider(instance, {
      account: accounts[0],
      scopes,
      interactionType: InteractionType.Redirect
    });
    return Client.initWithMiddleware({ authProvider: provider });
  }, [instance, accounts, scopes]);

  return <GraphCtx.Provider value={client}>{children}</GraphCtx.Provider>;
}

export function useGraphClient(): Client {
  const c = useContext(GraphCtx);
  if (!c) throw new Error("useGraphClient outside GraphProvider or before sign-in");
  return c;
}
```

Then in components:

```typescript
function MailList() {
  const graph = useGraphClient();
  const [items, setItems] = useState<Message[]>([]);

  useEffect(() => {
    graph.api("/me/messages")
      .select("subject,from,receivedDateTime")
      .top(25)
      .get()
      .then(r => setItems(r.value));
  }, [graph]);

  // render
}
```

Pair with TanStack Query (`@tanstack/react-query`) for caching, retries, and stale-while-revalidate semantics on top of Graph reads.

---

## Retry middleware

The SDK ships `RetryHandler` middleware that honours `Retry-After`. Tune via `RetryHandlerOptions`:

```typescript
import { Client, RetryHandlerOptions } from "@microsoft/microsoft-graph-client";

const client = Client.initWithMiddleware({
  authProvider,
  middlewareOptions: [new RetryHandlerOptions(undefined /* delay sec */, 5 /* max retries */)]
});
```

---

## Beta endpoint

```typescript
const beta = await client.api("/beta/me/insights/used").get();
// or
const betaClient = Client.initWithMiddleware({
  authProvider,
  baseUrl: "https://graph.microsoft.com/beta"
});
```

ADR required before shipping beta to production: see `beta-vs-v1-policy.md`.

---

## Trade-offs and exceptions

- **Bundle size**: `@microsoft/microsoft-graph-client` is fine; the types packages add no runtime bytes. Audit MSAL.js bundle if you only need a tiny scope.
- **Toolkit deprecation**: `@microsoft/mgt-*` is retiring (begins September 2025, full August 2026). New code uses the SDK directly. Migrate existing Toolkit components on a known timeline.
- **Manual batch splitting**: JS SDK does not auto-split batches >20. Page caller-side and call `$batch` in chunks of 20.
- **`isomorphic-fetch` polyfill**: required for Node <18 environments. Node 18+ has global `fetch`.
- **Raw `fetch` callers**: do not skip retry. If you must use `fetch`, implement the policy from `throttling-and-retry.md` exactly.
