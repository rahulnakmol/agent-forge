---
category: design-documentation
loading_priority: 3
tokens_estimate: 2600
keywords:
  - low-level design
  - LLD
  - component specification
  - API contract
  - data model
  - sequence diagram
  - deployment architecture
  - detailed design
version: "1.0"
last_updated: "2026-03-21"
---

# Low-Level Design (LLD) Document Template

This reference provides the complete structure and guidance for generating Low-Level Design documents. The LLD translates the HLD into implementation-ready specifications.

---

## Section 1: Document Control

| Field            | Value                          |
|------------------|--------------------------------|
| Document Title   | [Solution Name]: Low-Level Design |
| Version          | 1.0                            |
| Author           | [Architect Name]               |
| Reviewers        | [Reviewer 1], [Reviewer 2]     |
| Approval Status  | Draft / In Review / Approved   |
| Date Created     | [Date]                         |
| Last Updated     | [Date]                         |
| Related HLD      | [HLD Document Reference]       |

### Change History

| Version | Date | Author | Description of Change |
|---------|------|--------|-----------------------|
| 0.1     |      |        | Initial draft         |
| 1.0     |      |        | Approved baseline     |

---

## Section 2: Component Specifications

For each component identified in the HLD Container Diagram, provide the following specification.

### Component Specification Template

| Field | Value |
|-------|-------|
| Component Name | |
| Component Type | Web App / API / Function / Flow / Database / Message Broker |
| Technology | |
| Version | |
| Responsibilities | |
| Dependencies | |
| Scaling Characteristics | |

**Interface Contracts:**
- Inputs: data received, events consumed, triggers
- Outputs: data produced, events published, responses returned

**Configuration Parameters:**
- List all configurable settings with defaults and environment-specific overrides

### Per-Stack Component Templates

**Stack A: Power Platform:**
- **Power App Specification:** App type (canvas/model-driven), screens/views, data sources bound, security roles, offline capability
- **Power Automate Flow Design:** Trigger type, actions sequence, connectors used, error handling, run history retention
- **Dataverse Entity Design:** Table name, columns (name, type, required, default), relationships, business rules, calculated/rollup fields
- **Power BI Report:** Dataset source, refresh schedule, row-level security, key measures/visuals

**Stack B: Azure PaaS:**
- **App Service Configuration:** SKU, instance count, deployment slots, custom domains, SSL binding, health check path, auto-scale rules
- **Function App Specification:** Runtime, triggers and bindings per function, execution timeout, host.json settings, scaling behavior
- **Logic App Workflow Definition:** Trigger, actions, connectors, parallel branches, retry policies, run-after configuration
- **Azure SQL Configuration:** DTU/vCore tier, max size, geo-replication, backup retention, auditing, TDE

**Stack C: Containers:**
- **Container Specification:** Base image, Dockerfile reference, resource requests/limits (CPU, memory), readiness/liveness probes, environment variables, volume mounts
- **Kubernetes Manifest Overview:** Deployment replicas, service type, ingress rules, HPA configuration, PDB, namespace, network policies
- **Helm Chart Structure:** Chart values, dependencies, configurable parameters per environment

**Stack D: Dynamics 365:**
- **D365 Entity Customization:** Entity name, custom fields (name, type, requirement level), option sets, views, forms, business rules
- **Plugin Specification:** Registration step (message, entity, stage, mode), input/output parameters, execution pipeline, isolation mode
- **Workflow Definition:** Trigger conditions, steps, wait conditions, child workflows, scope

---

## Section 3: API Contracts

### API Endpoint Catalog

| Method | Path | Description | Auth | Rate Limit |
|--------|------|-------------|------|------------|
| GET    | /api/v1/resource | List resources | Bearer token | 100/min |
| POST   | /api/v1/resource | Create resource | Bearer token | 50/min |
| GET    | /api/v1/resource/{id} | Get resource by ID | Bearer token | 200/min |
| PUT    | /api/v1/resource/{id} | Update resource | Bearer token | 50/min |
| DELETE | /api/v1/resource/{id} | Delete resource | Bearer token | 20/min |

