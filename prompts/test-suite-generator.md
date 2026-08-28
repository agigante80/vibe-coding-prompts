---
name: test-suite-generator
category: development-workflow
version: 1.1.1
updated: 2026-08-28
description: Generate a comprehensive test suite with unit, integration and e2e coverage, plus skipped-test cleanup.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# Test Suite Generator

## **Objective**

Generate a comprehensive, production-ready test suite for the current project that ensures code quality, catches regressions, and provides confidence for continuous deployment.

---

## **Assessment Phase**

### 1. **Project Analysis**

* Detect language and framework; identify or recommend the testing stack; map critical components
* **Review existing tests comprehensively:**
  * Identify skipped/disabled tests (pytest.skip, @Ignore, test.skip, etc.)
  * Analyze why tests were skipped (comments, commit history, issue references)
  * Assess if skipped tests are still relevant or obsolete
  * Check for failing tests that were commented out
  * Review test coverage reports and identify gaps
* Identify dependencies and external integrations requiring mocking

### 2. **Testing Framework Selection**

Choose appropriate frameworks based on project type:

| Language | Unit Testing | Integration | E2E | Coverage |
|----------|-------------|-------------|-----|----------|
| **Python** | pytest, unittest | pytest | Playwright | pytest-cov |
| **JavaScript/TypeScript** | Jest, Vitest | Jest, Supertest | Playwright, Cypress | Jest, c8 |
| **Java** | JUnit 5, TestNG | Spring Test | Selenium | JaCoCo |
| **Go** | testing package | testing + testify | testing | go test -cover |
| **Rust** | cargo test | tests/ dir | tests/ dir | cargo-tarpaulin |

---

## **Handling Existing Tests**

### **Skipped/Disabled Test Analysis**

**Catalog**: List test name, skip reason, date, issue references

**Categorize**: fixable (update assertions/mocks/data), environment-dependent (conditional skip, document setup), flaky (fix timing/races), obsolete (document and remove), blocked (link issues, document clearly), unclear (investigate git history, then fix or document)

**Skip Documentation**: specific reason, issue reference, re-enabling conditions
```python
@pytest.mark.skip(reason="Requires PostgreSQL 14+. See issue #123")
```

---

## **Test Generation Strategy**

### **Test Types to Generate**

Shape the suite as a test pyramid: write LOTS of small fast unit tests, SOME coarser integration tests, and VERY FEW end-to-end tests; push every test as low in the pyramid as it can live.

#### 🧪 **Unit Tests** (Priority: HIGH, the bulk of the suite)
* Test individual functions, methods, and classes in isolation
* Cover happy paths, edge cases, and error conditions
* Mock external dependencies and I/O operations
* Coverage floor: 80% (a regression floor and a tool for FINDING untested code, never a goal; chasing a number produces assertion-free tests. Add mutation testing for critical logic to test the tests)

#### 🔗 **Integration Tests** (Priority: MEDIUM)
* Test component interactions and data flow
* Verify database operations and queries
* Test API endpoints with real/test databases
* Validate external service integrations
* Target: Critical workflows covered

#### 🌐 **End-to-End Tests** (Priority: LOW, very few)
* Test complete user workflows
* Validate UI interactions (if applicable)
* Test API flows from request to response
* Verify system behavior under realistic conditions
* Target: Core user journeys covered

#### ⚡ **Performance Tests** (Priority: LOW)
* Benchmark critical operations
* Test under load conditions
* Identify bottlenecks and memory leaks
* Target: Key endpoints/functions benchmarked

---

## **Implementation Requirements**

### **Test Structure**

Each test file follows this shape:

```
# Test file structure example (Python/pytest)

import pytest
from unittest.mock import Mock, patch

# Fixtures for reusable test data
@pytest.fixture
def sample_data():
    return {"key": "value"}

# Test class or function grouping
class TestComponentName:
    
    def test_happy_path(self, sample_data):
        """Test normal successful operation"""
        # Arrange
        component = Component(sample_data)
        
        # Act
        result = component.process()
        
        # Assert
        assert result.success is True
        assert result.data == expected_data
    
    def test_edge_case_empty_input(self):
        """Test handling of empty input"""
        # Test implementation
    
    def test_error_handling_invalid_data(self):
        """Test error handling for invalid data"""
        # Test implementation
```

### **Test Coverage Goals**

- [ ] **Critical paths**: 100% coverage
- [ ] **Business logic**: 90%+ coverage
- [ ] **Utilities and helpers**: 80%+ coverage
- [ ] **Error handling**: All error paths tested
- [ ] **Edge cases**: Null, empty, boundary values
- [ ] **Security**: Authentication, authorization, input validation
- [ ] **Variable validation**: All configuration and input variables tested

### **Variable Validation Testing**

Test every configuration variable/parameter/input:

**Test Coverage Required**:
| Category | Tests |
|----------|-------|
| **Default Values** | Verify correct defaults |
| **Valid Values** | Test all enum values, min/max boundaries |
| **Valid Behavior** | Verify correct operation with valid values |
| **Invalid Values** | Wrong type/range/enum raises clear errors |
| **Null/Empty** | Rejected if not allowed |
| **Error Messages** | Clear, actionable (include valid options) |

**Example**:
```python
def test_default_timeout():
    assert Configuration().timeout == 30

def test_valid_timeout():
    config = Configuration(timeout=60)
    assert config.timeout == 60
    assert service.execute(config).elapsed_time <= 60

def test_invalid_timeout():
    with pytest.raises(TypeError, match="timeout must be an integer"):
        Configuration(timeout="60")
    with pytest.raises(ValueError, match="timeout must be positive"):
        Configuration(timeout=-1)
```

