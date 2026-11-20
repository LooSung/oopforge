# Calculator Kotlin Hexagonal + CQRS Example

CQRS is **not a third architecture** next to layered/hexagonal — it's a read/write split you lay **on top of** one. This example shows it on [`calculator-kotlin-hexagonal`](../calculator-kotlin-hexagonal/), where it fits most naturally: the write and read sides each get their **own ports**.

A Kotlin port of [`calculator-java-hexagonal-cqrs`](../calculator-java-hexagonal-cqrs/): same HTTP contract, same JSON field names, same tests.

- **Command** (`POST /api/v1/calculations`) → `CalculateCommandService` via the write port `CalculationRepository`, returns `calculationId` only.
- **Query** (`GET /api/v1/calculations/history`, `GET /api/v1/calculations/{id}`) → `HistoryQueryService` via the read port `HistoryQueryRepository`, returns `HistorySummary` read models (never loads the aggregate).

Both adapters share one in-memory `CalculationStore`; the write adapter projects each calculation into the history read model. Domain classes have **zero** Spring imports.

## What to look at

| Side | File | Role |
|---|---|---|
| Domain | `calculator/domain/Calculation.kt` | Aggregate root — `Calculation.perform(...)` |
| Command | `calculator/application/command/Calculate.kt` | Inbound write port (returns `CalculationId`) |
| Command | `calculator/application/command/CalculationRepository.kt` | Outbound write port |
| Command | `calculator/application/command/CalculateCommandService.kt` | Write use case |
| Query | `calculator/application/query/HistorySummary.kt` | Read model (projection) |
| Query | `calculator/application/query/HistoryQueryRepository.kt` | Outbound read port |
| Query | `calculator/application/query/HistoryQueryService.kt` | Read use case (no side effects) |
| Adapter | `calculator/adapter/persistence/CalculationStore.kt` | Shared write model + read projection |
| Adapter | `calculator/adapter/web/CalculatorCommandController.kt` | REST → command |
| Adapter | `calculator/adapter/web/CalculatorQueryController.kt` | REST → query |

> Progression: [`*-layered`](../calculator-kotlin-layered/) (simplest) → [`*-hexagonal`](../calculator-kotlin-hexagonal/) (ports & adapters) → **this** (hexagonal + CQRS).

## Run

```bash
cd examples/calculator-kotlin-hexagonal-cqrs
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

## Checks

- `ArchitectureTest` (ArchUnit, via `./gradlew test`) enforces a framework-free domain, command/query isolation, and an adapter-free application core.
- `scripts/ci/archlint.py cqrs` keeps the query side read-only and the command side free of read-shaped return types (run from the repository root):

```bash
python3 scripts/ci/archlint.py cqrs \
  examples/calculator-kotlin-hexagonal-cqrs/src/main/kotlin/com/oopforge/example/calculator
```

## Kotlin notes

- **Explicit return types on the command side.** Every public function in
  `CalculateCommandService.kt` declares its return type, so a read-shaped type
  cannot slip in through an inferred expression body. `archlint.py cqrs` rejects
  a public Kotlin command function without one.
- **Nullable returns over `Optional`.** `CalculationHistory.findById` and
  `HistoryQueryRepository.findById` return `HistorySummary?`; the query controller
  maps it with `?.let { ... } ?: ResponseEntity.notFound().build()`.
- **Aggregate as a plain class.** `Calculation` has a `private constructor`, a
  companion factory `Calculation.perform(...)`, and only `val` properties. It is
  not a `data class`, so no public `copy()` can bypass the factory.
- **The type system replaces null checks.** Java's `Objects.requireNonNull` calls
  disappear: parameters are non-null types. Value rules use `require(...)`
  (division by zero, a non-positive history `limit`).
- **Read models as `data class`es.** `HistorySummary` and the web responses are
  plain value carriers with a companion `from(...)` mapper.
- **Copies at the store boundary.** `CalculationStore.historySnapshot()` returns
  `history.toList()`, so callers never hold the live list.
- **Locale-independent lower-casing.** The read model's operator uses
  `name.lowercase()`; Java's `toLowerCase()` follows the default locale.
- **One top-level declaration per file**, named after it; `fun main` sits next to
  `CalculatorHexagonalCqrsApplication`.

### Difference from the Java reference

`CalculateRequest.operator` is a non-null `Operator`, so a missing `operator` is
rejected with `400`; in Java the `null` reaches `Objects.requireNonNull` in
`Calculation.perform` and fails with `500`. A missing operand still becomes `0.0`,
as in Java, because Kotlin `Double` compiles to a JVM primitive.

## OOPforge

```text
/oopforge:craft calculator with history in Kotlin + Spring Boot, hexagonal + CQRS
```

See [`skills/oop/cqrs.md`](../../skills/oop/cqrs.md) and [examples/README.md](../README.md) for the full calculator family.
