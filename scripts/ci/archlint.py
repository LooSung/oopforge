#!/usr/bin/env python3
"""OOPforge architecture linter.

Makes the v0.7 AGENTS.md Hard Rules mechanically enforceable, so compliance
does not depend on the agent (or model size) remembering them.

Modes:
  layered  Each layer is its own package/folder; inbound adapter must not
           reference a repository directly (Java/Kotlin *Controller, Python
           router/, TypeScript controller/ and Next.js route.ts).
  cqrs     Query side has no side effects; command methods do not return
           read-shaped types (Response/Summary/Dto/View/ReadModel); a public
           Kotlin or TypeScript command function declares its return type.

Usage:
  archlint.py <layered|cqrs> <root> [<root> ...]

Exit code 0 = clean, 1 = violations found, 2 = bad invocation.
Pure stdlib (no runtime dependencies).
"""
import os
import re
import sys

JVM_LAYER_SUFFIX = {"Controller": "controller", "Service": "service", "Repository": "repository"}
JVM_EXTENSIONS = (".java", ".kt")
PY_LAYER_FOLDERS = {"router", "service", "repository", "domain", "readmodel"}
PY_LAYER_FILE = re.compile(r"(router|service|repository)", re.I)
MUTATING = re.compile(r"(\b(save|delete|update|insert|persist|store|remove)\s*\()|\.(save|delete)\s*\(")
READ_SHAPED = re.compile(r"[A-Za-z0-9_\[\],\s]*(Response|Summary|Dto|DTO|View|ReadModel)\b")
JAVA_METHOD = re.compile(r"public\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)")
PY_RETURN = re.compile(r"def\s+\w+\s*\([^)]*\)\s*->\s*([^:\n]+)")
KOTLIN_FUN = re.compile(
    r"^[ \t]*((?:[a-z]+[ \t]+)*)fun[ \t]+([A-Za-z0-9_]+)[ \t]*\(([^)]*)\)"
    r"[ \t]*(?::[ \t]*([^={\n]+?))?[ \t]*(=|\{|$)",
    re.M,
)
KOTLIN_HIDDEN = {"private", "internal", "protected"}
TS_LAYER_FOLDERS = {"controller", "service", "repository", "domain"}
TS_LAYER_FILE = re.compile(r"(controller|service|repository)", re.I)
TS_SKIP_DIRS = {"node_modules", ".next"}
TS_REPOSITORY_IMPORT = re.compile(r"""(?:from|import)\s*\(?\s*['"]([^'"]*repository[^'"]*)['"]""", re.I)
TS_METHOD = re.compile(
    r"^[ \t]*(?:export\s+)?((?:(?:public|private|protected|static|async|override)\s+)*)"
    r"(?:function\s+)?(#?[A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*(?::\s*([^{=;]+?))?\s*(\{|;|$)",
    re.M,
)
TS_NOT_METHODS = {"if", "for", "while", "switch", "catch", "return", "constructor"}


def _read(path):
    with open(path) as fh:
        return fh.read()


def jvm_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(JVM_EXTENSIONS):
                yield os.path.join(d, f)


def python_files(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".py") and f != "__init__.py":
                yield os.path.join(d, f)


def ts_files(root):
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in TS_SKIP_DIRS]
        for f in fs:
            if f.endswith(".ts") and not f.endswith(".d.ts"):
                yield os.path.join(d, f)


def ts_layer_tag(path):
    parent = os.path.basename(os.path.dirname(path))
    if parent in TS_LAYER_FOLDERS:
        return parent
    match = TS_LAYER_FILE.search(os.path.basename(path))
    return match.group(1).lower() if match else None


def jvm_suffix(fname):
    base = os.path.splitext(fname)[0]
    for suf in JVM_LAYER_SUFFIX:
        if base.endswith(suf):
            return suf
    return None


def py_layer_tag(path, root):
    parent = os.path.basename(os.path.dirname(path))
    if parent in PY_LAYER_FOLDERS:
        return parent
    match = PY_LAYER_FILE.search(os.path.basename(path))
    return match.group(1).lower() if match else None


