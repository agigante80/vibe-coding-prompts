#!/usr/bin/env python3
"""Fail if any prompt changed relative to a base ref without a version bump.

Usage: python3 scripts/check_version_bump.py <base-ref> [<head-ref>]

head-ref defaults to HEAD; the pre-push hook passes the ref actually being
pushed so the gate inspects the push, not the checkout.

Compares the front matter `version` parsed from the base and head git blobs,
so it cannot be fooled by version-like lines in prompt bodies, by renames,
or by deleting the version line.

Skip semantics (exit 0 with a message, warning-annotated on GitHub Actions):
an unusable base (unresolvable ref, the all-zero SHA, or histories with no
common ancestor) means there is nothing meaningful to diff. All other git
errors remain hard failures (exit 2).

Rules:
- Modified prompts and renamed-with-edits prompts need a strictly
  increasing version; `updated` must be a real date and never go backwards.
- Pure renames between prompt paths (identical content) pass.
- A path NEW to prompts/ (added, or renamed in from outside prompts/) must
  carry the seed version 1.0.0 UNLESS the path existed earlier in history
  (restoring a deleted prompt keeps its earned version).
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_prompt_index import (  # noqa: E402
    VERSION_RE, PromptError, is_prompt_path, parse_front_matter, valid_date,
)

SEED_VERSION = "1.0.0"


class SkipCheck(Exception):
    """No usable base to diff against; the check is vacuous, not failed."""


def git(*args, cwd=None):
    # encoding pinned: prompts contain UTF-8 emoji, and text=True alone would
    # use the locale encoding (cp1252 on Windows) and crash on git show output.
    return subprocess.run(
        ["git", *args], check=True, capture_output=True,
        encoding="utf-8", cwd=cwd,
    ).stdout


def semver_tuple(version):
    return tuple(int(part) for part in version.split("."))


def resolve_base(base_ref, head, cwd=None):
    """Return the merge-base commit, or raise SkipCheck when unusable."""
    probe = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"{base_ref}^{{commit}}"],
        capture_output=True, encoding="utf-8", cwd=cwd)
    if probe.returncode != 0:
        raise SkipCheck(f"base {base_ref} is not a usable commit "
                        "(unreachable, zero SHA, or unknown ref)")
    merge_base = subprocess.run(
        ["git", "merge-base", base_ref, head],
        capture_output=True, encoding="utf-8", cwd=cwd)
    if merge_base.returncode != 0:
        raise SkipCheck(f"{base_ref} and {head} share no common ancestor")
    return merge_base.stdout.strip()


def changed_prompts(base_commit, head, cwd=None):
    """Return (old_path, new_path) pairs for changed prompts.

    old_path is None when the path is new to prompts/: a plain add, or a
    rename whose SOURCE was outside prompts/ (e.g. promoted from a drafts
    directory), which must not inherit rename treatment or an arbitrary
    version would enter through that door. A 25% similarity threshold pairs
    even heavy rewrites as renames so they stay inside the gate.
    core.quotepath=off keeps non-ASCII paths literal instead of quoted octal
    escapes, which would silently fail the prompts/ path match.
    """
    out = git("-c", "core.quotepath=off", "diff", "--name-status",
              "--find-renames=25%", f"{base_commit}..{head}", cwd=cwd)
    pairs = []
    for line in out.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status == "M":
            old, new = parts[1], parts[1]
        elif status.startswith("R"):
            old, new = parts[1], parts[2]
            if not is_prompt_path(old):
                old = None  # entering prompts/ counts as a new prompt
        elif status == "A":
            old, new = None, parts[1]
        else:
            continue
        if is_prompt_path(new):
            pairs.append((old, new))
    return pairs


def front_matter_of(text, source):
    fields, _ = parse_front_matter(text, source)
    return fields.get("version", ""), fields.get("updated", "")


def path_has_history(base_commit, path, cwd=None):
    """True when the path existed at or before base (a restore, not new)."""
    out = git("rev-list", "-1", base_commit, "--", path, cwd=cwd)
    return bool(out.strip())


def check(base_ref, head="HEAD", cwd=None):
    """Return a list of failure messages (empty means the check passes)."""
    base_commit = resolve_base(base_ref, head, cwd=cwd)
    failures = []
    for old, new in changed_prompts(base_commit, head, cwd=cwd):
        new_text = git("show", f"{head}:{new}", cwd=cwd)
        if old is None:
            # New to prompts/: seed rule, with a restore escape hatch.
            try:
                version, _ = front_matter_of(new_text, new)
            except PromptError as exc:
                failures.append(f"{new}: head front matter unreadable ({exc})")
                continue
            if version == SEED_VERSION:
                print(f"ok: {new} (new prompt at {SEED_VERSION})")
            elif path_has_history(base_commit, new, cwd=cwd):
                print(f"ok: {new} (restored prompt at {version})")
            else:
                failures.append(
                    f"{new}: new prompt files start at {SEED_VERSION} "
                    f"(found {version}); if this is a rename, keep more "
                    f"similarity or split the rewrite into a separate commit")
            continue
        old_text = git("show", f"{base_commit}:{old}", cwd=cwd)
        if old_text == new_text:
            continue  # pure rename, no content change
        try:
            new_version, new_updated = front_matter_of(new_text, new)
        except PromptError as exc:
            failures.append(f"{new}: head front matter unreadable ({exc})")
            continue
        if not VERSION_RE.match(new_version):
            failures.append(
                f"{new}: version {new_version!r} is not MAJOR.MINOR.PATCH")
            continue
        if not valid_date(new_updated):
            failures.append(
                f"{new}: updated {new_updated!r} is not a valid YYYY-MM-DD date")
            continue
        try:
            old_version, old_updated = front_matter_of(old_text, old)
        except PromptError:
            # Base copy predates front matter; the new version is the seed.
            print(f"ok: {new} (front matter introduced at {new_version})")
            continue
        if not VERSION_RE.match(old_version):
            print(f"ok: {new} (base version unparseable; seeded {new_version})")
            continue
        if semver_tuple(new_version) <= semver_tuple(old_version):
            failures.append(
                f"{new}: content changed but version did not increase "
                f"({old_version} to {new_version})")
        elif valid_date(old_updated) and new_updated < old_updated:
            failures.append(
                f"{new}: updated went backwards ({old_updated} to {new_updated})")
        else:
            print(f"ok: {new} ({old_version} to {new_version})")
    return failures


def main(argv):
    if len(argv) not in (1, 2) or any(a.startswith("-") for a in argv):
        print("usage: check_version_bump.py <base-ref> [<head-ref>]",
              file=sys.stderr)
        return 2
    try:
        failures = check(*argv)
    except SkipCheck as reason:
        message = f"version bump check: skipped ({reason})"
        print(message)
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::warning::{message}")
        return 0
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
