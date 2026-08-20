# Skill stability

OOPforge 1.x treats every skill listed under `stable` in
[`skills/stability.json`](../skills/stability.json) as part of the public
methodology contract. This includes Craft, OOP discipline, continuity, workflow
stages, feature and bug-fix playbooks, domain modeling, Domain Events, outbox,
CQRS, Production Readiness, and skeleton guidance.

For stable skills:

- existing workflow meaning and required checkpoints remain compatible
  throughout 1.x;
- new optional guidance may be added in a minor release;
- corrections that preserve the contract ship as patches;
- removing or changing a required stage, hard rule, or canonical path requires
  the next major version.

New advanced skills start as `experimental` until an executable reference and
the relevant automated checks exist. Experimental skills may change in a minor
release and are never silently included in the stable execution path. The five
standalone anti-pattern guides remain experimental in 1.0; stable hard rules
and review detectors still enforce the overlapping measurable violations.

`scripts/ci/harness-smoke.sh static` checks that every shipped skill is listed
exactly once and that every listed path exists.
