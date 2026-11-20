# Calculator Kotlin Layered Example

Minimal **Spring Boot 3-tier (layered)** reference for OOPforge in Kotlin — the `calculate` use case across `controller / service / repository / domain`, no database (in-memory).

A Kotlin port of [`calculator-java-layered`](../calculator-java-layered/): same HTTP contract, same JSON field names, same tests. For ports & adapters, see [`calculator-kotlin-hexagonal`](../calculator-kotlin-hexagonal/).

Each layer is its **own package/folder** (the current layer-layout Hard Rule),
and the controller goes through the service — never straight to the repository.

## Layout

```text
com/oopforge/example/layered/calculator/
├── controller/   CalculatorController · dto/ (CalculateRequest, CalculationResponse)
├── service/      CalculatorService
├── repository/   CalculationRepository · InMemoryCalculationRepository
└── domain/       Calculation (aggregate) · Operator · CalculationId  (0 framework imports)
```

## Run

```bash
cd examples/calculator-kotlin-layered
./gradlew test
./gradlew bootRun
```

- Swagger UI: http://localhost:8080/swagger-ui · OpenAPI: http://localhost:8080/v3/api-docs

```bash
curl -X POST http://localhost:8080/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}'
```

The layer rules can also be checked without Gradle, from the repository root:

```bash
python3 scripts/ci/archlint.py layered \
  examples/calculator-kotlin-layered/src/main/kotlin/com/oopforge/example/layered/calculator
```

## Kotlin notes

- **Aggregate as a plain class.** `Calculation` has a `private constructor` and a
  companion factory, `Calculation.perform(...)`; every property is a `val`. It is
  not a `data class`, so no public `copy()` can bypass the factory.
- **The type system replaces null checks.** Java's `Objects.requireNonNull` calls
  disappear: parameters are non-null types. Value rules use `require(...)`, which
  throws `IllegalArgumentException` (division by zero in `Operator.DIVIDE`).
- **Nullable return over `Optional`.** `CalculationRepository.findById` returns
  `Calculation?`.
- **Value object as a `data class`.** `CalculationId` wraps a non-null `UUID` with
  a public constructor, so it needs no `@ConsistentCopyVisibility` and no `init`
  block.
- **Locale-independent lower-casing.** The response operator uses
  `name.lowercase()`, which gives the same result in every locale; Java's
  `toLowerCase()` follows the default locale.
- **One top-level declaration per file**, named after it; `fun main` sits next to
  `LayeredCalculatorApplication`.
- **Spring plumbing.** `kotlin("plugin.spring")` opens Spring-annotated classes,
  `jackson-module-kotlin` binds JSON to constructor parameters, and
  `-Xjsr305=strict` turns Spring's nullability annotations into Kotlin types.

### Deliberate difference from the Java reference

Java's `double` request fields turn a missing operand into `0.0`, so
`{"operator": "ADD", "operandB": 3}` returns `201` with `operandA: 0.0`. The
Kotlin request uses non-null `Double`, so a missing (or `null`) operand is
rejected with `400`.

Non-null `Double` alone is not enough: it compiles to a JVM primitive, and Jackson
would still supply `0.0`. `application.yml` therefore enables
`spring.jackson.deserialization.fail-on-null-for-primitives`.

The same non-null typing also rejects a missing `operator` with `400`; in Java the
`null` reaches `Objects.requireNonNull` in `Calculation.perform` and fails with
`500`.

## OOPforge

```text
/oopforge:craft calculate use case in Kotlin + Spring Boot, layered
```

See [examples/README.md](../README.md) for the full calculator family.
