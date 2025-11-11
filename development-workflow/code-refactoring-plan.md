# Code Refactoring Plan Generator

## **Objective**

Analyze the current codebase to identify code smells, technical debt, and architectural issues, then generate a prioritized, actionable refactoring roadmap with effort estimates and risk assessments.

---

## **Assessment Phase**

### 1. **Codebase Analysis**

**Project Discovery**:
- Detect project type, language, and framework
- Identify code organization patterns (monolith, microservices, modular)
- Catalog dependencies and third-party integrations
- Map file structure and module boundaries
- Analyze code metrics (LOC, complexity, duplication)
- Review existing tests and coverage

**Technology Stack Detection**:
```bash
# Identify languages and frameworks
find . -name "package.json" -o -name "requirements.txt" -o -name "pom.xml" \
  -o -name "Cargo.toml" -o -name "go.mod" -o -name "composer.json"

# Count files by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Measure codebase size
cloc . --exclude-dir=node_modules,vendor,dist,build
```

### 2. **Code Smell Detection**

**Structural Issues**:
- **God Objects** - Classes with too many responsibilities (>500 LOC, >20 methods)
- **Long Methods** - Functions exceeding 50 lines or multiple levels of nesting
- **Large Classes** - Classes with excessive methods or properties
- **Feature Envy** - Methods using other classes' data more than their own
- **Data Clumps** - Same group of variables passed around together
- **Primitive Obsession** - Overuse of primitives instead of domain objects
- **Switch/Case Statements** - Complex conditionals that should be polymorphic

**Duplication Issues**:
- **Duplicate Code** - Identical or similar code blocks (>5 lines)
- **Copy-Paste Programming** - Repetitive patterns without abstraction
- **Magic Numbers** - Hard-coded values without constants/enums
- **String Duplication** - Repeated string literals

**Complexity Issues**:
- **Cyclomatic Complexity** - Too many conditional branches (>10)
- **Deep Nesting** - Excessive indentation levels (>4)
- **Long Parameter Lists** - Functions with >4 parameters
- **Complex Conditionals** - Hard-to-understand boolean logic

**Coupling & Cohesion**:
- **Tight Coupling** - Classes with too many dependencies
- **Circular Dependencies** - Modules depending on each other
- **Shotgun Surgery** - Single change requires modifications across many files
- **Divergent Change** - Class changed for many different reasons
- **Low Cohesion** - Unrelated functionality grouped together

**Naming & Organization**:
- **Unclear Names** - Variables/functions with non-descriptive names
- **Inconsistent Naming** - Mixed conventions (camelCase, snake_case, etc.)
- **Dead Code** - Unused functions, variables, or imports
- **Commented-Out Code** - Old code left in comments
- **Missing Documentation** - Functions/classes without docs

---

## **Code Quality Metrics**

### **Automated Analysis Tools**

Use language-appropriate tools for objective measurements:

**JavaScript/TypeScript**:
```bash
# ESLint with complexity rules
npx eslint . --ext .js,.ts --max-warnings 0

# Code complexity
npx eslint . --plugin complexity --rule 'complexity: ["error", 10]'

# Detect duplicates
npx jscpd src/

# TypeScript specific
npx ts-prune  # Find unused exports
```

**Python**:
```bash
# Pylint for code quality
pylint **/*.py --fail-under=8.0

# Code complexity
radon cc . -a -nb  # Cyclomatic complexity
radon mi . -nb     # Maintainability index

# Detect duplicates
pylint --disable=all --enable=duplicate-code .

# Type checking
mypy . --strict
```

**Java**:
```bash
# PMD for code smells
pmd check -d src/ -R rulesets/java/quickstart.xml

# CheckStyle
checkstyle -c google_checks.xml src/

# SonarQube analysis
mvn sonar:sonar
```

**Go**:
```bash
# Static analysis
go vet ./...
staticcheck ./...

# Code complexity
gocyclo -over 10 .

# Detect common issues
golangci-lint run
```

**Rust**:
```bash
# Clippy for lints
cargo clippy -- -D warnings

# Code formatting
cargo fmt --check

# Unused dependencies
cargo machete
```

### **Complexity Thresholds**

