Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Strategy Selection Rationale** — Applies the correct migration strategy: strangler fig for any non-trivial codebase (>50K LOC) or low test coverage; big bang only for small (<50K LOC) + well-tested + no active WCF contracts. Documents the rationale explicitly. Score 5 if strategy is correctly selected with clear rationale; 1 if big bang is recommended for a large codebase or the decision is unjustified.

2. **WCF Migration Pattern** — Recommends gRPC for internal WCF services (not CoreWCF as destination) and HTTP+OpenAPI for external-facing. CoreWCF is only a compatibility bridge during transition. Score 5 if WCF migration pattern is correct for the stated scenario; 1 if CoreWCF is recommended as a destination or gRPC is recommended for external consumers.

3. **EF6 Migration Risk Coverage** — Explicitly addresses the EF6-to-EF Core differences: lazy loading disabled by default, EntitySQL eliminated, EDMX removed, change-tracker semantics changed. Does not treat the migration as a simple package swap. Score 5 if key breaking changes are identified and addressed; 1 if migration is described as straightforward without flagging breaking changes.

4. **Web Forms Migration Approach** — Recommends Blazor Server as the primary target for Web Forms migration (closest paradigm match for stateful event-driven components). MVC or Razor Pages only with explicit rationale. Score 5 if Blazor Server is recommended as the default with clear rationale; 1 if MVC is recommended without justification.

5. **Test Coverage Gate** — Requires establishing a characterization test suite on the legacy app before any code changes begin. Treats migration without tests as migration without safety. Score 5 if test coverage gate is explicitly required before migration work; 1 if migration proceeds without addressing test coverage.
