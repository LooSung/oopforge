# Calculator Java Hexagonal + CQRS Example

CQRS is **not a third architecture** next to layered/hexagonal — it's a read/write split you lay **on top of** one. This example shows it on [`calculator-java-hexagonal`](../calculator-java-hexagonal/), where it fits most naturally: the write and read sides each get their **own ports**.

- **Command** (`POST /api/v1/calculations`) → `CalculateCommandService` via the write port `CalculationRepository`, returns `calculationId` only.
- **Query** (`GET /api/v1/calculations/history`, `GET /api/v1/calculations/{id}`) → `HistoryQueryService` via the read port `HistoryQueryRepository`, returns `HistorySummary` read models (never loads the aggregate).

Both adapters share one in-memory `CalculationStore`; the write adapter projects each calculation into the history read model. Domain classes have **zero** Spring imports.

## What to look at

| Side | File | Role |
|---|---|---|
| Domain | `calculator/domain/Calculation.java` | Aggregate root — `Calculation.perform(...)` |
| Command | `calculator/application/command/Calculate.java` | Inbound write port (returns `CalculationId`) |
| Command | `calculator/application/command/CalculationRepository.java` | Outbound write port |
| Command | `calculator/application/command/CalculateCommandService.java` | Write use case |
| Query | `calculator/application/query/HistorySummary.java` | Read model (projection) |
| Query | `calculator/application/query/HistoryQueryRepository.java` | Outbound read port |
| Query | `calculator/application/query/HistoryQueryService.java` | Read use case (no side effects) |
| Adapter | `calculator/adapter/persistence/CalculationStore.java` | Shared write model + read projection |
| Adapter | `calculator/adapter/web/CalculatorCommandController.java` | REST → command |
| Adapter | `calculator/adapter/web/CalculatorQueryController.java` | REST → query |

> Progression: [`*-layered`](../calculator-java-layered/) (simplest) → [`*-hexagonal`](../calculator-java-hexagonal/) (ports & adapters) → **this** (hexagonal + CQRS).

## Run

```bash
cd examples/calculator-java-hexagonal-cqrs
./gradlew test
./gradlew bootRun
```

```bash
# command — returns only the id
curl -X POST http://localhost:8080/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'

# query — read the history projection
curl http://localhost:8080/api/v1/calculations/history
```

## CI

- `scripts/ci/archlint.py cqrs` runs on this example in `.github/workflows/arch-lint.yml` — query side stays read-only, command side returns no read-shaped data.
- `ArchitectureTest` (ArchUnit, via `./gradlew test`) enforces a framework-free domain, command/query isolation, and an adapter-free application core.

## OOPforge

```text
/oopforge:craft calculator with history in java-spring-hexagonal + CQRS
```

See [`skills/oop/cqrs.md`](../../skills/oop/cqrs.md) and [examples/README.md](../README.md) for the full calculator family.
