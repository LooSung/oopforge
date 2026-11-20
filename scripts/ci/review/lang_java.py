"""Java patterns for the per-file review detectors."""
from __future__ import annotations

import re
from typing import Dict

EXTENSIONS = (".java",)

FRAMEWORK_IMPORT = re.compile(
    r"^\s*import\s+(org\.springframework|jakarta\.persistence|"
    r"javax\.persistence|org\.hibernate)[\w.]*"
)
REPOSITORY_IMPORT = re.compile(
    r"^\s*import\s+([\w.]*repository[\w.]*)", re.IGNORECASE
)
_PUBLIC_FIELD = re.compile(
    r"^\s*public\s+(?!static|class|interface|enum)[\w.<>,\s]+\s+([A-Za-z][A-Za-z0-9_]*)\s*[;=]"
)
_THIS_ASSIGN = re.compile(r"\bthis\.([A-Za-z][A-Za-z0-9_]*)\s*=")


def public_mutable_fields(content: str) -> Dict[str, int]:
    fields = {}
    assigned = set(_THIS_ASSIGN.findall(content))
    for idx, raw in enumerate(content.splitlines(), start=1):
        match = _PUBLIC_FIELD.match(raw)
        if match and "final" not in raw.split(match.group(1), 1)[0]:
            fields[match.group(1)] = idx
    return {name: line for name, line in fields.items() if name in assigned}
