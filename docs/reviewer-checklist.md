# OOPforge Reviewer Checklist

Use this checklist after an agent generates or refactors code with OOPforge.

## Domain layer

- [ ] Domain objects do not import framework libraries.
- [ ] Aggregates protect their own invariants.
- [ ] Value objects are immutable.
- [ ] Domain events describe business facts, not technical actions.
- [ ] Entities do not expose public setters for invariant-sensitive fields.
- [ ] Cross-aggregate references use IDs instead of object references.

## Application layer

- [ ] Use cases coordinate domain objects but do not own business rules.
- [ ] Application services depend on ports, not infrastructure implementations.
- [ ] Transaction boundaries are explicit.
- [ ] Commands and results are small, explicit, and framework-agnostic where possible.

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
