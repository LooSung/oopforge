---
name: oop-domain-model
description: Core domain-model rules for designing an Aggregate, Value Object, and Domain Event within one boundary.
tags: [oop, ddd, domain-model]
stability: stable
---

# OOP — Domain Model

## When to use

Use this when deciding a domain object's responsibilities, state changes, invariants, and events.
Read it first when filling Aggregate Root, Domain Invariants, and State Transition in Craft's OOP Contract.

## Aggregate Root

- [ ] Define one boundary that keeps consistency within a single transaction.
- [ ] Allow external access only through the Aggregate Root.
- [ ] Create via an intention-revealing factory method. e.g., `Order.place(...)`, `User.register(...)`.
- [ ] Validate invariants on creation and on state change.
- [ ] Do not create public setters.
- [ ] Expose internal collections as a copy or an immutable view.
- [ ] Reference other Aggregates by ID, not by object.

## Value Object

- [ ] Make something a Value Object only when it has no identity and equality is by value.
- [ ] Validate on creation.
- [ ] When change is needed, return a new instance instead of mutating the existing one.
- [ ] Reduce primitive obsession. e.g., `Email` instead of `String email`.
- [ ] Do not share an API DTO or ORM entity as a domain Value Object.

## Domain Event

- [ ] Make an Event only for a meaningful fact that has already happened in the domain.
- [ ] Name it in past tense. e.g., `OrderPlaced`, `PaymentApproved`.
- [ ] Include the Aggregate ID and the time it occurred.
- [ ] Keep the payload to the minimum information needed.
- [ ] Record it inside the Aggregate; the application service retrieves and publishes it after saving.
- [ ] External message dispatch is owned by an adapter or infrastructure, not the domain.

## Decision criteria

| Question | Choice |
|---|---|
| Is there a state-change rule? | Aggregate behavior method |
| Is the value itself the meaning, with no identity? | Value Object |
| Is it a fact another boundary must know? | Domain Event |
| Does a plain constructor bypass invariants? | Factory method |

## Prohibited

- Do not hide business rules in a controller, router, or application-service private method.
- Do not put Spring, JPA, FastAPI, SQLAlchemy, or HTTP types into domain objects.
- Do not blur domain behavior with CRUD names like `create`, `update`, `delete`.
- Do not modify several Aggregates within one transaction.
  (Details: `skills/oop/transaction-boundary.md`.)
