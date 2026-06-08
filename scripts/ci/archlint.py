#!/usr/bin/env python3
"""OOPforge architecture linter.

Makes the v0.7 AGENTS.md Hard Rules mechanically enforceable, so compliance
does not depend on the agent (or model size) remembering them.

Modes:
  layered  Each layer is its own package/folder; a *Controller must not
           reference a Repository directly. (Java suffix convention.)
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

LAYER_SUFFIX = {"Controller": "controller", "Service": "service", "Repository": "repository"}
MUTATING = re.compile(r"\b(save|delete|update|insert|persist|store|remove)\s*\(")
READ_SHAPED = re.compile(r"[A-Za-z0-9_]*(Response|Summary|Dto|DTO|View|ReadModel)\b")
METHOD = re.compile(r"public\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)")


def java_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".java"):
                yield os.path.join(d, f)


def suffix_of(fname):
    base = fname[:-5]  # drop .java
    for suf in LAYER_SUFFIX:
        if base.endswith(suf):
            return suf
    return None


def check_layered(root):
    v = []
    by_dir = {}
    for path in java_files(root):
        suf = suffix_of(os.path.basename(path))
        if suf:
            by_dir.setdefault(os.path.dirname(path), set()).add(suf)
    for d, sufs in by_dir.items():
        if len(sufs) >= 2:
            v.append(f"L1 flat-package: {os.path.relpath(d, root)} mixes layers {sorted(sufs)} in one folder")
    for path in java_files(root):
        suf = suffix_of(os.path.basename(path))
        if suf and os.path.basename(os.path.dirname(path)) != LAYER_SUFFIX[suf]:
            v.append(f"L1 misplaced: {os.path.relpath(path, root)} should be under {LAYER_SUFFIX[suf]}/")
    for path in java_files(root):
        if os.path.basename(path).endswith("Controller.java"):
            if re.search(r"\bRepository\b", open(path).read()):
                v.append(f"L2 controller->repository: {os.path.relpath(path, root)} references a Repository directly")
    return v


def check_cqrs(root):
    v = []
    for path in java_files(root):
        name = os.path.basename(path)
        txt = open(path).read()
        if name.endswith(("QueryService.java", "QueryController.java")):
            if MUTATING.search(txt):
                v.append(f"C1 query-mutation: {os.path.relpath(path, root)} contains a mutating operation")
        if name.endswith("CommandService.java"):
            for ret, mname, _args in METHOD.findall(txt):
                if READ_SHAPED.match(ret):
                    v.append(f"C2 command-returns-read: {os.path.relpath(path, root)}::{mname} returns read-shaped '{ret}'")
    return v


def lint(mode, root):
    return check_layered(root) if mode == "layered" else check_cqrs(root)


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
