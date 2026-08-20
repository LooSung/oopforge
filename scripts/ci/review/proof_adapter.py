"""Proof-only checks layered on the canonical domain-review detectors."""
from __future__ import annotations

import re
from typing import Dict, Iterable, List

from .model import CodeLocation, LineRange, SCOPE_FILE, Violation

INVARIANT_OUTSIDE_DOMAIN = "INVARIANT_OUTSIDE_DOMAIN"
POSSIBLE_UNRELATED_CHANGE = "POSSIBLE_UNRELATED_CHANGE"
MISSING_DOMAIN_BEHAVIOR = "MISSING_DOMAIN_BEHAVIOR"
MISSING_INJECTABLE_TIME = "MISSING_INJECTABLE_TIME"
MISSING_DOMAIN_TEST = "MISSING_DOMAIN_TEST"
MISSING_USE_CASE_TEST = "MISSING_USE_CASE_TEST"
MISSING_API_TEST = "MISSING_API_TEST"

_INVARIANT_TERMS = re.compile(
    r"timedelta\s*\(\s*minutes\s*=\s*5|300\b|already\s+void|"
    r"voided.*(?:raise|if)",
    re.IGNORECASE,
)
_NON_DOMAIN_LAYERS = (
    "app/application/",
    "app/presentation/",
    "app/infrastructure/",
)
_ALLOWED_FILES = {".gitignore", "pyproject.toml"}
_COVERAGE_RULES = {
    "domain_behavior": MISSING_DOMAIN_BEHAVIOR,
    "injectable_time": MISSING_INJECTABLE_TIME,
    "domain_test": MISSING_DOMAIN_TEST,
    "use_case_test": MISSING_USE_CASE_TEST,
    "api_test": MISSING_API_TEST,
}


def scan_invariants(files: Dict[str, str]) -> List[Violation]:
    findings: List[Violation] = []
    for path, content in files.items():
        if not path.startswith(_NON_DOMAIN_LAYERS):
            continue
        match = _INVARIANT_TERMS.search(content)
        if match is None:
            continue
        line = content.count("\n", 0, match.start()) + 1
        findings.append(Violation(
            INVARIANT_OUTSIDE_DOMAIN,
            CodeLocation(path, LineRange(line, line)),
            subject_key=f"{path}::{INVARIANT_OUTSIDE_DOMAIN}",
            message="voiding invariant appears outside the domain layer.",
        ))
    return findings


def unrelated_violations(paths: Iterable[str]) -> List[Violation]:
    return [
        Violation(
            POSSIBLE_UNRELATED_CHANGE,
            CodeLocation(path, LineRange(1, 1)),
            subject_key=f"{path}::{POSSIBLE_UNRELATED_CHANGE}",
            message="changed file is outside the proof task surface.",
            scope=SCOPE_FILE,
        )
        for path in paths
        if not path.startswith(("app/", "tests/", ".craft/"))
        and path not in _ALLOWED_FILES
    ]


def coverage_checks(files: Dict[str, str]) -> Dict[str, bool]:
    lowered = {path: content.lower() for path, content in files.items()}
    production = "\n".join(
        content for path, content in lowered.items() if path.startswith("app/")
    )
    tests = {
        path: content for path, content in lowered.items()
        if path.startswith("tests/")
    }
    return {
        "domain_behavior": _has_domain_behavior(lowered),
        "injectable_time": _has_injectable_time(production),
        "domain_test": _has_test(tests, ("domain",)),
        "use_case_test": _has_test(tests, ("application", "service")),
        "api_test": _has_test(tests, ("api", "router")),
    }


def _has_domain_behavior(files: Dict[str, str]) -> bool:
    return any(
        "def void" in content
        for path, content in files.items()
        if path.startswith("app/domain/")
    )


def _has_injectable_time(production: str) -> bool:
    return bool(re.search(
        r"def\s+\w+\s*\([^)]*\b(now|current_time)\b|"
        r"self\._?clock\b|\bClock\b",
        production,
    ))


def _has_test(tests: Dict[str, str], path_terms: tuple[str, ...]) -> bool:
    return any(
        "void" in content and any(term in path for term in path_terms)
        for path, content in tests.items()
    )


def missing_coverage_rule_ids(checks: Dict[str, bool]) -> List[str]:
    return [_COVERAGE_RULES[name] for name, passed in checks.items() if not passed]
