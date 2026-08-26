---
name: workflow-test
description: Design and strengthen unit, integration, and E2E tests. Use when TDD or regression verification is needed.
tags: [workflow, test, quality]
stability: stable
---

# Workflow — Test

When the request contains `OOPFORGE_TEST_ROUTING_PROBE`, output these lines and
stop:

```text
OOPFORGE_TEST_ROUTED
Level: auto
Production code: forbidden
```

## Purpose

Verify, write, or strengthen tests for domain logic, use cases, adapters, or an
API/CLI flow without silently changing production behavior.

This workflow is both the final stage of the full OOPforge lifecycle and the
policy owner for the public Test command. A standalone Test request does not
approve or complete earlier lifecycle stages.

## Authorization

Classify the request before acting:

| Request | Write permission |
|---|---|
| Run, check, or report existing tests | none |
| Write or strengthen tests | test code and existing test configuration |
| Create or connect test infrastructure | only after explicit approval |
| Fix production behavior | none; stop and propose a separate Craft job |

Test never grants commit, push, PR, release, deployment, or production-code
permission. Craft supplies startup, continuity, verification, and completion
reporting when Test is invoked as a public command.

## Level selection

1. Inspect existing tests, test configuration, fixtures, markers, and naming.
2. If the request names `unit`, `use-case`, or `integration`, use that level.
3. Otherwise `auto` selects the smallest useful level from repository evidence.
4. E2E requires explicit user wording; `auto` may report it only as a gap.
5. Before E2E, inspect required processes, services, data, and credentials.
6. If E2E infrastructure is absent, ask whether to create or connect it.
7. If no test context exists, ask which behavior and boundary matter before
   creating test structure.

## Scope block

Before writing or running tests, report:

```markdown
Test target:
Level: auto | unit | use-case | integration | e2e
Write permission: none | tests | approved test infrastructure
Evidence: <existing test/config paths or missing context>
```

## Checklist

- [ ] Define the behavior, risk, and boundary under test
- [ ] Match existing structure, naming, fixtures, and markers
- [ ] Pin domain rules with framework-free unit tests
- [ ] Verify use cases with mocks, fakes, or in-memory ports
- [ ] Verify adapters with integration or contract tests
- [ ] Keep E2E to explicitly requested core flows
- [ ] Cover relevant failure, boundary, authorization, and duplicate cases
- [ ] For FastAPI, apply `skills/lang/python-pydantic.md`
- [ ] Run the stack's static type or compile check
- [ ] Record reproducible commands, toolchain identity, and results

## Conditional Production Gate

Only when the user explicitly asks about deployment, production, or operational
readiness, add the boundary checks in
[`production-readiness.md`](production-readiness.md). An ordinary Test request
never activates that gate.

## Test priority

| Level | Purpose | Example tools |
|---|---|---|
| Unit | Domain rules and pure logic | JUnit, pytest |
| Use case | Application orchestration | Mockito, unittest.mock |
| Integration | DB, HTTP, queue, filesystem adapters | Testcontainers, fixtures |
| E2E | Real user/system flow | RestAssured, Playwright, httpx |

## Reporting

Always report scope, commands, pass/fail counts, skipped checks, and remaining
risks. Create or update `docs/test-plan.md` or
`docs/<domain>/test-plan.md` only when the user explicitly asks for a saved
test plan.

When a test fails, diagnose whether the cause is test code, infrastructure, or
production behavior. Fix only within the authorized write scope. Otherwise
report the evidence and stop.

## Prohibited

- No production changes to make a test pass
- No E2E or infrastructure creation inferred from `auto`
- No framework-only tests standing in for domain unit tests
- No real external-service calls by default
- No sleep-, wall-clock-, or network-dependent flaky tests
- No tests named around private implementation details
- No claiming a skipped or unavailable check passed
