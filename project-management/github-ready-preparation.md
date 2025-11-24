# GitHub Ready Preparation

## **Objective**

Prepare a project for professional GitHub publication by establishing proper structure, documentation, automation, security, and community guidelines to ensure anyone can clone, understand, run, and contribute without external guidance.

---

## **Assessment Phase**

### 1. **Project Structure Analysis**

**Discover Current State**:
- Analyze repository structure and organization
- Identify project type (library, application, CLI tool, Docker image, etc.)
- Detect programming language and framework
- Review existing files and documentation
- Check for common structure issues (flat structure, mixed concerns)
- Identify missing essential files

**Required Files Audit**:
```bash
# Check for essential files
[ -f "README.md" ] && echo "✅ README.md" || echo "❌ Missing README.md"
[ -f "LICENSE" ] && echo "✅ LICENSE" || echo "❌ Missing LICENSE"
[ -f ".gitignore" ] && echo "✅ .gitignore" || echo "❌ Missing .gitignore"
[ -f "CHANGELOG.md" ] && echo "✅ CHANGELOG.md" || echo "⚠️  Missing CHANGELOG.md (optional)"
[ -f ".gitattributes" ] && echo "✅ .gitattributes" || echo "⚠️  Missing .gitattributes (optional)"
[ -f "CONTRIBUTING.md" ] && echo "✅ CONTRIBUTING.md" || echo "⚠️  Missing CONTRIBUTING.md"
[ -f "CODE_OF_CONDUCT.md" ] && echo "✅ CODE_OF_CONDUCT.md" || echo "⚠️  Missing CODE_OF_CONDUCT.md"
```

### 2. **.gitignore Review & Validation**

**Critical Checks**:
- Verify `.gitignore` is not excluding files that are needed for the project to function
- Ensure all build artifacts, temporary files, and OS-specific files are ignored
- Check that secrets, credentials, and environment files are properly ignored
- Validate that source code, configuration, and documentation are NOT ignored

**Organization Requirements**:
```gitignore
# === Dependencies ===
node_modules/
vendor/
__pycache__/

# === Build Output ===
dist/
build/
*.exe
*.dll

# === Environment & Secrets ===
.env
.env.local
*.key
*.pem
credentials.json

# === IDE & Editor ===
.vscode/
.idea/
*.swp

# === OS Files ===
.DS_Store
Thumbs.db

# === Logs ===
*.log
logs/
```

**Validation Steps**:
1. Check if any tracked files match patterns in `.gitignore` (orphaned patterns)
2. Verify essential files like `package.json`, `README.md`, `.env.example` are tracked
3. Ensure `.gitignore` patterns are not too broad (e.g., `*.json` would ignore `package.json`)
4. Identify missing patterns for common build output or temporary files
5. Remove obsolete patterns for directories or file types no longer in the project

**Test Needed Files Are Not Ignored**:
```bash
# Verify critical files are not accidentally ignored
git check-ignore README.md package.json src/ tests/ docs/ .env.example
# Should return nothing - these files must be tracked
```

### 3. **File Organization Verification**

**Repository Hygiene Audit**:
- Identify the purpose of every file in the repository
- Flag files that appear to be obsolete (old scripts, deprecated code, unused configurations)
- Find duplicate functionality or redundant files
- Ensure files are organized into appropriate directories
- Verify file naming conventions are consistent

**Common Issues to Flag**:
- Test files or scratch scripts in root directory (should be in `tests/` or `scripts/`)
- Multiple configuration files for the same purpose (e.g., `config.js`, `config.json`, `settings.js`)
- Old backup files (e.g., `app.js.bak`, `config.old.json`)
- Commented-out or deprecated code files that should be removed
- Documentation files scattered across directories instead of centralized in `docs/`
- Build artifacts that should be in `.gitignore`

