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
from update_prompt_index import (  # noqa: E402
    VERSION_RE, PromptError, parse_front_matter, valid_date,
)


def semver_tuple(version):
    return tuple(int(part) for part in version.split("."))


def git(*args, cwd=None):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True, cwd=cwd
    ).stdout


def changed_prompts(base_commit, cwd=None):
    """Return (old_path, new_path) pairs for modified or renamed prompts."""
    # A 25% similarity threshold pairs even heavy rewrites as renames so they
    # stay inside the gate. A rewrite below that is indistinguishable from a
    # delete plus a new prompt and is treated as one (new prompts are exempt;
    # update_prompt_index.py --check still validates their front matter).
    # core.quotepath=off keeps non-ASCII paths literal instead of quoted
    # octal escapes, which would silently fail the prompts/ prefix match.
    out = git("-c", "core.quotepath=off", "diff", "--name-status",
              "--find-renames=25%", f"{base_commit}..HEAD", cwd=cwd)
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


def front_matter_of(text, source):
    fields, _ = parse_front_matter(text, source)
    return fields.get("version", ""), fields.get("updated", "")


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
