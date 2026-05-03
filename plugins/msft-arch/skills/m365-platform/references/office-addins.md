# Office Add-ins (Office.js)

**Scope**: Office add-ins for Word, Excel, Outlook, PowerPoint, Project, OneNote. Office.js (`@microsoft/office-js`), unified manifest for Microsoft 365 (JSON) vs add-in only manifest (XML), commands, task panes, custom functions, event-based activation.

**Opinionated rule**: Office add-ins use the modern API (Office.js). Never VSTO for new work. VSTO add-ins ship .NET Framework binaries to Windows-only desktop Office, no cross-platform story, no web app shell, no Mac, no Office on the web. Office.js add-ins run anywhere Office runs (Windows, Mac, web, iPad in supported scopes).

Treat COM add-ins, VBA macros, and Office Web Add-ins (legacy phrasing for Office Add-ins) the same way: legacy, not for new work.

## Manifest format choice

Two formats coexist:

| Format | When to choose |
|---|---|
| **Add-in only manifest (XML)** | Maintenance of an existing XML-manifest add-in, targeting Office versions older than 2304, scenarios using Outlook contextual add-ins or Outlook modules (not yet in unified manifest) |
| **Unified manifest for Microsoft 365 (JSON)** | New greenfield work, Microsoft 365 Version 2307+ users, single distribution unit combining Office add-in + Teams app + declarative agent in one manifest |

The unified manifest is the future direction. New scaffolds from `atk new` (Microsoft 365 Agents Toolkit) and the Yo Office generator with the `--unified-manifest` option produce unified manifest projects.

Caveats for unified manifest:

- Sideload supported on Office on Windows 2304+ and Mac (Excel/PowerPoint/Word) 16.103+. Not yet on iPad or Outlook on Mac.
- Outlook contextual add-ins (activation rules) and Outlook modules are not supported: provide event-based activation or a Teams Tab equivalent instead.
- Visual Studio does not support the unified manifest: use VS Code with the Office Add-ins extension or the Microsoft 365 Agents Toolkit.

## Project shape (unified manifest, TypeScript task pane)

```
office-addin/
  manifest.json                 unified manifest, references icons + commands.html + taskpane.html
  src/
    commands/commands.ts        ribbon command actions registered via Office.actions.associate
    taskpane/taskpane.html      task pane shell
    taskpane/taskpane.ts        Office.onReady, business logic, Office.js calls
    functions/functions.ts      Excel custom functions (when applicable)
  webpack.config.js             SSL dev server, env injection
  package.json                  @microsoft/office-js, office-addin-debugging, office-addin-manifest
```

## Office.js patterns

```typescript
Office.onReady((info) => {
  if (info.host === Office.HostType.Excel) {
    document.getElementById('run').onclick = run;
  }
});

async function run() {
  await Excel.run(async (context) => {
    const range = context.workbook.getSelectedRange();
    range.load('values, address');
    await context.sync();
    console.log(`Selected ${range.address}: ${range.values}`);
  });
}
```

Apply per-host:

- **Word**: `Word.run` with `context.document.body`, content controls, search, range insertion.
- **Excel**: `Excel.run` with `context.workbook`, ranges, tables, charts, custom functions for cell-level logic.
- **Outlook**: `Office.context.mailbox.item` for read/compose properties, `getCallbackTokenAsync` for EWS, event-based activation for `OnNewMessageCompose`, `OnMessageRecipientsChanged`, etc.
- **PowerPoint**: `PowerPoint.run` with slides, shapes, selection, image insertion.

Use `requirements.capabilities` in the manifest to declare the minimum requirement set for each API call site (e.g. `ExcelApi 1.13`, `Mailbox 1.10`).

## Commands and ribbon

Define ribbon buttons and menus in the manifest's `extensions[].ribbons` array. Each command points to either:

- A function in `commands.ts` registered via `Office.actions.associate('actionId', fn)`.
- A task pane HTML page that opens when the user clicks.

Action IDs in the manifest must match the string passed to `Office.actions.associate` exactly.

## Task panes

Single-page web app rendered in a side panel inside the host. Use any framework (React + Fluent UI v9 recommended). Office.js APIs available throughout. Persist state in `OfficeRuntime.storage` or AAD-protected backend, not in browser localStorage (storage isolation rules).

## Excel custom functions

Author functions in TypeScript with JSDoc-driven metadata:

```typescript
/**
 * Adds two numbers.
 * @customfunction
 * @param a First number.
 * @param b Second number.
 * @returns The sum.
 */
function add(a: number, b: number): number {
  return a + b;
}
```

The build emits a `functions.json` metadata file referenced from the manifest. Streaming functions, async functions, and cancellation tokens are supported. Unified manifest enforces stricter naming and metadata rules than the XML manifest historically did.

## Authentication

- **Single sign-on (SSO)**: `OfficeRuntime.auth.getAccessToken({ allowSignInPrompt: true })` returns a bootstrap token; exchange server-side via on-behalf-of flow for downstream Graph or custom API access.
- **MSAL.js fallback**: Used when SSO is not configured or fails (browser pop-up consent flow). The Office add-in scaffolds in TTK and Yo Office include both paths.

For depth on token caches, scopes, Conditional Access impact, hand off to `/identity-architect`. For Graph permissions and patterns, hand off to `/microsoft-graph`.

## Event-based activation (Outlook)

Replaces older "compose VS read" launch events. Register handlers in `extensions[].autoRunEvents`:

```json
{
  "extensions": [{
    "autoRunEvents": [{
      "events": [
        { "type": "newMessageComposeCreated", "actionId": "onNewMessageCompose" }
      ]
    }]
  }]
}
```

Handler runs in a hidden runtime (no UI). Common uses: prepend a confidentiality footer, validate recipient domains, add a tracking pixel, run DLP checks before send.

## Verification with Microsoft Learn MCP

Run `microsoft_docs_search` for:

- `Office Add-ins manifest` to confirm current XML vs unified manifest guidance.
- `Convert an add-in to use the unified manifest for Microsoft 365` for migration steps.
- `Office.js requirement sets` for the latest API surface availability matrix.
- `Event-based activation Outlook` for current event types.

## Anti-patterns

- Do not pick VSTO for new work, ever.
- Do not use Internet Explorer-only APIs in task panes: Office on the web runs in the user's browser engine.
- Do not store secrets in `manifest.json`: it is downloaded with the add-in.
- Do not assume desktop-only: target the requirement sets for Office on the web and Mac too.
- Do not ship a unified-manifest add-in to users on Office < 2307 without a fallback XML manifest version (unless tenant admin deploys it for all users, which bypasses the version requirement).
- Do not skip `office-addin-manifest validate`: schema errors block AppSource and tenant deploy.
