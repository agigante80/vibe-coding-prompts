---
name: repo-tooling-gotchas
description: Snap gh cannot read /tmp, the dash hook scans commands, git pull prints a false error.
metadata:
  type: project
---

Environment quirks in this repo, each confirmed by hitting it:

- **`gh` is snap-packaged**: it cannot read files under `/tmp` or dot-directories in `$HOME`. Pipe issue and PR bodies via stdin instead: `cat body.md | gh issue create --body-file -`.
- **The block-dashes hook** (forge-kit-governance plugin, opted in via `.claude/no-dashes`) scans every Bash command and Write payload for em and en dashes. To search for them, build the bytes with printf escapes rather than typing the characters. Edit tool `old_string` may contain them, since only new content is scanned.
- **`git pull` prints `git: remote-https is not a git command`** here yet still succeeds; verify with `git rev-parse HEAD origin/main` rather than trusting the message.
- **The local version-bump gate reads committed blobs**, so running it before committing shows stale results. CI is the honest layer: it once caught a bump that a silent no-op replacement had never applied.
- **`.private-journal/` writes into the project cwd** and was accidentally committed once; gitignored here now, but check other repos.

**Why:** each produced a confusing failure that looked like a real defect.

**How to apply:** default to the stdin form of `gh`, and verify shell or regex changes in a throwaway repo under the scratchpad before committing. Linked: [[bounded-review-loop-practice]].
