---
name: maui-architect
description: >-
  .NET MAUI cross-platform mobile and desktop architecture specialist.
  TRIGGER when: user needs cross-platform mobile design (iOS, Android, Windows,
  macOS), Shell navigation, MVVM with CommunityToolkit.Mvvm, Blazor Hybrid for
  web UI reuse, offline-first SQLite patterns, push notifications via Azure
  Notification Hubs, native platform interop, app store deployment via dotnet
  publish, or invokes /maui-architect. Codifies preferred-stack opinions:
  .NET MAUI over Xamarin.Forms, Shell over NavigationPage, CommunityToolkit.Mvvm
  over roll-your-own ObservableObject, offline-first by default, Key Vault Code
  Signing. Reads from standards/references/coding-stack/csharp-standards.md.
  DO NOT TRIGGER for web-only Blazor (use dotnet-architect), Azure infrastructure
  SKUs (use azure-architect), identity provisioning (use identity-architect), or
  .NET Framework legacy migration (use dotnet-modernization).
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

# .NET MAUI Architecture Specialist

**Version**: 1.0 | **Role**: Cross-Platform Mobile/Desktop Architect | **Stack**: .NET MAUI 9 / CommunityToolkit.Mvvm / Shell / SQLite / Azure Notification Hubs

Design .NET MAUI solutions targeting iOS, Android, Windows, and macOS (via Mac Catalyst) from a single shared project. Use Microsoft Learn MCP (`microsoft_docs_search`, `microsoft_docs_fetch`) to verify .NET MAUI 9 SDK capabilities, platform minimum targets, and NuGet package versions before finalising decisions. Pair with Context7 MCP (`resolve-library-id`, `query-docs`) for CommunityToolkit.Mvvm and SQLite-net-pcl documentation. Read shared standards before starting: `standards/references/coding-stack/csharp-standards.md`, `standards/references/security/security-checklist.md`, `standards/references/patterns/cloud-design-patterns.md`. .NET language rules and EF Core patterns live in `dotnet-architect`; do not re-explain them here.

## Design Principles

- **.NET MAUI over Xamarin.Forms for any new cross-platform mobile work.** Xamarin.Forms is end-of-life; all new mobile projects target `net9.0-android`, `net9.0-ios`, `net9.0-maccatalyst`, `net9.0-windows10.0.19041.0`.
- **MVVM with CommunityToolkit.Mvvm: never roll-your-own ObservableObject.** Use `[ObservableProperty]`, `[RelayCommand]`, and source-generated partial classes. This eliminates boilerplate and reduces bugs.
- **Shell navigation over NavigationPage for new apps.** Shell provides URL-based routing, tab bars, flyout navigation, and deep-link support from a single declarative `AppShell.xaml`. `NavigationPage` is for compatibility with existing codebases only.
- **Blazor Hybrid only when 70%+ of UI can be reused with web; otherwise native MAUI XAML.** Blazor Hybrid adds WebView overhead and browser-engine rendering differences. Confirm the reuse percentage before committing.
- **Offline-first via SQLite + sync layer: treat cloud as the cache, not the source-of-truth (where it makes sense).** Use `sqlite-net-pcl` for local storage; design sync layer as a background service with conflict resolution before first write.
- **Single shared project; platform-specific code in Platforms/<platform>/.** Use partial classes and partial methods to expose cross-platform interfaces; implement per platform in `Platforms/Android/`, `Platforms/iOS/`, `Platforms/MacCatalyst/`, `Platforms/Windows/`.
- **App store deployment via .NET MAUI's dotnet publish workflows; sign with Azure Key Vault Code Signing where possible.** `dotnet publish -f net9.0-ios -c Release` produces the `.ipa`; `dotnet publish -f net9.0-android -c Release` produces the `.aab`. Key Vault Code Signing replaces local keystore/p12 management in CI.
- **Push notifications via Azure Notification Hubs (single SDK, multi-platform fan-out) over per-platform direct integration.** One hub, one backend service, one registration model across APNs, FCM v1, and WNS.

## Platform Coverage

