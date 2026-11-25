---
name: workflow-gates
description: Shared startup, plan input, verification, and completion report for Craft, Refactor, Test, and Crucible.
tags: [workflow, oop]
stability: stable
---

# Workflow — Gates

Craft, Refactor, Test, and Crucible open and close with these gates. Each
workflow adds only its own steps; none repeats them.

## Startup

1. **Resume** (`continuity.md`): list `.craft/`. If previous work exists, read
   `next-session-prompt.md` first and **emit the Resume block before any other
   output** — even if the user did not mention it. Re-scope an inherited prompt
   to one decision; it is evidence, not a session scope. If none exists and this
   is an execution task (feature, refactor, bug fix), create
   `.craft/<kind>-<slug>.md` and announce it in one line. Skip this for advisory
   or tiny tasks, or when `AGENTS.md` contains `OOPforge continuity: off`.
2. Confirm the **work target**. For app work it is the backend repo, not the
   OOPforge **pack** (`~/.oopforge`, skill paths). If `pwd` is the pack root
   during app work, confirm the agent was started from the target project. When
   maintaining OOPforge itself, the pack root is the target.
3. Resolve a path the user gives (`@…`, absolute, or relative) against the work
   target (current directory or git root), never under `{pack}/docs/…` or
   `~/.oopforge/…`. If it is missing,
   confirm the absolute path or project root with the user.
4. **Read narrowly**: in target code and logs, search first, read only the
   needed range, and print only summaries and failures. Read plans, work docs,
   rules, and skill files whole.
5. If you skip any step, leave a one-line reason.

## Plan input

When the user names an approved plan — a Delivery Plan, Design, or planning
document from Consult — or the work doc links one, read it before the code:

- Decisions it records are settled. Do not ask them again.
- Assumptions list only what the plan left open. A Contract cites the plan's
  sections instead of restating them.
- A conflict between the plan and the code is a stop: report it and ask.

A draft or unapproved plan is evidence, not a decision.

## Verification

- Complete the chosen workflow's checklist (each step should have a `verify:`).
- Check the project's stated rules (`AGENTS.md` or
  equivalent) against the changed files and name them.
- Confirm **Scope drift** is `none`, or list every out-of-request change with a
  reason.
- Run the tests the change needs. Record reproducible commands, toolchain
  identity (interpreter path or version, required env vars), and results. Do not
  re-run a check already recorded in this run unless code changed since.
- **Live run** (`test.md`) is opt-in: start the server only when the user asked or
  `OOPforge live run: on` is set. Otherwise report `Live run: not run` and what
  to check by hand.
- For any failed or skipped check, give the reason and the risk.

## Completion report

Small path (Craft's **Size gate**) — three lines:

```markdown
Changed: <file — what changed>
Verified: <command and result | not run — why>
Scope drift: none | <change — why>
```

Standard path:

```markdown
## Design Decisions
-

## Verification
- Tests:
- Project rules:
- Scope drift: none | <file/change — why>

## Remaining Risks
-
```

Add `## Environment Facts` only when this session learned one: something the
next session would otherwise relearn the hard way, such as a hook that breaks
the local server or a check slow enough to run once at the end. Offer to add it to
the target project's `AGENTS.md`, and add it only after the user agrees. Never
keep it only in agent memory or in `.craft/`.

**Completion gate**: if a continuity work doc exists, update it
(Status/Progress/Decisions) before reporting done. If the unit is done but work
remains, write `.craft/next-session-prompt.md` before reporting done — do not
wait to be asked (`continuity` Session cut).