### Versioning Strategy
- URL path versioning: `/api/v1/`, `/api/v2/`
- Header versioning alternative: `api-version` header
- Deprecation policy: minimum 6-month notice, sunset header

### Request/Response Schema Format
Document schemas using JSON Schema or TypeScript interface notation. Include examples for each endpoint.

### Error Response Format (RFC 7807)

```json
{
  "type": "https://example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The 'email' field must be a valid email address.",
  "instance": "/api/v1/resource",
  "traceId": "00-abcdef1234567890-abcdef12-01"
}
```

### Rate Limiting and Throttling
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 response with `Retry-After` header
- Throttling tiers by client role/subscription

---

## Section 4: Data Models

### Entity-Relationship Diagram
Include a Mermaid ER diagram. Refer to `c4-diagram-guide.md` for ER diagram templates.

### Entity Specification Template

| Field | Data Type | Required | Default | Constraints | Description |
|-------|-----------|----------|---------|-------------|-------------|
|       |           |          |         |             |             |

### Indexes and Performance

| Index Name | Table | Columns | Type | Purpose |
|------------|-------|---------|------|---------|
|            |       |         | Clustered / Non-clustered / Unique | |

### Per-Stack Data Model Patterns

**Stack A: Dataverse:**
- Table design: standard vs. custom tables, table type (standard, activity, virtual)
- Relationships: 1:N, N:N, polymorphic lookups
- Calculated and rollup fields, auto-number columns
- Alternate keys for integration
- Business rules for field-level validation

**Stack B: Azure SQL / Cosmos DB:**
- Azure SQL: normalized schema, stored procedures, views, temporal tables
- Cosmos DB: container design, partition key selection strategy, RU estimation, indexing policy, consistency level
- Hybrid: SQL for transactional, Cosmos for high-scale read

**Stack C: Container Databases:**
- Database-per-service pattern
- Redis cache: key naming conventions, TTL policies, eviction strategy
- PostgreSQL/MySQL: schema per microservice, migration tooling

**Stack D: D365 Entities:**
- Standard vs. custom entities, entity ownership type
- Custom fields: naming convention (publisher prefix), data types
- Option sets: global vs. local, values and labels
- Entity relationships: system relationships, custom relationships

---

## Section 5: Sequence Diagrams

Include Mermaid sequence diagrams for all key flows. Refer to `c4-diagram-guide.md` for templates.

### Required Sequence Diagrams

1. **User Authentication Flow:** User -> Frontend -> Entra ID -> Token validation -> API access
2. **Core Business Process Flow:** End-to-end primary use case with all component interactions
3. **Integration/Data Sync Flow:** Source system -> Integration layer -> Target system with error handling
4. **Error Handling Flow:** Error occurrence -> Classification -> Retry/dead-letter -> Alert -> Resolution

### Per-Stack Sequence Patterns
- Stack A: User -> Canvas App -> Dataverse -> Power Automate -> External System
- Stack B: User -> App Service -> APIM -> Azure Function -> Service Bus -> Azure SQL
- Stack C: User -> Ingress -> API Gateway -> Service A -> Service Bus -> Service B -> Database
- Stack D: User -> D365 UI -> Plugin -> External API -> Dataverse update

---

## Section 6: Configuration Specifications

### Application Settings Catalog

| Setting Name | Description | Default | Dev | Test | Prod | Source |
|--------------|-------------|---------|-----|------|------|--------|
|              |             |         |     |      |      | App Config / Key Vault / Env Var |

### Feature Flags

| Flag Name | Description | Default | Enabled In |
|-----------|-------------|---------|------------|
|           |             | false   |            |

### Connection Strings
Document the format and Key Vault reference pattern. Never include actual credentials.

```
@Microsoft.KeyVault(SecretUri=https://{vault-name}.vault.azure.net/secrets/{secret-name}/{version})
```

### Key Vault References

| Secret Name | Purpose | Rotation Policy | Consumers |
|-------------|---------|-----------------|-----------|
|             |         | 90 days         |           |

---

## Section 7: Deployment Architecture

### CI/CD Pipeline Design

