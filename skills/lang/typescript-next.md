---
name: typescript-next
description: Express the OOPforge Hard Rules in TypeScript server code inside a Next.js App Router app — src/server layers, one-line route files, server actions, zod boundaries, readonly domain state.
tags: [typescript, nextjs, domain, validation]
stability: experimental
---

# TypeScript Next.js (server code)

## When to use

Use this with `skeleton/backend-skeleton.md` for a `typescript-next-*` stack:
business rules that run on the server of a Next.js App Router app. The stack is
**experimental**: the references, `archlint.py`, the domain review, and ESLint
zones cover it, but it sits outside the 1.x compatibility promise. NestJS,
Express, and other Node backends are not this stack.

## Ownership inside one Next.js app

| Area | Owner |
|---|---|
| `src/server/**` — domain, application, repositories, adapters | OOPforge |
| `src/app/**/route.ts` and server actions — thin inbound adapters | OOPforge |
| Pages, layouts, components, client state (`.tsx`) | Compforge |

Compforge's `react-next-app` zones already forbid `features/` and `shared/`
from importing `src/server/`. A Server Component may call an application
service's public entry and pass serializable data down.

## Toolchain

Same versions as Compforge's `todo-react-next`: Next.js 15 App Router, React 19,
TypeScript `strict`, Vitest, ESLint 9 with typescript-eslint and
`import/no-restricted-paths` (`skeleton/lint-enforcement-typescript.md`). Add
zod 4 for boundaries and `@asteasolutions/zod-to-openapi` for the document.
Route handlers run on the Node runtime.

## Inbound adapters

- A route file is one line that re-exports the handler:
  `export { POST } from '../../../../server/calculator/controller/calculatorController';`
  The handler lives in `controller/` (layered) or `adapter/web/` (hexagonal).
- Route handlers expose OpenAPI: build the document from the zod schemas and
  serve it at `/v3/api-docs`.
- A server action (`'use server'`) is internal RPC: exempt from OpenAPI,
  validated with the same zod schema, calling the same application service.
- Correlation ids, idempotency, and error mapping are wrappers in the web
  adapter, not Next.js middleware: middleware runs on the Edge runtime and
  cannot share in-memory state with the handler.
- Use relative imports inside `src/`. The ESLint resolver does not follow `@/`
  aliases, so an aliased import silently escapes the zones.

## Hard Rules in TypeScript

| Hard Rule | TypeScript form | Checked by |
|---|---|---|
| Domain framework imports: 0 | no `next`, `react`, `zod`, Prisma, Drizzle, TypeORM in `domain/` | review, ESLint zones |
| No public setters | fields are `readonly` or private behind behaviour methods; constructor properties are `readonly` | review |
| Factory guards invariants | `private constructor` plus a `static` factory | code review |
| Boundary collections are copied | `ReadonlyArray<T>` is compile-time only — return `[...items]` | code review |
| Intent in types | exported functions and public methods declare return types; no `any`; no `!` in `domain/` | archlint (command services), ESLint, code review |

The transaction boundary is an explicit `TransactionRunner` (unit-of-work)
port owned by the application service; there is no framework annotation.

## Ports and wiring

- Outbound ports — repositories, the transaction runner, the outbox — return
  `Promise`: a real Node.js driver cannot implement a synchronous save. Domain
  classes stay synchronous. An in-memory transaction adapter uses
  `AsyncLocalStorage` where Java uses a `ThreadLocal`.
- Wire the graph at module level in `config/` (layered: `core/`) and import
  `server-only` there. Do not keep it on `globalThis`: a kept graph survives a
  module reload and throws error classes from the old evaluation, so
  `instanceof` stops matching. Under `next dev`, a recompile can reset
  in-memory stores; durable adapters do not have that problem.
- Map domain failures through one dedicated error class (the reference uses
  `DomainRuleViolation` → 422), not every built-in `RangeError`.

## Files and names

- `.ts` only. `.tsx` is UI and is left to Compforge's checks.
- camelCase files named after their main export. Layered folders:
  `controller/ service/ repository/ domain/`; hexagonal uses the Java names;
  CQRS files end in `CommandService.ts` or `QueryService.ts`.
- Tests mirror production under `tests/`, call route handlers with
  `new Request(...)`, and replace ArchUnit with the ESLint zones.
- Import `server-only` in the composition module; alias it to an empty module
  in `vitest.config.ts`.

## What the checks cannot see

- Arrow functions with expression bodies and test callbacks are not measured
  for length.
- archlint L2 matches a repository *path* in an import; an alias hides it.
- Array copies and non-null assertions are code-review items.

## Prohibited

- Domain imports from `next`, `react`, `zod`, or an ORM.
- A public mutable field, or a `public` constructor property without
  `readonly`, in `domain/`.
- Business logic in a route file, server action, or `.tsx` module.
- Next.js middleware holding request state the handler depends on.
