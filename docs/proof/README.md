# OOPforge Proof Protocol

This directory defines a reproducible control-versus-OOPforge comparison for
C4. It intentionally separates the experiment design from the results.

No effectiveness claim should be published until both runs and the evaluation
complete successfully.

## Question

Does OOPforge reduce architecture violations and architecture-driven rework
when the same coding agent adds domain behavior to an existing backend?

## Fixed task

Both runs start from an untouched copy of
`examples/calculator-python-hexagonal`.

The agent receives this task:

> Add a void-calculation use case. A calculation may be voided once and only
> within five minutes of being performed. A second void or a late void must be
> rejected. Expose `POST /calculations/{id}/void`; return 404 when the
> calculation does not exist and 409 when the transition is invalid. Persist
> the changed calculation and add domain, use-case, and API tests. Use an
> injectable clock so tests do not depend on sleep or wall-clock timing. Do not
> change unrelated behavior.

This task was chosen because it requires:

- a domain invariant;
- a state transition;
- repository lookup and save behavior;
- application orchestration;
- HTTP error mapping;
- deterministic time-based tests.

It is an existing-domain feature, so OOPforge can use the focused Craft path
without bypassing the human checkpoints required for a new domain.

## Independent variable

The control run uses the coding agent with no OOPforge skill.

The treatment run uses the same coding agent and model with a pinned copy of
OOPforge under the workspace's `.cursor/skills/oopforge`, then routes the
request through Craft. The business requirements are otherwise identical.

Project-local skill delivery was used because, when these pairs were run, clean
headless smoke tests had not proved that `cursor-agent --plugin-dir` loaded
Craft. OOPforge later verified both Cursor paths; see the
[support scope](../support-contract.md). That packaging evidence is separate
from this experiment, which measures the methodology.

## Fixed conditions

- Same model identifier.
- Same Cursor Agent version.
- Same source commit and starter tree.
- Fresh workspace and fresh agent session per run.
- Same sandbox and approval mode.
- No manual edits during either run.
- Same dependency versions and test commands.
- Control runs outside the OOPforge repository so parent `AGENTS.md` rules
  cannot contaminate it.

## Primary measures

Count violations after the first agent response:

1. Business invariant outside the domain model.
2. Framework import under `app/domain`.
3. Presentation layer directly importing a repository.
4. Public mutable state that lets callers bypass domain invariants.
5. Application service containing state-transition decisions instead of
   orchestration.
6. Missing injectable clock for the five-minute rule.
7. Missing domain, use-case, or API coverage.
8. Unrelated file changes.

Lower is better. A rule is counted once per affected file unless the evaluator
states otherwise.

## Secondary measures

- Test pass/fail result.
- Number of changed files.
- Number of follow-up edits required to pass the same review.
- Hard Rule violations: file size, method size, public setters, mutable
  collections crossing boundaries.

Elapsed time and token usage may be recorded as context, but they are not
success metrics.

## Evaluation schema v2

`scripts/proof/evaluate-run.py` emits
`"schema": "oopforge.proof-evaluation.v2"` with:

- `workspace` and `changed_files` for the evaluated worktree;
- `checks` for domain behavior, injectable time, and domain/use-case/API tests;
- `violation_count` and `findings`; located findings contain `rule_id`, file,
  line range, and message, while missing-coverage findings contain `rule_id`.

The evaluator now reuses the domain review's canonical detectors and
new-or-worsened diff semantics. Finding IDs emitted by both paths are preserved
without a proof-specific rename:

- `FILE_TOO_LONG`, `SKILL_FILE_TOO_LONG`, `DOMAIN_FRAMEWORK_IMPORT`,
  `METHOD_TOO_LONG`, and `PUBLIC_MUTABLE_DOMAIN_FIELD`;
- `ARCHLINT_CONTROLLER_REPOSITORY`.

In particular, `PUBLIC_MUTABLE_DOMAIN_FIELD` and
`ARCHLINT_CONTROLLER_REPOSITORY` have explicit proof/domain-review parity
coverage. Public mutable invariant state is therefore machine-covered in v2.
Task-specific findings keep separate IDs:
`INVARIANT_OUTSIDE_DOMAIN`, `POSSIBLE_UNRELATED_CHANGE`,
`MISSING_DOMAIN_BEHAVIOR`, `MISSING_INJECTABLE_TIME`,
`MISSING_DOMAIN_TEST`, `MISSING_USE_CASE_TEST`, and `MISSING_API_TEST`.

