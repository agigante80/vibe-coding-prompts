#!/usr/bin/env python3
"""Fail if any prompt changed relative to a base ref without a version bump.

Usage: python3 scripts/check_version_bump.py <base-ref>

Compares the front matter `version` parsed from the base and head git blobs,
so it cannot be fooled by version-like lines in prompt bodies, by renames,
or by deleting the version line (a missing/invalid head version fails).

Rules:
- Modified prompts and renamed-with-edits prompts need a version change.
- Pure renames (identical content) pass.
- Newly added prompts are exempt; front matter validity is enforced by
  update_prompt_index.py --check.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_prompt_index import PromptError, parse_front_matter  # noqa: E402


def git(*args, cwd=None):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True, cwd=cwd
    ).stdout


def changed_prompts(base_commit, cwd=None):
    """Return (old_path, new_path) pairs for modified or renamed prompts."""
    out = git("diff", "--name-status", "--find-renames",
              f"{base_commit}..HEAD", cwd=cwd)
    pairs = []
    for line in out.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status == "M":
            old = new = parts[1]
        elif status.startswith("R"):
            old, new = parts[1], parts[2]
        else:
            continue
        if new.startswith("prompts/") and new.endswith(".md"):
            pairs.append((old, new))
    return pairs


def version_of(text, source):
    fields, _ = parse_front_matter(text, source)
    return fields.get("version", "")


def check(base_ref, cwd=None):
    """Return a list of failure messages (empty means the check passes)."""
    base_commit = git("merge-base", base_ref, "HEAD", cwd=cwd).strip()
    failures = []
    for old, new in changed_prompts(base_commit, cwd=cwd):
        old_text = git("show", f"{base_commit}:{old}", cwd=cwd)
        new_text = git("show", f"HEAD:{new}", cwd=cwd)
        if old_text == new_text:
            continue  # pure rename, no content change
        try:
            new_version = version_of(new_text, new)
        except PromptError as exc:
            failures.append(f"{new}: head front matter unreadable ({exc})")
            continue
        if not new_version:
            failures.append(f"{new}: front matter has no version field")
            continue
        try:
            old_version = version_of(old_text, old)
        except PromptError:
            # Base copy predates front matter; the new version is the seed.
            print(f"ok: {new} (front matter introduced at {new_version})")
            continue
        if old_version == new_version:
            failures.append(
                f"{new}: content changed but version is still {new_version}")
        else:
            print(f"ok: {new} ({old_version} to {new_version})")
    return failures


def main(argv):
    if len(argv) != 1 or argv[0].startswith("-"):
        print("usage: check_version_bump.py <base-ref>", file=sys.stderr)
        return 2
    try:
        failures = check(argv[0])
    except subprocess.CalledProcessError as exc:
        print(f"error: git failed: {exc.stderr.strip()}", file=sys.stderr)
        return 2
    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        print(
            "\nBump the 'version:' field (and 'updated:') in each failing prompt.\n"
            "Rules: docs/prompt-creation-guide.md, section "
            "'Front Matter, Versioning and the README Index'.",
            file=sys.stderr,
        )
        return 1
    print("version bump check: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
