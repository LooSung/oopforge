# Calculator TypeScript Next.js Hexagonal + CQRS Example

CQRS is **not a third architecture** next to layered/hexagonal — it's a
read/write split you lay **on top of** one. This example shows it on the
hexagonal layout of the experimental TypeScript + Next.js stack: server code
lives under `src/server/` inside a Next.js App Router app, entered through thin
route handlers, and the write and read sides each get their **own ports**.

A TypeScript port of
[`calculator-java-hexagonal-cqrs`](../calculator-java-hexagonal-cqrs/): same HTTP
paths, same JSON field names, same tests.

- **Command** (`POST /api/v1/calculations`) → `CalculateCommandService` via the
  write port `CalculationRepository`, returns `calculationId` only.
- **Query** (`GET /api/v1/calculations/history`, `GET /api/v1/calculations/{id}`)
  → `HistoryQueryService` via the read port `HistoryQueryRepository`, returns
  `HistorySummary` read models (never loads the aggregate).

Both adapters share one in-memory `CalculationStore`; the write adapter projects
each calculation into the history read model. Domain classes have **zero**
framework imports.

## What to look at

All paths are under `src/server/calculator/`.

| Side | File | Role |
|---|---|---|
| Domain | `domain/calculation.ts` | Aggregate root — `Calculation.perform(...)` |
| Command | `application/command/calculate.ts` | Inbound write port (returns `CalculationId`) |
| Command | `application/command/calculationRepository.ts` | Outbound write port |
| Command | `application/command/calculateCommandService.ts` | Write use case |
| Query | `application/query/historySummary.ts` | Read model (projection) |
| Query | `application/query/historyQueryRepository.ts` | Outbound read port |
| Query | `application/query/historyQueryService.ts` | Read use case (no side effects) |
| Adapter | `adapter/persistence/calculationStore.ts` | Shared write model + read projection |
| Adapter | `adapter/web/calculatorCommandController.ts` | HTTP → command |
| Adapter | `adapter/web/calculatorQueryController.ts` | HTTP → query |
| Config | `config/calculatorConfig.ts` | Wiring (imports `'server-only'`) |

> Progression: [`*-layered`](../calculator-typescript-next-layered/) (simplest) →
> [`*-hexagonal`](../calculator-typescript-next-hexagonal/) (ports & adapters) →
> **this** (hexagonal + CQRS).

## Layout

```text
src/
├── app/                                       one-line re-exports, no logic
│   ├── api/v1/calculations/route.ts           export { calculate as POST } from …/calculatorCommandController
│   ├── api/v1/calculations/history/route.ts   export { listHistory as GET } from …/calculatorQueryController
│   ├── api/v1/calculations/[calculationId]/route.ts  export { getCalculation as GET } from …
│   └── v3/api-docs/route.ts                   export { GET } from …/openApiController
└── server/calculator/
    ├── domain/                 Calculation · CalculationId · Operator  (0 framework imports)
    ├── application/command/    Calculate · CalculationRepository · CalculateCommandService
    ├── application/query/      CalculationHistory · HistoryQueryRepository · HistoryQueryService · HistorySummary
    ├── adapter/persistence/    CalculationStore · InMemoryCalculationRepository · InMemoryHistoryQueryRepository
    ├── adapter/web/            controllers · zod schemas · openApiController · readJsonBody · badRequest
    └── config/                 calculatorConfig
tests/                          mirrors src/ (Vitest, handlers called with new Request(...))
```

## Run

```bash
cd examples/calculator-typescript-next-hexagonal-cqrs
npm install
npm run check   # eslint (zones + CQRS rules) → tsc → vitest → next build
npm run dev
```

```bash
# command — returns only the id
curl -X POST http://localhost:3000/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'

# query — read the history projection
curl http://localhost:3000/api/v1/calculations/history
```

- OpenAPI: http://localhost:3000/v3/api-docs

## TypeScript notes

- **Domain is framework-free.** `domain/` imports nothing from `next`, `react`,
  `zod`, `server-only`, an ORM, or `node:*`, and nothing outside `domain/`. Ids
  come from the global `crypto.randomUUID()`, which Node and Edge both provide.
- **Aggregate as a class behind a factory.** `Calculation` has a
  `private constructor` and `static perform(...)`; its state is `public readonly`
  constructor properties. No public mutable field, no non-readonly parameter
  property, no `!` non-null assertion. Collections leave as copies:
  `CalculationStore.historySnapshot()` returns `[...history]` typed
  `ReadonlyArray<HistorySummary>`.
- **`Instant` has no immutable twin.** A `Date` stays mutable behind `readonly`,
  so `Calculation` keeps epoch milliseconds and `performedAt` returns a fresh
  `Date` on each read. The `HistorySummary` read model stores the ISO-8601 string.
- **Ports are interfaces.** Java's nested `Calculate.CalculateCommand` record
  becomes the exported `CalculateCommand` interface beside `Calculate`;
  `Optional<T>` becomes `T | undefined`; `IllegalArgumentException` becomes
  `RangeError`; a `Map` is keyed by `id.value` because it compares object keys
  by identity.
- **Command returns an id; query has no side effects.** `handle(...)` returns a
  `CalculationId`, never a Response/Summary/Dto/View/ReadModel type, and
  `*QueryService.ts` calls nothing named save, delete, update, insert, persist,
  store, or remove. Exported functions and public methods declare their return
  types.
- **Boundary validation lives in `adapter/web/`.** zod schemas parse the JSON
  body, the `limit` query parameter, and the `calculationId` path parameter;
  malformed JSON and schema failures return `400` with a safe JSON body
  (`status`, `error`, a fixed `message`, `path`). The same schemas generate the
  OpenAPI document (`@asteasolutions/zod-to-openapi`).
