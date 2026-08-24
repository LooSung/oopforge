---
name: workflow-test
description: Design and strengthen unit, integration, and E2E tests. Use when TDD or regression verification is needed.
tags: [workflow, test, quality]
stability: stable
---

# Workflow — Test

## When to use
When writing or strengthening tests for domain logic, use cases, adapters, or an API/CLI flow.
You may write them first with TDD or as regression tests after implementation.

## Checklist
- [ ] Define the test target and scope
- [ ] Choose the needed test types among unit/integration/E2E
- [ ] Check the existing test structure and naming conventions
- [ ] Pin domain rules with unit tests
- [ ] Verify use cases with port mocks/fakes
- [ ] Verify adapters with real integration or contract tests
- [ ] Verify E2E minimally, for core user/system flows only
- [ ] Include failure/boundary/authorization/duplicate-execution cases
- [ ] For FastAPI, cover the boundary matrix in `skills/lang/python-pydantic.md`
- [ ] Run the stack's static type or compile check
- [ ] Record the run commands and results

## Conditional Production Gate

Only when the user explicitly asks about deployment, production, or operational
readiness:

- [ ] Run the invalid-input, duplicate-request, safe-error, and
      correlation/audit boundary checklist in the
      [Production Readiness gate](production-readiness.md).
- [ ] Record reproducible commands, results, blockers, and accepted operational
      risks for that gate.

Do not infer this gate from an ordinary feature or test request.

## Test priority

| Test | Purpose | Example tools |
|---|---|---|
| Unit | Pin domain rules and pure logic | JUnit, pytest |
| Use case | Verify application-service orchestration | Mockito, unittest.mock |
| Integration | Verify DB, HTTP, queue, filesystem adapters | Testcontainers, pytest fixtures |
| E2E | Confirm real user/system flows | RestAssured, Playwright, httpx |

## Output

Save to `docs/test-plan.md` or `docs/<domain>/test-plan.md`:

```markdown
# <Feature> — Test Plan

## Scope
- Target:
- Risk:

## Unit Tests
- 

## Integration Tests
- 

## E2E Checks
- 

## Fixtures / Test Data
- 

## Commands
- `...`

## Result
- 
```

## Prohibited
- **No changing domain logic without tests**
- **No skipping domain unit tests by trusting framework tests only**
- **No making real external-service calls the default**
- **No flaky tests depending on sleep/time/network**
- **No naming tests around implementation details**

## Next step
After tests pass -> review, commit, push, write MR/release notes
