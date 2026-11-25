# Calculator TypeScript NestJS Hexagonal + CQRS Example

CQRS is **not a third architecture** next to layered/hexagonal — it's a
read/write split you lay **on top of** one. This example shows it on the
hexagonal layout of the experimental TypeScript NestJS stack. The write side
and the read side each get their **own ports**.

A NestJS port of
[`calculator-java-hexagonal-cqrs`](../calculator-java-hexagonal-cqrs/): same HTTP
paths, same JSON field names, same tests.

- **Command** (`POST /api/v1/calculations`) → `CalculateCommandService` via the
  write port `CalculationRepository`, returns `calculationId` only.
- **Query** (`GET /api/v1/calculations/history`, `GET /api/v1/calculations/{id}`)
  → `HistoryQueryService` via the read port `HistoryQueryRepository`, returns
  `HistorySummary` read models (never loads the aggregate).

Both adapters share one in-memory `CalculationStore` (a singleton provider);
the write adapter projects each calculation into the history read model. Domain
classes have **zero** framework imports.

## What to look at

All paths are under `src/calculator/`.

| Side | File | Role |
|---|---|---|
| Domain | `domain/calculation.ts` | Aggregate root — `Calculation.perform(...)` |
| Command | `application/command/calculate.ts` | Inbound write port (returns `CalculationId`) |
| Command | `application/command/calculation.repository.ts` | Outbound write port |
| Command | `application/command/calculate-command.service.ts` | Write use case |
| Query | `application/query/history-summary.ts` | Read model (projection) |
| Query | `application/query/history-query.repository.ts` | Outbound read port |
| Query | `application/query/history-query.service.ts` | Read use case (no side effects) |
| Adapter | `adapter/persistence/calculation-store.ts` | Shared write model + read projection |
| Adapter | `adapter/web/calculator-command.controller.ts` | HTTP → command |
| Adapter | `adapter/web/calculator-query.controller.ts` | HTTP → query |
| Composition | `calculator.module.ts` | Binds each port to its adapter or service |

> Progression: [`*-layered`](../calculator-typescript-nestjs-layered/) (simplest) →
> [`*-hexagonal`](../calculator-typescript-nestjs-hexagonal/) (ports & adapters) →
> **this** (hexagonal + CQRS).

## Layout

```text
src/
├── main.ts                    bootstrap
├── configure-app.ts           validation pipe + OpenAPI (shared with e2e tests)
├── app.module.ts
└── calculator/
    ├── calculator.module.ts   composition
    ├── domain/                calculation (+ .spec) · calculation-id · operator  (0 framework imports)
    ├── application/command/   calculate · calculation.repository · calculate-command.service (+ .spec)
    ├── application/query/     calculation-history · history-query.repository · history-query.service (+ .spec) · history-summary
    ├── adapter/persistence/   calculation-store · in-memory-calculation.repository · in-memory-history-query.repository
    └── adapter/web/           command and query controllers · zod schemas · response shapes
test/                          e2e specs through AppModule with Supertest
```

## Run

Requires Node.js 20.19 or newer.

```bash
cd examples/calculator-typescript-nestjs-hexagonal-cqrs
npm install
npm run check   # oxlint + dependency-cruiser → tsc → vitest (unit, e2e) → nest build
npm run start
```

```bash
# command — returns only the id
curl -X POST http://localhost:3000/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'

# query — read the history projection
curl http://localhost:3000/api/v1/calculations/history
```

- OpenAPI: http://localhost:3000/v3/api-docs (UI at `/swagger-ui`)

## TypeScript and NestJS notes

- **Domain is framework-free.** `domain/` imports nothing from `@nestjs/*`,
  `zod`, `class-validator`, an ORM, or another layer. Ids come from the global
  `crypto.randomUUID()`.
- **Aggregate as a class behind a factory.** `Calculation` has a
  `private constructor` and `static perform(...)`; its state is `public readonly`
  constructor properties. No public mutable field, no `!` non-null assertion.
  Collections leave as copies: `CalculationStore.historySnapshot()` returns
  `[...history]` typed `ReadonlyArray<HistorySummary>`.
- **`Instant` has no immutable twin.** A `Date` stays mutable behind `readonly`,
  so `Calculation` keeps epoch milliseconds and `performedAt` returns a fresh
  `Date` on each read. The `HistorySummary` read model stores the ISO-8601 string.
- **Ports are abstract classes.** Nest injects by a runtime token, and a
  TypeScript interface does not exist at runtime. The inbound ports (`Calculate`,
  `CalculationHistory`) and outbound ports (`CalculationRepository`,
  `HistoryQueryRepository`) are abstract classes; `calculator.module.ts` binds
  each with `{ provide: Port, useClass: Implementation }`. Controllers inject the
  inbound ports, never the services.
- **Async ports.** The outbound ports return promises although the adapters are
  in-memory: every durable Node.js driver is asynchronous, and swapping an
  adapter must not change a port or a service. The domain stays synchronous.
