---
name: typescript-nestjs
description: Express the OOPforge Hard Rules in a TypeScript NestJS backend — layer folders inside feature modules, abstract-class ports, Zod boundaries, readonly domain state, and how to work next to NestJS's own agent skills.
tags: [typescript, nestjs, domain, validation]
stability: experimental
---

# TypeScript NestJS

## When to use

Use this with `skeleton/backend-skeleton.md` for a `typescript-nestjs-*` stack.
The stack is **experimental**: the references, `archlint.py`, the domain
review, dependency-cruiser, and oxlint cover it, but it sits outside the 1.x
compatibility promise. Express without Nest and plain Node backends are not
this stack; a Next.js app belongs to Compforge.

## Toolchain

The references use what `nest new --strict` generates on NestJS 12: ESM
(`"type": "module"`, `nodenext`, `.js` import suffixes), TypeScript 6
`strict`, Vitest 4 with Supertest, and oxlint. They add Zod 4,
`@nestjs/swagger`, and dependency-cruiser, and leave out `@nestjs/observe`.

An older project (CommonJS, Jest, ESLint) keeps its runner and linter. The
Hard Rules, folder layout, and `.dependency-cruiser.json` do not change; the
references do not cover that toolchain.

## Next to NestJS's own agent skills

`nest new` also writes `AGENTS.md`, `CLAUDE.md`, and first-party skills
(`nestjs`, `nestjs-feature`, `nestjs-data`, `nestjs-testing`,
`nestjs-production`, `nestjs-auth`). Keep them, and split the work:

| Question | Follow |
|---|---|
| Framework API: modules, pipes, guards, interceptors, testing module, config | NestJS skills |
| Where a rule lives, which layer imports which, Aggregate and port design | OOPforge |
| ORM entities and schemas (`nestjs-data`) | NestJS mechanics, but inside the persistence adapter behind a mapper; services depend on a repository port, never on the database client |

## Layout

- One feature module per bounded context: `src/<context>/<context>.module.ts`
  is the composition and the only file that names every layer.
- Layer folders inside the module. `nest g resource` puts controller and
  service side by side; move them into `controller/ service/ repository/
  domain/` (layered) or `domain/ application/ adapter/` (hexagonal).
  `archlint.py layered` reports a flat module.
- Kebab-case `name.type.ts` files: `calculator.controller.ts`,
  `calculation.repository.ts`, `calculation-command.service.ts`,
  `history-query.service.ts`. archlint reads the role from these names.
- Unit specs sit next to the code (`*.spec.ts`); HTTP tests run the app
  through `AppModule` with Supertest in `test/*.e2e-spec.ts`.

## Ports and wiring

- A port is an **abstract class**, not an interface: Nest injects by a runtime
  token, and an interface does not exist at runtime. Bind it in the module:
  `{ provide: CalculationRepository, useClass: InMemoryCalculationRepository }`.
- Outbound ports return `Promise`: a real Node.js driver cannot implement a
  synchronous save. Domain classes stay synchronous.
- Application services and adapters are `@Injectable()`; the domain is plain
  TypeScript. The transaction boundary is an explicit `TransactionRunner` port;
  an in-memory adapter uses `AsyncLocalStorage`.
- `@nestjs/cqrs` command and query handlers are allowed, but archlint checks
  only `*-command.service.ts` and `*-query.service.ts`.

## Boundaries

- Validate bodies with a Zod schema: `@Body({ schema })` and the built-in
  `StandardSchemaValidationPipe`. A missing or mistyped field is `400`.
  class-validator DTOs also work; keep them in the web adapter.
- `@nestjs/swagger` reads the Zod schemas; serve the document at
  `/v3/api-docs` (`SwaggerModule.setup(..., { jsonDocumentUrl: 'v3/api-docs' })`).
- Put the pipe and the document in one `configureApp(app)` used by `main.ts`
  and the e2e tests.
- Response schemas: `@ApiResponse({ standardSchema })` takes a Zod schema. A
  query parameter with a default is documented as required unless
  `@ApiQuery({ required: false })` says otherwise.
- Map domain failures through one error class in a global exception filter
  (the hexagonal reference maps `DomainRuleViolation` to 422 and every 400 to
  one safe body).
- Correlation ids and audit that must also cover malformed JSON and 404s run
  as Express middleware registered in `configureApp` before Nest's body
  parser; idempotency stays in the web adapter.

## Hard Rules in TypeScript

| Hard Rule | NestJS form | Checked by |
|---|---|---|
| Domain framework imports: 0 | no `@nestjs/*`, `zod`, `class-validator`, `class-transformer`, ORM, or other layer in `domain/` | review, dependency-cruiser |
| No public setters | fields `readonly` or private behind behaviour methods; constructor properties `readonly` | review, oxlint `parameter-properties` |
| Factory guards invariants | `private constructor` plus a `static` factory | code review |
| Boundary collections are copied | `ReadonlyArray<T>` is compile-time only — return `[...items]` | code review |
| Intent in types | exported functions and public methods declare return types; no `any`; no `!` | archlint (command services), oxlint |

## What the checks cannot see

- Arrow functions with expression bodies and test callbacks are not measured
  for length by the review; oxlint measures every function in production code.
- archlint L2 matches a repository *path* in an import; a path alias hides it.
- `@nestjs/cqrs` handlers, array copies, and factories are code-review items.

## Prohibited

- Domain imports from `@nestjs/*`, Zod, class-validator, class-transformer, or
  an ORM; entity decorators on domain classes.
- A service that injects a database client or ORM repository directly instead
  of a port.
- Business logic in a controller, interceptor, guard, or pipe.
- A flat feature module (controller, service, repository in one folder) on a
  layered stack.
