# OOPforge Reviewer Checklist

Use this checklist after an agent generates or refactors code with OOPforge.

## Enforcement policy

- **This repository blocks on its own gates.** The `lint`, `arch-lint`, and
  `examples` workflows fail on repository lint, canonical example architecture
  checks, or tests. The plain Python hexagonal example is checked by
  import-linter; the plain Java hexagonal example runs ArchUnit in Gradle tests.
- **The adopter template is non-blocking by default.** Copying
  [`templates/github/oopforge-domain-review.yml`](../templates/github/oopforge-domain-review.yml)
  posts review feedback and artifacts, but findings keep a `NEUTRAL` verdict
  and do not fail the workflow or block a merge.
- **Blocking in an adopter repository is opt-in.** Copy the matching canonical
  import-linter or ArchUnit template from
  [`skills/skeleton/lint-enforcement.md`](../skills/skeleton/lint-enforcement.md),
  run it in the adopter's CI, and configure that concrete lint/test check as a
  required status check in branch protection. Making the default domain-review
  job required does not turn its findings into failures.

## Domain layer

- [ ] Domain objects do not import framework libraries.
- [ ] Aggregates protect their own invariants.
- [ ] Value objects are immutable.
- [ ] Domain events describe business facts, not technical actions.
- [ ] Entities do not expose public setters for invariant-sensitive fields.
- [ ] Cross-aggregate references use IDs instead of object references.
- [ ] Domain behavior methods own invariants (not an anemic data bag — `skills/antipatterns/anemic-domain.md`).
- [ ] No God Aggregate: unrelated capabilities are not forced into one root (`skills/antipatterns/god-aggregate.md`).

## Application layer

- [ ] Use cases coordinate domain objects but do not own business rules.
- [ ] Application services depend on ports, not infrastructure implementations.
- [ ] Transaction boundaries are explicit — **one Aggregate modified per transaction** (`skills/oop/transaction-boundary.md`).
- [ ] Commands and results are small, explicit, and framework-agnostic where possible.
- [ ] Controllers/Routers do not own domain rules or call repositories directly (`skills/antipatterns/controller-fat.md`).
- [ ] Repositories do not own domain judgments (`skills/antipatterns/repository-with-business-logic.md`).

## Infrastructure layer

- [ ] Adapters implement ports.
- [ ] Framework annotations stay outside the domain layer.
- [ ] Persistence models do not leak into domain objects.
- [ ] External system failures are mapped at adapter boundaries.

## Tests

- [ ] Domain rules are tested without framework bootstrapping.
- [ ] Use cases are tested with fake or in-memory ports.
- [ ] Adapter tests are separated from domain tests.
- [ ] At least one test proves each important invariant.

## Architecture

- [ ] Dependencies point inward.
- [ ] Bounded context boundaries are explicit.
- [ ] Public APIs express use cases, not database tables.
- [ ] The generated design can be explained using the Discovery → Design → Delivery Plan → Skeleton → Implement → Test flow.
