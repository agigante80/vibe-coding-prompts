---
name: dependency-update-manager
category: security
version: 1.1.0
updated: 2026-08-27
description: Automate dependency updates with risk classification, testing and rollback.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# Dependency Update Manager

## **Objective**

Automate dependency updates with intelligent breaking change detection, automated testing, and safe rollback mechanisms to keep projects secure and up-to-date.

---

## **Assessment Phase**

### 1. **Project Analysis**

* Detect package managers and dependency systems:
  - **Node.js**: npm, yarn, pnpm (package.json, package-lock.json)
  - **Python**: pip, poetry, pipenv (requirements.txt, Pipfile, pyproject.toml)
  - **Java**: Maven, Gradle (pom.xml, build.gradle)
  - **Go**: go modules (go.mod, go.sum)
  - **Rust**: Cargo (Cargo.toml, Cargo.lock)
  - **Ruby**: Bundler (Gemfile, Gemfile.lock)
  - **PHP**: Composer (composer.json, composer.lock)
* Identify direct vs. transitive dependencies
* Catalog current versions and available updates
* Detect monorepo structures and workspace dependencies
* Review dependency lock files for consistency

### 2. **Update Classification**

Categorize updates by type and risk:

| Update Type | Version Change | Risk Level | Examples |
|------------|---------------|------------|----------|
| **Security Patch** | Any (CVE fix) | High Priority | Critical vulnerabilities, zero-days |
| **Major** | 1.x.x → 2.x.x | High Risk | Breaking changes, API redesigns |
| **Minor** | x.1.x → x.2.x | Medium Risk | New features, possible deprecations |
| **Patch** | x.x.1 → x.x.2 | Low Risk | Bug fixes, performance improvements |

---

## **Dependency Audit**

### **Security Vulnerability Scanning**

**Tools**: Node.js (`npm audit`, `yarn audit`), Python (`pip-audit`, `safety`), Java (`mvn dependency-check`, `gradle dependencyCheckAnalyze`), Go (`govulncheck`), Rust (`cargo audit`), Ruby (`bundle audit`), PHP (`composer audit`)

### **Outdated Package Detection**

**Tools**: Node.js (`npm outdated`, `npm-check-updates`), Python (`pip list --outdated`, `poetry show --outdated`), Java (`mvn versions:display-dependency-updates`), Go (`go list -u -m all`), Rust (`cargo outdated`), Ruby (`bundle outdated`), PHP (`composer outdated`)

### **Dependency Health Analysis**

**Check**: Deprecated packages, typosquatting risks, bloat, circular deps, license compatibility, community activity, maintenance status

---

## **Update Strategy**

### **Prioritization Framework**

**Priority 1 - Immediate (Security Critical)**:
- CVE with CVSS score ≥ 7.0
- Known exploits in the wild
- Direct dependencies with public vulnerabilities
- Zero-day vulnerabilities

**Priority 2 - High (Within 48 hours)**:
- CVE with CVSS score 4.0-6.9
- Deprecated packages with security implications
- Major version updates with security improvements

**Priority 3 - Medium (Within 1 week)**:
- Minor version updates with bug fixes
- Dependencies with multiple patch versions behind
- Performance improvements
- Compatibility updates

**Priority 4 - Low (Next sprint)**:
- Minor feature additions
- Documentation updates
- Single patch version behind
- Dev dependencies with no production impact

### **Update Batching**

Group updates intelligently:

1. **Security-only batch** - All security patches together
2. **Major version batch** - One major update at a time (test thoroughly)
3. **Minor/Patch batch** - Group compatible minor/patch updates
4. **Dev dependencies batch** - Separate from production dependencies

---

## **Breaking Change Detection**

**Automated analysis**:
1. **Changelog**: Parse CHANGELOG.md/HISTORY.md for "BREAKING", "removed", "deprecated"
2. **Migration guides**: Look for MIGRATION.md/UPGRADING.md, codemods
3. **API compatibility**: Compare exported APIs, detect removed functions/classes/methods
4. **Type definitions**: Compare TypeScript types for breaking changes

