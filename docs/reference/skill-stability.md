# Skill stability

[`skills/stability.json`](../../skills/stability.json) separates established skills
from guidance that is still being explored. The registry also lets static checks
catch missing or unlisted skill files.

For stable skills:

- avoid unnecessary behavioral churn;
- document user-visible changes and migration steps;
- keep the skill covered by relevant references or checks.

`stable` is a maintenance signal, not a hosted-service guarantee or a freeze on
every sentence. Stable skills preserve the
[core 1.x usage contract](support-scope.md#versioning-and-compatibility) while
their explanations, examples, and compatible checks can improve.

New advanced skills start as `experimental` until enough usage, reference
material, and checks exist. Experimental skills may change more freely and are
not silently added to the default execution path.

`scripts/ci/harness-smoke.sh static` checks that every shipped skill is listed
exactly once and that every listed path exists.
