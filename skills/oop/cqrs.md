---
name: oop-cqrs
description: Apply medium-level CQRS — split read (Query) from write (Command) while sharing the store — on layered/hexagonal. Includes entry criteria and prohibitions.
tags: [cqrs, oop, ddd, layered, hexagonal]
stability: experimental
---

# OOP — CQRS (medium)

## When to use

When read and write shapes differ enough that one model cannot serve both well.
**Default depth is medium**: split the Command/Query paths and DTOs but **share the store (DB)**.
Event sourcing or separate read/write databases is out of scope for this skill (a long-term item).

## Entry criteria (do not adopt unless at least one holds)

- [ ] The read model and write model differ greatly in shape (queries join/aggregate; writes are a single aggregate).
- [ ] Complex queries/reporting are polluting aggregate logic.
- [ ] Read-performance needs (cache/projection) justify the split.

If criteria are unmet, keep plain layered/hexagonal. **Unneeded CQRS is an anti-pattern.**

## Core rules

- **Command**: load the aggregate -> call a behavior method -> save. The domain keeps invariants.
- **Query**: do **not** load the aggregate. Read directly via a read-only model (ReadModel/DTO).
- The query side has **no side effects**. The command side **returns no read-shaped data** — an ID or void.

## Layered mapping

```text
order/
├── controller/
│   ├── OrderCommandController.java   # POST/PUT/DELETE
│   └── OrderQueryController.java     # GET
├── service/
│   ├── OrderCommandService.java      # aggregate orchestration
│   └── OrderQueryService.java        # ReadModel queries only
├── repository/
│   ├── OrderRepository.java          # aggregate save/load (command)
│   └── OrderQueryRepository.java     # ReadModel/projection queries (query)
├── domain/                           # Order aggregate (command only)
└── readmodel/                        # read-only DTOs like OrderSummary
```

- Write: `OrderCommandController -> OrderCommandService -> Order(domain) -> OrderRepository`
- Read: `OrderQueryController -> OrderQueryService -> OrderQueryRepository -> OrderSummary`

## Hexagonal mapping

- Expose the Command use case as a provided port (`PlaceOrder`) and go through the domain.
- Expose Query as a **separate provided port** (`OrderQueries`) that returns a read model, not domain objects.
- The Query's required port is a read-only query port, not the aggregate Repository.

```text
application/
├── provided/
│   ├── PlaceOrder.java          # command use case
│   └── OrderQueries.java        # query use case (returns read model)
├── required/
│   ├── OrderRepository.java     # command: persist the aggregate
│   └── OrderReadModelQuery.java # query: projection lookup
└── service/
    ├── PlaceOrderService.java
    └── OrderQueryService.java
```

## OOP Contract additions

For a CQRS task, add a line each to Craft's OOP Contract:

```markdown
Read/Write split: <command path | query path>
Read Model: <name of read-only DTO, where it is built>
Store: shared  # medium always shares
```

## Prohibited

- **Do not pull separate read/write DBs or event sourcing into medium** — a separate decision, separate work.
- **No loading the aggregate in a Query** — query directly via the read model.
- **A Command must not return a query DTO** — an ID or void.
- **No applying CQRS when entry criteria are unmet** — over-engineering.
- **Keep Command/Query from mixing in the same service class** — separation is the point.

## Related

- `skills/lang/backend-stack.md` — stack selection (CQRS is a variant)
- `skills/skeleton/backend-skeleton.md` — layer-folder standard
- `skills/oop/use-case-boundary.md` — use case / port boundary
- `AGENTS.md` Hard Rules — CQRS rules
