<!-- Memory index. Each line: - [Title](file.md) - one-line description (~150 chars max) -->
<!-- Add entries here as Claude Code builds up project memory across conversations. -->

- [Prompt versioning and generated index](prompt-versioning-system.md) - Three-layer versioning: front matter, generated index, CI bump gate; bumps are per PR.
- [1600-word cap on prompt bodies](prompt-word-cap-policy.md) - Every prompt body stays under 1600 words; compress in the same edit that adds content.
- [Bounded code-review loop and its evidence](bounded-review-loop-practice.md) - Cap review loops at 4 rounds with a bad-fix trip wire; tickets are finished outcomes.
- [Environment gotchas: gh, dash hook, git output](repo-tooling-gotchas.md) - Snap gh cannot read /tmp, the dash hook scans commands, git pull prints a false error.
- [How the user runs autonomous batches](user-working-style.md) - Owns batches end to end; pre-authorization is durable; tickets are the record; report honestly.
- [Repository references and CI entry points](repo-key-references.md) - Repo URL, index, authoring guide, CI job name, issue labels, and the pending branch-protection item.
