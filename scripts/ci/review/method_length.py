"""Shared stdlib-only Python, Java, and Kotlin method span scanner."""
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
_KOTLIN_FUN = re.compile(
    r"(?m)^(?P<indent>[ \t]*)(?:@[\w.:]+(?:\([^)]*\))?\s+)*"
    r"(?:(?:public|protected|private|internal|override|open|final|abstract|"
    r"suspend|inline|operator|infix|tailrec|external)\s+)*"
    r"fun\s+(?:<[^>]+>\s*)?(?:[\w.<>?]+\.)?(?P<name>[A-Za-z_]\w*)\s*\("
)
_KOTLIN_BODY = re.compile(r"[ \t]*(?::[ \t]*[^={\n]+?)?[ \t]*([={])")
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


def _matching_paren(content: str, opening: int) -> int | None:
    depth = 0
    for index in range(opening, len(content)):
        depth += {"(": 1, ")": -1}.get(content[index], 0)
        if depth == 0:
            return index
    return None


def _expression_end(lines: list[str], first: int, indent: int) -> int:
    """An expression body ends before the next line at the same or lower indent.

    A closing bracket at the function's own indent still belongs to it.
    """
    end = first
    for number in range(first + 1, len(lines) + 1):
        line = lines[number - 1]
        depth = len(line) - len(line.lstrip())
        if not line.strip() or depth > indent:
            end = number if line.strip() else end
            continue
        if depth == indent and line.lstrip()[0] in ")]}":
            end = number
            continue
        break
    return end


def _kotlin_span_end(clean: str, lines: list[str], body: re.Match, indent: int) -> int | None:
    if body.group(1) == "{":
        closing = _matching_brace(clean, body.end() - 1)
        return None if closing is None else clean.count("\n", 0, closing) + 1
    return _expression_end(lines, clean.count("\n", 0, body.end()) + 1, indent)


def _kotlin_methods(content: str) -> list[MethodSpan]:
    clean = _strip_java_noise(content)
    lines = clean.splitlines()
    methods: list[MethodSpan] = []
    for match in _KOTLIN_FUN.finditer(clean):
        closing = _matching_paren(clean, match.end() - 1)
        body = None if closing is None else _KOTLIN_BODY.match(clean, closing + 1)
        if body is None:
            continue
        end = _kotlin_span_end(clean, lines, body, len(match.group("indent")))
        if end is None:
            continue
        params = clean[match.end():closing]
        arity = len([part for part in params.split(",") if part.strip()])
        start = clean.count("\n", 0, match.start()) + 1
        methods.append(MethodSpan(f"{match.group('name')}/{arity}", start, end))
    return methods


def scan_methods(path: str, content: str) -> list[MethodSpan]:
    if path.endswith(".py"):
        return _python_methods(content)
    if path.endswith(".java"):
        return _java_methods(content)
    if path.endswith(".kt"):
        return _kotlin_methods(content)
    return []
