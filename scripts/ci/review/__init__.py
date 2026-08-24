"""OOPforge domain review.

Read-only PR-diff reviewer that surfaces new or worsened hard-rule,
antipattern, and archlint violations. Pure stdlib.

Layout:
  model             -- ReviewRun aggregate, value objects, RuleCatalog
  changeset         -- parse `git diff -U0` into added line ranges
  detectors         -- per-file scans into candidate Violations
  archlint_adapter  -- reuse layered/CQRS fitness functions on a git ref
  delivery          -- summary comment + machine JSON + correction prompt
  main              -- reviewPullRequest orchestration + CLI
"""
