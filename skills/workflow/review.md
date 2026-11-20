---
name: workflow-review
description: Review one backend diff, branch, or pull request against OOPforge rules and report prioritized findings without changing code.
tags: [workflow, review, quality]
stability: experimental
---

# Workflow — Review

Contents: Purpose · Target · Read before judging · Checks · Severity · Finding format · Report · Posting · After the review · Prohibited · Completion

## Purpose

Judge a backend change after it exists. Consult advises before or around work;
Review reads one finished change and reports what must change before it
merges. Review reports findings. It never applies them.

## Target

Resolve exactly one target, in this order:

1. **Pull request** — a number or URL. Read its description, diff, and head
   commit (`gh pr view`, `gh pr diff`).
2. **Branch** — diff it against its merge base with the default branch.
3. **Pasted diff** — review exactly the pasted text; the base commit is `pasted`.
4. **Nothing named** — the working tree (staged and unstaged) against `HEAD`.

Record the **base commit**: the short SHA of the reviewed head. Every finding
refers to that commit. If the target has no diff, say so and stop.

Review the changed lines and the code they call or are called by. A problem
that existed before this change is not a finding; mention at most one under
**Not checked** when it blocks understanding the change.

Frontend files in the diff are outside OOPforge. Name them in one line and
point to Compforge review; do not judge them. OOPforge covers Java Spring and
Python FastAPI backends (`lang/backend-stack.md`).

## Read before judging

1. The PR description, when there is one. A risk-first section ("look here
   first") sets the reading order. Its test section and its "not verified"
   list tell you which evidence exists. A DRY · YAGNI · KISS self-check is a
   claim to verify, not evidence.
2. The linked work card, when accessible. Its scope decides scope drift.
3. The target project's `AGENTS.md` / `CLAUDE.md` rules, then the OOPforge
   Hard Rules in `{pack}/AGENTS.md`, `skills/principles/oop-discipline.md`,
   and the relevant sections of `{pack}/docs/reference/reviewer-checklist.md`.
4. Only the `skills/antipatterns/` files the diff touches.

## Checks

1. **Rules** — project rules, Hard Rules, reviewer checklist.
2. **Domain** — rules and invariants live in the domain and hold on every path
   that changes state; no framework types in the domain.
3. **Boundaries** — layer and dependency direction, ports and adapters, no
   business logic in controllers or repositories.
4. **Consistency** — transaction boundaries, one aggregate per transaction
   unless stated, idempotency of retried or repeated requests, ordering of
   side effects.
5. **API contract** — status codes, error shape, validation, backward
   compatibility of existing fields and routes.
6. **Persistence** — migrations, rollback path, indexes, data that existing
   rows already hold.
7. **Security** — authentication, authorization scope, data exposed in
   responses and logs.
8. **Tests** — new behavior and each fixed defect has a test at the right level.
   Trace the call path; cite the line that proves the defect.
9. **Scope** — every change maps to the stated card or PR purpose.
10. **Comments** — a comment the diff left contradicting its code is P2; a new
    narration comment is P3. A comment is a claim: confirm behavior from code
    and tests, never from the comment alone.
11. **Self-check** — test the author's DRY · YAGNI · KISS claims against the diff.
12. **Tools, when available** — each one optional; record a missing one in
    one line under **Not checked**:
    - the pack reviewer, run locally on the same range CI uses:
      `PYTHONPATH={pack}/scripts/ci python3 -m review.main --base <base> --head <head> --root <target>`;
    - the architecture linter for a matching layout:
      `python3 {pack}/scripts/ci/archlint.py <layered|cqrs> <root>`;
    - the harness bug reviewer (Claude Code: `/code-review`), without fix or
      comment flags. Merge its results into the levels below and drop duplicates.

Run project tests only when the user asks or the project documents a cheap
command. Never install dependencies or start external services.

## Severity

| Level | Meaning |
|---|---|
| **P1** | Must fix before merge: wrong result, data loss or corruption, crash, broken API contract, migration that cannot roll back, authentication or authorization bypass, Hard Rule MUST violated |
| **P2** | Should fix before merge: wrong on a realistic edge case, invariant enforced on only some paths, missing idempotency on a retried call, Hard Rule SHOULD violated, new behavior without a test |
| **P3** | Optional improvement: naming, simplification, follow-up card |

Between two levels, choose the lower and state the doubt. Formatting the
linter owns is not a finding. Praise is not a finding.

## Finding format

```markdown
**[P1 · <card key or area>] <the defect in one sentence>**

`<path>:<line>` (a permalink at the base commit when a remote exists)

<What happens> → <why it is wrong, citing the file and line it contradicts> →
<the smallest fix direction>. <Failing input and observed result, when known.>

Next: `/oopforge:<craft|test|refactor> <one-line request naming the file>`
```

Write each finding so the author can act without asking back: the input, the
observed result, and the expected result.

Pick the `Next` command by what the fix changes:

- **craft** — behavior is wrong or a named state is missing. Craft's bug-fix
  path writes the failing test first.
- **test** — behavior is right but a test is missing, weak, or asserts the
  wrong thing. Production code stays unchanged.
- **refactor** — structure only, behavior unchanged: boundaries, naming,
  narration comments, duplication.

Write the request in the author's words so it runs as written; on Codex or
Cursor write `Use OOPforge <command>: …` instead. A finding with no code fix,
such as a scope question for the author, gets no `Next` line.

## Report

Write the report in the user's language.

```markdown
## Review — <target> @ <base commit>

Before merge: <N> (P1 <a> · P2 <b>). Optional: <c> (P3).

### P1
### P2
### P3

### Not checked
- <check that was not run> — <why>

### Scope drift
none | <file — change outside the stated purpose>

### Next
1. `/oopforge:craft …` — behavior fixes, P1 first
2. `/oopforge:test …` — missing or weak tests
3. `/oopforge:refactor …` — structure, after the tests above pin behavior
```

Omit an empty level heading or an empty `Next` step. With no findings, say so
and list what was checked. Merge `Next` lines that touch the same file into one
request.

## Posting

Report in the conversation by default. Post to the pull request only when this
request explicitly asks: one summary comment plus one inline comment per finding
at its line, anchored to the base commit. Show the exact comments before posting.
Never approve or request changes on the user's behalf unless asked.

## After the review

Fixes are Craft, Test, or Refactor work, in the order of the `Next` section.
When the author answers a review, the PR can carry a response table — commit |
finding | what changed. A follow-up Review re-checks those findings and the new
diff only.

## Prohibited

- Never modify production code, tests, configuration, migrations, CI, or dependencies.
- Never run a reviewer in a mode that applies fixes.
- Never post to a pull request without an explicit request in this turn.
- Never report a finding without the line that proves it.
- Never present an unrun check as passed.
- Never widen OOPforge beyond the stacks in `skills/lang/backend-stack.md`.

## Completion

Report the target and base commit, the counts per level, what was not checked,
and the `Next` commands when fixes are needed (`/oopforge:craft`,
`/oopforge:test`, then `/oopforge:refactor`).
