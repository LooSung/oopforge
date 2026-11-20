"""TypeScript patterns for the per-file review detectors.

Only `.ts` files are scanned; `.tsx` UI modules belong to Compforge. The
mutable-field check is a text scan, not a parser. It reports a class field
that is neither `readonly`, `private`, `protected`, nor `#private`, and a
`public` constructor parameter property without `readonly`.
"""
from __future__ import annotations

import re
from typing import Dict

from .source_text import blank, closing_paren, line_of, member_lines

EXTENSIONS = (".ts",)

_FROM = r"^\s*import\s+(?:type\s+)?(?:[^'\"]*?\s+from\s+)?['\"]"
FRAMEWORK_IMPORT = re.compile(
    _FROM + r"(next|react|react-dom|zod|@prisma/client|drizzle-orm|typeorm|"
    r"mongoose|sequelize)(?:/[^'\"]*)?['\"]"
)
REPOSITORY_IMPORT = re.compile(
    _FROM + r"([^'\"]*repository[^'\"]*)['\"]", re.IGNORECASE
)

_NOISE = re.compile(
    r"//[^\n]*|/\*.*?\*/|`(?:\\.|[^`\\])*`|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'",
    re.DOTALL,
)
_TYPE_HEADER = re.compile(r"\bclass\b")
_FIELD = re.compile(
    r"\s*((?:(?:public|private|protected|static|readonly|declare|override|abstract)\s+)*)"
    r"([A-Za-z_$][\w$]*)\s*[?!]?\s*[:=]"
)
_CONSTRUCTOR = re.compile(r"\bconstructor\s*\(")
_PUBLIC_PARAM = re.compile(r"\bpublic\s+(?!readonly\b)(?:override\s+)?([A-Za-z_$][\w$]*)")
_HIDDEN = {"private", "protected", "readonly"}


def _constructor_properties(text: str) -> Dict[str, int]:
    fields: Dict[str, int] = {}
    for header in _CONSTRUCTOR.finditer(text):
        opening = header.end() - 1
        params = text[opening:closing_paren(text, opening)]
        for match in _PUBLIC_PARAM.finditer(params):
            fields[match.group(1)] = line_of(text, opening + match.start(1))
    return fields


def public_mutable_fields(content: str) -> Dict[str, int]:
    text = _NOISE.sub(blank, content)
    lines = text.splitlines()
    fields = _constructor_properties(text)
    for line in sorted(set(member_lines(text, _TYPE_HEADER))):
        if line > len(lines):
            continue
        match = _FIELD.match(lines[line - 1])
        if match and not (_HIDDEN & set(match.group(1).split())):
            fields[match.group(2)] = line
    return fields
