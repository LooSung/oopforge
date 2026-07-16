"""Adapter: scan a set of files into candidate Violations.

MVP hard-rule detectors, all per-file (no project-root inference needed):
  - FILE_TOO_LONG            code file > 300 lines
  - SKILL_FILE_TOO_LONG      skills/**/*.md > 200 lines
  - DOMAIN_FRAMEWORK_IMPORT  a file under a `domain/` folder imports a framework

Method-length (20) and archlint layered/CQRS reuse are deferred (see design doc);
they need language-aware parsing / project-root detection.
"""
from __future__ import annotations

import re
from typing import Dict, List

from .model import (
    CodeLocation,
    DOMAIN_FRAMEWORK_IMPORT,
    FILE_TOO_LONG,
    LineRange,
    RuleCatalog,
    SKILL_FILE_TOO_LONG,
    Violation,
)

FILE_LIMIT = 300
SKILL_LIMIT = 200

_JAVA_FW = re.compile(
    r"^\s*import\s+(org\.springframework|jakarta\.persistence|"
    r"javax\.persistence|org\.hibernate)[\w.]*"
)
_PY_FW = re.compile(r"^\s*(?:from|import)\s+(fastapi|sqlalchemy|flask|django)\b")


def _norm(path: str) -> str:
    return "/" + path.replace("\\", "/").lstrip("/")


def _is_code_file(path: str) -> bool:
    return path.endswith((".py", ".java"))


def _is_skill_file(path: str) -> bool:
    return "/skills/" in _norm(path) and path.endswith(".md")


def _is_domain_file(path: str) -> bool:
    return "/domain/" in _norm(path) and _is_code_file(path)


def _line_count(content: str) -> int:
    if content == "":
        return 0
    return len(content.splitlines())


def _detect_file_too_long(path: str, content: str) -> List[Violation]:
    total = _line_count(content)
    if total <= FILE_LIMIT:
        return []
    return [Violation(
        FILE_TOO_LONG,
        CodeLocation(path, LineRange(1, total)),
        subject_key=path,
        message=f"file is {total} lines (limit {FILE_LIMIT}); a reviewer should hold "
                f"a diff in one sitting.",
    )]


def _detect_skill_too_long(path: str, content: str) -> List[Violation]:
    total = _line_count(content)
    if total <= SKILL_LIMIT:
        return []
    return [Violation(
        SKILL_FILE_TOO_LONG,
        CodeLocation(path, LineRange(1, total)),
        subject_key=path,
        message=f"skill file is {total} lines (limit {SKILL_LIMIT}); one concept "
                f"per skill -- split it.",
    )]


def _detect_domain_framework_import(path: str, content: str) -> List[Violation]:
    pattern = _JAVA_FW if path.endswith(".java") else _PY_FW
    out: List[Violation] = []
    for idx, line in enumerate(content.splitlines(), start=1):
        match = pattern.match(line)
        if not match:
            continue
        symbol = match.group(1)
        out.append(Violation(
            DOMAIN_FRAMEWORK_IMPORT,
            CodeLocation(path, LineRange(idx, idx)),
            subject_key=f"{path}::import:{symbol}",
            message=f"domain file imports framework '{symbol}'; the domain layer "
                    f"must not depend on frameworks.",
        ))
    return out


def scan(files: Dict[str, str], catalog: RuleCatalog) -> List[Violation]:
    """files maps path -> content at one ref. Absent files are simply omitted."""
    out: List[Violation] = []
    for path, content in files.items():
        if catalog.excludes(path):
            continue
        if catalog.is_enabled(FILE_TOO_LONG) and _is_code_file(path):
            out.extend(_detect_file_too_long(path, content))
        if catalog.is_enabled(SKILL_FILE_TOO_LONG) and _is_skill_file(path):
            out.extend(_detect_skill_too_long(path, content))
        if catalog.is_enabled(DOMAIN_FRAMEWORK_IMPORT) and _is_domain_file(path):
            out.extend(_detect_domain_framework_import(path, content))
    return out
