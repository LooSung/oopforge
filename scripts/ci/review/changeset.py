"""Adapter: turn a unified diff (`git diff -U0 base...head`) into a Changeset.

Only the new-side (added/modified) line ranges are kept -- those are the lines
the PR is responsible for.
"""
from __future__ import annotations

import re
from typing import Dict, List

from .model import Changeset, LineRange

_FILE_RE = re.compile(r"^\+\+\+ b/(.+)$")
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def parse_unified_diff(diff_text: str) -> Changeset:
    added: Dict[str, List[LineRange]] = {}
    current: str | None = None
    for line in diff_text.splitlines():
        file_match = _FILE_RE.match(line)
        if file_match:
            path = file_match.group(1).strip()
            current = None if path == "/dev/null" else path
            continue
        hunk_match = _HUNK_RE.match(line)
        if hunk_match and current:
            start = int(hunk_match.group(1))
            count = int(hunk_match.group(2) or "1")
            if count == 0:
                continue  # pure deletion -> nothing added on the new side
            added.setdefault(current, []).append(LineRange(start, start + count - 1))
    return Changeset(added)
