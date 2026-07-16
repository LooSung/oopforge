"""Application entry: reviewPullRequest orchestration + git adapter + CLI.

Read-only. Always exits 0 (verdict is NEUTRAL / non-blocking in the MVP).

Run as a module so package imports resolve:
    PYTHONPATH=scripts/ci python3 -m review.main --base origin/main --root "$PWD"
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from typing import Dict, Optional

from .changeset import parse_unified_diff
from .delivery import machine_json, summary_markdown
from .detectors import scan
from .model import ReviewReport, ReviewRun, RuleCatalog


def _git(args, root: str) -> Optional[str]:
    try:
        out = subprocess.run(
            ["git", *args], cwd=root, check=True,
            capture_output=True, text=True,
        )
        return out.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _diff(base: str, head: str, root: str) -> str:
    text = _git(["diff", "-U0", f"{base}...{head}"], root)
    return text or ""


def _read_at(ref: str, path: str, root: str) -> Optional[str]:
    return _git(["show", f"{ref}:{path}"], root)


def _collect(ref: str, paths, root: str) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for path in paths:
        content = _read_at(ref, path, root)
        if content is not None:
            files[path] = content
    return files


def review_pull_request(base: str, head: str, root: str) -> ReviewReport:
    catalog = RuleCatalog.defaults()
    changeset = parse_unified_diff(_diff(base, head, root))
    changed = changeset.files()
    head_violations = scan(_collect(head, changed, root), catalog)
    base_violations = scan(_collect(base, changed, root), catalog)
    run = ReviewRun.open(base, head, changeset)
    run.assess(head_violations, base_violations)
    return run.summarize()


def _parse_args(argv):
    p = argparse.ArgumentParser(description="OOPforge read-only PR domain review.")
    p.add_argument("--base", required=True, help="base ref (e.g. origin/main)")
    p.add_argument("--head", default="HEAD", help="head ref (default HEAD)")
    p.add_argument("--root", default=".", help="repository root")
    p.add_argument("--comment-out", help="write the Markdown summary here")
    p.add_argument("--json-out", help="write the machine-readable findings here")
    return p.parse_args(argv)


def main(argv) -> int:
    args = _parse_args(argv)
    report = review_pull_request(args.base, args.head, args.root)
    summary = summary_markdown(report)
    print(summary)
    if args.comment_out:
        with open(args.comment_out, "w") as fh:
            fh.write(summary + "\n")
    if args.json_out:
        with open(args.json_out, "w") as fh:
            fh.write(machine_json(report) + "\n")
    return 0  # read-only, non-blocking


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
