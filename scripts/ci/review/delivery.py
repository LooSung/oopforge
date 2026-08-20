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
    return lines + [
        "",
        "_Only new or worsened violations on changed lines are shown "
        "(read-only, non-blocking)._",
    ]


def summary_markdown(report: ReviewReport) -> str:
    lines = [COMMENT_MARKER, "## OOPforge domain review"]
    findings = sorted(
        report.findings,
        key=lambda f: (f.location.path, f.location.lines.start, f.rule_id),
    )
    lines.extend(_finding_summary(findings) if findings else _clean_summary())
    return "\n".join(lines)


def machine_findings(report: ReviewReport) -> Dict[str, Any]:
    return {
        "schema": "oopforge.domain-review.v1",
        "base_ref": report.base_ref,
        "head_ref": report.head_ref,
        "verdict": {
            "status": report.verdict.status,
            "finding_count": report.verdict.finding_count,
        },
        "findings": [
            {
                "rule_id": f.rule_id,
                "severity": f.severity,
                "path": f.location.path,
                "line_start": f.location.lines.start,
                "line_end": f.location.lines.end,
                "message": f.message,
            }
            for f in report.findings
        ],
    }


def machine_json(report: ReviewReport) -> str:
    return json.dumps(machine_findings(report), indent=2, sort_keys=True)
