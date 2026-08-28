---
name: prove-your-tests-can-fail
category: development-workflow
version: 1.0.0
updated: 2026-08-28
description: Verify that tests can actually fail, catching assertions that pass no matter what the code does.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# Prove Your Tests Can Fail

## **Objective**

Audit a test suite for assertions that cannot fail, then fix or remove them. Line coverage reports such tests as covering their targets; they are decoration, not evidence. This prompt complements the [Test Suite Generator](./test-suite-generator.md): that one writes tests, this one checks the tests are worth having.

---

## **The Rule**

A test is worth having only once it has been SEEN TO FAIL. Break the behavior it claims to pin, run the test against the broken copy, watch it go red, then restore. A test never seen red proves nothing about the code.

---

## **Assessment Phase**

### 1. **Project Analysis**

* Detect the test framework and how tests are invoked (from manifests and CI config)
* Locate the assertions most likely to be vacuous: substring checks on messages, boolean conditions over fixtures, tests whose names promise more than their body checks
* Check whether a mutation-testing tool exists for the stack (mutmut/cosmic-ray for Python, Stryker for JS/TS/C#, PIT for Java, cargo-mutants for Rust) and whether the project already configures one

### 2. **The Recognizable Shapes**

Sweep for these mechanical patterns; each is a real failure class:

1. **The needle is in the haystack's own prose.** A substring assertion satisfied by the message's boilerplate rather than its data (asserting `"files" in line` when `files` is a literal in the format string). Assert the rendered VALUE, not a word inside a sentence.
2. **The fixture cannot reach the branch.** A more general guard refuses the input first, so the specific branch under test never runs and the case passes for the wrong reason.
3. **Only one side of a rule is exercised.** Every fixture agrees with both arms of a condition, so `and` and `or` are indistinguishable. Add an input where the arms disagree.
4. **A crash standing in for a failure.** The suite dies before printing a tally, which reads exactly like the check catching something. Assert on the recorded outcome, not on the absence of output.
5. **The mutation is delivered to nothing.** The broken copy was never the one executed (wrong file, wrong variable, stale build). A green run then means "never ran", not "harmless".

---

## **The Manual Method** (no tooling required)

For each assertion you doubt:

1. Name the code change that OUGHT to break it (flip the operator, hardcode the return, swap the message's value)
2. Make that change in the code the test suite ACTUALLY EXECUTES (working tree, not a copy the runner never imports: see shape 5)
3. Run the test; record red or green beside the test
4. Restore the code (`git checkout -- <file>`), and re-run to confirm green again

If it stays green, the test is not testing what its name says: rewrite the assertion, add the missing fixture, or delete the test with a note.

---

## **When to Reach for Tooling**

Use the stack's mutation tool for breadth once the manual method has fixed the known shapes. Two hard-won requirements for any tool run:

* **Kill the process GROUP on timeout and reap it**: a mutant with an infinite loop otherwise leaks processes that pin CPU long after the run moves on
* **Verify delivery**: know exactly how the project points a test run at the mutated copy; if the mutation reaches nothing, every mutant looks killed

**Expect triage, not a defect list.** Some survivors are equivalent mutants that change nothing observable; some are covered by a sibling suite. Classify each survivor: real gap (fix the test), equivalent (record and skip), out of scope (note where it IS covered).

---

## **Deliverables**

1. **Vacuous-assertion report**: each suspect test, the shape it matches, the mutation tried, red or green
2. **Fixed tests** with assertions that bind to values and branches, each seen red before restore
3. **Mutation tool configuration** (if the stack has one): timeout with group kill, delivery verified, survivor triage recorded
4. **Documentation updates**: `/docs/TESTING_AND_RELIABILITY.md` gains the seen-to-fail rule and the survivor triage log

---

## **Success Criteria**

- [ ] Every fixed or new assertion has been observed red against a deliberate break
- [ ] No substring assertion satisfied by message boilerplate remains
- [ ] Both arms of every audited rule are exercised by at least one disagreeing fixture
- [ ] Mutation survivors (if a tool ran) are triaged: real, equivalent, or covered elsewhere
- [ ] `/docs/TESTING_AND_RELIABILITY.md` updated

---

## **Usage Instructions**

**When to run**: after generating or inheriting a test suite, after a bug shipped through green tests, before trusting coverage numbers in a quality gate, or as the verification step of a review loop.

**Execution**:
```
Audit my tests for assertions that cannot fail.
Test command: [how the suite runs]
Focus: [whole suite / specific module / tests added since ref X]
Mutation tooling: [available/none/unknown]
```

**Expected outcome**: a report of vacuous assertions with their shapes, fixed tests each seen red once, and (where tooling exists) a triaged mutation run wired into the project's practices.
