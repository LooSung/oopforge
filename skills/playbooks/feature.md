---
name: playbook-feature
description: Execution playbook for adding one use case to an existing domain under OOPforge rules.
tags: [playbook, feature, oop]
stability: experimental
---

# Playbook — Feature

## When to use

Use this when adding one new behavior or use case to an existing domain.
For a new domain or large feature, start from Discovery.

Follow `skills/workflow/implement.md` for the detailed implementation order.
Follow `skills/workflow/craft.md` for the OOP Contract format and final verification.

## Checklist

- [ ] Read the relevant Aggregate, application service, port, and adapter. → verify: owners and call path named
- [ ] Review the existing domain rules and tests. → verify: invariants that the feature must preserve listed
- [ ] Decide which domain object will own the new behavior. → verify: owner is a domain type, not the application service
- [ ] Minimize the scope of port and adapter changes. → verify: only ports the use case needs
- [ ] Follow the single-use-case procedure in `skills/workflow/implement.md`. → verify: one use case + tests green
- [ ] Follow the verification and completion report in `skills/workflow/craft.md`. → verify: Scope drift is `none` (or justified)

## Prohibited

- Do not hide the new behavior in an application-service private method.
- Do not create a generic Manager, Helper, or Util class first.
- Do not implement several use cases at once.
- Do not mix in unrelated refactoring.
