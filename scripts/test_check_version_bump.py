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
from test_update_prompt_index import VALID  # noqa: E402  (shared fixture)

_original_run = subprocess.run


def _isolated_run(cmd, **kwargs):
    kwargs.setdefault("env", GIT_ENV)
    return _original_run(cmd, **kwargs)


def setUpModule():
    cvb.subprocess.run = _isolated_run


def tearDownModule():
    cvb.subprocess.run = _original_run

# One fixture for both suites: the index tests' VALID prompt, with a body
# line this suite edits to simulate content changes.
PROMPT_V1 = (VALID
             .replace("One two three four five.", "Original body text.")
             .replace("version: 1.2.3", "version: 1.0.0"))


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
    # Uses the production git() wrapper (with the module-level env patch) so
    # the tests exercise the same invocation path as the code under test.
    cvb.git(*args, cwd=cwd)


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
        """A second bump on the same updated date must not be rejected."""
        first = (PROMPT_V1.replace("Original body", "Edited once")
                 .replace("version: 1.0.0", "version: 1.0.1"))
        repo = self.make_repo(initial_text=first)
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            first.replace("Edited once", "Edited twice")
            .replace("version: 1.0.1", "version: 1.0.2"),
            encoding="utf-8")  # updated date deliberately unchanged
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_non_kebab_filenames_rejected_by_linter_not_gated(self):
        """Layered defense: is_prompt_path ignores non-kebab names so the
        gate never half-tracks them, and the index linter hard-rejects
        them, so such a file cannot exist with green CI."""
        import update_prompt_index as upi
        self.assertFalse(upi.is_prompt_path("prompts/caf\u00e9-prompt.md"))
        self.assertFalse(upi.is_prompt_path('prompts/a"b.md'))
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "prompts"
            d.mkdir()
            (d / "caf\u00e9-prompt.md").write_text(
                PROMPT_V1.replace("sample-prompt", "caf\u00e9-prompt"),
                encoding="utf-8")
            with self.assertRaises(upi.PromptError):
                upi.collect(d)

    def test_impossible_calendar_date_fails(self):
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(
            PROMPT_V1.replace("Original body", "Edited body")
            .replace("version: 1.0.0", "version: 1.0.1")
            .replace("updated: 2026-08-27", "updated: 2026-31-01"),
            encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("not a valid YYYY-MM-DD date", failures[0])

    def test_new_prompt_at_seed_version_exempt(self):
        repo = self.make_repo()
        (repo / "prompts" / "brand-new.md").write_text(PROMPT_V1.replace(
            "sample-prompt", "brand-new"), encoding="utf-8")
        self.commit_all(repo)
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_new_prompt_above_seed_version_fails(self):
        """Smuggling a bumped prompt in as a 'new' file is rejected."""
        repo = self.make_repo()
        (repo / "prompts" / "brand-new.md").write_text(
            PROMPT_V1.replace("sample-prompt", "brand-new")
            .replace("version: 1.0.0", "version: 2.3.0"),
            encoding="utf-8")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("start at 1.0.0", failures[0])

    def test_promotion_from_drafts_with_high_version_fails(self):
        """A rename INTO prompts/ is a new prompt: arbitrary versions are
        rejected even when the content is byte-identical."""
        repo = self.make_repo()
        drafts = repo / "prompts" / "drafts"
        drafts.mkdir()
        (drafts / "idea.md").write_text(
            PROMPT_V1.replace("sample-prompt", "idea")
            .replace("version: 1.0.0", "version: 9.9.9"),
            encoding="utf-8")
        run_git(repo, "checkout", "-q", "main")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "draft on main")
        run_git(repo, "checkout", "-q", "feature")
        run_git(repo, "merge", "-q", "main")
        run_git(repo, "mv", "prompts/drafts/idea.md", "prompts/idea.md")
        self.commit_all(repo)
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("start at 1.0.0", failures[0])

    def test_restored_prompt_keeps_historical_version(self):
        """Re-adding a previously deleted prompt keeps its earned version."""
        repo = self.make_repo()
        old = (PROMPT_V1.replace("sample-prompt", "veteran")
               .replace("version: 1.0.0", "version: 3.2.0"))
        run_git(repo, "checkout", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(old, encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "add veteran")
        run_git(repo, "rm", "-q", "prompts/veteran.md")
        run_git(repo, "commit", "-qm", "delete veteran")
        run_git(repo, "checkout", "-q", "feature")
        run_git(repo, "merge", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(old, encoding="utf-8")
        self.commit_all(repo, "restore veteran")
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_typechange_to_symlink_fails(self):
        """Replacing a prompt with a symlink must not slip past the gate."""
        repo = self.make_repo()
        target = repo / "prompts" / "other-content.txt"
        target.write_text("different content entirely", encoding="utf-8")
        p = repo / "prompts" / "sample-prompt.md"
        p.unlink()
        p.symlink_to("other-content.txt")
        self.commit_all(repo, "swap for symlink")
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("front matter unreadable", failures[0])

    def test_restore_after_merge_delete_uses_true_last_version(self):
        """History simplification around a merge must not hand the hatch a
        stale blob: the prompt earned 2.0.0 on a merged branch, was deleted
        through a merge, and a bumpless re-add of new content must fail
        against 2.0.0, not pass against the stale 1.0.0 side."""
        repo = self.make_repo()
        run_git(repo, "checkout", "-q", "main")
        # bump branch: prompt reaches 2.0.0 and merges to main
        run_git(repo, "checkout", "-qb", "bump")
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1.replace("version: 1.0.0", "version: 2.0.0")
                     .replace("Original body", "Big rewrite"), encoding="utf-8")
        self.commit_all(repo, "bump to 2.0.0")
        run_git(repo, "checkout", "-q", "main")
        run_git(repo, "merge", "-q", "--no-ff", "bump")
        # delete branch: branched BEFORE the bump, deletes the prompt
        run_git(repo, "checkout", "-qb", "deleter", "main~1")
        run_git(repo, "rm", "-q", "prompts/sample-prompt.md")
        self.commit_all(repo, "delete prompt")
        run_git(repo, "checkout", "-q", "main")
        # modify/delete conflict is deterministic: the merge MUST stop
        merge = subprocess.run(["git", "merge", "--no-ff", "deleter"],
                               cwd=repo, capture_output=True, env=GIT_ENV)
        self.assertNotEqual(merge.returncode, 0, "expected modify/delete conflict")
        run_git(repo, "rm", "-q", "prompts/sample-prompt.md")
        run_git(repo, "commit", "-qm", "merge deleter, resolve as delete")
        # feature: re-add with new content at a version below the earned 2.0.0
        run_git(repo, "checkout", "-qB", "feature", "main")
        p.parent.mkdir(exist_ok=True)  # dir vanished with its last file
        p.write_text(PROMPT_V1.replace("version: 1.0.0", "version: 1.0.1")
                     .replace("Original body", "Fresh content"), encoding="utf-8")
        self.commit_all(repo, "re-add low")
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("did not increase", failures[0])

    def _symlink_base(self, initial_text):
        repo = self.make_repo(initial_text=initial_text)
        run_git(repo, "checkout", "-q", "main")
        p = repo / "prompts" / "sample-prompt.md"
        (repo / "prompts" / "target.txt").write_text("payload", encoding="utf-8")
        p.unlink()
        p.symlink_to("target.txt")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "symlink base")
        run_git(repo, "checkout", "-qB", "feature", "main")
        return repo, p

    def test_symlink_swap_judged_against_history(self):
        """Base is a symlink blob: the swapped-in file is judged against
        the path's real versioned history, so a downgrade fails."""
        repo, p = self._symlink_base(PROMPT_V1)  # history holds 1.0.0
        p.unlink()
        p.write_text(PROMPT_V1.replace("version: 1.0.0", "version: 0.5.0"),
                     encoding="utf-8")
        self.commit_all(repo, "swap in downgraded file")
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("did not increase", failures[0])

    def test_symlink_swap_without_history_requires_seed(self):
        """No versioned history behind the symlink: the seed rule applies,
        so an arbitrary high version cannot enter."""
        repo, p = self._symlink_base("# bare file, no front matter\n")
        p.unlink()
        p.write_text(PROMPT_V1.replace("version: 1.0.0", "version: 7.7.7"),
                     encoding="utf-8")
        self.commit_all(repo, "swap at arbitrary version")
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("introduce front matter at", failures[0])

    def test_emoji_blobs_parse_exactly(self):
        """cat-file sizes are BYTES; multi-byte content must not corrupt
        record boundaries or exact-restore matching."""
        emoji = PROMPT_V1.replace("Original body text.",
                                  "Body with emoji \U0001f9ea\U0001f512\U0001f680.")
        repo = self.make_repo(initial_text=emoji)
        run_git(repo, "checkout", "-q", "main")
        p = repo / "prompts" / "sample-prompt.md"
        second = emoji.replace("version: 1.0.0", "version: 1.1.0").replace(
            "emoji", "more emoji \U0001f3af")
        p.write_text(second, encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "second emoji version")
        blobs = cvb.historical_blobs("main", "prompts/sample-prompt.md", cwd=repo)
        self.assertEqual(len(blobs), 2)
        self.assertIn(emoji, blobs)
        self.assertIn(second, blobs)

    def test_restore_of_any_exact_historical_state_passes(self):
        """Restoring an OLDER exact blob (not just the newest) is legal."""
        repo = self.make_repo()
        run_git(repo, "checkout", "-q", "main")
        p = repo / "prompts" / "sample-prompt.md"
        v1 = p.read_text(encoding="utf-8")
        p.write_text(v1.replace("version: 1.0.0", "version: 2.0.0")
                     .replace("Original body", "Newer body"), encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "bump to 2.0.0")
        run_git(repo, "rm", "-q", "prompts/sample-prompt.md")
        run_git(repo, "commit", "-qm", "delete")
        run_git(repo, "checkout", "-qB", "feature", "main")
        p.parent.mkdir(exist_ok=True)
        p.write_text(v1, encoding="utf-8")  # exact ORIGINAL 1.0.0 state
        self.commit_all(repo, "restore original state")
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_shallow_clone_warns(self):
        import contextlib, io
        repo = self.make_repo()
        clone = Path(str(repo) + "-shallow")
        subprocess.run(["git", "clone", "-q", "--depth", "1",
                        f"file://{repo}", str(clone)], check=True,
                       capture_output=True, env=GIT_ENV)
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(clone)]))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                cvb.check("HEAD", cwd=clone)
            except cvb.SkipCheck:
                pass
        self.assertIn("shallow clone", out.getvalue())

    def test_unusable_base_skips(self):
        repo = self.make_repo()
        with self.assertRaises(cvb.SkipCheck):
            cvb.check("refs/heads/does-not-exist", cwd=repo)
        with self.assertRaises(cvb.SkipCheck):
            cvb.check("0" * 40, cwd=repo)

    def test_invalid_head_is_hard_error_not_skip(self):
        """rc 128 from merge-base must propagate, never read as a skip."""
        repo = self.make_repo()
        with self.assertRaises(subprocess.CalledProcessError):
            cvb.check("main", "refs/heads/does-not-exist", cwd=repo)

    def test_restore_with_changed_content_same_version_fails(self):
        """Delete then re-add with edits must still require a bump."""
        repo = self.make_repo()
        old = (PROMPT_V1.replace("sample-prompt", "veteran")
               .replace("version: 1.0.0", "version: 3.2.0"))
        run_git(repo, "checkout", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(old, encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "add veteran")
        run_git(repo, "rm", "-q", "prompts/veteran.md")
        run_git(repo, "commit", "-qm", "delete veteran")
        run_git(repo, "checkout", "-q", "feature")
        run_git(repo, "merge", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(
            old.replace("Original body", "Rewritten body"), encoding="utf-8")
        self.commit_all(repo, "re-add veteran, edited, no bump")
        failures = cvb.check("main", cwd=repo)
        self.assertEqual(len(failures), 1)
        self.assertIn("did not increase", failures[0])

    def test_restore_with_changed_content_and_bump_passes(self):
        repo = self.make_repo()
        old = (PROMPT_V1.replace("sample-prompt", "veteran")
               .replace("version: 1.0.0", "version: 3.2.0"))
        run_git(repo, "checkout", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(old, encoding="utf-8")
        run_git(repo, "add", "-A")
        run_git(repo, "commit", "-qm", "add veteran")
        run_git(repo, "rm", "-q", "prompts/veteran.md")
        run_git(repo, "commit", "-qm", "delete veteran")
        run_git(repo, "checkout", "-q", "feature")
        run_git(repo, "merge", "-q", "main")
        (repo / "prompts" / "veteran.md").write_text(
            old.replace("Original body", "Rewritten body")
            .replace("version: 3.2.0", "version: 3.2.1"), encoding="utf-8")
        self.commit_all(repo, "re-add veteran, edited and bumped")
        self.assertEqual(cvb.check("main", cwd=repo), [])

    def test_require_base_turns_skip_into_error(self):
        repo = self.make_repo()
        import contextlib, io, os
        cwd = os.getcwd()
        os.chdir(repo)
        try:
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = cvb.main(["--require-base", "refs/heads/nope"])
        finally:
            os.chdir(cwd)
        self.assertEqual(code, 2)
        self.assertIn("base is required but unusable", err.getvalue())

    def test_empty_base_arg_is_usage_error(self):
        import contextlib, io
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = cvb.main([""])
        self.assertEqual(code, 2)
        self.assertIn("usage:", err.getvalue())

    def test_unrelated_histories_skip(self):
        repo = self.make_repo()
        run_git(repo, "checkout", "-q", "--orphan", "island")
        run_git(repo, "commit", "-qm", "orphan root")
        with self.assertRaises(cvb.SkipCheck):
            cvb.check("main", "island", cwd=repo)

    def test_head_ref_gates_the_named_ref_not_the_checkout(self):
        """With an explicit head ref, the gate inspects that ref even when
        a different (clean) branch is checked out."""
        repo = self.make_repo()
        p = repo / "prompts" / "sample-prompt.md"
        p.write_text(PROMPT_V1.replace("Original body", "Edited body"),
                     encoding="utf-8")
        self.commit_all(repo)  # violation lives on 'feature'
        run_git(repo, "checkout", "-q", "main")  # clean checkout
        self.assertEqual(cvb.check("main", "main", cwd=repo), [])
        failures = cvb.check("main", "feature", cwd=repo)
        self.assertEqual(len(failures), 1)


if __name__ == "__main__":
    unittest.main()
