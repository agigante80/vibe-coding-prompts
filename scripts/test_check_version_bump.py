#!/usr/bin/env python3
"""Tests for check_version_bump.py against real temporary git repositories.

Run: python3 -m unittest discover -s scripts -p "test_*.py"
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_version_bump as cvb  # noqa: E402

_original_run = subprocess.run


def _isolated_run(cmd, **kwargs):
    kwargs.setdefault("env", GIT_ENV)
    return _original_run(cmd, **kwargs)


def setUpModule():
    cvb.subprocess.run = _isolated_run


def tearDownModule():
    cvb.subprocess.run = _original_run

PROMPT_V1 = """---
name: sample-prompt
category: testing
version: 1.0.0
updated: 2026-08-27
description: A sample prompt.
platforms: [claude]
---

# Sample Prompt

Original body text.
"""


GIT_ENV = {
    **os.environ,
    # Isolate from the developer's global/system git config (gpgsign,
    # hooksPath, templates) so the fixtures behave identically everywhere.
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
}


def run_git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                   env=GIT_ENV)


class CheckVersionBumpTests(unittest.TestCase):
    def make_repo(self, initial_text=PROMPT_V1):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name)
        run_git(repo, "init", "-q", "-b", "main")
        run_git(repo, "config", "user.email", "t@example.com")
        run_git(repo, "config", "user.name", "t")
        (repo / "prompts").mkdir()
        (repo / "prompts" / "sample-prompt.md").write_text(initial_text, encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "base")
        run_git(repo, "checkout", "-qb", "feature")
        return repo

    def commit_all(self, repo, msg="change"):
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", msg)

    def test_edit_without_bump_fails(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1.replace("Original body", "Edited body"), encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("version did not increase", failures[0])

    def test_edit_with_bump_passes(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            PROMPT_V1.replace("Original body", "Edited body")
            .replace("version: 1.0.0", "version: 1.0.1"),
            encoding="utf-8")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_body_version_line_does_not_satisfy_gate(self):
        """A 'version:' line inside the body must not count as a bump."""
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1 + "\nversion: 2\n", encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)

    def test_pure_rename_passes(self):
        repo = self.make_repo()
        run_git(repo, "mv", "prompts/sample-prompt.md", "prompts/renamed-prompt.md")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_rename_with_edit_without_bump_fails(self):
        repo = self.make_repo()
        run_git(repo, "mv", "prompts/sample-prompt.md", "prompts/renamed-prompt.md")
        p = repo / "prompts" / "renamed-prompt.md"
        p.write_text(PROMPT_V1.replace("Original body", "Edited body"), encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("renamed-prompt.md", failures[0])

    def test_version_line_deleted_fails(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1.replace("version: 1.0.0\n", ""), encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("is not MAJOR.MINOR.PATCH", failures[0])

    def test_front_matter_introduced_passes(self):
        """Seeding front matter onto a bare prompt counts as the initial version."""
        repo = self.make_repo(initial_text="# Bare prompt\n\nNo front matter yet.\n")
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1, encoding="utf-8")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_downgrade_fails(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            PROMPT_V1.replace("Original body", "Edited body")
            .replace("version: 1.0.0", "version: 0.9.0"),
            encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("did not increase", failures[0])

    def test_updated_going_backwards_fails(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            PROMPT_V1.replace("Original body", "Edited body")
            .replace("version: 1.0.0", "version: 1.0.1")
            .replace("updated: 2026-08-27", "updated: 2025-01-01"),
            encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("updated went backwards", failures[0])

    def test_same_day_second_bump_passes(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            PROMPT_V1.replace("Original body", "Edited body")
            .replace("version: 1.0.0", "version: 1.0.1"),
            encoding="utf-8")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_new_prompt_exempt(self):
        repo = self.make_repo()
        (repo / "prompts" / "brand-new.md").write_text(PROMPT_V1.replace(
            "sample-prompt", "brand-new"), encoding="utf-8")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])


if __name__ == "__main__":
    unittest.main()
