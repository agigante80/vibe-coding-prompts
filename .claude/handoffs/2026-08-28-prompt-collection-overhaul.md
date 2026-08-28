# Session handoff: prompt collection overhaul

Date: 2026-08-28

## Summary
A multi-day session that took the repository from a hand-maintained prompt collection with drifting indexes to a versioned, CI-enforced library: twelve critical prompt reviews implemented, the structure flattened, a generated index with a version-bump gate built and hardened, and two new prompts authored. The backlog is now nothing but new-prompt proposals.

## Done this session
- **Structure and docs**: flattened six category directories into `prompts/`, moved the authoring guide to `docs/`, deleted six duplicated category READMEs, rewrote the root README (532 lines to ~75, generated index), added MIT LICENSE and CONTRIBUTING.md. (#16 to #20, #1)
- **Prompt reviews**: filed twelve critical reviews with verified source links, then implemented all of them. Notable fixes: a data-loss `git reset --hard HEAD~1` in an example script, the deprecated and harmful `X-XSS-Protection` recommendation, a Pino sampling example that dropped 95% of all logs, a SemVer format contradiction, and the documentation-standardization redesign (approval gates, declared extensions, Diataxis scoping). (#4 to #15)
- **Versioning system**: YAML front matter on every prompt, `scripts/update_prompt_index.py` generating the README table, `scripts/check_version_bump.py` gating bumps from git blobs, CI workflow, pre-commit config. Hardened across four follow-up tickets. (#18, #19, #20, #24, #25, #27, #31, #46)
- **New prompts**: `autonomous-backlog-workflow` and `prove-your-tests-can-fail`, authored from the user field-tested specs. (#2, #3)
- **Backlog hygiene**: triaged the old README TODO list into twelve `prompt-proposal` issues (#33 to #44) with discard rationale recorded on #23.
- Final state: 14 prompts, all under the 1600-word cap, 81 tests passing, CI green on main, all merged branches deleted. Backlog: 16 open issues (14 `prompt-proposal`, 2 `prompt-review`).

## In progress (where we left off)
Nothing in flight. No open PRs, no branches other than `main`, working tree clean. The last commit of implementation work was 07d7297; the checkpoint commits that follow it carry only these `.claude/memory/` and `.claude/handoffs/` files.

## Next steps
1. Enable **branch protection on `main`** requiring the `verify` check (human-only; until then the push-side gate is advisory).
2. Work the twelve prompt proposals, one per batch. Suggested priority: #34 (API documentation generator) and #35 (code review checklist) for reach, #44 (tutorial and guide creator) to give the collection its first user-facing-docs prompt, filling the gap the Diataxis scope note in documentation-standardization now makes explicit.
3. Each proposal follows the same shape: author per `docs/prompt-creation-guide.md`, front matter at 1.0.0, regenerate the index, bounded review loop, merge.
4. Triage four issues filed by another session while this one ran (not reviewed here): #51 and #52 (`prompt-review`: security-audit-generator names OWASP Top 10:2025 but does not cover it; no SBOM or build provenance anywhere) and #53, #54 (`prompt-proposal`: AI feature security audit for the OWASP LLM Top 10; agent instruction file generator for AGENTS.md). #51 and #52 look like genuine content gaps in a prompt this session already edited, so check them against the current file before assuming they still apply.

## Decisions and why
- **Flat `prompts/` over category directories** (#17 Option A): twelve prompts across six directories meant two files each and six README indexes that all drifted; category now lives in front matter and renders as an index column.
- **Front matter over a comment marker or a central registry** (#18): the table needs descriptions and categories anyway, so one structured block feeds both the version and the index. A central registry was rejected because it reintroduces the forget-to-update failure.
- **CI as the enforcement layer, pre-commit as convenience** (#20): client-side git hooks are not copied on clone, so they can never be the guarantee.
- **Exact restores pass only at the highest earned version** (#31 review): restoring an older state is a net downgrade across pushes.
- **Declared extensions instead of exactly-9 files** (#5): the rigid rule was in a delete-and-recreate loop with two sibling prompts that legitimately produce extra `/docs/` files.
- **Review loops stopped at the trip wire several times** rather than chasing two clean rounds; residual findings were ticketed (#29, #46 and others). Fix commits injected new defects at roughly 20 to 30 percent, so late rounds removed value.

## Open questions / blocked on
- Branch protection (above) is the only blocked item.
- The `platforms` field criteria are not documented anywhere; `autonomous-backlog-workflow` lists all four platforms but the rationale for including or excluding `copilot-chat` on long prompts is unstated.

## Key context to reload
- `CLAUDE.md` and `docs/prompt-creation-guide.md` (conventions, bump rules, required sections).
- `.claude/memory/MEMORY.md` and its six memory files.
- Commands: `python3 -m unittest discover -s scripts -p "test_*.py"`, `python3 scripts/update_prompt_index.py [--check]`, `python3 scripts/check_version_bump.py <base-ref>`.
- Backlog: `gh issue list --label prompt-proposal`.