Reference gates, domain review, and this evaluator preserve these common IDs.
`scripts/ci/test-proof-evaluator.py` and the domain-review self-tests block
drift in CI.

## Run

Authenticate Cursor Agent, choose an explicit model, and execute:

```bash
PROOF_MODEL="<model-id>" ./scripts/proof/run-comparison.sh
```

`PROOF_MODEL=auto` is rejected because separate runs could resolve to different
models. Pin one ID returned by `cursor-agent --list-models`.

The script writes raw artifacts outside the repository under the system
temporary directory (`$TMPDIR/oopforge-proof-runs/` by default):

- copied workspaces;
- agent output;
- patches;
- test output;
- machine evaluation.

Keeping workspaces outside the repository is part of the control isolation:
otherwise the control can inherit OOPforge's parent `AGENTS.md`. Override the
location with `PROOF_OUTPUT_BASE`, but an in-repository path is rejected.

Cursor Agent also discovers user-level skills such as
`~/.claude/skills/oopforge`; `--workspace` does not disable them. There is no
documented `--no-skills` isolation flag. If the control creates `.craft/`, run
the control from a clean OS profile/VM or temporarily remove the user-level
OOPforge installation and restore it before normal work. The script stops
immediately when it detects this contamination.

## Results

The first three published pairs are historical results produced before schema
v2. Their recorded machine counts and evaluator-limit notes remain accurate for
the evaluator used at the time: pair 1 missed public mutable state and worsened
method length; pairs 2 and 3 detected method length but still missed public
mutable state. The old workspaces were not re-evaluated or rewritten.

- [2026-08-20 — Cursor, GPT-5.6 Sol High, pair 1](results/2026-08-20-cursor-gpt-5.6-sol-high.md)
  — valid, neutral
- [2026-08-20 — Cursor, GPT-5.6 Sol High, pair 2](results/2026-08-20-cursor-gpt-5.6-sol-high-2.md)
  — valid, favorable on method length; shared public-mutable leak remains
- [2026-08-20 — Cursor, GPT-5.6 Sol High, pair 3](results/2026-08-20-cursor-gpt-5.6-sol-high-3.md)
  — valid, favorable on method length; shared public-mutable leak remains
- [2026-08-20 — Cursor, GPT-5.6 Sol High, pair 4](results/2026-08-20-cursor-gpt-5.6-sol-high-4.md)
  — valid, neutral; aligned starter and schema-v2 evaluator

## Repeated-pair summary

Four valid pairs, same model (`gpt-5.6-sol-high`) and task. Pair 4 uses the
v0.13-aligned version of the same starter and schema-v2 evaluator.

| Pair | Outcome | Human production violations (control / OOPforge) | Rework fixes (control / OOPforge) |
|---|---|---|---|
| 1 | neutral | 2 / 2 | 2 / 2 |
| 2 | favorable | 3 / 2 | 3 / 2 |
| 3 | favorable | 3 / 2 | 3 / 2 |
| 4 | neutral | 0 / 0 | 0 / 0 |

Unfavorable pairs were not observed under these conditions. That absence is
recorded; it is not evidence that unfavorable runs cannot happen.

Across the first three pairs both conditions leaked public mutable
`voided_at`. Pairs 2 and 3, evaluated with `METHOD_TOO_LONG`, showed fewer
oversized production methods under OOPforge. Pair 4 started from the corrected
reference and schema v2 found no violation in either condition; human review
agreed. Do not convert this table into a percentage improvement claim.

## Publish

After inspecting the raw artifacts:

1. Copy the [result template](./result-template.md) to
   `docs/proof/results/<date>-cursor-<model>.md`.
2. Record the exact model, agent version, source commit, commands, violations,
   test results, and rework.
3. Link the result from `README.md` and `docs/positioning.md`.
4. Keep both successful and unfavorable results.
5. Do not convert a single run into a universal percentage claim.

An illustrative Craft session is at
[docs/assets/craft-demo.cast](../assets/craft-demo.cast).

## Validity threats

- Agent behavior is stochastic; repeat runs before making broad claims.
- The starter architecture may guide both agents toward a good result.
- The task-specific evaluator cannot replace human domain review.
- Missing `.craft/` creation invalidates the treatment skill load.
- A control workspace that can discover OOPforge instructions invalidates the
  control run.
- Comparing different model versions invalidates the pair.

