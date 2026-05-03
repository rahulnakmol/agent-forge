---
category: quality
loading_priority: 1
tokens_estimate: 600
keywords: [review, checklist, architecture-quality, scalability, operational-excellence]
---

# Architecture Review Checklist

When reviewing ANY design, evaluate every item below. Items that fail are flagged with specific remediation.

## Architecture Quality

- [ ] **Single Responsibility**: Each component does one thing well
- [ ] **Open/Closed**: Extensible without modification (plugin points, strategy pattern)
- [ ] **Dependency Inversion**: Abstractions, not concretions; domain does not reference infrastructure
- [ ] **Bounded Contexts**: Clear domain boundaries with explicit contracts at every seam
- [ ] **Immutability**: Data structures are immutable by default; mutation is isolated and justified
- [ ] **Pure Functions**: Business logic has no side effects; infrastructure is at the edges
- [ ] **Explicit Error Handling**: Result types for expected failures, exceptions only for the unexpected
- [ ] **Composability**: Components can be mixed, matched, and reused without modification
- [ ] **Testability**: Every component testable in isolation without infrastructure dependencies

## Scalability

- [ ] **Horizontal scaling**: Stateless services, externalized state (Redis, database, blob storage)
- [ ] **Eventual consistency**: Async where possible, synchronous only when business requires it
- [ ] **Event-driven**: Decouple producers from consumers; use Event Grid or Service Bus
- [ ] **Caching strategy**: What is cached, for how long, and how is it invalidated
- [ ] **Database scaling**: Read replicas, partitioning, CQRS where read/write patterns diverge

## Operational Excellence

- [ ] **Observability**: Structured logging, metrics, distributed tracing (Application Insights, OpenTelemetry)
- [ ] **Deployment**: Blue/green or canary deployments, zero-downtime, automated rollback
- [ ] **Resilience**: Circuit breakers, retries with exponential backoff, bulkhead isolation
- [ ] **Configuration**: Environment-based configuration, no secrets in code, Azure Key Vault for sensitive values