**Impact assessment**: Count files importing dependency (grep), identify test files exercising it, estimate refactoring effort

---

## **Automated Update Workflow**

**1. Preparation**: Create update branch `git checkout -b deps/update-[package]-[version]`, backup lock files

**2. Update**: Conservative (one at a time): `npm update [package]@[version]`. Aggressive (patches): `npm update` or `npx npm-check-updates -i`

**3. Testing**: Install (`npm ci`), run tests/type-check/lint/build/integration/e2e

**4. Validation**: All tests pass, no type/lint errors, build succeeds, bundle size OK, critical flows work

**5. Commit**: `git commit -m "chore(deps): update [package] [old]→[new]\n\n- Fixes: [issue]\n- Breaking: [none/list]\n- Tests: [passing]"`

---

## **Rollback Strategy**

### **Quick Rollback**

If update causes issues:

```bash
# Restore from backup
cp package-lock.json.backup package-lock.json
npm ci

# Or revert specific package
npm install [package-name]@[previous-version]

# Git revert
git revert HEAD
```

### **Pinning Strategy**

For problematic updates:

```json
// package.json
{
  "dependencies": {
    "problematic-package": "1.2.3"  // Exact version, not ^1.2.3
  },
  "resolutions": {  // Yarn
    "problematic-package": "1.2.3"
  },
  "overrides": {  // npm 8.3+
    "problematic-package": "1.2.3"
  }
}
```

---

## **Automation Configuration**

### **Dependabot Setup**

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Enable for package ecosystem
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 5
    
    # Group minor and patch updates
    groups:
      production-dependencies:
        dependency-type: "production"
        update-types:
          - "minor"
          - "patch"
      
      development-dependencies:
        dependency-type: "development"
        update-types:
          - "minor"
          - "patch"
    
    # Which dependencies receive update PRs. The groups above batch version
    # updates; security updates arrive individually unless you opt in to
    # grouped security updates (applies-to: security-updates in a group).
    allow:
      - dependency-type: "direct"
      - dependency-type: "indirect"

    labels:
      - "dependencies"
      - "automated"
```

**Auto-merge** cannot be expressed in `dependabot.yml`. It requires GitHub's auto-merge feature plus branch protection, wired by a small workflow:

```yaml
# .github/workflows/dependabot-automerge.yml
name: Dependabot auto-merge
on: pull_request
permissions: {contents: write, pull-requests: write}
jobs:
  automerge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: dependabot/fetch-metadata@v2
        id: meta
      - if: steps.meta.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env: {PR_URL: '${{ github.event.pull_request.html_url }}', GH_TOKEN: '${{ secrets.GITHUB_TOKEN }}'}
