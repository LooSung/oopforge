"""Shared stdlib-only Python and Java method span scanner."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MethodSpan:
    name: str
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


class _PythonMethods(ast.NodeVisitor):
    def __init__(self) -> None:
        self.scope: list[str] = []
        self.methods: list[MethodSpan] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def _visit_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        if node.end_lineno is not None:
            name = ".".join([*self.scope, node.name])
            self.methods.append(MethodSpan(name, node.lineno, node.end_lineno))
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()


_JAVA_METHOD = re.compile(
    r"(?m)^[ \t]*(?:@[\w.]+(?:\([^)]*\))?\s+)*"
    r"(?:(?:public|protected|private|static|final|abstract|synchronized|native|"
    r"strictfp|default)\s+)*(?:<[^>{}]+>\s+)?"
    r"(?:[\w.$<>\[\],?]+\s+)?(?P<name>[A-Za-z_$][\w$]*)\s*"
    r"\((?P<params>[^;{}]*)\)\s*(?:throws\s+[^{]+)?\{"
)
_JAVA_CONTROL = {"if", "for", "while", "switch", "catch", "try", "do"}
_JAVA_NOISE = re.compile(
    r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'",
    re.DOTALL,
)


def _python_methods(content: str) -> list[MethodSpan]:
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []
    visitor = _PythonMethods()
    visitor.visit(tree)
    return visitor.methods


def _strip_java_noise(content: str) -> str:
    return _JAVA_NOISE.sub(
        lambda match: re.sub(r"[^\n]", " ", match.group()),
        content,
    )


def _matching_brace(content: str, opening: int) -> int | None:
    depth = 0
    for index in range(opening, len(content)):
        if content[index] == "{":
            depth += 1
        elif content[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def _java_methods(content: str) -> list[MethodSpan]:
    clean = _strip_java_noise(content)
    methods: list[MethodSpan] = []
    for match in _JAVA_METHOD.finditer(clean):
        name = match.group("name")
        if name in _JAVA_CONTROL:
            continue
        opening = clean.find("{", match.start(), match.end())
        closing = _matching_brace(clean, opening)
        if closing is None:
            continue
        start = clean.count("\n", 0, match.start()) + 1
        end = clean.count("\n", 0, closing) + 1
        arity = 0 if not match.group("params").strip() else match.group("params").count(",") + 1
        methods.append(MethodSpan(f"{name}/{arity}", start, end))
    return methods


def scan_methods(path: str, content: str) -> list[MethodSpan]:
    if path.endswith(".py"):
        return _python_methods(content)
    if path.endswith(".java"):
        return _java_methods(content)
    return []
