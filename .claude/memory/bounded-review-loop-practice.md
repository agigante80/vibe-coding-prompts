---
name: bounded-review-loop-practice
description: Cap review loops at 4 rounds with a bad-fix trip wire; tickets are finished outcomes.
metadata:
  type: feedback
---

Code-review loops in this project are bounded, per the user global CLAUDE.md:

- Round 1 reviews the change; fix high and medium findings, ticket the rest.
- Round 2 reviews ONLY the fix commits; the target never grows.
- Round 3+ only if round 2 found a high. **Hard cap: 4 rounds.**
- **Trip wire:** two consecutive rounds each finding a defect in the previous round fix means stop immediately.
- A ticket is a FINISHED OUTCOME for a finding, not a failure to fix it.
- Report the stopping reason and how many rounds found defects in prior fixes.

**Why:** measured across roughly ten loops in this repo, fix commits carried a 20 to 30 percent defect-injection rate under adversarial review. Loops that ran past the trip wire produced churn, not quality. Several genuinely serious bugs (a data-loss `git reset --hard HEAD~1`, a gate that let real edits skip the bump check) were caught in round 1 or 2, so the early rounds pay for themselves and the late ones do not.

**How to apply:** run `/code-review high <branch>` after implementing, fix, then run round 2 scoped to the fix commit only (`/code-review medium <sha> review only this fix commit`). File residuals as tickets with the severity and repro. Two habits that measurably cut injection: assert-guard every scripted text replacement (a silent no-op once shipped a commit claiming a fix it never made), and verify shell or regex changes empirically in a throwaway repo before committing.
