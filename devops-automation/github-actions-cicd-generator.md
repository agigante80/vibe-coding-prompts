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

### 4. **Docker Image Tagging & Publishing**

* Tag dynamically:
  * `main` → `latest-<short_commit>`
  * `develop` → `development-<short_commit>`

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

### **Configuration Documentation**
2. Documentation of required secrets and setup (GitHub Secrets, Docker Hub tokens)
3. Environment variables and configuration guide
4. Manual workflow dispatch usage examples
5. Troubleshooting guide for common issues

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
- [ ] Docker images successfully published to Docker Hub and GHCR
- [ ] Short description validation prevents >100 character descriptions
- [ ] Security scans upload SARIF to GitHub Security tab
- [ ] Automated releases created with semantic versioning
- [ ] Manual workflow dispatch works with all input parameters
- [ ] Secrets properly configured and secured
- [ ] Workflow completes within reasonable timeframe (<10 minutes)
- [ ] **`/docs/` files updated** with CI/CD configuration and procedures

---

## 🔹 **Best Practices**

### **Modular Job Design**
- Separate concerns into distinct jobs (lint, test, build, deploy)
- Use job dependencies to control execution order
- Implement parallel execution where possible
- Share artifacts between jobs efficiently

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

### **Fail Fast, Fail Clearly**
- Run fast checks (lint) before slow ones (integration tests)
- Provide clear error messages in workflow output
- Set appropriate timeouts for all jobs
- Implement proper cleanup on failure

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