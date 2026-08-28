---
name: github-actions-cicd-generator
category: devops-automation
version: 3.0.0
updated: 2026-08-28
description: Generate a complete, security-hardened GitHub Actions pipeline for any stack, with Docker publishing and release automation.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# GitHub Actions CI/CD Generator

## **Objective**

Generate or modernize a complete GitHub Actions CI/CD pipeline for the current project: lint, test, build, container publishing and release automation, with security hardening built in rather than bolted on. Works for any language or stack by detecting the project first.

---

## **Assessment Phase**

### 1. **Project Analysis**

* Detect language and build tooling from manifests: `package.json` (Node), `pyproject.toml`/`requirements.txt` (Python), `go.mod` (Go), `Cargo.toml` (Rust), `pom.xml`/`build.gradle` (Java), `composer.json` (PHP)
* Detect test and lint commands from the manifest scripts or standard conventions
* Detect containerization: `Dockerfile`, `docker-compose.yml`, registry hints in existing configs
* Inventory existing workflows in `.github/workflows/`: modernize in place rather than duplicating; list what each currently does before changing anything
* Detect release signals: `VERSION` file, tags, changelog tooling (see [Version Management](./version-management.md))

### 2. **Pipeline Requirements**

Ask only what cannot be detected: deployment target (registry, cloud, none), environments needing approvals, matrix needs (OS/runtime versions), and whether releases are automated from conventional commits.

---

## **Pipeline Architecture**

Generate parallel, fail-fast jobs with explicit dependencies:

1. **lint** and **test** run in parallel on every push and pull request; test uploads coverage per the [Test Suite Generator](./test-suite-generator.md) conventions
2. **build** runs after both pass; produces the artifact or container image
3. **docker** (when a Dockerfile exists): build once, scan with Trivy (fail on HIGH/CRITICAL), push only on protected refs
4. **release** (tags only): create the GitHub Release, publish artifacts, apply the full Docker tag set

Use dependency caching (`actions/setup-*` built-in caches), `concurrency` groups that cancel superseded PR runs but never audits of pushed refs, and job-level `timeout-minutes`.

---

## **Security Requirements** (non-negotiable)

* **Least-privilege token**: top-level `permissions: contents: read`; escalate per job only for what that job does (e.g. `packages: write` on the publish job)
* **Pin third-party actions to a full commit SHA** with the version as a comment; resolve the SHA at generation time. Tag pinning is mutable and is the primary supply-chain risk GitHub's hardening guide warns about
* **No expression interpolation in `run:` scripts**: pass `github.*` values through `env:` and reference them as shell variables, so a crafted branch name or PR title cannot inject commands
* **OIDC over long-lived secrets** for cloud and registry auth wherever the provider supports it; never echo secrets, never pass them as CLI arguments
* **No `pull_request_target` with checkout of PR code**; if fork PRs need secrets, isolate them behind a labeled approval flow
* Enable Dependabot for `github-actions` ecosystem so pinned SHAs stay fresh

Point users at OpenSSF Scorecard: the generated pipeline should score cleanly on token-permissions, pinned-dependencies and CI-tests checks.

---

## **Versioning and Docker Tagging Policy**

* Maintain a `VERSION` file as the single source of truth, updated by the release flow (details in [Version Management](./version-management.md))
* Branches: `main` is the latest stable state; features come in via `feature/*` PRs; releases cut from tags `vX.Y.Z`
* **Git tags carry the `v` prefix; Docker tags do not.** Each release `vX.Y.Z` publishes the cascade `:X.Y.Z`, `:X.Y`, `:X`
* **`:latest` follows the newest stable release only** (skip the cascade's `:latest` when releasing a patch for an older minor); builds from `main` publish `:edge` instead, so release and branch builds never race over one tag
* Encode SemVer build metadata by replacing `+` with `-` in tags (Docker forbids `+`)

---

## **Workflow Skeleton**

Generate concrete workflows from this shape, filled with the detected commands:

```yaml
name: CI
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
permissions:
  contents: read
concurrency:
  group: ci-${{ github.event_name == 'pull_request' && github.ref || github.run_id }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@<pinned-SHA> # vX.Y.Z
      - uses: actions/setup-<runtime>@<pinned-SHA> # vX.Y.Z, with built-in cache
      - run: <detected lint command>
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<pinned-SHA> # vX.Y.Z
      - uses: actions/setup-<runtime>@<pinned-SHA> # vX.Y.Z
      - run: <detected test command with coverage floor>
  docker:
    needs: [lint, test]
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@<pinned-SHA> # vX.Y.Z
      - run: docker build -t "$IMAGE:$GITHUB_SHA" .
        env: { IMAGE: <registry>/<image> }
      - run: trivy image --severity HIGH,CRITICAL --exit-code 1 "$IMAGE:$GITHUB_SHA"
        env: { IMAGE: <registry>/<image> }
      # push :edge from main, the version cascade from v* tags (policy above)
```

A separate `release.yml` on `v*` tags creates the GitHub Release, publishes artifacts, and applies the tag cascade.

---

## **Deliverables**

1. `.github/workflows/ci.yml` and `release.yml` (or modernized existing workflows), valid and complete for the detected stack
2. Pinned-SHA resolution for every third-party action, with version comments
3. `.github/dependabot.yml` entry for the `github-actions` ecosystem
4. Registry auth wiring (OIDC where supported; documented secrets otherwise)
5. Documentation updates: `/docs/TESTING_AND_RELIABILITY.md` (CI gates), `/docs/ARCHITECTURE.md` (pipeline diagram), README badge

---

## **Success Criteria**

- [ ] Pipeline runs green on the first push for the detected stack (lint, test, build)
- [ ] Every third-party action pinned to a full commit SHA
- [ ] Top-level token is read-only; each escalation is job-scoped and justified
- [ ] No `github.*` expression appears inside a `run:` script
- [ ] Docker images scanned before push; tag policy matches this prompt exactly
- [ ] Release from a `v*` tag produces the GitHub Release plus the tag cascade
- [ ] `/docs/` files updated

---

## **Usage Instructions**

**When to run**: new project without CI, legacy workflows to modernize, adding container publishing or release automation, or after a security review flags workflow risks.

**Execution**:
```
Generate a CI/CD pipeline for this project.
Stack: [auto-detect or state it]
Registry: [GHCR/Docker Hub/none]
Deploy target: [none/cloud/environment names]
Release automation: [conventional commits/manual tags]
```

**Expected outcome**: complete hardened workflows tailored to the detected stack, with versioning and tagging wired per this policy, ready to commit and run.
