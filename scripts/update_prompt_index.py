#!/usr/bin/env python3
"""Generate the prompt index table in README.md from prompt front matter.

Scans prompts/*.md, parses each file's YAML front matter, and rewrites the
region of README.md between the markers:

    <!-- prompts-index:start -->
    <!-- prompts-index:end -->

Zero third-party dependencies: the front matter grammar used by this repo is
flat `key: value` pairs plus one inline list, parsed here directly.

Usage:
    python3 scripts/update_prompt_index.py            # rewrite README.md
    python3 scripts/update_prompt_index.py --check    # exit 1 if stale
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
README = REPO_ROOT / "README.md"
START = "<!-- prompts-index:start -->"
END = "<!-- prompts-index:end -->"
REQUIRED_FIELDS = ("name", "category", "version", "updated", "description", "platforms")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class PromptError(Exception):
    """A prompt file has missing or malformed front matter."""


def parse_front_matter(text, source):
    """Parse the leading front matter block. Returns (fields, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise PromptError(f"{source}: missing front matter (file must start with ---)")
    try:
        closing = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise PromptError(f"{source}: unterminated front matter block")
    fields = {}
    for raw in lines[1:closing]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise PromptError(f"{source}: malformed front matter line: {raw!r}")
        key, _, value = raw.partition(":")
        fields[key.strip()] = value.strip()
    body = "\n".join(lines[closing + 1:])
    return fields, body


def validate(fields, source):
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    if missing:
        raise PromptError(f"{source}: missing front matter field(s): {', '.join(missing)}")
    if not VERSION_RE.match(fields["version"]):
        raise PromptError(f"{source}: version {fields['version']!r} is not MAJOR.MINOR.PATCH")
    if not DATE_RE.match(fields["updated"]):
        raise PromptError(f"{source}: updated {fields['updated']!r} is not YYYY-MM-DD")


def collect(prompts_dir):
    """Read every prompt file and return sorted table entries."""
    entries = []
    files = sorted(prompts_dir.glob("*.md"))
    if not files:
        raise PromptError(f"no prompt files found in {prompts_dir}")
    for path in files:
        fields, body = parse_front_matter(path.read_text(encoding="utf-8"), path.name)
        validate(fields, path.name)
        if fields["name"] != path.stem:
            raise PromptError(f"{path.name}: front matter name {fields['name']!r} does not match filename")
        entries.append({
            "name": fields["name"],
            "category": fields["category"],
            "version": fields["version"],
            "updated": fields["updated"],
            "description": fields["description"],
            "words": len(body.split()),
            "path": f"./prompts/{path.name}",
        })
    entries.sort(key=lambda e: (e["category"], e["name"]))
    return entries


def render_table(entries):
    rows = [
        "| Prompt | Category | Version | Updated | Words | Description |",
        "|--------|----------|---------|---------|-------|-------------|",
    ]
    for e in entries:
        rows.append(
            f"| [{e['name']}]({e['path']}) | {e['category']} | {e['version']} "
            f"| {e['updated']} | {e['words']} | {e['description']} |"
        )
    return "\n".join(rows)


def inject(readme_text, table):
    """Replace the marker-delimited region with the freshly rendered table."""
    start = readme_text.find(START)
    end = readme_text.find(END)
    if start == -1 or end == -1 or end < start:
        raise PromptError(f"README.md: markers {START} / {END} not found or out of order")
    return readme_text[: start + len(START)] + "\n" + table + "\n" + readme_text[end:]


def main(argv):
    check = "--check" in argv
    try:
        entries = collect(PROMPTS_DIR)
        current = README.read_text(encoding="utf-8")
        updated = inject(current, render_table(entries))
    except (PromptError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if updated == current:
        print(f"prompt index: up to date ({len(entries)} prompts)")
        return 0
    if check:
        print(
            "error: README.md prompt index is stale.\n"
            "Run: python3 scripts/update_prompt_index.py",
            file=sys.stderr,
        )
        return 1
    README.write_text(updated, encoding="utf-8")
    print(f"prompt index: rewritten ({len(entries)} prompts)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
