"""Domain model for the PR architecture review (no framework, no I/O).

The core value lives here: deciding which raw violations are NEW (introduced by
the diff) and located on changed lines. Everything else is an adapter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# --- Rule identities (MVP: hard rules only) ---------------------------------
FILE_TOO_LONG = "FILE_TOO_LONG"
SKILL_FILE_TOO_LONG = "SKILL_FILE_TOO_LONG"
DOMAIN_FRAMEWORK_IMPORT = "DOMAIN_FRAMEWORK_IMPORT"

WARN = "WARN"


@dataclass(frozen=True)
class LineRange:
    start: int
    end: int

    def overlaps(self, other: "LineRange") -> bool:
        return self.start <= other.end and other.start <= self.end


@dataclass(frozen=True)
class CodeLocation:
    path: str
    lines: LineRange


@dataclass(frozen=True)
class Violation:
    """Raw detector output (a candidate, before new-only/line-level filtering).

    subject_key is a line-number-independent identity of the violating subject,
    so a violation counts as NEW only when its subject is new -- surviving the
    line shifts a diff introduces.
    """
    rule_id: str
    location: CodeLocation
    subject_key: str
    message: str

    def identity(self) -> Tuple[str, str]:
        return (self.rule_id, self.subject_key)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    location: CodeLocation
    severity: str
    message: str


@dataclass(frozen=True)
class Verdict:
    finding_count: int
    status: str = "NEUTRAL"  # MVP is non-blocking regardless of findings


class Changeset:
    """Added/changed line ranges per changed file (new side of the diff)."""

    def __init__(self, added: Dict[str, List[LineRange]]):
        self._added = {p: list(rs) for p, rs in added.items()}

    def files(self) -> List[str]:
        return sorted(self._added)

    def covers(self, location: CodeLocation) -> bool:
        ranges = self._added.get(location.path)
        if not ranges:
            return False
        return any(location.lines.overlaps(r) for r in ranges)


@dataclass
class RuleCatalog:
    """MVP: fixed hard-rule set + path exclusions. Convention defaults only."""
    enabled: Tuple[str, ...] = (
        FILE_TOO_LONG,
        SKILL_FILE_TOO_LONG,
        DOMAIN_FRAMEWORK_IMPORT,
    )
    exclusions: Tuple[str, ...] = (
        "/test/", "/tests/", "test_", "_test.", ".test.",
        "/build/", "/dist/", "/target/", "/node_modules/",
        "/.venv/", "/__pycache__/", "/vendor/",
        "/examples/",  # runnable references, deliberately illustrate patterns
    )

    @staticmethod
    def defaults() -> "RuleCatalog":
        return RuleCatalog()

    def is_enabled(self, rule_id: str) -> bool:
        return rule_id in self.enabled

    def excludes(self, path: str) -> bool:
        p = "/" + path.replace("\\", "/").lstrip("/")
        return any(token in p for token in self.exclusions)


class ReviewRun:
    """Aggregate root. Owns the new-only + line-level invariants and read-only
    verdict for one pull-request review."""

    def __init__(self, base_ref: str, head_ref: str, changeset: Changeset):
        self._base_ref = base_ref
        self._head_ref = head_ref
        self._changeset = changeset
        self._findings: List[Finding] = []

    @staticmethod
    def open(base_ref: str, head_ref: str, changeset: Changeset) -> "ReviewRun":
        return ReviewRun(base_ref, head_ref, changeset)

    def assess(self, head_violations: List[Violation],
               base_violations: List[Violation]) -> None:
        """Admit a head violation as a Finding only when it is NEW (subject not
        present in base) AND its location overlaps the changeset."""
        base_ids = {v.identity() for v in base_violations}
        for v in head_violations:
            if v.identity() in base_ids:
                continue  # pre-existing subject -> stay silent
            if not self._changeset.covers(v.location):
                continue  # not on changed lines -> out of review scope
            self._findings.append(
                Finding(v.rule_id, v.location, WARN, v.message)
            )

    def findings(self) -> List[Finding]:
        return list(self._findings)

    def verdict(self) -> Verdict:
        return Verdict(finding_count=len(self._findings))

    def summarize(self) -> "ReviewReport":
        return ReviewReport(
            base_ref=self._base_ref,
            head_ref=self._head_ref,
            findings=list(self._findings),
            verdict=self.verdict(),
        )


@dataclass(frozen=True)
class ReviewReport:
    """Read projection of a ReviewRun for delivery."""
    base_ref: str
    head_ref: str
    findings: List[Finding] = field(default_factory=list)
    verdict: Verdict = field(default_factory=lambda: Verdict(0))
