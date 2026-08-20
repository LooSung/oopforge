# OOPforge 1.x support contract

This document is the canonical support boundary for OOPforge 1.x.

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
installation, and automatic Cursor setup are not supported 1.x paths.

`doctor.sh` validates files and links. It does not prove agent activation.
Activation evidence comes from `scripts/ci/harness-smoke.sh`: a positive run
must report `OOPFORGE_LOADED`, and an isolated negative control must report
`OOPFORGE_NOT_LOADED`.

## Automated evidence

- Pull requests block on packaging/static smoke with no provider credentials.
- Tag, schedule, and manual live workflows run authenticated positive and
  negative controls for all three harnesses.
- A missing live-smoke credential is a failed gate, not a skipped success.
- Reference, proof, domain-review, and CI detectors use the canonical finding
  IDs documented by the proof protocol.

Required repository secrets are `ANTHROPIC_API_KEY` or
`CLAUDE_CODE_OAUTH_TOKEN`, `OPENAI_API_KEY`, and `CURSOR_API_KEY`.

## Compatibility

The paths in [`skills/stability.json`](../skills/stability.json) are stable for
1.x. Patch releases correct claims or regressions without changing the
contract. Minor releases may add optional, backward-compatible guidance.
Removing a stable skill, checkpoint, hard rule, stack, or canonical harness
path requires the next major version.

CLI vendors may make a previously verified path unavailable. Until a clean
positive/negative smoke re-establishes it, documentation must mark that path
unverified rather than claiming support.

## Not supported in 1.x

Saga orchestration, an OOPforge MCP server, additional languages, marketplace
publication, a standalone OOPforge CLI, frontend/mobile work, and a claim that
OOPforge universally improves agent output are outside this contract.
