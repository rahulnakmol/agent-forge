---
category: stack-selection
loading_priority: 3
tokens_estimate: 2400
keywords:
  - azure paas
  - app service
  - azure functions
  - logic apps
  - api management
  - azure sql
  - cosmos db
  - entra external id
  - event grid
  - service bus
  - blob storage
  - integration patterns
  - cost optimization
version: "1.0"
last_updated: "2026-03-21"
---

# Stack B: Low-Code + Azure PaaS

Stack B extends Stack A by adding Azure PaaS services for capabilities that exceed Power Platform limits. The Power Platform remains the primary UI and workflow layer; Azure PaaS handles custom APIs, advanced data, messaging, and integration scenarios that connectors and cloud flows cannot address.

The key architectural principle of Stack B: Power Platform is the front door (user-facing apps, workflows, portals), and Azure is the engine room (custom compute, data processing, integration backbone).

## Azure App Service

Azure App Service hosts custom web applications and APIs as managed PaaS workloads without managing infrastructure.

**Web apps:** Host custom front-end applications (React, Angular, Blazor) when canvas apps or model-driven apps cannot deliver the required UX. Common scenarios: customer-facing web portals with complex interactivity, real-time dashboards with SignalR, single-page applications with rich client-side logic.

**API apps:** Host custom REST APIs that Power Platform canvas apps or Power Automate flows call via custom connectors or HTTP actions. Use when: (1) the target system has no connector, (2) you need server-side business logic too complex for Power Automate, (3) you need to aggregate data from multiple sources into a single response.

**WebJobs:** Background processing tied to an App Service plan. Use for continuous or triggered background tasks: file processing, queue consumers, scheduled cleanup. For new workloads, prefer Azure Functions over WebJobs unless you need the App Service hosting model.

**Deployment slots:** Enable zero-downtime deployments with staging slots. Deploy to a staging slot, validate, then swap to production. Use slot settings for environment-specific configuration (connection strings, feature flags). Auto-swap from staging to production after health check passes.

**Scaling:** App Service plans support manual scaling (set instance count), autoscale rules (CPU > 70% for 5 minutes, add 1 instance), and per-app scaling (different apps on the same plan scale independently). For predictable traffic patterns, use scheduled autoscale rules.

## Azure Functions

Azure Functions provide serverless compute for event-driven workloads.

**Consumption plan:** Pay only for execution time. Cold start latency ranges from 1-10 seconds. Use for infrequent, latency-tolerant operations: webhook handlers, scheduled data processing, queue-triggered transformations.

**Premium plan:** Pre-warmed instances eliminate cold starts. Use for latency-sensitive APIs called by Power Apps or Power Automate that cannot tolerate multi-second delays. Premium also provides VNet integration for accessing resources on private networks.

**Durable Functions:** Orchestrate stateful workflows across multiple function calls. Patterns include:
- *Function chaining:* Execute steps sequentially with automatic retry. Use for multi-step data transformations.
- *Fan-out/fan-in:* Execute multiple functions in parallel, then aggregate results. Use for parallel processing (e.g., process 100 invoices simultaneously).
- *Async HTTP API:* Start long-running operation, return status URL, poll for completion. Use when Power Automate triggers a job that takes minutes to complete.
- *Monitor:* Periodically check external status until a condition is met. Use for waiting on external system approval or file availability.
- *Human interaction:* Pause workflow until a human approves or provides input. Use in combination with Power Automate approval flows.

**Event-driven triggers:** Functions trigger from: HTTP requests, queue messages (Service Bus, Storage Queue), blob uploads, Event Grid events, Cosmos DB change feed, Timer (CRON). Each trigger type has binding extensions that handle serialization and connection management automatically.

## Azure Logic Apps

Logic Apps provide enterprise integration workflows with a visual designer similar to Power Automate but with stronger enterprise integration capabilities.

**Standard (single-tenant):** Runs on App Service infrastructure. Supports VNet integration, private endpoints, and custom built-in connectors. Use Standard for production enterprise integrations that need network isolation and deterministic performance.

**Consumption (multi-tenant):** Pay-per-execution model similar to Power Automate. Use for lighter integration scenarios where cost efficiency matters more than network isolation.

**B2B and EDI:** Logic Apps includes native B2B capabilities: AS2, X12, EDIFACT message processing for supply chain integrations with trading partners. Integration accounts store partner profiles, agreements, schemas, and maps.

**When Logic Apps vs Power Automate:**
- Use Power Automate when: makers build and maintain the flow, Dataverse is the primary data source, flow is tied to a Power App.
- Use Logic Apps when: pro developers build and maintain, VNet integration required, B2B/EDI processing, complex XML/JSON transformations with Liquid or XSLT, ISE (isolated) deployment needed.

