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

Run comprehensive vulnerability checks:

```bash
# Node.js
npm audit --production
npm audit fix --dry-run
yarn audit

# Python
pip-audit
safety check --json

# Java
mvn dependency-check:check
./gradlew dependencyCheckAnalyze

# Go
go list -json -m all | nancy sleuth
govulncheck ./...

# Rust
cargo audit

# Ruby
bundle audit check --update

# PHP
composer audit
```

### **Outdated Package Detection**

Identify available updates:

```bash
# Node.js
npm outdated
npx npm-check-updates -u --dry-run

# Python
pip list --outdated
poetry show --outdated

# Java
mvn versions:display-dependency-updates

# Go
go list -u -m all

# Rust
cargo outdated

# Ruby
bundle outdated

# PHP
composer outdated
```

### **Dependency Health Analysis**

**Check for**:
- Deprecated packages (no longer maintained)
- Package typosquatting risks
- Excessive dependencies (bloat)
- Circular dependencies
- License compatibility issues
- Download count and community activity
- Last release date and maintenance status

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

### **Automated Analysis**

**Check for breaking changes**:

1. **Changelog Analysis**
   - Parse CHANGELOG.md, HISTORY.md, RELEASES.md
   - Search for keywords: "BREAKING", "breaking change", "removed", "deprecated"
   - Identify API removals and signature changes

2. **Migration Guide Detection**
   - Look for MIGRATION.md, UPGRADING.md
   - Extract migration steps and required code changes
   - Identify automated migration tools (codemods)

3. **API Compatibility**
   - Compare exported APIs between versions
   - Detect removed functions, classes, methods
   - Identify signature changes (parameters, return types)

4. **TypeScript/Type Definitions**
   - Compare type definitions for breaking changes
   - Detect changed interfaces and type signatures
   - Identify removed or renamed types

### **Impact Assessment**

For each update, analyze:

```bash
# Example: Check what files import the dependency
# Node.js/TypeScript
grep -r "from 'package-name'" --include="*.{js,ts,jsx,tsx}"
grep -r "require('package-name')" --include="*.{js,ts}"

# Python
grep -r "import package_name" --include="*.py"
grep -r "from package_name" --include="*.py"

# Count affected files
echo "Affected files: $(grep -r "import package" --include="*.py" | wc -l)"
```

**Generate impact report**:
- Number of files importing the dependency
- Test files that exercise the dependency
- Critical paths using the dependency
- Estimated refactoring effort (hours)

---

## **Automated Update Workflow**

### **1. Preparation**

```bash
# Create update branch
git checkout -b deps/update-[package-name]-[version]

# Ensure clean working directory
git status

# Backup lock files
cp package-lock.json package-lock.json.backup
```

### **2. Update Execution**

**Conservative approach** (recommended):

```bash
# Update one package at a time
npm update [package-name]@[version]

# Or specify exact version
npm install [package-name]@[exact-version]
```

**Aggressive approach** (for patch updates):

```bash
# Update all packages (use with caution)
npm update

# Or interactive mode
npx npm-check-updates -i
```

### **3. Automated Testing**

Run comprehensive test suite:

```bash
# Install dependencies
npm ci  # or yarn install --frozen-lockfile

# Run all tests
npm test

# Run type checking
npm run type-check  # or tsc --noEmit

# Run linting
npm run lint

# Build project
npm run build

# Run integration tests
npm run test:integration

# Run E2E tests (if applicable)
npm run test:e2e
```

### **4. Validation Checks**

**Verify**:
- [ ] All tests pass
- [ ] No new type errors
- [ ] No new linting errors
- [ ] Build succeeds
- [ ] Bundle size acceptable (check with bundlesize, size-limit)
- [ ] No console warnings or errors
- [ ] Critical user flows work (manual testing)
- [ ] Performance benchmarks maintained

### **5. Commit & PR**

```bash
# Commit with semantic message
git add package.json package-lock.json
git commit -m "chore(deps): update [package] from [old-ver] to [new-ver]

- Fixes: [security-issue or bug]
- Breaking changes: [none/list]
- Migration steps: [none/required]
- Tests: [all passing]"

# Push and create PR
git push origin deps/update-[package-name]-[version]
```

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
    
    # Security updates always separate
    allow:
      - dependency-type: "direct"
      - dependency-type: "indirect"
    
    # Auto-approve and merge patch updates
    labels:
      - "dependencies"
      - "automated"
    
    reviewers:
      - "team-name"
```

### **Renovate Bot Configuration**

Create `renovate.json`:

```json
{
  "extends": ["config:base"],
  "schedule": ["before 10am on monday"],
  "automerge": true,
  "automergeType": "pr",
  "automergeStrategy": "squash",
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "pin", "digest"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["minor"],
      "automerge": false,
      "labels": ["review-required"]
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["breaking-change", "review-required"]
    },
    {
      "matchPackagePatterns": ["*"],
      "matchUpdateTypes": ["patch"],
      "groupName": "all patch dependencies",
      "groupSlug": "all-patch"
    }
  ]
}
```

### **CI Integration**

Add to `.github/workflows/dependencies.yml`:

```yaml
name: Dependency Updates

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Check for updates
        run: |
          npm outdated || true
          npm audit || true
      
      - name: Update patch versions
        run: npm update
      
      - name: Run tests
        run: npm test
      
      - name: Create PR if changes
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: 'chore(deps): update dependencies'
          title: 'chore(deps): automated dependency updates'
          branch: deps/automated-updates
          labels: dependencies, automated
```

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
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
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