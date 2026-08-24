#!/usr/bin/env python3
"""Self-test the proof runner's commit-pinned workspace export."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/proof/run-comparison.sh"
STARTER = "examples/calculator-python-hexagonal"


def git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def check_export(output: Path, commit: str) -> None:
    control = output / "control/workspace"
    treatment = output / "treatment/workspace"
    expected_project = git_output("show", f"{commit}:{STARTER}/pyproject.toml")
    expected_skill = git_output("show", f"{commit}:skills/SKILL.md")
    assert (control / "pyproject.toml").read_bytes() == expected_project
    skill = treatment / ".cursor/skills/oopforge/SKILL.md"
    assert skill.read_bytes() == expected_skill
    assert not (control / ".cursor").exists()
    ignored = {".venv", ".mypy_cache", ".pytest_cache", "__pycache__"}
    assert not any(path.name in ignored for path in control.rglob("*"))


def main() -> None:
    commit = git_output("rev-parse", "HEAD").decode().strip()
    with tempfile.TemporaryDirectory() as temp:
        env = os.environ.copy()
        env.update({
            "PROOF_MODE": "export",
            "PROOF_ALLOW_DIRTY": "1",
            "PROOF_OUTPUT_BASE": temp,
            "PROOF_RUN_ID": "self-test",
        })
        subprocess.run([str(RUNNER)], cwd=ROOT, env=env, check=True)
        output = Path(temp) / "self-test"
        assert (output / "source-commit.txt").read_text().strip() == commit
        check_export(output, commit)
    print("proof runner self-test: PASS")


if __name__ == "__main__":
    main()
