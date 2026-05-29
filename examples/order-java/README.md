# Order Java Example

Minimal **Spring Boot + hexagonal** reference for OOPforge.

Demonstrates one bounded context (`order`), one use case (`PlaceOrder`), domain events, and ports/adapters — without a database (in-memory repository).

## What to look at

| Layer | File | Role |
|---|---|---|
| Domain | `order/domain/Order.java` | Aggregate root — `Order.place(...)` |
| Domain | `order/domain/OrderPlaced.java` | Domain event |
| Application | `order/application/provided/PlaceOrder.java` | Inbound port |
| Application | `order/application/required/OrderRepository.java` | Outbound port |
| Application | `order/application/service/PlaceOrderService.java` | Use case |
| Adapter | `order/adapter/web/OrderController.java` | REST → use case |
| Adapter | `order/adapter/persistence/InMemoryOrderRepository.java` | Port implementation |

Domain classes have **zero** Spring/JPA imports.

## Run

```bash
cd examples/order-java
./gradlew test
./gradlew bootRun
```

```bash
curl -X POST http://localhost:8080/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerId":"cust-1","lines":[{"productId":"p-1","quantity":2,"unitPrice":1000}]}'
```

## OOPforge workflow mapping

This example is the **proof** for README Before/After. To extend it with OOPforge agents:

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:skeleton java-spring
/oopforge:implement place-order
/oopforge:test place-order
```

See [docs/claude-code.md](../../docs/claude-code.md) and [docs/cursor.md](../../docs/cursor.md).
