# Bundle Size Budgets

**Scope**: Performance budgets for M365 platform extensions. SPFx web parts and ACEs, Teams app packages, Office add-in task panes. Lighthouse audits, lazy loading, externals, code splitting.

**Opinionated rule**: Bundle size matters: SPFx < 500KB gzipped, Teams app < 1MB. These are not aspirational targets, they are gates. Cards, web parts, and task panes load inside hosts that already carry their own JavaScript payload. A heavy extension stalls the entire page and erodes user trust in the host.

| Surface | Budget | Measured how |
|---|---|---|
| SPFx web part bundle | < 500KB gzipped per entry | `webpack-bundle-analyzer` against `dist/*.js` |
| SPFx ACE bundle | < 250KB gzipped (mobile-sensitive) | same |
| Teams app package zip | < 1MB total | `du -h appPackage/build/appPackage.dev.zip` |
| Teams tab page initial JS | < 500KB gzipped | Lighthouse network panel |
| Office add-in task pane initial JS | < 500KB gzipped | Lighthouse, browser dev tools |
| Outlook event-based handler | < 100KB gzipped (cold-start sensitive) | Lighthouse, dev tools |

## How budgets are blown

The five recurring causes:

1. **Bundling all of Fluent UI**: Fluent UI v8 and v9 are large. Import only the specific components used. Avoid `import * from '@fluentui/react'`.
2. **Bundling React when the host already provides it**: SPFx exposes React via the SPFx loader. Externalize React in `webpack.config.js`. Do not double-ship.
3. **Polyfills for browsers the host does not support**: Modern Office hosts run on Edge/Chromium engines. Drop IE11 polyfills.
4. **Source maps in production**: Set `--ship` (gulp) or `--mode production` (webpack) to drop source maps from the shipped bundle.
5. **Leaking dev dependencies into runtime**: testing libraries, mock data files, fixture JSON. Audit `dist/` after every build.

## SPFx techniques

**Externalize peers**: In `config/config.json`, add:

```json
{
  "externals": {
    "react": {
      "path": "https://unpkg.com/react@17/umd/react.production.min.js",
      "globalName": "React"
    },
    "react-dom": {
      "path": "https://unpkg.com/react-dom@17/umd/react-dom.production.min.js",
      "globalName": "ReactDOM"
    }
  }
}
```

(Match versions to the SPFx-provided React peer; consult the active SPFx version's release notes.)

**Tree-shake Fluent UI v9**:

```typescript
import { Button } from '@fluentui/react-components';        // good
import * as fui from '@fluentui/react-components';          // bad
```

**Code-split heavy chunks**: Dynamic `import()` for Quick View HTML rendering, charting libs, rich-text editors. SPFx supports dynamic imports out of the box on Webpack 5 (1.19+).

**Isolated web parts**: When loading third-party scripts, set `"isDomainIsolated": true`. Each isolated web part runs in its own iframe; bundle size affects only that iframe, not the whole page.

**Strip dev-only assets**: Delete fixture JSON, sample data, README from the bundled output. Add to `.gitignore` and ensure they are not in `src/` if production builds include all of `src/`.

## Teams app package techniques

Teams app package = manifest.json + 2 icon PNGs + (optional) tab/bot/me code if hosted within the package. Keep:

- Icons under 100KB each (color.png 192x192, outline.png 32x32 transparent).
- No fonts in the package: Teams provides Segoe UI.
- No source maps in shipped JS.
- No node_modules anywhere in the package.

## Office add-in task pane techniques

- Lazy-load the task pane shell: render skeleton first, then hydrate.
- Externalize Office.js (loaded from the host CDN via `<script>` tag in the task pane HTML, not bundled).
- Cache static assets aggressively (long max-age + content hash in filename).
- Validate cold start time: Outlook event-based handlers run in a constrained runtime with strict cold-start budget.

## Lighthouse audits

Run a Lighthouse audit against the rendered task pane or Teams tab URL:

```bash
npx lighthouse https://localhost:3000/ --preset=desktop --view
```

Targets:

- Performance score > 90.
- Total blocking time < 200ms.
- Largest contentful paint < 2.5s.
- Cumulative layout shift < 0.1.

For production hosts (HTTPS endpoints behind the manifest), run Lighthouse in CI with `lighthouse-ci` and assert thresholds. See `/cicd-architect` for pipeline integration.

## Verification recipe

Add to every PR for an SPFx solution:

```bash
gulp clean
gulp bundle --ship
ls -lh dist/*.js | awk '{print $5, $9}'         # shipped sizes
gzip -c dist/*.js | wc -c                       # gzipped size
npx webpack-bundle-analyzer dist/stats.json     # visualize
```

For Teams apps:

```bash
atk package
ls -lh appPackage/build/appPackage.*.zip
unzip -l appPackage/build/appPackage.dev.zip    # confirm contents
```

For Office add-ins:

```bash
npm run build
ls -lh dist/*.js
npx lighthouse https://localhost:3000/taskpane.html --preset=desktop
```

## Anti-patterns

- Do not ship development bundles to production. `--ship` or `--mode production` always.
- Do not import an entire icon library: import only the icons used.
- Do not add Moment.js to a new project: use `date-fns` or native `Intl.DateTimeFormat`.
- Do not rely on the network for critical first paint: extensions should render usable UI from the bundled code, then enrich with API data.
- Do not skip the gzipped measurement: raw bundle size is misleading; CDNs serve gzip or brotli.
- Do not let bundle-size regressions land silently: add a CI check that compares the gzipped size to a baseline and fails the PR on a > 5% regression.
