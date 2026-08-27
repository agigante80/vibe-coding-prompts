---
name: github-actions-cicd-generator
category: devops-automation
version: 2.0.0
updated: 2026-08-27
description: Versioning, branching and Docker tagging policy for GitHub Actions pipelines.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# CI/CD GitHub Actions Generator

## Versioning Policy

### VERSION File
- Maintain a `VERSION` file to explicitly indicate the current version of the application. This file should be updated for each release.

### Branch Rules Versioning
1. **Main Branch**: The `main` branch should reflect the latest stable release.
2. **Feature Branches**: Feature branches should follow the naming convention `feature/feature-name` and get merged into `main` only when fully tested.
3. **Release Branches**: Create a release branch from `main` when preparing for a new release, following the naming convention `release/vX.Y.Z`.

### Docker Tagging Policy
- The Docker images should be tagged with the following conventions:
  - `latest` for the images built from the `main` branch.
  - Unprefixed cascading version tags for each release: `:1.5.0`, `:1.5`, `:1`, plus `:latest`. The git tag carries the `v` prefix (`v1.5.0`); Docker tags do not (see the [Version Management](./version-management.md) tag mapping, including the `+` to `-` build-metadata encoding).
- Example for an image named `ORG/PROJECT` releasing git tag `v1.5.0`:
  - `ORG/PROJECT:1.5.0`, `ORG/PROJECT:1.5`, `ORG/PROJECT:1`, `ORG/PROJECT:latest`

## Best Practices
- Ensure that the `VERSION` file is updated in every pull request that introduces version changes.
- Use `docker-compose` to automate testing of different versions in separate environments.
- Integrate CI/CD tests during the merge to `main` branch to ensure the latest features do not break existing functionalities.