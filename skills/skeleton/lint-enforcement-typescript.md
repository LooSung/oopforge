---
name: lint-enforcement-typescript
description: Enforce TypeScript Next.js server layer boundaries in CI with ESLint import zones on top of archlint, the way ArchUnit and import-linter do for the other stacks.
tags: [lint, ci, typescript, nextjs, layered, hexagonal]
stability: experimental
---

# Lint Enforcement — TypeScript Next.js

## When to use

For a `typescript-next-*` stack, right after the skeleton. It uses the same two
layers as `lint-enforcement.md`:

1. **Fast stdlib gate** — `scripts/ci/archlint.py layered|cqrs <app>/src`
   checks layer folders, route files and `controller/` importing a repository
   path, and the CQRS rules.
2. **Standard tool** — ESLint `import/no-restricted-paths`, the mechanism
   Compforge's `react-next-app` template already uses for the UI side.

Do not invent a tool. Copy the matching config and change only its paths.

## Canonical templates

| Stack | Canonical file | Zones |
|---|---|---|
| `typescript-next-layered` | `examples/calculator-typescript-next-layered/eslint.config.js` | domain isolated; controller and `src/app` never import repository; downward-only service and repository |
| `typescript-next-hexagonal` | `examples/calculator-typescript-next-hexagonal/eslint.config.js` | domain isolated; application never imports adapter or config; `src/app` imports only the web adapter |
| CQRS variant | `examples/calculator-typescript-next-hexagonal-cqrs/eslint.config.js` | hexagonal zones plus command and query sides kept apart |

## The resolver line is required

```js
settings: {
  'import/resolver': { node: { extensions: ['.js', '.ts'] } },
},
```

Without it the default resolver cannot resolve `.ts` imports and every zone
passes silently — the layered reference proved it with a negative test. Keep
imports inside `src/` relative: the node resolver does not follow `@/` aliases
either.

## Zone shape

```js
const CALCULATOR = './src/server/calculator';
const zones = [
  {
    target: `${CALCULATOR}/domain`,
    from: './',
    except: [`${CALCULATOR}/domain`],
    message: '[domain-isolation] domain/ imports nothing outside domain/.',
  },
  {
    target: [`${CALCULATOR}/controller`, './src/app'],
    from: `${CALCULATOR}/repository`,
    message: '[controller-no-repository] Go through the service.',
  },
];
```

Name each zone in its message (`[domain-isolation]`) so a failure says which
rule broke. The references add the same Hard Rules as plain ESLint rules:
`no-explicit-any`, `no-non-null-assertion`, `max-lines` 300,
`max-lines-per-function` 20, `explicit-module-boundary-types`, readonly-only
`parameter-properties`, and for `domain/` a framework import ban plus
`no-restricted-syntax` for readonly state and private constructors.

## Prove the zones fire

A zone that never failed is unverified. After copying a config:

1. Add one violating import, for example a repository import in a controller.
2. Run `npm run lint`; it must fail and name the zone.
3. Remove the import.

## CI

- Each reference's `npm run check` runs lint, `tsc --noEmit`, Vitest, and
  `next build`; the `typescript` job in `.github/workflows/examples.yml` runs
  it on Node 22.
- `.github/workflows/arch-lint.yml` runs archlint on the layered and CQRS
  references' `src/`.

## Next to Compforge in one app

When `compforge init` installed `eslint.compforge.config.js`, add the OOPforge
zones as another object in the same flat config array. The two lists target
different folders — Compforge `src/features` and `src/shared`, OOPforge
`src/server` and route files — so both apply without overlap.

## Prohibited

- Zones without the resolver setting.
- `@/` alias imports inside `src/server/`.
- Turning a zone off to make a build pass; move the import instead.
- Linting `.tsx` UI modules with these zones; Compforge owns them.
