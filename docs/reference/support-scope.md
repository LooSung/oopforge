# OOPforge support scope

This document records the currently tested OOPforge scope. It is a compatibility
guide for a skill pack, not a hosted-service SLA.

## Supported backend scope

- Java with Spring: layered and hexagonal references.
- Python with FastAPI: layered and hexagonal references.
- Java and Python hexagonal CQRS references.
- Python Pydantic v2 boundaries with mypy and the official Pydantic plugin.
- Domain modeling, use-case and transaction boundaries, Domain Events,
  transactional outbox, and opt-in Production Readiness.

## Experimental backend scope

These stacks have runnable layered, hexagonal, and hexagonal CQRS references,
`archlint.py` and domain-review coverage, and a second standard tool, but sit
outside the 1.x compatibility promise until promoted
([evidence](../verification/kotlin-typescript-stacks-2026-11-20.md)):

- Kotlin with Spring (`lang/kotlin-spring.md`), checked with ArchUnit.
- TypeScript server code inside a Next.js App Router app — `src/server/`,
  route handlers, server actions (`lang/typescript-next.md`), checked with
  ESLint `import/no-restricted-paths` zones. Next.js pages, components, and
  client state belong to Compforge; NestJS, Express, and other Node backends
  are not supported.

The calculator projects are executable references, not production
frameworks. Their in-memory persistence, outbox, idempotency, and audit adapters
must be replaced by durable shared infrastructure for multi-instance deployment.

## Canonical harness paths

| Harness | Supported load path | Invocation |
|---|---|---|
| Claude Code | `~/.claude/skills/oopforge` and `~/.claude/commands/oopforge` symlinks | `/oopforge:craft …`, `/oopforge:refactor …`, `/oopforge:consult …`, `/oopforge:test …`, `/oopforge:crucible …`, `/oopforge:review …`, or `/oopforge:jira …` |
| Claude Code | `forge` plugin marketplace: `/plugin marketplace add LooSung/oopforge`, then `/plugin install oopforge@forge` | same slash commands |
| Codex CLI | `~/.codex/skills/oopforge` symlink | select `oopforge`, then use the matching `craft`, `refactor`, `consult`, `test`, `crucible`, `review`, or `jira` natural-language intent |
| Cursor Agent CLI | explicit `--plugin-dir` | use the matching `craft`, `refactor`, `consult`, `test`, `crucible`, `review`, or `jira` natural-language intent |
| Cursor Agent CLI | `.cursor/skills/oopforge` plus pack `--add-dir` | same natural-language intents |

The marketplace path is **experimental**: install, update, removal, and
positive live probes passed, but a clean negative control is still pending
([marketplace-2026-11-19](../verification/marketplace-2026-11-19.md)). Use
one Claude Code path, not both: the symlinks and the plugin register the same
commands.

Cursor directory auto-discovery, Cursor headless OOPforge `/` commands, and
automatic Cursor setup are not currently supported paths.

Cursor Agent `2026.08.11-e8db854` discovers an existing
`~/.claude/skills/oopforge` installation even in a no-plugin workspace. The
live smoke therefore injects a run-specific probe into temporary candidate
skills. This distinguishes both canonical candidate paths from other global
OOPforge installations without changing the user's configuration.

`doctor.sh` validates files and links. It does not prove agent activation.
Maintainers can run `scripts/ci/harness-smoke.sh live <harness>` with their own
local CLI authentication. A positive run must report the Test route, `auto`
level, and production-code boundary; an isolated negative control must report
`OOPFORGE_NOT_LOADED`.
Claude and Codex can reuse their local login state. Cursor's isolated live probe
reuses its OS credential-store token through sanitized login metadata, or a
local `CURSOR_API_KEY` when present. No provider credential is stored in the
repository.

## Automated evidence

- Pull requests and pushes run packaging/static smoke without provider
  credentials.
- Authenticated live probes are optional maintainer checks, not hosted CI gates.
- Reference, proof, domain-review, and CI detectors use the canonical finding
  IDs documented by the proof protocol.

## Versioning and compatibility

The pack version is the shared version in the three plugin manifests, Git tag,
and changelog. Skill maturity is tracked separately in
[`skills/stability.json`](../../skills/stability.json).

OOPforge 1.x keeps this core usage contract compatible:

- the canonical harness load paths and Craft invocation above;
- the Discovery → Design → Delivery Plan → Skeleton → Implement → Test stage
  order and its human checkpoints;
- the meaning of existing Hard Rules and the OOP Contract fields;
- stable skill paths used by the default execution routes.

For the pack version:

- **major** removes or incompatibly changes that core usage contract;
- **minor** adds compatible skills, checks, examples, stacks, or load paths;
- **patch** corrects guidance, packaging, tests, or documentation without
  changing the contract.

`stable` is a maturity signal, not a promise that every sentence is frozen.
Stable guidance may improve within 1.x when the core contract remains
compatible and user-visible changes are documented. Experimental skills are
outside the compatibility promise.

CLI vendors may make a previously verified path unavailable. Until a clean
local positive/negative smoke re-establishes it, documentation should mark that
path unverified rather than claiming support.

## Not currently supported

Saga orchestration, an OOPforge MCP server, additional languages, a listing
in the official Claude plugin directory, a standalone OOPforge CLI, frontend/mobile work, and a claim that
OOPforge universally improves agent output are outside this scope.
