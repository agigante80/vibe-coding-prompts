# Development Workflow Prompts

This folder contains prompts for establishing and maintaining efficient development processes.

## Available Prompts

### 🔄 Automated Development Workflow
**File**: `automated-development.md`

**Purpose**: Establishes a fully automated development workflow that maintains high quality while requiring minimal human intervention.

### 🧪 Test Suite Generator
**File**: `test-suite-generator.md`

**Purpose**: Generates comprehensive, production-ready test suites with unit, integration, and end-to-end tests for any project.

### 🏗️ Code Refactoring Plan Generator
**File**: `code-refactoring-plan.md`

**Purpose**: Analyzes codebases to identify code smells, technical debt, and architectural issues, then generates a prioritized, actionable refactoring roadmap.

**Key Features**:
- Automated CI/CD monitoring and PR merging
- Continuous refactoring and cleanup activities
- Automated documentation updates
- Quality gate enforcement
- Focus on product understanding over pure coding
- Learning-oriented development approach

**Automation Capabilities**:
- **Code Quality**: Automated formatting, linting, and testing
- **Integration**: Automatic PR merging when all checks pass
- **Documentation**: Real-time updates as code changes
- **Security**: Continuous vulnerability scanning and remediation
- **Refactoring**: Systematic code improvement and cleanup
- **Release Management**: Automated versioning and deployment

**Learning Focus Areas**:
- **Product Understanding**: Requirements analysis and user experience
- **Better Requirements**: Clear acceptance criteria and edge cases
- **Holistic Development**: Architecture decisions and long-term maintainability
- **Collaboration**: Effective team coordination and knowledge sharing

**Best For**:
- Large refactoring projects requiring sustained effort
- Teams wanting to focus on product development over process management
- Maintaining momentum on complex, long-term improvements
- Learning product development skills while ensuring code quality
- Establishing sustainable development practices

**Usage Tips**:
- Ensure robust testing infrastructure before enabling full automation
- Start with lower-risk projects to validate the workflow
- Maintain clear boundaries between automated and human-reviewed changes
- Use for sustained periods to see the full benefits of automation

---

**Key Features**:
- Multi-language test framework detection and setup
- Generates unit, integration, and E2E tests
- Creates test fixtures and mocking infrastructure
- Includes CI/CD test integration
- Provides pre-commit hooks for automatic testing
- Coverage reporting and quality gates
- Test documentation and maintenance guidelines

**Test Coverage**:
- **Unit Tests**: 80%+ code coverage target
- **Integration Tests**: Critical workflows and component interactions
- **E2E Tests**: Core user journeys and system behavior
- **Performance Tests**: Key operations and bottleneck identification

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
- ✅ **Platform-friendly**: At ~1570 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

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
- Managing large-scale refactoring or cleanup efforts
- Wanting to maintain development velocity without constant oversight
- Learning product development while ensuring quality
- Establishing sustainable development practices for teams
- Reducing manual overhead in routine development tasks
- Focusing team attention on high-value product decisions

## Integration with Other Prompts

Development workflow prompts work well with:
- **Project Management**: Use assessments to guide automated improvements
- **DevOps Automation**: Leverage robust CI/CD for workflow automation
- **Documentation**: Automate documentation updates as part of the workflow

## Workflow Philosophy

This approach emphasizes:
- **Product Over Process**: Focus human attention on product decisions
- **Quality Automation**: Ensure quality through automated checks rather than manual review
- **Continuous Learning**: Use development time for skill building and understanding
- **Sustainable Pace**: Maintain consistent progress without burnout
- **Incremental Improvement**: Make small, continuous improvements rather than large overhauls

## Automation Boundaries

### Fully Automated
- Code formatting and style enforcement
- Test execution and basic quality checks
- Documentation generation and updates
- Routine refactoring and cleanup tasks
- Security vulnerability scanning
- Dependency updates with validation

### Human Review Required
- Major architectural changes
- Breaking API modifications
- New feature specifications
- Security policy updates
- External service integrations
- Business logic changes

## Success Metrics

Track progress using:
- **Code Quality**: Improving metrics over time
- **Development Velocity**: Consistent feature delivery
- **Bug Rates**: Decreasing production issues
- **Test Coverage**: Increasing automated test coverage
- **Technical Debt**: Systematic reduction over time
- **Team Learning**: Growing product and requirements analysis skills

## Customization Guidelines

When adapting these prompts:
1. **Automation Scope**: Define what can be safely automated in your context
2. **Quality Gates**: Set appropriate thresholds for automated decisions
3. **Learning Objectives**: Customize focus areas for your team's growth needs
4. **Review Triggers**: Define when human intervention is required
5. **Metrics**: Choose success indicators relevant to your project goals

## Prerequisites

Before implementing this workflow:
- Comprehensive automated testing suite
- Reliable CI/CD pipeline with quality gates
- Clear coding standards and style guides
- Security scanning and monitoring tools
- Team agreement on automation boundaries