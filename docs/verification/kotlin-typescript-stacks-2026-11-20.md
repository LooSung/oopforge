# Experimental Kotlin Spring and TypeScript Next.js stacks — 2026-11-20

- Candidate: branch `feat/kotlin-spring` (references at `2db9fdb`, plus the
  skills and docs commit that adds this record). Not yet run on GitHub
  Actions.
- Machine: macOS, JDK 21.0.7 (Temurin), Node 24.22.1, npm 11.19.1, Claude Code
  2.1.311. CI pins Node 22 for the TypeScript job.
- Toolchains: Kotlin Gradle plugin 2.4.21, Spring Boot 3.5.14, Gradle 8.12;
  Next.js 15.5.29, TypeScript 5.8.3, Vitest 3.2.7, ESLint 9.39.5, zod 4.6.7,
  `@asteasolutions/zod-to-openapi` 9.1.0.

## Kotlin probes (scratch project, before the skeleton)

| Check | Result |
|---|---|
| Kotlin 2.4.21 + Boot 3.5.14 + Gradle 8.12 + JDK 21 build and tests | Pass; KGP warns Gradle 8.12 is deprecated and Kotlin 2.5.0 needs 8.14.4 |
| Private-constructor `data class`: outside `copy(amount = -1)` | Compiles with a warning — `copy()` stays public |
| Same with `@ConsistentCopyVisibility` | Fails to compile: "it is private" |
| ArchUnit on Kotlin bytecode, seeded domain → web dependency | Rule fails as expected |
| Bare `@NotNull` on a constructor property, missing field | Kotlin 2.0.21: 200 (constraint skipped); 2.4.21: 400 |
| `@field:NotNull`, missing field | 400 on both |
| Non-null `Double` request field, missing operand | `0.0`, like Java, until `fail-on-null-for-primitives: true` (then 400) |

## References

| Reference | Tests | Second tool |
|---|---|---|
| `calculator-kotlin-layered` | 6 pass | ArchUnit |
| `calculator-kotlin-hexagonal` | 17 pass (same count as Java) | ArchUnit |
| `calculator-kotlin-hexagonal-cqrs` | 8 pass | ArchUnit |
| `calculator-typescript-next-layered` | 8 pass (4 ported, 4 boundary) | ESLint zones |
| `calculator-typescript-next-hexagonal` | 20 pass (15 ported, 5 added) | ESLint zones |
| `calculator-typescript-next-hexagonal-cqrs` | 13 pass (5 ported, 8 adapter) | ESLint zones |

- TypeScript `npm run check` (lint, `tsc --noEmit`, Vitest, `next build`) is
  green from a clean `.next` in each project.
- Every ESLint zone was seen failing on a seeded import, then cleared.
  Removing the `import/resolver` setting made a seeded violation pass, which
  is why the skill requires it.
- `archlint.py` passes on the Kotlin and TypeScript layered and CQRS
  references; the domain review reports nothing on the 186 `.kt`/`.ts` files
  of all six.

## Enforcement

- `test-archlint.py`: 24 cases, including Kotlin, TypeScript, and mixed
  Java + Kotlin roots. Each Kotlin and TypeScript rule has a fixture that must
  fail; before this change a Kotlin- or TypeScript-only root passed with zero
  checks.
- `test-review-extended.py`: Kotlin and TypeScript detector cases (constructor
  and body `var`, readonly, `#private`, locals, `.tsx` exclusion, block and
  expression method spans).
- Java/Python regression: `review.detectors.scan` over the six existing
  references plus seeded violations for every per-language branch gives
  identical findings before and after every enforcement commit.

## Harness

| Check | Result |
|---|---|
| `harness-smoke.sh live claude`: Test routing positive, safe-mode negative control | Pass, pass |
| `/oopforge:consult`, candidate via `--plugin-dir`, plan mode: Kotlin order API | `kotlin-spring-layered` (hexagonal if ports are needed), experimental |
| Same: business rules behind Next.js route handlers | `typescript-next-layered`/`-hexagonal`, experimental |
| Same: NestJS order API | Not supported; points to the supported stacks |

Not run: Codex CLI and Cursor Agent CLI live probes, a FuseForge connected run
with a Kotlin or Next.js backend, and GitHub Actions on the branch.