**Organization Checklist**:
```bash
# Find files that may need organization
find . -type f -name "*.bak" -o -name "*.old" -o -name "*_old.*" -o -name "*.tmp"
find . -maxdepth 1 -type f -name "test_*" -o -name "*_test.*"  # Tests in root
find . -type f -name "config*" | wc -l  # Multiple config files?
```

**Documentation Requirements**:
- Ambiguous files must have their purpose documented in README or inline comments
- Directory structure should align with documented architecture
- Files with unclear names should be renamed or have explanation added
- Deprecated files should be removed, not just commented out or renamed

### 4. **Dependency Management Check**

**Verify Package Management**:
- **Node.js**: `package.json`, `package-lock.json` or `yarn.lock`
- **Python**: `requirements.txt`, `pyproject.toml`, `Pipfile`
- **Java**: `pom.xml`, `build.gradle`
- **Go**: `go.mod`, `go.sum`
- **Rust**: `Cargo.toml`, `Cargo.lock`
- **Ruby**: `Gemfile`, `Gemfile.lock`
- **PHP**: `composer.json`, `composer.lock`

**Validation**:
```bash
# Check if dependencies are properly locked
npm ls --depth=0 2>/dev/null || \
pip list 2>/dev/null || \
go list -m all 2>/dev/null
```

### 5. **Security Scan**

**Secrets Detection**:
```bash
# Scan for hardcoded secrets
grep -r "api_key\|API_KEY\|secret\|SECRET\|password\|PASSWORD\|token\|TOKEN" \
  --include="*.js" --include="*.py" --include="*.java" --include="*.go" \
  --exclude-dir=node_modules --exclude-dir=vendor

# Check for common secret patterns
git log --all --full-history -- **/.env
```

**Vulnerability Scanning**:
```bash
# Node.js
npm audit

# Python
pip-audit || safety check

# Check .gitignore covers sensitive files
grep -E "\.env$|\.env\.local|secrets|credentials|\.pem$|\.key$" .gitignore
```

### 6. **CI/CD Infrastructure**

**Check Automation**:
```bash
# GitHub Actions
ls -la .github/workflows/

# Check for common workflow files
[ -f ".github/workflows/ci.yml" ] && echo "✅ CI workflow exists"
[ -f ".github/workflows/release.yml" ] && echo "✅ Release workflow exists"
```

---

## **GitHub Readiness Checklist**

### 🧠 **1. Project Fundamentals**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | Clear folder structure | Organize into `src/`, `tests/`, `docs/`, `config/`, etc. | ⬜ |
| **Critical** | `.gitignore` properly configured | Exclude build artifacts, logs, secrets; ensure needed files tracked | ⬜ |
| **Critical** | `.gitignore` organized | Sections for dependencies, build, env, IDE, OS, logs | ⬜ |
| **Critical** | File organization audit | Identify obsolete files, document ambiguous files, remove duplicates | ⬜ |
| **Critical** | `README.md` | Professional, comprehensive documentation | ⬜ |
| **Critical** | `LICENSE` | MIT, Apache-2.0, GPL, or other explicit license | ⬜ |
| **Critical** | Dependencies managed | `package.json`, `requirements.txt`, etc. with locked versions | ⬜ |
| **Recommended** | `CHANGELOG.md` | Version history and notable changes | ⬜ |
| **Optional** | `.gitattributes` | Consistent line endings and text normalization | ⬜ |

**Folder Structure Template**:
```
project-root/
├── .github/
│   ├── workflows/          # CI/CD workflows
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Build/deployment scripts
├── config/                 # Configuration files
├── .gitignore
├── .gitattributes
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── package.json / requirements.txt / etc.
```

### 🚀 **2. Build & Run**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | Installation instructions | Clear, step-by-step in README | ⬜ |
| **Critical** | Build script | `npm run build`, `make`, `cargo build`, etc. | ⬜ |
| **Critical** | Start script | `npm start`, `python -m app`, `docker-compose up` | ⬜ |
| **Recommended** | `.env.example` | Template for required environment variables | ⬜ |
| **Recommended** | Docker setup | `Dockerfile` and/or `docker-compose.yml` | ⬜ |
| **Optional** | Makefile | Simplified build commands | ⬜ |

