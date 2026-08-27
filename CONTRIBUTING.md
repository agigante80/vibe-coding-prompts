# Contributing

Thanks for wanting to improve this prompt collection.

## The short version

1. Read the [Prompt Creation Guide](./docs/prompt-creation-guide.md). It defines the required structure, length limits, and quality checklist for every prompt.
2. Add or edit a prompt under [`prompts/`](./prompts/). Every prompt carries YAML front matter (name, category, version, updated, description, platforms).
3. **Bump the `version` field** on any content change and set `updated` to today. Bump rules are in the guide's Versioning section.
4. Regenerate the README index: `python3 scripts/update_prompt_index.py`
5. Open a pull request. CI verifies the front matter, the version bump, and that the README index is fresh; a stale index or missing bump fails the build.

Optional but recommended: `pip install pre-commit && pre-commit install` runs the same checks before every commit, so CI never surprises you.

## Filing issues

Use the issue tracker for defects in prompts (label: `prompt-review`) and for new prompt proposals. Reference the prompt's `name` and `version` so reports are unambiguous.
