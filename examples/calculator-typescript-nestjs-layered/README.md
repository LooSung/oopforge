# Calculator TypeScript NestJS Layered Example

Minimal **3-tier (layered)** reference for OOPforge on the experimental
TypeScript NestJS stack: the `calculate` use case across
`controller / service / repository / domain`, no database (in-memory).

A NestJS port of [`calculator-java-layered`](../calculator-java-layered/):
same HTTP paths, same JSON field names, same tests.

Each layer is its **own folder** inside the feature module (the layer-layout
Hard Rule), and the controller goes through the service — never straight to
the repository. `nest g resource` puts controller and service side by side in
one folder; OOPforge's layered stack moves them into layer folders.

## Layout

```text
src/
├── main.ts                    bootstrap
├── configure-app.ts           validation pipe + OpenAPI (shared with e2e tests)
├── app.module.ts
└── calculator/
    ├── calculator.module.ts   composition: the only file that names every layer
    ├── controller/   calculator.controller · calculate.request (zod) · calculation.response
    ├── service/      calculator.service (+ .spec)
    ├── repository/   calculation.repository (abstract port) · in-memory-calculation.repository
    └── domain/       calculation (aggregate, + .spec) · operator · calculation-id  (0 framework imports)
test/                  e2e specs through AppModule with Supertest
```

## Run

Requires Node.js 20.19 or newer.

```bash
cd examples/calculator-typescript-nestjs-layered
npm install
npm run check   # oxlint + dependency-cruiser → tsc → vitest (unit, e2e) → nest build
npm run start
```

- OpenAPI: http://localhost:3000/v3/api-docs (UI at `/swagger-ui`)

```bash
curl -X POST http://localhost:3000/api/v1/calculations \
  -H 'Content-Type: application/json' \
  -d '{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}'
```

## TypeScript and NestJS notes

- **Domain is framework-free.** `domain/` imports nothing from `@nestjs/*`,
  `zod`, `class-validator`, an ORM, or another layer. Ids come from the global
  `crypto.randomUUID()`.
- **Aggregate as a class behind a factory.** `Calculation` has a
  `private constructor` and `static perform(...)`; its state is `public readonly`
  constructor properties. No public mutable field, no `!` non-null assertion. A
  collection would leave as a copy (`[...items]`); this example has none.
- **Enum with behaviour.** Java's `Operator` enum becomes a class with four
  `static readonly` instances, a private constructor, and `Operator.of(name)`.
- **Ports are abstract classes.** Nest injects by a runtime token, and a
  TypeScript interface does not exist at runtime, so `CalculationRepository` is
  an abstract class. `calculator.module.ts` binds it with
  `{ provide: CalculationRepository, useClass: InMemoryCalculationRepository }`.
- **Async repository.** The port returns promises although the adapter is
  in-memory: every durable Node.js driver is asynchronous, and swapping the
  adapter must not change the port or the service. The domain stays synchronous.
- **Boundary validation in the controller.** `@Body({ schema: calculateRequest })`
  with Nest's built-in `StandardSchemaValidationPipe` validates the body with
  zod; `@nestjs/swagger` reads the same schema into the OpenAPI document.
- **ESM.** `"type": "module"` with `nodenext`, so relative imports end in `.js`.
- **Size and shape.** No `any`; exported functions and public methods declare
  their return types; every function ≤ 20 lines; every file ≤ 300 lines.

## Enforcement: dependency-cruiser and oxlint replace ArchUnit

`npm run lint` runs oxlint for the code-level Hard Rules and dependency-cruiser
for the layer rules. dependency-cruiser resolves the `.js` import suffixes to
the `.ts` sources through `tsconfig.json`.

| Java ArchUnit rule | Rule here |
|---|---|
| `layers_only_depend_downward` | dependency-cruiser `controller-no-repository`, `service-downward-only`, `repository-downward-only` |
| `domain_is_framework_free` | dependency-cruiser `domain-isolation` (anything outside `domain/`, packages included; Node built-ins allowed) |
| — | oxlint `parameter-properties` (readonly only), `no-non-null-assertion`, `no-explicit-any`, `explicit-module-boundary-types`, `no-floating-promises`, `max-lines-per-function` (20), `max-lines` (300) |

A violating import fails with the rule's name, for example:

```text
error controller-no-repository: src/calculator/controller/x.ts → src/calculator/repository/calculation.repository.ts
```

## Tests

| Java test | TypeScript test |
|---|---|
| `CalculationTest` | `src/calculator/domain/calculation.spec.ts` |
| `CalculatorServiceTest` | `src/calculator/service/calculator.service.spec.ts` |
| `OpenApiContractTest` | `test/open-api.e2e-spec.ts` |
| `ArchitectureTest` | `.dependency-cruiser.json` and `.oxlintrc.json` (see above) |

`test/calculator.e2e-spec.ts` has no Java counterpart. It pins the boundary
behaviour (`201` with a lower-case operator, and `400` for malformed JSON, a
missing operand, or an unknown operator).

## Deliberate differences from the Java reference

- **Missing operand.** Java's primitive `double` turns a missing operand into
  `0.0`, so `{"operator": "ADD", "operandB": 3}` returns `201`. The zod schema
  requires both operands and returns `400`.
- **Missing operator.** Java returns `500` from `Objects.requireNonNull`; the
  schema returns `400`.
- **Numeric strings.** Jackson coerces `"6"` to `6.0`; `z.number()` rejects it
  with `400`.
- **Content type.** Spring returns `415` for a body that is not
  `application/json`; Nest does not parse it, and the schema returns `400`.
- **Division by zero.** Both return `500`; Nest's body is
  `{"statusCode": 500, "message": "Internal server error"}`.
- **Error body.** Nest's default `400` body is
  `{message, error: "Bad Request", statusCode}`; for malformed JSON the message
  is the JSON parser's.
