# Development Workflow Prompts

This folder contains prompts for establishing and maintaining efficient development processes.

## Available Prompts

### 🧪 Test Suite Generator
**File**: `test-suite-generator.md`

**Purpose**: Generates comprehensive, production-ready test suites with unit, integration, and end-to-end tests for any project.

### 🏗️ Code Refactoring Plan Generator
**File**: `code-refactoring-plan.md`

**Purpose**: Analyzes codebases to identify code smells, technical debt, and architectural issues, then generates a prioritized, actionable refactoring roadmap.

### 📁 File & Folder Organization Refactoring
**File**: `file-organization-refactoring.md`

**Purpose**: Systematically reorganizes project files and folders, removes obsolete files, standardizes naming conventions, and establishes clear structure while ensuring application functionality throughout the process.

**Key Features**:
- Analyzes current project structure and identifies organizational issues
- Creates target structure based on project type and best practices
- Generates safe migration scripts with testing after each change
- Updates all import paths automatically
- Removes obsolete files (backups, temp files, deprecated code)
- Standardizes file naming conventions
- Integrates with `/docs/REFACTORING_PLAN.md`
- Preserves Git history using `git mv`
- Comprehensive verification (tests, build, application health)

**Organization Goals**:
- Clear directory structure (src/, tests/, config/, docs/)
- No source files in project root
- Consistent naming conventions
- Logical grouping of related files
- Separation of concerns
- Easy navigation and file discovery

**Best For**:
- Projects with cluttered root directories
- Flat structures needing hierarchy
- Codebases with scattered files
- Removing accumulated obsolete files
- Standardizing naming across projects
- Preparing for major refactoring
- Improving team onboarding

**Safety Measures**:
- One file at a time with testing
- Automated import path updates
- Git history preservation
- Full test suite validation
- Application health verification
- Rollback procedures

---

**Key Features**:
- Multi-language test framework detection and setup
- Generates unit, integration, and E2E tests
- Creates test fixtures and mocking infrastructure
- Includes CI/CD test integration
- Provides pre-commit hooks for automatic testing
- Coverage reporting and quality gates
- Test documentation and maintenance guidelines
- **Comprehensive variable validation testing** (defaults, valid values, error handling)

**Test Coverage**:
- **Unit Tests**: 80%+ code coverage target
- **Integration Tests**: Critical workflows and component interactions
- **E2E Tests**: Core user journeys and system behavior
- **Performance Tests**: Key operations and bottleneck identification
- **Variable Validation**: Every configuration variable tested (defaults, valid values, invalid values with errors)

**Best For**:
- Adding tests to legacy projects without coverage
- Establishing test infrastructure for new projects
- Improving existing test suites with best practices
- Implementing test-driven development (TDD)
- Meeting quality assurance and deployment requirements
- Ensuring code reliability and catching regressions

**Usage Tips**:
- Review and customize generated tests for your specific context
- Adjust coverage thresholds based on project criticality
- Integrate test execution into your development workflow
- Use generated fixtures as templates for additional test data
- For projects with many skipped tests, pay special attention to the remediation strategy
- Ensure all configuration variables are validated (default values, valid values, invalid values with clear errors)
- ✅ **Platform-friendly**: At ~2561 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

---

**Key Features**:
- Multi-language code smell detection (JavaScript, Python, Java, Go, Rust)
- Automated complexity analysis and metrics calculation
- Prioritized refactoring roadmap with effort estimates
- Risk assessment for each refactoring task
- Quick wins, medium refactorings, and strategic improvements
- Refactoring techniques and patterns catalog
- Safety measures and testing requirements
- Integration with automated linting and quality tools

**Analysis Coverage**:
- **Structural Issues**: God objects, long methods, feature envy, data clumps
- **Duplication**: Copy-paste code, magic numbers, string duplication
- **Complexity**: Cyclomatic complexity, deep nesting, long parameter lists
- **Coupling & Cohesion**: Tight coupling, circular dependencies, shotgun surgery
- **Naming & Organization**: Unclear names, dead code, missing documentation

**Prioritization Framework**:
- Technical debt severity scoring (1-10)
- Business impact assessment (1-10)
- Effort estimation (1-10)
- Priority calculation: (Debt × 2 + Impact × 3) / Effort

**Best For**:
- Legacy codebases needing systematic improvement
- Teams experiencing declining development velocity
- Pre-planning major architectural changes
- Quarterly code quality health checks
- Onboarding new developers to complex code
- Establishing code quality baselines and metrics
- Managing technical debt strategically

**Usage Tips**:
- Run analysis on legacy code before major feature work
- Use automated tools (ESLint, Pylint, SonarQube) for objective metrics
- Start with quick wins to build momentum
- Ensure adequate test coverage before refactoring
- Refactor incrementally rather than big-bang rewrites
- Track metrics before/after to measure impact
- ✅ **Platform-friendly**: At ~2485 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

## When to Use Development Workflow Prompts

Use these prompts when:
- Adding comprehensive test coverage to projects
- Conducting code quality audits and refactoring
- Establishing sustainable development practices
- Managing technical debt systematically
- Improving developer velocity through better code quality

## Integration with Other Prompts

Development workflow prompts work well with:
- **Project Management**: Use project reassessment to identify areas needing tests or refactoring
- **DevOps Automation**: Integrate test execution and quality checks into CI/CD pipelines
- **Documentation**: Document test strategies and refactoring plans in `/docs/`
- **Security**: Include security testing and secure refactoring practices

## Prerequisites

Before implementing this workflow:
- Comprehensive automated testing suite
- Reliable CI/CD pipeline with quality gates
- Clear coding standards and style guides
- Security scanning and monitoring tools
- Team agreement on automation boundaries