"""Kotlin patterns for the per-file review detectors.

The mutable-field check is a text scan, not a parser. It reports a public `var`
declared in a primary constructor or directly in a class/object body, unless a
`private set` or `protected set` follows it. A `var` inside a function, `init`
block, or lambda is local state and is not reported.
"""
from __future__ import annotations

import re
from typing import Dict, List

from .source_text import blank, closing_paren, line_of, member_lines

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


def _is_public(modifiers: str) -> bool:
    return not (_HIDDEN & set(modifiers.split()))


def _constructor_vars(text: str) -> Dict[str, int]:
    fields: Dict[str, int] = {}
    for header in _CLASS_PARAMS.finditer(text):
        opening = header.end() - 1
        params = text[opening:closing_paren(text, opening)]
        for match in _VAR.finditer(params):
            if _is_public(match.group(1)):
                fields[match.group(2)] = line_of(text, opening + match.start(2))
    return fields


def _restricted_setter(lines: List[str], line: int) -> bool:
    same = lines[line - 1]
    if re.search(r"\b(private|protected)\s+set\b", same):
        return True
    for following in lines[line:]:
        if following.strip():
            return bool(_RESTRICTED_SET.match(following))
    return False


def public_mutable_fields(content: str) -> Dict[str, int]:
    text = _NOISE.sub(blank, content)
    lines = text.splitlines()
    fields = _constructor_vars(text)
    for line in sorted(set(member_lines(text, _TYPE_HEADER))):
        if line > len(lines):
            continue
        match = re.match(r"\s*" + _VAR.pattern, lines[line - 1])
        if match and _is_public(match.group(1)) and not _restricted_setter(lines, line):
            fields[match.group(2)] = line
    return fields
