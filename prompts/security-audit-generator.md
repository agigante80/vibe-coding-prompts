# Security Audit Generator

## **Objective**

Perform a comprehensive security audit of the current project, identifying vulnerabilities, security misconfigurations, and compliance gaps with actionable remediation steps.

---

## **Assessment Scope**

### 1. **Project Discovery**

* Detect project type, language, and framework
* Identify web frameworks, APIs, and external integrations
* Catalog dependencies and third-party libraries
* Map authentication and authorization mechanisms
* Identify data storage and sensitive information handling
* Review deployment architecture and infrastructure

### 2. **Security Standards**

Apply appropriate security standards based on project type:

| Project Type | Primary Standards | Key Focus Areas |
|-------------|------------------|-----------------|
| **Web Applications** | OWASP Top 10, CSP | XSS, CSRF, injection attacks, session management |
| **APIs** | OWASP API Security | Authentication, rate limiting, input validation |
| **Mobile Apps** | OWASP Mobile | Data storage, network security, code obfuscation |
| **Cloud Services** | CIS Benchmarks | IAM, encryption, network security, logging |
| **Containers** | CIS Docker/K8s | Image security, runtime protection, secrets |

---

## **Security Audit Areas**

### 🔐 **Authentication & Authorization**

**Check for**:
- Weak password policies (length, complexity, rotation)
- Missing multi-factor authentication (MFA)
- Insecure session management and token handling
- Improper access controls and privilege escalation risks
- Hard-coded credentials in code or configuration
- OAuth/SAML misconfigurations
- JWT vulnerabilities (weak signing, no expiration)

**Scan**:
```bash
# Common patterns to search
grep -r "password\|secret\|api_key\|token" --include="*.{js,py,java,env}"
grep -r "admin\|root" --include="*.config"
```

### 🛡️ **Input Validation & Injection**

**Check for**:
- SQL injection vulnerabilities (raw queries, string concatenation)
- Command injection risks (shell execution, eval)
- Path traversal vulnerabilities
- XML/XXE injection
- LDAP/NoSQL injection
- Server-Side Request Forgery (SSRF)
- Deserialization vulnerabilities

**Validate**:
- All user inputs are sanitized and validated
- Parameterized queries/prepared statements used
- ORM properly configured
- File upload restrictions (type, size, location)

### 🌐 **Web Security Headers**

**Required headers**:
```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

### 🔒 **Data Protection**

**Check for**:
- Sensitive data transmitted without encryption (use HTTPS everywhere)
- Weak encryption algorithms (MD5, SHA1, DES)
- Insecure data storage (plaintext passwords, unencrypted databases)
- Missing encryption at rest for sensitive data
- Insufficient logging and monitoring of data access
- Personal Identifiable Information (PII) exposure
- Missing data retention and deletion policies

**Compliance checks**:
- GDPR: Right to erasure, data portability, consent
- HIPAA: PHI encryption, access logs, audit trails
- PCI-DSS: Credit card data handling, network segmentation

### 📦 **Dependencies & Supply Chain**

**Audit**:
- Known vulnerabilities in dependencies (CVEs)
- Outdated packages with security patches available
- Deprecated or unmaintained libraries
- Excessive permissions in dependencies
- Typosquatting risks in package names
- Missing Software Bill of Materials (SBOM)

**Tools to use**:
```bash
# Node.js
npm audit --production
npm outdated

# Python
pip-audit
safety check

# Java
mvn dependency-check:check

# Go
go list -json -m all | nancy sleuth

# Rust
cargo audit
```

### ⚙️ **Configuration & Secrets**

**Check for**:
- Debug mode enabled in production
- Verbose error messages exposing internal details
- Default credentials not changed
- Secrets in version control (.env files, config files)
- Insecure CORS policies (wildcard origins)
- Missing rate limiting and throttling
- Exposed admin panels or debug endpoints
- Unnecessary services or ports exposed

**Best practices**:
- Use environment variables or secret management (Vault, AWS Secrets Manager)
- Implement .gitignore for sensitive files
- Rotate secrets regularly
- Use least privilege principle

### 🐳 **Container & Infrastructure**

**Check for**:
- Running containers as root user
- Using outdated or vulnerable base images
- Exposed Docker daemon or Kubernetes API
- Missing network policies and segmentation
- Secrets in Dockerfiles or environment variables
- Insufficient resource limits (CPU, memory)
- Missing security scanning in CI/CD pipeline

**Best practices**:
- Use minimal base images (Alpine, distroless)
- Scan images with Trivy, Clair, or Snyk
- Implement pod security policies
- Use secrets management (Kubernetes secrets, sealed secrets)

### 🔍 **Code Security Patterns**

**Scan for dangerous patterns**:
```python
# Python
eval(), exec(), compile()
pickle.loads() # Deserialization
os.system(), subprocess with shell=True

# JavaScript
eval(), Function constructor
innerHTML without sanitization
document.write() with user input

# Java
Runtime.exec()
ObjectInputStream deserialization
SQL string concatenation
```

**Static Analysis Tools**:
- **Python**: bandit, safety
- **JavaScript**: ESLint security plugins, npm audit
- **Java**: SpotBugs, FindSecBugs
- **Go**: gosec
- **Rust**: cargo-audit
- **Multi-language**: SonarQube, Semgrep

---

## **Vulnerability Scanning**

### **Automated Scans**

Run comprehensive security scans:

```bash
# Container scanning
trivy image your-image:tag --severity HIGH,CRITICAL

