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

import datetime
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


def is_prompt_path(path_str):
    """The single definition of 'a prompt file' shared by all tooling layers.

    Only files directly inside prompts/ count; subdirectories (drafts,
    archives) are ignored by the index, the version gate, and the hooks
    alike, so no layer sees a file another layer misses.
    """
    return bool(re.fullmatch(r"prompts/[^/]+\.md", path_str))


def parse_front_matter(text, source):
    """Parse the leading front matter block. Returns (fields, body)."""
    lines = text.splitlines()
    if lines and lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
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
        value = value.strip()
        if value[:1] in ("'", '"'):
            quote = value[0]
            chars, index, closed = [], 1, False
            while index < len(value):
                char = value[index]
                if char == "\\" and index + 1 < len(value):
                    nxt = value[index + 1]
                    if nxt in (quote, "\\"):
                        # \" is an escaped quote, \\ an escaped backslash;
                        # consuming both keeps a trailing \\" parsing as
                        # literal backslash plus CLOSING quote.
                        chars.append(nxt)
                        index += 2
                        continue
                if char == quote:
                    closed = True
                    break
                chars.append(char)
                index += 1
            if not closed:
                raise PromptError(f"{source}: unterminated quote in line: {raw!r}")
            trailing = value[index + 1:].strip()
            if trailing and not trailing.startswith("#"):
                raise PromptError(
                    f"{source}: content after the closing quote in line: {raw!r}")
            value = "".join(chars)
        else:
            comment = value.find(" #")
            if comment != -1:
                value = value[:comment].rstrip()
        fields[key.strip()] = value
    body = "\n".join(lines[closing + 1:])
    return fields, body


def valid_date(value):
    """True for a real calendar date in YYYY-MM-DD form."""
    if not DATE_RE.match(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate(fields, source):
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    if missing:
        raise PromptError(f"{source}: missing front matter field(s): {', '.join(missing)}")
    if not VERSION_RE.match(fields["version"]):
        raise PromptError(f"{source}: version {fields['version']!r} is not MAJOR.MINOR.PATCH")
    if not valid_date(fields["updated"]):
        raise PromptError(
            f"{source}: updated {fields['updated']!r} is not a valid YYYY-MM-DD date")


def collect(prompts_dir):
    """Read every prompt file and return sorted table entries."""
    entries = []
    files = sorted(
        p for p in prompts_dir.glob("*.md")
        if is_prompt_path(f"prompts/{p.name}"))
    if not files:
        raise PromptError(f"no prompt files found in {prompts_dir}")
    for path in files:
        if path.is_symlink():
            # A symlinked prompt reads fine here but its content then changes
            # via the TARGET file, which the version gate never sees; reject
            # at the linter so one can never enter with green CI.
            raise PromptError(f"{path.name}: prompt files must be regular files, not symlinks")
        fields, body = parse_front_matter(path.read_text(encoding="utf-8-sig"), path.name)
        validate(fields, path.name)
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", path.stem):
            raise PromptError(
                f"{path.name}: prompt filenames must be kebab-case "
                "([a-z0-9-], no spaces or special characters)")
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


def _cell(value):
    """Escape characters that would break a GFM table cell."""
    return str(value).replace("|", "\\|")


def render_table(entries):
    rows = [
        "| Prompt | Category | Version | Updated | Words | Description |",
        "|--------|----------|---------|---------|-------|-------------|",
    ]
    for e in entries:
        rows.append(
            f"| [{_cell(e['name'])}]({e['path']}) | {_cell(e['category'])} "
            f"| {_cell(e['version'])} | {_cell(e['updated'])} | {e['words']} "
            f"| {_cell(e['description'])} |"
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
    unknown = [a for a in argv if a != "--check"]
    if unknown:
        print(f"error: unknown argument(s): {' '.join(unknown)}", file=sys.stderr)
        return 2
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
