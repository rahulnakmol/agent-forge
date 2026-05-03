# Teams Toolkit (Microsoft 365 Agents Toolkit)

**Scope**: Microsoft 365 Agents Toolkit (TTK successor, package `@microsoft/m365agentstoolkit-cli`, command `atk`), Teams app manifest schema v1.16+, Bot Framework SDK v4, TeamsFx SDK v2, TypeScript or C# back-ends.

**Naming note**: Microsoft renamed the toolkit. Older docs and templates use TTK, `teamsfx`, `teamsapp-cli`. New scaffolds use `atk`. Treat them as the same product family. The CLI commands remain analogous (`new`, `provision`, `deploy`, `package`, `validate`, `publish`, `preview`).

**Opinionated rule**: Teams Toolkit (TTK) for new Teams apps. SPFx as Teams tab when shared with SharePoint context. TTK owns scaffolds, manifest, infra-as-code (Bicep), local debug tunneling, and provisioning. Hand-rolling a Teams app manifest is acceptable only for tiny experiments.

## Capabilities and surfaces

| Capability | Surface | Use when |
|---|---|---|
| Personal tab | One-on-one in Teams | User-specific tools, dashboards, settings |
| Channel tab | Group conversation | Shared workflow, project board, status panel |
| Meeting tab | Pre/during/post meeting | Agenda, polls, in-meeting collaboration |
| Bot | Chat conversation | Q&A, notifications, conversational workflows |
| Message extension (search) | Compose box | Pull external content into a message |
| Message extension (action) | Compose box, command | Form-driven message creation |
| Link unfurling | Compose box | Render preview cards for known URLs |
| Connectors (legacy) | Channel | Avoid for new work, use bots + Adaptive Cards instead |
| Outlook + Teams unified app | Both hosts | One manifest, two homes via unified manifest |

## Project shape

```
teams-app/
  appPackage/                 manifest.json (v1.16+), color.png, outline.png
  bot/ or tabs/ or api/       app code per capability
  infra/                      azure.bicep, azure.parameters.json
  m365agents.yml              provision/deploy stages (replaces older teamsapp.yml)
  m365agents.local.yml        local-debug stage
  env/                        .env.dev, .env.local, .env.prod
  package.json                @microsoft/teamsfx, @microsoft/teamsfx-react, botbuilder
```

## CLI commands (latest)

```bash
npm install -g @microsoft/m365agentstoolkit-cli
atk -h                                       # list commands
atk new                                      # scaffold new app, interactive
atk new --capabilities tab-spfx              # SPFx tab
atk new --capabilities notification          # notification bot
atk new --capabilities command-bot           # command and response bot
atk provision --env dev                      # provision Azure + AAD + Teams app reg
atk deploy --env dev                         # deploy code to provisioned infra
atk package                                  # build app package zip
atk validate --env dev                       # manifest validation
atk publish --env prod                       # publish to org app catalog
atk preview --env local                      # local debug
```

For older projects, fall back to `teamsapp` (CLI v3) or `teamsfx` (CLI v2). Verify with `microsoft_docs_search` for `Teams Toolkit command line interface` to match the project's pinned generation.

## Bot Framework SDK v4 patterns

Use `botbuilder` (Node.js) or `Microsoft.Bot.Builder` (C#) v4. Implement:

- `ActivityHandler` subclass for message and conversation event routing.
- `OnAdaptiveCardInvokeAsync` (C#) or `onAdaptiveCardInvoke` (Node) to handle `Action.Execute` invokes.
- `TeamsActivityHandler` for Teams-specific events (mention, file consent, meeting events).
- Storage abstraction: `MemoryStorage` for dev only, `BlobsStorage` or `CosmosDbPartitionedStorage` for production state.

## SSO and identity

TTK scaffolds include the SSO plumbing:

- AAD app registration created at `provision`.
- Token exchange via TeamsFx SDK: `new TeamsFx().getCredential().getToken(scopes)`.
- Graph access via `createMicrosoftGraphClient(teamsfx, scopes)`.

For depth on scopes, app vs delegated, Conditional Access impact, hand off to `/identity-architect`. For Graph permission shapes and throttling, hand off to `/microsoft-graph`.

## Manifest v1.16+ key fields

```json
{
  "manifestVersion": "1.16",
  "id": "<uuid>",
  "name": { "short": "...", "full": "..." },
  "description": { "short": "...", "full": "..." },
  "developer": { "name": "...", "websiteUrl": "...", "privacyUrl": "...", "termsOfUseUrl": "..." },
  "icons": { "color": "color.png", "outline": "outline.png" },
  "accentColor": "#...",
  "bots": [...], "composeExtensions": [...], "staticTabs": [...], "configurableTabs": [...],
  "permissions": ["identity", "messageTeamMembers"],
  "validDomains": [...],
  "webApplicationInfo": { "id": "<aad-app-id>", "resource": "api://..." }
}
```

## Anti-patterns

- Do not skip `atk validate`: manifest schema errors block publish.
- Do not bake secrets into `manifest.json`: TTK environment files (`env/.env.<env>`) are for non-secrets, Azure Key Vault references are for secrets.
- Do not use legacy O365 Connectors for new actionable workflows: bots + Adaptive Cards (`Action.Execute`) are the supported model.
- Do not ship a bot without persistent storage: in-memory state breaks on App Service restart.
- Do not let the package balloon past 1MB: see `bundle-size-budgets.md`.

## Verification with Microsoft Learn MCP

Run `microsoft_docs_search` for:

- `Microsoft 365 Agents Toolkit CLI` to confirm current command surface.
- `Teams app manifest schema` for the latest version and field deprecations.
- `Bot Framework SDK v4` for activity handler patterns.
- `Teams SSO` for current token exchange flow.
