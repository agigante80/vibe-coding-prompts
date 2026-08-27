# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A library of reusable AI "meta-prompts" for software development workflows. There is no application code, build system, or test suite; every deliverable is a Markdown file. The prompts are platform-agnostic (ChatGPT, Claude, Copilot, Gemini) and follow a shared structure so they auto-detect a target project's stack rather than assuming one.

`PROMPT_CREATION_GUIDE.md` is the authoritative authoring standard. Read it before creating or significantly editing any prompt.

## Structure

- Category directories, each with its own `README.md` listing its prompts:
  `documentation/`, `devops-automation/`, `development-workflow/`, `project-management/`, `security/`, `operations/`
- `docs/`: concept docs (vibe coding philosophy, meta-prompt system, prompt engineering guide), not prompts
- `.github/REPOSITORY_METADATA.md`: GitHub description and topics
- Root `README.md`: the main index holding the Quick Selection Guide table, workflow/cadence tables, and per-prompt descriptions

## Prompt conventions

- Filenames: `kebab-case-descriptive-name.md`
- Required sections: **Objective**, **Assessment Phase** (starting with project/stack auto-detection), **Deliverables**, **Success Criteria**
- Header hierarchy H1 → H2 → H3; H2 section titles are bolded (`## **Objective**`)
- Length: keep prompts **under ~1600 words** (repo-wide policy from a deliberate trim; the guide's broader 400 to 2000 range is the outer bound). Check with `wc -w <file>`.
- Prompts must be universal: auto-detect context, provide fallbacks when detection fails, work across languages/stacks without modification

## The `/docs/` standardization system

Prompts here instruct AI agents to maintain a standardized 9-file `/docs/` structure in *target* projects (`PROJECT_OVERVIEW.md`, `ARCHITECTURE.md`, `AI_INTERACTION_GUIDE.md`, `REFACTORING_PLAN.md`, `TESTING_AND_RELIABILITY.md`, `IMPROVEMENT_AREAS.md`, `SECURITY_AND_PRIVACY.md`, `ROADMAP.md`, plus `docs/README.md`; `VERSIONING.md` is optional). `documentation/documentation-standardization.md` defines this system. When writing a prompt, its Deliverables should specify which of these `/docs/` files the prompt's output updates; this keeps all prompts consistent with each other.

## When adding or renaming a prompt, update all indexes

A new prompt touches at least four files:

1. The prompt file itself in the right category directory
2. The category's `README.md` ("Available Prompts" entry)
3. Root `README.md`: Quick Selection Guide table, Available Prompts section, and workflow tables if it fits a cadence
4. `PROMPT_CREATION_GUIDE.md` if it changes stated word counts or examples

Cross-file consistency matters: past commits fixed contradictions between prompts and docs, so when changing a convention (e.g. `/docs/` file list, word limits), sweep every prompt that states it.