| Metric | Good | Acceptable | Needs Refactoring | Critical |
|--------|------|------------|-------------------|----------|
| **Cyclomatic Complexity** | 1-5 | 6-10 | 11-20 | >20 |
| **Lines of Code (Method)** | 1-20 | 21-50 | 51-100 | >100 |
| **Lines of Code (Class)** | 1-200 | 201-500 | 501-1000 | >1000 |
| **Parameters per Function** | 0-3 | 4-5 | 6-8 | >8 |
| **Nesting Depth** | 1-2 | 3-4 | 5-6 | >6 |
| **Code Duplication %** | 0-3% | 3-5% | 5-10% | >10% |
| **Test Coverage** | 80-100% | 60-79% | 40-59% | <40% |

---

## **Refactoring Categories**

### 🔧 **Quick Wins (1-2 days)**

**High Impact, Low Effort**:
- Extract magic numbers to constants/enums
- Rename unclear variables and functions
- Remove dead code and unused imports
- Fix inconsistent code formatting
- Add missing type hints/annotations
- Extract duplicated code into functions
- Simplify complex conditionals
- Add basic JSDoc/docstrings

### 🔨 **Medium Refactorings (3-7 days)**

**Medium Impact, Medium Effort**:
- Break down god objects into smaller classes
- Extract long methods into smaller functions
- Introduce design patterns (Strategy, Factory, etc.)
- Reduce tight coupling with dependency injection
- Reorganize file structure for better cohesion
- Extract interfaces for better abstraction
- Implement proper error handling
- Add comprehensive unit tests

### 🏗️ **Major Refactorings (1-4 weeks)**

**High Impact, High Effort**:
- Architectural restructuring (monolith → microservices)
- Replace legacy frameworks with modern alternatives
- Migrate from inheritance to composition
- Implement proper separation of concerns (MVC, Clean Architecture)
- Break circular dependencies
- Establish proper module boundaries
- Migrate to strongly-typed system
- Comprehensive test suite implementation

### 🚧 **Infrastructure Improvements (1-3 months)**

**Strategic, Long-term**:
- Database schema refactoring
- API versioning and migration
- Performance optimization (caching, indexing)
- Security hardening and audit fixes
- Scalability improvements
- CI/CD pipeline modernization
- Observability and monitoring setup
- Documentation overhaul

---

## **Prioritization Framework**

### **Scoring System**

Rate each refactoring on three dimensions:

**1. Technical Debt Severity (1-10)**:
- 9-10: Critical - Blocking new features, causing bugs
- 7-8: High - Significantly slowing development
- 5-6: Medium - Noticeable but manageable
- 3-4: Low - Minor inconvenience
- 1-2: Trivial - Cosmetic improvements

**2. Business Impact (1-10)**:
- 9-10: Critical - Security, data loss, or downtime risk
- 7-8: High - User-facing bugs or performance issues
- 5-6: Medium - Developer productivity impact
- 3-4: Low - Code quality improvement
- 1-2: Trivial - Nice-to-have cleanup

**3. Effort Required (1-10)**:
- 9-10: Massive - Months of work, high risk
- 7-8: Large - Weeks of work, significant testing
- 5-6: Medium - Days of work, moderate risk
- 3-4: Small - Hours to a day, low risk
- 1-2: Trivial - Minutes to an hour, no risk

**Priority Score Formula**:
```
Priority = (Technical Debt × 2 + Business Impact × 3) / Effort
```

Higher scores = Higher priority refactoring

---

## **Refactoring Techniques**

### **Method-Level Refactorings**

1. **Extract Method** - Break long functions into smaller, named pieces
2. **Inline Method** - Remove unnecessary abstraction layers
3. **Extract Variable** - Name intermediate calculations
4. **Inline Variable** - Remove single-use variables
5. **Rename Method/Variable** - Improve clarity
6. **Change Function Declaration** - Adjust parameters and return types
7. **Introduce Parameter Object** - Group related parameters
8. **Replace Temp with Query** - Eliminate temporary variables

### **Class-Level Refactorings**

1. **Extract Class** - Split responsibilities
2. **Inline Class** - Merge trivial classes
3. **Move Method/Field** - Improve cohesion
4. **Extract Interface** - Define contracts
5. **Pull Up Method** - Share common code in superclass
6. **Push Down Method** - Move specialized code to subclass
7. **Replace Inheritance with Delegation** - Prefer composition
8. **Encapsulate Field** - Hide internal state

