"""Adapter: reuse scripts/ci/archlint.py on a git ref via a detached worktree.

Layered checks run only when controller/ or router/ folders exist. CQRS
checks run only when command/query service files exist. Hexagonal trees
without those signals are skipped so ports-and-adapters layout is not
scored as a flat-package miss.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from typing import List

from .model import (
    ARCHLINT_COMMAND_RETURNS_READ,
    ARCHLINT_CONTROLLER_REPOSITORY,
    ARCHLINT_FLAT_PACKAGE,
    ARCHLINT_LAYER_MISPLACED,
    ARCHLINT_QUERY_MUTATION,
    CodeLocation,
    LineRange,
    RuleCatalog,
    SCOPE_FILE,
    Violation,
)

_CI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CI_DIR not in sys.path:
    sys.path.insert(0, _CI_DIR)

import archlint  # noqa: E402

_RULES = (
    ("L1 flat-package", ARCHLINT_FLAT_PACKAGE),
    ("L1 misplaced", ARCHLINT_LAYER_MISPLACED),
    ("L2 controller->repository", ARCHLINT_CONTROLLER_REPOSITORY),
    ("L2 router->repository", ARCHLINT_CONTROLLER_REPOSITORY),
    ("C1 query-mutation", ARCHLINT_QUERY_MUTATION),
    ("C2 command-returns-read", ARCHLINT_COMMAND_RETURNS_READ),
)


def _walk(root: str, catalog: RuleCatalog):
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel != "." and catalog.excludes(rel + "/"):
            dirnames[:] = []
            continue
        yield dirpath, dirnames, filenames


def select_modes(root: str, catalog: RuleCatalog) -> List[str]:
    modes: List[str] = []
    suffixes = (
        "CommandService.java", "command_service.py",
        "QueryService.java", "query_service.py",
    )
    layered = cqrs = False
    for _, dirnames, filenames in _walk(root, catalog):
        if "controller" in dirnames or "router" in dirnames:
            layered = True
        if any(name.endswith(suffixes) for name in filenames):
            cqrs = True
    if layered:
        modes.append("layered")
    if cqrs:
        modes.append("cqrs")
    return modes


def _rule_for(message: str) -> str | None:
    for prefix, rule_id in _RULES:
        if message.startswith(prefix + ":"):
            return rule_id
    return None


def _path_for(message: str) -> str:
    rest = message.split(": ", 1)[1]
    return rest.split(" ", 1)[0].split("::", 1)[0]


def parse_messages(messages: List[str], catalog: RuleCatalog) -> List[Violation]:
    out: List[Violation] = []
    for message in messages:
        rule_id = _rule_for(message)
        if rule_id is None or not catalog.is_enabled(rule_id):
            continue
        path = _path_for(message)
        if catalog.excludes(path):
            continue
        out.append(Violation(
            rule_id,
            CodeLocation(path, LineRange(1, 1)),
            subject_key=f"{path}::{rule_id}",
            message=message,
            scope=SCOPE_FILE,
        ))
    return out


def _lint_root(root: str, catalog: RuleCatalog) -> List[str]:
    messages: List[str] = []
    for mode in select_modes(root, catalog):
        messages.extend(archlint.lint(mode, root))
    return messages


def _git(args: List[str], root: str) -> bool:
    try:
        subprocess.run(
            ["git", *args], cwd=root, check=True,
            capture_output=True, text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def scan_tree(root: str, ref: str, catalog: RuleCatalog) -> List[Violation]:
    tmp = tempfile.mkdtemp(prefix="oopforge-archlint-")
    try:
        if not _git(["worktree", "add", "--detach", tmp, ref], root):
            return []
        return parse_messages(_lint_root(tmp, catalog), catalog)
    finally:
        _git(["worktree", "remove", "--force", tmp], root)
        shutil.rmtree(tmp, ignore_errors=True)
