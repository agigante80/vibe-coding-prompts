# Vibe Coding Prompts

A curated collection of reusable, versioned AI meta-prompts for software development workflows: documentation, testing, CI/CD, security, refactoring, and operations.

Each prompt is a self-contained Markdown file you paste into your AI assistant (Claude, ChatGPT, Gemini, or Copilot Chat). Prompts auto-detect your project's stack instead of assuming one, so the same prompt works across languages and frameworks.

## Quick start

1. Pick a prompt from the index below and open it.
2. Copy the prompt body (everything below the front matter) into your AI assistant, inside your project's context.
3. Answer the prompt's short intake questions (project type, stack, constraints).
4. Review everything the AI produces before committing it.

Each prompt's front matter carries a `version` and `updated` date, so you can tell at a glance whether the copy you saved earlier is still current.

## Prompt index

This table is generated from each prompt's front matter by `scripts/update_prompt_index.py` and verified in CI. Do not edit it by hand.

<!-- prompts-index:start -->
| Prompt | Category | Version | Updated | Words | Description |
|--------|----------|---------|---------|-------|-------------|
| [code-refactoring-plan](./prompts/code-refactoring-plan.md) | development-workflow | 1.1.0 | 2026-08-28 | 1594 | Analyze code smells and technical debt, producing a prioritized refactoring roadmap. |
| [file-organization-refactoring](./prompts/file-organization-refactoring.md) | development-workflow | 1.1.1 | 2026-08-28 | 1601 | Reorganize project files and folders safely with tested, incremental migrations. |
| [test-suite-generator](./prompts/test-suite-generator.md) | development-workflow | 1.1.0 | 2026-08-28 | 1586 | Generate a comprehensive test suite with unit, integration and e2e coverage, plus skipped-test cleanup. |
| [version-management](./prompts/version-management.md) | development-workflow | 1.1.0 | 2026-08-27 | 1008 | Semantic versioning strategy with a VERSION file, conventional commits and automated releases. |
| [github-actions-cicd-generator](./prompts/github-actions-cicd-generator.md) | devops-automation | 2.0.0 | 2026-08-27 | 219 | Versioning, branching and Docker tagging policy for GitHub Actions pipelines. |
| [documentation-standardization](./prompts/documentation-standardization.md) | documentation | 1.0.0 | 2026-08-27 | 1724 | Standardize project documentation into the 9-file /docs/ structure with auditing and cleanup. |
| [readme-generator](./prompts/readme-generator.md) | documentation | 1.1.0 | 2026-08-27 | 1587 | Generate or update a professional README, preserving images and validating Docker Hub descriptions. |
| [logging-implementation-best-practices](./prompts/logging-implementation-best-practices.md) | operations | 1.1.0 | 2026-08-27 | 1595 | Production logging with structured JSON, PII redaction, rotation, retention and observability. |
| [github-ready-preparation](./prompts/github-ready-preparation.md) | project-management | 1.1.1 | 2026-08-28 | 1597 | Prepare a repository for professional public release on GitHub. |
| [project-reassessment](./prompts/project-reassessment.md) | project-management | 1.1.1 | 2026-08-28 | 1544 | Full repository health check aligning code, documentation and policies. |
| [dependency-update-manager](./prompts/dependency-update-manager.md) | security | 1.1.0 | 2026-08-27 | 1582 | Automate dependency updates with risk classification, testing and rollback. |
| [security-audit-generator](./prompts/security-audit-generator.md) | security | 1.1.1 | 2026-08-28 | 1582 | Comprehensive security audit with OWASP-based checks and prioritized remediation. |
<!-- prompts-index:end -->

## When to run what

| Situation | Suggested order |
|-----------|-----------------|
| Starting a new project | documentation-standardization, file-organization-refactoring, readme-generator, test-suite-generator, github-actions-cicd-generator |
| Inheriting an existing project | project-reassessment, security-audit-generator, dependency-update-manager, code-refactoring-plan |
| Preparing a public release | github-ready-preparation, security-audit-generator, readme-generator, test-suite-generator |
| Security incident response | security-audit-generator, dependency-update-manager, project-reassessment |
| Monthly health check | project-reassessment, security-audit-generator |
| Quarterly maintenance | project-reassessment, code-refactoring-plan, file-organization-refactoring, documentation-standardization |
| Weekly upkeep | dependency-update-manager |

When a scenario includes both, run file-organization-refactoring before test-suite-generator: moving files first avoids updating test imports twice.

## Philosophy: vibe coding and meta-prompts

This collection is built around two ideas:

- **Vibe coding**: a conversational, iterative way of programming where you describe intent in natural language and refine through feedback. Read more in [What is Vibe Coding?](./docs/vibe-coding.md)
- **Meta-prompts**: prompts that define how to solve a whole category of problems, adapting to any stack, rather than solving one instance. Read more in the [Universal Meta-Prompt System](./docs/universal-meta-level-prompt-system.md).

For prompt-length limits per platform, see the [Prompt Engineering Guide](./docs/prompt-engineering-guide.md).

## A note on this repository's own standards

Several prompts here define standards for target software projects (a 9-file `/docs/` structure, test suites, CI/CD pipelines). This repository itself is a content library, not a software project: its `/docs/` holds concept guides, its tests cover the index tooling in `scripts/`, and the documentation standards its prompts enforce apply to the projects you run them on, not to this repo.

## Contributing

New prompts and improvements are welcome. Start with [CONTRIBUTING.md](./CONTRIBUTING.md) and the [Prompt Creation Guide](./docs/prompt-creation-guide.md), which define the required structure, front matter, versioning rules, and the generated index workflow. Planned prompt ideas are tracked in the [issue tracker](https://github.com/agigante80/vibe-coding-prompts/issues).

## License

Released under the [MIT License](./LICENSE).

## Sponsor

I build and maintain this in my own time. It is free, it stays free, and it gets maintained either way.

If it saved you some time and you feel like saying thanks, you can do that at [github.com/sponsors/agigante80](https://github.com/sponsors/agigante80). Entirely optional, and nothing about the project changes either way.
