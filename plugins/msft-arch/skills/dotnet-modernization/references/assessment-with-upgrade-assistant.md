# Assessment with .NET Upgrade Assistant (and GitHub Copilot Modernization Agent)

**Applies to**: .NET Framework 4.x projects targeted for migration to .NET 8/9 LTS.

> As of Visual Studio 2026 and VS 2022 17.14+, the **GitHub Copilot modernization agent** is the recommended tool. The legacy Upgrade Assistant is deprecated but still available via opt-in (`Tools > Options > Projects and Solutions > Modernization > Enable legacy Upgrade Assistant`). Use the Copilot agent when the customer's VS version supports it; use the legacy tool or CLI for older environments.

---

## Tool Selection

| Customer VS version | Recommended tool |
|---|---|
| VS 2026 or VS 2022 17.14+ | GitHub Copilot modernization agent (built-in) |
| VS 2022 < 17.14 | Legacy .NET Upgrade Assistant (VS extension) |
| No Visual Studio / CI | `upgrade-assistant` .NET Global Tool (CLI) |

Install the CLI tool:

```dotnetcli
dotnet tool install -g upgrade-assistant
```

Note: if extra NuGet feed sources are configured, add `--ignore-failed-sources` to suppress feed errors.

---

## Assessment Workflow

### Phase 1: Analyse (before touching code)

1. Back up or branch the repository.
2. Run analysis to generate a compatibility report.

**Visual Studio (Copilot modernization agent):**
Open the project, invoke the agent from the chat pane. It produces a step-by-step migration plan with automated code fixes and commits per change.

**Visual Studio (legacy Upgrade Assistant):**
Right-click the project in Solution Explorer, select **Upgrade**, then choose **Analyze project**. The report lists each incompatible API, missing NuGet package, and configuration file issue.

**CLI:**
```dotnetcli
upgrade-assistant analyze <solution>.sln
```

### Phase 2: Review the Report

Key areas to audit manually regardless of tool:

- **API compatibility score**: anything below 90% signals a significant manual effort tail.
- **NuGet packages**: packages targeting `net4x` only must be replaced or removed. Check for .NET 8/9 equivalents.
- **WCF references**: `System.ServiceModel` is a hard incompatibility for server-side hosting (client-only `System.ServiceModel.Http` exists in .NET). Flag for the WCF migration path.
- **EF6 references**: `EntityFramework 6.x` does not port directly; review `references/ef6-to-efcore.md`.
- **Web Forms references**: `System.Web` is not available on .NET 8/9. Flag for the Web Forms migration path.
- **Global.asax / HttpModules / HttpHandlers**: replace with ASP.NET Core middleware.
- **`packages.config`**: migrate to `PackageReference` format before upgrading the TFM.
- **`web.config` / `app.config`**: replace with `appsettings.json` + `IConfiguration`.

### Phase 3: Upgrade (incremental or in-place)

Upgrade projects in dependency order: upgrade leaf libraries before the main application project.

**In-place upgrade (single project):**
1. Right-click project > Upgrade > In-place project upgrade.
2. Select target framework: `.NET 8.0` or `.NET 9.0`.
3. Select all components, click **Upgrade selection**.
4. Review results: green = upgraded, warning = manual review needed.

**CLI in-place:**
```dotnetcli
upgrade-assistant upgrade <project>.csproj --target-tfm-support LTS
```

### Phase 4: Address the Long Tail

The tool automates 40-60% of common porting tasks. Manual attention is required for:

- Custom HTTP modules replaced by ASP.NET Core middleware
- Session state (in-proc to distributed: Redis or Azure Cache for Redis)
- `System.Web.Security` replaced by ASP.NET Core Identity or Entra ID
- `AppDomain`, `Thread.CurrentPrincipal`, `ConfigurationManager`: each has a .NET 8/9 equivalent
- `System.Drawing` (GDI+): replace with `SkiaSharp` or `ImageSharp` for cross-platform support
- P/Invoke dependencies on Windows-only native DLLs: assess whether Windows Container is required

---

## Output Artefacts

After assessment, produce:
- **Compatibility report** (from tool output)
- **Manual fix register**: each hard incompatibility, owner, and estimated effort
- **Migration phase plan**: ordered list of components with sequence and dependency graph
- **Tooling recommendation**: which tool per VS version, with CLI fallback

---

## References

- GitHub Copilot modernization agent: https://learn.microsoft.com/dotnet/core/porting/github-copilot-app-modernization/overview
- Legacy Upgrade Assistant overview: https://learn.microsoft.com/dotnet/core/porting/upgrade-assistant-overview
- Porting from .NET Framework to .NET: https://learn.microsoft.com/dotnet/core/porting/
