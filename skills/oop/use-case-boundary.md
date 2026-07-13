---
name: oop-use-case-boundary
description: Define the responsibility boundary of the application service and the Repository port to keep use cases thin.
tags: [oop, ddd, application, port]
stability: stable
---

# OOP — Use Case Boundary

## When to use

Use this when implementing a use case or wiring an external dependency.
Read it first when filling Use Case, Required Ports, and Transaction Boundary in Craft's OOP Contract.

## Application Service

- [ ] Express one use case as one class or one method.
- [ ] Name the method as a business verb. e.g., `placeOrder`, `cancelOrder`, `approvePayment`.
- [ ] Load or create domain objects and call their behavior methods.
- [ ] State the transaction boundary explicitly.
- [ ] Inject external dependencies via port interfaces.
- [ ] Take input as a command/request DTO and return an ID or result.
- [ ] Retrieve and publish domain events from the Aggregate.

## Repository Port

- [ ] Define the port per Aggregate.
- [ ] Keep only the methods you need. Do not mechanically create a full CRUD set.
- [ ] Reveal query intent in domain language. e.g., `findActiveByCustomer`, `findOverdueOrders`.
- [ ] Use domain objects and domain IDs as input/output.
- [ ] Do not expose framework types like JPA, SQLAlchemy, Pageable, or HTTP DTOs.
- [ ] Keep the implementation and mapper in infrastructure or an adapter.

## Flow

```text
Inbound adapter
  -> Application service
  -> Aggregate behavior
  -> Repository port
  -> Outbound adapter
```

## Prohibited

- Do not stack state-transition conditionals in the application service.
- Do not put place/cancel/ship/refund all into a single `OrderService`.
- Do not let the controller/router call the repository directly.
- Do not let the repository own transaction start/commit or external API calls.
- Do not expose a persistence model or API DTO on the port interface.
- Do not modify several Aggregates in one transaction — see `skills/oop/transaction-boundary.md`.
