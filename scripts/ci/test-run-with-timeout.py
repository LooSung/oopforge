#!/usr/bin/env python3
"""Self-tests for run-with-timeout.py."""

from __future__ import annotations

import subprocess
import sys
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("run-with-timeout.py")


class RunWithTimeoutTests(unittest.TestCase):
    def execute(self, timeout: str, code: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), timeout, sys.executable, "-c", code],
            capture_output=True,
            check=False,
            text=True,
        )

    def test_success_preserves_output(self) -> None:
        result = self.execute("2", "print('done')")
        self.assertEqual(0, result.returncode)
        self.assertEqual("done\n", result.stdout)

    def test_failure_preserves_exit_code(self) -> None:
        result = self.execute("2", "raise SystemExit(7)")
        self.assertEqual(7, result.returncode)

    def test_timeout_returns_124_promptly(self) -> None:
        started = time.monotonic()
        result = self.execute("0.1", "import time; time.sleep(5)")
        self.assertEqual(124, result.returncode)
        self.assertLess(time.monotonic() - started, 2)
        self.assertIn("TIMEOUT after 0.1s", result.stderr)


if __name__ == "__main__":
    unittest.main()