**Build Validation**:
```bash
# Test build process
npm run build && npm start  # or equivalent
docker build -t test-image .
docker-compose up -d
```

### 🧪 **3. Testing**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | Automated tests | Unit and integration tests | ⬜ |
| **Critical** | Tests runnable | `npm test`, `pytest`, etc. | ⬜ |
| **Recommended** | Coverage measurement | 70%+ code coverage ideal | ⬜ |
| **Recommended** | CI test execution | Tests run on every push/PR | ⬜ |
| **Recommended** | Test badges | Show test status in README | ⬜ |

**Test Frameworks by Language**:
- **JavaScript/TypeScript**: Jest, Mocha, Vitest
- **Python**: pytest, unittest
- **Java**: JUnit, TestNG
- **Go**: `go test`
- **Rust**: `cargo test`

### 🧰 **4. Automation / CI/CD**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | CI workflow | `.github/workflows/ci.yml` - build, test, lint | ⬜ |
| **Recommended** | Release automation | Auto-versioning and GitHub Releases | ⬜ |
| **Recommended** | Docker publishing | Push to Docker Hub/GHCR on release | ⬜ |
| **Recommended** | Code scanning | Security vulnerability scanning | ⬜ |
| **Recommended** | Dependabot | Automated dependency updates | ⬜ |
| **Optional** | Manual triggers | `workflow_dispatch` support | ⬜ |

**Minimal CI Workflow Template**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        run: |
          # Install dependencies
      - name: Lint
        run: |
          # Run linter
      - name: Test
        run: |
          # Run tests
      - name: Build
        run: |
          # Build project
```

### 🧭 **5. Documentation**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | `README.md` | Comprehensive project documentation | ⬜ |
| **Recommended** | `/docs/` folder | Additional guides, API reference, architecture | ⬜ |
| **Recommended** | Inline comments | Explain non-obvious logic | ⬜ |
| **Recommended** | API documentation | OpenAPI/Swagger for APIs | ⬜ |
| **Optional** | Doc generator | Sphinx, JSDoc, Docusaurus, etc. | ⬜ |

**Documentation Must Include**:
- What the project does (problem + solution)
- Installation instructions
- Usage examples
- Configuration options
- Contributing guidelines
- License information

### 👥 **6. Community & Contribution**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Recommended** | `CONTRIBUTING.md` | How to submit issues and PRs | ⬜ |
| **Recommended** | `CODE_OF_CONDUCT.md` | Community guidelines | ⬜ |
| **Recommended** | Issue templates | `.github/ISSUE_TEMPLATE/` | ⬜ |
| **Recommended** | PR template | `.github/PULL_REQUEST_TEMPLATE.md` | ⬜ |
| **Optional** | Labels | Categorize issues (bug, enhancement, etc.) | ⬜ |
| **Optional** | Milestones | Track project goals | ⬜ |

**Issue Template Example**:
```markdown
## Description
[Clear description of the issue]

## Steps to Reproduce
1. Step one
2. Step two

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., Ubuntu 22.04]
- Version: [e.g., 1.2.3]
```

### 🔐 **7. Security & Secrets**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | No secrets in repo | Scan history with `git-secrets` or `trufflehog` | ⬜ |
| **Critical** | `.env.example` | Document required environment variables | ⬜ |
| **Critical** | `.gitignore` secrets | Ensure `.env`, `*.key`, `*.pem` are ignored | ⬜ |
| **Recommended** | Dependabot enabled | Automated dependency security updates | ⬜ |
| **Recommended** | `SECURITY.md` | Security policy and vulnerability reporting | ⬜ |
| **Optional** | Secret scanning | Enable GitHub secret scanning | ⬜ |

**Security Scan Commands**:
```bash
# Install and run git-secrets
git secrets --scan-history

