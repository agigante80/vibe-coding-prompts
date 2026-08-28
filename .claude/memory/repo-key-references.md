---
name: repo-key-references
description: Repo URL, index, authoring guide, CI job name, issue labels, and the pending branch-protection item.
metadata:
  type: reference
---

Repository: <https://github.com/agigante80/vibe-coding-prompts> (MIT, public).

Key places:
- **Prompt index**: the generated table in the root `README.md`; single source of truth for prompt names, versions and word counts.
- **Authoring standard**: `docs/prompt-creation-guide.md` (front matter contract, bump rules, required sections, generated-index workflow).
- **Agent guidance**: `CLAUDE.md` at the repo root (commands, structure, conventions).
- **CI**: `.github/workflows/prompt-index.yml`, job name `verify`: runs the 81-test suite, the index freshness check, and the version-bump gate.
- **Backlog**: GitHub issues. Label `prompt-proposal` marks new-prompt ideas; `prompt-review` marks critical reviews of existing prompts.

**Outstanding human-only item as of 2026-08-28**: branch protection on `main` requiring the `verify` check is NOT enabled; until it is, the push-side gate is advisory for direct pushes.
