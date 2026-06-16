---
name: workflow-discovery
description: The first step when starting a new domain/feature. Define the domain language and boundaries only, with no code.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Discovery

## When to use
When modeling a new domain or starting a large feature. The **first** stage.
Always do this before Design. Skipping it heads straight to the wrong abstraction.

## Checklist
- [ ] Define the ubiquitous language (glossary)
- [ ] Identify bounded contexts (there may be several)
- [ ] List core aggregate candidates per context
- [ ] Identify external systems/actors
- [ ] Non-functional requirements (performance, consistency model), one line each
- [ ] Explicitly write down unknowns (Open Questions)

## Output

Save to `docs/discovery.md` in this format:

```markdown
# <Domain> — Discovery

## Glossary
- **Order**: a customer's purchase intent. Changeable until payment.
- **OrderLine**: a single item + quantity within an Order.
- ...

## Bounded Contexts
1. **Ordering** — Order, OrderLine, Customer
2. **Payment** — Payment, Refund
3. **Fulfillment** — Shipment, Inventory

## Aggregate Candidates
- Ordering: `Order` (root), `OrderLine` (entity in aggregate)
- Payment: `Payment` (root)

## Actors / External
- Customer (web), AdminUser (back office)
- Payment Gateway (external), Inventory Service (internal)

## Non-Functional
- Payment is synchronous; fulfillment is eventual consistency
- Order creation within 200ms at p99

## Open Questions
- Partial refund policy?
- Whether to run a queue when inventory is short?
```

## Prohibited
- **No writing code** — not even signatures. Words and sentences only.
- **No framework mentions** — Spring/FastAPI/JPA do not appear yet.
- **No CRUD thinking** — instead of "update an Order", say "confirm the order", "cancel the order".
- **No empty Open Questions** — there can't be nothing unknown. State it.

## Next step
After user approval -> `workflow-design`
