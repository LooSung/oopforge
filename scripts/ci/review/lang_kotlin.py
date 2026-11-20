"""Kotlin patterns for the per-file review detectors.

The mutable-field check is a text scan, not a parser. It reports a public `var`
declared in a primary constructor or directly in a class/object body, unless a
`private set` or `protected set` follows it. A `var` inside a function, `init`
block, or lambda is local state and is not reported.
"""
from __future__ import annotations

import re
from typing import Dict, List

EXTENSIONS = (".kt",)

FRAMEWORK_IMPORT = re.compile(
    r"^\s*import\s+(org\.springframework|jakarta\.persistence|"
    r"javax\.persistence|org\.hibernate)[\w.]*"
)
REPOSITORY_IMPORT = re.compile(
    r"^\s*import\s+([\w.]*repository[\w.]*)", re.IGNORECASE
)

_NOISE = re.compile(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\])*\"", re.DOTALL)
_TYPE_HEADER = re.compile(r"(?<!:)\b(class|object|interface)\b")
_CLASS_PARAMS = re.compile(r"\bclass\s+\w+[^({\n]*\(")
_VAR = re.compile(r"((?:[a-z]+\s+)*)var\s+([A-Za-z_]\w*)")
_RESTRICTED_SET = re.compile(r"^\s*(private|protected)\s+set\b")
_HIDDEN = {"private", "protected", "internal"}


def _blank(match: re.Match) -> str:
    return re.sub(r"[^\n]", " ", match.group())


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _is_public(modifiers: str) -> bool:
    return not (_HIDDEN & set(modifiers.split()))


def _closing_paren(text: str, opening: int) -> int:
    depth = 0
    for index in range(opening, len(text)):
        depth += {"(": 1, ")": -1}.get(text[index], 0)
        if depth == 0:
            return index
    return len(text)


def _constructor_vars(text: str) -> Dict[str, int]:
    fields: Dict[str, int] = {}
    for header in _CLASS_PARAMS.finditer(text):
        opening = header.end() - 1
        params = text[opening:_closing_paren(text, opening)]
        for match in _VAR.finditer(params):
            if _is_public(match.group(1)):
                fields[match.group(2)] = _line_of(text, opening + match.start(2))
    return fields


def _member_lines(text: str) -> List[int]:
    """Line numbers whose statements sit directly in a class/object body."""
    stack: List[bool] = []
    statement_start, member = 0, []
    for index, char in enumerate(text):
        if char == "{":
            stack.append(bool(_TYPE_HEADER.search(text[statement_start:index])))
            statement_start = index + 1
        elif char == "}":
            if stack:
                stack.pop()
            statement_start = index + 1
        elif char in "\n;":
            statement_start = index + 1
            if stack and stack[-1]:
                member.append(_line_of(text, index) + 1)
    return member


def _restricted_setter(lines: List[str], line: int) -> bool:
    same = lines[line - 1]
    if re.search(r"\b(private|protected)\s+set\b", same):
        return True
    for following in lines[line:]:
        if following.strip():
            return bool(_RESTRICTED_SET.match(following))
    return False


def public_mutable_fields(content: str) -> Dict[str, int]:
    text = _NOISE.sub(_blank, content)
    lines = text.splitlines()
    fields = _constructor_vars(text)
    for line in sorted(set(_member_lines(text))):
        if line > len(lines):
            continue
        match = re.match(r"\s*" + _VAR.pattern, lines[line - 1])
        if match and _is_public(match.group(1)) and not _restricted_setter(lines, line):
            fields[match.group(2)] = line
    return fields
