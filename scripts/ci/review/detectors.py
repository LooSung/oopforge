"""Adapter: scan a set of files into candidate Violations.

Per-file detectors:
  - FILE_TOO_LONG                 code file > 300 lines
  - SKILL_FILE_TOO_LONG           skills/**/*.md > 200 lines
  - DOMAIN_FRAMEWORK_IMPORT       a file under a `domain/` folder imports a framework
  - METHOD_TOO_LONG               Python/Java method > 20 lines
  - PUBLIC_MUTABLE_DOMAIN_FIELD   public domain field assigned in behavior

Project-root archlint reuse lives in archlint_adapter.py.
"""
from __future__ import annotations

import re
from typing import Dict, List

from .method_length import scan_methods
from .model import (
    CodeLocation,
    DOMAIN_FRAMEWORK_IMPORT,
    FILE_TOO_LONG,
    LineRange,
    METHOD_TOO_LONG,
    PUBLIC_MUTABLE_DOMAIN_FIELD,
    RuleCatalog,
    SKILL_FILE_TOO_LONG,
    Violation,
)

FILE_LIMIT = 300
SKILL_LIMIT = 200
METHOD_LIMIT = 20

_JAVA_FW = re.compile(
    r"^\s*import\s+(org\.springframework|jakarta\.persistence|"
    r"javax\.persistence|org\.hibernate)[\w.]*"
)
_PY_FW = re.compile(r"^\s*(?:from|import)\s+(fastapi|sqlalchemy|flask|django)\b")
_DATACLASS = re.compile(r"^@dataclass(?:\((.*)\))?\s*$")
_PY_FIELD = re.compile(r"^    ([A-Za-z][A-Za-z0-9_]*)\s*:")
_SELF_ASSIGN = re.compile(r"\bself\.([A-Za-z][A-Za-z0-9_]*)\s*=")
_JAVA_PUBLIC_FIELD = re.compile(
    r"^\s*public\s+(?!static|class|interface|enum)[\w.<>,\s]+\s+([A-Za-z][A-Za-z0-9_]*)\s*[;=]"
)
_THIS_ASSIGN = re.compile(r"\bthis\.([A-Za-z][A-Za-z0-9_]*)\s*=")


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


def _detect_method_too_long(path: str, content: str) -> List[Violation]:
    out: List[Violation] = []
    for method in scan_methods(path, content):
        if method.length <= METHOD_LIMIT:
            continue
        out.append(Violation(
            METHOD_TOO_LONG,
            CodeLocation(path, LineRange(method.start, method.end)),
            subject_key=f"{path}::{method.name}",
            message=f"method '{method.name}' is {method.length} lines "
                    f"(limit {METHOD_LIMIT}); extract one responsibility.",
            magnitude=method.length,
        ))
    return out


def _py_public_mutable_fields(content: str) -> Dict[str, int]:
    fields: Dict[str, int] = {}
    assigned: set[str] = set()
    watching = False
    for idx, raw in enumerate(content.splitlines(), start=1):
        deco = _DATACLASS.match(raw.strip())
        if deco is not None:
            watching = "frozen=True" not in (deco.group(1) or "")
            continue
        if not watching:
            continue
        field = _PY_FIELD.match(raw)
        if field:
            fields[field.group(1)] = idx
        assigned.update(_SELF_ASSIGN.findall(raw))
    return {name: line for name, line in fields.items() if name in assigned}


def _java_public_mutable_fields(content: str) -> Dict[str, int]:
    fields = {}
    assigned = set(_THIS_ASSIGN.findall(content))
    for idx, raw in enumerate(content.splitlines(), start=1):
        match = _JAVA_PUBLIC_FIELD.match(raw)
        if match and "final" not in raw.split(match.group(1), 1)[0]:
            fields[match.group(1)] = idx
    return {name: line for name, line in fields.items() if name in assigned}


def _detect_public_mutable_domain(path: str, content: str) -> List[Violation]:
    fields = (
        _py_public_mutable_fields(content) if path.endswith(".py")
        else _java_public_mutable_fields(content)
    )
    return [
        Violation(
            PUBLIC_MUTABLE_DOMAIN_FIELD,
            CodeLocation(path, LineRange(line, line)),
            subject_key=f"{path}::field:{name}",
            message=f"domain field '{name}' is public and assigned in "
                    f"behavior; callers can bypass the invariant.",
        )
        for name, line in fields.items()
    ]


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
        if catalog.is_enabled(METHOD_TOO_LONG) and _is_code_file(path):
            out.extend(_detect_method_too_long(path, content))
        if catalog.is_enabled(PUBLIC_MUTABLE_DOMAIN_FIELD) and _is_domain_file(path):
            out.extend(_detect_public_mutable_domain(path, content))
    return out