## Azure API Management (APIM)

APIM provides a unified API gateway for all custom APIs in the architecture.

**API gateway functions:** Request routing, SSL termination, request/response transformation, caching, rate limiting, IP filtering, JWT validation. Every custom API built on App Service or Functions should be fronted by APIM in production.

**Developer portal:** Auto-generated API documentation portal for internal and external developers. Enables API discovery, interactive testing, and API key self-service. Customize the portal with organization branding and content.

**Policies:** Apply cross-cutting concerns declaratively:
- *Inbound:* Validate JWT, check rate limit, transform request headers, set backend URL.
- *Backend:* Forward request, retry on failure, circuit breaker.
- *Outbound:* Transform response, filter headers, cache response.
- *On-error:* Return custom error response, log to Application Insights.

**Rate limiting and OAuth:** Protect APIs with rate limits per subscription key or per caller identity. Integrate with Entra ID (Azure AD) for OAuth 2.0 token validation. Issue subscription keys for external consumers via the developer portal.

**Tiers:** Consumption ($3.50/10K calls), Developer (non-production, $50/month), Basic ($150/month), Standard ($700/month), Premium ($2,800/month per unit, multi-region, VNet). Start with Consumption for low-traffic APIs; move to Standard/Premium for production enterprise APIs.

## Azure SQL Database

Azure SQL provides fully managed relational database with built-in intelligence.

**When to use:** Structured relational data that exceeds Dataverse query performance limits, complex reporting queries with joins across many tables, data warehouse staging, line-of-business data that does not belong in Dataverse (e.g., high-volume transactional data from external systems).

**Elastic pools:** Share resources across multiple databases. Use when you have many databases with varying, unpredictable usage patterns. Each database can burst to the pool maximum, but the pool cost is based on aggregate capacity.

**Geo-replication:** Create readable secondary databases in different Azure regions for disaster recovery and read-scale. Active geo-replication supports up to four readable secondaries. Auto-failover groups provide automatic failover with a single connection endpoint.

**Always-on (Business Critical tier):** Built-in high availability with same-region readable secondary replicas included in the price. Use for mission-critical workloads requiring RPO < 5 seconds and RTO < 30 seconds.

## Azure Cosmos DB

Cosmos DB provides multi-model, globally distributed database for specific scenarios.

**When to use over Azure SQL:** Schema-flexible documents, global distribution with single-digit millisecond reads, multi-model needs (document, graph, column-family, key-value), massive scale with guaranteed throughput.

**Consistency levels:** Strong, Bounded Staleness, Session (default and recommended for most apps), Consistent Prefix, Eventual. Session consistency gives read-your-writes within a session while allowing global distribution.

**Partitioning:** Choose partition key carefully; it determines data distribution and query efficiency. Good partition keys have high cardinality, even distribution, and are included in most queries. Bad partition keys cause hot partitions and throttling.

**Cost management:** Cosmos DB costs are dominated by RU/s (Request Units per second). Use serverless mode for development and low-traffic workloads. Use autoscale provisioned throughput for production with variable load. Use standard provisioned throughput for stable, predictable workloads.

## Azure AD B2C / Entra External ID

External identity management for customer-facing applications.

**When to use:** Power Pages needs external authentication beyond basic local auth, custom web apps need social login, B2B partner portals need federation with partner identity providers.

**Social logins:** Pre-built integration with Google, Facebook, Apple, LinkedIn, Twitter, Microsoft accounts. Configure in minutes through the Azure portal.

**Custom policies (Identity Experience Framework):** XML-based policy framework for complex identity scenarios: multi-factor authentication, progressive profiling, identity proofing, custom token enrichment. Use custom policies only when user flows (portal configuration) cannot meet the requirement.

## Azure Event Grid

Event Grid provides event-driven pub/sub messaging for reactive architectures.

**When to use:** Decoupling event producers from consumers, fan-out event distribution, reacting to Azure resource events (blob created, resource provisioned), custom application events.

**Topics and subscriptions:** System topics capture Azure resource events automatically. Custom topics accept events from your applications. Event subscriptions route events to handlers (Functions, Logic Apps, webhooks, Service Bus queues).

**Event domains:** Manage thousands of topics as a single entity for multi-tenant scenarios. Each tenant gets a topic within the domain; the domain provides unified authentication and authorization.

## Azure Service Bus

Service Bus provides enterprise messaging with queues and topics for reliable asynchronous communication.

**Message queues:** Point-to-point messaging. Producer sends message to queue; single consumer receives and processes. Use for: work distribution, load leveling, decoupling producers from consumers, guaranteed delivery.

