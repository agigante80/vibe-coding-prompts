# GitHub Actions CI/CD Workflow Generator

## **Objective**

Analyze this repository and determine whether it already includes a GitHub Actions workflow for CI/CD (e.g., `.github/workflows/ci-cd.yml`).

If a workflow exists → **review, improve, and modernize it** to meet all the requirements below.

If it doesn't exist → **create a complete, fully functional `.github/workflows/ci-cd.yml`** that implements all these requirements from scratch.

The resulting workflow must automatically adapt to the project's language, framework, and structure, and must be **modular, fast, secure, maintainable, and manually runnable**.

It must also include **Docker Hub and GHCR publishing**, **short Docker description validation**, **Docker test builds**, **automatic releases**, and **SARIF-based security scanning**.

---

## 🔹 Behavior

* If `.github/workflows/ci-cd.yml` **exists**:
  * Parse and review the YAML.
  * Improve naming, structure, and modularity.
  * Add any missing jobs or steps required by this specification.
  * Upgrade for better caching, parallelism, and security.
  * Ensure compliance with Docker Hub + GHCR requirements.
  * Maintain existing logic and environment-specific details.

* If no CI/CD workflow exists:
  * Generate a new one implementing all the below requirements.

---

## 🔹 General Requirements

The workflow must be:

* **Modular** → Reusable, logically separated jobs (`lint`, `test`, `build`, `validate-short-description`, `docker-test`, `docker-publish`, `security-scan`, `deployment-test`, `release`).
* **Fast** → Use caching, parallel jobs, and artifact reuse.
* **Secure** → Handle secrets properly, perform security scans, and use least privileges.
* **Maintainable** → Clearly structured, commented, minimal duplication.
* **Manually Runnable** → Triggerable via `workflow_dispatch` with input parameters.

---

## 🔹 Functional Requirements

### 1. **Auto-Detect Project Type**

* Detect main language/toolchain from files like `package.json`, `requirements.txt`, `pom.xml`, `Cargo.toml`, etc.
* Automatically configure lint, test, and build commands.

### 2. **Pipeline Stages**

* **Lint** → Run static analysis and format checks.
* **Test** → Execute unit/integration tests.
* **Build** → Compile or bundle code.
* **Validate Short Description** → Ensure `./docker/description/short.md` has **≤100 characters**; fail workflow if exceeded.
* **Docker Test Build** → Perform a **local test build** of the Docker image before pushing:
  * Build without publishing to validate Dockerfile correctness.
  * Use cached layers.
  * Fail immediately on build errors.
  * Print resulting image size.
* **Docker Publish** → Build and publish Docker image(s) to both:
  1. **Docker Hub**
  2. **GitHub Container Registry (GHCR)**
* **Security Scan** → Scan image and dependencies (`trivy`, `npm audit`, etc.), upload SARIF to GitHub Security tab.
* **Deployment Test** → Validate deployment manifests (`docker-compose.yml`, Helm, K8s, etc.).
* **Release** → Update Docker Hub descriptions (via API) and create a GitHub Release with semantic versioning.

### 3. **Manual and Automatic Triggers**

```yaml
on:
  push:
    branches: [main, develop]
  workflow_dispatch:
```

* Support manual triggers with optional inputs (branch, release type, notes, etc.).

### 4. **Dynamic Versioning System**

Implement Git-based dynamic versioning that generates context-aware version strings:

**Version Format:**
```
<base_version>-<context>-<commit>
```

**Examples:**
- Main branch with tag: `1.0.0`
- Main branch, no tag: `0.1.0-main-71f02b6`
- Develop branch: `0.1.0-dev-71f02b6`
- Feature branch: `0.1.0-feature-auth-71f02b6`

**Requirements:**
* Create `get_version.sh` script that:
  - Reads base version from `package.json` or equivalent
  - Uses Git commands to determine branch, commit, and tags
  - Generates version string based on context
  - Falls back gracefully when Git unavailable
  - Sanitizes branch names (replace special chars with `-`)
* Workflow must:
  - Checkout with `fetch-depth: 0` (full Git history for tags)
  - Run `get_version.sh` early in pipeline
  - Store version as job output for downstream jobs
  - Pass VERSION to Docker build as `--build-arg`
* Dockerfile must:
  - Accept `ARG VERSION=unknown`
  - Set `ENV VERSION=${VERSION}`
* Application must:
  - Read VERSION from environment variable
  - Fall back to package.json if env var not set
  - Display version in logs at startup
  - Expose version in health/info endpoint