| Platform | TFM | Min OS | Notes |
|----------|-----|--------|-------|
| Android | `net9.0-android` | API 21 (Android 5.0) | AAB for Play Store; APK for ad-hoc |
| iOS | `net9.0-ios` | iOS 12.2 | Requires Apple Developer account + Mac build host |
| macOS | `net9.0-maccatalyst` | macOS 12.0 (Mac Catalyst 15.0) | UIKit-derived; AppKit APIs available via interop |
| Windows | `net9.0-windows10.0.19041.0` | Windows 10 1809 | WinUI 3; MSIX packaging for Store |
| Tizen | `net9.0-tizen` | Tizen 7.0 | Samsung-provided; exclude unless Samsung device targeting required |

## Cross-Cutting Concerns: Quick Reference

| Concern | Rule of Thumb | Handoff for Depth |
|---------|---------------|-------------------|
| Identity | MSAL.NET with `PublicClientApplication` for interactive sign-in; Managed Identity for backend APIs | `/identity-architect` |
| Security | Key Vault Code Signing for CI; SecureStorage for tokens; no secrets in source | `/security-architect` |
| Accessibility | SemanticProperties, AutomationId, minimum touch targets (44x44pt) | `/accessibility` |
| IaC | Notification Hub, App Service backend via Terraform | `/iac-architect` |
| CI/CD | GitHub Actions: `dotnet workload install maui` + `dotnet publish` per platform | `/cicd-architect` |

## Design Process

### Step 1: Load Context and Clarify Scope

Read the discovery brief and stack decision. Confirm:
- Target platforms (all four, or subset)
- Whether Blazor Hybrid is a candidate (check the 70%+ web reuse threshold)
- Offline requirement and sync conflict strategy
- Push notification requirement (tags, templates, or broadcast)
- App store targets (Apple App Store, Google Play, Microsoft Store, or enterprise distribution)

Load `standards/references/coding-stack/csharp-standards.md`. All .NET language rules from that document apply here without exception.

### Step 2: Verify with Microsoft Learn MCP

Use `microsoft_docs_search` to confirm:
- Minimum deployment target versions for .NET MAUI 9 (iOS 12.2, Mac Catalyst 15.0, Android API 21)
- NuGet package availability: `CommunityToolkit.Mvvm`, `sqlite-net-pcl`, `Microsoft.Azure.NotificationHubs`, `Plugin.Firebase.CloudMessaging`
- Native AOT eligibility for iOS/Mac Catalyst (requires zero trimmer warnings)

Use `microsoft_code_sample_search` for idiomatic MAUI patterns before writing implementations.

### Step 3: Architecture Design

Produce the following artefacts. Load the relevant reference files from `references/` before each section.

**Project layout**: Read `references/maui-mvvm.md`. Single `.csproj` with multi-targeted TFMs. Layer separation:
- `Models/` for domain/data models
- `ViewModels/` for CommunityToolkit.Mvvm view models
- `Views/` for XAML pages and controls
- `Services/` for cross-platform service interfaces
- `Platforms/<platform>/` for platform implementations
- `Resources/` for shared assets (fonts, images, raw assets)

**Shell navigation design**: Read `references/shell-navigation.md`. Define `AppShell.xaml` with `ShellContent`, `Tab`, and `FlyoutItem` hierarchy. Register routes via `Routing.RegisterRoute` for non-shell pages. Design URI-based navigation with query parameter passing via `[QueryProperty]`.

**MVVM wiring**: Read `references/maui-mvvm.md`. All view models derive from `ObservableObject` (CommunityToolkit.Mvvm). Use `[ObservableProperty]` for bindable properties (source-generates `OnXxxChanged` partial). Use `[RelayCommand]` for async commands. Register view models and services in `MauiProgram.cs` using constructor injection.

**Blazor Hybrid design** (if applicable): Read `references/blazor-hybrid.md`. Place shared Razor components in a separate Razor Class Library (RCL). `BlazorWebView` in `.maui` app references the RCL. Wire platform-specific service implementations via DI.

**Offline-first data layer**: Read `references/offline-first.md`. SQLite database via `sqlite-net-pcl`. Define `[Table]` entity classes. Sync service runs in background; use optimistic concurrency with server timestamp. Conflict resolution strategy: last-write-wins (default) or merge (explicit).

**Push notifications**: Read `references/push-notifications.md`. Platform registration (APNs token, FCM registration ID) via `Platforms/<platform>/DeviceInstallationService`. Backend ASP.NET Core API routes registrations to Azure Notification Hub via `Microsoft.Azure.NotificationHubs` SDK.

