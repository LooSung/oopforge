# Calculator TypeScript Next.js Hexagonal Example

Experimental **Next.js App Router + hexagonal** reference for OOPforge: the
`calculate` use case via ports and adapters, with domain and application code
under `src/server/` and no database (in-memory adapters).

It ports [`calculator-java-hexagonal`](../calculator-java-hexagonal/) at full
parity: the same HTTP path, headers, status codes, JSON bodies, and test
scenarios. The differences are listed at the end.

## What to look at

| Layer | File | Role |
|---|---|---|
| Domain | `calculator/domain/calculation.ts` | Aggregate root: `Calculation.perform(...)` |
| Domain | `calculator/domain/operator.ts` | Operators carry their own `apply()` (no switch) |
| Domain | `calculator/domain/calculationPerformed.ts` | Domain event |
| Application | `calculator/application/provided/calculate.ts` | Inbound port |
| Application | `calculator/application/required/calculationRepository.ts` | Outbound port |
| Application | `calculator/application/required/transactionRunner.ts` | Unit-of-work port |
| Application | `calculator/application/service/calculateService.ts` | Use case |
| Adapter | `calculator/adapter/web/calculatorController.ts` | Route handler → use case |
| Adapter | `calculator/adapter/web/calculateAction.ts` | Server action → same use case |
| Adapter | `calculator/adapter/persistence/inMemoryTransactionalAdapter.ts` | Atomic repository + outbox |
| Adapter | `calculator/adapter/messaging/outboxRelay.ts` | At-least-once external delivery |
| Config | `calculator/config/calculatorConfig.ts` | Composition root (`server-only`) |

Domain files import nothing outside `domain/`: no `next`, `react`, `zod`, or ORM.

The calculate transaction saves the Aggregate, drains its event once, and
dispatches a handler that appends `CalculationPerformedV1` to the same
in-memory transaction. The relay runs after commit; its consumer deduplicates
by outbox message ID.

The web adapter validates requests with zod, maps failures to safe JSON,
replays matching `Idempotency-Key` requests, rejects key conflicts, echoes
`X-Correlation-Id`, and records a secret-free audit entry. Idempotency, audit,
repository, and outbox stores are in-memory reference adapters, not
multi-instance production storage.

## Layout

```text
src/
├── app/                              route files only, one line each
│   ├── calculations/route.ts         export { POST } from adapter/web/calculatorController
│   └── v3/api-docs/route.ts          export { GET } from adapter/web/apiDocsController
└── server/calculator/
    ├── domain/                       Calculation · Operator · CalculationId · events · DomainRuleViolation
    ├── application/
    │   ├── provided/                 Calculate (inbound port)
    │   ├── required/                 repository · outbox · dispatcher · TransactionRunner ports
    │   ├── service/                  CalculateService · dispatcher · CalculationPerformedHandler
    │   └── integration/              CalculationPerformedV1
    ├── adapter/
    │   ├── web/                      handlers · server action · zod schemas · idempotency · correlation · errors · OpenAPI
    │   ├── persistence/              InMemoryTransactionalAdapter
    │   ├── messaging/                OutboxRelay · CalculationPerformedConsumer
    │   └── audit/                    InMemoryAuditAdapter
    └── config/                       calculatorConfig.ts
tests/                                mirrors src/ (Vitest)
```

## Run

Requires Node.js 20 or newer (global Web Crypto).

```bash
cd examples/calculator-typescript-next-hexagonal
npm ci
npm run check   # ESLint zones + tsc + Vitest + next build
npm run dev
```

```bash
curl -X POST http://localhost:3000/calculations \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 6f1c2a54-demo' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'

curl http://localhost:3000/v3/api-docs
```

`next build` generates `next-env.d.ts`; it is gitignored as a generated file.

## Architecture checks: ESLint zones instead of ArchUnit

The Java `ArchitectureTest` is replaced by `import/no-restricted-paths` zones
in `eslint.config.js`, which `npm run lint` enforces:

| Zone | Rule |
|---|---|
| `domain/` | imports nothing outside `domain/`, packages included; `no-restricted-imports` also blocks Node built-ins, which are not file paths |
| `application/` | never imports `adapter/` or `config/` |
| `src/app/` | imports only `adapter/web/` |

The resolver is set to `.ts` explicitly, because the default node resolver
does not resolve `.ts` imports and the zones would then pass silently. They
were proven with temporary violating imports: each zone failed `npm run lint`
with its message, for example
`Unexpected path "../application/provided/calculate" imported in restricted zone. Domain imports nothing outside domain/ ...`.

## TypeScript notes

How the OOPforge Hard Rules look in this stack:

