# Calculator TypeScript Next.js Layered Example

Minimal **3-tier (layered)** reference for OOPforge on the experimental
TypeScript + Next.js stack: the `calculate` use case across
`controller / service / repository / domain`, no database (in-memory). The
server code lives under `src/server/` inside a Next.js App Router app and is
entered through thin route handlers.

A TypeScript port of [`calculator-java-layered`](../calculator-java-layered/):
same HTTP paths, same JSON field names, same tests.

Each layer is its **own folder** (the layer-layout Hard Rule), and the
controller goes through the service — never straight to the repository.

## Layout

```text
src/
├── app/                              Next.js routes: one-line re-exports, no logic
│   ├── api/v1/calculations/route.ts  export { POST } from …/controller/calculatorController
│   └── v3/api-docs/route.ts          export { GET } from …/controller/openApiController
└── server/
    ├── core/dependencies.ts          composition root (imports 'server-only')
    └── calculator/
        ├── controller/   calculatorController · openApiController · readJsonBody · badRequest
        │                 dto/ (CalculateRequest, CalculationResponse — zod schemas)
        ├── service/      CalculatorService (CalculateCommand, CalculationResult)
        ├── repository/   CalculationRepository · InMemoryCalculationRepository
        └── domain/       Calculation (aggregate) · Operator · CalculationId  (0 framework imports)
tests/                                mirrors src/ (Vitest, handlers called with new Request(...))
```

## Run

Requires Node.js 20 or newer (global Web Crypto).

```bash
cd examples/calculator-typescript-next-layered
npm install
npm run check   # eslint (layer zones) → tsc → vitest → next build
npm run dev
```

- OpenAPI: http://localhost:3000/v3/api-docs

```bash
curl -X POST http://localhost:3000/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}'
```

## TypeScript notes

- **Domain is framework-free.** `domain/` imports nothing from `next`, `react`,
  `zod`, `server-only`, an ORM, or `node:*`, and nothing outside `domain/`. Ids
  come from the global `crypto.randomUUID()`, which Node and Edge both provide.
- **Aggregate as a class behind a factory.** `Calculation` has a
  `private constructor` and `static perform(...)`; its state is `public readonly`
  constructor properties. No public mutable field, no non-readonly parameter
  property, no `!` non-null assertion. A collection would leave as a copy
  (`[...items]`) typed `ReadonlyArray<T>`; this example has none.
- **Enum with behaviour.** Java's `Operator` enum becomes a class with four
  `static readonly` instances, a private constructor, and `Operator.of(name)`.
- **Errors.** Java's `IllegalArgumentException` becomes `RangeError`. The type
  system replaces `Objects.requireNonNull`, and `Optional<T>` becomes
  `T | undefined`.
- **Value equality.** A `Map` compares object keys by identity, so the repository
  keys calculations by `id.value`, not by the `CalculationId` instance.
- **Boundary validation lives in the controller.** zod schemas in
  `controller/dto/` parse the body; malformed JSON and schema failures return
  `400` with a safe JSON body (`status`, `error`, a fixed `message`, `path`). The
  same schemas generate the OpenAPI document (`@asteasolutions/zod-to-openapi`).
- **Async repository.** `CalculationRepository` returns promises although the
  reference adapter is in-memory: every durable Node.js driver is asynchronous,
  and swapping the adapter must not change the interface or the service. So
  `CalculatorService.calculate` and the controller are `async`; the domain stays
  synchronous.
- **Controller → service → repository.** Controllers and route files never import
  a repository. `src/server/core/dependencies.ts` wires the service to the
  in-memory repository at module level and imports `server-only` to mark the
  server seam; Vitest aliases `server-only` to its empty module. Under `next dev`
  a recompile can reset the in-memory repository, a property of the in-memory
  adapter that a durable adapter does not have.
- **Thin routes.** Every file under `src/app/` is a one-line re-export of a
  handler from `controller/`.
- **Size and shape.** No `any`; exported functions and public methods declare
  their return types; every function ≤ 20 lines; every file ≤ 300 lines;
  comments only for a "why" the code cannot carry. Imports inside `src/` are
  relative, because the ESLint resolver does not resolve `@/` aliases and would
  silently skip the zones.

## Enforcement: ESLint replaces ArchUnit

The Java `ArchitectureTest` is replaced by `eslint.config.js`, run by
`npm run lint`. `import/no-restricted-paths` needs the
`import/resolver: { node: { extensions: ['.js', '.ts'] } }` setting; without it,
`.ts` imports do not resolve and the zones pass silently.

| Java ArchUnit rule | ESLint rule |
|---|---|
| `layers_only_depend_downward` | zones `[controller-no-repository]` (controller and `src/app`), `[service-no-controller]`, `[repository-downward-only]` |
| `domain_is_framework_free` | zone `[domain-isolation]` plus `no-restricted-imports` `[domain-framework-free]` |
| — | `[domain-readonly]`, `[domain-factory]`, `parameter-properties`, `no-non-null-assertion`, `no-explicit-any`, `explicit-module-boundary-types`, `max-lines-per-function` (20), `max-lines` (300) |

A violating import fails the lint with the zone's name, for example:

```text
1:8  error  Unexpected path "../repository/inMemoryCalculationRepository" imported in restricted zone. [controller-no-repository] Controllers and route files go through the service, never a repository  import/no-restricted-paths
```

## Tests

| Java test | TypeScript test |
|---|---|
| `CalculationTest` | `tests/server/calculator/domain/calculation.test.ts` |
| `CalculatorServiceTest` | `tests/server/calculator/service/calculatorService.test.ts` |
| `OpenApiContractTest` | `tests/server/openApiContract.test.ts` |
| `ArchitectureTest` | `eslint.config.js` (see above) |

`tests/server/calculator/controller/calculatorController.test.ts` has no Java
counterpart. It pins the boundary behaviour this port adds (`201` with a
lower-case operator, and `400` for malformed JSON, a missing operand, or an
unknown operator).

## Deliberate differences from the Java reference

- **Missing operand.** Java's primitive `double` turns a missing operand into
  `0.0`, so `{"operator": "ADD", "operandB": 3}` returns `201`. The TypeScript
  schema requires both operands and returns `400`.
- **Missing operator.** Java binds `null` and `Objects.requireNonNull` throws, so
  it returns `500`. The TypeScript schema returns `400`.
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
- **Async repository.** The repository returns promises where Java's is
  synchronous; HTTP behaviour is identical.
- **Number format.** JSON numbers serialize as `42`, not `42.0` (same value).
- **OpenAPI.** The document is built from the zod schemas and served at
  `/v3/api-docs`; there is no Swagger UI.

## OOPforge

```text
/oopforge:craft calculate use case in TypeScript + Next.js, layered
```

See [examples/README.md](../README.md) for the full calculator family.
