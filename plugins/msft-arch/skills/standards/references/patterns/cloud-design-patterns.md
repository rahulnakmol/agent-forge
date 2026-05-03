# Cloud Design Patterns

**Source**: [Microsoft Azure Architecture Center: Cloud Design Patterns](https://learn.microsoft.com/azure/architecture/patterns/)

44 canonical patterns, organized by problem category. Each entry includes a one-line description, when to use it, when NOT to use it, and the Microsoft Learn URL.

---

## How to Apply Patterns

Patterns are named solutions to recurring problems: starting points, not blueprints. Every pattern involves trade-offs. Identify the primary problem, the constraints (latency budget, team skill, platform services), and the acceptable trade-offs. Patterns can be combined: Event Sourcing + CQRS + Saga is common for distributed commerce. Combining too many in one component creates accidental complexity.

---

## Data Management

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Cache-Aside** | Load data on demand into a cache from a data store | Read-heavy workloads; cache misses are acceptable | Data must always be consistent with the store; cache invalidation is complex | [learn.microsoft.com/azure/architecture/patterns/cache-aside](https://learn.microsoft.com/azure/architecture/patterns/cache-aside) |
| **CQRS** | Separate read and write models using distinct interfaces | Read and write workloads have very different scale requirements | Simple CRUD apps where separate models add complexity without benefit | [learn.microsoft.com/azure/architecture/patterns/cqrs](https://learn.microsoft.com/azure/architecture/patterns/cqrs) |
| **Event Sourcing** | Record all changes as an append-only sequence of events | Audit requirements; temporal queries; event-driven downstream consumers | High write throughput without event replay requirements; team lacks event-sourcing experience | [learn.microsoft.com/azure/architecture/patterns/event-sourcing](https://learn.microsoft.com/azure/architecture/patterns/event-sourcing) |
| **Index Table** | Create secondary indexes over frequently queried fields | NoSQL stores without native secondary indexes; hot query paths | RDBMS with built-in index support; use native indexes | [learn.microsoft.com/azure/architecture/patterns/index-table](https://learn.microsoft.com/azure/architecture/patterns/index-table) |
| **Materialized View** | Pre-compute views over data for specific query shapes | Complex aggregations that are too slow to compute at query time | Data changes frequently and cache staleness is unacceptable | [learn.microsoft.com/azure/architecture/patterns/materialized-view](https://learn.microsoft.com/azure/architecture/patterns/materialized-view) |
| **Sharding** | Partition a data store horizontally by a shard key | Single-node throughput or storage limits are approached | Queries must frequently cross shard boundaries (cross-shard joins are expensive) | [learn.microsoft.com/azure/architecture/patterns/sharding](https://learn.microsoft.com/azure/architecture/patterns/sharding) |
| **Static Content Hosting** | Serve static assets directly from blob storage | SPAs, images, JS/CSS bundles (anything that does not need server processing) | Content is personalized per request | [learn.microsoft.com/azure/architecture/patterns/static-content-hosting](https://learn.microsoft.com/azure/architecture/patterns/static-content-hosting) |
| **Valet Key** | Issue scoped tokens for direct client access to storage | Large file uploads/downloads; avoids proxying through your API | Fine-grained per-operation authorization is required beyond what the token can encode | [learn.microsoft.com/azure/architecture/patterns/valet-key](https://learn.microsoft.com/azure/architecture/patterns/valet-key) |

---

## Design and Implementation

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Ambassador** | Sidecar proxy handles cross-cutting network concerns on behalf of a service | Legacy services that cannot be modified; language-agnostic retry/auth/telemetry | Latency budget is extremely tight (sidecar adds a hop) | [learn.microsoft.com/azure/architecture/patterns/ambassador](https://learn.microsoft.com/azure/architecture/patterns/ambassador) |
| **Anti-Corruption Layer** | Translation façade between a modern system and a legacy domain model | Greenfield systems integrating with legacy APIs or databases | The legacy system will be decommissioned quickly; simpler direct integration may suffice | [learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer](https://learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer) |
| **Backends for Frontends** | Dedicated API backends per client type (mobile, web, IoT) | Different clients have substantially different data needs | One backend can serve all clients with reasonable field projection | [learn.microsoft.com/azure/architecture/patterns/backends-for-frontends](https://learn.microsoft.com/azure/architecture/patterns/backends-for-frontends) |
| **Compute Resource Consolidation** | Pack multiple small workloads onto shared compute | Cost optimization; low-complexity workloads | Workloads have conflicting resource profiles or security isolation requirements | [learn.microsoft.com/azure/architecture/patterns/compute-resource-consolidation](https://learn.microsoft.com/azure/architecture/patterns/compute-resource-consolidation) |
| **External Configuration Store** | Centralize configuration outside the deployment artifact | Multiple services share config; runtime config changes without redeployment | Single-service app with simple config (adds operational overhead) | [learn.microsoft.com/azure/architecture/patterns/external-configuration-store](https://learn.microsoft.com/azure/architecture/patterns/external-configuration-store) |
| **Pipes and Filters** | Decompose a processing task into a sequence of reusable, composable stages | ETL pipelines; document processing; stream transformations | Stages need to share complex state; shared state breaks the abstraction | [learn.microsoft.com/azure/architecture/patterns/pipes-and-filters](https://learn.microsoft.com/azure/architecture/patterns/pipes-and-filters) |
| **Sidecar** | Deploy supplementary components in a co-located process or container | Service Mesh telemetry, secrets injection, proxy, log forwarding | Monolithic deployment where container orchestration is unavailable | [learn.microsoft.com/azure/architecture/patterns/sidecar](https://learn.microsoft.com/azure/architecture/patterns/sidecar) |
| **Strangler Fig** | Migrate a legacy system by incrementally replacing its surface area | Long-running migrations that cannot be done in one cutover | Systems with tight coupling where routes cannot be split incrementally | [learn.microsoft.com/azure/architecture/patterns/strangler-fig](https://learn.microsoft.com/azure/architecture/patterns/strangler-fig) |
| **Edge Workload Configuration** | Manage configuration for distributed edge workloads as versioned operational events | IoT and edge fleets with many nodes requiring synchronized, auditable config | Centralized cloud-only deployments where standard config stores suffice | [learn.microsoft.com/azure/architecture/patterns/edge-workload-configuration](https://learn.microsoft.com/azure/architecture/patterns/edge-workload-configuration) |
| **Deployment Stamps** | Release versioned copies of the app+infrastructure as controlled units | Multi-region rollouts; A/B deployments; tenant isolation | Low-complexity single-region apps (adds infrastructure overhead) | [learn.microsoft.com/azure/architecture/patterns/deployment-stamp](https://learn.microsoft.com/azure/architecture/patterns/deployment-stamp) |

---

## Messaging

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Asynchronous Request-Reply** | Decouple long-running backend work from a synchronous front-end call | Backend processing exceeds a client's connection timeout | Processing is fast enough to return synchronously | [learn.microsoft.com/azure/architecture/patterns/asynchronous-request-reply](https://learn.microsoft.com/azure/architecture/patterns/asynchronous-request-reply) |
| **Choreography** | Each service reacts to events and decides its own participation | Loosely coupled services that evolve independently | Multiple services need tight coordination with rollback; use Orchestration/Saga instead | [learn.microsoft.com/azure/architecture/patterns/choreography](https://learn.microsoft.com/azure/architecture/patterns/choreography) |
| **Claim Check** | Split large messages into a pointer (claim) and the payload stored externally | Messages exceed broker size limits (Service Bus: 256 KB standard / 100 MB premium) | Messages are small; added indirection is unnecessary complexity | [learn.microsoft.com/azure/architecture/patterns/claim-check](https://learn.microsoft.com/azure/architecture/patterns/claim-check) |
| **Competing Consumers** | Multiple workers process messages from a shared queue in parallel | Scale-out message processing; order not required | Messages must be processed in strict order per entity; use Sequential Convoy | [learn.microsoft.com/azure/architecture/patterns/competing-consumers](https://learn.microsoft.com/azure/architecture/patterns/competing-consumers) |
| **Messaging Bridge** | Intermediary translates between incompatible messaging protocols | Integrating systems using different brokers (e.g., AMQP ↔ MQTT) | All systems can be migrated to a common protocol | [learn.microsoft.com/azure/architecture/patterns/messaging-bridge](https://learn.microsoft.com/azure/architecture/patterns/messaging-bridge) |
| **Priority Queue** | Route high-priority messages to dedicated consumers for faster processing | SLA differentiation; premium-tier request handling | All messages have equal priority | [learn.microsoft.com/azure/architecture/patterns/priority-queue](https://learn.microsoft.com/azure/architecture/patterns/priority-queue) |
| **Publisher-Subscriber** | Broadcast events to multiple consumers without coupling sender to receiver | Fan-out notifications; domain events; audit log feeds | Consumer list is fixed and small; direct call is clearer | [learn.microsoft.com/azure/architecture/patterns/publisher-subscriber](https://learn.microsoft.com/azure/architecture/patterns/publisher-subscriber) |
| **Queue-Based Load Leveling** | Buffer requests in a queue to smooth traffic spikes | Bursty ingestion; downstream processing that cannot autoscale fast enough | End-to-end latency SLA cannot absorb queue depth delay | [learn.microsoft.com/azure/architecture/patterns/queue-based-load-leveling](https://learn.microsoft.com/azure/architecture/patterns/queue-based-load-leveling) |
| **Saga** | Coordinate distributed transactions across microservices with compensating actions | Multi-service transactions without a distributed ACID transaction manager | Operations can be wrapped in a single ACID transaction; prefer that simpler approach | [learn.microsoft.com/azure/architecture/patterns/saga](https://learn.microsoft.com/azure/architecture/patterns/saga) |
| **Sequential Convoy** | Process related messages in order without blocking other groups | Order-sensitive operations per entity (e.g., all events for customer X in order) | Ordering is not required; use Competing Consumers for throughput | [learn.microsoft.com/azure/architecture/patterns/sequential-convoy](https://learn.microsoft.com/azure/architecture/patterns/sequential-convoy) |

---

## Reliability

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Bulkhead** | Isolate components into pools so one failure does not cascade | Critical paths that must survive partial failure | All paths have equal criticality and shared resources are tightly constrained | [learn.microsoft.com/azure/architecture/patterns/bulkhead](https://learn.microsoft.com/azure/architecture/patterns/bulkhead) |
| **Circuit Breaker** | Stop calling a failing dependency until it recovers | Downstream service has transient or prolonged failures | Downstream is in the same process or on the same host | [learn.microsoft.com/azure/architecture/patterns/circuit-breaker](https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker) |
| **Compensating Transaction** | Undo the effects of a sequence of steps if a later step fails | Eventually consistent operations spanning multiple services | Operations are idempotent and can simply be retried | [learn.microsoft.com/azure/architecture/patterns/compensating-transaction](https://learn.microsoft.com/azure/architecture/patterns/compensating-transaction) |
| **Geode** | Deploy backend nodes globally; any node can handle any region's traffic | Ultra-low-latency, globally distributed read-heavy workloads | Data sovereignty regulations prevent cross-region data replication | [learn.microsoft.com/azure/architecture/patterns/geodes](https://learn.microsoft.com/azure/architecture/patterns/geodes) |
| **Health Endpoint Monitoring** | Expose a `/health` endpoint for external probes | All externally deployed services (required for load balancer integration) | In-process libraries where health is inferred by process liveness | [learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring](https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring) |
| **Leader Election** | Elect one instance to coordinate a distributed task | Scheduled jobs, distributed locks, singleton workers in a scaled-out deployment | Only one instance is ever deployed; no election needed | [learn.microsoft.com/azure/architecture/patterns/leader-election](https://learn.microsoft.com/azure/architecture/patterns/leader-election) |
| **Rate Limiting** | Throttle consumption to avoid overwhelming downstream resources | Protecting shared resources from bursty callers | All callers are trusted internal services with bounded rate | [learn.microsoft.com/azure/architecture/patterns/rate-limiting-pattern](https://learn.microsoft.com/azure/architecture/patterns/rate-limiting-pattern) |
| **Retry** | Automatically re-attempt transient failures with backoff | Calls to external services with known transient failure modes | Failures are not transient (bad input, authorization failure); retry wastes time | [learn.microsoft.com/azure/architecture/patterns/retry](https://learn.microsoft.com/azure/architecture/patterns/retry) |
| **Scheduler Agent Supervisor** | Orchestrate multi-step distributed workflows with monitoring and recovery | Long-running workflows that need step-level visibility and recovery | Short, fast operations; scheduler overhead exceeds the benefit | [learn.microsoft.com/azure/architecture/patterns/scheduler-agent-supervisor](https://learn.microsoft.com/azure/architecture/patterns/scheduler-agent-supervisor) |

---

## Security

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Federated Identity** | Delegate authentication to an external identity provider | SSO, social login, enterprise identity; avoid building your own auth | The external IdP cannot meet your compliance or availability requirements | [learn.microsoft.com/azure/architecture/patterns/federated-identity](https://learn.microsoft.com/azure/architecture/patterns/federated-identity) |
| **Gatekeeper** | Front-end proxy validates and sanitizes all requests before passing to backend | Hardening backend services that cannot be directly exposed | The gateway becomes a single point of failure without HA design | [learn.microsoft.com/azure/architecture/patterns/gatekeeper](https://learn.microsoft.com/azure/architecture/patterns/gatekeeper) |
| **Quarantine** | Validate external assets meet quality standards before consuming them | Third-party data ingestion; file upload pipelines; supply chain security | All data originates internally and is already trusted | [learn.microsoft.com/azure/architecture/patterns/quarantine](https://learn.microsoft.com/azure/architecture/patterns/quarantine) |

---

## Performance and Scalability

| Pattern | One-line description | Use when | Avoid when | URL |
|---|---|---|---|---|
| **Gateway Aggregation** | Combine multiple backend calls into a single client-facing request | Mobile clients with limited bandwidth; chatty microservice APIs | Backends are fast and client can afford multiple calls | [learn.microsoft.com/azure/architecture/patterns/gateway-aggregation](https://learn.microsoft.com/azure/architecture/patterns/gateway-aggregation) |
| **Gateway Offloading** | Delegate cross-cutting concerns (auth, certs, rate limits) to the gateway | Common capabilities shared across many backend services | Each service has unique policy requirements the gateway cannot generalize | [learn.microsoft.com/azure/architecture/patterns/gateway-offloading](https://learn.microsoft.com/azure/architecture/patterns/gateway-offloading) |
| **Gateway Routing** | Route to multiple backends from a single endpoint | Migrating backends; multi-version APIs; blue/green routing | Only one backend exists; a gateway adds latency without benefit | [learn.microsoft.com/azure/architecture/patterns/gateway-routing](https://learn.microsoft.com/azure/architecture/patterns/gateway-routing) |
| **Throttling** | Control resource consumption by applying limits per caller, tenant, or globally | Multi-tenant SaaS; protecting expensive downstream APIs | Callers are fully trusted and resource exhaustion is not a concern | [learn.microsoft.com/azure/architecture/patterns/throttling](https://learn.microsoft.com/azure/architecture/patterns/throttling) |

---

## Trade-offs and Exceptions

- **Event Sourcing is not a default**: Adds storage cost, replay complexity, and schema versioning burden. Use only when audit history or temporal queries are explicit requirements.
- **CQRS without Event Sourcing**: Separate read models work with a conventional RDBMS via views or projections. Event Sourcing is not required.
- **Circuit Breaker + Retry**: Use both together. Retry for transient faults; Circuit Breaker to stop calling once the failure rate threshold is breached. Polly (for .NET) implements both.
- **Saga complexity**: Every compensating action must be tested. Keep sagas short: a 6-step saga has 6 rollback paths.
- **Gateway proliferation**: Adopting BFF, Gateway Aggregation, Gateway Offloading, and Gateway Routing simultaneously risks sprawl. Evaluate Azure API Management as a unified plane before building custom gateways.
