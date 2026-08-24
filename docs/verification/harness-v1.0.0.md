# v1.0.0 harness verification

## Candidate

- Commit: `e5d7dd2`
- Date: 2026-08-21
- Policy: local authenticated checks; no repository provider secrets

## Activation and isolation

| Harness | CLI version | Positive | Negative | Status |
|---|---|---|---|---|
| Claude Code | 2.1.212 | installed command loaded | safe mode isolated | pass |
| Codex CLI | 0.148.0 | global skill loaded | no-skill home isolated | pass |
| Cursor Agent CLI | 2026.08.11-e8db854 | plugin-dir and project-local loaded | clean workspace isolated | pass |

Positive controls require `OOPFORGE_LOADED`, `Assumptions`, and `OOP Contract`.
Negative controls require `OOPFORGE_NOT_LOADED` without `OOPFORGE_LOADED`.

## Advisory Craft routing

| Harness | Request | Expected route | Status |
|---|---|---|---|
| Claude Code | Java Email value object, advisory only | `skills/oop/domain-model.md` | pass |
| Codex CLI | Java Email value object, advisory only | `skills/oop/domain-model.md` | pass |
| Cursor Agent CLI | Java Email value object, advisory only | `skills/oop/domain-model.md` | pass |

## Release decision

All three supported harnesses passed activation, isolation, and advisory Craft
routing on the candidate. Repository and reference-project gates also passed
before v1.0.0 was released.
