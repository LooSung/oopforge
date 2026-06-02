# Order Java Layered Example

**Spring Boot 3-tier (Controller → Service → Repository)** reference for OOPforge — same `place-order` flow as [`order-java`](../order-java/) (hexagonal).

Uses in-memory persistence (no database). OpenAPI via **springdoc** (`/swagger-ui`, `/v3/api-docs`).

## What to look at

| Layer | Path | Role |
|---|---|---|
| Controller | `order/controller/OrderController.java` | REST + DTO mapping |
| Service | `order/service/OrderService.java` | Use case orchestration |
| Repository | `order/repository/` | Persistence port + in-memory impl |
| Domain | `order/domain/Order.java` | Aggregate — framework import 0 |

## Run

```bash
cd examples/order-java-layered
./gradlew test
./gradlew bootRun
```

```bash
curl -X POST http://localhost:8080/api/v1/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerId":"cust-1","lines":[{"productId":"p-1","quantity":2,"unitPrice":1000}]}'
```

Swagger UI: http://localhost:8080/swagger-ui

## OOPforge skeleton

```text
/oopforge:craft Create a java-spring-layered skeleton for place-order
```

Skeleton skill: `skills/skeleton/backend-skeleton.md` (stack via `skills/lang/backend-stack.md`)
