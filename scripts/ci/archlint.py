#!/usr/bin/env python3
"""OOPforge architecture linter.

Makes the v0.7 AGENTS.md Hard Rules mechanically enforceable, so compliance
does not depend on the agent (or model size) remembering them.

Modes:
  layered  Each layer is its own package/folder; inbound adapter must not
           reference a repository directly (Java *Controller, Python router/).
  cqrs     Query side has no side effects; command methods do not return
           read-shaped types (Response/Summary/Dto/View/ReadModel).

Usage:
  archlint.py <layered|cqrs> <root> [<root> ...]

Exit code 0 = clean, 1 = violations found, 2 = bad invocation.
Pure stdlib (no runtime dependencies).
"""
import os
import re
import sys

JAVA_LAYER_SUFFIX = {"Controller": "controller", "Service": "service", "Repository": "repository"}
PY_LAYER_FOLDERS = {"router", "service", "repository", "domain", "readmodel"}
PY_LAYER_FILE = re.compile(r"(router|service|repository)", re.I)
MUTATING = re.compile(r"(\b(save|delete|update|insert|persist|store|remove)\s*\()|\.(save|delete)\s*\(")
READ_SHAPED = re.compile(r"[A-Za-z0-9_\[\],\s]*(Response|Summary|Dto|DTO|View|ReadModel)\b")
JAVA_METHOD = re.compile(r"public\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)")
PY_RETURN = re.compile(r"def\s+\w+\s*\([^)]*\)\s*->\s*([^:\n]+)")


def _read(path):
    with open(path) as fh:
        return fh.read()


def java_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".java"):
                yield os.path.join(d, f)


def python_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".py") and f != "__init__.py":
                yield os.path.join(d, f)


def java_suffix(fname):
    base = fname[:-5]
    for suf in JAVA_LAYER_SUFFIX:
        if base.endswith(suf):
            return suf
    return None


def py_layer_tag(path, root):
    parent = os.path.basename(os.path.dirname(path))
    if parent in PY_LAYER_FOLDERS:
        return parent
    match = PY_LAYER_FILE.search(os.path.basename(path))
    return match.group(1).lower() if match else None


def check_layered_java(root):
    v, by_dir = [], {}
    for path in java_files(root):
        suf = java_suffix(os.path.basename(path))
        if suf:
            by_dir.setdefault(os.path.dirname(path), set()).add(suf)
    for d, sufs in by_dir.items():
        if len(sufs) >= 2:
            v.append(f"L1 flat-package: {os.path.relpath(d, root)} mixes layers {sorted(sufs)} in one folder")
    for path in java_files(root):
        suf = java_suffix(os.path.basename(path))
        if suf and os.path.basename(os.path.dirname(path)) != JAVA_LAYER_SUFFIX[suf]:
            v.append(f"L1 misplaced: {os.path.relpath(path, root)} should be under {JAVA_LAYER_SUFFIX[suf]}/")
    for path in java_files(root):
        if os.path.basename(path).endswith("Controller.java") and re.search(r"\bRepository\b", _read(path)):
            v.append(f"L2 controller->repository: {os.path.relpath(path, root)} references a Repository directly")
    return v


def check_layered_python(root):
    v, by_dir = [], {}
    for path in python_files(root):
        tag = py_layer_tag(path, root)
        if tag:
            by_dir.setdefault(os.path.dirname(path), set()).add(tag)
    for d, tags in by_dir.items():
        if len(tags) >= 2:
            v.append(f"L1 flat-package: {os.path.relpath(d, root)} mixes layers {sorted(tags)} in one folder")
    for path in python_files(root):
        tag = py_layer_tag(path, root)
        if tag and os.path.basename(os.path.dirname(path)) != tag:
            v.append(f"L1 misplaced: {os.path.relpath(path, root)} should be under {tag}/")
    for path in python_files(root):
        if os.path.basename(os.path.dirname(path)) != "router":
            continue
        if re.search(r"(^|\n)\s*(from|import)\s+[\w.]*repository", _read(path)):
            v.append(f"L2 router->repository: {os.path.relpath(path, root)} imports repository directly")
    return v


def check_cqrs_java(root):
    v = []
    for path in java_files(root):
        name = os.path.basename(path)
        txt = _read(path)
        if name.endswith(("QueryService.java", "QueryController.java")) and MUTATING.search(txt):
            v.append(f"C1 query-mutation: {os.path.relpath(path, root)} contains a mutating operation")
        if name.endswith("CommandService.java"):
            for ret, mname, _args in JAVA_METHOD.findall(txt):
                if READ_SHAPED.match(ret):
                    v.append(f"C2 command-returns-read: {os.path.relpath(path, root)}::{mname} returns read-shaped '{ret}'")
    return v


def check_cqrs_python(root):
    v = []
    for path in python_files(root):
        name = os.path.basename(path)
        txt = _read(path)
        if name.endswith("query_service.py") and MUTATING.search(txt):
            v.append(f"C1 query-mutation: {os.path.relpath(path, root)} contains a mutating operation")
        if name.endswith("command_service.py"):
            for ret in PY_RETURN.findall(txt):
                if READ_SHAPED.search(ret):
                    v.append(f"C2 command-returns-read: {os.path.relpath(path, root)} returns read-shaped '{ret.strip()}'")
    return v


def lint(mode, root):
    violations = []
    if any(True for _ in java_files(root)):
        violations += check_layered_java(root) if mode == "layered" else check_cqrs_java(root)
    if any(True for _ in python_files(root)):
        violations += check_layered_python(root) if mode == "layered" else check_cqrs_python(root)
    return violations


def main(argv):
    if len(argv) < 3 or argv[1] not in ("layered", "cqrs"):
        print(__doc__)
        return 2
    mode, roots = argv[1], argv[2:]
    total = 0
    for root in roots:
        v = lint(mode, root)
        if v:
            total += len(v)
            print(f"FAIL ({mode}) {root}")
            for x in v:
                print("  -", x)
        else:
            print(f"PASS ({mode}) {root}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