| Stage | Activities | Tools | Gate |
|-------|-----------|-------|------|
| Build | Compile, unit test, SAST scan, package | Azure DevOps / GitHub Actions | All tests pass, no critical findings |
| Test | Integration test, API test, performance test | | All tests pass |
| Staging | Deploy to staging, smoke test, UAT sign-off | | Manual approval |
| Production | Deploy to prod, smoke test, monitoring validation | | Manual approval |

### Environment Topology

| Environment | Purpose | Subscription | Resource Group | Region |
|-------------|---------|--------------|----------------|--------|
| Dev         | Development and unit testing | | | |
| Test        | Integration and QA testing | | | |
| Staging     | Pre-production validation | | | |
| Prod        | Production workload | | | |

### Infrastructure as Code
- Stack A: Power Platform solutions (managed/unmanaged), environment variables
- Stack B: Bicep templates or Terraform modules for Azure resources
- Stack C: Helm charts for Kubernetes, Bicep/Terraform for cluster infrastructure
- Stack D: D365 solutions, configuration migration data

### Deployment Strategy
- Blue-green: parallel environments, traffic switch (recommended for Stack B, C)
- Canary: gradual rollout with traffic splitting (recommended for Stack C)
- Rolling: sequential instance updates (suitable for Stack B)
- Solution import: managed solution promotion (Stack A, D)

---

## Section 8: Error Handling and Logging Strategy

### Error Classification

| Class | Description | Handling | Example |
|-------|-------------|----------|---------|
| Transient | Temporary failure, likely to succeed on retry | Automatic retry with backoff | Network timeout, 503 response |
| Permanent | Will not succeed on retry | Log, alert, return error to caller | 400 validation, 404 not found |
| Business Rule | Domain logic violation | Return structured error, no retry | Insufficient funds, duplicate entry |

### Retry Policies

| Scenario | Max Retries | Initial Delay | Backoff | Circuit Breaker Threshold |
|----------|-------------|---------------|---------|--------------------------|
| HTTP call | 3 | 1s | Exponential (2x) | 5 failures in 60s |
| Message processing | 5 | 5s | Exponential (2x) | 10 failures in 300s |
| Database connection | 3 | 500ms | Exponential (2x) | 3 failures in 30s |

### Structured Logging Format

```json
{
  "timestamp": "ISO8601",
  "level": "Information|Warning|Error|Critical",
  "correlationId": "guid",
  "service": "service-name",
  "operation": "operation-name",
  "message": "descriptive message",
  "properties": {},
  "exception": {}
}
```

### Correlation ID Propagation
- Generated at the entry point (API gateway / frontend)
- Passed via `X-Correlation-ID` header through all service calls
- Included in all log entries and message metadata
- Queryable in Application Insights using customDimensions

---

## Section 9: Monitoring and Alerting Design

### Metrics Catalog

| Metric Name | Source | Warning Threshold | Critical Threshold | Alert Action |
|-------------|--------|-------------------|-------------------|--------------|
| Response Time (P95) | App Insights | > 2s | > 5s | Email + Teams |
| Error Rate | App Insights | > 1% | > 5% | PagerDuty |
| CPU Usage | Azure Monitor | > 70% | > 90% | Auto-scale + Alert |
| Queue Depth | Service Bus | > 1000 | > 5000 | Email + Teams |
| Availability | Availability Tests | < 99.9% | < 99.5% | PagerDuty |

### Health Check Endpoints
- `/health`: basic liveness (returns 200 if process is running)
- `/health/ready`: readiness (checks dependencies: database, cache, external APIs)
- `/health/startup`: startup probe (checks initialization complete)

### Dashboard Design
- Application Insights: request rates, response times, failure rates, dependency calls
- Azure Dashboard: infrastructure metrics, resource health, cost tracking
- Power BI: business metrics, SLA reporting, trend analysis

### Alerting Rules and Escalation

| Severity | Response Time | Notification Channel | Escalation |
|----------|---------------|---------------------|------------|
| Critical (Sev 1) | 15 min | PagerDuty + Phone | Incident Manager at 30 min |
| High (Sev 2) | 1 hour | Teams + Email | Team Lead at 2 hours |
| Medium (Sev 3) | 4 hours | Email | Sprint backlog |
| Low (Sev 4) | Next sprint | Email | Backlog |
