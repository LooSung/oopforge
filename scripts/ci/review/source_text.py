"""Text-scan helpers shared by the brace-language detector modules."""
from __future__ import annotations

import re
from typing import List


def blank(match: re.Match) -> str:
    """Replace a match with spaces, keeping its newlines so line numbers hold."""
    return re.sub(r"[^\n]", " ", match.group())


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def closing_paren(text: str, opening: int) -> int:
    depth = 0
    for index in range(opening, len(text)):
        depth += {"(": 1, ")": -1}.get(text[index], 0)
        if depth == 0:
            return index
    return len(text)


def member_lines(text: str, type_header: re.Pattern) -> List[int]:
    """Lines directly in a type body: a `{` whose statement matches type_header."""
    stack: List[bool] = []
    statement_start, member = 0, []
    for index, char in enumerate(text):
        if char == "{":
            stack.append(bool(type_header.search(text[statement_start:index])))
            statement_start = index + 1
        elif char == "}":
            if stack:
                stack.pop()
            statement_start = index + 1
        elif char in "\n;":
            statement_start = index + 1
            if stack and stack[-1]:
                member.append(line_of(text, index) + 1)
    return member
