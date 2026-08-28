---
name: user-working-style
description: Owns batches end to end; pre-authorization is durable; tickets are the record; report honestly.
metadata:
  type: user
---

The user runs long autonomous sessions against this repo and expects the agent to own a batch end to end: select, validate, implement, test, review under bounded loops, document, merge, and report honestly.

Preferences demonstrated repeatedly:

- **Pre-authorization is durable within a batch.** Statements like "I won't mind a full rewrite" or "I have no issue moving/renaming/deleting anything" are standing permission for that work; do not re-ask.
- **Tickets are the unit of record.** Every review finding not fixed becomes a GitHub issue with severity, repro and rationale. Every discovery during implementation becomes its own ticket, linked to its origin.
- **Reporting must be honest and specific**: say what was NOT done and why, name the stopping reason for each review loop, and never claim a clean loop that did not happen.
- **Suggestions want pros and cons** with a recommendation, not a survey.
- **Verified sources only.** When citing external guidance, fetch the page and confirm it says what is claimed before linking it.

**Why:** the user built this repo around exactly these practices (the autonomous-backlog-workflow and prove-your-tests-can-fail prompts encode them) and corrected drift away from them.

**How to apply:** end each batch with per-ticket outcomes, tests run, review rounds with stopping reasons, tickets created, and the items only a human can do. Linked: [[bounded-review-loop-practice]].