**Topics and subscriptions:** Pub/sub messaging. Publisher sends to topic; multiple subscriptions with filters receive relevant messages. Use for: event broadcasting with subscriber-specific filtering, fan-out with selective consumption.

**Sessions:** Group related messages for ordered, exclusive processing. Use for: FIFO processing within a session, correlated message workflows (all messages for a single order processed sequentially).

**Dead-letter queue (DLQ):** Messages that cannot be processed after maximum retry attempts automatically move to the DLQ. Monitor DLQ depth as an operational metric. Process DLQ messages with a separate consumer for investigation and reprocessing.

**Transactions:** Service Bus supports local transactions: receive from one queue and send to another within a single atomic operation. Use for: reliable message forwarding, saga orchestration steps.

## Azure Blob Storage

Blob Storage manages unstructured data at scale.

**When to use:** Document storage (PDFs, images, videos), file uploads from Power Apps, report output storage, data lake staging, static website hosting, backup and archive.

**CDN integration:** Azure CDN caches blob content at edge locations globally. Use for: public static content (images, CSS, JS), large file downloads, video streaming.

**Lifecycle management:** Automatically transition blobs between tiers (Hot -> Cool -> Cold -> Archive) based on age. Configure deletion policies for regulatory compliance (retain for 7 years, then delete). Lifecycle policies run once per day.

## When Power Platform Hands Off to Azure

Decision criteria for introducing specific Azure services:

| Power Platform Limitation | Azure PaaS Resolution |
|---|---|
| Custom connector hits rate limits or needs capabilities beyond HTTP/REST | Build custom API on App Service; register as custom connector endpoint |
| Complex orchestration with retry, parallelism, compensation | Durable Functions for stateful workflow orchestration |
| High-throughput messaging (>6K req/5min) | Service Bus queues/topics for asynchronous processing; Event Grid for pub/sub |
| Advanced relational queries, cross-table joins, stored procedures | Azure SQL Database with direct connectivity from Functions or App Service |
| Global distribution, sub-10ms reads, schema flexibility | Cosmos DB with appropriate consistency level |
| External user authentication with social login | Entra External ID (B2C) for identity management |
| File processing (large documents, images, video) | Blob Storage with Functions trigger for processing pipeline |
| Unified API surface for multiple backends | API Management as gateway with policies |

## Integration Patterns Between Power Platform and Azure PaaS

**Pattern 1: Custom connector to App Service API.** Power Apps canvas app calls a custom connector that points to an App Service API behind APIM. The API performs complex logic, calls external systems, and returns results to the app. This is the most common Stack B pattern.

**Pattern 2: Power Automate to Azure Function.** A Power Automate flow triggers an Azure Function via HTTP action for compute-intensive processing (PDF generation, image analysis, complex calculations). The Function returns results to the flow, which continues with Power Platform actions (update Dataverse, send notification).

**Pattern 3: Event-driven integration.** Dataverse row change triggers a Power Automate flow that publishes a message to Service Bus. Azure Functions consume the message, process it (transform, enrich, validate), and write results to Azure SQL or Cosmos DB. Power BI connects directly to the Azure data tier for analytics.

**Pattern 4: Async long-running operations.** Power Apps submits a request to Durable Functions via HTTP. Durable Functions returns a status URL. Power Automate polls the status URL and notifies the user when processing completes. Use for: batch imports, report generation, multi-system updates.

## Cost Optimization

**Reserved instances:** Commit to 1-year or 3-year reserved capacity for App Service, Azure SQL, and Cosmos DB. Savings of 30-60% over pay-as-you-go. Use for production workloads with predictable baseline usage.

**Consumption vs Premium tiers:**
- Start with consumption/serverless tiers for new services during development and early production.
- Move to premium/provisioned tiers when usage patterns stabilize and consumption costs exceed premium pricing.
- Azure Functions: consumption plan is cheaper below ~3 million executions/month; premium plan is cheaper above.
- Cosmos DB: serverless is cheaper below ~500 RU/s average; provisioned is cheaper above.

**Dev/test pricing:** Use Azure Dev/Test pricing (available through Enterprise Agreement or Visual Studio subscriptions) for non-production environments. Savings of 40-60% on VMs and PaaS services.

**Right-sizing:** Review Azure Advisor recommendations monthly. Downsize over-provisioned App Service plans, SQL databases, and other resources. Use Azure Monitor metrics to identify services running below 20% utilization.

**Shut down non-production:** Use automation (Azure Automation, Logic Apps) to shut down dev/test environments outside business hours. Saves 65%+ on compute costs for non-production.