```

### **Renovate Bot Configuration**

Create `renovate.json`:

```json
{
  "extends": ["config:recommended"],
  "schedule": ["before 10am on monday"],
  "automerge": false,
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "pin", "digest"],
      "automerge": true,
      "automergeType": "pr",
      "automergeStrategy": "squash",
      "groupName": "all patch dependencies"
    },
    {
      "matchUpdateTypes": ["minor"],
      "labels": ["review-required"]
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["breaking-change", "review-required"]
    }
  ]
}
```

Note: `config:base` was renamed to `config:recommended` in Renovate v36; the default stays `automerge: false` so only the explicit patch rule merges unattended.

### **CI Integration**

Do NOT add a scheduled workflow that runs `npm update` and opens PRs: it duplicates the bot you just configured and produces conflicting update PRs. A custom scheduled job is justified only for ecosystems your bot does not cover; if you write one, use current action majors pinned to full commit SHAs, a supported Node LTS, and `permissions: contents: read` plus the minimum needed to open a PR.

---

## **Deliverables**

Generate the following:

1. **Dependency Audit Report**:
   - Current dependency tree visualization
   - Security vulnerabilities with CVSS scores
   - Outdated packages list with available versions
   - Deprecated packages requiring replacement
   - License compliance status

2. **Update Plan**:
   - Prioritized update queue (Security → Major → Minor → Patch)
   - Breaking change analysis for each major update
   - Estimated effort and risk assessment
   - Recommended update batches
   - Migration guides and codemods (if available)

3. **Automation Setup**:
   - Dependabot or Renovate configuration
   - CI/CD integration for automated testing
   - Auto-merge rules for low-risk updates
   - Notification and alerting setup

4. **Documentation**:
   - Update process and guidelines
   - Rollback procedures
   - Breaking change handling workflow
   - Contact points for dependency issues

### **Documentation Updates**
All dependency updates and management procedures must be documented in `/docs/`:

- **`/docs/SECURITY_AND_PRIVACY.md`**: Add vulnerability management process, dependency security policies, and CVE tracking procedures
- **`/docs/IMPROVEMENT_AREAS.md`**: Document outdated dependencies, breaking change migration efforts, and dependency optimization opportunities
- **`/docs/REFACTORING_PLAN.md`**: Add major version upgrade tasks with breaking change analysis and migration steps
- **`/docs/ARCHITECTURE.md`**: Update dependency tree, third-party integrations, and technology stack documentation

---

## **Success Criteria**

- [ ] All security vulnerabilities addressed (Critical and High CVEs resolved)
- [ ] Dependencies categorized by update priority (Security → Major → Minor → Patch)
- [ ] Automated dependency scanning in place (Dependabot, Renovate, etc.)
- [ ] Test suite validates updates automatically in CI/CD
- [ ] Breaking changes documented with migration paths and codemods
- [ ] Rollback strategy tested and documented
- [ ] Auto-merge configured for low-risk updates
- [ ] Team trained on update process and rollback procedures
- [ ] Monitoring for new vulnerabilities active (alerts configured)
- [ ] **`/docs/` files updated** with dependency management procedures

---

## **Best Practices**

### **Update Hygiene**

* Update dependencies regularly (weekly or bi-weekly)
* Don't let dependencies get too far behind
* Read changelogs before updating
* Test thoroughly, especially major updates
* Keep lock files in version control
* Document update decisions and issues

### **Risk Mitigation**

* Update dev dependencies separately from production
* Use feature flags for risky updates
* Deploy updates in stages (dev → staging → production)
* Monitor error rates and metrics after updates
* Have rollback plan ready
* Keep communication open with team

### **Continuous Improvement**

* Track time spent on dependency updates
* Identify problematic dependencies (frequent issues)
* Consider alternatives for high-maintenance packages
* Contribute fixes upstream when possible
* Share knowledge and learnings with team

---

## **Usage Instructions**

### **When to Run This Prompt**

* Starting dependency management for a project
* Setting up automated dependency updates
* Preparing for major version upgrades
* Responding to security vulnerabilities
* Regular maintenance cycles (weekly/monthly)
* Before major releases or deployments
* Onboarding dependency management practices

### **Initial Setup**
1. Review the [Prompt Creation Guide](../docs/prompt-creation-guide.md) to understand documentation requirements
2. Examine existing `/docs/` files to understand current project state
3. Identify package manager(s) in use (npm, pip, cargo, etc.)
4. Ensure CI/CD pipeline exists for automated testing

### **Execution**
```
I need to set up automated dependency management for my [PROJECT_TYPE].

Package manager: [npm/yarn/pnpm/pip/poetry/maven/gradle/cargo/etc.]
Current dependency count: [number or "unknown"]
Known security issues: [yes/no/unknown]
Breaking change tolerance: [high/medium/low]
Update frequency preference: [daily/weekly/monthly]
Auto-merge preference: [yes for low-risk/no, manual review all]
```

### **Expected Outcome**
The AI will analyze your dependency ecosystem, identify security vulnerabilities with CVSS scores, categorize updates by priority and risk level, set up automated dependency scanning (Dependabot, Renovate, etc.), configure auto-merge for low-risk updates, provide breaking change analysis for major updates with migration guides, establish rollback procedures, and document all dependency management procedures in `/docs/` files. You'll receive a comprehensive dependency management system that keeps your project secure and up-to-date with minimal manual intervention.