# Calculator TypeScript NestJS Hexagonal Example

Experimental **NestJS + hexagonal** reference for OOPforge: the `calculate`
use case via ports and adapters, no database (in-memory adapters).

A NestJS port of [`calculator-java-hexagonal`](../calculator-java-hexagonal/):
the same HTTP path, headers, status codes, JSON bodies, and test scenarios. The
differences are listed at the end.

The calculate transaction saves the Aggregate, drains its event once, and
dispatches a handler that appends `CalculationPerformedV1` to the same
in-memory transaction. The relay runs after commit; its consumer deduplicates
by outbox message ID. As in the Java reference, nothing schedules the relay:
tests call `OutboxRelay.relay()`.

The web adapter validates requests with zod, maps failures to safe JSON,
replays matching `Idempotency-Key` requests, rejects key conflicts, echoes
`X-Correlation-Id`, and records a secret-free audit entry. Idempotency, audit,
repository, and outbox stores are in-memory reference adapters, not
multi-instance production storage.

## Layout

```text
src/
├── main.ts                        bootstrap
├── configure-app.ts               correlation middleware · validation pipe · exception filter · OpenAPI (shared with e2e tests)
├── app.module.ts
└── calculator/
    ├── calculator.module.ts       composition: the only file that binds ports to adapters
    ├── domain/                    Calculation · Operator · CalculationId · events · DomainRuleViolation  (0 framework imports)
    ├── application/
    │   ├── provided/              Calculate (inbound port)
    │   ├── required/              repository · outbox · dispatcher · TransactionRunner ports
    │   ├── service/               CalculateService · dispatcher · CalculationPerformedHandler
    │   └── integration/           CalculationPerformedV1
    └── adapter/
        ├── web/                   controller · zod schemas · idempotency · correlation middleware · exception filter · OpenAPI
        ├── persistence/           InMemoryTransactionalAdapter (repository + outbox + transaction runner)
        ├── messaging/             OutboxRelay · CalculationPerformedConsumer
        └── audit/                 InMemoryAuditAdapter
test/                               e2e specs through AppModule with Supertest
```

Unit specs sit next to their source as `*.spec.ts`.

## Run

Requires Node.js 20.19 or newer.

```bash
cd examples/calculator-typescript-nestjs-hexagonal
npm install
npm run check   # oxlint + dependency-cruiser → tsc → vitest (unit, e2e) → nest build
npm run start
```

```bash
curl -X POST http://localhost:3000/calculations \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 6f1c2a54-demo' \
  -d '{"operandA": 8, "operator": "DIVIDE", "operandB": 2}'

curl http://localhost:3000/v3/api-docs
```

## TypeScript and NestJS notes

- **Domain.** Aggregates and value objects have a `private constructor` and a
  static factory (`Calculation.perform`, `CalculationId.generate`/`of`,
  `Operator.of`). State is `readonly` or private. `ReadonlyArray` is
  compile-time only, so drained events leave as a fresh array. A `Date` is
  mutable, so `DomainEvent` keeps epoch milliseconds and hands out copies, and
  records that cross ports carry ISO-8601 strings.
- **Ports are abstract classes.** Nest injects by a runtime token, and an
  interface does not exist at runtime, so `Calculate`, `CalculationRepository`,
  `OutboxPort`, `TransactionRunner`, and `DomainEventDispatcher` are abstract
  classes. Services import them as values, not `import type`, because Nest
  reads constructor parameter types from decorator metadata.
- **Application.** Depends only on the domain, its own ports, and
  `@nestjs/common` for `@Injectable()`. Ports return promises because every
  durable Node.js driver is asynchronous. The transaction boundary is the
  explicit `TransactionRunner` port, and each transaction modifies one
  Aggregate.
- **Composition.** `calculator.module.ts` binds one `InMemoryTransactionalAdapter`
  to three ports with `useExisting`, so a calculation and its outbox rows commit
  together; `useFactory` builds the dispatcher with its handler list. Tests
  replace a provider with `overrideProvider(Calculate)`, the counterpart of
  `@MockitoBean`.
- **Concurrency.** Java's `ThreadLocal` transaction becomes `AsyncLocalStorage`,
  because concurrent requests interleave at every `await`. Java's per-key
  `synchronized` becomes a per-key promise chain in `IdempotencyStore`.
- **Correlation and audit.** `correlationAudit` is plain Express middleware
  registered with `app.use()` in `configure-app.ts`, before Nest registers its
  body parser on `init()`. Like Java's servlet filter, it sees every request,
  malformed JSON and unknown routes included, sets `X-Correlation-Id` first, and
  writes the audit entry on the response's `finish`, after the exception filter
  has chosen the status.