### **Architectural Refactorings**

1. **Extract Module** - Create logical boundaries
2. **Introduce Service Layer** - Separate business logic
3. **Replace Conditional with Polymorphism** - Use OOP properly
4. **Introduce Dependency Injection** - Reduce coupling
5. **Event-Driven Architecture** - Decouple components
6. **CQRS Pattern** - Separate reads and writes
7. **Strangler Fig Pattern** - Gradually replace legacy systems
8. **Repository Pattern** - Abstract data access

---

## **Risk Assessment**

### **Refactoring Risk Levels**

**Low Risk** (Green Light):
- Renaming variables/functions (with IDE support)
- Extracting methods/functions
- Adding type annotations
- Removing dead code
- Formatting and style fixes
- Adding tests without changing code
- Improving documentation

**Medium Risk** (Proceed with Caution):
- Moving methods between classes
- Changing function signatures
- Restructuring file organization
- Introducing new abstractions
- Database query optimization
- Performance improvements
- Dependency updates

**High Risk** (Requires Planning):
- Architectural changes
- Breaking API changes
- Database schema migrations
- Replacing core libraries/frameworks
- Changing authentication/authorization
- Modifying critical business logic
- Large-scale code reorganization

### **Safety Measures**

**Before Refactoring**:
- [ ] All tests passing (100% green)
- [ ] Test coverage adequate (>70% for changed areas)
- [ ] Feature branch created
- [ ] Backup of current state
- [ ] Team notified of refactoring scope
- [ ] Risk assessment documented

**During Refactoring**:
- [ ] Work in small, incremental steps
- [ ] Run tests after each change
- [ ] Commit frequently with clear messages
- [ ] Keep CI/CD pipeline green
- [ ] Use automated refactoring tools when possible
- [ ] Pair programming for high-risk changes

**After Refactoring**:
- [ ] Full test suite passing
- [ ] Code review completed
- [ ] Performance benchmarks maintained or improved
- [ ] Documentation updated
- [ ] Team walkthrough conducted
- [ ] Monitoring alerts configured

---

## **Deliverables**

### **Refactoring Analysis Report**
1. **Executive Summary** - High-level overview of codebase health
2. **Code Quality Metrics** - Complexity, duplication, coverage scores
3. **Identified Code Smells** - Categorized list with locations and severity
4. **Technical Debt Assessment** - Total debt hours and cost estimation
5. **Risk Heat Map** - Visual representation of problem areas

### **Prioritized Refactoring Roadmap**
6. **Quick Wins List** - Immediate improvements (1-2 days each)
7. **Medium Refactorings** - Planned improvements (1-2 weeks each)
8. **Major Refactorings** - Strategic initiatives (1-3 months each)
9. **Effort Estimates** - Time and resource requirements for each item
10. **Risk Assessment** - Potential issues and mitigation strategies

### **Implementation Plan**
11. **Phase 1 (Month 1)** - Critical fixes and quick wins
12. **Phase 2 (Months 2-3)** - Medium-priority refactorings
13. **Phase 3 (Months 4-6)** - Major architectural improvements
14. **Dependencies & Sequencing** - What must be done before what
15. **Team Allocation** - Who works on which refactorings

### **Tooling & Automation**
16. **Linting Configuration** - ESLint, Pylint, etc. setup
17. **Pre-commit Hooks** - Automated quality checks
18. **CI/CD Integration** - Quality gates in pipeline
19. **Code Review Checklist** - Standards for reviews
20. **Refactoring Scripts** - Automated transformation tools

### **Documentation Updates**
All refactoring analysis and plans must be documented in `/docs/`:

- **`/docs/REFACTORING_PLAN.md`**: Add complete refactoring roadmap with phases, prioritized tasks, effort estimates, risk assessments, and completion tracking
- **`/docs/IMPROVEMENT_AREAS.md`**: Document identified code smells, technical debt items, complexity hotspots, and architectural issues with severity scores
- **`/docs/ARCHITECTURE.md`**: Update with planned architectural changes, refactoring goals, and target state after major refactorings
- **`/docs/TESTING_AND_RELIABILITY.md`**: Add test coverage goals for refactored code, quality gates, and refactoring safety procedures

---

## **Success Criteria**

