#!/usr/bin/env python3
"""Tests for update_prompt_index.py (stdlib unittest, no dependencies).

Run: python3 -m unittest discover -s scripts -p "test_*.py" -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_prompt_index as upi  # noqa: E402

VALID = """---
name: sample-prompt
category: testing
version: 1.2.3
updated: 2026-08-27
description: A sample prompt used by the test suite.
platforms: [chatgpt, claude]
---

# Sample Prompt

One two three four five.
"""


def write_prompt(directory, filename, text):
    path = Path(directory) / filename
    path.write_text(text, encoding="utf-8")
    return path


class ParseFrontMatterTests(unittest.TestCase):
    def test_valid_block_parses_fields_and_body(self):
        fields, body = upi.parse_front_matter(VALID, "sample-prompt.md")
        self.assertEqual(fields["name"], "sample-prompt")
        self.assertEqual(fields["version"], "1.2.3")
        self.assertIn("# Sample Prompt", body)

    def test_missing_front_matter_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.parse_front_matter("# No front matter here\n", "x.md")

    def test_unterminated_block_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.parse_front_matter("---\nname: x\n# never closed\n", "x.md")

    def test_malformed_line_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.parse_front_matter("---\nnot a key value pair\n---\nbody\n", "x.md")


class ValueCleanupTests(unittest.TestCase):
    def test_inline_comment_stripped(self):
        text = "---\nname: x\nversion: 1.0.0                # bump on EVERY content change\n---\nbody"
        fields, _ = upi.parse_front_matter(text, "x.md")
        self.assertEqual(fields["version"], "1.0.0")

    def test_surrounding_quotes_stripped(self):
        text = '---\ndescription: "Logging: structured JSON"\n---\nbody'
        fields, _ = upi.parse_front_matter(text, "x.md")
        self.assertEqual(fields["description"], "Logging: structured JSON")

    def test_space_hash_starts_comment_like_yaml(self):
        # YAML plain scalars treat ' #' as a comment start; the parser matches that.
        text = "---\ndescription: Use plans #see docs\n---\nbody"
        fields, _ = upi.parse_front_matter(text, "x.md")
        self.assertEqual(fields["description"], "Use plans")

    def test_hash_without_preceding_space_kept(self):
        text = "---\ndescription: Ranked as repo#1 by us\n---\nbody"
        fields, _ = upi.parse_front_matter(text, "x.md")
        self.assertEqual(fields["description"], "Ranked as repo#1 by us")

    def test_quoted_value_with_trailing_comment(self):
        text = '---\nversion: "1.0.1" # note\n---\nbody'
        fields, _ = upi.parse_front_matter(text, "x.md")
        self.assertEqual(fields["version"], "1.0.1")

    def test_unterminated_quote_raises(self):
        text = '---\ndescription: "half quoted\n---\nbody'
        with self.assertRaises(upi.PromptError):
            upi.parse_front_matter(text, "x.md")

    def test_utf8_bom_tolerated(self):
        fields, _ = upi.parse_front_matter("\ufeff" + VALID, "x.md")
        self.assertEqual(fields["name"], "sample-prompt")


class ValidateTests(unittest.TestCase):
    def fields(self, **overrides):
        base = dict(
            name="sample-prompt", category="testing", version="1.0.0",
            updated="2026-08-27", description="d", platforms="[chatgpt]",
        )
        base.update(overrides)
        return base

    def test_valid_fields_pass(self):
        upi.validate(self.fields(), "x.md")

    def test_missing_field_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.validate(self.fields(description=""), "x.md")

    def test_bad_version_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.validate(self.fields(version="7"), "x.md")

    def test_bad_date_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.validate(self.fields(updated="27/08/2026"), "x.md")


class CollectTests(unittest.TestCase):
    def test_collect_counts_words_and_sorts(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_prompt(tmp, "sample-prompt.md", VALID)
            second = VALID.replace("sample-prompt", "another-prompt").replace(
                "category: testing", "category: alpha")
            write_prompt(tmp, "another-prompt.md", second)
            entries = upi.collect(Path(tmp))
        self.assertEqual([e["category"] for e in entries], ["alpha", "testing"])
        # body: "# Sample Prompt" (3 words) + "One two three four five." (5 words)
        self.assertEqual(entries[1]["words"], 8)

    def test_name_filename_mismatch_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_prompt(tmp, "wrong-name.md", VALID)
            with self.assertRaises(upi.PromptError):
                upi.collect(Path(tmp))

    def test_empty_directory_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(upi.PromptError):
                upi.collect(Path(tmp))


class InjectTests(unittest.TestCase):
    README = f"intro\n{upi.START}\nold table\n{upi.END}\noutro\n"

    def test_replaces_region_and_preserves_rest(self):
        result = upi.inject(self.README, "NEW TABLE")
        self.assertIn("intro", result)
        self.assertIn("NEW TABLE", result)
        self.assertIn("outro", result)
        self.assertNotIn("old table", result)

    def test_idempotent(self):
        once = upi.inject(self.README, "T")
        twice = upi.inject(once, "T")
        self.assertEqual(once, twice)

    def test_missing_markers_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.inject("no markers here", "T")

    def test_out_of_order_markers_raises(self):
        with self.assertRaises(upi.PromptError):
            upi.inject(f"{upi.END}\n{upi.START}", "T")


class RenderTableTests(unittest.TestCase):
    def test_pipe_in_description_escaped(self):
        entry = dict(name="p", category="c", version="1.0.0", updated="2026-08-27",
                     description="Use Plan | Act mode.", words=1, path="./prompts/p.md")
        table = upi.render_table([entry])
        self.assertIn("Use Plan \\| Act mode.", table)
        # every row still has exactly 6 cells (7 unescaped delimiters)
        row = table.splitlines()[-1]
        self.assertEqual(row.count("|") - row.count("\\|"), 7)

    def test_renders_linked_row(self):
        entry = dict(name="sample-prompt", category="testing", version="1.2.3",
                     updated="2026-08-27", description="Desc.", words=8,
                     path="./prompts/sample-prompt.md")
        table = upi.render_table([entry])
        self.assertIn("[sample-prompt](./prompts/sample-prompt.md)", table)
        self.assertIn("| 1.2.3 |", table)
        self.assertTrue(table.startswith("| Prompt |"))


class EndToEndTests(unittest.TestCase):
    def run_main(self, argv):
        """Run main() against a temp repo layout, returning (code, readme_text)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            prompts = tmp / "prompts"
            prompts.mkdir()
            write_prompt(prompts, "sample-prompt.md", VALID)
            readme = tmp / "README.md"
            readme.write_text(f"# T\n{upi.START}\n{upi.END}\n", encoding="utf-8")
            orig_dir, orig_readme = upi.PROMPTS_DIR, upi.README
            upi.PROMPTS_DIR, upi.README = prompts, readme
            try:
                code = upi.main(argv)
            finally:
                upi.PROMPTS_DIR, upi.README = orig_dir, orig_readme
            return code, readme.read_text(encoding="utf-8")

    def test_write_then_check_passes(self):
        code, text = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("[sample-prompt](./prompts/sample-prompt.md)", text)

    def test_check_fails_on_stale_readme(self):
        code, _ = self.run_main(["--check"])
        self.assertEqual(code, 1)

    def test_unknown_flag_rejected(self):
        code, _ = self.run_main(["--chek"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
