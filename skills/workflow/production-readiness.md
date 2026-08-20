---
name: workflow-production-readiness
description: Opt-in NFR gate for explicit deploy, production, or operational-readiness requests.
tags: [workflow, production, operations]
stability: experimental
---

# Workflow — Production Readiness

## Activation gate

Use this gate **only** when the user explicitly asks to deploy or asks about
deployment, production, or operational readiness.

Do not infer it from an ordinary feature/API request, a generic request to make
code "ready," release-note work, or the presence of validation or security
concerns. Without the explicit signal, stay on the normal Craft path.

This is one conditional gate layered onto the selected Delivery Plan,
Implement, or Test workflow. It does not replace those workflows.

## Purpose

Make operational behavior at system boundaries explicit before deployment.
Keep these non-functional responsibilities in adapters, middleware,
configuration, and application boundary coordination. Do not add framework,
logging, retry, audit, idempotency, or other operational concerns to the domain.

## Adapter ownership

| Concern | Owner | Required behavior |
|---|---|---|
| Input validation | Inbound adapter | Validate wire shape, size, format, and required fields before invoking the use case. Domain methods still enforce business invariants. |
| Safe errors | Inbound adapter | Map failures to stable public errors; never expose stack traces, SQL, credentials, or internal topology. |
| API idempotency | Inbound adapter + idempotency adapter | Accept and scope the key at ingress; persist/replay the outcome through an application port. Keep duplicate handling outside the domain. |
| Retry and timeout | Outbound adapter | Set an explicit timeout budget. Retry only transient, safe operations with bounded attempts and backoff; do not multiply retries across layers. |
| Observability | Middleware/adapters | Propagate correlation context and emit structured logs, metrics, and traces around boundaries without changing domain behavior. |
| Audit | Audit adapter via an application port | Record actor, action, target, result, and correlation identifier when policy requires it. |
| PII and secrets | Adapters/configuration | Minimize and redact PII in telemetry, load secrets from approved configuration, and never place secrets in code, errors, logs, or audit records. |

## Gate checklist

- [ ] Name the deployment or production context and the important boundary
      failure modes.
- [ ] Assign every applicable concern above to a concrete adapter, middleware,
      configuration, or application port; mark non-applicable items with a reason.
- [ ] Define timeout, retry, idempotency, telemetry, audit, and data-handling
      acceptance evidence before implementation.
- [ ] Confirm domain files contain no framework or operational NFR concerns.
- [ ] Run the boundary tests below and record commands and results.
- [ ] List every unmet item as a deployment blocker or an explicitly accepted
      operational risk.

## Boundary test checklist

- [ ] **Invalid input:** malformed, missing, oversized, and out-of-range
      boundary data is rejected before the use case; business-invalid data is
      rejected by the domain invariant.
- [ ] **Duplicate request:** repeating the same idempotency key does not repeat
      the side effect and returns the defined replay/conflict behavior.
- [ ] **Safe error:** unexpected adapter/dependency failures return the public
      error contract without internal details, PII, or secrets.
- [ ] **Correlation and audit:** the correlation identifier reaches logs/traces
      and required audit records; actor/action/target/result are present and
      sensitive values are absent.

## Completion report

Record:

- deployment context and boundary assumptions;
- applicable controls and their adapter owners;
- boundary-test commands and results;
- blockers and accepted operational risks.

Passing this gate means the requested boundary policy has evidence. It is not a
claim that every organization-specific production requirement is satisfied.
