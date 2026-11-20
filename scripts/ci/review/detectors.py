"""Adapter: scan a set of files into candidate Violations.

Per-file detectors:
  - FILE_TOO_LONG                 code file > 300 lines
  - SKILL_FILE_TOO_LONG           skills/**/*.md > 200 lines
  - DOMAIN_FRAMEWORK_IMPORT       a file under a `domain/` folder imports a framework
  - METHOD_TOO_LONG               Python/Java method > 20 lines
  - PUBLIC_MUTABLE_DOMAIN_FIELD   public field on a mutable domain dataclass
  - ARCHLINT_CONTROLLER_REPOSITORY presentation imports a repository directly

Per-language patterns live in lang_<language>.py; project-root archlint reuse
lives in archlint_adapter.py.
"""
from __future__ import annotations

from types import ModuleType
from typing import List, Optional

from . import lang_java, lang_python
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

_LANGUAGES = (lang_java, lang_python)


def _language(path: str) -> Optional[ModuleType]:
    for language in _LANGUAGES:
        if path.endswith(language.EXTENSIONS):
            return language
    return None


def _norm(path: str) -> str:
    return "/" + path.replace("\\", "/").lstrip("/")


def _is_code_file(path: str) -> bool:
    return _language(path) is not None


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
    pattern = _language(path).FRAMEWORK_IMPORT
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


def _detect_public_mutable_domain(path: str, content: str) -> List[Violation]:
    fields = _language(path).public_mutable_fields(content)
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
    pattern = _language(path).REPOSITORY_IMPORT
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