# Or use trufflehog
trufflehog git file://. --only-verified

# Check for common patterns
grep -r "password\s*=\s*['\"]" --include="*.py" --include="*.js"
```

### 🧱 **8. Releases & Distribution**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | Semantic versioning | Use `MAJOR.MINOR.PATCH` (e.g., `1.2.3`) | ⬜ |
| **Critical** | Dynamic versioning | Git-based version generation (`get_version.sh`) | ⬜ |
| **Recommended** | GitHub Releases | Tag versions with release notes | ⬜ |
| **Recommended** | Package publishing | npm, PyPI, Docker Hub, etc. | ⬜ |
| **Recommended** | `CHANGELOG.md` | Automated or manual changelog | ⬜ |
| **Optional** | Release automation | Semantic-release or similar | ⬜ |

**Versioning Strategy**:
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes

**Dynamic Versioning Implementation**:

Create `get_version.sh` script for Git-based version generation:

```bash
#!/bin/bash
set -e

# Get base version from package.json or equivalent
BASE_VERSION=$(node -p "require('./package.json').version" 2>/dev/null || echo "0.1.0")

# Get Git context
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
TAG=$(git describe --exact-match --tags 2>/dev/null || echo "")

# Generate version based on context
if [ "$BRANCH" = "main" ] && [ -n "$TAG" ]; then
    VERSION="$TAG"                                    # Tagged: 1.0.0
elif [ "$BRANCH" = "main" ]; then
    VERSION="${BASE_VERSION}-main-${COMMIT}"          # Main: 0.1.0-main-abc1234
elif [ "$BRANCH" = "develop" ]; then
    VERSION="${BASE_VERSION}-dev-${COMMIT}"           # Develop: 0.1.0-dev-abc1234
else
    SANITIZED_BRANCH=$(echo "$BRANCH" | sed 's/[^a-zA-Z0-9._-]/-/g')
    VERSION="${BASE_VERSION}-${SANITIZED_BRANCH}-${COMMIT}"  # Feature: 0.1.0-feature-auth-abc1234
fi

