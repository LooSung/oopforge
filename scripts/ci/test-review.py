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
    METHOD_TOO_LONG,
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


def test_file_length_detector():
    catalog = RuleCatalog.defaults()
    long_code = {"app/big.py": "\n".join(f"x = {i}" for i in range(350))}
    check("file-too-long fires >300",
          any(v.rule_id == FILE_TOO_LONG for v in detectors.scan(long_code, catalog)))
    short_code = {"app/ok.py": "\n".join(f"x = {i}" for i in range(10))}
    check("file-too-long silent <=300", detectors.scan(short_code, catalog) == [])


def test_import_detector():
    catalog = RuleCatalog.defaults()
    domain_fw = {"app/domain/order.py": "from sqlalchemy import Column\nx = 1\n"}
    dv = detectors.scan(domain_fw, catalog)
    check("domain framework import fires",
          any(v.rule_id == DOMAIN_FRAMEWORK_IMPORT for v in dv))
    check("domain framework import located on import line",
          dv and dv[0].location.lines.start == 1)
    non_domain_fw = {"app/adapter/repo.py": "from sqlalchemy import Column\n"}
    check("framework import outside domain is ignored",
          detectors.scan(non_domain_fw, catalog) == [])
    pydantic = {"app/domain/money.py": "from pydantic import BaseModel\n"}
    check("pydantic domain import fires",
          any(v.rule_id == DOMAIN_FRAMEWORK_IMPORT
              for v in detectors.scan(pydantic, catalog)))
    excluded = {"examples/x/app/domain/order.py": "from sqlalchemy import Column\n"}
    check("excluded path is skipped", detectors.scan(excluded, catalog) == [])


def test_python_method_detector():
    catalog = RuleCatalog.defaults()
    python_long = {
        "app/domain/order.py":
        "def place_order():\n" + "".join(f"    value_{i} = {i}\n" for i in range(20))
    }
    pv = detectors.scan(python_long, catalog)
    check("python method-too-long fires >20",
          any(v.rule_id == METHOD_TOO_LONG and v.magnitude == 21 for v in pv))


def test_java_method_detector():
    catalog = RuleCatalog.defaults()
    java_long = {
        "src/main/java/Order.java":
        "class Order {\n"
        "  void placeOrder() {\n"
        + "".join(f"    int value{i} = {i};\n" for i in range(19))
        + "  }\n}\n"
    }
    jv = detectors.scan(java_long, catalog)
    check("java method-too-long fires >20",
          any(v.rule_id == METHOD_TOO_LONG and v.magnitude == 21 for v in jv))


def test_java_method_noise():
    catalog = RuleCatalog.defaults()
    java_noise = {
        "src/main/java/Annotated.java":
        "class Annotated {\n"
        "  @Deprecated\n"
        "  public <T> void placeOrder(\n"
        "      T value\n"
        "  ) {\n"
        '    String braces = \"{}\";\n'
        "    // } ignored\n"
        + "".join(f"    int value{i} = {i};\n" for i in range(15))
        + "  }\n}\n"
    }
    nv = detectors.scan(java_noise, catalog)
    check("java scanner handles annotations and ignored braces",
          any(v.rule_id == METHOD_TOO_LONG for v in nv))


def _violation(rule=FILE_TOO_LONG, path="app/big.py", start=1, end=350,
               subject="app/big.py", magnitude=None):
    return Violation(rule, CodeLocation(path, LineRange(start, end)),
                     subject, "msg", magnitude)


def test_new_only_and_line_level():
    changeset = Changeset({"app/big.py": [LineRange(1, 350)]})
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [])
    check("new violation on changed lines is admitted", len(run.findings()) == 1)
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation()], [_violation()])
    check("pre-existing violation stays silent", run.findings() == [])
    untouched = Changeset({"other.py": [LineRange(1, 5)]})
    run = ReviewRun.open("base", "head", untouched)
    run.assess([_violation()], [])
    check("violation off changed lines is not reported", run.findings() == [])


def test_line_shift_and_worsening():
    changeset = Changeset({"app/big.py": [LineRange(1, 350)]})
    run = ReviewRun.open("base", "head", changeset)
    run.assess([_violation(start=1, end=360)], [_violation(start=1, end=350)])
    check("subject match survives line shift", run.findings() == [])
    method_changes = Changeset({"app/order.py": [LineRange(25, 26)]})
    head = _violation(METHOD_TOO_LONG, "app/order.py", 1, 26,
                      "app/order.py::place_order", 26)
    base = _violation(METHOD_TOO_LONG, "app/order.py", 1, 24,
                      "app/order.py::place_order", 24)
    run = ReviewRun.open("base", "head", method_changes)
    run.assess([head], [base])
    check("worsened method violation is admitted", len(run.findings()) == 1)

    run = ReviewRun.open("base", "head", method_changes)
    run.assess([base], [base])
    check("unchanged method violation stays silent", run.findings() == [])
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
    check("clean summary says no violations",
          "No new or worsened hard-rule violations" in delivery.summary_markdown(clean))

    payload = delivery.machine_findings(report)
    check("machine schema is versioned", payload["schema"] == "oopforge.domain-review.v1")
    check("machine findings count matches", len(payload["findings"]) == 1)


def main():
    print("domain-review self-test:")
    test_changeset_parse()
    test_file_length_detector()
    test_import_detector()
    test_python_method_detector()
    test_java_method_detector()
    test_java_method_noise()
    test_new_only_and_line_level()
    test_line_shift_and_worsening()
    test_delivery()
    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
