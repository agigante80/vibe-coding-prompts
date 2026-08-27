---
name: github-actions-cicd-generator
category: devops-automation
version: 1.0.0
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
  - Version tags (e.g., `v1.0.0`) for tagged releases.
- Example of tagging:
  - For the latest image: `agigante80/vibe-coding-prompts:latest`
  - For a specific release: `agigante80/vibe-coding-prompts:v1.0.0`

## Best Practices
- Ensure that the `VERSION` file is updated in every pull request that introduces version changes.
- Use `docker-compose` to automate testing of different versions in separate environments.
- Integrate CI/CD tests during the merge to `main` branch to ensure the latest features do not break existing functionalities.