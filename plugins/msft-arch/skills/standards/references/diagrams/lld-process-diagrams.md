---
category: design-documentation
loading_priority: 3
tokens_estimate: 2800
keywords:
  - process diagram
  - sequence diagram
  - state machine
  - data pipeline
  - error handling
  - authentication flow
  - Mermaid
  - implementation diagram
  - coding agent
  - low-level design
dependencies: [c4-diagram-guide, tech-design-spec, lld-template, integration-patterns]
version: "1.0"
last_updated: "2026-03-21"
---

# LLD Process Diagrams - Mermaid Templates

This reference provides comprehensive Mermaid.js templates for low-level process diagrams and component interaction flows. These diagrams bridge the gap between architecture documentation and actual implementation: a mid-level developer or coding agent should be able to look at these diagrams and understand exactly what to build, what calls what, what data flows where, and how errors are handled.

---

## 1. Component Interaction Flow Diagrams

These diagrams show method-level interactions between components. Every arrow is labeled with the action and payload shape. Both synchronous and asynchronous interactions are explicitly marked.

### Stack A: Canvas App --> Dataverse --> Power Automate --> External API

```mermaid
sequenceDiagram
    actor User
    participant App as Canvas App<br/>(Power Apps)
    participant DV as Dataverse
    participant Flow as Power Automate<br/>(Cloud Flow)
    participant ExtAPI as External API

    User->>App: Submit form (OrderRequest)
    App->>DV: Patch(Orders, {customer, items, total})
    DV-->>App: Created record (Order.Id)
    App-->>User: "Order submitted" confirmation

    Note over DV,Flow: Dataverse trigger fires on create
    DV->>Flow: Trigger: When row added (Order entity)
    Flow->>Flow: Compose: Transform to API payload
    Flow->>ExtAPI: HTTP POST /api/orders<br/>{orderId, customer, lineItems[]}
    ExtAPI-->>Flow: 200 OK {externalRef, estimatedDate}
    Flow->>DV: Update row: Order.ExternalRef, Order.Status="Confirmed"

    alt API returns error
        ExtAPI-->>Flow: 400/500 error response
        Flow->>Flow: Retry (3x with exponential backoff)
        alt Retry exhausted
            Flow->>DV: Update row: Order.Status="Failed"
            Flow->>Flow: Send failure notification (Teams/Email)
        end
    end
```

### Stack B: React App --> APIM --> Azure Function --> Azure SQL --> Service Bus

```mermaid
sequenceDiagram
    actor User
    participant SPA as React SPA<br/>(Static Web App)
    participant APIM as Azure API Management
    participant Func as Azure Function<br/>(.NET 8 Isolated)
    participant SQL as Azure SQL Database
    participant SB as Service Bus<br/>(Topic)
    participant Worker as Worker Function<br/>(Service Bus Trigger)

    User->>SPA: Click "Create Order"
    SPA->>APIM: POST /api/v1/orders<br/>Authorization: Bearer {token}<br/>{customerId, items[], notes}
    APIM->>APIM: Validate JWT (Entra ID)
    APIM->>APIM: Check rate limit (100 req/min)
    APIM->>Func: Forward request + subscription key

    Func->>SQL: BEGIN TRANSACTION
    Func->>SQL: INSERT INTO Orders (customerId, status, total)
    Func->>SQL: INSERT INTO OrderItems (orderId, sku, qty, price) x N
    SQL-->>Func: Rows inserted, orderId generated
    Func->>SQL: COMMIT

    Func->>SB: Publish to "order-events" topic<br/>{orderId, type: "OrderCreated", timestamp}
    SB-->>Func: Accepted (sequenceNumber)

    Func-->>APIM: 201 Created {orderId, status: "pending"}
    APIM-->>SPA: 201 Created (+ correlation-id header)
    SPA-->>User: Order confirmation screen

    Note over SB,Worker: Async processing
    SB->>Worker: Receive message (order-events/inventory-sub)
    Worker->>SQL: SELECT stock FROM Inventory WHERE sku IN (...)
    Worker->>SQL: UPDATE Inventory SET stock = stock - qty
    Worker->>SB: Publish {orderId, type: "InventoryReserved"}
```

