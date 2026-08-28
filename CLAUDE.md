# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A library of reusable AI "meta-prompts" for software development workflows. The only code is the index tooling in `scripts/`; every other deliverable is a Markdown file. Prompts are platform-agnostic (ChatGPT, Claude, Copilot, Gemini) and auto-detect a target project's stack rather than assuming one.

`docs/prompt-creation-guide.md` is the authoritative authoring standard. Read it before creating or significantly editing any prompt.

## Commands

- Run the test suite: `python3 -m unittest discover -s scripts -p "test_*.py"`
- Regenerate the README prompt index: `python3 scripts/update_prompt_index.py` (`--check` verifies without writing)
- Check version bumps against a base: `python3 scripts/check_version_bump.py <base-ref>`

## Structure

- `prompts/`: all prompt files, flat; the category lives in each file's front matter
- `docs/`: concept docs (vibe coding, meta-prompt system, prompt engineering) plus the prompt creation guide
- `scripts/`: index generator, version-bump gate, and their unittest suites
- `.github/workflows/prompt-index.yml`: CI that runs the tests, the index freshness check, and the bump gate on PRs
- Root `README.md`: short page whose prompt table is GENERATED between the `prompts-index` markers; never hand-edit that region

## Prompt conventions

- Filenames: `kebab-case-descriptive-name.md`, matching the front matter `name`
- Every prompt starts with YAML front matter: `name`, `category`, `version` (SemVer), `updated` (YYYY-MM-DD), `description`, `platforms`
- **Any content change to a prompt requires a version bump** (strictly increasing SemVer; CI compares the PR base to its head, so one bump covers a PR's commits; also enforced on pushes to main) and an `updated` refresh in the same pull request (CI enforces the format and that the date never goes backwards)
- Required sections: **Objective**, **Assessment Phase** (starting with project/stack auto-detection), **Deliverables**, **Success Criteria**. Three legacy prompts predate this rule (github-actions-cicd-generator, version-management, documentation-standardization); their reworks are tracked in #4, #10 and #5
- Length: keep prompts **under ~1600 words** (`wc -w`, minus front matter)
- Prompts must be universal: auto-detect context, provide fallbacks, work across stacks

## When adding or editing a prompt

1. Edit or create the file in `prompts/` with complete front matter (bump `version` on edits)
2. Run `python3 scripts/update_prompt_index.py` to refresh the README table
3. Commit both together; CI fails on a stale index or a missing bump

## The `/docs/` standardization system (in target projects)

Prompts instruct AI agents to maintain a standardized `/docs/` structure in *target* projects: 9 required files plus declared extensions (defined by `prompts/documentation-standardization.md`). This repository itself is exempt: it is a content library, and its own `/docs/` holds concept guides (the README states this explicitly). When writing a prompt, its Deliverables should specify which target-project `/docs/` files the output updates.

Cross-file consistency matters: when changing a convention (the `/docs/` file list, word limits, front matter fields), sweep every prompt and doc that states it.
