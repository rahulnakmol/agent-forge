Score the output 1-5 on each criterion. Return the AVERAGE.

1. **LTS Framework Targeting** — Recommends net8.0 or net9.0 with explicit LangVersion pinning and Nullable enabled. Never recommends .NET Framework or netstandard for greenfield work. Score 5 if LTS targeting is correctly specified; 1 if older framework or netstandard is recommended.

2. **API Surface Preference** — Applies the Minimal APIs > Web API > MVC preference for new work. Recommends Minimal API with route groups for new microservices; Web API only for large existing codebases. Blazor Server preferred over WASM for internal/low-user-count apps. Score 5 if API surface preference is correctly applied; 1 if MVC is recommended without justification for new work.

3. **Result-T Error Handling** — Recommends Result<T> or OneOf<T,E> for control flow instead of exceptions. Exceptions reserved for truly exceptional, unrecoverable conditions. No try/catch for business logic like not-found or validation failures. Score 5 if Result<T> pattern is correctly recommended; 1 if exceptions are recommended for business logic branches.

4. **EF Core and Data Access Best Practices** — Recommends AsNoTracking() for read-only queries, compiled queries for hot paths, and async hygiene (no .Result/.Wait()). Constructor injection only; no service locator. Score 5 if EF Core best practices are correctly applied; 1 if tracked queries are recommended for reads or .Result/.Wait() is used.

5. **Managed Identity for Azure Resources** — Recommends DefaultAzureCredential / Managed Identity for all Azure resource access. No connection strings or service principal secrets inline in source or appsettings. Score 5 if Managed Identity is correctly recommended; 1 if connection strings or secrets are recommended for Azure service access.
