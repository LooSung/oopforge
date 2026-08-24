#!/usr/bin/env python3
"""Check local Markdown links in tracked and untracked repository documents."""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+[^)]*)?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
EXTERNAL_SCHEMES = {"data", "http", "https", "mailto", "tel"}


@dataclass(frozen=True)
class Finding:
    source: Path
    line: int
    target: str
    reason: str

    def render(self, root: Path) -> str:
        source = self.source.relative_to(root)
        return f"{source}:{self.line}: {self.reason}: {self.target}"


def without_fenced_code(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    fence = ""
    for number, line in enumerate(text.splitlines(), 1):
        marker = line.lstrip()[:3]
        if marker in {"```", "~~~"}:
            fence = "" if fence == marker else marker
            continue
        if not fence:
            lines.append((number, line))
    return lines


def slugify(heading: str) -> str:
    plain = re.sub(r"[*_`~]", "", heading.strip().lower())
    plain = re.sub(r"[^\w\s\u0080-\uffff-]", "", plain)
    return re.sub(r"[\s-]+", "-", plain).strip("-")


def heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    duplicates: dict[str, int] = {}
    for _, line in without_fenced_code(path.read_text(encoding="utf-8")):
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(1))
        count = duplicates.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        duplicates[base] = count + 1
    return anchors


def local_target(raw: str) -> tuple[str, str] | None:
    target = raw.strip("<>")
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or target.startswith("//"):
        return None
    return urllib.parse.unquote(parsed.path), urllib.parse.unquote(parsed.fragment)


def resolve_target(root: Path, source: Path, path_text: str) -> Path | None:
    target = source if not path_text else source.parent / path_text
    resolved = target.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def check_target(root: Path, source: Path, line: int, raw: str) -> Finding | None:
    parsed = local_target(raw)
    if parsed is None:
        return None
    path_text, fragment = parsed
    target = resolve_target(root, source, path_text)
    if target is None:
        return Finding(source, line, raw, "link escapes repository")
    if not target.exists():
        return Finding(source, line, raw, "missing local target")
    if fragment and target.is_file() and fragment not in heading_anchors(target):
        return Finding(source, line, raw, "missing heading anchor")
    return None


def check_file(root: Path, source: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = source.read_text(encoding="utf-8")
    for line_number, line in without_fenced_code(text):
        for match in LINK_RE.finditer(line):
            finding = check_target(root, source, line_number, match.group(1))
            if finding:
                findings.append(finding)
    return findings


def repository_markdown(root: Path) -> list[Path]:
    result = subprocess.run(
        [
            "git", "ls-files", "-z", "--cached", "--others",
            "--exclude-standard", "--", "*.md",
        ],
        cwd=root,
        check=True,
        capture_output=True,
    )
    paths = [root / item for item in result.stdout.decode().split("\0") if item]
    return [path for path in paths if path.is_file()]


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    findings = [
        finding
        for source in repository_markdown(root)
        for finding in check_file(root, source)
    ]
    if findings:
        for finding in findings:
            print(f"FAIL {finding.render(root)}")
        return 1
    print("OK documentation links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
