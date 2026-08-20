#!/usr/bin/env python3
"""Evaluate one C4 proof workspace using canonical domain-review checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

CI_DIR = Path(__file__).resolve().parents[1] / "ci"
sys.path.insert(0, str(CI_DIR))

from review.changeset import parse_unified_diff  # noqa: E402
from review.detectors import scan  # noqa: E402
from review.model import ReviewRun, RuleCatalog  # noqa: E402
from review.proof_adapter import (  # noqa: E402
    coverage_checks,
    missing_coverage_rule_ids,
    scan_invariants,
    unrelated_violations,
)


def git_output(root: Path, args: list[str]) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=root,
        text=True,
    )


def changed_paths(root: Path) -> list[str]:
    output = git_output(
        root, ["diff", "--name-only", "--diff-filter=ACMR", "HEAD"]
    )
    return [line for line in output.splitlines() if line]


def current_files(root: Path, paths: list[str]) -> dict[str, str]:
    return {
        path: (root / path).read_text(encoding="utf-8", errors="replace")
        for path in paths
        if (root / path).is_file()
    }


def baseline_text(root: Path, rel: str) -> str:
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def baseline_files(root: Path, paths: list[str]) -> dict[str, str]:
    return {path: baseline_text(root, path) for path in paths}


def architecture_findings(
    root: Path,
    paths: list[str],
    current: dict[str, str],
) -> list[dict[str, object]]:
    catalog = RuleCatalog.defaults()
    previous = baseline_files(root, paths)
    head = scan(current, catalog) + scan_invariants(current)
    base = scan(previous, catalog) + scan_invariants(previous)
    head.extend(unrelated_violations(paths))
    changeset = parse_unified_diff(git_output(root, ["diff", "-U0", "HEAD"]))
    run = ReviewRun.open("HEAD", "WORKTREE", changeset)
    run.assess(head, base)
    return [_finding_dict(item) for item in run.findings()]


def _finding_dict(finding) -> dict[str, object]:
    return {
        "rule_id": finding.rule_id,
        "file": finding.location.path,
        "line_start": finding.location.lines.start,
        "line_end": finding.location.lines.end,
        "message": finding.message,
    }


def _missing_findings(checks: dict[str, bool]) -> list[dict[str, object]]:
    return [{"rule_id": rule_id} for rule_id in missing_coverage_rule_ids(checks)]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evaluate-run.py <workspace>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    paths = changed_paths(root)
    current = current_files(root, paths)
    checks = coverage_checks(current)
    findings = architecture_findings(root, paths, current)
    findings.extend(_missing_findings(checks))
    result = {
        "schema": "oopforge.proof-evaluation.v2",
        "workspace": str(root),
        "changed_files": paths,
        "checks": checks,
        "violation_count": len(findings),
        "findings": findings,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
