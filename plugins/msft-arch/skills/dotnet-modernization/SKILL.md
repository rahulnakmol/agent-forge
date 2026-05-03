---
name: dotnet-modernization
description: >-
  .NET Framework to .NET 8/9 LTS migration specialist. TRIGGER when: user
  mentions legacy .NET Framework 4.x, ASP.NET (non-Core), WCF services,
  EF6, ASP.NET Web Forms, "modernize", "upgrade", or ".NET Framework";
  or when discover outputs an engagement classified as Modernization with
  a .NET Framework stack. Codifies migration strategy: strangler fig over
  big bang for any non-trivial codebase (greater than 50K LOC), .NET Upgrade
  Assistant (now superseded by GitHub Copilot modernization agent in VS 2026)
  for assessment phase, WCF to gRPC (internal) or HTTP+OpenAPI (external),
  EF6 to EF Core with explicit review of LINQ queries and lazy loading,
  Web Forms to Blazor Server (preferred), Windows Container as last resort
  when full migration is not viable for 12-18 months.
  DO NOT TRIGGER for greenfield .NET 8/9 work (use dotnet-architect), Azure
  infrastructure sizing (use azure-architect), or containerization strategy
  for already-modern apps (use container-architect).
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - microsoft_docs_search
  - microsoft_docs_fetch
  - microsoft_code_sample_search
---

# .NET Modernization Specialist

**Version**: 1.0 | **Role**: .NET Framework to .NET 8/9 LTS Migration Architect | **Stack**: Migration, Strangler Fig, WCF, EF6, Web Forms, Windows Containers

This skill owns the migration path from .NET Framework 4.x to .NET 8/9 LTS. It covers strategy selection (strangler fig vs. big bang), assessment tooling, component-by-component migration patterns (WCF, EF6, Web Forms), containerization fallbacks, and the test-coverage prerequisite. It does NOT redesign the target-state .NET architecture: that belongs to `/dotnet-architect`. Chain to `/dotnet-architect` immediately after the migration plan is complete to design the new world.

Use `microsoft_docs_search` and `microsoft_docs_fetch` to verify current .NET Upgrade Assistant status, GitHub Copilot modernization agent capabilities, and .NET 9 migration guidance before finalising decisions. Use `microsoft_code_sample_search` for gRPC and EF Core sample patterns. Read shared standards: `standards/references/coding-stack/csharp-standards.md`, `standards/references/coding-stack/ef-core-checklist.md`.

## Migration Principles (non-negotiable)

- **Strangler fig over big bang for any non-trivial codebase (greater than 50K LOC).** Big bang is reserved for small, well-tested, low-dependency codebases under active development where a feature freeze is acceptable for the migration window.
- **.NET Upgrade Assistant for assessment phase; manual fixes for the long tail.** As of VS 2026 / VS 2022 17.14+, the GitHub Copilot modernization agent replaces the legacy Upgrade Assistant; use whichever tooling matches the customer's VS version, and expect 40-60% automated coverage: the remainder requires human judgment.
- **WCF to gRPC for new internal services; HTTP+OpenAPI for external/integration.** CoreWCF is a compatibility bridge, not a destination: use it only when binary-compatible client contracts are a hard constraint during a transition window.
- **EF6 to EF Core: migration is not always 1:1: review LINQ queries, lazy loading, transaction scopes.** EF Core disables lazy loading by default, eliminates EntitySQL, changes change-tracker semantics, and removes EDMX. Each difference is a potential regression.
- **ASP.NET Web Forms to Blazor Server (closest paradigm match), then MVC, then Razor Pages.** Blazor Server preserves the stateful, event-driven component model that Web Forms developers know; choose MVC or Razor Pages only when server-push latency is a concern or the team already has strong MVC investment.
- **Windows Container as last resort when full migration is not viable for the next 12-18 months.** Windows Containers on Windows Server Core lift .NET Framework 4.x apps into a container without code changes; they buy time but do not eliminate the migration debt.
- **Test coverage on legacy code first: modernization without tests is rewriting blind.** Establish a characterization test suite against the legacy app before touching a single project file. See `references/test-coverage-first.md`.

## Assessment Decision Tree

```
Legacy .NET Framework codebase detected
        |
        v
[1] Run assessment tooling (Upgrade Assistant / Copilot modernization agent)
        |
        +-- API compatibility score >= 90%?
        |        YES --> In-place upgrade viable; consider side-by-side new-TFM project
        |        NO  --> Strangler fig required
        |
[2] LOC > 50K?
        YES --> Strangler fig (mandatory)
        NO  --> Big bang viable IF: tests exist, team size <= 5, no active WCF contracts
        |
[3] WCF services present?
        YES --> Identify internal vs. external consumers
        |        Internal: gRPC (see references/wcf-to-grpc.md)
        |        External: HTTP+OpenAPI or CoreWCF bridge
        NO  --> Continue
        |
[4] EF6 present?
        YES --> EF6-to-EF Core analysis (see references/ef6-to-efcore.md)
        NO  --> Continue
        |
[5] ASP.NET Web Forms present?
        YES --> Blazor Server first (see references/webforms-to-blazor.md)
        NO  --> Continue
        |
[6] Full migration NOT viable in 12-18 months?
        YES --> Windows Container fallback (see references/windows-container-fallback.md)
        NO  --> Proceed with migration plan
```

## Design Process

### Step 1: Load Context + Discovery Brief

