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


def summary_markdown(report: ReviewReport) -> str:
    lines = [COMMENT_MARKER, "## OOPforge domain review"]
    findings = sorted(
        report.findings,
        key=lambda f: (f.location.path, f.location.lines.start, f.rule_id),
    )
    if not findings:
        lines.append("")
        lines.append("No new hard-rule violations introduced by this PR. ✅")
        lines.append("")
        lines.append("_Read-only review; pre-existing violations are not reported._")
        return "\n".join(lines)

    lines.append("")
    lines.append(f"Found **{len(findings)}** new hard-rule violation(s) on changed lines:")
    lines.append("")
    lines.append("| Rule | Location | Detail |")
    lines.append("|---|---|---|")
    for f in findings:
        loc = f"`{f.location.path}`:{f.location.lines.start}"
        detail = f.message.replace("|", "\\|")
        lines.append(f"| `{f.rule_id}` | {loc} | {detail} |")
    lines.append("")
    lines.append("_Only NEW violations on changed lines are shown (read-only, non-blocking)._")
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
