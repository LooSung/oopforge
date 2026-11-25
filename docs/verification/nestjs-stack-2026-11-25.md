# Experimental TypeScript NestJS stack — 2026-11-25

- Candidate: branch `feat/nestjs` (enforcement `c85c955`, references
  `d37cd42`, `46012db`, `d7da57a`, Next.js removal `772777a`, plus the skills
  and docs commit that adds this record), released as v1.15.0.
- GitHub Actions on pull request #6 at `b645d1a`: Lint, Arch Lint, Domain
  Review, and Harness Packaging pass; Examples run `45571377828` passes all
  twelve jobs, including the three NestJS references on Node 22.
- Machine: macOS, Node 24.22.1, npm 11.19.1. CI pins Node 22 for the
  TypeScript job.
- Toolchain (resolved): NestJS 12.6.0, `@nestjs/cli` 12.0.15, TypeScript
  6.0.3, Vitest 4.1.12 with Vite 8.3.8, Supertest 7.3.2, oxlint 1.95.0,
  dependency-cruiser 18.9.0, Zod 4.6.7, `@nestjs/swagger` 12.1.2.

## Probes (scratch project from `nest new --strict`)

| Check | Result |
|---|---|
| Scaffold unit test, e2e through `AppModule`, `nest build`, oxlint | Pass; constructor injection resolves under Vitest 4 |
| Scaffold extras | `AGENTS.md`, `CLAUDE.md`, six first-party agent skills, `@nestjs/observe` (left out of the references) |
| `@Body({ schema })` + `StandardSchemaValidationPipe`, missing or mistyped operand | 400 |
| `@nestjs/swagger` with a Zod body schema | Request schema appears in `/v3/api-docs` without a converter |
| dependency-cruiser on ESM `.js` imports, seeded domain → repository and controller → repository | Both rules fire, exit 2; clean tree exit 0 |
| Same without `options.tsConfig` | Still resolves `.js` → `.ts` |
| Same with `tsPreCompilationDeps: false`, type-only repository import | Passes silently — why the skill requires `true` |
| `node:crypto` import in `domain/` | Allowed by `dependencyTypesNot: ["core"]` |

## Unmodified enforcement on a seeded NestJS tree (before `c85c955`)

- `archlint layered` failed NestJS's flat feature folder (intended) but also
  tagged co-located `*.spec.ts` files as layers.
- `archlint cqrs` passed `calculate.command-service.ts` without a return type.
- The domain review missed `@nestjs/common`, `class-validator`, and
  `class-transformer` imports in `domain/`, and a decorated public field.

`c85c955` fixes each; every new fixture fails on the previous code. Java,
Kotlin, and Python findings over the existing references are unchanged.

## References

| Reference | Tests | Second tools |
|---|---|---|
| `calculator-typescript-nestjs-layered` | 8 pass (3 unit, 5 e2e) | dependency-cruiser, oxlint |
| `calculator-typescript-nestjs-hexagonal` | 18 pass (6 unit, 12 e2e: 15 ported, 3 added) | dependency-cruiser, oxlint |
| `calculator-typescript-nestjs-hexagonal-cqrs` | 13 pass (4 unit, 9 e2e, all ported) | dependency-cruiser, oxlint |

- `npm run check` (oxlint, dependency-cruiser, `tsc --noEmit`, unit and e2e
  Vitest, `nest build`) exits 0 in each.
- Every dependency-cruiser rule was seen failing on a seeded import; the
  layered oxlint rules (`max-lines-per-function`, `no-explicit-any`,
  `no-non-null-assertion`, `explicit-module-boundary-types`,
  `parameter-properties`) each failed on a seeded file.
- `archlint.py layered` passes on the layered reference and `archlint.py cqrs`
  on the CQRS reference; seeded C1 and C2 violations fail it.
- The domain review reports nothing on the 101 `.ts` files of all three.
- Boundary behaviour was checked with curl against `node dist/main.js`; each
  README lists the differences from Java (missing operand `400`, Nest error
  bodies, malformed JSON message).

## Next.js stack removal

`772777a` removes the three `calculator-typescript-next-*` references,
`lang/typescript-next.md`, the Next.js ESLint zone skill, the `route.ts`
archlint rule, and their CI steps. The
[2026-11-20 record](kotlin-typescript-stacks-2026-11-20.md) stays as history.

## Harness

Claude Code 2.1.325.

| Check | Result |
|---|---|
| `harness-smoke.sh live claude`: Test routing positive, safe-mode negative control | Pass, pass |
| `/oopforge:consult`, candidate via `--plugin-dir`, plan mode: NestJS order API | `typescript-nestjs-layered`/`-hexagonal`, experimental, choice left to the user |
| Same: business rules in Next.js route handlers and server actions | No OOPforge stack; the Next.js app is Compforge's; move the rules to a separate backend such as NestJS |
| Same: Express order API | Not supported; NestJS, Java Spring, or Python FastAPI offered |

The first Express run read the installed v1.14.0 skill under
`~/.claude/skills/oopforge` instead of the candidate: its conclusion was the
same, but it offered the removed Next.js stack. The rerun read the candidate.
An installed copy can shadow `--plugin-dir` for skill reads.

Not run: Codex CLI and Cursor Agent CLI live probes, and a FuseForge connected
run with a NestJS backend.
