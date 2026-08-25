#!/usr/bin/env python3

import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/ci/harness-smoke.sh"


class HarnessSmokeAssertionsTest(unittest.TestCase):
    def run_assertion(self, mode: str, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "probe.txt"
            output.write_text(content)
            return subprocess.run(
                [str(SCRIPT), mode, str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_negative_accepts_exact_token(self) -> None:
        result = self.run_assertion("assert-negative", "OOPFORGE_NOT_LOADED\n")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_negative_accepts_terminal_period(self) -> None:
        result = self.run_assertion("assert-negative", "OOPFORGE_NOT_LOADED.\n")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_negative_rejects_loaded_token(self) -> None:
        result = self.run_assertion(
            "assert-negative", "OOPFORGE_NOT_LOADED.\nOOPFORGE_LOADED\n"
        )
        self.assertNotEqual(0, result.returncode)

    def test_positive_rejects_negative_token_with_period(self) -> None:
        result = self.run_assertion(
            "assert-positive",
            "OOPFORGE_LOADED\nAssumptions\nOOP Contract\nOOPFORGE_NOT_LOADED.\n",
        )
        self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
