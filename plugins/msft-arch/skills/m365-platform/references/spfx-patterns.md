# SharePoint Framework (SPFx) Patterns

**Scope**: SPFx 1.20+ (Sept 2024 GA), Node.js 18, Yeoman generator v5, Webpack 5, TypeScript 4.7+, Fluent UI React v9 for new work (v8 if matching existing themes), PnPjs v4 for SharePoint and Graph data access.

**Opinionated rule**: SPFx > legacy SharePoint Framework / Add-ins for new SharePoint customizations. The SharePoint Add-in model is deprecated, sandbox solutions are end-of-life, full-trust farm solutions are SharePoint Server only. SPFx is the only forward path on SharePoint Online.

## When to use SPFx

Use SPFx for:

- SharePoint pages: client-side web parts in modern pages, isolated web parts for tightly scoped third-party scripts.
- SharePoint extensions: application customizers (top/bottom placeholders), field customizers (column rendering), ListView command sets (toolbar actions on list items).
- Adaptive Card Extensions (ACEs) for Viva Connections dashboards (Card View + Quick View pairs, Data Visualization Card, HTML Quick View as of 1.20).
- Teams tabs that share SharePoint context (single codebase, two manifests).

Do not use SPFx for:

- Standalone Teams apps with no SharePoint dependency: use Microsoft 365 Agents Toolkit (TTK) instead.
- Outlook add-ins or Office task panes: use Office.js + Yo Office or TTK with Office add-in template.
- Anonymous external-facing portals: use Power Pages.

## Project shape

```
spfx-solution/
  config/                         package-solution.json, serve.json, write-manifests.json
  src/
    webparts/<name>/              .ts entry, .module.scss, manifest.json, *.tsx components
    extensions/<name>/            applicationCustomizer / fieldCustomizer / commandSet
    adaptiveCardExtensions/<n>/   ACE entry, cardView/, quickView/
  package.json                    @microsoft/sp-* pinned to current SPFx version (e.g. 1.20.0)
  gulpfile.js                     build, bundle, serve, clean, package-solution
  tsconfig.json                   target ES2017+, strict mode
```

## Patterns to apply

**Isolated web parts**: Set `"isDomainIsolated": true` in `package-solution.json` for any web part that loads third-party scripts or makes cross-origin calls to APIs the tenant does not fully trust. Each isolated web part runs in a unique app domain, scoped permissions in Entra ID.

**PnPjs v4 over raw SPHttpClient**: Use `@pnp/sp` and `@pnp/graph` for fluent, typed access to lists, items, files, sites, and Graph endpoints. Configure once in web part `onInit()` with the SPFx context, reuse the configured instance.

**MSGraphClientV3 for Graph from SPFx**: Inject via SPFx context (`context.msGraphClientFactory.getClient('3')`). Permissions requested in `package-solution.json` under `webApiPermissionRequests`, granted by tenant admin in SharePoint admin center API access page.

**AadHttpClient for custom APIs**: For non-Graph APIs protected by Entra ID, use `context.aadHttpClientFactory.getClient(resourceAppId)`. Same `webApiPermissionRequests` flow for tenant admin grant.

**Teams-context dual rendering**: Detect Teams host with `this.context.sdks.microsoftTeams`. Branch UI for Teams (no SharePoint chrome, Teams theme tokens) vs SharePoint (full chrome). Single bundle, two manifests (one for SharePoint web part, one for Teams tab pointing at the same web part GUID).

**Adaptive Card Extensions for Viva**: Use `BaseAdaptiveCardExtension`, pair `BaseComponentsCardView` (1.18+ default) with `BaseAdaptiveCardQuickView` or HTML Quick View (1.20+). Data Visualization Card Template (1.19+) for charting.

**Fluent UI v9 for new work**: `@fluentui/react-components` is the v9 package. Use design tokens (`tokens.colorNeutralBackground1`) over hex codes. Match SharePoint and Teams theme automatically via `FluentProvider`.

## Build and packaging

```bash
gulp clean
gulp build
gulp bundle --ship                # production minified bundle
gulp package-solution --ship      # produces .sppkg in sharepoint/solution/
```

Upload `.sppkg` to the tenant app catalog (or site collection app catalog for scoped deploy). Trust the solution. Tenant admin grants any pending API permissions.

## Anti-patterns

- Do not import the SharePoint JSOM (`SP.js`) in new SPFx work: use REST or PnPjs.
- Do not use `jQuery` or jQuery plugins: bundle bloat, accessibility risk, no upside on modern browsers.
- Do not store secrets in `package-solution.json` or web part properties: SPFx is client-side, properties are world-readable in the page source.
- Do not embed third-party scripts via `<script>` tags in extensions: use isolated web parts and proper API permissions.
- Do not skip `gulp bundle --ship`: shipping unminified bundles blows the 500KB budget instantly.

## Verification with Microsoft Learn MCP

Before finalizing an SPFx design, run `microsoft_docs_search` for:

- Current SPFx release notes (`SharePoint Framework v1.X release notes`).
- Latest Node.js, Yeoman, gulp-cli compatibility matrix.
- Active deprecations in the current SPFx version.
- Adaptive Card Extensions tutorials matching the target Viva Connections experience.