- **Boundary.** zod validates in `adapter/web/` only, through
  `@Body({ schema })` and Nest's `StandardSchemaValidationPipe`; unknown keys are
  stripped. The global `WebExceptionFilter` maps schema failures and malformed
  JSON (both `BadRequestException`) to 400 `invalid_request`, key conflicts to
  409, `DomainRuleViolation` to 422, and anything else to 500, logged with the
  correlation id but without details. Other HTTP errors, such as a 404, keep
  Nest's answer.
- **OpenAPI.** `@nestjs/swagger` reads the request schema from
  `@Body({ schema })` and the response schemas from
  `@ApiResponse({ standardSchema })`; zod's `.meta({ id })` names the
  `CalculateRequest`, `CalculationResponse`, and `ApiError` components.
- **ESM.** `"type": "module"` with `nodenext`, so relative imports end in `.js`.
- **Style.** No `any`; exported functions and public methods declare return
  types; every production function ≤ 20 lines; every file ≤ 300 lines.

## Enforcement: dependency-cruiser and oxlint replace ArchUnit

`npm run lint` runs oxlint for the code-level Hard Rules and dependency-cruiser
for the hexagonal rules. Spec files are excluded from the cruise.

| Java ArchUnit rule | Rule here |
|---|---|
| domain free of Spring and Jakarta | dependency-cruiser `domain-isolation` (anything outside `domain/`, packages included; Node built-ins allowed) |
| application never depends on adapters | dependency-cruiser `application-no-adapter`, `application-no-composition` (`*.module.ts`, `main.ts`, `configure-app.ts`) |
| — | dependency-cruiser `application-no-transport` (no `zod`, `express`, `@nestjs/swagger`, `@nestjs/platform-express` in `application/`) |
| — | oxlint `parameter-properties` (readonly only), `no-non-null-assertion`, `no-explicit-any`, `explicit-module-boundary-types`, `no-floating-promises`, `max-lines-per-function` (20), `max-lines` (300) |

Each rule was seen failing on a seeded import, for example:

```text
error application-no-adapter: src/calculator/application/service/x.ts → src/calculator/adapter/web/idempotency.store.ts
```

## Tests

| Java test | NestJS test |
|---|---|
| `CalculationTest` | `src/calculator/domain/calculation.spec.ts` |
| `CalculateServiceTest` | `src/calculator/application/service/calculate.service.spec.ts` |
| `OutboxRelayTest` | `src/calculator/adapter/messaging/outbox-relay.spec.ts` |
| `ProductionReadinessWebIntegrationTest` | `test/production-readiness-web-integration.e2e-spec.ts` |
| `UnexpectedFailureWebIntegrationTest` | `test/unexpected-failure-web-integration.e2e-spec.ts` |
| `DomainEventIntegrationTest` | `test/domain-event-integration.e2e-spec.ts` |
| `ArchitectureTest` | `.dependency-cruiser.json` and `.oxlintrc.json` (see above) |

Six unit tests and twelve e2e tests. Three have no Java counterpart:
`test/api-docs.e2e-spec.ts` pins the generated contract to the one route;
`serializesConcurrentRequestsWithTheSameKey` races two same-key requests to
prove the per-key lock; `rejectsMalformedJsonWithSafeJson` proves the body
parser's error reaches the global filter.

## Deliberate differences from the Java reference

- **No server action.** The Next.js reference's second inbound adapter, a
  server action, is Next.js-only and is not ported, nor are its three tests.
- **Async ports.** Ports return promises where Java's are synchronous; HTTP
  behaviour is the same.
- **JSON numbers.** `8 / 2` returns `"result": 4`; Jackson writes `4.0`. The
  JSON values are equal, but the bytes differ.
- **Numeric strings.** `"operandA": "8"` returns 400 `invalid_request`.
- **Content type.** A body sent as `text/plain` is not parsed, and the schema
  returns 400 `invalid_request`.
- **Other methods.** `GET` or `PUT /calculations` gets Nest's default 404 body
  (`Cannot GET /calculations`), with an `X-Correlation-Id` header.
- **422 mapping.** Only `DomainRuleViolation` maps to 422; Java maps every
  `IllegalArgumentException`.
- **Event type.** The outbox `eventType` is an explicit constant, because
  production bundles may minify class names.
- **Correlation in logs.** The unexpected-failure log line carries the
  correlation id in its message instead of through MDC.
- **Test strings.** The "body does not contain" assertions name TypeScript
  types (`ZodError`, `DomainRuleViolation`, `Error`) instead of the Spring and
  JDK exception names.

## OOPforge

```text
/oopforge:craft calculate use case in typescript-nestjs-hexagonal
```

See [examples/README.md](../README.md) for the full calculator family.
