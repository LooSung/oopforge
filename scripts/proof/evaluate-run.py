#!/usr/bin/env python3
"""Evaluate one C4 proof workspace with deterministic, task-specific checks."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path


FRAMEWORK_IMPORT = re.compile(r"^\s*(?:from|import)\s+(fastapi|pydantic|sqlalchemy)\b", re.MULTILINE)
REPOSITORY_IMPORT = re.compile(r"^\s*(?:from|import)\s+.*repository", re.MULTILINE)
INVARIANT_TERMS = re.compile(
    r"timedelta\s*\(\s*minutes\s*=\s*5|300\b|already\s+void|voided.*(?:raise|if)",
    re.IGNORECASE,
)


def changed_files(root: Path) -> list[Path]:
    output = subprocess.check_output(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
        cwd=root,
        text=True,
    )
    return [root / line for line in output.splitlines() if line]


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def baseline_text(root: Path, rel: str) -> str:
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def method_length_findings(content: str, rel: str) -> list[dict[str, object]]:
    if not rel.endswith(".py"):
        return []
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return [{"rule": "syntax-error", "file": rel}]
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.end_lineno is None:
            continue
        length = node.end_lineno - node.lineno + 1
        if length > 20:
            findings.append(
                {
                    "rule": "method-over-20-lines",
                    "file": rel,
                    "method": node.name,
                    "lines": length,
                }
            )
    return findings


def content_findings(content: str, rel: str) -> list[dict[str, object]]:
    findings = method_length_findings(content, rel)
    line_count = len(content.splitlines())
    if line_count > 300:
        findings.append({"rule": "file-over-300-lines", "file": rel, "lines": line_count})
    if rel.startswith("app/domain/") and FRAMEWORK_IMPORT.search(content):
        findings.append({"rule": "domain-framework-import", "file": rel})
    if rel.startswith("app/presentation/") and REPOSITORY_IMPORT.search(content):
        findings.append({"rule": "presentation-repository-import", "file": rel})
    if (
        rel.startswith(("app/application/", "app/presentation/", "app/infrastructure/"))
        and INVARIANT_TERMS.search(content)
    ):
        findings.append({"rule": "invariant-outside-domain", "file": rel})
    return findings


def finding_key(finding: dict[str, object]) -> tuple[object, ...]:
    return finding.get("rule"), finding.get("file"), finding.get("method")


def architecture_findings(paths: list[Path], root: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in paths:
        rel = relative(path, root)
        if not path.exists() or path.is_dir():
            continue
        current = content_findings(text(path), rel)
        previous_keys = {
            finding_key(item) for item in content_findings(baseline_text(root, rel), rel)
        }
        findings.extend(item for item in current if finding_key(item) not in previous_keys)
        if not rel.startswith(("app/", "tests/", ".craft/")) and rel not in {
            ".gitignore",
            "pyproject.toml",
        }:
            findings.append({"rule": "possible-unrelated-change", "file": rel})
    return findings


def coverage_checks(paths: list[Path], root: Path) -> dict[str, bool]:
    changed = {relative(path, root): text(path).lower() for path in paths if path.exists()}
    production = "\n".join(
        content for name, content in changed.items() if name.startswith("app/")
    )
    tests = {name: content for name, content in changed.items() if name.startswith("tests/")}
    return {
        "domain_behavior": any(
            "def void" in content
            for name, content in changed.items()
            if name.startswith("app/domain/")
        ),
        "injectable_time": bool(
            re.search(
                r"def\s+\w+\s*\([^)]*\b(now|current_time)\b|self\._?clock\b|\bClock\b",
                production,
            )
        ),
        "domain_test": any("void" in content and "domain" in name for name, content in tests.items()),
        "use_case_test": any(
            "void" in content and ("application" in name or "service" in name)
            for name, content in tests.items()
        ),
        "api_test": any(
            "void" in content and ("api" in name or "router" in name)
            for name, content in tests.items()
        ),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evaluate-run.py <workspace>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    paths = changed_files(root)
    checks = coverage_checks(paths, root)
    findings = architecture_findings(paths, root)
    for name, passed in checks.items():
        if not passed:
            findings.append({"rule": f"missing-{name.replace('_', '-')}"})
    result = {
        "workspace": str(root),
        "changed_files": [relative(path, root) for path in paths],
        "checks": checks,
        "violation_count": len(findings),
        "findings": findings,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
