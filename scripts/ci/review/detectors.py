"""Adapter: scan a set of files into candidate Violations.

Per-file detectors:
  - FILE_TOO_LONG                 code file > 300 lines
  - SKILL_FILE_TOO_LONG           skills/**/*.md > 200 lines
  - DOMAIN_FRAMEWORK_IMPORT       a file under a `domain/` folder imports a framework
  - METHOD_TOO_LONG               Python/Java method > 20 lines
  - PUBLIC_MUTABLE_DOMAIN_FIELD   public field on a mutable domain dataclass
  - ARCHLINT_CONTROLLER_REPOSITORY presentation imports a repository directly

Project-root archlint reuse lives in archlint_adapter.py.
"""
from __future__ import annotations

import ast
import re
from typing import Dict, List

from .method_length import scan_methods
from .model import (
    ARCHLINT_CONTROLLER_REPOSITORY,
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
_PY_FW = re.compile(
    r"^\s*(?:from|import)\s+(fastapi|pydantic|sqlalchemy|flask|django)\b"
)
_PY_REPOSITORY_IMPORT = re.compile(
    r"^\s*(?:from|import)\s+([\w.]*repository[\w.]*)", re.IGNORECASE
)
_JAVA_REPOSITORY_IMPORT = re.compile(
    r"^\s*import\s+([\w.]*repository[\w.]*)", re.IGNORECASE
)
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


def _is_presentation_file(path: str) -> bool:
    return "/presentation/" in _norm(path) and _is_code_file(path)


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


def _decorator_name(node: ast.expr) -> str:
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id
    return target.attr if isinstance(target, ast.Attribute) else ""


def _is_frozen_dataclass(node: ast.ClassDef) -> bool | None:
    for decorator in node.decorator_list:
        if _decorator_name(decorator) != "dataclass":
            continue
        if not isinstance(decorator, ast.Call):
            return False
        return any(
            item.arg == "frozen"
            and isinstance(item.value, ast.Constant)
            and item.value.value is True
            for item in decorator.keywords
        )
    return None


def _py_public_mutable_fields(content: str) -> Dict[str, int]:
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {}
    fields: Dict[str, int] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or _is_frozen_dataclass(node) is not False:
            continue
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if not item.target.id.startswith("_"):
                    fields[item.target.id] = item.lineno
    return fields


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
            message=f"domain dataclass field '{name}' is publicly mutable; "
                    f"callers can bypass the invariant.",
        )
        for name, line in fields.items()
    ]


def _detect_presentation_repository(path: str, content: str) -> List[Violation]:
    pattern = _PY_REPOSITORY_IMPORT if path.endswith(".py") else _JAVA_REPOSITORY_IMPORT
    out: List[Violation] = []
    for line, raw in enumerate(content.splitlines(), start=1):
        match = pattern.match(raw)
        if match:
            out.append(Violation(
                ARCHLINT_CONTROLLER_REPOSITORY,
                CodeLocation(path, LineRange(line, line)),
                subject_key=f"{path}::repository-import:{match.group(1).lower()}",
                message="presentation code imports a repository directly; "
                        "route through an application service.",
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
        if catalog.is_enabled(METHOD_TOO_LONG) and _is_code_file(path):
            out.extend(_detect_method_too_long(path, content))
        if catalog.is_enabled(PUBLIC_MUTABLE_DOMAIN_FIELD) and _is_domain_file(path):
            out.extend(_detect_public_mutable_domain(path, content))
        if (catalog.is_enabled(ARCHLINT_CONTROLLER_REPOSITORY)
                and _is_presentation_file(path)):
            out.extend(_detect_presentation_repository(path, content))
    return out
