---
name: oop-domain-model
description: Core domain-model rules for designing an Aggregate and Value Object within one consistency boundary.
tags: [oop, ddd, domain-model]
stability: stable
---

# OOP — Domain Model

## When to use

Use this when deciding a domain object's responsibilities, state changes, and invariants.
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

## Event responsibility

An Aggregate may record a meaningful fact as part of accepted behavior.
Use `skills/oop/domain-events.md` for Domain vs Integration Event,
recording, dispatch, handlers, and external delivery.

## Decision criteria

| Question | Choice |
|---|---|
| Is there a state-change rule? | Aggregate behavior method |
| Is the value itself the meaning, with no identity? | Value Object |
| Did accepted behavior produce a fact others may react to? | Domain Event (`skills/oop/domain-events.md`) |
| Does a plain constructor bypass invariants? | Factory method |

## Prohibited

- Do not hide business rules in a controller, router, or application-service private method.
- Do not put Spring, JPA, FastAPI, SQLAlchemy, or HTTP types into domain objects.
- Do not blur domain behavior with CRUD names like `create`, `update`, `delete`.
- Do not modify several Aggregates within one transaction.
  (Details: `skills/oop/transaction-boundary.md`.)
