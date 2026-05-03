---
category: design-documentation
loading_priority: 3
tokens_estimate: 2000
keywords:
  - integration patterns
  - REST API
  - Service Bus
  - Event Grid
  - Power Automate
  - Dataverse
  - Dynamics 365
  - dual-write
  - custom connector
  - OData
  - async messaging
  - file integration
version: "1.0"
last_updated: "2026-03-21"
---

# Integration Patterns Reference

This reference catalogs integration patterns organized by type and stack, providing guidance on when to use each pattern and how to implement it within the Microsoft ecosystem.

---

## Synchronous Patterns

### REST API
- **When to use:** Standard request-response interactions, CRUD operations, real-time data retrieval
- **Versioning:** URL path versioning (`/api/v1/`) preferred; header versioning (`api-version`) as alternative
- **Pagination:** Use `$top`, `$skip` for OData; `limit`, `offset` or cursor-based for custom APIs
- **Error handling:** RFC 7807 Problem Details format; appropriate HTTP status codes
- **Best practice:** Always route through Azure API Management for security, throttling, and observability

### gRPC
- **When to use:** Inter-service communication requiring high throughput and low latency; strongly-typed contracts
- **Schema management:** Protocol Buffer (`.proto`) files with versioned schemas in a shared registry
- **Transport:** HTTP/2 over TLS; requires gRPC-capable load balancer (Azure Application Gateway v2 or AKS ingress)
- **Best practice:** Use for internal service-to-service calls in Stack C; not suitable for browser clients without gRPC-Web proxy

### GraphQL
- **When to use:** Frontend-driven queries requiring flexible field selection; Backend-for-Frontend (BFF) pattern
- **Implementation:** Azure App Service or Container App hosting a GraphQL server (e.g., Hot Chocolate for .NET)
- **Best practice:** Place behind APIM; implement query depth limiting and complexity analysis to prevent abuse

### OData
- **When to use:** Dataverse and D365 native data access; standardized query capabilities
- **Capabilities:** `$filter`, `$select`, `$expand`, `$orderby`, `$top`, `$count`
- **Authentication:** OAuth 2.0 via Entra ID with application or delegated permissions
- **Best practice:** Use Dataverse Web API for Stack A and Stack D; leverage FetchXML for complex queries not expressible in OData

---

## Asynchronous Patterns

### Azure Event Grid
- **When to use:** Event-driven architectures; reacting to state changes in Azure resources or custom events
- **Topics:** System topics (Azure resource events) and custom topics (application events)
- **Subscriptions:** Filter by event type, subject prefix/suffix; webhook or Azure service endpoint
- **Retry policy:** Exponential backoff, max 24 hours, configurable max delivery attempts (default 30)
- **Dead-lettering:** Route failed events to a Storage Blob container for investigation
- **Best practice:** Use for loose coupling between services; combine with Event Grid domains for multi-tenant scenarios

### Azure Service Bus
- **When to use:** Reliable messaging requiring guaranteed delivery, ordering, or complex routing
- **Queues:** Point-to-point messaging; FIFO ordering with sessions; duplicate detection
- **Topics/Subscriptions:** Publish-subscribe with SQL or correlation filter rules
- **Sessions:** Ordered message processing grouped by session ID (e.g., per-entity processing)
- **Dead-letter queue:** Automatic after max delivery count; custom dead-lettering via rules
- **Best practice:** Use for critical business messages; implement correlation IDs for end-to-end tracing

### Azure Storage Queues
- **When to use:** Simple, high-volume queuing (millions of messages); no ordering or routing requirements
- **Poison messages:** Messages exceeding dequeue count moved to poison queue by Azure Functions runtime
- **Limitations:** Max message size 64 KB; no built-in dead-letter; at-least-once delivery
- **Best practice:** Use when Service Bus features are not needed and cost optimization is a priority

### Power Automate Triggers
- **Automated flows:** Triggered by Dataverse events (record created, updated, deleted), email arrival, form submission
- **Scheduled flows:** Polling-based on configurable intervals (minimum 1 minute for premium connectors)
- **Instant flows:** Manual trigger with optional input parameters
- **Best practice:** Use for business user-configurable workflows; implement proper error handling with try-catch scopes

---

## Power Platform Integration Patterns

### Standard Connectors
- Over 900 pre-built connectors available (SharePoint, SQL Server, HTTP, Outlook, Teams, etc.)
- Categorized as Standard (included in base license) and Premium (require premium license)
- Connection sharing: connection references for solution-aware deployments across environments

### Custom Connectors
- Built from OpenAPI (Swagger) specification or from scratch
- Authentication types: OAuth 2.0 (Authorization Code, Client Credentials), API Key, Basic Auth
- Policies: request/response transformations, parameter mapping
- Certification: publish to Microsoft connector ecosystem for organization-wide or public use
- **Best practice:** Wrap external APIs in custom connectors for governance and reusability

### Dataverse Web API
- RESTful CRUD operations on Dataverse tables via `https://{org}.api.crm.dynamics.com/api/data/v9.2/`
- Batch operations: `$batch` endpoint for multi-operation requests
- Change tracking: `Prefer: odata.track-changes` header for delta sync
- **Best practice:** Use for programmatic integration from Azure services into Dataverse

### Virtual Tables
- Present external data as Dataverse tables without copying data
- Backed by OData v4 virtual entity data provider or custom data providers
- Read-only by default; write support requires custom provider
- **Best practice:** Use when real-time external data is needed in model-driven apps without ETL

### Dataverse Plugins
- Server-side .NET code executing on data operations (Create, Update, Delete, Retrieve)
- Registration: pre-validation, pre-operation, post-operation stages; synchronous or asynchronous mode
- Isolation: sandbox mode (limited network access) or none (full trust, on-premises only)
- **Best practice:** Use for complex server-side validation and integration that must execute transactionally with the data operation