### Stack C: Ingress --> API Container --> Service Container --> Database --> Message Broker

```mermaid
sequenceDiagram
    participant Ingress as NGINX Ingress<br/>(AKS)
    participant API as API Pod<br/>(Go / .NET)
    participant Svc as Domain Service Pod<br/>(Go / .NET)
    participant DB as PostgreSQL Flex<br/>(Azure)
    participant Redis as Redis Cache<br/>(Azure)
    participant Broker as RabbitMQ / Service Bus
    participant Worker as Worker Pod<br/>(KEDA-scaled)

    Ingress->>API: POST /api/v1/orders<br/>(TLS terminated, X-Request-Id injected)
    API->>Redis: GET cache:customer:{id}
    alt Cache hit
        Redis-->>API: Customer profile (JSON)
    else Cache miss
        API->>Svc: gRPC GetCustomer(customerId)
        Svc->>DB: SELECT * FROM customers WHERE id = $1
        DB-->>Svc: Customer row
        Svc-->>API: CustomerResponse (protobuf)
        API->>Redis: SET cache:customer:{id} EX 300
    end

    API->>Svc: gRPC CreateOrder(OrderRequest)
    Svc->>DB: INSERT INTO orders (...) RETURNING id
    DB-->>Svc: order_id
    Svc->>Broker: Publish order.created {orderId, items[]}
    Svc-->>API: CreateOrderResponse {orderId, status}

    API-->>Ingress: 201 Created {orderId}

    Note over Broker,Worker: KEDA scales workers based on queue depth
    Broker->>Worker: Consume order.created message
    Worker->>DB: Process order fulfillment logic
    Worker->>Broker: Publish order.fulfilled {orderId}
```

### Stack D: D365 Form --> Plugin --> External API --> Dual-Write --> F&O

```mermaid
sequenceDiagram
    actor User
    participant D365 as D365 CE<br/>(Sales/Service)
    participant Plugin as D365 Plugin<br/>(C# IPlugin)
    participant ExtAPI as External System API
    participant DW as Dual-Write<br/>(Runtime)
    participant FO as D365 Finance<br/>& Operations

    User->>D365: Save Opportunity (status = "Won")
    D365->>Plugin: Pre-Operation: ValidateOpportunity
    Plugin->>Plugin: Validate required fields, check business rules
    Plugin-->>D365: Validation passed (continue pipeline)

    D365->>Plugin: Post-Operation: OnOpportunityWon
    Plugin->>ExtAPI: POST /api/contracts<br/>{account, value, products[]}
    ExtAPI-->>Plugin: 201 {contractId}
    Plugin->>D365: Update: Opportunity.ContractRef = contractId

    Note over D365,DW: Dual-write syncs to F&O
    D365->>DW: Change detected on Account entity
    DW->>DW: Apply field mappings (CE --> F&O)
    DW->>FO: Upsert Customer record in F&O
    FO-->>DW: Sync confirmed

    alt Dual-write conflict
        DW->>DW: Conflict resolution (CE wins / F&O wins / manual)
        DW->>D365: Log conflict in Integration Journal
    end
```

---

## 2. Business Process Flow Diagrams

These diagrams show end-to-end business processes with decision points, parallel paths, and error handling. Swimlane-style subgraphs indicate which component handles each step.

### CRUD Operation with Validation

```mermaid
flowchart TD
    subgraph User["User Layer"]
        A[Submit Form] --> B{Client-side<br/>validation}
        B -->|Invalid| C[Show field errors]
        C --> A
        B -->|Valid| D[Send API request]
    end

    subgraph API["API Layer"]
        D --> E{Authenticate<br/>request}
        E -->|Unauthorized| F[Return 401]
        E -->|Authorized| G{Authorize<br/>action}
        G -->|Forbidden| H[Return 403]
        G -->|Permitted| I[Validate business rules]
        I -->|Invalid| J[Return 422 + error details]
        I -->|Valid| K[Persist to database]
    end

    subgraph Data["Data Layer"]
        K --> L{Constraint<br/>check}
        L -->|Violation| M[Return 409 Conflict]
        L -->|OK| N[Commit transaction]
        N --> O[Publish domain event]
    end

    O --> P[Return 201 Created]
    P --> Q[Display success]
```

