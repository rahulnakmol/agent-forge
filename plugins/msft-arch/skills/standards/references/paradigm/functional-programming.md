---
category: paradigm
loading_priority: 2
tokens_estimate: 800
keywords: [functional-programming, immutability, pure-functions, result-types, composition, pattern-matching]
---

# Functional Programming Paradigm

The Microsoft Architecture suite applies functional programming as the default paradigm for business logic. OOP is reserved for framework integration and infrastructure concerns.

## Core Principles

**Immutability first**: Use records (C#), `readonly`/`const` (TypeScript), frozen dataclasses (Python). Mutable state is a bug waiting to happen. If you need mutation, isolate it at the edges.

**Pure functions**: Business logic as pure functions. Inputs in, outputs out, no side effects. A function that reads from a database is not business logic; it is infrastructure. Separate them.

**Composition**: Small functions composed into pipelines. Use the pipe operator, method chaining, or railway-oriented programming. A 200-line function is a design failure.

**Pattern matching**: Discriminated unions + pattern matching over if/else chains. Make illegal states unrepresentable.

**Result types**: `Result<T, Error>` over try/catch for expected failures. Exceptions are for exceptional (unexpected) situations. A validation failure is not exceptional.

**Higher-order functions**: `map`, `filter`, `reduce` for data transformation. Loops are for infrastructure; pipelines are for domain logic.

**Algebraic data types**: Model domain states explicitly. `OrderState = Draft | Submitted | Approved | Rejected` is better than a string field and a prayer.

## C# Pattern

```csharp
public sealed record CreateOrderCommand(CustomerId Id, IReadOnlyList<OrderLine> Lines);
public sealed record OrderCreated(OrderId Id, Money Total, DateTimeOffset CreatedAt);

public static Result<OrderCreated, OrderError> CreateOrder(
    CreateOrderCommand cmd,
    IReadOnlyList<Product> catalog)
    => ValidateLines(cmd.Lines, catalog)
        .Bind(lines => CalculateTotal(lines))
        .Map(total => new OrderCreated(OrderId.New(), total, DateTimeOffset.UtcNow));
```

## TypeScript Pattern

```typescript
type OrderState =
  | { kind: 'draft'; lines: ReadonlyArray<OrderLine> }
  | { kind: 'submitted'; total: Money; submittedAt: Date }
  | { kind: 'approved'; approvedBy: UserId };

const processOrder = (state: OrderState): Result<OrderState, OrderError> =>
  match(state)
    .with({ kind: 'draft' }, handleDraft)
    .with({ kind: 'submitted' }, handleSubmission)
    .exhaustive();
```

## When to Apply

- ALL business logic: pure functions with typed inputs/outputs
- Data transformations: pipelines over imperative loops
- State management: discriminated unions over string enums
- Error handling: Result types for expected failures
- Domain modeling: immutable records/value objects
