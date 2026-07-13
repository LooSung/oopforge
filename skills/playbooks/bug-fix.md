---
name: playbook-bug-fix
description: Execution playbook to reproduce a domain bug with a failing test and resolve it with the smallest change.
tags: [playbook, bug-fix, tdd]
stability: experimental
---

# Playbook — Bug Fix

## When to use

Use this when fixing a wrong state transition, an invariant violation, duplicate handling,
an authorization error, or a regression bug.

Follow `skills/workflow/test.md` for test design and run records.
Follow `skills/workflow/craft.md` for the OOP Contract format and final verification.

## Checklist

- [ ] Write the symptom in one sentence. → verify: symptom is observable, not a guessed cause
- [ ] Find the affected Aggregate and use case. → verify: Aggregate + use case named
- [ ] Write a failing test that reproduces the bug. → verify: test fails for the reported symptom
- [ ] Confirm the test actually fails before the fix. → verify: red run recorded
- [ ] Write down the root cause. → verify: cause points at a domain rule or transition
- [ ] Fix with the smallest code change. → verify: diff limited to the failing path (surgical)
- [ ] Confirm the failing test and related regression tests pass. → verify: green run recorded
- [ ] Follow the verification and completion report in `skills/workflow/craft.md`. → verify: Scope drift is `none` (or justified)

## Prohibited

- Do not fix directly without a failing test.
- Do not add a conditional that only masks the symptom.
- Do not mix a bug fix with structural rework.
- Do not claim done if you could not reproduce it.