### Approval Workflow with Escalation

```mermaid
flowchart TD
    A[Request Submitted] --> B[Determine Approver<br/>based on amount/type]
    B --> C{Amount > $50K?}
    C -->|Yes| D[Route to VP + Director]
    C -->|No| E{Amount > $10K?}
    E -->|Yes| F[Route to Director]
    E -->|No| G[Route to Manager]

    D --> H{Approval<br/>Decision}
    F --> H
    G --> H

    H -->|Approved| I[Update status = Approved]
    H -->|Rejected| J[Update status = Rejected<br/>Notify requestor with reason]
    H -->|No response<br/>48h| K{Escalation<br/>attempt}
    K -->|First escalation| L[Remind approver + notify skip-level]
    L --> H
    K -->|Second escalation<br/>96h| M[Auto-escalate to skip-level approver]
    M --> H
    K -->|Third escalation<br/>120h| N[Auto-reject + notify admin]

    I --> O[Trigger downstream process]
    J --> P[Archive request]
```

### Data Import / Processing Pipeline

```mermaid
flowchart TD
    A[File arrives in<br/>Blob Storage] --> B[Trigger: BlobCreated event]
    B --> C[Validate file format<br/>CSV/JSON/XML schema check]
    C -->|Invalid| D[Move to /rejected<br/>Send alert email]
    C -->|Valid| E[Parse file into records]
    E --> F[Batch records<br/>chunks of 1000]

    F --> G[For each batch]
    G --> H[Validate each record<br/>business rules]
    H --> I{Valid?}
    I -->|Yes| J[Upsert to database]
    I -->|No| K[Write to error log<br/>with row number + reason]
    J --> L{More batches?}
    K --> L
    L -->|Yes| G
    L -->|No| M[Generate import report]
    M --> N{Error rate<br/>> 5%?}
    N -->|Yes| O[Flag for manual review<br/>Send alert]
    N -->|No| P[Mark import complete<br/>Archive source file]
```

---

## 3. State Machine Diagrams

These diagrams model entities with complex lifecycles. Each transition includes the guard condition (in brackets) and the action performed.

### Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft: User creates order

    Draft --> Submitted: [All required fields valid]<br/>Lock editing
    Draft --> Cancelled: [User cancels]<br/>Release holds

    Submitted --> UnderReview: [Auto-assign reviewer]<br/>Notify reviewer
    Submitted --> Draft: [Reviewer returns for revision]

    UnderReview --> Approved: [Reviewer approves]<br/>Create fulfillment record
    UnderReview --> Rejected: [Reviewer rejects]<br/>Notify requestor with reason
    UnderReview --> Draft: [Reviewer requests changes]

    Approved --> Processing: [Fulfillment initiated]<br/>Reserve inventory
    Approved --> Cancelled: [Requestor cancels before processing]<br/>Release allocation

    Processing --> Completed: [All items fulfilled]<br/>Generate invoice
    Processing --> PartiallyFulfilled: [Some items fulfilled]<br/>Back-order remainder
    Processing --> Failed: [Fulfillment error]<br/>Trigger compensation

    PartiallyFulfilled --> Completed: [Remaining items fulfilled]
    PartiallyFulfilled --> Failed: [Cannot fulfill remainder]

    Completed --> Archived: [Retention period elapsed]<br/>Move to cold storage

    Failed --> Processing: [Retry approved]<br/>Re-reserve inventory
    Failed --> Cancelled: [Retry denied]<br/>Refund + release

    Cancelled --> [*]
    Archived --> [*]
    Rejected --> [*]
