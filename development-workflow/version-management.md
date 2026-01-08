# Version Management & Automated Releases

## Overview

This guide covers semantic versioning concepts, strategies, and best practices for managing software versions. For complete CI/CD workflow implementation including dynamic versioning scripts and automation, see [GitHub Actions CI/CD Generator](../devops-automation/github-actions-cicd-generator.md).

## Purpose

Establish a consistent, automated versioning system that:
- Uses semantic versioning (semver) for stable releases
- Includes build metadata for development builds
- Integrates with GitHub Actions for automatic version bumping
- Supports pre-release tags (alpha, beta, RC)
- Maintains traceability through commit hashes

## When to Use This Prompt

- Setting up a new project's versioning strategy
- Migrating from manual to automated versioning
- Implementing CI/CD pipelines with proper version tagging
- Standardizing version management across multiple projects
- Preparing for production releases with proper versioning

## Version Pattern Specification

### Version Format

Follow semantic versioning: `MAJOR.MINOR.PATCH[-PRERELEASE][-METADATA]`

**Components:**
- **MAJOR**: Breaking changes (increment when incompatible API changes)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)
- **PRERELEASE**: Optional stage identifier (alpha, beta, rc)
- **METADATA**: Build information (commit hash, build number)

### Version Examples by Stage

| Stage | Version Example | Description | Use Case |
|-------|----------------|-------------|----------|
| **Stable Release** | `1.4.0` | Clean semantic version from `main` | Production deployments |
| **Dev Build** | `1.4.1-dev-abcdef7` | Includes commit hash | Feature branch testing |
| **Pre-release (Alpha)** | `1.5.0-alpha.1` | Early testing version | Internal testing |
| **Pre-release (Beta)** | `1.5.0-beta.1` | Feature-complete testing | External beta testers |
| **Release Candidate** | `1.5.0-rc.1` | Final pre-release testing | Pre-production validation |
| **Hotfix** | `1.4.1` | Patch on stable | Critical bug fixes |

## Implementation Strategy

### Phase 1: Version File Setup

#### 1.1 Create VERSION File

Create a `VERSION` file in your project root:

```bash
# Create VERSION file
echo "1.0.0" > VERSION
git add VERSION
git commit -m "chore: initialize version file"
```

**Location:** `/VERSION` (root of repository)

**Format:** Plain text, single line, semantic version number

**Example:**
```
1.4.0
```

#### 1.2 Create .versionrc Configuration

For projects using `standard-version` or `semantic-release`:

```json
{
  "packageFiles": [
    {
      "filename": "VERSION",
      "type": "plain-text"
    },
    {
      "filename": "package.json",
      "type": "json"
    }
  ],
  "bumpFiles": [
    {
      "filename": "VERSION",
      "type": "plain-text"
    },
    {
      "filename": "package.json",
      "type": "json"
    }
  ],
  "types": [
    {"type": "feat", "section": "Features"},
    {"type": "fix", "section": "Bug Fixes"},
    {"type": "chore", "hidden": true},
    {"type": "docs", "hidden": true},
    {"type": "style", "hidden": true},
    {"type": "refactor", "section": "Code Refactoring"},
    {"type": "perf", "section": "Performance Improvements"},
    {"type": "test", "hidden": true}
  ]
}
```

### Phase 2: GitHub Actions Workflows

**For complete CI/CD workflow setup**, run **[GitHub Actions CI/CD Generator](../devops-automation/github-actions-cicd-generator.md)**

**Version-specific workflows needed**:
- **Dev Build** (`.github/workflows/dev-build.yml`): Generate version as `BASE-dev-COMMITHASH`, run tests, upload artifacts
- **Stable Release** (`.github/workflows/release.yml`): On merge to main, bump version with `standard-version` or commit message analysis, create tag, generate CHANGELOG, publish to registry
- **Pre-release** (`.github/workflows/pre-release.yml`): Generate alpha/beta/rc versions, create pre-release tags

Use conventional commits to determine version bump: `fix:` (patch), `feat:` (minor), `BREAKING CHANGE:` (major)

### Phase 3: Version Management Scripts

Add npm scripts in `package.json`:
```json
{
  "scripts": {
    "version:dev": "node scripts/version-dev.js",
    "version:bump": "node scripts/version-bump.js",
    "version:current": "cat VERSION",
    "release:major": "npm run version:bump -- major",
    "release:minor": "npm run version:bump -- minor",
    "release:patch": "npm run version:bump -- patch"
  }
}
```

Create helper scripts in `/scripts/`:
- `version-dev.js`: Read VERSION, append `-dev-COMMITHASH`, update package.json
- `version-bump.js`: Parse VERSION, bump major/minor/patch, write to VERSION and package.json
- `version-check.js`: Verify VERSION and package.json match (exit 1 if mismatch)

## Conventional Commits Integration

Use commit types to trigger bumps:
- `feat:` → MINOR
- `fix:` → PATCH  
- `feat!:` or `BREAKING CHANGE:` → MAJOR

Example: `feat: add CSV export` bumps 1.4.0→1.5.0

## Documentation Requirements

Add to README.md:
- Version badge: `![Version](https://img.shields.io/github/v/release/user/repo)`
- Installation instructions for stable (`@latest`) and dev (`@dev`) versions
- Link to semantic versioning

Create `VERSIONING.md` documenting version format, release process, and automated workflow

## Best Practices

**DO**: Use conventional commits, include commit hashes in dev builds, tag all releases, push tags to GitHub, generate changelogs, test before release, sync VERSION with package.json

**DON'T**: Manually edit versions without updating VERSION, skip pushing tags, release without testing, use `+` in Docker tags (use `-`), forget changelogs

## Troubleshooting

- **Version mismatch**: Run `npm run version:check`, fix VERSION file if needed
- **Failed release**: Check `GITHUB_TOKEN` has `contents: write`, verify commit format, check branch protection
- **Tags not on GitHub**: Ensure workflow uses `git push origin main --follow-tags`

## Deliverables

1. VERSION file in repository root
2. GitHub Actions workflows (dev-build, release, pre-release)
3. Version management scripts in `/scripts`
4. Updated package.json with version scripts
5. VERSIONING.md documentation
6. CHANGELOG.md automatically generated
7. Git tags for all releases (pushed to GitHub)
8. GitHub Releases created with `make_latest: true`
11. **Multi-platform builds** (linux/amd64, linux/arm64)
12. **Multiple Docker tags** per release (`:1.5.0`, `:1.5`, `:1`, `:latest`)

---

**Related Prompts:**
- [GitHub Actions CI/CD Generator](../devops-automation/github-actions-cicd-generator.md) - Complete CI/CD pipeline with dynamic versioning
- [GitHub Ready Preparation](../project-management/github-ready-preparation.md) - Prepare for repository publishing
- [Documentation Creation](./documentation-creation.md) - Generate comprehensive documentation

**Dependencies:**
- Git (with conventional commits)
- Node.js and npm
- GitHub Actions enabled
- Proper branch protection rules

**Estimated Time:** 2-4 hours for initial setup, <5 minutes per release thereafter