# Dependency scanning
snyk test --severity-threshold=high

# SAST (Static Application Security Testing)
semgrep --config=auto

# Secret scanning
gitleaks detect --source . --verbose

# Infrastructure as Code
checkov -d .
tfsec .
```

### **Manual Testing Checklist**

- [ ] Test authentication bypass attempts
- [ ] Verify authorization on all endpoints
- [ ] Test input validation with malicious payloads
- [ ] Check for CSRF protection on state-changing operations
- [ ] Verify session timeout and logout functionality
- [ ] Test file upload for malicious content
- [ ] Attempt privilege escalation
- [ ] Test API rate limiting and throttling
- [ ] Verify error handling doesn't leak information

---

## **Deliverables**

Generate the following:

1. **Security Audit Report**:
   * Executive summary with risk scores
   * Detailed vulnerability findings categorized by severity
   * CVSS scores for each vulnerability
   * Affected components and attack vectors
   * Exploitability assessment

2. **Remediation Plan**:
   * Prioritized action items (Critical → High → Medium → Low)
   * Specific fix recommendations with code examples
   * Estimated effort and timeline for each fix
   * Quick wins vs. long-term improvements

3. **Security Tooling Setup**:
   * Pre-commit hooks for secret scanning
   * CI/CD security scanning integration
   * Dependency update automation
   * Security monitoring and alerting

4. **Compliance Checklist**:
   * OWASP Top 10 compliance status
   * Industry-specific compliance (GDPR, HIPAA, PCI-DSS)
   * Gap analysis and recommendations

5. **Security Documentation**:
   * Security policies and procedures
   * Incident response plan
   * Secure coding guidelines
   * Security testing procedures

### **Documentation Updates**
All security audit findings and remediation plans must be documented in `/docs/`:

- **`/docs/SECURITY_AND_PRIVACY.md`**: Add discovered vulnerabilities, security policies, data handling procedures, incident response plan, and compliance status
- **`/docs/IMPROVEMENT_AREAS.md`**: Document security technical debt, vulnerabilities requiring long-term fixes, and security enhancement opportunities
- **`/docs/REFACTORING_PLAN.md`**: Add security remediation tasks with priority, effort estimates, and dependencies
- **`/docs/TESTING_AND_RELIABILITY.md`**: Include security testing procedures, vulnerability scanning setup, and security quality gates

---

## **Risk Scoring**

Classify vulnerabilities by severity:

| Severity | CVSS Score | Response Time | Examples |
|----------|-----------|---------------|----------|
| **Critical** | 9.0-10.0 | Immediate | RCE, authentication bypass, data breach |
| **High** | 7.0-8.9 | 24-48 hours | Privilege escalation, SQL injection |
| **Medium** | 4.0-6.9 | 1-2 weeks | XSS, CSRF, weak encryption |
| **Low** | 0.1-3.9 | Next sprint | Information disclosure, missing headers |

---

## **Success Criteria**

- [ ] All critical and high vulnerabilities identified and documented
- [ ] Remediation plan with specific, actionable steps and timelines
- [ ] Security scanning integrated into CI/CD pipeline
- [ ] No secrets or credentials in version control
- [ ] Dependencies updated to patched versions (CVEs resolved)
- [ ] Security headers properly configured and tested
- [ ] Automated security testing in place (pre-commit and CI/CD)
- [ ] Compliance requirements met (OWASP, GDPR, etc.)
- [ ] Incident response plan documented and tested
- [ ] **`/docs/` files updated** with security findings and procedures

---

## **Best Practices**

### **Preventive Measures**

* Implement security from the start (shift-left security)
* Use security linters and automated scanning
* Regular dependency updates and patch management
* Security training for development team
* Code review focusing on security concerns
* Threat modeling for new features

### **Continuous Security**

* Schedule regular security audits (quarterly)
* Monitor security advisories for dependencies
* Implement security incident response procedures
* Maintain security changelog
* Perform penetration testing before major releases
* Bug bounty program for external security research

---

## **Usage Instructions**

### **When to Run This Audit**

* Starting a new project (baseline security assessment)
* Before production deployment or major releases
* After security incidents or breach attempts
* Quarterly security review cycles
* Compliance audit requirements
* After major dependency updates
* When adding authentication or payment processing

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine existing `/docs/SECURITY_AND_PRIVACY.md` if it exists
3. Ensure security scanning tools are available (or will be recommended)
4. Have access to dependency management tools for your project

### **Execution**
```
I need a comprehensive security audit for my [PROJECT_TYPE].

Project type: [web app/API/mobile app/cloud service/etc.]
Technology stack: [Node.js, Python, Java, etc.]
Authentication: [OAuth, JWT, session-based, none]
Data sensitivity: [PII, financial, healthcare, public]
Compliance requirements: [GDPR, HIPAA, PCI-DSS, SOC2, none]
Current security measures: [describe existing security if any]
```

### **Expected Outcome**
The AI will perform a comprehensive security analysis using OWASP Top 10 and industry best practices, scan for vulnerabilities in code and dependencies, check for security misconfigurations, analyze authentication and authorization mechanisms, generate a detailed security audit report with CVSS-scored vulnerabilities, provide a prioritized remediation plan with specific fix recommendations, set up automated security scanning in CI/CD, and document all findings and procedures in `/docs/` files. You'll receive a complete security assessment with actionable steps to improve your security posture.
* Adding new features or integrations
* Onboarding security-focused team members