```

### Case Management Lifecycle

```mermaid
stateDiagram-v2
    [*] --> New: Case created (portal/email/phone)

    New --> Triaged: [Auto-classify by ML model]<br/>Assign priority + category
    New --> Triaged: [Manual classification]

    Triaged --> Assigned: [Match agent by skill/capacity]<br/>Notify assigned agent
    Triaged --> Escalated: [Priority = Critical AND no agent available]<br/>Page on-call team

    Assigned --> InProgress: [Agent accepts]<br/>Start SLA timer
    Assigned --> Triaged: [Agent rejects/unavailable]<br/>Re-route

    InProgress --> WaitingOnCustomer: [Agent requests info]<br/>Pause SLA timer
    InProgress --> WaitingOnThirdParty: [Depends on vendor/partner]<br/>Pause SLA timer
    InProgress --> Resolved: [Agent resolves]<br/>Stop SLA timer

    WaitingOnCustomer --> InProgress: [Customer responds]<br/>Resume SLA timer
    WaitingOnCustomer --> Resolved: [No response in 7 days]<br/>Auto-resolve

    WaitingOnThirdParty --> InProgress: [Third party responds]<br/>Resume SLA timer
    WaitingOnThirdParty --> Escalated: [SLA breach imminent]

    Escalated --> InProgress: [Escalation team takes over]

    Resolved --> Closed: [Customer confirms OR 48h no objection]
    Resolved --> InProgress: [Customer reopens within 48h]

    Closed --> [*]
```

---

## 4. Data Pipeline Flow Diagrams

These diagrams show data transformation steps with error handling branches.

### ETL Pipeline

```mermaid
flowchart LR
    subgraph Source["Source Systems"]
        S1[SQL Server<br/>On-Premises]
        S2[REST API<br/>SaaS Platform]
        S3[SFTP<br/>Partner Files]
    end

    subgraph Extract["Extract Layer"]
        E1[ADF Copy Activity<br/>Full/Incremental]
        E2[ADF REST Connector<br/>Paginated fetch]
        E3[ADF SFTP Connector<br/>File pickup]
    end

    subgraph Stage["Staging"]
        ST[Azure Data Lake<br/>raw/ zone<br/>Parquet format]
    end

    subgraph Transform["Transform Layer"]
        T1[Databricks / Synapse<br/>Data cleaning]
        T2[Schema validation<br/>Type casting]
        T3[Business rules<br/>Dedup, enrich, derive]
        T4[Data quality checks<br/>Completeness, accuracy]
    end

    subgraph Load["Load Layer"]
        L1[Azure SQL<br/>curated/ zone]
        L2[Dataverse<br/>via API]
        L3[Synapse Analytics<br/>serving/ zone]
    end

    subgraph Error["Error Handling"]
        ERR[Dead-letter store<br/>+ alert pipeline]
    end

    S1 --> E1 --> ST
    S2 --> E2 --> ST
    S3 --> E3 --> ST
    ST --> T1 --> T2 --> T3 --> T4
    T4 -->|Pass| L1
    T4 -->|Pass| L2
    T4 -->|Pass| L3
    T4 -->|Fail| ERR
```

### Real-Time Event Processing

```mermaid
flowchart LR
    subgraph Producers["Event Producers"]
        P1[IoT Devices]
        P2[Application Events]
        P3[D365 Webhooks]
    end

    subgraph Ingest["Ingestion"]
        EH[Azure Event Hub<br/>Partitioned by tenant]
    end

    subgraph Process["Stream Processing"]
        SA[Azure Stream Analytics<br/>or Databricks Streaming]
        V[Validate schema<br/>+ enrich from cache]
        R[Apply business rules<br/>windowed aggregations]
        RT[Route by event type]
    end

    subgraph Act["Actions"]
        A1[Hot path: Alert<br/>if threshold exceeded]
        A2[Warm path: Update<br/>operational dashboard]
        A3[Cold path: Archive<br/>to Data Lake]
    end

    P1 --> EH
    P2 --> EH
    P3 --> EH
    EH --> SA --> V --> R --> RT
    RT -->|Critical| A1
    RT -->|Operational| A2
    RT -->|Historical| A3