- **Command returns an id; query has no side effects.** `handle(...)` resolves to
  a `CalculationId`, never a Response/Summary/Dto/View/ReadModel type, and
  `*-query.service.ts` calls nothing named save, delete, update, insert, persist,
  store, or remove. `scripts/ci/archlint.py cqrs` checks both.
- **Boundary validation in `adapter/web/`.** Zod schemas validate the JSON body
  (`@Body({ schema })`), the `limit` query parameter (`@Query('limit', { schema })`),
  and the `calculationId` path parameter (`@Param(..., { schema })`) through
  Nest's built-in `StandardSchemaValidationPipe`. `@nestjs/swagger` reads the
  same schemas into the OpenAPI document; `@ApiQuery({ required: false })`
  corrects `limit`, which the schema's default makes optional.
- **Route order.** `GET history` is declared before `GET :calculationId` in the
  query controller, so Nest registers the literal path first.
- **ESM.** `"type": "module"` with `nodenext`, so relative imports end in `.js`.
- **Size and shape.** No `any`; exported functions and public methods declare
  their return types; every function ≤ 20 lines; every file ≤ 300 lines.

## Enforcement: dependency-cruiser and oxlint replace ArchUnit

`npm run lint` runs oxlint for the code-level Hard Rules and dependency-cruiser
for the boundaries. dependency-cruiser resolves the `.js` import suffixes to
the `.ts` sources through `tsconfig.json`; `*.spec.ts` files are not cruised.

| Java ArchUnit rule | Rule here |
|---|---|
| `domainIsFrameworkFree` | dependency-cruiser `domain-isolation` (anything outside `domain/`, packages included; Node built-ins allowed) |
| `commandAndQuerySidesAreIsolated` | dependency-cruiser `command-no-query` and `query-no-command` |
| `applicationDoesNotDependOnAdapters` | dependency-cruiser `application-no-adapter` (adapters and `*.module.ts`) |
| `scripts/ci/archlint.py cqrs` (C1, C2) | the same script, which reads `*-command.service.ts` and `*-query.service.ts` |
| — | oxlint `parameter-properties` (readonly only), `no-non-null-assertion`, `no-explicit-any`, `explicit-module-boundary-types`, `no-floating-promises`, `max-lines-per-function` (20), `max-lines` (300) |

A violating import fails with the rule's name, for example:

```text
error query-no-command: src/calculator/application/query/x.ts → src/calculator/application/command/calculate.ts
```

## Tests

| Java test | TypeScript test |
|---|---|
| `CalculationTest` | `src/calculator/domain/calculation.spec.ts` |
| `CalculateCommandServiceTest` | `src/calculator/application/command/calculate-command.service.spec.ts` |
| `HistoryQueryServiceTest` | `src/calculator/application/query/history-query.service.spec.ts` |
| `CalculatorApiTest` | `test/calculator-api.e2e-spec.ts` |
| `ArchitectureTest` | `.dependency-cruiser.json`, `.oxlintrc.json`, and `archlint.py cqrs` (see above) |

Three files have no Java counterpart. `test/open-api.e2e-spec.ts` covers
`/v3/api-docs` (three paths, `limit` optional). `test/calculator-command.e2e-spec.ts`
and `test/calculator-query.e2e-spec.ts` pin the boundary behaviour: id-only
`201`, lookup by id, `404`, and `400` for malformed JSON, a missing operand, a
malformed id, or `limit=0`.

## Deliberate differences from the Java reference

- **Missing operand.** Java's primitive `double` turns a missing operand into
  `0.0`, so `{"operator": "ADD", "operandB": 3}` returns `201`. The zod schema
  requires both operands and returns `400`.
- **Missing operator.** Java returns `500` from `Objects.requireNonNull`; the
  schema returns `400`.
- **`limit` ≤ 0.** Java's read adapter throws `IllegalArgumentException`, so it
  returns `500`. The schema returns `400`; the read adapter keeps its own guard.
- **`limit` parsing.** `z.coerce.number()` is not Spring's `int` binding: an
  empty `?limit=` returns `400` (Spring falls back to `20`), and `?limit=1e2` or
  `?limit=0x10` are accepted, because `Number()` reads them as `100` and `16`
  (Spring returns `400`).
- **Malformed id.** Java's `UUID.fromString` throws, so `GET /not-a-uuid` returns
  `500`. The schema returns `400` and accepts only the canonical 8-4-4-4-12 hex
  form, in either case.
- **Numeric strings.** Jackson coerces `"6"` to `6.0`; `z.number()` rejects it
  with `400`.
- **Content type.** Spring returns `415` for a body that is not
  `application/json`; Nest does not parse it, and the schema returns `400`.
- **Division by zero.** Both return `500`; Nest's body is
  `{"statusCode": 500, "message": "Internal server error"}`.
- **Not found.** Java returns `404` with an empty body; Nest's
  `NotFoundException` returns `{"message": "Not Found", "statusCode": 404}`.
- **Error body.** Nest's default `400` body is
  `{message, error: "Bad Request", statusCode}`; for malformed JSON the message
  is the JSON parser's.