echo "$VERSION"
```

**Requirements**:
- Script must be executable: `chmod +x get_version.sh`
- Works in CI/CD with `fetch-depth: 0`
- Falls back gracefully when Git unavailable
- Sanitizes branch names (replace special chars)
- Used in Dockerfile: `ARG VERSION=unknown` → `ENV VERSION=${VERSION}`
- Application reads from environment variable
- Version displayed at startup and in health endpoint

### 📊 **9. Metadata & Visibility**

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | Repository description | Clear one-liner on GitHub | ⬜ |
| **Recommended** | GitHub topics | Add relevant tags (e.g., `python`, `docker`, `ai`) | ⬜ |
| **Recommended** | Website link | Link to docs or homepage | ⬜ |
| **Recommended** | README badges | Build, version, license, downloads | ⬜ |
| **Recommended** | Screenshots/GIFs | Visual representation of the project | ⬜ |
| **Optional** | Social preview | Custom Open Graph image | ⬜ |

**Essential Badges**:
```markdown
![Build](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/github/v/release/USER/REPO)
![License](https://img.shields.io/github/license/USER/REPO)
![Downloads](https://img.shields.io/github/downloads/USER/REPO/total)
```

### 🤖 **10. AI/Agent Integration** (Optional)

| Priority | Item | Description | Status |
|----------|------|-------------|--------|
| **Critical** | API credentials separated | No hardcoded tokens | ⬜ |
| **Recommended** | Agent documentation | Describe capabilities and endpoints | ⬜ |
| **Recommended** | Security boundaries | What data can/can't be accessed | ⬜ |
| **Recommended** | Example configs | For testing locally | ⬜ |
| **Optional** | MCP documentation | If using Model Context Protocol | ⬜ |

---

## **Common .gitignore Templates**

### **Node.js**
```gitignore
node_modules/
npm-debug.log
.env
.env.local
dist/
build/
*.log
.DS_Store
```

### **Python**
```gitignore
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.env
.env.local
dist/
build/
*.egg-info/
.pytest_cache/
```

### **Java**
```gitignore
target/
*.class
*.jar
*.war
.gradle/
build/
.env
```

### **Go**
```gitignore
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary
*.test

# Output
bin/
dist/

# Env
.env
.env.local
```

### **Rust**
```gitignore
target/
Cargo.lock
*.pdb
.env
.env.local
```

### **Universal**
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Secrets
*.key
*.pem
secrets/
credentials/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## **Deliverables**

### **Essential Files Created**
1. **`.gitignore`** - Comprehensive ignore rules for your language/framework
2. **`LICENSE`** - Appropriate open-source license (MIT, Apache-2.0, etc.)
3. **`README.md`** - Professional, complete documentation (or update existing)
4. **`CHANGELOG.md`** - Initial version history
5. **`.env.example`** - Template for environment variables
6. **`get_version.sh`** - Dynamic version generation script (executable)

### **Community Files**
6. **`CONTRIBUTING.md`** - Contribution guidelines
7. **`CODE_OF_CONDUCT.md`** - Community standards
8. **`.github/ISSUE_TEMPLATE/bug_report.md`** - Bug report template
9. **`.github/ISSUE_TEMPLATE/feature_request.md`** - Feature request template
10. **`.github/PULL_REQUEST_TEMPLATE.md`** - PR template

### **Automation & CI/CD**
11. **`.github/workflows/ci.yml`** - Build, test, lint workflow with dynamic versioning
12. **`.github/workflows/release.yml`** - Release automation (optional)
13. **`.github/dependabot.yml`** - Automated dependency updates
14. **Updated Dockerfile** - With `ARG VERSION` and `ENV VERSION` support

### **Security**
14. **`SECURITY.md`** - Security policy and vulnerability reporting
15. **Security scan report** - Results from secrets scanning
16. **Dependency audit report** - Vulnerability assessment

### **Documentation**
17. **`/docs/` structure** - Additional documentation organized
18. **API documentation** - If applicable (OpenAPI, etc.)
19. **Architecture diagrams** - If applicable

### **Documentation Updates**
All GitHub preparation work must be documented in `/docs/`:

- **`/docs/README.md`**: Update with repository setup instructions, contribution workflow, and links to new community files
- **`/docs/PROJECT_OVERVIEW.md`**: Add GitHub visibility status, community guidelines, release strategy, and distribution channels
- **`/docs/SECURITY_AND_PRIVACY.md`**: Document security policies, vulnerability reporting process, secrets management, and GitHub security features enabled
- **`/docs/ROADMAP.md`**: Include release schedule, versioning strategy, planned GitHub integrations, and community engagement plans

---

## **Success Criteria**

- [ ] All critical files present (`.gitignore`, `LICENSE`, `README.md`, dependencies)
- [ ] Folder structure organized and logical
- [ ] No secrets or credentials in repository history
- [ ] Dependencies properly managed and locked
- [ ] **`get_version.sh` script created and executable** (`chmod +x get_version.sh`)
- [ ] **Dynamic versioning working**: Script generates correct version strings
- [ ] **Dockerfile updated** with `ARG VERSION` and `ENV VERSION`
- [ ] **Application reads VERSION** from environment variable with fallback
- [ ] **Version displayed at startup** in application logs
- [ ] **CI/CD uses `fetch-depth: 0`** for full Git history (required for tags)
- [ ] **CI/CD runs `get_version.sh`** and passes VERSION to Docker build
- [ ] Tests exist and run successfully
- [ ] CI/CD workflow configured and passing
- [ ] README comprehensive with badges and examples
- [ ] Contributing and community guidelines established
- [ ] Security scanning enabled (Dependabot, secret scanning)
- [ ] Release strategy defined with semantic versioning and dynamic versioning
- [ ] GitHub topics and metadata configured
- [ ] Project can be cloned and run by anyone without guidance
- [ ] All builds pass, tests pass, linting passes
- [ ] Documentation synchronized with code
- [ ] **`/docs/` files updated** with GitHub setup, versioning strategy, and policies

---

## **Best Practices**

### **Repository Hygiene**
- Keep repository root clean (move configs to dedicated folders)
- Use consistent naming conventions (kebab-case for files)
- Delete unused files and branches
- Keep commit history clean and meaningful
- Use conventional commits (feat:, fix:, docs:, etc.)

### **Documentation Excellence**
- Write README for newcomers, not experts
- Provide runnable examples in documentation
- Keep documentation synchronized with code
- Use diagrams and visuals where helpful
- Document breaking changes prominently

### **Security First**
- Never commit secrets (scan history before first push)
- Use environment variables for all credentials
- Enable branch protection rules
- Require PR reviews for main branch
- Use signed commits (optional but recommended)

### **Automation Strategy**
- Automate everything that can be automated
- Fail fast (run quick checks before slow ones)
- Cache dependencies in CI to speed up builds
- Use matrix strategies for multi-platform testing
- Keep CI workflows simple and maintainable

### **Community Building**
- Respond to issues and PRs promptly
- Be welcoming to first-time contributors
- Document decision-making process
- Use GitHub Discussions for Q&A
- Celebrate contributions and milestones

### **Release Management**
- Use semantic versioning consistently
- Write clear, user-focused release notes
- Tag all releases properly
- Maintain changelog discipline
- Consider pre-releases for testing (beta, rc)

---

## **Usage Instructions**

### **When to Run This Preparation**

* Before first public push to GitHub
* When converting private repo to public
* Before submitting to showcases or job applications
* When preparing for open source release
* During project audits or quality reviews
* Before major version releases (v1.0, v2.0)

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Ensure you have a clean working directory (commit or stash changes)
3. Backup your repository before making structural changes
4. Have GitHub account and repository URL ready
5. Know your preferred license (MIT, Apache-2.0, GPL, etc.)

### **Execution**
```
I need to prepare my project for GitHub publication.

Project name: [name]
Project type: [library/CLI/web app/API/Docker image/etc.]
Programming language: [JavaScript/Python/Java/Go/Rust/etc.]
Current status: [new project/existing private repo/needs cleanup]
License preference: [MIT/Apache-2.0/GPL/other]
CI/CD platform: [GitHub Actions/GitLab CI/other]
Docker publishing: [yes/no]
Target audience: [developers/DevOps/end-users/etc.]
Special considerations: [AI integration/MCP/sensitive data/etc.]
```

### **Expected Outcome**
The AI will analyze your project structure, create or update all essential files (`.gitignore`, `LICENSE`, `README.md`, `CONTRIBUTING.md`, etc.), scan for and report any secrets or security issues, set up CI/CD workflows for automated testing and releases, organize folder structure following best practices, create issue and PR templates, configure Dependabot for security updates, generate comprehensive documentation, add appropriate badges and metadata, and ensure the project is ready for professional GitHub publication. You'll receive a completely GitHub-ready repository that anyone can clone, understand, run, and contribute to without external guidance.

---

## **GitHub Ready Assessment Report**

After running this prompt, you'll receive a detailed report:

### **Readiness Score**: X/100

**Critical Issues** (Must Fix):
- [ ] Missing LICENSE file
- [ ] Secrets found in repository
- [ ] No README.md

**Recommended Improvements**:
- [ ] Add CI/CD workflow
- [ ] Create CONTRIBUTING.md
- [ ] Set up Dependabot

**Optional Enhancements**:
- [ ] Add project screenshots
- [ ] Create CHANGELOG.md
- [ ] Set up release automation

### **Next Steps**:
1. Fix critical issues immediately
2. Implement recommended improvements
3. Consider optional enhancements
4. Review generated files and customize
5. Test the complete workflow (clone → build → run → test)
6. Push to GitHub and verify all workflows pass
