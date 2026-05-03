# Technical Story Generation

## Overview

Technical user stories represent work that is necessary for the system to function
but does not directly deliver user-facing value. These stories are typically NOT
explicitly stated in the PRD but are inferred from the features, non-functional
requirements, and architectural context.

This document describes how to identify, generate, and estimate technical stories.

---

## When to Create Technical Stories

Create a technical user story when:

1. The work is infrastructure, tooling, or plumbing that enables user-facing features.
2. The work has no direct user interaction or visible UI change.
3. The work is driven by non-functional requirements (performance, security,
   reliability, scalability).
4. The work involves system-to-system integration with no user-facing component.
5. The work is a prerequisite for multiple user stories (shared foundation).

Do NOT create a separate technical story when:

1. The technical work is small and naturally part of a user story (e.g., adding a
   database column as part of implementing a feature).
2. The technical work cannot be delivered or validated independently.
3. The technical work has no value without the user story it supports.

### Rule of Thumb

If the technical work takes less than 2 story points AND is tightly coupled to a
single user story, include it in that user story. If it takes 3+ points OR serves
multiple user stories, create a separate technical story.

---

## Technical Story Categories

### 1. API Contract Definition and Implementation

Generate these when the PRD implies new APIs or services.

**Signals in the PRD:**
- "The system will expose..." or "integrates with..."
- Multiple features accessing the same data or capability
- Mobile and web clients needing the same functionality

**Story Templates:**
```
As a backend developer, I want to define the REST API contract for [feature]
so that frontend and backend teams can work in parallel.

As a backend developer, I want to implement the [resource] API endpoints
so that client applications can [perform action].

As a backend developer, I want to create API versioning strategy
so that we can evolve APIs without breaking existing clients.
```

**Typical Estimate:** 3-8 story points per API resource

### 2. Data Migration and Schema Design

Generate these when the PRD implies new data models or changes to existing data.

**Signals in the PRD:**
- "Migrate from [old system]..." or "consolidate data from..."
- New entities or attributes not in the current schema
- Data transformation or cleanup requirements

**Story Templates:**
```
As a data engineer, I want to design the database schema for [feature domain]
so that all required data can be stored and queried efficiently.

As a data engineer, I want to create migration scripts for [data source]
so that existing data is available in the new system.

As a data engineer, I want to implement data validation rules for [entity]
so that data integrity is maintained during migration.
```

**Typical Estimate:** 5-13 story points depending on data volume and complexity

### 3. Infrastructure Setup and Configuration

Generate these when the PRD implies new environments, services, or infrastructure.

**Signals in the PRD:**
- New deployment targets (e.g., "available in EU region")
- Scalability requirements (e.g., "support 10,000 concurrent users")
- New service dependencies (e.g., "integrate with message queue")

**Story Templates:**
```
As a DevOps engineer, I want to provision [environment] infrastructure
so that the [feature] can be deployed and tested.

As a DevOps engineer, I want to configure [service] (e.g., Redis, Kafka,
Elasticsearch) so that [feature] has the required runtime dependencies.

As a DevOps engineer, I want to set up infrastructure-as-code for [component]
so that environments can be reproducibly created and destroyed.
```

**Typical Estimate:** 3-8 story points per environment/service

### 4. Security Hardening

Generate these when the PRD involves authentication, authorization, PII, or
compliance requirements.

**Signals in the PRD:**
- "Authenticated users can..." or "role-based access..."
- PII handling (names, emails, payment info)
- Compliance mentions (GDPR, HIPAA, SOC2, PCI-DSS)

**Story Templates:**
```
As a security engineer, I want to implement authentication using [method]
so that only authorized users can access the system.

As a security engineer, I want to configure role-based access control
so that users can only perform actions appropriate to their role.

As a security engineer, I want to implement data encryption at rest and
in transit so that PII is protected per [compliance standard].

As a security engineer, I want to set up audit logging for [sensitive actions]
so that we have a tamper-proof record for compliance.
```

**Typical Estimate:** 5-13 story points per security domain

### 5. Monitoring and Observability

Generate these for any production-grade feature. If the PRD mentions SLAs,
uptime requirements, or operational concerns, these are mandatory.

