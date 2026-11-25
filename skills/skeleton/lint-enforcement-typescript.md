---
name: lint-enforcement-typescript
description: Enforce TypeScript NestJS layer boundaries in CI with dependency-cruiser and the code-level Hard Rules with oxlint, on top of archlint, the way ArchUnit and import-linter do for the other stacks.
tags: [lint, ci, typescript, nestjs, layered, hexagonal]
stability: experimental
---

# Lint Enforcement — TypeScript NestJS

## When to use

For a `typescript-nestjs-*` stack, right after the skeleton. It uses the same
two layers as `lint-enforcement.md`:

1. **Fast stdlib gate** — `scripts/ci/archlint.py layered|cqrs <app>/src`
   checks layer folders, a controller importing a repository path, and the
   CQRS rules. It skips `*.spec.ts`, `*-spec.ts`, `dist/`, and `node_modules/`.
2. **Standard tools** — dependency-cruiser for import boundaries (the
   ArchUnit and import-linter role) and oxlint, which `nest new` installs, for
   the code-level Hard Rules.

Do not invent a tool. Copy the matching configs and change only their paths.

## Canonical templates

| Stack | Canonical files | Boundary rules |
|---|---|---|
| `typescript-nestjs-layered` | `examples/calculator-typescript-nestjs-layered/.dependency-cruiser.json`, `.oxlintrc.json` | domain isolated; controller never imports repository; service and repository import downward only |
| `typescript-nestjs-hexagonal` | `examples/calculator-typescript-nestjs-hexagonal/.dependency-cruiser.json` | `domain-isolation`; `application-no-adapter`, `application-no-composition` (`*.module.ts`, `main.ts`, `configure-app.ts`), `application-no-transport` (zod, express, swagger) |
| CQRS variant | `examples/calculator-typescript-nestjs-hexagonal-cqrs/.dependency-cruiser.json` | `domain-isolation`, `application-no-adapter` (module files included), `command-no-query`, `query-no-command` |

## Rule shape

```json
{
  "name": "domain-isolation",
  "severity": "error",
  "from": { "path": "^src/[^/]+/domain/" },
  "to": { "pathNot": "^src/[^/]+/domain/", "dependencyTypesNot": ["core"] }
}
```

- `tsPreCompilationDeps: true` is required: without it, `import type` edges
  disappear and a type-only repository import in a controller passes (the
  layered reference proved it with a seeded import). dependency-cruiser
  resolves ESM `.js` suffixes to the `.ts` sources; `options.tsConfig` adds
  the project's path settings.
- `pathNot` on `domain/` also forbids every npm package, so a framework import
  fails the same rule. `dependencyTypesNot: ["core"]` keeps Node built-ins.
- Exclude `\.spec\.ts$` from the cruise; tests may wire layers together.
- Name each rule for the Hard Rule it guards, so the failure says which broke.

oxlint carries `max-lines` 300, `max-lines-per-function` 20 (off for specs and
`test/`), `typescript/no-explicit-any`, `no-non-null-assertion`,
`explicit-module-boundary-types`, `parameter-properties` (readonly only), and
`no-floating-promises`. Run it with `--type-aware`.

## Prove the rules fire

A rule that never failed is unverified. After copying the configs:

1. Add one violating import, for example a repository import in a
   controller, and one oversized function.
2. Run `npm run lint`; dependency-cruiser must name the rule and exit
   non-zero, and oxlint must report the function.
3. Remove both.

## CI

- Each reference's `npm run check` runs oxlint and dependency-cruiser, `tsc
  --noEmit`, the unit and e2e Vitest suites, and `nest build`; the `typescript`
  job in `.github/workflows/examples.yml` runs it on Node 22.
- `.github/workflows/arch-lint.yml` runs archlint on the layered and CQRS
  references' `src/`.

## Prohibited

- A config without `tsPreCompilationDeps: true`.
- Path aliases (`@/…`) inside `src/` without checking that dependency-cruiser
  resolves them; archlint L2 cannot see through an alias.
- Turning a rule off to make a build pass; move the import instead.
