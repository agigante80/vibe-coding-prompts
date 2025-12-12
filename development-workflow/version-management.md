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

**Note:** For production-ready CI/CD workflows with dynamic versioning (`get_version.sh`), see [GitHub Actions CI/CD Generator](../devops-automation/github-actions-cicd-generator.md). The examples below demonstrate basic versioning workflows.

#### 2.1 Development Build Workflow

Create `.github/workflows/dev-build.yml`:

```yaml
name: Development Build

on:
  push:
    branches-ignore:
      - main
      - 'release/**'
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  dev-build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Generate dev version
        id: version
        run: |
          BASE_VERSION=$(cat VERSION)
          COMMIT_HASH=${GITHUB_SHA::7}
          DEV_VERSION="${BASE_VERSION}-dev-${COMMIT_HASH}"
          echo "version=${DEV_VERSION}" >> $GITHUB_OUTPUT
          echo "Development version: ${DEV_VERSION}"
      
      - name: Update package.json version
        run: |
          npm version ${{ steps.version.outputs.version }} --no-git-tag-version
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dev-build-${{ steps.version.outputs.version }}
          path: |
            dist/
            package.json
          retention-days: 7
      
      - name: Comment PR with version
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🔨 Development build ready: \`${{ steps.version.outputs.version }}\``
            })
```

#### 2.2 Stable Release Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
      
      - name: Determine version bump
        id: bump
        run: |
          # Check commit messages for version bump hints
          COMMITS=$(git log --format=%B -n 10)
          
          if echo "$COMMITS" | grep -qE "^(feat|feature)(\(.+\))?!:|^BREAKING CHANGE:"; then
            echo "bump=major" >> $GITHUB_OUTPUT
          elif echo "$COMMITS" | grep -qE "^feat(\(.+\))?:"; then
            echo "bump=minor" >> $GITHUB_OUTPUT
          else
            echo "bump=patch" >> $GITHUB_OUTPUT
          fi
      
      - name: Bump version
        id: version
        run: |
          CURRENT_VERSION=$(cat VERSION)
          IFS='.' read -ra PARTS <<< "$CURRENT_VERSION"
          MAJOR=${PARTS[0]}
          MINOR=${PARTS[1]}
          PATCH=${PARTS[2]}
          
          case "${{ steps.bump.outputs.bump }}" in
            major)
              MAJOR=$((MAJOR + 1))
              MINOR=0
              PATCH=0
              ;;
            minor)
              MINOR=$((MINOR + 1))
              PATCH=0
              ;;
            patch)
              PATCH=$((PATCH + 1))
              ;;
          esac
          
          NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
          echo "$NEW_VERSION" > VERSION
          echo "version=${NEW_VERSION}" >> $GITHUB_OUTPUT
          echo "New version: ${NEW_VERSION}"
      
      - name: Update package.json
        run: |
          npm version ${{ steps.version.outputs.version }} --no-git-tag-version
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Generate changelog
        run: |
          # Install conventional-changelog-cli if not in package.json
          npx conventional-changelog-cli -p angular -i CHANGELOG.md -s
      
      - name: Commit version bump
        run: |
          git add VERSION package.json package-lock.json CHANGELOG.md
          git commit -m "chore(release): v${{ steps.version.outputs.version }}"
      
      - name: Create Git tag
        run: |
          git tag -a "v${{ steps.version.outputs.version }}" -m "Release v${{ steps.version.outputs.version }}"
      
      - name: Push changes and tags to GitHub
        run: |
          git push origin main --follow-tags
      
      - name: Create GitHub Release
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const changelog = fs.readFileSync('CHANGELOG.md', 'utf8');
            
            // Extract latest version changes
            const latestChanges = changelog.split('##')[1] || 'Release notes';
            
            await github.rest.repos.createRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              tag_name: 'v${{ steps.version.outputs.version }}',
              name: 'Release v${{ steps.version.outputs.version }}',
              body: latestChanges,
              draft: false,
              prerelease: false,
              make_latest: true
            });
```

#### 2.3 Pre-release Workflow

Create `.github/workflows/pre-release.yml`:

```yaml
name: Pre-release

on:
  push:
    branches:
      - 'release/**'
      - 'hotfix/**'

permissions:
  contents: write

jobs:
  pre-release:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Determine pre-release type
        id: prerelease
        run: |
          BRANCH_NAME=${GITHUB_REF#refs/heads/}
          
          if [[ $BRANCH_NAME == release/* ]]; then
            echo "type=rc" >> $GITHUB_OUTPUT
          elif [[ $BRANCH_NAME == hotfix/* ]]; then
            echo "type=beta" >> $GITHUB_OUTPUT
          else
            echo "type=alpha" >> $GITHUB_OUTPUT
          fi
      
      - name: Generate pre-release version
        id: version
        run: |
          BASE_VERSION=$(cat VERSION)
          COMMIT_HASH=${GITHUB_SHA::7}
          PRERELEASE_COUNT=$(git tag -l "v${BASE_VERSION}-${{ steps.prerelease.outputs.type }}.*" | wc -l)
          PRERELEASE_NUM=$((PRERELEASE_COUNT + 1))
          
          PRERELEASE_VERSION="${BASE_VERSION}-${{ steps.prerelease.outputs.type }}.${PRERELEASE_NUM}-${COMMIT_HASH}"
          echo "version=${PRERELEASE_VERSION}" >> $GITHUB_OUTPUT
          echo "Pre-release version: ${PRERELEASE_VERSION}"
      
      - name: Update package.json
        run: |
          npm version ${{ steps.version.outputs.version }} --no-git-tag-version
      
      - name: Install and test
        run: |
          npm ci
          npm test
          npm run build
      
      - name: Create and push pre-release tag to GitHub
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git tag -a "v${{ steps.version.outputs.version }}" -m "Pre-release v${{ steps.version.outputs.version }}"
          git push origin "v${{ steps.version.outputs.version }}"
      
      - name: Create GitHub Pre-release
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.repos.createRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              tag_name: 'v${{ steps.version.outputs.version }}',
              name: 'Pre-release v${{ steps.version.outputs.version }}',
              body: `Pre-release build for testing (${{ steps.prerelease.outputs.type }})`,
              draft: false,
              prerelease: true
            });
```

### Phase 3: Version Management Scripts

#### 3.1 Add npm Scripts

Update your `package.json`:

```json
{
  "scripts": {
    "version:dev": "node scripts/version-dev.js",
    "version:bump": "node scripts/version-bump.js",
    "version:current": "cat VERSION",
    "version:check": "node scripts/version-check.js",
    "release:major": "npm run version:bump -- major",
    "release:minor": "npm run version:bump -- minor",
    "release:patch": "npm run version:bump -- patch"
  }
}
```

#### 3.2 Create Version Management Scripts

Create `scripts/version-dev.js`:

```javascript
#!/usr/bin/env node
const fs = require('fs');
const { execSync } = require('child_process');

const baseVersion = fs.readFileSync('VERSION', 'utf8').trim();
const commitHash = execSync('git rev-parse --short HEAD').toString().trim();
const devVersion = `${baseVersion}-dev-${commitHash}`;

console.log(`Development version: ${devVersion}`);

// Update package.json
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
packageJson.version = devVersion;
fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2) + '\n');
```

Create `scripts/version-bump.js`:

```javascript
#!/usr/bin/env node
const fs = require('fs');

const bumpType = process.argv[2] || 'patch';
const currentVersion = fs.readFileSync('VERSION', 'utf8').trim();
const [major, minor, patch] = currentVersion.split('.').map(Number);

let newVersion;
switch (bumpType) {
  case 'major':
    newVersion = `${major + 1}.0.0`;
    break;
  case 'minor':
    newVersion = `${major}.${minor + 1}.0`;
    break;
  case 'patch':
  default:
    newVersion = `${major}.${minor}.${patch + 1}`;
    break;
}

console.log(`Bumping version: ${currentVersion} → ${newVersion}`);

// Update VERSION file
fs.writeFileSync('VERSION', newVersion + '\n');

// Update package.json
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
packageJson.version = newVersion;
fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2) + '\n');

console.log(`Version bumped to ${newVersion}`);
```

Create `scripts/version-check.js`:

```javascript
#!/usr/bin/env node
const fs = require('fs');

const versionFile = fs.readFileSync('VERSION', 'utf8').trim();
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));

console.log(`VERSION file: ${versionFile}`);
console.log(`package.json:  ${packageJson.version}`);

// Check if versions match (ignoring metadata)
const versionFileBase = versionFile.split('-')[0];
const packageJsonBase = packageJson.version.split('-')[0];

if (versionFileBase !== packageJsonBase) {
  console.error('❌ Version mismatch detected!');
  process.exit(1);
}

console.log('✅ Versions are in sync');
```

## Conventional Commits Integration

### Commit Message Format

Use conventional commits to automate version bumping:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types that trigger version bumps:**

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | MINOR | `feat: add user authentication` |
| `fix:` | PATCH | `fix: resolve memory leak in worker` |
| `feat!:` or `BREAKING CHANGE:` | MAJOR | `feat!: redesign API endpoints` |
| `perf:` | PATCH | `perf: optimize database queries` |
| `refactor:` | PATCH (optional) | `refactor: simplify auth logic` |

**Examples:**

```bash
# Minor version bump (new feature)
git commit -m "feat: add export to CSV functionality"

# Patch version bump (bug fix)
git commit -m "fix: correct date formatting in reports"

# Major version bump (breaking change)
git commit -m "feat!: redesign authentication system

BREAKING CHANGE: OAuth endpoints have been restructured"
```

## Version Validation

### Pre-commit Hook

Create `.husky/pre-commit`:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Check version consistency
npm run version:check
```

### CI Version Check

Add to your workflows:

```yaml
- name: Validate version
  run: npm run version:check
```

## Documentation Requirements

### Update README.md

Add version badge and release information:

```markdown
# Project Name

