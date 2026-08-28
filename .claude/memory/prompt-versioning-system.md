---
name: prompt-versioning-system
description: "Three-layer versioning: front matter, generated index, CI bump gate; bumps are per PR."
metadata:
  type: project
---

The repository enforces prompt versioning through three cooperating layers, and a change to one usually needs the others swept:

1. **YAML front matter** on every `prompts/*.md` (name, category, version, updated, description, platforms). `version` is SemVer-lite: MAJOR when the output contract changes (users must re-read), MINOR when a capability or check is added, PATCH for wording fixes.
2. **`scripts/update_prompt_index.py`** generates the README table between the `prompts-index` markers and doubles as the metadata linter (kebab filenames, no symlinks, valid dates, quoted-value rules). Never hand-edit that README region.
3. **`scripts/check_version_bump.py`** compares front matter parsed from base and head git BLOBS (never diff text), so body text containing `version:` cannot fool it. CI runs both on PRs and on pushes to main.

The bump rule is per PULL REQUEST, not per commit: the gate diffs the PR base against its head, so one bump covers all of a PR commits touching that prompt.

**Why:** every hand-maintained index in this repo rotted (all twelve word counts in the old README were wrong, by up to 4x). Generation plus CI enforcement is the only thing that held.

**How to apply:** after editing any prompt, bump `version` and `updated`, run `python3 scripts/update_prompt_index.py`, and commit both together. When changing a convention (the /docs/ file set, the word cap, front matter fields), sweep every prompt and doc that restates it. See [[prompt-word-cap-policy]] and [[bounded-review-loop-practice]].