**Key Principles**: every variable tested, defaults first, boundaries, clear errors, behavior over assignment

### **Mocking and Fixtures**

* Reusable fixtures and factories for test data; mock external APIs, databases and file systems
* Test databases or in-memory alternatives; clean up resources after each test

---

## **Test Organization**

### **Directory Structure**

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_external_services.py
├── e2e/
│   ├── test_user_workflows.py
│   └── test_critical_paths.py
├── fixtures/
│   ├── sample_data.py
│   └── mock_responses.py
├── conftest.py  # pytest configuration
└── README.md    # Test documentation
```

---

## **Automation Integration**

### **Pre-commit Hooks**

Use the pre-commit framework (or husky for JS): raw `.git/hooks/` scripts are per-clone and invisible to the team, while a committed config is shared:

```yaml
# .pre-commit-config.yaml  (each developer runs: pre-commit install)
repos:
  - repo: local
    hooks:
      - id: unit-tests
        name: unit tests
        entry: pytest tests/unit --cov=src --cov-fail-under=80
        language: system
        pass_filenames: false
```

### **CI/CD Integration**

A complete minimal workflow, Python example; generate the equivalent for the detected stack (setup-node + npm test, setup-go + go test, etc.). Pin third-party actions to a full commit SHA in real projects. Scope coverage to the source tree: bare `--cov` measures test files and site-packages instead of your code.

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements.txt pytest pytest-cov
      - name: Run unit tests
        run: pytest tests/unit --cov=src --cov-fail-under=80
      - name: Run integration tests
        run: pytest tests/integration
```

Using a coverage service (Codecov etc.)? Add `--cov-report=xml` and that service's upload step.

---

## **Quality Standards**

### **Each Test Must:**

* Clear descriptive name; Arrange-Act-Assert pattern; independent of execution order
* Fast (unit tests < 100ms each); cleans up resources; asserts expected behavior

### **Test Documentation**

* Docstrings for purpose, documented complex setups, noted special requirements

---

## **Deliverables**

Generate the following:

1. **Skipped Test Analysis Report** (if existing tests found):
   * Inventory of all skipped/disabled tests
   * Categorization with remediation recommendations
   * Priority order for fixing tests
   * Estimated effort for each category
2. **Complete test suite** organized by test type (new + fixed existing)
3. **Test configuration files** (pytest.ini, jest.config.js, etc.)
4. **Fixtures and test data** for reusable components
5. **CI/CD test integration** in existing workflows
6. **Test documentation** explaining how to run and maintain tests
7. **Coverage report** showing current coverage status and improvements

### **Documentation Updates**

Update the following files in `/docs/`:

- **`/docs/TESTING_AND_RELIABILITY.md`**:
  - Add test framework configuration details (pytest, Jest, JUnit, etc.)
  - Document test execution commands for each test type
  - Include the coverage floor (80%) and its diagnostic-not-target framing
  - Add CI/CD integration details and workflows
  - Document skipped test handling procedures
  - Add test organization structure (unit, integration, e2e)

- **`/docs/README.md`**:
  - Add "Running Tests" section with quick start commands
  - Link to `TESTING_AND_RELIABILITY.md` for detailed testing docs
  - Include test setup prerequisites (dependencies, environment)

- **`/docs/ARCHITECTURE.md`**:
  - Document test directory structure (`tests/unit/`, `tests/integration/`, etc.)
  - Add test fixture locations and organization
  - Describe test data management approach

- **`/docs/AI_INTERACTION_GUIDE.md`** (if using AI-assisted development):
  - Add rules for maintaining test quality
  - Document automation for running tests before commits
  - Include test update triggers (when code changes)

---

## **Success Criteria**

- [ ] **Skipped tests addressed**: Fixed, documented, or removed with justification
- [ ] All active tests pass successfully (no skips without documented reason)
- [ ] Coverage does not decrease (floor 80%); coverage used as a diagnostic, not a target
- [ ] Tests run in CI/CD pipeline automatically
- [ ] No flaky or intermittent test failures
- [ ] Test execution time is reasonable (< 5 minutes for full suite)
- [ ] Critical business logic has comprehensive coverage
- [ ] Documentation explains test structure and maintenance
- [ ] Clear process for handling future skipped tests
- [ ] **`/docs/` files updated** with test configuration and procedures

---

## **Best Practices**

### **General Testing**
* Test behavior, not implementation; one focused thing per test. Verify new tests can actually fail: [Prove Your Tests Can Fail](./prove-your-tests-can-fail.md)
* No test interdependencies; mock external dependencies consistently
* Run tests frequently, update them with code changes, and hold test code to production standards

### **Preventing Test Skipping**

**Root Causes of Skipped Tests:** flakiness (fix waits and race conditions, avoid sleep()), environment issues (docker, test containers, proper setup/teardown), slow tests (optimize or move to a nightly suite), external dependencies (mock them), missing data (reliable fixtures and factories), unclear failures (detailed messages and logs)

**Prevention:** deterministic tests (no random data, fixed time), complete isolation (no shared state), proper fixtures and cleanup, retries only for truly unavoidable flakiness, fix failures immediately instead of skipping, and require a documented reason plus issue link for any skip

---

## **Usage Instructions**

Run this prompt when: starting a project needing test infrastructure, adding tests to legacy code, improving existing suites, implementing TDD, or preparing for production deployment.