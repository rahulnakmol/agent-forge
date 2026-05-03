# Microsoft Learn MCP: Usage Patterns

The Microsoft Learn MCP server exposes three tools that provide structured access to official Microsoft and Azure documentation. Used well, they ground every recommendation in current first-party content. Used poorly, they add latency without improving accuracy. This guide explains when and how to use each tool.

---

## The Three Tools

### `microsoft_docs_search`

**What it does**: Sends a query against the Microsoft Learn corpus and returns up to 10 content chunks (max 500 tokens each), each with a title, URL, and excerpt.

**When to use**:
- You need a quick factual confirmation: "Is this API still the recommended approach?"
- You want to identify which documentation page covers a topic before fetching the full page.
- The user asks about a product, service, SDK, or feature and you want to verify your training knowledge is current.
- You need to confirm version-specific behavior (e.g., "does EF Core 9 support this query pattern?").

**When NOT to use**:
- The question is about general programming concepts, not Microsoft-specific products.
- You already have a high-confidence answer grounded in a previous search in the same session.
- The query is about business logic, architecture trade-offs, or strategic decisions; those are not answered by documentation search.

**Query patterns that work well**:

```text
# Specific, product-qualified, version-qualified
"EF Core 9 complex types ExecuteUpdate"
"Azure Managed Identity system-assigned AKS workload identity"
".NET 9 primary constructors C# 13 features"
"Azure AI Content Safety prompt shield configuration"

# Feature comparison
"Entra External ID vs Azure AD B2C when to use"
"Service Bus vs Event Hubs Azure messaging comparison"

# Checklist / best practice queries
"Azure App Service security best practices checklist"
"Azure Container Apps environment variables secrets"
```

**Query patterns that return poor results**:

```text
# Too vague: returns generic overview pages
"Azure security"
"how to use .NET"

# Too implementation-specific: docs don't cover custom code patterns
"how to write a retry loop in C#"

# Not a Microsoft topic
"REST API design principles"
```

---

### `microsoft_docs_fetch`

**What it does**: Fetches and converts a full Microsoft documentation page to markdown, preserving headings, code blocks, tables, and links.

**When to use**:
- `microsoft_docs_search` returned a highly relevant URL and you need the complete content (full tutorial steps, all configuration options, complete API reference).
- The search excerpt is truncated and the critical detail is likely in the missing portion.
- You need a complete code sample that the excerpt cut off.
- Verifying prerequisites or a migration guide where partial information could be misleading.

**When NOT to use**:
- The search result already answered the question; fetching adds latency without value.
- The URL is a landing page (e.g., `learn.microsoft.com/azure/`) rather than a specific document page; landing pages contain navigation, not content.
- The page is a PDF, image, or binary; the tool only handles HTML documentation pages.

**Workflow**:

```text
Step 1: microsoft_docs_search → "EF Core 9 compiled queries"
Step 2: Identify the most relevant URL from the results
Step 3: microsoft_docs_fetch → fetch that URL for the full EF Core 9 what's-new page
Step 4: Extract the specific compiled query section
```

---

### `microsoft_code_sample_search`

**What it does**: Searches for code snippets and examples in official Microsoft Learn documentation, returning up to 20 results with code and context.

**When to use**:
- You need a concrete implementation example, not just prose explanation.
- The user asks "show me how to configure X" or "what does a Y look like in code."
- You want to verify API usage (method signatures, parameter names, required using directives).

**Optional `language` parameter**: Filter by `csharp`, `python`, `typescript`, `bicep`, `powershell`, etc. Use it when you know the target language to improve result relevance.

**When NOT to use**:
- Conceptual questions that do not need code.
- The code pattern is so standard that official docs are unlikely to have a specific example (e.g., "write a for loop").

---

## Verification Workflow: When to Verify Before Recommending

Always verify via Microsoft Learn MCP when recommending:

1. **A specific Azure service feature** that may have changed behavior, pricing tier, or availability since training cutoff.
2. **An API method or parameter** that has been modified or deprecated (e.g., Azure SDK for .NET v12 vs v11).
3. **A Microsoft Identity platform URL, endpoint, or flow**: these change with product rebranding (Azure AD → Entra ID).
4. **EF Core / ASP.NET Core version-specific behavior**: EF Core 9 has different defaults from EF Core 8 in several areas.
5. **Azure pricing tiers and SKUs**: capabilities vary by tier and change with product updates.

Do not verify when:
- The recommendation is a general software engineering principle that happens to use Microsoft tools.
- You already verified the same fact earlier in the same session.
- The user is asking for a code review, refactor, or opinion; documentation search adds no value there.

---

## Pairing with Context7 MCP

The Microsoft Learn MCP covers Microsoft's own documentation. For SDK-level documentation (NuGet package APIs, third-party library integration, OpenAPI specifications), pair with **Context7 MCP** (Use `mcp__claude_ai_Context7__resolve-library-id` first to get the canonical library ID, then call `mcp__claude_ai_Context7__query-docs` with that ID):

| Need | Tool |
|---|---|
| "How does Azure Service Bus SDK v7 configure sessions?" | Microsoft Learn MCP → `microsoft_code_sample_search` |
| "What are all the overloads on `ServiceBusProcessor`?" | Context7 MCP → resolve library, then query docs |
| "What does the Polly v8 `ResiliencePipeline` API look like?" | Context7 MCP |
| "What retry policy does Azure recommends for Cosmos DB?" | Microsoft Learn MCP → `microsoft_docs_search` |

---

## Failure Modes to Watch For

**Stale documentation**: Microsoft Learn content is updated frequently, but the MCP cache may lag. For anything released in the last 30–60 days, treat search results as indicative, not authoritative. Check the article's "Article reviewed" date at the bottom.

**Partial coverage**: Not all Microsoft products have equally deep documentation. Azure Arc, Azure Operator Nexus, and newer AI services may have sparse coverage. If three searches return nothing relevant, state this clearly rather than hallucinating content.

**Renamed products**: Many Microsoft services were renamed in 2023–2024 (Azure Active Directory → Microsoft Entra ID; Azure Communication Services → Azure Communication Services, still the same; Azure Purview → Microsoft Purview). Queries using old names may return redirected or partial results. Use both old and new names in your query.

**Feature flag / preview gaps**: GA documentation may not reflect private-preview features. If a user asks about a preview feature, note that documentation coverage is incomplete and recommend checking the product's GitHub issues and release notes.

**Region availability gaps**: Docs sometimes describe features without clearly marking regional availability. Always verify GA region support in the Azure Products by Region page when recommending a new service.

---

## Trade-offs and Exceptions

- **Latency**: Each MCP call adds ~1–3 seconds. For time-sensitive interactions, limit to one search + one optional fetch. For deep research tasks, multiple calls are appropriate.
- **Context window**: Each search result consumes tokens. If you are already operating near the context limit, summarize search results rather than including them verbatim.
- **Conflicting results**: If two search results give contradictory guidance, fetch both full pages and compare dates. The more recently updated page is authoritative.
- **Non-English queries**: The search tool works best with English queries. If the user is communicating in another language, translate the technical query to English for the search, then respond in the user's language.
