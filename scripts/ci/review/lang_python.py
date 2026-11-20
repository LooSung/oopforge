"""Python patterns for the per-file review detectors."""
from __future__ import annotations

import ast
import re
from typing import Dict

EXTENSIONS = (".py",)

FRAMEWORK_IMPORT = re.compile(
    r"^\s*(?:from|import)\s+(fastapi|pydantic|sqlalchemy|flask|django)\b"
)
REPOSITORY_IMPORT = re.compile(
    r"^\s*(?:from|import)\s+([\w.]*repository[\w.]*)", re.IGNORECASE
)


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


def public_mutable_fields(content: str) -> Dict[str, int]:
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