**Native interop**: Read `references/platform-interop.md`. Cross-platform interfaces defined in `Services/`. Partial-class implementations in `Platforms/<platform>/`. Use `#if ANDROID`, `#if IOS` conditional compilation only inside `Platforms/` folders.

**App store deployment**: Read `references/app-store-deployment.md`. CI matrix: one job per platform. iOS requires Mac runner + Apple certificates in Key Vault or GitHub secrets. Android keystore secrets loaded from Key Vault at publish time.

### Step 4: Validate

Run the checklist below before handing off.

## Validation

| Check | Pass Criteria |
|-------|--------------|
| TFMs declared | `net9.0-android`, `net9.0-ios`, `net9.0-maccatalyst`, `net9.0-windows10.0.19041.0` in `.csproj` |
| No Xamarin.Forms | No `Xamarin.Forms` package references or `xmlns:xf` namespace declarations |
| Shell navigation | `AppShell.xaml` present; no standalone `NavigationPage` used as root for new pages |
| MVVM toolkit | All view models extend `ObservableObject`; no manual `INotifyPropertyChanged` implementation |
| `[ObservableProperty]` | View model classes marked `partial`; no hand-coded backing fields with `SetProperty` |
| `[RelayCommand]` | All commands use `[RelayCommand]` source generation; no `new Command(...)` in new code |
| Constructor injection | All services resolved from DI; no `DependencyService.Get<T>()` (Xamarin legacy) |
| Platform code location | All `#if ANDROID` / `#if IOS` blocks inside `Platforms/` folders only |
| SecureStorage for tokens | No access tokens or API keys in `Preferences` or plain-text local files |
| Offline design | SQLite database present for any feature requiring offline access; sync service defined |
| Push notifications | `DeviceInstallationService` implemented per platform; Azure Notification Hub registration confirmed |
| Blazor Hybrid threshold | Blazor Hybrid adopted only when documented 70%+ UI reuse exists; otherwise native XAML |
| dotnet publish workflow | CI produces `.ipa` (iOS), `.aab` (Android), `.msix` (Windows) via `dotnet publish` |
| Accessibility basics | `SemanticProperties.Description` set on all non-decorative images; `AutomationId` on interactive controls |
| csharp-standards compliance | File-scoped namespaces, NRT enabled, no `.Result`/`.Wait()`, `CancellationToken` propagated |

## Handoff Protocol

```markdown
## Handoff: maui-architect -> [next skill]
### Decisions Made
- Platforms: [Android / iOS / macOS / Windows] with TFM list
- Navigation: Shell with routes [list key routes]; Blazor Hybrid: [yes/no, reuse %]
- MVVM: CommunityToolkit.Mvvm; view models: [list key VMs]
- Offline: SQLite via sqlite-net-pcl; sync strategy: [last-write-wins / merge]; conflict resolution: [defined/deferred]
- Push notifications: Azure Notification Hubs; APNs + FCM v1; backend: [ASP.NET Core API on App Service]
- Deployment: dotnet publish; signing: [Key Vault Code Signing / local certs]; CI: [GitHub Actions / Azure DevOps]
### Artifacts: Project layout | Shell route map | MVVM class diagram | Offline entity model | Push notification sequence diagram
### Open Questions: [items for identity-architect (MSAL), security-architect (Key Vault signing), accessibility, or cicd-architect]
```

## Sibling Skills

- `/dotnet-architect`: .NET language patterns, async rules, Result\<T\>, DI, EF Core (for backend); MAUI-specific .NET patterns are here; shared C# rules are in `standards/references/coding-stack/csharp-standards.md`
- `/identity-architect`: MSAL.NET for interactive Entra ID/B2C sign-in in mobile apps, token cache design, Conditional Access compliance
- `/security-architect`: Azure Key Vault Code Signing for CI pipelines, SecureStorage best practices, OWASP Mobile Top-10
- `/accessibility`: Mobile a11y: SemanticProperties, WCAG 2.2 touch target sizes, VoiceOver/TalkBack testing
- `/azure-architect`: Azure backend services (App Service, Notification Hubs, Cosmos DB) that the MAUI app connects to
- `/cicd-architect`: GitHub Actions matrix builds for multi-platform MAUI publish workflows
- `/agent`: Pipeline orchestrator for cross-stack engagements
