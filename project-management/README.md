# Project Management Prompts

This folder contains prompts for project assessment, planning, and coordination activities.

## Available Prompts

### 📊 Project Reassessment & Synchronization
**File**: `project-reassessment.md`

**Purpose**: Performs comprehensive project analysis to ensure alignment between code, documentation, and policies.

### 🚀 GitHub Ready Preparation
**File**: `github-ready-preparation.md`

**Purpose**: Prepares projects for professional GitHub publication with proper structure, documentation, automation, security, and community guidelines.

**Key Features**:
- Complete codebase and documentation analysis
- Cross-verification of architecture, dependencies, and features
- Identification of inconsistencies and gaps
- Automated documentation synchronization
- Quality assurance through testing and security checks
- Detailed reporting with actionable next steps

**Assessment Areas**:
- **Code Analysis**: Structure, quality, and adherence to standards
- **Documentation Review**: Completeness and accuracy vs. implementation
- **Dependency Audit**: Current versions, security, and compatibility
- **Test Coverage**: Gaps and reliability assessment  
- **Security Posture**: Vulnerability analysis and compliance
- **Configuration**: Environment setup and deployment readiness

**Best For**:
- Taking over existing projects
- Periodic project health checks
- Pre-release quality assurance
- Post-migration validation
- Team onboarding and knowledge transfer
- Compliance audits and assessments

**Usage Tips**:
- Run this assessment before major releases or handovers
- Use results to prioritize technical debt and improvements
- Schedule regular assessments (monthly/quarterly) for ongoing projects
- Ensure all team members understand the compliance requirements

**Key Features**:
- Comprehensive 10-category GitHub readiness checklist
- Essential files creation (LICENSE, .gitignore, README, CONTRIBUTING, etc.)
- CI/CD workflow setup (GitHub Actions)
- Security scanning and secrets detection
- Community guidelines and templates (issues, PRs, Code of Conduct)
- Dependency management and Dependabot configuration
- Release automation and semantic versioning
- Repository metadata and visibility optimization
- Folder structure organization
- GitHub-specific best practices

**Readiness Categories**:
- **Project Fundamentals**: Structure, dependencies, essential files
- **Build & Run**: Installation, build scripts, Docker setup
- **Testing**: Automated tests, coverage, CI integration
- **Automation/CI-CD**: GitHub Actions, releases, security scans
- **Documentation**: README, guides, API docs
- **Community**: Contributing guidelines, templates, Code of Conduct
- **Security**: Secret scanning, .env setup, vulnerability management
- **Releases**: Versioning, changelogs, distribution
- **Metadata**: Topics, badges, descriptions, screenshots
- **AI Integration** (optional): MCP, agent docs, security boundaries

**Best For**:
- First public GitHub release
- Converting private to public repositories
- Open source project preparation
- Portfolio and job application projects
- Professional project presentation
- Community contribution setup
- Pre-release security and quality audits

**Usage Tips**:
- Run before first public push to avoid exposing secrets
- Back up repository before structural changes
- Review generated files and customize for your context
- Test complete workflow (clone → build → run → test) before pushing
- Enable GitHub features (Dependabot, secret scanning) after push
- ✅ **Platform-friendly**: At ~2610 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

## When to Use Project Management Prompts

Use these prompts when:
- Starting work on an inherited or existing project
- Conducting periodic project health evaluations
- Preparing for major releases or deployments
- Onboarding new team members to a project
- Auditing compliance with organizational standards
- Planning resource allocation and sprint priorities

## Integration with Other Prompts

Project management prompts work well with:
- **Documentation**: Use assessment results to guide documentation improvements
- **DevOps Automation**: Validate CI/CD pipeline effectiveness
- **Development Workflow**: Inform process improvements based on assessment findings

## Assessment Methodology

The reassessment process follows this structure:
1. **Discovery**: Automated analysis of project structure and dependencies
2. **Verification**: Cross-checking implementation against documentation
3. **Testing**: Validation of all quality gates and standards
4. **Reporting**: Generation of detailed findings and recommendations
5. **Planning**: Prioritized action items for improvement

## Quality Gates

Project assessments enforce these standards:
- All tests must pass before proceeding
- Security scans must show no critical vulnerabilities
- Documentation must be synchronized with current code
- Code coverage must meet minimum thresholds
- Performance benchmarks must be satisfied

## Deliverables

Each assessment produces:
- **Status Report**: Current project health and compliance
- **Gap Analysis**: Missing or outdated components
- **Action Plan**: Prioritized improvement recommendations
- **Risk Assessment**: Potential issues and mitigation strategies
- **Next Steps**: Clear guidance for continued development

## Customization Guidelines

When adapting these prompts:
1. **Quality Standards**: Adjust testing and coverage requirements
2. **Compliance Rules**: Modify for your organization's policies
3. **Assessment Scope**: Include/exclude areas based on project type
4. **Reporting Format**: Customize output for your stakeholders
5. **Action Prioritization**: Weight factors according to your context