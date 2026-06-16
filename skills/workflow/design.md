---
name: workflow-design
description: The step after Discovery. Draw use-case signatures and aggregate structure. No implementation yet.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Design

## When to use
When Discovery is done. Before Skeleton.
A stage that draws **signatures only** and never implements.

## Checklist
- [ ] List use cases per bounded context (verb names)
- [ ] Define input/output signatures for each use case
- [ ] State invariants per aggregate
- [ ] Define candidate domain events
- [ ] Define repository port signatures
- [ ] Abstract external dependencies as ports (interfaces)

## Output

Save to `docs/design.md`:

```markdown
# <Domain> — Design

## Use Cases (Ordering)
- `placeOrder(customerId, lines): OrderId`
- `cancelOrder(orderId, reason): void`
- `confirmPayment(orderId, paymentId): void`

## Aggregates

### Order (root)
- Identity: `OrderId`
- State: `status`, `lines`, `customerId`
- Invariants:
  - lines cannot be empty
  - cannot cancel in SHIPPED state
  - total = sum(line amounts)
- Methods (signatures only):
  - `place(...)`, `cancel(reason)`, `confirm()`

## Domain Events
- `OrderPlaced(orderId, customerId, total)`
- `OrderCancelled(orderId, reason)`
- `OrderConfirmed(orderId)`

## Ports (interfaces only)
- `OrderRepository.findById(id): Order?`
- `OrderRepository.save(order): void`
- `PaymentGateway.charge(orderId, amount): PaymentResult`
```

## Prohibited
- **No implementation code** — do not write method bodies. Signatures only.
- **No framework dependencies** — no `@Service`, `@Entity`, etc.
- **No DTO design** — that is the Skeleton/Implement stage.
- **No infinite abstraction** — one interface level. No Adapter pattern.

## Next step
After user approval -> `workflow-skeleton`
