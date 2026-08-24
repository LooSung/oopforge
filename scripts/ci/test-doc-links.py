#!/usr/bin/env python3
"""Self-tests for check-doc-links.py."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check-doc-links.py")
SPEC = importlib.util.spec_from_file_location("check_doc_links", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class DocLinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_existing_file_and_anchor_pass(self) -> None:
        self.write("guide.md", "# Fixed Task\n")
        source = self.write("README.md", "[task](guide.md#fixed-task)\n")
        self.assertEqual([], MODULE.check_file(self.root, source))

    def test_missing_file_fails(self) -> None:
        source = self.write("README.md", "[missing](docs/missing.md)\n")
        findings = MODULE.check_file(self.root, source)
        self.assertEqual("missing local target", findings[0].reason)

    def test_missing_anchor_fails(self) -> None:
        self.write("guide.md", "# Existing\n")
        source = self.write("README.md", "[task](guide.md#missing)\n")
        findings = MODULE.check_file(self.root, source)
        self.assertEqual("missing heading anchor", findings[0].reason)

    def test_external_and_fenced_links_are_ignored(self) -> None:
        content = "[web](https://example.com)\n```\n[demo](missing.md)\n```\n"
        source = self.write("README.md", content)
        self.assertEqual([], MODULE.check_file(self.root, source))

    def test_parent_link_inside_repository_passes(self) -> None:
        self.write("README.md", "# Root\n")
        source = self.write("docs/guide.md", "[root](../README.md#root)\n")
        self.assertEqual([], MODULE.check_file(self.root, source))

    def test_repository_markdown_includes_untracked_but_not_ignored(self) -> None:
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        tracked = self.write("tracked.md", "# Tracked\n")
        untracked = self.write("untracked.md", "# Untracked\n")
        ignored = self.write("ignored.md", "# Ignored\n")
        self.write(".gitignore", "ignored.md\n")
        subprocess.run(["git", "add", "tracked.md", ".gitignore"],
                       cwd=self.root, check=True)
        self.assertEqual(
            {tracked, untracked},
            set(MODULE.repository_markdown(self.root)),
        )
        self.assertNotIn(ignored, MODULE.repository_markdown(self.root))


if __name__ == "__main__":
    unittest.main()
