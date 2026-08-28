---
name: autonomous-backlog-workflow
category: project-management
version: 1.0.0
updated: 2026-08-28
description: Select, validate, implement, review and close a coherent batch of backlog tickets autonomously, with bounded quality loops.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# Autonomous Backlog Workflow

## **Objective**

Work a ticket backlog autonomously: pick a coherent, high-value batch, validate every ticket against current reality, implement what can be finished without human decisions, test and review it under BOUNDED loops, and leave both the codebase and the backlog better than found.

**Division of authority with [Project Reassessment](./project-reassessment.md)**: that prompt surveys the repository and PRODUCES the prioritized action plan (and the `/docs/` work records); this one CONSUMES a queue and executes it. Run reassessment to decide what should be done; run this to do it, feeding results back into the same `/docs/` records.

**What this costs**: this is a long-session prompt. It assumes a ticket system, an automated test gate, and a code-review capability. It is not a quick-task prompt.

---

## **Assessment Phase**

### 1. **Repository and Backlog Analysis**

* Locate the backlog: the stated ticket system, else `gh issue list`, a tracker config, or a TODO/ROADMAP file in the repo; if none exists, say so and stop rather than inventing work
* Inspect git status, current branch, recent commits, and any uncommitted work; never clobber pre-existing changes, and establish the baseline the final diff will be attributed to
* Read the ENTIRE open backlog: titles, bodies, comments, links
* Detect the project's conventions: test commands, commit style, review tooling, CI gates

### 2. **Batch Selection**

* Target roughly five tickets, but coherence beats count: take fewer when little is actionable, more when tickets share one area, dependency chain, or root cause
* Rank by impact, severity, dependency position, effort-to-value, confidence the problem still exists, and whether it can be COMPLETED autonomously
* Do prerequisites before dependents; skip tickets that hinge on decisions only a human can make (label them for human input and move on)
* State why this batch, and how its tickets relate, before touching code

---

## **Per-Ticket Validation**

**Do not trust the ticket description.** Premises rot: reproduction steps stop reproducing, blockers clear, counts drift, work gets done by other routes. For each selected ticket, verify against current code and history whether the problem still exists, whether it was superseded or partially fixed, and whether it is still worth doing. Then decide autonomously: implement, rewrite, re-scope, split, or close with evidence. A ticket is never implemented merely because it exists.

---

## **Implementation Rules**

* Stay on the ticket's scope; make supporting changes only where correctness or safety requires them
* **When a finding names an instance, sweep for the family before fixing.** The most expensive recurring mistake is correcting the reported instance and leaving its twins (the identical assertion fifty lines up, the same claim in a second document). Report what the sweep covered and how
* Capture genuinely separate discoveries as new tickets immediately, with enough context to be actionable; do not silently expand scope
* Commit and push in logical increments with the project's message conventions; never let the batch live only in a working tree

---

## **Testing**

Follow the project's testing conventions, and hold every new or changed test to the standard of [Prove Your Tests Can Fail](./prove-your-tests-can-fail.md): a test earns its place only once it has been SEEN TO FAIL against a deliberate break. Line coverage is a diagnostic, not the goal; the defects that matter live on lines coverage already reports as covered. Validate behavior at runtime (real invocations, real CI runs) where practical, not only through unit assertions.

---

## **The Bounded Review Loop**

Run the project's code-review capability against the change, then:

* **Round 1**: fix findings at high or medium severity. Everything below becomes a ticket immediately, not a negotiation
* **Round 2**: review ONLY the fix commits; fix highs and mediums as in round 1; the target must not grow each round
* **Round 3+**: only if round 2 found a high; fix highs, ticket the rest. **Hard cap: 4 rounds total**
* **Trip wire**: two consecutive rounds each finding a defect in the previous round's FIX means stop immediately; past that point iteration removes value
* **A ticket is a finished outcome for a finding.** Filing is not failing to fix; without this exit the loop has no honorable end
* Report the stopping reason and how many rounds found defects in prior fixes, so continuing is the operator's call, not a default

---

## **Deliverables**

1. Batch rationale: what was selected, why, how the tickets relate
2. Implemented, tested, reviewed and pushed changes for every completed ticket
3. Updated tickets: each closed with what actually shipped, or re-scoped/split/labeled with evidence
4. New tickets for every discovery and every unfixed review finding, linked to their origins
5. A final report: per-ticket outcome, tests run, review rounds with the loop's stopping reason, and anything genuinely needing a human
6. Documentation updates in the target project: `/docs/REFACTORING_PLAN.md` (completed tasks marked, new ones added), `/docs/IMPROVEMENT_AREAS.md` (debt cleared or newly found), and `/docs/ROADMAP.md` when a batch moves a milestone

---

## **Success Criteria**

- [ ] Every selected ticket validated against current reality before work
- [ ] Every family sweep reported alongside its instance fix
- [ ] New and changed tests seen red at least once
- [ ] Review loop terminated by a round with no highs or mediums, the 4-round cap, or the trip wire, with the reason reported
- [ ] Backlog reflects reality: no closed-but-undone or done-but-open tickets
- [ ] `/docs/` work records updated so the tracker and the docs agree
- [ ] All work committed and pushed; final diff attributable to the batch

---

## **Usage Instructions**

**When to run**: recurring backlog-burning sessions, overnight autonomous work, or clearing the queue before a milestone.

**Execution**:
```
Work my backlog autonomously.
Ticket system: [GitHub Issues/Jira/etc.]
Test gate: [command]
Review capability: [tool/skill name]
Batch size guidance: [default ~5 / your preference]
Out of bounds: [tickets or areas to leave alone]
```

**Expected outcome**: a coherent batch implemented and closed, discoveries and residual findings filed, quality loops bounded and reported honestly, and a backlog that matches the repository's true state.
