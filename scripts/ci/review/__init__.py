"""OOPforge domain-review MVP (roadmap C2).

Read-only PR-diff reviewer that surfaces ONLY NEW hard-rule violations
introduced by a pull request. Pure stdlib.

Layout mirrors the OOP Contract from the design stage:
  model      -- domain: ReviewRun aggregate, value objects, RuleCatalog
  changeset  -- adapter: parse `git diff -U0` into added line ranges
  detectors  -- adapter: scan a file set into candidate Violations
  delivery   -- adapter: render summary comment + machine JSON
  main       -- application: reviewPullRequest orchestration + CLI
"""
