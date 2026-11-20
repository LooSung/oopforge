# Calculator Kotlin Hexagonal Example

Minimal **Spring Boot + hexagonal** reference for OOPforge in Kotlin — the `calculate` use case via ports & adapters, no database (in-memory repository).

A Kotlin port of [`calculator-java-hexagonal`](../calculator-java-hexagonal/): same HTTP contract, same JSON field names, same tests. Same calculator as [`calculator-kotlin-layered`](../calculator-kotlin-layered/), but with inbound/outbound ports and a domain event.

## What to look at

| Layer | File | Role |
|---|---|---|
| Domain | `calculator/domain/Calculation.kt` | Aggregate root — `Calculation.perform(...)` |
| Domain | `calculator/domain/Operator.kt` | Enum with polymorphic `apply()` (no `when`) |
| Domain | `calculator/domain/CalculationPerformed.kt` | Domain event |
| Application | `calculator/application/provided/Calculate.kt` | Inbound port |
| Application | `calculator/application/required/CalculationRepository.kt` | Outbound port |
| Application | `calculator/application/service/CalculateService.kt` | Use case |
| Adapter | `calculator/adapter/web/CalculatorController.kt` | REST → use case |
| Adapter | `calculator/adapter/persistence/InMemoryTransactionalAdapter.kt` | Atomic repository + outbox |
| Adapter | `calculator/adapter/messaging/OutboxRelay.kt` | At-least-once external delivery |

Domain classes have **zero** Spring imports.

The calculate transaction saves the Aggregate, drains its event once, and
dispatches a handler that appends `CalculationPerformedV1` to the same
in-memory transaction. The relay runs after commit; its consumer deduplicates
by outbox message ID.

The web adapter validates requests, maps failures to safe JSON, replays matching
`Idempotency-Key` requests, rejects key conflicts, echoes `X-Correlation-Id`,
and records a secret-free audit entry. Idempotency, audit, repository, and
outbox stores are in-memory reference adapters, not multi-instance production
storage.

## Run

```bash
cd examples/calculator-kotlin-hexagonal
./gradlew test
./gradlew bootRun
```

`./gradlew test` includes ArchUnit checks that keep the domain free of Spring
and Jakarta dependencies and prevent the application layer from depending on
adapters.

```bash
curl -X POST http://localhost:8080/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'
```

## Kotlin notes

- **Aggregate as a plain class.** `Calculation` has a `private constructor`, a
  companion factory `Calculation.perform(...)`, and only `val` properties. It is
  not a `data class`, so no public `copy()` can bypass the factory.
- **Invariants in `init` when the constructor is public.**
  `CalculationPerformedV1` is a `data class` with a public constructor, so its
  `schemaVersion` rule lives in `init { require(...) }`, which `copy()` cannot
  skip.
- **Events leave as a copy.** `Calculation.popEvents()` returns
  `events.toList()` and then clears the private `MutableList`; callers never
  hold the live list. The audit entries, consumer effects, and dispatcher
  handlers cross their boundaries the same way.
- **The type system replaces null checks.** Java's `Objects.requireNonNull`
  calls disappear: parameters are non-null types, and the domain has no `!!` or
  `lateinit`. Division by zero is a `require(...)`.
- **The exception family is HTTP contract.** `require`/`requireNotNull` throw
  `IllegalArgumentException` (→ `422 calculation_rejected`); `check`/`checkNotNull`
  throw `IllegalStateException` (→ `500 internal_error`). The transaction misuse
  guards and the operand unwrapping in `NormalizedRequest.from` use `check*`, so
  they fail with `500` as the Java originals do.
- **Nullable returns over `Optional`.** `CalculationRepository.findById` and
  `OutboxPort.publishedAt` return `T?`.
- **`@field:` validation targets.** `CalculateRequest` puts `@field:NotNull` on
  nullable properties, so a missing field is rejected with `400`.
- **JDK whitespace for header checks.** Kotlin's `trim()` and `isBlank()` also
  treat no-break spaces as whitespace. `CorrelationAuditFilter` and
  `IdempotencyStore` pass `Character::isWhitespace` to keep Java's `strip()` and
  `isBlank()` behaviour.
- **Locale-independent lower-casing.** The response's operator uses
  `name.lowercase()`; Java's `toLowerCase()` follows the default locale.
- **Mockito without MockK.** `UnexpectedFailureWebIntegrationTest` puts
  `@MockitoBean` on a `lateinit` field (the only `lateinit`, and test-only) and
  stubs with a generic `anyValue()` helper: Kotlin null-checks the result of
  `ArgumentMatchers.any()` before it reaches a non-null parameter.
- **One top-level declaration per file**, named after it; `fun main` sits next to
  `CalculatorHexagonalApplication`.

### Difference from the Java reference

`InMemoryAuditAdapter.AuditEntry` is a `data class`, not a record, so
`auditContainsOnlySafeFields` asserts its primary-constructor parameter names
instead of `getRecordComponents()`.

## OOPforge

```text
/oopforge:craft calculate use case in kotlin-spring-hexagonal
```

See [examples/README.md](../README.md) for the full calculator family.
