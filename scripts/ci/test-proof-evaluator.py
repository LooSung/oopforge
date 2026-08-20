#!/usr/bin/env python3
"""Self-test the task-specific C4 proof evaluator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVALUATOR = ROOT / "scripts/proof/evaluate-run.py"
sys.path.insert(0, str(ROOT / "scripts/ci"))

from review.detectors import scan  # noqa: E402
from review.model import (  # noqa: E402
    ARCHLINT_CONTROLLER_REPOSITORY,
    METHOD_TOO_LONG,
    PUBLIC_MUTABLE_DOMAIN_FIELD,
    RuleCatalog,
)
from review.proof_adapter import (  # noqa: E402
    INVARIANT_OUTSIDE_DOMAIN,
    MISSING_API_TEST,
    MISSING_DOMAIN_BEHAVIOR,
    MISSING_DOMAIN_TEST,
    MISSING_USE_CASE_TEST,
)

BASELINE_MODEL = (
    "class Calculation:\n"
    "    def perform(self):\n"
    + "".join(f"        value_{index} = {index}\n" for index in range(21))
)


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def baseline(root: Path) -> None:
    write(root, ".gitkeep", "")
    write(root, "app/domain/calculation/model.py", BASELINE_MODEL)
    write(
        root,
        "app/presentation/router.py",
        "from app.infrastructure.repository import Repository\n",
    )
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=OOPforge",
            "-c",
            "user.email=proof@oopforge.local",
            "commit",
            "-q",
            "-m",
            "baseline",
        ],
        cwd=root,
        check=True,
    )


def evaluate(root: Path) -> dict[str, object]:
    subprocess.run(["git", "add", "-N", "."], cwd=root, check=True)
    result = subprocess.run(
        ["python3", str(EVALUATOR), str(root)],
        text=True,
        capture_output=True,
        check=False,
    )
    return json.loads(result.stdout)


def clean_case(root: Path) -> None:
    write(
        root,
        "app/domain/calculation/model.py",
        BASELINE_MODEL + "    def void(self, now):\n"
        "        self.voided_at = now\n",
    )
    write(
        root,
        "app/presentation/router.py",
        "from app.infrastructure.repository import Repository\n\n"
        "def route():\n"
        "    return 'ok'\n",
    )
    write(
        root,
        "app/application/void_service.py",
        "class VoidService:\n"
        "    def __init__(self, clock):\n"
        "        self.clock = clock\n",
    )
    write(root, "tests/domain/test_calculation.py", "def test_void():\n    assert True\n")
    write(root, "tests/application/test_void_service.py", "def test_void():\n    assert True\n")
    write(root, "tests/test_api.py", "def test_void_api():\n    assert True\n")


def bad_case(root: Path) -> None:
    write(
        root,
        "app/application/void_service.py",
        "from datetime import timedelta\n"
        "from fastapi import HTTPException\n\n"
        "def void(calculation):\n"
        "    if calculation.performed_at + timedelta(minutes=5):\n"
        "        raise HTTPException(409)\n",
    )


def worsen_method(root: Path) -> None:
    write(
        root,
        "app/domain/calculation/model.py",
        BASELINE_MODEL
        + "        added_1 = 1\n"
        + "        added_2 = 2\n",
    )


def prepare(root: Path) -> None:
    root.mkdir()
    baseline(root)


def assert_clean(root: Path) -> None:
    prepare(root)
    clean_case(root)
    result = evaluate(root)
    assert result["violation_count"] == 0, result


def assert_bad(root: Path) -> None:
    prepare(root)
    bad_case(root)
    result = evaluate(root)
    rules = {finding["rule_id"] for finding in result["findings"]}
    expected = {
        INVARIANT_OUTSIDE_DOMAIN,
        MISSING_DOMAIN_BEHAVIOR,
        MISSING_DOMAIN_TEST,
        MISSING_USE_CASE_TEST,
        MISSING_API_TEST,
    }
    assert expected <= rules, result


def assert_worsened(root: Path) -> None:
    prepare(root)
    clean_case(root)
    worsen_method(root)
    result = evaluate(root)
    rules = {finding["rule_id"] for finding in result["findings"]}
    assert METHOD_TOO_LONG in rules, result


def common_rule_files() -> dict[str, str]:
    return {
        "app/domain/order.py":
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class Order:\n"
        "    status: str\n",
        "app/presentation/admin.py":
        "from app.infrastructure.repository import OrderRepository\n",
    }


def assert_common_id_parity(root: Path) -> None:
    prepare(root)
    clean_case(root)
    shared_files = common_rule_files()
    for path, content in shared_files.items():
        write(root, path, content)
    expected = {item.rule_id for item in scan(shared_files, RuleCatalog.defaults())}
    result = evaluate(root)
    actual = {
        item["rule_id"] for item in result["findings"]
        if item["rule_id"] in expected
    }
    assert result["schema"] == "oopforge.proof-evaluation.v2", result
    assert actual == expected, (actual, expected, result)
    canonical = {PUBLIC_MUTABLE_DOMAIN_FIELD, ARCHLINT_CONTROLLER_REPOSITORY}
    assert expected == canonical


def assert_test_files_excluded(root: Path) -> None:
    prepare(root)
    clean_case(root)
    path = "tests/domain/test_bad_model.py"
    write(
        root,
        path,
        "from fastapi import Depends\n"
        "from dataclasses import dataclass\n\n"
        "@dataclass\n"
        "class TestOrder:\n"
        "    status: str\n\n"
        "def oversized():\n"
        + "".join(f"    value_{index} = {index}\n" for index in range(21)),
    )
    result = evaluate(root)
    assert all(item.get("file") != path for item in result["findings"]), result


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        assert_clean(Path(temp) / "clean")
        assert_bad(Path(temp) / "bad")
        assert_worsened(Path(temp) / "worsened")
        assert_common_id_parity(Path(temp) / "parity")
        assert_test_files_excluded(Path(temp) / "test-exclusion")
    print("proof evaluator self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
