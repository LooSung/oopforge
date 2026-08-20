#!/usr/bin/env python3
"""Self-test for C2+ domain-review extensions."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from review import delivery  # noqa: E402
from review.archlint_adapter import parse_messages, select_modes  # noqa: E402
from review.detectors import scan  # noqa: E402
from review.model import (  # noqa: E402
    ARCHLINT_CONTROLLER_REPOSITORY,
    ARCHLINT_FLAT_PACKAGE,
    Changeset,
    CodeLocation,
    LineRange,
    PUBLIC_MUTABLE_DOMAIN_FIELD,
    ReviewRun,
    RuleCatalog,
    SCOPE_FILE,
    Violation,
)

FAILURES = []


def check(name, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILURES.append(name)


def test_public_mutable_python():
    catalog = RuleCatalog.defaults()
    leaking = {
        "app/domain/order.py":
        "@dataclass\n"
        "class Order:\n"
        "    voided_at: datetime | None = None\n"
    }
    found = scan(leaking, catalog)
    check("constructor-only public dataclass field fires",
          any(v.rule_id == PUBLIC_MUTABLE_DOMAIN_FIELD for v in found))
    frozen = {
        "app/domain/order.py":
        "@dataclass(frozen=True)\n"
        "class Money:\n"
        "    amount: int\n"
        "    def add(self, now):\n"
        "        return Money(self.amount)\n"
    }
    check("frozen dataclass stays silent", scan(frozen, catalog) == [])


def test_presentation_repository():
    catalog = RuleCatalog.defaults()
    files = {
        "app/presentation/router.py":
        "from app.infrastructure.repository import OrderRepository\n"
    }
    found = scan(files, catalog)
    check("presentation repository import uses canonical boundary ID",
          any(v.rule_id == ARCHLINT_CONTROLLER_REPOSITORY for v in found))
    tests = {
        "tests/app/presentation/router.py":
        "from app.infrastructure.repository import OrderRepository\n"
    }
    check("presentation detector excludes test files", scan(tests, catalog) == [])


def test_file_level_admission():
    changeset = Changeset({"app/router.py": [LineRange(20, 40)]})
    run = ReviewRun.open("base", "head", changeset)
    head = Violation(
        ARCHLINT_CONTROLLER_REPOSITORY,
        CodeLocation("app/router.py", LineRange(1, 1)),
        "app/router.py::ARCHLINT_CONTROLLER_REPOSITORY",
        "L2 router->repository: app/router.py imports repository directly",
        scope=SCOPE_FILE,
    )
    run.assess([head], [])
    check("file-level finding on a changed file is admitted", len(run.findings()) == 1)
    other = Changeset({"app/service.py": [LineRange(1, 5)]})
    run = ReviewRun.open("base", "head", other)
    run.assess([head], [])
    check("file-level finding off the changeset stays silent", run.findings() == [])


def test_archlint_parse_and_modes():
    catalog = RuleCatalog.defaults()
    messages = [
        "L1 flat-package: order mixes layers ['Controller', 'Service'] in one folder",
        "L2 router->repository: app/router.py imports repository directly",
    ]
    parsed = parse_messages(messages, catalog)
    check("archlint parser keeps flat-package",
          any(v.rule_id == ARCHLINT_FLAT_PACKAGE for v in parsed))
    check("archlint parser keeps controller-repository",
          any(v.rule_id == ARCHLINT_CONTROLLER_REPOSITORY for v in parsed))
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "app", "domain"))
        open(os.path.join(tmp, "app", "domain", "model.py"), "w").write("x = 1\n")
        check("hexagonal tree skips layered and cqrs",
              select_modes(tmp, catalog) == [])
        os.makedirs(os.path.join(tmp, "app", "router"))
        open(os.path.join(tmp, "app", "router", "api.py"), "w").write("x = 1\n")
        check("router folder enables layered",
              "layered" in select_modes(tmp, catalog))


def test_correction_delivery():
    changeset = Changeset({"app/domain/order.py": [LineRange(3, 3)]})
    run = ReviewRun.open("base", "head", changeset)
    run.assess([
        Violation(
            PUBLIC_MUTABLE_DOMAIN_FIELD,
            CodeLocation("app/domain/order.py", LineRange(3, 3)),
            "app/domain/order.py::field:voided_at",
            "domain field 'voided_at' is public",
        )
    ], [])
    report = run.summarize()
    prompt = delivery.correction_prompt(report)
    payload = delivery.machine_findings(report)
    check("correction prompt lists the rule", "PUBLIC_MUTABLE_DOMAIN_FIELD" in prompt)
    check("machine JSON marks correction needed", payload["correction"]["needed"] is True)
    check("summary asks the agent to correct", "Agent correction" in delivery.summary_markdown(report))


def main():
    print("domain-review C2+ self-test:")
    test_public_mutable_python()
    test_presentation_repository()
    test_file_level_admission()
    test_archlint_parse_and_modes()
    test_correction_delivery()
    print("RESULT:", "PASS" if not FAILURES else f"FAIL ({FAILURES})")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
