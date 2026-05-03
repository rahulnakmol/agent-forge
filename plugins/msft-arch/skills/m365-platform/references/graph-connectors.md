# Graph Connectors (Microsoft 365 Copilot Connectors)

**Scope**: Custom Microsoft 365 Copilot connectors (formerly Microsoft Graph connectors), schema registration, item ingestion API, semantic labels, content property, `urlToItemResolver`, user activities, external groups for ACL.

**Opinionated rule**: Graph Connectors when surfacing 3rd-party content in M365 search. Native M365 Search and Copilot already index SharePoint, OneDrive, Teams, mail, and calendar. Use a Graph Connector to bring data from external systems (Jira, ServiceNow, Salesforce, custom line-of-business apps, file shares) into the same M365 Search and Copilot result surface.

## When to use a Graph Connector

Use a Graph Connector when:

- External system holds knowledge that users search for inside M365 (tickets, KB articles, SOPs, contracts, CRM records).
- Users today context-switch out of M365 to find this content.
- Copilot summaries should ground on this content.
- Tenant admin authorizes the data ingestion.

Do not use a Graph Connector when:

- The data already lives in SharePoint or OneDrive (it is already indexed).
- Real-time sub-second access is required (connectors crawl on a schedule, not on demand).
- Users need write-back to the external system from search results (search is read-only).

## Build options

| Path | Use when |
|---|---|
| Microsoft 365 Agents Toolkit (TTK / `atk`) | Greenfield, want scaffolding + sample code + sideload-friendly dev loop |
| Connector SDK (.NET) | Existing .NET service, on-prem agent, file-share or SQL ingestion patterns |
| Copilot connectors REST API directly | Custom orchestration, language not covered by SDK, large-scale custom pipelines |

## Schema registration

Every connector defines a flat schema: a list of source properties with attributes (`isQueryable`, `isSearchable`, `isRetrievable`, `isRefinable`, `isExactMatchRequired`), semantic labels, and aliases.

```json
{
  "baseType": "microsoft.graph.externalItem",
  "properties": [
    { "name": "ticketId",  "type": "String",         "isQueryable": true, "isRetrievable": true, "isExactMatchRequired": true },
    { "name": "title",     "type": "String",         "isSearchable": true, "isRetrievable": true, "labels": ["title"] },
    { "name": "createdBy", "type": "String",         "isQueryable": true, "isRetrievable": true, "labels": ["createdBy"] },
    { "name": "lastEditedDate", "type": "DateTime",  "isQueryable": true, "isRetrievable": true, "labels": ["lastModifiedDateTime"] },
    { "name": "url",       "type": "String",         "isRetrievable": true, "labels": ["url"] },
    { "name": "tags",      "type": "StringCollection", "isQueryable": true, "isRetrievable": true, "isExactMatchRequired": true, "aliases": ["labels", "categories"] }
  ]
}
```

Rules:

- A property cannot be both **searchable** and **refinable**.
- `isExactMatchRequired: true` only applies to non-searchable properties.
- Properties mapped to semantic labels must be **retrievable**.
- The `content` property is built-in: do not declare it. Pass content text in the item payload during ingestion.

## Semantic labels (high-impact)

Apply semantic labels so M365 Search and Copilot understand the meaning of each property. Highest-impact labels (descending): `title`, `lastModifiedDateTime`, `lastModifiedBy`, `url`, `fileName`, `fileExtension`. Also useful: `createdBy`, `authors`, `createdDateTime`, `iconUrl`, `containerName`, `containerUrl`.

Each label maps to **exactly one** property. Wrong mappings degrade search quality more than missing labels.

## Item ingestion

Each external item is an `externalItem` resource with:

- `id`: stable identifier in the external system.
- `properties`: dictionary keyed by schema property name, plus `content`.
- `acl`: list of access control entries (allow/deny, principal type, principal value).
- `activities`: optional user activity list (`viewed`, `modified`) to improve ranking.

```json
{
  "@odata.type": "microsoft.graph.externalItem",
  "id": "ticket-CTS-12345",
  "acl": [
    { "type": "everyone", "value": "everyone", "accessType": "grant" }
  ],
  "properties": {
    "ticketId": "CTS-12345",
    "title": "Wi-Fi outage in Building C",
    "createdBy": "alice@contoso.com",
    "lastEditedDate": "2026-04-12T14:32:00Z",
    "url": "https://tickets.contoso.com/CTS-12345",
    "tags": ["network", "wifi", "outage"]
  },
  "content": {
    "type": "text",
    "value": "Users in Building C report intermittent Wi-Fi disconnects. Root cause traced to AP firmware. Mitigation in progress."
  }
}
```

## URL-to-item resolver

Add a `urlToItemResolver` so M365 Search can map a pasted URL back to the indexed item (powers link unfurling and "this item already exists" hints in Copilot).

```json
{
  "urlToItemResolvers": [
    {
      "@odata.type": "#microsoft.graph.externalConnectors.itemIdResolver",
      "urlMatchInfo": {
        "baseUrls": ["https://tickets.contoso.com"],
        "urlPattern": "/(?<id>CTS-[0-9]+)"
      },
      "itemId": "ticket-{id}"
    }
  ]
}
```

## Access control (ACL)

Connectors enforce ACL at index time. Per-item ACL options:

- `everyone`: all licensed M365 users in the tenant.
- `everyoneExceptGuests`: excludes B2B guests.
- `group`: AAD security or M365 group ID.
- `user`: specific AAD user ID.
- `external group`: synthetic group defined in the connector via `externalGroup` resource (use when the source system has its own group model that does not map to AAD).

Use deny entries sparingly: they require explicit listing of who is excluded.

## Activities (ranking signal)

Post `addActivities` events whenever a user views or modifies an item in the source system. Activities improve relevance ranking and personalize results.

## Verification with Microsoft Learn MCP

Run `microsoft_docs_search` for:

- `Microsoft 365 Copilot connectors overview` for the current build paths.
- `Register and manage schema for Microsoft 365 Copilot connectors` for the latest semantic label catalog.
- `Copilot connectors API` for the REST endpoint surface.
- `urlToItemResolver` for current resolver types and examples.

## Anti-patterns

- Do not skip semantic labels: search quality drops sharply.
- Do not put rich text or markdown in `content` without normalization: index it as plain text, store original elsewhere.
- Do not use `everyone` ACL when the source has finer permissions: respect the source's access model.
- Do not ingest huge blobs into `content`: trim to relevant excerpt, link to source for the full document.
- Do not forget to publish the connector to the Microsoft 365 admin center (`Search & intelligence` > `Data Sources`).
