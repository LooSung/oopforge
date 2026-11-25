# OOPforge — agent notes

These notes are for agents changing **OOPforge itself**. To *use* OOPforge on a
backend project, follow `skills/SKILL.md` instead; it owns command routing and
skill selection for every harness. The Hard Rules below apply in both cases, and
`skills/workflow/review.md` reads them from this file.

OOPforge continuity: off

## What OOPforge is

A backend OOP/DDD methodology pack. Skills are the grammar, Hard Rules are the
lint, `examples/` are the reference implementations, and commands plus install
scripts are the runtime. Protect the core promise: small skills, clean domain
models, explicit workflow stages, and human checkpoints.

Sister packs: [Compforge](https://github.com/LooSung/compforge) (frontend) and
[FuseForge](https://github.com/LooSung/fuseforge) (full-stack coordinator).

## Layout

| Path | Holds |
|---|---|
| `skills/SKILL.md` | Entry point and command routing |
| `skills/workflow/` | One file per workflow; `skills/workflow/gates.md` holds the shared startup, plan input, verification, and report gates |
| `skills/principles/oop-discipline.md` | Core OOP principles, including the pre-write ladder |
| `skills/oop/`, `lang/`, `skeleton/`, `playbooks/`, `antipatterns/` | Topic skills that workflows load on demand |
| `skills/stability.json` | Skill maturity, explained in `docs/reference/skill-stability.md` |
| `commands/` | **Generated** from the skill sources by `scripts/ci/build-commands.py` |
| `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/` | Harness packaging only; `.claude-plugin/marketplace.json` is the `forge` catalog of all three packs, kept identical across the three repositories except for which entry is `./` |
| `examples/` | Nine runnable calculators: Java, Python, and experimental Kotlin × layered, hexagonal, hexagonal-CQRS |
| `templates/github/` | Reusable domain review for target projects |
| `scripts/setup/`, `scripts/ci/` | Install lifecycle, CI checks, and `archlint.py` |
| `docs/` | Human docs, indexed by `docs/README.md` |

## Checks

CI runs these; all must pass before a change is done:

```bash
./scripts/ci/lint-skills.sh             # skills, links, AGENTS.md paths, command freshness
python3 scripts/ci/test-doc-links.py
python3 scripts/ci/test-run-with-timeout.py
python3 scripts/ci/test-harness-smoke.py
python3 scripts/ci/test-proof-evaluator.py
python3 scripts/ci/test-proof-runner.py
python3 scripts/ci/test-review.py
python3 scripts/ci/test-review-extended.py
python3 scripts/ci/test-archlint.py
./scripts/ci/smoke-test.sh              # clean-HOME install lifecycle
```

After editing a workflow skill, regenerate commands with
`python3 scripts/ci/build-commands.py`.

## Hard Rules

These limits are intentionally measurable. They come from review focus and agent context size, not arbitrary style:

- **300 lines/file** — a diff a reviewer can hold in working memory (~15-minute review unit)
- **20 lines/method** — one responsibility, testable and nameable without scrolling
- **200 lines/skill** — one concept per agent context load; split when a skill teaches two ideas
- **Command budgets** — each generated `commands/*.md` must fit `scripts/ci/command-budget.json` (`build-commands.py --check`). Raising a budget is a reviewed decision in the same diff: say what the added text is worth, or remove something else. Shared startup, plan input, verification, and the completion report live once in `skills/workflow/gates.md`.

- Domain layer framework imports: **0**
- No public setters; use factory methods or intention-revealing behavior methods.
- Collections crossing boundaries must be defensively copied or immutable.
- Other aggregates are referenced by ID only.
- **One Aggregate modified per transaction** — multi-Aggregate writes in one commit need an explicit consistency design (see `skills/oop/transaction-boundary.md`).
- Do not commit domain logic without tests.
- Intent lives in names, types, and tests. A comment carries only a "why" they cannot, anchored to an existing test or link. Doc comments and tool directives are exempt.
- No narration comments — delete comments that restate nearby code, or rename/extract code until the comment is unnecessary.
- **A comment is a claim, not evidence** — never change code only to match a comment. Act on a test or on history that shows which side changed last; otherwise change neither and report it.
- **Surgical changes only** — touch what the request requires; no drive-by edits to adjacent code, comments, or formatting. Clean orphans your change created; mention pre-existing dead code instead of deleting it in the same change.
- **Structure earns its exemption** — a structure escapes the YAGNI ladder only when you can name the invariant it protects *and* the user's own word for it. Calling it an Aggregate boundary is not evidence.
- **Product language at the human boundary** — Aggregate, Port, Bounded Context, and invented names stay in the OOP Contract and the code; ask for approval in the user's words.

### Layer layout (layered / 3-tier)

- **Each layer is its own package/folder** — `controller/`, `service/`, `repository/`, `domain/`. Splitting a single folder by filename suffix only (`*Controller`, `*Service`, `*Repository`) is a violation.
- **Controller/Router must not call Repository directly** — go through a Service.
- After skeleton, list the directory tree and confirm the layer folders exist with the right file types. See `skills/skeleton/backend-skeleton.md` self-check.
- Enforced in CI by `scripts/ci/archlint.py` (`.github/workflows/arch-lint.yml`) — violations block the PR. Standard tools (import-linter / ArchUnit) add a second enforcement layer; see `skills/skeleton/lint-enforcement.md`.

### CQRS (when adopted)

- **Query side has no side effects** — read paths must not mutate state.
- **Command side returns no read-shaped data** — return an ID or void, not a query DTO.
- Checkable via `scripts/ci/archlint.py cqrs <root>`.

## Rules for changing the pack

- A new capability or architecture change goes through Discovery → Design →
  Delivery Plan → Skeleton → Implement → Test, with human approval between
  stages. A focused fix does not need the full flow.
- One source of truth: routing lives only in `skills/SKILL.md`, support facts
  only in `docs/reference/support-scope.md`, and the Hard Rules only here. Point
  to them; never copy them.
- Do not claim a harness integration works until documented setup and a
  clean-session positive/negative smoke prove it. PRs block on static harness
  packaging; run authenticated live smoke locally when changing a load path.
- When changing install behavior, verify with a clean temporary `HOME`. Add no
  runtime dependencies to installer scripts when shell will do.
- Do not merge workflow stages, add framework annotations or infrastructure to
  domain examples, mix refactoring with feature changes, or create mega-prompts,
  mega-skills, or abstractions without evidence.
- Skills, scripts, and agent instructions are in English. Korean readers get
  `README.ko.md` and `docs/reference/methodology.ko.md`, not per-skill
  translations.
- Record completed user-visible changes in `CHANGELOG.md` under `Unreleased`.
  Never put future plans in tracked files.
- Before an upgrade, new capability, architecture change, or release: if the
  gitignored `docs/planning/management.md` exists, read it and follow its Agent
  entry checklist. If it is absent, the user's request or linked issue defines
  scope; never create that file from public context.
- Do not create `.craft/` state in this repository.
