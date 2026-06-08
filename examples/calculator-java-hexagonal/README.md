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
| Adapter | `calculator/adapter/persistence/InMemoryCalculationRepository.java` | Port implementation |

Domain classes have **zero** Spring imports.

## Run

```bash
cd examples/calculator-java-hexagonal
./gradlew test
./gradlew bootRun
```

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
