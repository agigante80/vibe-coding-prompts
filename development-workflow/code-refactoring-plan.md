# Code Refactoring Plan Generator

## **Objective**

Analyze codebase to identify code smells, technical debt, and architectural issues, then generate prioritized refactoring roadmap with effort estimates and risk assessments.

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

Use language-appropriate tools:
- **JavaScript/TypeScript**: ESLint (complexity rules), jscpd (duplicates), ts-prune (unused exports)
- **Python**: pylint (quality), radon (complexity/maintainability), mypy (types)
- **Java**: PMD (code smells), CheckStyle, SonarQube
- **Go**: go vet, staticcheck, gocyclo, golangci-lint
- **Rust**: cargo clippy, cargo fmt, cargo machete

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

1. **Refactoring Analysis Report**: Code quality metrics, identified code smells, technical debt assessment, risk heat map
2. **Prioritized Roadmap**: Quick wins, medium/major refactorings, effort estimates, risk assessment
3. **Implementation Plan**: Phased approach (months 1-6), dependencies, team allocation
4. **Tooling**: Linting config, pre-commit hooks, CI/CD quality gates
5. **Documentation Updates**: Update `/docs/REFACTORING_PLAN.md`, `/docs/IMPROVEMENT_AREAS.md`, `/docs/ARCHITECTURE.md`, `/docs/TESTING_AND_RELIABILITY.md`

---

## **Success Criteria**

- [ ] Code smells identified and categorized
- [ ] Complexity metrics calculated
- [ ] Tasks prioritized with effort estimates
- [ ] Risk assessment completed
- [ ] Automated quality tools configured
- [ ] `/docs/` files updated with refactoring roadmap

---

## **Best Practices**

**Incremental**: Small frequent refactorings, keep system working, deploy gradually  
**Test-Driven**: Never refactor without tests, add tests first if missing  
**Boy Scout Rule**: Leave code better than found  
**Communication**: Discuss major changes, document why  
**Measure**: Track metrics before/after

---

## **Usage Instructions**

**When to run**: Legacy codebase work, after rapid development, declining velocity, quarterly health checks, before major features

**Execution**:
```
I need a refactoring plan for [PROJECT_TYPE].
Language: [JS/Python/Java/Go/Rust]
Pain points: [slow dev, bugs, performance]
Test coverage: [%]
Available time: [% of sprint]
```

**Outcome**: AI analyzes codebase, identifies smells/debt, generates prioritized roadmap with effort/risk estimates, provides refactoring techniques, configures tools, updates `/docs/`
