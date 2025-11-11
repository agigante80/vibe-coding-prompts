# Security Prompts

This folder contains prompts focused on security auditing, vulnerability assessment, and compliance validation.

## Available Prompts

### 🔐 Security Audit Generator
**File**: `security-audit-generator.md`

**Purpose**: Performs comprehensive security audit identifying vulnerabilities, misconfigurations, and compliance gaps.

### 📦 Dependency Update Manager
**File**: `dependency-update-manager.md`

**Purpose**: Automates dependency updates with intelligent breaking change detection and safe rollback mechanisms.

**Key Features**:
- Multi-framework vulnerability detection (OWASP Top 10, CIS Benchmarks)
- Authentication and authorization review
- Input validation and injection testing
- Dependency vulnerability scanning
- Container and infrastructure security
- Code pattern analysis for dangerous operations
- Automated scanning tool integration
- CVSS-based risk scoring

**Security Coverage**:
- **Authentication & Authorization**: Password policies, MFA, session management, access controls
- **Input Validation**: SQL injection, XSS, command injection, SSRF, deserialization
- **Web Security**: Headers, CORS, CSRF protection, content security policies
- **Data Protection**: Encryption, PII handling, GDPR/HIPAA/PCI-DSS compliance
- **Dependencies**: CVE scanning, outdated packages, supply chain security
- **Configuration**: Secrets management, debug modes, exposed services
- **Infrastructure**: Container security, Kubernetes policies, cloud configurations

**Best For**:
- Pre-production security assessments
- Quarterly security review cycles
- Compliance audit preparation (GDPR, HIPAA, PCI-DSS)
- Post-incident security reviews
- Baseline security for new projects
- Penetration testing preparation
- Security-focused code reviews

**Usage Tips**:
- Run automated scans first to identify obvious issues
- Review manual testing checklist thoroughly
- Prioritize critical and high severity findings
- Integrate security scanning into CI/CD pipeline
- Document remediation progress and timeline
- ✅ **Platform-friendly**: At ~1286 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

---

**Key Features**:
- Multi-ecosystem support (npm, pip, Maven, Cargo, Bundler, Composer)
- Security vulnerability scanning with CVSS scoring
- Breaking change detection and analysis
- Automated testing workflow
- Smart update batching and prioritization
- Dependabot and Renovate configuration
- Safe rollback mechanisms

**Update Management**:
- **Security Patches**: Immediate priority with automated scanning
- **Major Updates**: Breaking change analysis and migration guides
- **Minor/Patch**: Batched updates with automated testing
- **Dev Dependencies**: Separate workflow from production

**Best For**:
- Setting up automated dependency management
- Responding to security vulnerabilities (CVEs)
- Major version upgrade planning
- Reducing technical debt from outdated packages
- Establishing regular update cycles
- CI/CD integration for dependency checks
- Teams wanting automated, safe updates

**Usage Tips**:
- Start with security updates first
- Test major updates individually
- Batch minor/patch updates together
- Use Dependabot or Renovate for automation
- Monitor bundle size impact
- Keep lock files in version control
- ✅ **Platform-friendly**: At ~1630 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

## When to Use Security Prompts

Use these prompts when:
- Preparing for production deployment
- Conducting regular security assessments
- Responding to security incidents
- Meeting compliance requirements
- Onboarding security practices to teams
- Auditing third-party integrations
- Implementing security-first development

## Integration with Other Prompts

Security prompts work well with:
- **DevOps Automation**: Add security scanning to CI/CD pipelines
- **Project Management**: Include security audits in project assessments
- **Development Workflow**: Integrate security testing into development process
- **Documentation**: Document security policies and procedures

## Tools Referenced

The prompts in this folder reference these security tools:
- **Vulnerability Scanning**: Trivy, Snyk, npm audit, pip-audit
- **SAST**: Semgrep, SonarQube, Bandit, ESLint security plugins
- **Secret Scanning**: Gitleaks, TruffleHog, git-secrets
- **Infrastructure**: Checkov, tfsec, kube-bench
- **Dependency Check**: OWASP Dependency-Check, Safety, Cargo audit

## Security Standards

Prompts align with industry standards:
- **OWASP Top 10** - Web application security risks
- **OWASP API Security** - API-specific vulnerabilities
- **OWASP Mobile** - Mobile application security
- **CIS Benchmarks** - Infrastructure and container security
- **NIST Cybersecurity Framework** - Security program structure
- **GDPR, HIPAA, PCI-DSS** - Compliance requirements