- **Domain.** Aggregates and value objects have a `private constructor` and a
  static factory (`Calculation.perform`, `CalculationId.generate`/`of`,
  `Operator.of`). State is `readonly` or private; ESLint rejects public
  mutable fields, non-`readonly` public constructor properties, public
  setters, and `!` non-null assertions. `ReadonlyArray` is compile-time only,
  so drained events leave as a fresh array. A `Date` is mutable, so
  `DomainEvent` keeps epoch milliseconds and hands out copies, and records
  that cross ports carry ISO-8601 strings.
- **Application.** Depends only on the domain and its own ports. Ports return
  promises because every durable Node.js driver is asynchronous; with
  synchronous ports, a real adapter would mean rewriting the ports and the
  service. The transaction boundary is the explicit `TransactionRunner` port,
  and each transaction modifies one Aggregate.
- **Concurrency.** Java's `ThreadLocal` transaction becomes `AsyncLocalStorage`,
  because concurrent requests interleave at every `await`. Java's per-key
  `synchronized` becomes a per-key promise chain in `IdempotencyStore`. The
  in-memory adapter's methods never await, so they need no lock.
- **Boundary.** zod validates in `adapter/web/` only. Malformed JSON and schema
  failures return 400 with the same safe body as Java; unknown keys are
  stripped. Domain rule violations (`DomainRuleViolation`) return 422.
  Anything else returns 500 and is logged without its details.
- **Inbound adapters.** Route files are one-line re-exports. Correlation and
  audit live in a wrapper in `adapter/web/`, not in Next.js middleware, which
  runs on the Edge runtime and cannot share the in-memory audit store.
- **Server action.** `calculateAction` is the second inbound adapter. It is
  internal RPC, so it is left out of the OpenAPI document, but its input is
  still untrusted: it goes through the same zod schema and calls the same
  `Calculate` service. It returns `{ ok: true, calculation }` or
  `{ ok: false, error }` with the HTTP error codes, because Next.js redacts
  thrown errors.
- **Composition.** Next.js has no DI container. `createCalculatorConfig()`
  wires the graph; only the entry modules (`calculatorController`,
  `calculateAction`) read the module-level default graph. It is deliberately
  not kept on `globalThis`: a graph that outlives a module re-evaluation runs
  old code and throws error classes that the reloaded `instanceof` checks no
  longer recognise. Each evaluation, such as a dev reload, therefore starts
  with empty in-memory stores. Tests build fresh graphs, and replacing one
  collaborator through `createCalculatorConfig({ calculate })` stands in for
  `@MockitoBean`.
- **OpenAPI.** `adapter/web/openApiDocument.ts` builds the document from the
  zod schemas with `@asteasolutions/zod-to-openapi`, using zod's `.meta({ id })`
  rather than patching zod's prototype.
- **Style.** Exported functions and public methods declare return types; no
  `any`. Every function is at most 20 lines, tests included, and every file
  at most 300 lines (ESLint `max-lines-per-function` and `max-lines`). Imports
  inside `src/` are relative, because the resolver does not follow `@/`
  aliases. Files are `.ts`, camelCase, and named after their main export.

## Differences from the Java reference

- **Async ports.** Ports return promises where Java's are synchronous; HTTP
  behaviour is identical.
- **JSON numbers.** Jackson writes doubles as `8.0`; JavaScript writes `8`.
  The JSON values are equal, but the bytes differ.
- **Numeric strings.** zod rejects `"operandA": "8"` with 400, where Jackson's
  default scalar coercion probably accepts it. This edge is untested in both
  references.
- **Content-Type.** The route handler parses the body as JSON whatever the
  `Content-Type`; Spring requires `application/json`.
- **Other methods.** A non-POST request to `/calculations` gets Next.js's
  built-in 405. That response bypasses the wrapper, so it carries no
  `X-Correlation-Id`; Java's servlet filter sees every request.
- **422 mapping.** Only `DomainRuleViolation` maps to 422; Java maps every
  `IllegalArgumentException`.
- **Event type.** The outbox `eventType` is an explicit constant, because
  production bundles may minify class names.
- **Correlation in logs.** The unexpected-failure log carries the correlation
  id as an argument instead of through MDC.
- **Additions with no Java counterpart:** `/v3/api-docs` (the Java hexagonal
  reference ships no springdoc), the server action, and a test that races two
  same-key requests to prove the per-key lock.
- **Test strings.** The "body does not contain" assertions name TypeScript
  types (`ZodError`, `DomainRuleViolation`, `Error`) instead of the Spring and
  JDK exception names.

## OOPforge

```text
/oopforge:craft calculate use case in typescript-next-hexagonal
```

See [examples/README.md](../README.md) for the full calculator family.