Read the discovery brief from `/discover`. Confirm:
- Current .NET Framework version (`net4x` TFM, e.g., `net472`, `net48`)
- Total LOC (estimate if unmeasured: count `.cs` + `.aspx` + `.asmx` files)
- WCF endpoints present? (check `.svc` files, `web.config` `<system.serviceModel>`)
- EF6 present? (check NuGet `EntityFramework >= 6.x`)
- Web Forms present? (`.aspx`, `.ascx`, code-behind files)
- External integrations and client contracts (breaks during migration)
- Active vs. maintenance-mode codebase (affects big-bang viability)
- Current test coverage percentage

Load `references/test-coverage-first.md` before proceeding to step 2.

### Step 2: Verify with Microsoft Learn MCP

Use `microsoft_docs_search` to confirm:
- Current status of GitHub Copilot modernization agent vs. legacy Upgrade Assistant
- .NET 9 LTS migration notes for any framework in scope
- CoreWCF feature support matrix (if customer requires WCF bridge)

Use `microsoft_code_sample_search` for:
- gRPC service definition patterns (Protobuf + `Grpc.AspNetCore`)
- EF Core `DbContext` registration replacing EF6 patterns

### Step 3: Produce Migration Strategy

Produce:
- **Strategy selection**: strangler fig or big bang, with explicit rationale
- **Migration phases**: ordered list of components with sequence (dependencies first)
- **Component-by-component plan**: WCF, EF6, Web Forms each have a dedicated reference; link and summarise decisions
- **Containerization path**: Linux container (preferred) or Windows Container fallback with criteria
- **Test-coverage gate**: characterization test suite requirement before code changes begin
- **Tooling recommendation**: GitHub Copilot modernization agent (VS 2026 / VS 2022 17.14+) or legacy Upgrade Assistant; CLI fallback via `dotnet tool install -g upgrade-assistant`
- **Handoff decision**: when the migration plan is complete, chain immediately to `/dotnet-architect` to design the target-state .NET 8/9 implementation

Strangler fig phases follow this canonical sequence:
1. Introduce reverse proxy / facade (YARP or Azure APIM in front of legacy)
2. Identify the strangler boundary (bounded context or API surface)
3. Implement new service in .NET 8/9 (delegating to `/dotnet-architect`)
4. Route traffic incrementally to new service; validate parity
5. Retire legacy component; repeat per bounded context
6. Decommission facade once last component migrated

### Step 4: Validate

Run the validation checklist before handoff.

## Validation

| Check | Pass Criteria |
|-------|--------------|
| Strategy rationale | Big bang only for < 50K LOC + tests + no active WCF contracts; strangler fig otherwise |
| Test-coverage gate | Characterization test suite exists or is committed to before any migration work starts |
| WCF decision | Internal: gRPC target defined. External: HTTP+OpenAPI or CoreWCF bridge with exit date |
| EF6 migration | LINQ query review, lazy loading audit, transaction scope analysis documented |
| Web Forms decision | Blazor Server (default), MVC, or Razor Pages with explicit rationale |
| Container path | Linux container targeted; Windows Container only if full migration not viable < 18 months |
| Tooling version | Correct tool identified (Copilot modernization agent vs. legacy Upgrade Assistant) |
| Target framework | `net8.0` or `net9.0`; no `net4x` targets in the new project |
| Handoff ready | `/dotnet-architect` brief prepared for target-state design |
| Azure hosting | `/azure-architect` flagged for hosting + WAF validation |

## Handoff Protocol

```markdown
## Handoff: dotnet-modernization -> dotnet-architect
### Decisions Made
- Strategy: [strangler fig (phases: N) / big bang]; rationale: [LOC, test coverage, WCF contracts]
- WCF: [gRPC (internal) / HTTP+OpenAPI (external) / CoreWCF bridge (transition only)]
- EF6: [EF Core 8/9]; LINQ changes: [list]; lazy loading: [disabled, explicit loading adopted]; transactions: [execution strategy]
- Web Forms: [Blazor Server / MVC / Razor Pages]; rationale: [...]
- Container path: [Linux container on .NET 8/9 / Windows Container fallback (exit date: MM/YYYY)]
- Test coverage: [characterization suite status]
### Artifacts: Migration strategy doc | Phase sequence | Component risk register | Container path decision
### Open Questions: [items for dotnet-architect (target-state design), azure-architect (hosting), iac-architect (deployment)]

## Handoff: discover -> dotnet-modernization (incoming contract)
### Trigger conditions
- Engagement type: Modernization
- Stack signals: "legacy", "modernize", ".NET Framework", "WCF", "Web Forms", "EF6"
### Context expected from discover
- Current .NET Framework version, LOC estimate, WCF/EF6/Web Forms presence, test coverage, active client contracts
```

## Sibling Skills

- `/discover`: Predecessor. Chain FROM discover when "legacy", "modernize", or ".NET Framework" is detected in discovery output.
- `/dotnet-architect`: Target-state design (C# patterns, ASP.NET Core, EF Core, Aspire, Blazor). Chain TO dotnet-architect immediately after the migration plan is complete to design the new world. Do not duplicate target-state patterns here.
- `/azure-architect`: Target hosting topology, WAF validation, service selection for the migrated workload.
- `/iac-architect`: Terraform/AVM infrastructure for the target deployment.
- `/agent`: Pipeline orchestrator for cross-stack engagements.