**Signals in the PRD:**
- SLA or uptime requirements (e.g., "99.9% availability")
- "Alerting when..." or "dashboard showing..."
- Performance benchmarks

**Story Templates:**
```
As a DevOps engineer, I want to set up application performance monitoring
so that we can detect and diagnose performance issues.

As a DevOps engineer, I want to create health check endpoints for [service]
so that load balancers and orchestrators can manage availability.

As a DevOps engineer, I want to configure alerting for [critical metrics]
so that the on-call team is notified of production issues.

As a DevOps engineer, I want to create an operational dashboard for [feature]
so that the team can monitor system health in real time.
```

**Typical Estimate:** 3-5 story points per service

### 6. CI/CD Pipeline Configuration

Generate these when the PRD implies a new service, new deployment target, or
changes to the deployment topology.

**Signals in the PRD:**
- New microservice or application
- New deployment target (mobile app, new cloud region)
- Blue-green or canary deployment requirements

**Story Templates:**
```
As a DevOps engineer, I want to create a CI pipeline for [service]
so that code changes are automatically built and tested.

As a DevOps engineer, I want to configure CD pipeline for [environment]
so that validated builds are automatically deployed.

As a DevOps engineer, I want to set up feature flag infrastructure
so that incomplete features can be safely merged to main.
```

**Typical Estimate:** 3-5 story points per pipeline

### 7. Performance Testing

Generate these when the PRD specifies performance requirements or high-traffic
scenarios.

**Signals in the PRD:**
- Response time requirements (e.g., "page load under 2 seconds")
- Throughput requirements (e.g., "process 1000 transactions/second")
- Concurrent user targets

**Story Templates:**
```
As a QA engineer, I want to create load test scripts for [feature]
so that we can validate performance under expected traffic.

As a QA engineer, I want to establish performance baselines for [endpoints]
so that regressions can be detected automatically.

As a QA engineer, I want to configure performance test infrastructure
so that load tests can run as part of the CI/CD pipeline.
```

**Typical Estimate:** 3-8 story points per test suite

### 8. Integration Setup

Generate these when the PRD requires integration with third-party services or
internal systems.

**Signals in the PRD:**
- Third-party service names (Stripe, Twilio, SendGrid, etc.)
- "Integrate with [internal system]"
- OAuth, SSO, or federated identity requirements

**Story Templates:**
```
As a developer, I want to set up the [third-party] SDK and configuration
so that the application can interact with [service].

As a developer, I want to create an abstraction layer for [third-party]
so that the integration can be swapped or mocked for testing.

As a developer, I want to implement retry and circuit-breaker logic for
[integration] so that the application degrades gracefully on failures.
```

**Typical Estimate:** 3-8 story points per integration

---

## Technical Story Estimation Rules

| Complexity Factor                | Points Adjustment         |
|----------------------------------|---------------------------|
| Well-known technology            | Base estimate             |
| New technology (team has no exp) | +3-5 points               |
| Multiple environments            | +2-3 points per env       |
| Compliance/audit requirements    | +3-5 points               |
| Data migration > 1M records      | +5-8 points               |
| Cross-team dependency            | +2-3 points               |

---

## Assignment to Features

Technical stories are children of Features, just like user stories. Assign each
technical story to the feature it most directly supports:

- If a tech story supports a single feature, it is a child of that feature.
- If a tech story supports multiple features (e.g., shared auth), assign it to the
  feature that is most foundational or will be built first.
- If a tech story is truly cross-cutting (e.g., CI/CD pipeline for the whole
  project), assign it to the most architectural feature or create a dedicated
  "Platform Foundation" feature under the appropriate epic.

---

## Completeness Checklist

For each feature in the backlog, verify these technical story categories:

- [ ] API contracts defined (if feature involves APIs)
- [ ] Database schema changes identified (if feature involves data)
- [ ] Infrastructure provisioned (if feature needs new services)
- [ ] Security controls in place (if feature handles sensitive data)
- [ ] Monitoring configured (if feature is production-critical)
- [ ] CI/CD pipeline updated (if feature introduces new components)
- [ ] Performance tests created (if feature has SLA requirements)
- [ ] Third-party integrations set up (if feature uses external services)