- [ ] All code smells identified and categorized by severity
- [ ] Complexity metrics calculated for entire codebase
- [ ] Refactoring tasks prioritized using scoring framework
- [ ] Quick wins identified and can be executed immediately
- [ ] Major refactorings have detailed implementation plans
- [ ] Risk assessment completed for all proposed changes
- [ ] Effort estimates provided (person-hours/days)
- [ ] Dependencies between refactorings mapped
- [ ] Automated quality tools configured (linters, formatters)
- [ ] Team trained on refactoring techniques and safety measures
- [ ] **`/docs/` files updated** with refactoring roadmap and technical debt

---

## **Best Practices**

### **Incremental Over Big Bang**
- Make small, frequent refactorings rather than massive rewrites
- Keep the system working at all times (no long-lived broken branches)
- Deploy refactorings gradually to production
- Use feature flags to toggle between old and new implementations

### **Test-Driven Refactoring**
- Never refactor without adequate test coverage
- Add tests before refactoring if coverage is insufficient
- Use tests as safety net to catch regressions
- Consider characterization tests for legacy code

### **Boy Scout Rule**
- Leave code better than you found it
- Refactor opportunistically when touching code for other reasons
- Don't wait for perfect time - refactor continuously
- Build refactoring time into sprint planning

### **Communication & Documentation**
- Discuss major refactorings with team before starting
- Document why refactorings are needed, not just what changes
- Share learnings and patterns discovered
- Update architecture documentation proactively

### **Measure Impact**
- Track metrics before and after refactoring
- Monitor performance impact (positive and negative)
- Measure developer velocity changes
- Survey team satisfaction with code quality

---

## **Usage Instructions**

### **When to Run This Analysis**

* Starting work on a legacy codebase
* After rapid feature development period (technical debt accumulated)
* Before major new feature development
* Quarterly codebase health assessments
* When developer velocity is declining
* Before bringing new team members onboard
* After major incidents caused by code quality issues

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine existing `/docs/REFACTORING_PLAN.md` and `/docs/IMPROVEMENT_AREAS.md` if they exist
3. Ensure code quality tools are available (linters, complexity analyzers)
4. Have comprehensive test suite or plan to add tests

### **Execution**
```
I need a comprehensive refactoring plan for my [PROJECT_TYPE].

Project language: [JavaScript/Python/Java/Go/Rust/etc.]
Codebase age: [months/years]
Team size: [number of developers]
Current pain points: [slow development, bugs, performance, etc.]
Test coverage: [percentage or "unknown"]
Available refactoring time: [% of sprint capacity]
Risk tolerance: [low/medium/high]
```

### **Expected Outcome**
The AI will analyze your entire codebase using automated tools and pattern detection, identify code smells and technical debt with severity scoring, calculate complexity metrics and quality scores, generate a prioritized refactoring roadmap with effort estimates, provide specific refactoring techniques for each issue, assess risks and provide mitigation strategies, configure automated quality tools and pre-commit hooks, and document everything in `/docs/` files. You'll receive a comprehensive, actionable plan to systematically improve code quality while managing risk and maintaining delivery velocity.

---

## **Example Refactoring Plan Output**

### **Priority 1 - Quick Wins (Week 1)**
1. ✅ Extract 12 magic numbers to constants (2 hours, Low Risk)
2. ✅ Remove 47 unused imports and dead functions (3 hours, Low Risk)
3. ✅ Rename 23 unclear variables in auth module (4 hours, Low Risk)
4. ✅ Fix code formatting inconsistencies (1 hour, Low Risk)

### **Priority 2 - Medium Impact (Weeks 2-4)**
5. 🔨 Split `UserController` god class (1200 LOC → 4 classes, 2 days, Medium Risk)
6. 🔨 Extract duplicate validation logic into validators (1.5 days, Low Risk)
7. 🔨 Reduce cyclomatic complexity in payment processing (3 days, High Risk)
8. 🔨 Introduce repository pattern for data access (4 days, Medium Risk)

### **Priority 3 - Strategic (Months 2-3)**
9. 🏗️ Migrate from inheritance to composition in core domain (2 weeks, High Risk)
10. 🏗️ Break circular dependencies between modules (3 weeks, High Risk)
11. 🏗️ Implement proper error handling with Result types (2 weeks, Medium Risk)
12. 🏗️ Increase test coverage from 45% to 80% (4 weeks, Low Risk)