def check_layered_jvm(root):
    v, by_dir = [], {}
    for path in jvm_files(root):
        suf = jvm_suffix(os.path.basename(path))
        if suf:
            by_dir.setdefault(os.path.dirname(path), set()).add(suf)
    for d, sufs in by_dir.items():
        if len(sufs) >= 2:
            v.append(f"L1 flat-package: {os.path.relpath(d, root)} mixes layers {sorted(sufs)} in one folder")
    for path in jvm_files(root):
        suf = jvm_suffix(os.path.basename(path))
        if suf and os.path.basename(os.path.dirname(path)) != JVM_LAYER_SUFFIX[suf]:
            v.append(f"L1 misplaced: {os.path.relpath(path, root)} should be under {JVM_LAYER_SUFFIX[suf]}/")
    for path in jvm_files(root):
        if jvm_suffix(os.path.basename(path)) == "Controller" and re.search(r"\bRepository\b", _read(path)):
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


def _java_command_violations(rel, txt):
    return [f"C2 command-returns-read: {rel}::{mname} returns read-shaped '{ret}'"
            for ret, mname, _args in JAVA_METHOD.findall(txt) if READ_SHAPED.match(ret)]


def _kotlin_command_violations(rel, txt):
    v = []
    for mods, mname, _args, ret, term in KOTLIN_FUN.findall(txt):
        if KOTLIN_HIDDEN & set(mods.split()):
            continue
        if not ret and term == "=":
            v.append(f"C2 command-implicit-return: {rel}::{mname} has an expression body without a declared return type")
        elif ret and READ_SHAPED.search(ret):
            v.append(f"C2 command-returns-read: {rel}::{mname} returns read-shaped '{ret.strip()}'")
    return v


def check_cqrs_jvm(root):
    v = []
    for path in jvm_files(root):
        base, ext = os.path.splitext(os.path.basename(path))
        rel, txt = os.path.relpath(path, root), _read(path)
        if base.endswith(("QueryService", "QueryController")) and MUTATING.search(txt):
            v.append(f"C1 query-mutation: {rel} contains a mutating operation")
        if base.endswith("CommandService"):
            check = _kotlin_command_violations if ext == ".kt" else _java_command_violations
            v += check(rel, txt)
    return v


def check_layered_ts(root):
    v, by_dir = [], {}
    for path in ts_files(root):
        tag = ts_layer_tag(path)
        if tag:
            by_dir.setdefault(os.path.dirname(path), set()).add(tag)
    for d, tags in by_dir.items():
        if len(tags) >= 2:
            v.append(f"L1 flat-package: {os.path.relpath(d, root)} mixes layers {sorted(tags)} in one folder")
    for path in ts_files(root):
        tag, rel = ts_layer_tag(path), os.path.relpath(path, root)
        if tag and os.path.basename(os.path.dirname(path)) != tag:
            v.append(f"L1 misplaced: {rel} should be under {tag}/")
        inbound = tag == "controller" or os.path.basename(path) == "route.ts"
        if inbound and TS_REPOSITORY_IMPORT.search(_read(path)):
            v.append(f"L2 controller->repository: {rel} imports a repository directly")
    return v


def _ts_command_violations(rel, txt):
    v = []
    for mods, mname, _args, ret, term in TS_METHOD.findall(txt):
        hidden = {"private", "protected"} & set(mods.split()) or mname.startswith("#")
        if hidden or mname in TS_NOT_METHODS or term != "{":
            continue
        if not ret:
            v.append(f"C2 command-implicit-return: {rel}::{mname} has no declared return type")
        elif READ_SHAPED.search(ret):
            v.append(f"C2 command-returns-read: {rel}::{mname} returns read-shaped '{ret.strip()}'")
    return v


def check_cqrs_ts(root):
    v = []
    for path in ts_files(root):
        base = os.path.splitext(os.path.basename(path))[0]
        rel, txt = os.path.relpath(path, root), _read(path)
        if base.endswith(("QueryService", "QueryController")) and MUTATING.search(txt):
            v.append(f"C1 query-mutation: {rel} contains a mutating operation")
        if base.endswith("CommandService"):
            v += _ts_command_violations(rel, txt)
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
    if any(True for _ in jvm_files(root)):
        violations += check_layered_jvm(root) if mode == "layered" else check_cqrs_jvm(root)
    if any(True for _ in ts_files(root)):
        violations += check_layered_ts(root) if mode == "layered" else check_cqrs_ts(root)
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
