#!/usr/bin/env python3
"""Self-test for the domain-review MVP (roadmap C2).

Proves the domain logic: unified-diff parsing, per-file detectors, and the
new-only + line-level admission in ReviewRun. Pure stdlib; run in CI.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from review import delivery, detectors  # noqa: E402
from review.changeset import parse_unified_diff  # noqa: E402
from review.model import (  # noqa: E402
    Changeset,
    CodeLocation,
    DOMAIN_FRAMEWORK_IMPORT,
    FILE_TOO_LONG,
    LineRange,
    ReviewRun,
    RuleCatalog,
    Violation,
)

FAILURES = []


def check(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILURES.append(name)


def test_changeset_parse():
    diff = (
        "diff --git a/app/x.py b/app/x.py\n"
        "--- a/app/x.py\n"
        "+++ b/app/x.py\n"
        "@@ -0,0 +5,3 @@\n"
        "diff --git a/old.py b/old.py\n"
        "--- a/old.py\n"
        "+++ /dev/null\n"
        "@@ -1,2 +0,0 @@\n"
    )
    cs = parse_unified_diff(diff)
    check("changeset lists only added-side files", cs.files() == ["app/x.py"])
    check("changeset covers added range",
          cs.covers(CodeLocation("app/x.py", LineRange(5, 7))))
    check("changeset excludes untouched line",
          not cs.covers(CodeLocation("app/x.py", LineRange(1, 1))))


def test_detectors():
    catalog = RuleCatalog.defaults()
    long_code = {"app/big.py": "\n".join(f"x = {i}" for i in range(350))}
    check("file-too-long fires >300",
          any(v.rule_id == FILE_TOO_LONG for v in detectors.scan(long_code, catalog)))

    short_code = {"app/ok.py": "\n".join(f"x = {i}" for i in range(10))}
    check("file-too-long silent <=300", detectors.scan(short_code, catalog) == [])

    domain_fw = {"app/domain/order.py": "from sqlalchemy import Column\nx = 1\n"}
    dv = detectors.scan(domain_fw, catalog)
    check("domain framework import fires",
          any(v.rule_id == DOMAIN_FRAMEWORK_IMPORT for v in dv))
    check("domain framework import located on import line",
          dv and dv[0].location.lines.start == 1)

    non_domain_fw = {"app/adapter/repo.py": "from sqlalchemy import Column\n"}
    check("framework import outside domain is ignored",
          detectors.scan(non_domain_fw, catalog) == [])

    excluded = {"examples/x/app/domain/order.py": "from sqlalchemy import Column\n"}
    check("excluded path is skipped", detectors.scan(excluded, catalog) == [])


def _violation(rule=FILE_TOO_LONG, path="app/big.py", start=1, end=350, subject="app/big.py"):
    return Violation(rule, CodeLocation(path, LineRange(start, end)), subject, "msg")


def test_new_only_and_line_level():
    changeset = Changeset({"app/big.py": [LineRange(1, 350)]})

    # NEW: subject absent in base + on changed lines -> admitted
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [])
    check("new violation on changed lines is admitted", len(run.findings()) == 1)

    # PRE-EXISTING: same (rule, subject) in base -> silent
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [_violation()])
    check("pre-existing violation stays silent", run.findings() == [])

    # OUT OF SCOPE: violation not on changed lines -> silent
    untouched = Changeset({"other.py": [LineRange(1, 5)]})
    run = ReviewRun.open("base", "head", untouched)
    run.assess([_violation()], [])
    check("violation off changed lines is not reported", run.findings() == [])

    # LINE-SHIFT ROBUSTNESS: same subject, different lines in base -> still pre-existing
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation(start=1, end=360)], [_violation(start=1, end=350)])
    check("subject match survives line shift", run.findings() == [])

    # Verdict is always neutral
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [])
    check("verdict is neutral even with findings", run.verdict().status == "NEUTRAL")


def test_delivery():
    changeset = Changeset({"app/big.py": [LineRange(1, 350)]})
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [])
    report = run.summarize()
    md = delivery.summary_markdown(report)
    check("summary carries idempotent marker", delivery.COMMENT_MARKER in md)
    check("summary lists the finding", "FILE_TOO_LONG" in md)

    clean = ReviewRun.open("base", "head", changeset).summarize()
    check("clean summary says no violations", "No new hard-rule violations" in delivery.summary_markdown(clean))

    payload = delivery.machine_findings(report)
    check("machine schema is versioned", payload["schema"] == "oopforge.domain-review.v1")
    check("machine findings count matches", len(payload["findings"]) == 1)


def main():
    print("domain-review self-test:")
    test_changeset_parse()
    test_detectors()
    test_new_only_and_line_level()
    test_delivery()
    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
