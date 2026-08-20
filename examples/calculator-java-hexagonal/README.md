# Calculator Java Hexagonal Example

Minimal **Spring Boot + hexagonal** reference for OOPforge — the `calculate` use case via ports & adapters, no database (in-memory repository).

Same calculator as [`calculator-java-layered`](../calculator-java-layered/), but with inbound/outbound ports and a domain event.

## What to look at

| Layer | File | Role |
|---|---|---|
| Domain | `calculator/domain/Calculation.java` | Aggregate root — `Calculation.perform(...)` |
| Domain | `calculator/domain/Operator.java` | Enum with polymorphic `apply()` (no switch) |
| Domain | `calculator/domain/CalculationPerformed.java` | Domain event |
| Application | `calculator/application/provided/Calculate.java` | Inbound port |
| Application | `calculator/application/required/CalculationRepository.java` | Outbound port |
| Application | `calculator/application/service/CalculateService.java` | Use case |
| Adapter | `calculator/adapter/web/CalculatorController.java` | REST → use case |
| Adapter | `calculator/adapter/persistence/InMemoryTransactionalAdapter.java` | Atomic repository + outbox |
| Adapter | `calculator/adapter/messaging/OutboxRelay.java` | At-least-once external delivery |

Domain classes have **zero** Spring imports.

The calculate transaction saves the Aggregate, drains its event once, and
dispatches a handler that appends `CalculationPerformedV1` to the same
in-memory transaction. The relay runs after commit; its consumer deduplicates
by outbox message ID.

## Run

```bash
cd examples/calculator-java-hexagonal
./gradlew test
./gradlew bootRun
```

`./gradlew test` includes ArchUnit checks that keep the domain free of Spring
and Jakarta dependencies and prevent the application layer from depending on
adapters. The examples workflow enforces these checks in CI.

```bash
curl -X POST http://localhost:8080/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'
```

## OOPforge

```text
/oopforge:craft calculate use case in java-spring-hexagonal
```

See [examples/README.md](../README.md) for the full calculator family.
