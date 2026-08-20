"""Adapter: render a ReviewReport into the read-only delivery surfaces.

Two outputs (design decision G):
  - a human-readable Markdown summary (one aggregated PR comment)
  - a machine-readable JSON artifact for a future agent self-correction loop

Posting the comment / uploading the artifact is done by the GitHub Action; this
module only produces content, so it stays free of any API dependency.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from .model import ReviewReport

# Stable marker lets the workflow find and UPDATE its own comment (idempotent).
COMMENT_MARKER = "<!-- oopforge-domain-review -->"


def _clean_summary() -> list[str]:
    return [
        "",
        "No new or worsened hard-rule violations introduced by this PR. ✅",
        "",
        "_Read-only review; pre-existing violations are not reported._",
    ]


def _finding_summary(findings) -> list[str]:
    lines = [
        "",
        f"Found **{len(findings)}** new or worsened hard-rule violation(s) "
        "on changed lines:",
        "",
        "| Rule | Location | Detail |",
        "|---|---|---|",
    ]
    for f in findings:
        loc = f"`{f.location.path}`:{f.location.lines.start}"
        detail = f.message.replace("|", "\\|")
        lines.append(f"| `{f.rule_id}` | {loc} | {detail} |")
    return lines + _finding_footer()


def _finding_footer() -> list[str]:
    return [
        "",
        "_Only new or worsened violations on the changed surface are shown "
        "(read-only, non-blocking)._",
        "",
        "### Agent correction",
        "",
        "Fix only the listed subjects. Re-run domain review.",
        "Do not mix unrelated refactors.",
    ]


def summary_markdown(report: ReviewReport) -> str:
    lines = [COMMENT_MARKER, "## OOPforge domain review"]
    findings = sorted(
        report.findings,
        key=lambda f: (f.location.path, f.location.lines.start, f.rule_id),
    )
    lines.extend(_finding_summary(findings) if findings else _clean_summary())
    return "\n".join(lines)


def machine_json(report: ReviewReport) -> str:
    return json.dumps(machine_findings(report), indent=2, sort_keys=True)


def _correction_lines(report: ReviewReport) -> list[str]:
    findings = sorted(
        report.findings,
        key=lambda f: (f.location.path, f.location.lines.start, f.rule_id),
    )
    if not findings:
        return ["No correction needed.", ""]
    lines = [
        "Fix only these domain-review findings. Surgical changes only.",
        "Re-run the reviewer after the fix. Do not mix unrelated refactors.",
        "",
    ]
    for index, finding in enumerate(findings, start=1):
        loc = f"{finding.location.path}:{finding.location.lines.start}"
        lines.append(f"{index}. `{finding.rule_id}` at `{loc}` — {finding.message}")
    return lines + [""]


def correction_prompt(report: ReviewReport) -> str:
    return "\n".join(["# OOPforge domain-review correction", ""] + _correction_lines(report))


def _finding_dicts(report: ReviewReport) -> list[Dict[str, Any]]:
    return [
        {
            "rule_id": f.rule_id,
            "severity": f.severity,
            "path": f.location.path,
            "line_start": f.location.lines.start,
            "line_end": f.location.lines.end,
            "message": f.message,
        }
        for f in report.findings
    ]


def machine_findings(report: ReviewReport) -> Dict[str, Any]:
    return {
        "schema": "oopforge.domain-review.v1",
        "base_ref": report.base_ref,
        "head_ref": report.head_ref,
        "verdict": {
            "status": report.verdict.status,
            "finding_count": report.verdict.finding_count,
        },
        "findings": _finding_dicts(report),
        "correction": {
            "needed": report.verdict.finding_count > 0,
            "instruction": "Fix only the listed findings. Surgical. Re-run domain review.",
        },
    }
