---
name: workflow-crucible
description: Run one backend change end to end in one request — Consult plan, Craft, Refactor when earned, Test — with one mandatory stop at plan approval.
tags: [workflow, orchestration, ddd]
stability: experimental
---

# Workflow — Crucible

Contents: Purpose · When to use · Load order · Stages · Stops · Work doc · Completion report · Prohibited

## Purpose

Chain the existing workflows for a user who asks to go from plan to tested code
in one request. Crucible adds no rules of its own: each stage runs its workflow
file as written. Crucible only orders the stages, carries the approved plan
forward, and decides when to stop.

## When to use

The request asks for the whole path — plan, build, clean up, test. For one step,
use that step's command. Advice only stays in Consult. If the whole job fits
Craft's **Size gate**, say so in one line and run Craft alone.

## Load order

Read a stage's workflow file when that stage starts, never the slash command,
which inlines more than a stage needs:

1. `workflow/gates.md` once, at start. Its startup, verification, and
   completion gates apply to every stage.
2. `workflow/consult.md` for stage 1.
3. `workflow/craft.md` and `principles/oop-discipline.md` for stage 2.
4. `workflow/refactor.md` only if stage 3 runs.
5. `workflow/test.md` for stage 4.

After context compaction, read this file and the current stage's file again.

## Stages

### 1. Plan — Consult, Document mode

- For a new domain or large feature, write Discovery, then Design, then
  Delivery Plan, each with its own checkpoint. For one use case in an existing
  domain, write one Delivery Plan.
- The plan records scope, non-goals, the public names to approve, the test
  strategy, and whether a refactor is expected.
- **Stop and ask the user to approve the plan.** This stop is mandatory.
  Implementation begins only after approval, so Consult never applies its own
  output in the same turn.

### 2. Build — Craft

- The approved plan is the input, through the `gates.md` **Plan input** gate.
- Implement along Craft's selected path with the tests that path requires
  (a bug fix starts with a failing test). Commit.

### 3. Refactor — only when earned

- Run only when the plan expected it, or stage 2 left a named smell in code it
  touched. Otherwise write `Refactor: skipped — <reason>` and move on.
- One decision, visible behavior unchanged, tests green before and after.
  Commit separately; never fold it into the build commit.

### 4. Test — gap pass

- Read the verification already recorded by stages 2 and 3. Add or strengthen
  tests at the smallest useful level (`test.md` Level selection) only where the
  plan's test strategy is still uncovered. Do not re-run a recorded check
  unless code changed since.
- No production code changes. A failing test that needs a production fix is a
  stop.

## Stops

After the plan is approved, continue between stages without asking. Stop only
when:

- a decision the plan does not settle would change behavior, scope, or a public
  name;
- a check fails and the fix is outside the current stage's write permission;
- the work would need scope drift;
- Continuity's session-cut condition is met — stop at a stage boundary and write
  `next-session-prompt.md`.

On a stop, report the stage, what is done, and the one question. If the user
asks to stop after every stage, do so for the rest of the run.

## Work doc

Keep one continuity work doc for the run: `.craft/crucible-<slug>.md`. It
records the plan path, the current stage, and each stage's commit. Stages do not
create their own work docs.

## Completion report

Write one report at the end: the block below, then the `gates.md` completion
sections once — not once per stage.

```markdown
## Stages
- Plan: <path> — approved
- Build: <commit>
- Refactor: <commit> | skipped — <reason>
- Test: <commit> | no gaps — <why>
```

## Prohibited

- Never start stage 2 before the plan is approved.
- Never put refactor moves in the build commit, or feature changes in the
  refactor commit.
- Never change production code in stage 4.
- Never push, open a pull request, or release; that stays with the user.
- Never run stages in parallel or hand them to other agents.
