# OOPforge support scope

This document records the currently tested OOPforge scope. It is a compatibility
guide for a skill pack, not a hosted-service SLA.

## Supported backend scope

- Java with Spring: layered and hexagonal references.
- Python with FastAPI: layered and hexagonal references.
- Java and Python hexagonal CQRS references.
- Domain modeling, use-case and transaction boundaries, Domain Events,
  transactional outbox, and opt-in Production Readiness.

The six calculator projects are executable references, not production
frameworks. Their in-memory persistence, outbox, idempotency, and audit adapters
must be replaced by durable shared infrastructure for multi-instance deployment.

## Canonical harness paths

| Harness | Supported load path | Craft invocation |
|---|---|---|
| Claude Code | `~/.claude/skills/oopforge` and `~/.claude/commands/oopforge` symlinks | `/oopforge:craft …` |
| Codex CLI | `~/.codex/skills/oopforge` symlink | select `oopforge`, then `Use OOPforge craft: …` |
| Cursor Agent CLI | explicit `--plugin-dir` | `Use OOPforge craft: …` |
| Cursor Agent CLI | `.cursor/skills/oopforge` plus pack `--add-dir` | `Use OOPforge craft: …` |

Cursor directory auto-discovery, Cursor headless `/oopforge:craft`, marketplace
installation, and automatic Cursor setup are not currently supported paths.

`doctor.sh` validates files and links. It does not prove agent activation.
Maintainers can run `scripts/ci/harness-smoke.sh live <harness>` with their own
local CLI authentication. A positive run must report `OOPFORGE_LOADED`, and an
isolated negative control must report `OOPFORGE_NOT_LOADED`.
Claude and Codex can reuse their local login state. Cursor's isolated live probe
requires a local `CURSOR_API_KEY`; no provider credential is stored in the
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

- the canonical harness load paths and Craft invocations above;
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

Saga orchestration, an OOPforge MCP server, additional languages, marketplace
publication, a standalone OOPforge CLI, frontend/mobile work, and a claim that
OOPforge universally improves agent output are outside this scope.