---

## D365 Integration Patterns

### Dual-Write
- Real-time bidirectional sync between D365 CE (Dataverse) and D365 F&O
- Supported scenarios: customer, vendor, product, sales order table maps
- Limitations: not customizable for complex transformations; requires specific schema alignment
- **Best practice:** Use for standard D365 CE-F&O integration scenarios; supplement with custom integration for complex transformations

### Virtual Entities
- Read external data through the Dataverse interface in D365 CE
- Backed by Finance and Operations virtual entity data provider
- Supports read and write for supported F&O entities
- **Best practice:** Use for looking up F&O data from CE without data duplication

### Data Export Service
- Near-real-time export of Dataverse data changes to Azure SQL Database
- Supports initial sync and incremental change tracking
- **Note:** Being deprecated in favor of Azure Synapse Link for Dataverse

### Azure Synapse Link for Dataverse
- Continuous export of Dataverse data to Azure Synapse Analytics or Azure Data Lake
- Supports both initial load and incremental updates
- Enables large-scale analytics and reporting without impacting Dataverse performance
- **Best practice:** Use for analytics workloads, data warehousing, and historical reporting

### F&O Data Entities
- OData endpoints exposing F&O business data (composite and standard entities)
- Batch operations via Data Management Framework (DMF) for bulk import/export
- Recurring integrations: file-based exchange via Azure Blob Storage
- **Best practice:** Use data entities for bulk data operations; use OData for real-time queries

### Business Events
- F&O event publishing to external systems via Service Bus, Event Grid, or HTTPS
- Triggered by business processes (e.g., purchase order confirmed, invoice posted)
- Catalog of standard business events; custom business events via extensions
- **Best practice:** Use for event-driven integration where F&O is the source of business events

---

## File-Based Integration

### Azure Blob Storage
- **When to use:** Large file transfers, batch processing, CSV/JSON/XML document exchange
- **Implementation:** Logic Apps or Azure Functions with Blob trigger; SAS tokens for secure access
- **Lifecycle management:** Tiered storage (Hot, Cool, Archive) with automated lifecycle policies

### SFTP
- **When to use:** Legacy system integration requiring SFTP protocol
- **Implementation:** Azure Logic Apps SFTP-SSH connector or Azure Blob Storage SFTP endpoint (preview)
- **Best practice:** Prefer Azure Blob Storage with SFTP support over separate SFTP servers

### Azure Data Factory
- **When to use:** Complex ETL/ELT pipelines, large-scale data movement, data transformation
- **Capabilities:** 100+ connectors, mapping data flows, wrangling data flows, copy activity
- **Orchestration:** Pipeline activities, triggers (schedule, tumbling window, event-based)
- **Best practice:** Use for batch data integration; combine with Synapse Link for near-real-time + batch hybrid

---

## Per-Stack Integration Recommendations

| Pattern | Stack A | Stack B | Stack C | Stack D |
|---------|---------|---------|---------|---------|
| REST API (via APIM) | Limited | Recommended | Recommended | Available |
| gRPC | Not available | Possible | Recommended | Not available |
| GraphQL | Not available | Optional | Optional | Not available |
| OData | Native | Available | Available | Native |
| Event Grid | Via connector | Recommended | Recommended | Via Business Events |
| Service Bus | Via connector | Recommended | Recommended | Recommended |
| Storage Queues | Via connector | Optional | Optional | Via Logic Apps |
| Power Automate | Primary | Supplementary | Supplementary | Supplementary |
| Standard Connectors | Primary | Supplementary | Limited use | Supplementary |
| Custom Connectors | Recommended | Available | Limited use | Available |
| Dataverse Web API | Native | Recommended | Available | Native |
| Virtual Tables | Available | Available | Not typical | Available |
| Dual-Write | N/A | N/A | N/A | Recommended (CE+F&O) |
| Synapse Link | Available | Recommended | Available | Recommended |
| Data Factory | Via connector | Recommended | Available | Recommended |
| Blob Storage | Via connector | Recommended | Recommended | Via Logic Apps |

**Legend:** Primary = main integration approach; Recommended = best practice for the stack; Available = supported but not primary; Supplementary = used alongside primary patterns; Limited use = technically possible but not typical; Not available = not supported in this stack; N/A = not applicable.

---

## Anti-Patterns to Avoid

### Synchronous Chains Spanning More Than 3 Services
- **Problem:** Cascading latency, single point of failure, tight coupling
- **Solution:** Break chains with async messaging (Service Bus); use the saga pattern for distributed transactions

### Polling When Event-Driven Is Available
- **Problem:** Wasted compute, delayed detection, unnecessary API load
- **Solution:** Use Event Grid, Service Bus, or Dataverse webhooks for real-time notification

### Point-to-Point When Hub/Spoke Is Needed
- **Problem:** N-squared integration complexity, no central governance
- **Solution:** Use APIM as the API hub; use Service Bus topics for event distribution; use Logic Apps for integration orchestration

### Bypassing APIM for Direct Service Calls
- **Problem:** No centralized security, no throttling, no observability, no versioning
- **Solution:** Route all external and cross-boundary API calls through APIM; use VNet integration and private endpoints for internal routing

### Storing Secrets in Application Settings
- **Problem:** Secrets visible in portal, deployment templates, and source control
- **Solution:** Store all secrets in Azure Key Vault; reference via Key Vault references in App Service or managed identity access

### Ignoring Idempotency in Message Processing
- **Problem:** Duplicate processing causes data corruption or duplicate business actions
- **Solution:** Design all message handlers to be idempotent; use deduplication IDs in Service Bus; implement upsert logic in data operations
