---
name: antipattern-controller-fat
description: The anti-pattern where Controller/Router owns business rules, transactions, or persistence instead of a use case.
tags: [antipattern, controller, layered]
stability: experimental
---

# Anti-pattern — Fat Controller

## Symptom

HTTP (or CLI) adapter methods contain domain conditionals, calculate totals, open
transactions, or call the Repository directly. The application service is missing
or is a pass-through.

```text
@PostMapping("/orders/{id}/cancel")
fun cancel(...) {
  val order = repo.find(id)           // controller -> repository
  if (order.status != OPEN) throw ...
  order.status = CANCELLED
  repo.save(order)
}
```

## Why it is bad

- Business rules leak into the delivery mechanism; a second adapter (batch, message) duplicates them.
- Layer Hard Rule broken: Controller must not call Repository directly.
- Hard to unit-test without spinning the web stack.
- Encourages anemic domain + procedural scripts in the edge.

## Why it happens

"Just one endpoint" shortcuts, generated CRUD controllers, and agents that map
OpenAPI operations straight onto handlers without a use-case layer.

## Correct shape

Controller/Router: parse → call one use case → map result/errors to HTTP.

```text
POST /orders/{id}/cancel
  -> CancelOrderUseCase.execute(command)
    -> order.cancel(reason)
    -> OrderRepository.save
```

## Detection

- Controller/Router imports a Repository (or ORM session) type.
- Handler bodies longer than a thin map/call/map; status/`if` business branches inside.
- No application-service / use-case type for the operation.
- Same rule appears in two controllers (REST + admin) with slight drift.

## Remediation

1. Extract a use-case method/class named as a business verb.
2. Move rules into the Aggregate; keep the adapter free of domain conditionals.
3. Inject the use case into the controller; remove direct repository calls.
4. Cover the use case with port fakes; keep controller tests for HTTP mapping only.

## Related

- `skills/oop/use-case-boundary.md` — application service role
- `AGENTS.md` Hard Rules — Controller must not call Repository
- `skills/antipatterns/anemic-domain.md` — often co-occurs
- `skills/antipatterns/repository-with-business-logic.md` — rules pushed the other way