* Docker images must:
  - Include version in OCI labels (`org.opencontainers.image.version`)
  - Tag images with generated version

**get_version.sh Template:**
```bash
#!/bin/bash
set -e

BASE_VERSION=$(node -p "require('./package.json').version" 2>/dev/null || echo "0.1.0")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
TAG=$(git describe --exact-match --tags 2>/dev/null || echo "")

if [ "$BRANCH" = "main" ] && [ -n "$TAG" ]; then
    VERSION="$TAG"
elif [ "$BRANCH" = "main" ]; then
    VERSION="${BASE_VERSION}-main-${COMMIT}"
elif [ "$BRANCH" = "develop" ]; then
    VERSION="${BASE_VERSION}-dev-${COMMIT}"
else
    SANITIZED_BRANCH=$(echo "$BRANCH" | sed 's/[^a-zA-Z0-9._-]/-/g')
    VERSION="${BASE_VERSION}-${SANITIZED_BRANCH}-${COMMIT}"
fi

echo "$VERSION"
```

**CI/CD Integration:**
```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for full Git history

      - name: Generate dynamic version
        id: version
        run: |
          chmod +x get_version.sh
          VERSION=$(bash get_version.sh)
          echo "version=$VERSION" >> $GITHUB_OUTPUT
          echo "📦 Version: $VERSION"
```

### 5. **Docker Image Tagging & Publishing**

* Tag dynamically using generated version:
  * Tagged main: `1.0.0`, `latest`
  * Untagged main: `0.1.0-main-abc1234`, `latest`
  * Develop: `0.1.0-dev-abc1234`, `develop`
  * Feature: `0.1.0-feature-name-abc1234`

* Authenticate and push to both registries:

```yaml
env:
  DOCKERHUB_USER: ${{ secrets.DOCKER_USERNAME }}
  DOCKERHUB_TOKEN: ${{ secrets.DOCKER_TOKEN }}
  GHCR_USER: ${{ github.actor }}
  GHCR_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Authenticate securely:

```bash
echo "${DOCKERHUB_TOKEN}" | docker login -u "${DOCKERHUB_USER}" --password-stdin docker.io
echo "${GHCR_TOKEN}" | docker login ghcr.io -u "${GHCR_USER}" --password-stdin
```

### 5. **Security Scanning**

* Use `trivy` for container vulnerability scanning
* Upload results as SARIF to GitHub Security tab
* Fail on high/critical vulnerabilities (configurable threshold)

### 6. **Release Automation**

* Automatically create GitHub releases on main branch
* Use semantic versioning based on commit messages
* Update Docker Hub repository descriptions via API

---

## 🔹 Implementation Notes

* Use GitHub Actions marketplace actions where appropriate
* Implement proper error handling and cleanup
* Cache dependencies aggressively for speed
* Use matrix strategies for multi-platform builds when needed
* Include comprehensive logging and debugging output
* Ensure all secrets are properly secured and scoped

---

## 🔹 **Deliverables**

### **CI/CD Workflow Files**
1. Complete `.github/workflows/ci-cd.yml` file with all required jobs
2. Additional workflow files for releases, security scans, etc.
3. Reusable workflow templates for common tasks
4. Workflow documentation in repository

### **Dynamic Versioning Implementation**
2. **`get_version.sh`** script with executable permissions
3. Updated Dockerfile with `ARG VERSION` and `ENV VERSION`
4. Application code reading VERSION from environment
5. Version display in application logs at startup
6. Version exposed in health/info endpoint
7. Docker image labels with OCI version metadata

### **Configuration Documentation**
8. Documentation of required secrets and setup (GitHub Secrets, Docker Hub tokens)
9. Environment variables and configuration guide
10. Manual workflow dispatch usage examples
11. Troubleshooting guide for common issues
12. Version format documentation and examples

### **Security Integration**
6. SARIF security scan configuration
7. Vulnerability scanning setup (Trivy, etc.)
8. Secret scanning pre-commit hooks
9. Security policy documentation

### **Documentation Updates**
All CI/CD setup and workflow configurations must be documented in `/docs/`:

- **`/docs/ARCHITECTURE.md`**: Add CI/CD pipeline architecture, job dependencies, deployment flow, and infrastructure integration points
- **`/docs/TESTING_AND_RELIABILITY.md`**: Document automated testing in CI/CD, quality gates, test execution strategy, and reliability metrics
- **`/docs/SECURITY_AND_PRIVACY.md`**: Add security scanning configuration, SARIF integration, vulnerability thresholds, and incident response for security findings
- **`/docs/README.md`**: Update with CI/CD status badges, how to trigger workflows manually, and links to pipeline documentation

---

## 🔹 **Success Criteria**

- [ ] CI/CD workflow executes successfully on push and manual trigger
- [ ] All quality gates (lint, test, build) pass before deployment
- [ ] **Dynamic versioning working**: `get_version.sh` generates correct version strings
- [ ] **Full Git history available**: Workflow uses `fetch-depth: 0`
- [ ] **VERSION passed to Docker build**: `--build-arg VERSION=$VERSION`
- [ ] **VERSION in Docker environment**: `docker run --rm image env | grep VERSION` shows correct value
- [ ] **Version in OCI labels**: `docker inspect image | jq '.[0].Config.Labels."org.opencontainers.image.version"'`
- [ ] Docker images successfully published to Docker Hub and GHCR with version tags
- [ ] Short description validation prevents >100 character descriptions
- [ ] Security scans upload SARIF to GitHub Security tab
- [ ] Automated releases created with semantic versioning
- [ ] Manual workflow dispatch works with all input parameters
- [ ] Secrets properly configured and secured
- [ ] **Application displays version at startup** in logs
- [ ] **Health endpoint exposes version** (e.g., `/health` returns `{"version":"0.1.0-dev-abc1234"}`)
- [ ] Workflow completes within reasonable timeframe (<10 minutes)
- [ ] **`/docs/` files updated** with CI/CD configuration, versioning strategy, and procedures

---

## 🔹 **Best Practices**

### **Dynamic Versioning**
- **Always use `fetch-depth: 0`** in checkout to get full Git history (required for tags)
- **Make `get_version.sh` executable** and commit: `chmod +x get_version.sh && git add get_version.sh`
- **Handle missing Git gracefully** with fallbacks: `git rev-parse HEAD 2>/dev/null || echo "unknown"`
- **Sanitize branch names** to remove special characters: `sed 's/[^a-zA-Z0-9._-]/-/g'`
- **Use short commit hashes** (7 chars): `git rev-parse --short HEAD`
- **Don't hardcode versions** in Dockerfile - use ARG/ENV pattern
- **Display version prominently** at application startup
- **Include version in Docker labels** following OCI spec
- **Test version generation locally** before pushing: `./get_version.sh`

### **Modular Job Design**
- Separate concerns into distinct jobs (version, lint, test, build, deploy)
- Use job dependencies to control execution order
- Implement parallel execution where possible
- Share artifacts between jobs efficiently
- Pass version as job output to downstream jobs

### **Caching Strategy**
- Cache dependencies aggressively (npm, pip, cargo, etc.)
- Use action-specific caching (actions/cache, actions/setup-node)
- Invalidate caches on lock file changes
- Monitor cache hit rates and adjust

### **Security First**
- Never expose secrets in logs or outputs
- Use GitHub's secret masking
- Implement least privilege for tokens
- Rotate secrets regularly
- Use OIDC for cloud provider authentication when possible
- **Don't include sensitive info in version strings** (no private branch names or secrets)

### **Fail Fast, Fail Clearly**
- Run fast checks (lint, version) before slow ones (integration tests)
- Provide clear error messages in workflow output
- Set appropriate timeouts for all jobs
- Implement proper cleanup on failure
- **Don't fail builds on version generation errors** - use fallbacks

---

## 🔹 **Usage Instructions**

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine existing `/docs/` files to understand current project state
3. Check if `.github/workflows/ci-cd.yml` exists (will improve if present, create if absent)
4. Ensure Docker Hub credentials are available for container registry setup

### **Execution**
```
I need a GitHub Actions CI/CD workflow for my [PROJECT_TYPE] project.

Project language: [Node.js/Python/Java/Go/Rust/etc.]
Docker Hub repository: [username/repo-name]
Deployment target: [Docker Hub, GHCR, both]
Security requirements: [SARIF scanning, Trivy, etc.]
Release strategy: [semantic versioning, manual, automated]
```

### **Expected Outcome**
The AI will analyze your project structure, create or improve the CI/CD workflow with all required jobs (lint, test, build, Docker publish, security scan, release), configure proper caching and parallelization, set up security scanning with SARIF integration, and document everything in `/docs/` files. You'll receive a production-ready workflow that runs automatically on push and can be triggered manually.