- **Thin routes.** Every file under `src/app/` is a one-line re-export.
  `CalculatorQueryController` has two GET handlers and a module can export `GET`
  only once, so handlers keep the Java method names (`calculate`, `listHistory`,
  `getCalculation`) and each route file aliases one. Next.js 15 passes dynamic
  `params` as a `Promise`, so `getCalculation` awaits it.
- **Wiring.** `config/calculatorConfig.ts` builds the store, adapters, and
  services, and imports `server-only` to mark the server seam (Vitest aliases it
  to its empty module). It keeps the result on `globalThis`, because `next dev`
  re-evaluates modules each time it compiles another route: a plain module
  variable lost the first command before the history route compiled.
  `next start` shares one module instance across routes either way.
- **Size and shape.** No `any`; every function ≤ 20 lines; every file ≤ 300
  lines; comments only for a "why" the code cannot carry. Imports inside `src/`
  are relative, because the ESLint resolver does not resolve `@/` aliases and
  would silently skip the zones.

## Enforcement: ESLint replaces ArchUnit

The Java `ArchitectureTest` is replaced by `eslint.config.js`, run by
`npm run lint`. `import/no-restricted-paths` needs the
`import/resolver: { node: { extensions: ['.js', '.ts'] } }` setting; without it,
`.ts` imports do not resolve and the zones pass silently.

| Java ArchUnit rule | ESLint rule |
|---|---|
| `domainIsFrameworkFree` | zone `[domain-isolation]` plus `no-restricted-imports` `[domain-framework-free]` |
| `commandAndQuerySidesAreIsolated` | zones `[command-no-query]` and `[query-no-command]` |
| `applicationDoesNotDependOnAdapters` | zone `[application-no-adapter]` (adapters and `config/`) |
| `scripts/ci/archlint.py cqrs` (C1, C2) | `no-restricted-syntax` `[query-no-side-effects]` on `*QueryService.ts`, `[command-returns-id]` on `*CommandService.ts` |
| — | `[domain-readonly]`, `[domain-factory]`, `parameter-properties`, `no-non-null-assertion`, `no-explicit-any`, `explicit-module-boundary-types`, `max-lines-per-function` (20), `max-lines` (300) |

A violating import fails the lint with the zone's name, for example:

```text
1:8  error  Unexpected path "../command/calculateCommandService" imported in restricted zone. [query-no-command] The query side never imports the command side  import/no-restricted-paths
```

## Tests

| Java test | TypeScript test |
|---|---|
| `CalculationTest` | `tests/server/calculator/domain/calculation.test.ts` |
| `CalculateCommandServiceTest` | `tests/server/calculator/application/command/calculateCommandService.test.ts` |
| `HistoryQueryServiceTest` | `tests/server/calculator/application/query/historyQueryService.test.ts` |
| `CalculatorApiTest` | `tests/server/calculator/adapter/web/calculatorApi.test.ts` (calls the route files) |
| `ArchitectureTest` | `eslint.config.js` (see above) |

Three files have no Java counterpart. `tests/server/openApiContract.test.ts`
covers `/v3/api-docs`. `calculatorCommandController.test.ts` and
`calculatorQueryController.test.ts` pin the boundary behaviour this port adds:
id-only `201`, lookup by id, `404`, and `400` for malformed JSON, a missing
operand, a malformed id, or `limit=0`.

## Deliberate differences from the Java reference

- **Missing operand.** Java's primitive `double` turns a missing operand into
  `0.0`, so `{"operator": "ADD", "operandB": 3}` returns `201`. The TypeScript
  schema requires both operands and returns `400`.
- **Missing operator.** Java binds `null` and `Objects.requireNonNull` throws, so
  it returns `500`. The TypeScript schema returns `400`.
- **`limit` ≤ 0.** Java's read adapter throws `IllegalArgumentException`, so it
  returns `500`. The TypeScript schema returns `400`; the read adapter keeps its
  own guard.
- **`limit` parsing.** `z.coerce.number()` is not Spring's `int` binding: an
  empty `?limit=` returns `400` (Spring falls back to `20`), and `?limit=1e2` or
  `?limit=0x10` are read as `100` and `16` (Spring returns `400`).
- **Malformed id.** Java's `UUID.fromString` throws, so `GET /not-a-uuid` returns
  `500`. The TypeScript schema returns `400`, and it accepts only the canonical
  8-4-4-4-12 hex form that Java's parser loosens.
- **Numeric strings.** Jackson coerces `"6"` to `6.0`; `z.number()` rejects it
  with `400`.
- **Content type.** Spring returns `415` for a body that is not
  `application/json`; the route handler parses the body whatever its
  `Content-Type`.
- **Division by zero.** Both return `500`. Spring adds its JSON error body;
  Next.js returns an empty body and logs the `RangeError`.
- **Error body.** Spring's default error body is
  `{timestamp, status, error, path}`; this port returns
  `{status, error, message, path}` for `400`.
- **`performedAt` precision.** `toISOString()` has millisecond precision; Java's
  `Instant.toString()` can carry micro- or nanoseconds.
- **Number format.** JSON numbers serialize as `42`, not `42.0` (same value).
- **OpenAPI.** The Java CQRS reference has no springdoc. This port follows the
  OpenAPI default policy: the document is built from the zod schemas, served at
  `/v3/api-docs`, and lists the three Java paths. There is no Swagger UI.

## OOPforge

```text
/oopforge:craft calculator with history in TypeScript + Next.js, hexagonal + CQRS
```

See [`skills/oop/cqrs.md`](../../skills/oop/cqrs.md) and
[examples/README.md](../README.md) for the full calculator family.