```

---

## 5. Error Handling Flow Diagrams

### API Error Handling with Retry and Circuit Breaker

```mermaid
sequenceDiagram
    participant Caller as Calling Service
    participant CB as Circuit Breaker
    participant Target as Target API

    Caller->>CB: Request to Target API
    alt Circuit CLOSED (normal operation)
        CB->>Target: Forward request
        alt Success (2xx)
            Target-->>CB: 200 OK
            CB->>CB: Reset failure counter
            CB-->>Caller: 200 OK
        else Transient error (500, 503, timeout)
            Target-->>CB: Error response
            CB->>CB: Increment failure counter
            alt Failure count < threshold (5)
                CB->>CB: Wait (exponential backoff: 1s, 2s, 4s, 8s, 16s)
                CB->>Target: Retry request
            else Failure count >= threshold
                CB->>CB: Transition to OPEN state<br/>Set timer (30 seconds)
                CB-->>Caller: 503 Service Unavailable<br/>(circuit open, not forwarding)
            end
        else Client error (4xx)
            Target-->>CB: 400/404/422
            CB-->>Caller: Forward error (no retry for client errors)
        end
    else Circuit OPEN (blocking requests)
        CB-->>Caller: 503 Service Unavailable<br/>(fast-fail, no attempt)
        Note over CB: After 30s timer expires,<br/>transition to HALF-OPEN
    else Circuit HALF-OPEN (testing recovery)
        CB->>Target: Allow single probe request
        alt Probe succeeds
            Target-->>CB: 200 OK
            CB->>CB: Transition to CLOSED<br/>Reset failure counter
            CB-->>Caller: 200 OK
        else Probe fails
            Target-->>CB: Error response
            CB->>CB: Transition back to OPEN<br/>Reset timer
            CB-->>Caller: 503 Service Unavailable
        end
    end
```

### Message Processing with Dead-Letter Queue

```mermaid
sequenceDiagram
    participant Queue as Service Bus Queue
    participant Proc as Message Processor
    participant DLQ as Dead-Letter Queue
    participant Store as Data Store
    participant Alert as Alert Pipeline

    Queue->>Proc: Receive message (PeekLock)
    Proc->>Proc: Deserialize + validate schema

    alt Valid message
        Proc->>Store: Process business logic + persist
        alt Processing succeeds
            Store-->>Proc: Success
            Proc->>Queue: Complete message (remove from queue)
        else Processing fails (transient)
            Store-->>Proc: Transient error
            Proc->>Queue: Abandon message (return to queue)<br/>DeliveryCount incremented
            Note over Queue: Message re-delivered after<br/>visibility timeout (30s)
        end
    else Invalid message (poison)
        Proc->>Queue: DeadLetter message<br/>Reason: "Schema validation failed"
    end

    Note over Queue: After MaxDeliveryCount (10)<br/>exceeded, auto dead-letter
    Queue->>DLQ: Move to dead-letter queue<br/>DeadLetterReason: "MaxDeliveryCountExceeded"

    Note over DLQ,Alert: Monitoring
    DLQ->>Alert: Alert: DLQ depth > 0
    Alert->>Alert: Page on-call + create incident
```

---

## 6. Authentication / Authorization Flow Diagrams

### OAuth2 Authorization Code Flow with Entra ID

```mermaid
sequenceDiagram
    actor User
    participant SPA as Browser / SPA
    participant Entra as Microsoft Entra ID
    participant API as Backend API
    participant Graph as Microsoft Graph

    User->>SPA: Navigate to application
    SPA->>Entra: Redirect to /authorize<br/>response_type=code<br/>scope=api://{clientId}/.default openid profile<br/>code_challenge={PKCE}
    Entra->>User: Login prompt (MFA if configured)
    User->>Entra: Credentials + MFA
    Entra-->>SPA: Redirect with authorization_code

    SPA->>Entra: POST /token<br/>grant_type=authorization_code<br/>code={auth_code}<br/>code_verifier={PKCE_verifier}
    Entra-->>SPA: {access_token, id_token, refresh_token}

    SPA->>API: GET /api/v1/data<br/>Authorization: Bearer {access_token}
    API->>API: Validate JWT signature (Entra public keys)
    API->>API: Check aud, iss, exp, roles/scopes

    opt API needs to call downstream service
        API->>Entra: POST /token<br/>grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer<br/>(On-Behalf-Of flow)
        Entra-->>API: {downstream_access_token}
        API->>Graph: GET /me/manager<br/>Authorization: Bearer {downstream_token}
        Graph-->>API: Manager profile
    end

    API-->>SPA: 200 OK {data}
    SPA-->>User: Render data
