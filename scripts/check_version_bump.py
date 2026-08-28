#!/usr/bin/env python3
"""Fail if any prompt changed relative to a base ref without a version bump.

Usage: python3 scripts/check_version_bump.py <base-ref> [<head-ref>]

head-ref defaults to HEAD; the pre-push hook passes the ref actually being
pushed so the gate inspects the push, not the checkout.

Compares the front matter `version` parsed from the base and head git blobs,
so it cannot be fooled by version-like lines in prompt bodies, by renames,
or by deleting the version line.

Skip semantics (exit 0 with a message, warning-annotated on GitHub Actions):
an unusable base (unknown ref, the all-zero SHA, or histories with no common
ancestor) means there is nothing meaningful to diff. This applies to push
and pre-push contexts where such states are legitimate. The PR gate passes
--require-base, which turns every skip into a hard failure (exit 2): a pull
request ALWAYS has a resolvable base, so an unusable one is a broken gate,
and a broken gate must never pass silently. Real git errors (rc 128:
corrupt objects, invalid head, not a repository) are hard failures in every
mode.

Rules:
- Modified prompts and renamed-with-edits prompts need a strictly
  increasing version; `updated` must be a real date and never go backwards.
- Pure renames between prompt paths (identical content) pass THIS gate,
  but the index check still fails them until the front matter name is
  updated to the new stem, which is a content change requiring a bump; in
  practice every rename ships with a bump.
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
    """Return the merge-base commit, or raise SkipCheck when unusable.

    Only returncode 1 means "the ref/ancestry legitimately does not exist"
    (git rev-parse -q --verify and git merge-base both use it for exactly
    that). Any other failure (128: corrupt object, bad head, not a repo)
    is a real error and must propagate as CalledProcessError, never a skip.
    """
    probe = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"{base_ref}^{{commit}}"],
        capture_output=True, encoding="utf-8", cwd=cwd)
    if probe.returncode == 1:
        raise SkipCheck(f"base {base_ref} is not a usable commit "
                        "(unreachable, zero SHA, or unknown ref)")
    probe.check_returncode()
    merge_base = subprocess.run(
        ["git", "merge-base", base_ref, head],
        capture_output=True, encoding="utf-8", cwd=cwd)
    if merge_base.returncode == 1:
        raise SkipCheck(f"{base_ref} and {head} share no common ancestor")
    merge_base.check_returncode()
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
        if status in ("M", "T"):
            # T (typechange, e.g. file replaced by a symlink) is judged as a
            # modification: the new blob is the link target path, which has
            # no front matter, so the gate fails it rather than skipping.
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


def historical_blobs(base_commit, path, cwd=None):
    """Every content the path had at or before base, newest first.

    One rev-list plus ONE `git cat-file --batch` subprocess regardless of
    how many commits touched the path. cat-file's explicit "missing"
    marker distinguishes absent blobs (skipped) from real git errors
    (which raise), and --full-history plus version-aware consumers defeat
    merge-side history simplification.
    """
    hashes = git("log", "--full-history", "--format=%H",
                 "--diff-filter=ACMR", base_commit, "--", path,
                 cwd=cwd).split()
    if not hashes:
        return []
    batch_input = "".join(f"{h}:{path}\n" for h in hashes).encode()
    # Parse in BYTES: cat-file sizes are byte counts, and prompts contain
    # multi-byte UTF-8 (emoji), so slicing a decoded str by the byte size
    # would swallow separators and corrupt subsequent records.
    proc = subprocess.run(
        ["git", "cat-file", "--batch"], input=batch_input,
        capture_output=True, cwd=cwd)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(
            proc.returncode, proc.args, proc.stdout, proc.stderr)
    blobs, out, pos = [], proc.stdout, 0
    while pos < len(out):
        newline = out.index(b"\n", pos)
        header = out[pos:newline]
        pos = newline + 1
        if header.endswith(b" missing"):
            continue
        size = int(header.rsplit(b" ", 1)[1])
        blobs.append(out[pos:pos + size].decode("utf-8"))
        pos = pos + size + 1  # skip the trailing separator newline
    return blobs


def best_historical(blobs, path):
    """(blob, version) of the highest-versioned historical copy, or
    (None, None) when no blob carries a parseable version."""
    best_blob, best_ver, best_key = None, None, None
    for text in blobs:
        try:
            version, _ = front_matter_of(text, path)
        except PromptError:
            continue
        if not VERSION_RE.match(version):
            continue
        key = semver_tuple(version)
        if best_key is None or key > best_key:
            best_blob, best_ver, best_key = text, version, key
    return best_blob, best_ver


def warn_if_shallow(cwd=None):
    """A shallow clone truncates history walks silently; say so once."""
    git_dir = git("rev-parse", "--git-dir", cwd=cwd).strip()
    shallow = Path(cwd or ".") / git_dir / "shallow"
    if shallow.exists():
        print("warning: shallow clone; historical version checks may be "
              "incomplete here (CI, with full history, is authoritative)")


def check(base_ref, head="HEAD", cwd=None):
    """Return a list of failure messages (empty means the check passes)."""
    warn_if_shallow(cwd=cwd)
    base_commit = resolve_base(base_ref, head, cwd=cwd)
    failures = []
    for old, new in changed_prompts(base_commit, head, cwd=cwd):
        new_text = git("show", f"{head}:{new}", cwd=cwd)
        if old is None:
            # New to prompts/: seed rule, with a bounded restore hatch.
            try:
                version, _ = front_matter_of(new_text, new)
            except PromptError as exc:
                failures.append(f"{new}: head front matter unreadable ({exc})")
                continue
            blobs = historical_blobs(base_commit, new, cwd=cwd)
            if new_text in blobs:
                # Exact restore of ANY prior state keeps that state's version.
                print(f"ok: {new} (restored prompt, unchanged at {version})")
                continue
            hist_blob, hist_ver = best_historical(blobs, new)
            if hist_blob is not None:
                # Changed content on a restored path is judged like a
                # modification against the highest version it ever earned.
                old_text, old_label = hist_blob, f"{new} (historical {hist_ver})"
            elif version == SEED_VERSION:
                print(f"ok: {new} (new prompt at {SEED_VERSION})")
                continue
            else:
                failures.append(
                    f"{new}: new prompt files start at {SEED_VERSION} "
                    f"(found {version}); if this is a rename, keep more "
                    f"similarity or split the rewrite into a separate commit")
                continue
        else:
            old_text = git("show", f"{base_commit}:{old}", cwd=cwd)
            old_label = old
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
            old_version, old_updated = front_matter_of(old_text, old_label)
        except PromptError:
            # Base copy has no readable front matter (pre-migration legacy,
            # or a symlink blob). Do NOT blanket-accept: apply the same
            # rules as a new path, so a swapped-in file cannot carry an
            # arbitrary version through this door.
            blobs = historical_blobs(base_commit, new, cwd=cwd)
            hist_blob, hist_ver = best_historical(blobs, new)
            if hist_blob is not None:
                old_text, old_label = hist_blob, f"{new} (historical {hist_ver})"
                old_version, old_updated = front_matter_of(old_text, old_label)
            elif new_version == SEED_VERSION:
                print(f"ok: {new} (front matter introduced at {SEED_VERSION})")
                continue
            else:
                failures.append(
                    f"{new}: base has no readable front matter and no "
                    f"versioned history; introduce front matter at "
                    f"{SEED_VERSION}, not {new_version}")
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
    require_base = "--require-base" in argv
    positional = [a for a in argv if a != "--require-base"]
    if (len(positional) not in (1, 2)
            or any(a.startswith("-") or not a for a in positional)):
        print("usage: check_version_bump.py [--require-base] "
              "<base-ref> [<head-ref>]", file=sys.stderr)
        return 2
    try:
        failures = check(*positional)
    except SkipCheck as reason:
        if require_base:
            print(f"error: base is required but unusable: {reason}",
                  file=sys.stderr)
            return 2
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