![Version](https://img.shields.io/github/v/release/username/repo)
![Dev Build](https://img.shields.io/github/workflow/status/username/repo/Development%20Build)

## Installation

### Stable Release
\`\`\`bash
npm install package-name@latest
\`\`\`

### Development Build
\`\`\`bash
npm install package-name@dev
\`\`\`

## Versioning

This project follows [Semantic Versioning](https://semver.org/).

- Stable releases: `1.4.0`
- Development builds: `1.4.1-dev-abcdef7`
- Pre-releases: `1.5.0-rc.1`
```

### Create VERSIONING.md

Document your versioning strategy:

```markdown
# Versioning Strategy

## Version Format

`MAJOR.MINOR.PATCH[-PRERELEASE][-METADATA]`

## Release Process

1. Feature branches create dev builds: `1.4.1-dev-abcdef7`
2. Merging to `main` creates stable releases: `1.4.1`
3. Release branches create RCs: `1.5.0-rc.1`

## Version Bumping

- **Major**: Breaking changes (v2.0.0)
- **Minor**: New features (v1.5.0)
- **Patch**: Bug fixes (v1.4.1)

## Automated Releases

Versions are automatically managed by GitHub Actions based on conventional commits.
```

## Best Practices

### ✅ DO:
- Use conventional commits for automatic version bumping (or manual version file updates)
- Include commit hashes in development builds (using hyphens for Docker compatibility)
- Tag all releases in Git and push to GitHub
- Always push version commits and tags to remote
- Use `make_latest: true` for stable releases in GitHub API
- Generate changelogs automatically
- Test builds before releasing
- Use pre-release tags for testing (alpha, beta, rc)
- Keep VERSION file in sync with package.json
- Use Docker tag `latest` for most recent stable release (not Git tag)
- Publish to multiple registries (Docker Hub + GitHub Container Registry)
- Generate multiple Docker tags per release (`1.5.0`, `1.5`, `1`, `latest`)

### ❌ DON'T:
- Manually edit version numbers without updating VERSION file
- Skip version tags in Git or forget to push them
- Keep version changes only locally
- Release without testing
- Use plus signs (`+`) in Docker tags (use hyphens instead)
- Forget to update changelogs
- Mix pre-release and stable versions in dependencies
- Create releases without pushing commits first
- Use Git `latest` tag (Docker tags only)

## Troubleshooting

### Version Mismatch Between FILES

**Problem:** VERSION file and package.json show different versions

**Solution:**
```bash
# Sync package.json to VERSION file
npm run version:check
# If mismatch, manually fix:
echo "1.4.0" > VERSION
npm version 1.4.0 --no-git-tag-version
```

### Failed Automated Release

**Problem:** GitHub Action fails to create release

**Solution:**
1. Check `GITHUB_TOKEN` permissions (needs `contents: write`)
2. Verify conventional commits are formatted correctly
3. Check for merge conflicts in VERSION file
4. Ensure the workflow has permission to push to protected branches

### Tags Not Appearing on GitHub

**Problem:** Git tags created locally but not visible on GitHub

**Solution:**
1. Verify workflow uses `git push origin main --follow-tags`
2. Check that `GITHUB_TOKEN` has push permissions
3. Ensure branch protection rules allow CI to push
4. Manually verify: `git ls-remote --tags origin`

### Pre-release Not Created

**Problem:** Pre-release workflow doesn't trigger

**Solution:**
1. Verify branch name matches pattern (`release/**`, `hotfix/**`)
2. Check workflow file syntax
3. Ensure workflow has proper permissions

## Integration with Other Workflows

### Docker Image Tagging

```yaml
- name: Build and tag Docker image
  run: |
    VERSION=$(cat VERSION)
    # Extract major.minor.patch components
    IFS='.' read -ra PARTS <<< "$VERSION"
    MAJOR=${PARTS[0]}
    MINOR=${PARTS[1]}
    
    # Build with multiple tags
    docker build \
      -t myapp:${VERSION} \
      -t myapp:${MAJOR}.${MINOR} \
      -t myapp:${MAJOR} \
      -t myapp:latest \
      .
    
    # Push all tags
    docker push myapp:${VERSION}
    docker push myapp:${MAJOR}.${MINOR}
    docker push myapp:${MAJOR}
    docker push myapp:latest
```

### Multi-Registry Publishing

```yaml
- name: Login to registries
  run: |
    echo "${{ secrets.DOCKER_TOKEN }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
    echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

- name: Build and push to multiple registries
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: |
      ${{ secrets.DOCKER_USERNAME }}/myapp:${{ steps.version.outputs.version }}
      ${{ secrets.DOCKER_USERNAME }}/myapp:latest
      ghcr.io/${{ github.repository_owner }}/myapp:${{ steps.version.outputs.version }}
      ghcr.io/${{ github.repository_owner }}/myapp:latest
    labels: |
      org.opencontainers.image.version=${{ steps.version.outputs.version }}
      org.opencontainers.image.source=${{ github.repositoryUrl }}
```

### NPM Publishing

```yaml
- name: Publish to NPM
  run: |
    npm config set //registry.npmjs.org/:_authToken=${{ secrets.NPM_TOKEN }}
    npm publish --access public
```

### Changelog Generation

Use `conventional-changelog`:

```bash
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

## Success Metrics

After implementation, you should have:

- ✅ Automated version bumping on merge to main
- ✅ Development builds with commit hashes
- ✅ Pre-release tags for testing
- ✅ GitHub releases automatically created with proper tagging
- ✅ Docker `latest` tag always points to most recent stable release
- ✅ All version changes pushed to GitHub (not just local)
- ✅ Changelogs generated from commits
- ✅ Version consistency across files
- ✅ CI/CD integration working
- ✅ Multi-registry publishing (Docker Hub + GHCR)
- ✅ Multiple Docker tags per release (semver + major + minor + latest)
- ✅ Multi-platform builds (amd64 + arm64)

## Deliverables

1. **VERSION file** in repository root (or use package.json as source of truth)
2. **GitHub Actions workflows** (can be single unified workflow or separate)
3. **Version management scripts** in `/scripts` (e.g., `get_version.sh`)
4. **Updated package.json** with version scripts
5. **VERSIONING.md** documentation
6. **CHANGELOG.md** automatically generated
7. **Git tags** for all releases (pushed to GitHub, format: `v1.0.0`)
8. **GitHub Releases** created automatically with `make_latest: true`
9. **Version commits** pushed to GitHub (not only local)
10. **Docker images** published to Docker Hub and GHCR
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