```

### Service-to-Service with Managed Identity

```mermaid
sequenceDiagram
    participant Func as Azure Function<br/>(System-assigned MI)
    participant IMDS as Azure IMDS<br/>(169.254.169.254)
    participant Entra as Microsoft Entra ID
    participant Target as Target Service<br/>(SQL / Key Vault / Storage)

    Note over Func: No credentials stored.<br/>Identity is infrastructure.

    Func->>IMDS: GET /metadata/identity/oauth2/token<br/>resource=https://{target-resource}<br/>api-version=2019-08-01
    IMDS->>Entra: Request token for managed identity<br/>ObjectId={MI object ID}
    Entra-->>IMDS: {access_token, expires_in}
    IMDS-->>Func: {access_token}

    Func->>Target: Request with Authorization: Bearer {token}
    Target->>Target: Validate token, check RBAC assignment
    Target-->>Func: Response

    Note over Func: Token cached by MSAL.<br/>Auto-refresh before expiry.
```

### D365 Plugin Impersonation

```mermaid
sequenceDiagram
    actor User as D365 User
    participant D365 as D365 Platform
    participant Plugin as Plugin (IPlugin)
    participant ExtSvc as External Service

    User->>D365: Update Account record
    D365->>Plugin: Execute(IServiceProvider)
    Plugin->>Plugin: Get IPluginExecutionContext<br/>context.UserId = {calling user}<br/>context.InitiatingUserId = {original user}

    alt Plugin runs as calling user (default)
        Plugin->>D365: IOrganizationService calls<br/>execute as context.UserId
    else Plugin runs as specific user (impersonation)
        Plugin->>Plugin: Create IOrganizationService<br/>with CallerId = {target user GUID}
        Plugin->>D365: IOrganizationService calls<br/>execute as impersonated user
    end

    Plugin->>ExtSvc: Call external API<br/>(uses app registration, NOT user identity)
    ExtSvc-->>Plugin: Response
    Plugin-->>D365: Continue pipeline
    D365-->>User: Save confirmed
```

---

## Diagram Quality Checklist

Before including any diagram in a `design.md`, verify it meets these standards:

| Check | Requirement |
|-------|-------------|
| Labeled arrows | Every arrow has a label describing the action or data being passed |
| Error paths | At least one error/exception path is shown (not just happy path) |
| Async markers | Asynchronous operations are clearly marked with notes or dashed lines |
| Technology names | Components use specific technology names (e.g., "Azure Function" not "serverless function") |
| Name consistency | Component names match exactly with the System Components table in `design.md` |
| Payload shapes | Request/response payload shapes are indicated (at minimum, key field names) |
| Authentication | Auth mechanism is shown where applicable (Bearer token, managed identity, API key) |
| Participant labels | Each participant includes both logical name and technology in the label |

---

## Usage Pattern for Coding Agents

When a coding agent receives a `design.md` file, it should consume the diagrams in this order:

1. **Component Interaction Flow** -- understand the call chain between components, method signatures, and payload shapes. This tells the agent what endpoints to implement and what each endpoint calls.

2. **Business Process Flow** -- understand the business logic, decision points, and branching paths. This tells the agent what conditional logic to implement.

3. **State Machine Diagrams** -- understand entity lifecycles and valid state transitions. This tells the agent what status fields to create and what transitions to enforce.

4. **API Contracts** (from `design.md`) -- get exact interface definitions, request/response schemas, and error formats for implementation.

5. **Data Models** (from `design.md`) -- get exact schema definitions, relationships, and constraints for database migrations.

6. **Error Handling Flow** -- understand retry policies, circuit breaker configuration, and dead-letter handling for resilience implementation.

7. **Auth Flow** -- understand the authentication and authorization approach for securing endpoints and service-to-service calls.

---

*Cross-references: `tech-design-spec.md`, `c4-diagram-guide.md`, `lld-template.md`, `integration-patterns.md`, `sub-agent-orchestration.md`*
