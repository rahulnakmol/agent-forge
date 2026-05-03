# Adaptive Cards Design

**Scope**: Adaptive Cards 1.5 schema, Universal Action Model (`Action.Execute`), Outlook actionable messages, Teams cards, Viva Connections ACE quick views, fallback to `Action.Submit` for older Teams clients.

**Opinionated rule**: Adaptive Cards for actionable messages in Outlook and Teams. Never custom HTML in Outlook. Outlook strips, sanitizes, and renders inconsistently across clients (desktop, web, mobile, Mac). Adaptive Cards render the same card the same way across hosts and update in place.

## Why Adaptive Cards

- One JSON payload, multiple hosts (Teams, Outlook, Viva Connections quick views, Microsoft 365 Copilot, custom apps).
- Host-aware theming: same card adopts Teams light/dark and Outlook chrome automatically.
- Universal Action Model lets a single bot back the same card in Teams and Outlook.
- Updateable via `refresh` and `card.refresh.action`: bot returns a new card payload to replace the rendered card.

## Schema basics (1.5)

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "originator": "<guid-from-actionable-messages-onboarding>",
  "body": [
    { "type": "TextBlock", "text": "Approve PO", "weight": "Bolder", "size": "Medium" },
    { "type": "Input.Text", "id": "comment", "placeholder": "Optional comment" }
  ],
  "actions": [
    {
      "type": "Action.Execute",
      "title": "Approve",
      "verb": "approve",
      "data": { "poId": "PO-123" },
      "fallback": { "type": "Action.Submit", "title": "Approve", "data": { "verb": "approve", "poId": "PO-123" } }
    }
  ]
}
```

Set `version` to the lowest version that the lowest-supported host can render. Wrap every `Action.Execute` in an `ActionSet` if older Teams clients are in scope (some older clients ignore `fallback` outside an ActionSet).

## Universal Action Model (`Action.Execute`)

`Action.Execute` replaces both `Action.Http` (Outlook actionable messages, deprecated for new work) and `Action.Submit` (Teams bots, still required for link unfurling and message extension actions).

Flow:

1. Card rendered in Teams or Outlook with `Action.Execute` button.
2. User clicks: host posts `adaptiveCard/action` invoke activity to the bot.
3. Bot reads `verb` and `data`, runs business logic.
4. Bot returns a response with `statusCode: 200`, `type: "application/vnd.microsoft.card.adaptive"`, and a new card payload.
5. Host replaces the rendered card in place.

Outlook-specific:

- The bot must subscribe to the **Outlook Actionable Messages** channel in the Bot Framework portal.
- The card MUST include `originator` (GUID from the Actionable Messages onboarding form).
- `userIds` in `refresh` is ignored in Outlook (refresh always honored, no scale issue, users open mail asynchronously).

Teams-specific:

- Set `userIds` in `refresh` (max 60 users) to enable auto-refresh on display. Without it, users see a "Refresh" button.
- Wrap `Action.Execute` in `ActionSet` for fallback support.
- Bot processes both `Action.Execute` (modern) and `Action.Submit` (fallback for older clients). Fallback path produces a degraded experience: bot cannot return a new card on `Action.Submit`.

## Bot handler shape

C# (`Microsoft.Bot.Builder`):

```csharp
protected override async Task<AdaptiveCardInvokeResponse> OnAdaptiveCardInvokeAsync(
    ITurnContext<IInvokeActivity> turnContext,
    AdaptiveCardInvokeValue invokeValue,
    CancellationToken cancellationToken)
{
    var verb = invokeValue.Action.Verb;       // e.g. "approve"
    var data = invokeValue.Action.Data;       // payload from the card
    // run business logic, build new card
    return new AdaptiveCardInvokeResponse {
        StatusCode = 200,
        Type = "application/vnd.microsoft.card.adaptive",
        Value = newCardJson
    };
}
```

Node.js (`botbuilder`):

```typescript
async onAdaptiveCardInvoke(context, invokeValue) {
  const verb = invokeValue.action.verb;
  const data = invokeValue.action.data;
  return { statusCode: 200, type: 'application/vnd.microsoft.card.adaptive', value: newCardJson };
}
```

## Authoring tooling

- Adaptive Cards Designer (https://adaptivecards.io/designer) for visual authoring with host preview (Teams, Outlook).
- Templating language for data binding (`${expression}` syntax) via `adaptivecards-templating` npm package: keep card layout and data separate.
- Validate JSON schema with the schema URL above.

## Use cases by host

**Outlook actionable messages**: approval flows (expense, PO, leave), survey, status update from a bot. Always single-shot or short-flow scenarios. Cards arrive via email from a bot service registered in the Actionable Messages program.

**Teams**: bot posts (proactive notifications, bot-initiated chats), message extension previews (unfurled links), task module dialogs, meeting side-panel cards.

**Viva Connections (ACE)**: Card View (Basic, Image, Primary Text, Data Visualization) with Quick View (Adaptive Card or HTML in 1.20+). Quick View typically uses simpler cards (no Action.Execute, ACE handles the action callback).

**Copilot extensibility**: Adaptive Cards as the response surface for declarative agents and message extensions in Copilot.

## Anti-patterns

- Do not use `Action.Http` for new Outlook actionable messages: it is the legacy model and does not work in Teams.
- Do not embed `<iframe>` or HTML in card text: hosts strip it.
- Do not omit `originator` in Outlook cards: the host refuses to render.
- Do not rely on bot state to identify the user: include user identity claim from the invoke activity (`turnContext.Activity.From.AadObjectId`).
- Do not skip the `fallback` action in Teams: older clients that do not support 1.4+ silently drop the button.
- Do not mix `Action.Http` and `Action.Execute` in the same card: hosts pick one model per card.

## Verification with Microsoft Learn MCP

Run `microsoft_docs_search` for:

- `Universal Action Model Adaptive Cards` for the latest invoke schema.
- `Outlook Actionable Messages onboarding` for `originator` provisioning.
- `Teams Adaptive Cards backward compatibility` for fallback patterns.
- `Adaptive Cards 1.5` for schema additions.
