---
name: workflow-continuity
description: Restore previous work at Craft start, cut a session at one decision, and write a next-session prompt without being asked.
tags: [workflow, memory, continuity]
stability: stable
---

# Workflow — Continuity

## Purpose

Keep work alive across chats. Task docs hold decisions. One file,
`next-session-prompt.md`, holds **what to do next**. The next Craft run
reads that file first and asks before implementing — the user does not
have to mention previous work or request a handoff.

## Work location

- Default: `.craft/` in the target project root.
- Override: `OOPforge work dir: <path>` in the target `AGENTS.md`.
- Opt-out: `OOPforge continuity: off` — create nothing, including the prompt.
- One doc per task: `<work dir>/<kind>-<slug>.md` (`feature` / `refactor` / `bugfix`).
- **What's next (exactly one file):** `<work dir>/next-session-prompt.md`.
  Never copy that text into a handoff, session log, or task doc.

## Resume protocol (Craft start — before any code)

1. If a work dir exists, list it.
2. Previous work exists when any of these is true: `next-session-prompt.md`
   is present; a task doc has `Stage` other than `done`; a handoff/README
   in the work dir points at unfinished work.
3. If previous work exists, **read `next-session-prompt.md` first** (if
   missing, the newest incomplete task doc), then emit the **Resume block**
   below before any other output — even if the user did not mention it.
4. If the user pasted the prompt or said continue, skip the question and
   resume — still emit the block, so the scope is on the record.
5. If the user points at a specific doc, follow that doc.
6. If no previous work, follow **First session (auto-create)** below.

### Resume block (required output — no code before this)

```markdown
## Resume

Previous work: <one line, product language>
Last verified: <what is already finished and checked>
Proposed job:  <one decision for this session>
Parked:        <what this session will not touch>

Continue this, or a new request instead?
```

**Re-scope what you inherit.** A prompt written by an earlier session can be
oversized. If its `This session` names more than one decision, or the file
runs past ~100 lines, put the first decision in `Proposed job` and move the
rest to `Parked`. An inherited prompt is evidence, not a session scope.

Never fill `Proposed job` with a default that drops unfinished previous work.

## First session (auto-create, opt-out)

When no related work doc exists, **decide creation by task kind.** Do not ask.

| Task class | Action |
|---|---|
| `feature` / `refactor` / `bugfix` | **auto-create** then announce in one line |
| advisory · recommendation-only · tiny | do not create |
| `AGENTS.md` has `OOPforge continuity: off` | do not create |

> Recording this task in `.craft/<kind>-<slug>.md`. (To disable, add `OOPforge continuity: off` to `AGENTS.md`.)

1. Create the work dir and the work doc.
2. If the target `.gitignore` lacks `.craft/`, add it (personal notes).
3. If you use an override path, gitignore that path.

## Session cut (where this chat stops)

One session ships **one decision**. Cut without being asked when any is true:

- the current stage/decision is verified;
- the next item is a different decision (new boundary, new branch, a new
  name the user did not use);
- remaining work is blocked on a person or another system;
- continuing would mix a second architecture change into this chat.

Do not cut mid-failing tests or before the current unit's verification.

On cut, or when a unit finishes with work still remaining:

1. Update the task doc (`Status` / `Progress` / `Decisions`).
2. Write (replace) `next-session-prompt.md` from the template below.
3. If an older prompt exists, move it to `.craft/archive/` with one line
   why — do not delete (the work dir is gitignored).
4. Announce in one line: this session stops here; the next chat starts
   from that file.

Do not wait for the user to request a handoff.

## Next-session prompt (link, do not copy)

Keep it short. If it grows past ~100 lines, you copied a design — move
that into the task doc and leave a link. The job line uses product language.

```markdown
# Next session

## Situation
- Repo, branch, what is blocked. One short paragraph.

## Read first (no code yet)
1. this file
2. AGENTS.md
3. the current task doc (link)

## This session
- One job. One decision.

## Not this session
- Parked work and why.

## Confirmed (do not re-ask)
- User-settled facts only.
```

## Work-doc format

```markdown
# <Title> — <kind>

## Status
- Stage: <discovery|design|skeleton|implement|test|refactor|done>
- Updated: <date>
- Next: <pointer to next-session-prompt.md — do not duplicate the prompt>

## Context / Goal
- What, and why.

## Decisions (append-only)
- [<date>] <decision> — <reason>

## Progress
- [x] done
- [ ] remaining

## Open Questions / Risks
- Unknowns, risks.

## Links
- commit / PR / related code paths
```

## Update rules

- Append to `Decisions`; do not delete existing lines.
- If a new finding conflicts with earlier records, search the whole work
  dir and correct the earlier claim too; append-only does not preserve
  false facts.
- When a work unit finishes, update `Status` and `Progress`.
- Reflect Craft's completion report in this doc.
- **Completion gate**: do not report done before updating this doc.
  If work remains, also write `next-session-prompt.md`.

## Large tasks / program

- Per-stage artifacts may sit beside the work dir; the task doc stays the
  local entry. **What now** lives only in `next-session-prompt.md`.
- A handoff holds cross-task facts and traps. It **links** the prompt.
  It does not duplicate "what's next".
- Never delete a superseded doc — move it to `<work dir>/archive/` with one
  line saying why. An ignored path has no history to recover from.
- The work dir is gitignored, so a long program's only copy is local. Once it
  holds reasoning nobody could reconstruct from the code, **say so once** and
  let the user decide where it should live. Do not silently keep months of
  decisions in an ignored folder.

## Prohibited

- **No `.craft/` for advisory/tiny tasks** — auto-create only for execution.
- **No creation when `OOPforge continuity: off`**.
- **No code on resume before the Resume block** is emitted and answered.
- **No inheriting a prompt as scope** — re-scope to one decision first.
- **No second copy of "what's next"** — one prompt file.
- **No design treatise in the prompt** — link, do not copy.
- **No asking the user to write the prompt** — the agent writes it.
- **No overwriting the decision log** — append only.
- **No secrets** in the work dir.
- **Do not force committing the work dir** — gitignored by default.
