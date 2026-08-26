#!/usr/bin/env python3

import json
import pathlib
import sys


def check_manifests(root: pathlib.Path) -> None:
    names = (
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
    )
    claude, _, cursor = [json.loads((root / name).read_text()) for name in names]
    versions = {json.loads((root / name).read_text())["version"] for name in names}
    assert len(versions) == 1, "manifest versions differ"
    assert isinstance(claude.get("repository"), str)
    assert claude.get("skills") == ["./skills/"]
    assert claude.get("commands") == ["./commands/"]
    assert cursor.get("skills") == "./.cursor-plugin/skills/"
    assert "commands" not in cursor, "Cursor must not package Claude commands"


def check_stability(root: pathlib.Path) -> None:
    registry = json.loads((root / "skills/stability.json").read_text())
    listed = registry["stable"] + registry["experimental"]
    actual = sorted(
        str(path.relative_to(root)) for path in (root / "skills").rglob("*.md")
    )
    assert len(listed) == len(set(listed)), "stability registry has duplicates"
    assert sorted(listed) == actual, "skill stability registry differs from files"
    assert registry["schema"] == "oopforge.skill-stability.v1"
    for status in ("stable", "experimental"):
        for relative in registry[status]:
            frontmatter = (root / relative).read_text().split("---", 2)[1]
            assert f"stability: {status}" in frontmatter


def check_required_paths(root: pathlib.Path) -> None:
    required = (
        "commands/craft.md",
        "commands/refactor.md",
        "commands/consult.md",
        "commands/test.md",
        ".cursor-plugin/skills/oopforge/SKILL.md",
        "skills/workflow/craft.md",
        "skills/workflow/consult.md",
        "skills/workflow/test.md",
        "skills/principles/oop-discipline.md",
        "docs/setup/cursor.md",
        "docs/reference/support-scope.md",
    )
    for relative in required:
        assert (root / relative).is_file(), f"missing harness path: {relative}"


def check_activation_probes(root: pathlib.Path) -> None:
    paths = (
        "commands/craft.md",
        "commands/refactor.md",
        "commands/consult.md",
        "commands/test.md",
        "skills/SKILL.md",
        ".cursor-plugin/skills/oopforge/SKILL.md",
    )
    for relative in paths:
        content = (root / relative).read_text()
        assert "OOPFORGE_ACTIVATION_PROBE" in content, f"missing probe: {relative}"


def check_contract(root: pathlib.Path, relative: str, markers: tuple[str, ...]) -> None:
    content = (root / relative).read_text()
    for marker in markers:
        assert marker in content, f"{relative}: missing contract marker: {marker}"


def check_contracts(root: pathlib.Path) -> None:
    check_contract(
        root, "commands/refactor.md", ("workflow/refactor.md", "Do not reclassify")
    )
    check_contract(
        root,
        "skills/workflow/consult.md",
        ("Select exactly one mode", "Never modify production code"),
    )
    check_contract(
        root,
        "commands/test.md",
        ("workflow/test.md", "Do not reclassify", "production behavior"),
    )
    check_contract(
        root,
        "skills/workflow/test.md",
        ("OOPFORGE_TEST_ROUTING_PROBE", "Production code: forbidden", "E2E requires"),
    )
    check_contract(
        root,
        "skills/SKILL.md",
        ("/oopforge:test", "Use OOPforge test:", "workflow/test.md"),
    )


def main() -> None:
    root = pathlib.Path(sys.argv[1]).resolve()
    check_manifests(root)
    check_stability(root)
    check_required_paths(root)
    check_activation_probes(root)
    check_contracts(root)
    print("PASS static harness packaging")


if __name__ == "__main__":
    main()
