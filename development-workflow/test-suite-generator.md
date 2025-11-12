# Test Suite Generator

## **Objective**

Generate a comprehensive, production-ready test suite for the current project that ensures code quality, catches regressions, and provides confidence for continuous deployment.

---

## **Assessment Phase**

### 1. **Project Analysis**

* Detect project type and language (Python, JavaScript/TypeScript, Java, Go, Rust, etc.)
* Identify existing testing framework or recommend appropriate ones
* Analyze project structure and critical components
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
| **Python** | pytest, unittest | pytest | pytest, selenium | pytest-cov |
| **JavaScript/TypeScript** | Jest, Vitest | Jest, Supertest | Playwright, Cypress | Jest, c8 |
| **Java** | JUnit 5, TestNG | Spring Test | Selenium | JaCoCo |
| **Go** | testing package | testing + testify | testing | go test -cover |
| **Rust** | cargo test | cargo test | - | cargo-tarpaulin |

---

## **Handling Existing Tests**

### **Skipped/Disabled Test Analysis**

If the project has existing tests with many skipped/disabled:

#### 1. **Catalog All Skipped Tests**

Create an inventory with:
* Test name and location
* Skip reason (from decorators/comments)
* Date skipped (from git history if available)
* Associated issue/ticket references

**Common Skip Patterns:**
```python
# Python
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(condition, reason="...")
@unittest.skip("...")

# JavaScript/Jest
test.skip('...', () => {})
xit('...', () => {})

# Java
@Ignore("...")
@Disabled("...")
```

#### 2. **Categorize Skipped Tests**

Group into categories:

* **Fixable** - Tests that can be repaired (outdated assertions, mock issues)
* **Environment-Dependent** - Require specific setup (CI-only, database-dependent)
* **Flaky** - Intermittent failures due to timing, race conditions
* **Obsolete** - Test legacy/removed features, no longer relevant
* **Blocked** - Waiting on bug fixes, external dependencies, or features
* **Unclear** - No documented reason, investigation needed

#### 3. **Remediation Strategy**

For each category:

**Fixable Tests:**
* Update assertions to match current implementation
* Fix mocking/stubbing issues
* Update test data and fixtures
* Modernize to current testing patterns

**Environment-Dependent:**
* Add environment checks and conditional skipping
* Document required environment setup
* Create fixture/setup utilities for local testing
* Ensure they run in CI/CD

**Flaky Tests:**
* Add retry mechanisms with backoff
* Fix timing issues (use proper waits, not sleep)
* Eliminate race conditions
* Consider refactoring underlying code

**Obsolete Tests:**
* Document reason for removal
* Archive for historical reference
* Remove from test suite
* Update documentation

**Blocked Tests:**
* Link to blocking issues/tickets
* Add clear skip messages with issue references
* Set up tracking for when blockers are resolved
* Create reminder to re-enable

**Unclear Tests:**
* Investigate git history and related code
* Try running and document failure reason
* Consult team/documentation
* Either fix, document skip reason, or remove

#### 4. **Skip Reason Documentation**

For tests that must remain skipped:

```python
@pytest.mark.skip(reason="Requires PostgreSQL 14+. See issue #123")
@pytest.mark.skipif(not has_cuda(), reason="GPU tests require CUDA")
@pytest.mark.xfail(reason="Known bug in dependency v2.1. See PR #456")
```

Always include:
* Clear, specific reason
* Reference to tracking issue/PR
* Conditions for re-enabling
* Alternative coverage if available

---

## **Test Generation Strategy**

### **Test Types to Generate**

#### 🧪 **Unit Tests** (Priority: HIGH)
* Test individual functions, methods, and classes in isolation
* Cover happy paths, edge cases, and error conditions
* Mock external dependencies and I/O operations
* Target: 80%+ code coverage

#### 🔗 **Integration Tests** (Priority: MEDIUM)
* Test component interactions and data flow
* Verify database operations and queries
* Test API endpoints with real/test databases
* Validate external service integrations
* Target: Critical workflows covered

#### 🌐 **End-to-End Tests** (Priority: MEDIUM)
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

Each test file must include:

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

Every configuration variable, parameter, and input must be thoroughly tested:

#### **Default Value Testing**
Test that each variable has the correct default value:
```python
def test_default_value_is_correct():
    """Verify default value matches specification"""
    config = Configuration()
    assert config.timeout == 30  # Expected default: 30 seconds
    assert config.retry_count == 3  # Expected default: 3 retries
    assert config.log_level == "INFO"  # Expected default: INFO
```

#### **Valid Value Testing**
Test that variables accept expected valid values and behave correctly:
```python
def test_valid_value_accepted_and_works():
    """Verify valid values are accepted and produce expected behavior"""
    # Test with expected valid value
    config = Configuration(timeout=60)
    assert config.timeout == 60
    
    # Verify behavior with this valid value
    result = service.execute(config)
    assert result.elapsed_time <= 60
    
    # Test with another valid value
    config.log_level = "DEBUG"
    assert config.log_level == "DEBUG"
    logger = Logger(config)
    assert logger.will_log("DEBUG") is True

def test_all_valid_enum_values():
    """Test all possible valid enum/choice values"""
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for level in valid_levels:
        config = Configuration(log_level=level)
        assert config.log_level == level
        # Verify behavior is correct for each level
        logger = Logger(config)
        assert logger.current_level == level

def test_valid_boundary_values():
    """Test minimum and maximum valid values"""
    # Test minimum valid value
    config = Configuration(timeout=1)
    assert config.timeout == 1
    
    # Test maximum valid value
    config = Configuration(timeout=3600)
    assert config.timeout == 3600
```

#### **Invalid Value Testing**
Test that variables reject invalid values and provide appropriate errors:
```python
def test_invalid_value_raises_error():
    """Verify invalid values are rejected with clear error messages"""
    # Test with wrong type
    with pytest.raises(TypeError) as exc_info:
        config = Configuration(timeout="invalid")
    assert "timeout must be an integer" in str(exc_info.value)
    
    # Test with out-of-range value
    with pytest.raises(ValueError) as exc_info:
        config = Configuration(timeout=-1)
    assert "timeout must be positive" in str(exc_info.value)
    
    # Test with invalid enum value
    with pytest.raises(ValueError) as exc_info:
        config = Configuration(log_level="INVALID")
    assert "log_level must be one of" in str(exc_info.value)
    assert "DEBUG, INFO, WARNING, ERROR, CRITICAL" in str(exc_info.value)

def test_invalid_impossible_values():
    """Test impossible or nonsensical values"""
    # Test impossible numeric value
    with pytest.raises(ValueError) as exc_info:
        config = Configuration(retry_count=0)
    assert "retry_count must be at least 1" in str(exc_info.value)
    
    # Test null/None when not allowed
    with pytest.raises(TypeError) as exc_info:
        config = Configuration(timeout=None)
    assert "timeout cannot be None" in str(exc_info.value)
    
    # Test empty string when not allowed
    with pytest.raises(ValueError) as exc_info:
        config = Configuration(api_key="")
    assert "api_key cannot be empty" in str(exc_info.value)

def test_invalid_value_combinations():
    """Test invalid combinations of values"""
    # Test conflicting configuration
    with pytest.raises(ValueError) as exc_info:
        config = Configuration(
            min_connections=10,
            max_connections=5  # Invalid: max < min
        )
    assert "max_connections must be >= min_connections" in str(exc_info.value)
```

#### **Variable Validation Test Coverage**

For **every** configurable variable, ensure tests for:

| Test Category | Test Cases | Example |
|--------------|------------|---------|
| **Default Value** | Verify default is correct | `assert config.timeout == 30` |
| **Valid Values** | Test all expected valid values | Test each enum value, min/max boundaries |
| **Valid Behavior** | Verify correct behavior with valid values | Service works correctly with timeout=60 |
| **Type Validation** | Wrong type raises TypeError | String instead of int raises error |
| **Range Validation** | Out-of-range raises ValueError | Negative timeout raises error |
| **Enum Validation** | Invalid choice raises ValueError | Invalid log level raises error |
| **Null/Empty** | Null/empty rejected (if not allowed) | Empty string raises error |
| **Impossible Values** | Nonsensical values rejected | Zero retries raises error |
| **Error Messages** | Clear, actionable error messages | Error includes valid options |

#### **Example: Complete Variable Validation Suite**

```python
class TestConfigurationValidation:
    """Comprehensive validation tests for all configuration variables"""
    
    # DEFAULT VALUE TESTS
    def test_default_timeout_is_30_seconds(self):
        config = Configuration()
        assert config.timeout == 30
    
    def test_default_retry_count_is_3(self):
        config = Configuration()
        assert config.retry_count == 3
    
    def test_default_log_level_is_info(self):
        config = Configuration()
        assert config.log_level == "INFO"
    
    # VALID VALUE TESTS
    @pytest.mark.parametrize("timeout", [1, 30, 60, 300, 3600])
    def test_valid_timeout_values_accepted(self, timeout):
        config = Configuration(timeout=timeout)
        assert config.timeout == timeout
    
    @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    def test_valid_log_levels_accepted(self, level):
        config = Configuration(log_level=level)
        assert config.log_level == level
    
    def test_valid_timeout_produces_expected_behavior(self):
        config = Configuration(timeout=5)
        service = Service(config)
        # Verify service actually respects the timeout
        with pytest.raises(TimeoutError):
            service.long_running_operation()  # Takes >5 seconds
    
    # INVALID VALUE TESTS
    def test_invalid_timeout_type_raises_error(self):
        with pytest.raises(TypeError) as exc:
            Configuration(timeout="60")
        assert "timeout must be an integer" in str(exc.value)
    
    def test_negative_timeout_raises_error(self):
        with pytest.raises(ValueError) as exc:
            Configuration(timeout=-1)
        assert "timeout must be positive" in str(exc.value)
        assert "got: -1" in str(exc.value)
    
    def test_invalid_log_level_raises_error_with_valid_options(self):
        with pytest.raises(ValueError) as exc:
            Configuration(log_level="TRACE")
        assert "log_level must be one of" in str(exc.value)
        assert "DEBUG, INFO, WARNING, ERROR, CRITICAL" in str(exc.value)
    
    def test_zero_retry_count_raises_error(self):
        with pytest.raises(ValueError) as exc:
            Configuration(retry_count=0)
        assert "retry_count must be at least 1" in str(exc.value)
    
    def test_none_timeout_raises_error(self):
        with pytest.raises(TypeError) as exc:
            Configuration(timeout=None)
        assert "timeout cannot be None" in str(exc.value)
```

**Key Principles:**
- **Test every variable** - No configuration should go untested
- **Test default first** - Ensure defaults match specification
- **Test valid boundaries** - Min and max valid values
- **Test invalid with errors** - Verify rejection and error messages
- **Error messages must be clear** - Include what was wrong and valid options
- **Test behavior, not just assignment** - Verify the value actually affects behavior

### **Mocking and Fixtures**

* Create reusable fixtures for common test data
* Mock external APIs, databases, and file systems
* Use test databases or in-memory alternatives
* Implement test data factories for complex objects
* Clean up resources after each test

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

Generate hooks to run tests automatically:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running tests before commit..."
pytest tests/unit --cov --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

### **CI/CD Integration**

Add test stages to existing workflows:

```yaml
# .github/workflows/test.yml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Run Unit Tests
      run: pytest tests/unit --cov --cov-report=xml
    - name: Run Integration Tests
      run: pytest tests/integration
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
```

---

## **Quality Standards**

### **Each Test Must:**

* Have a clear, descriptive name explaining what it tests
* Follow Arrange-Act-Assert (AAA) pattern
* Be independent and not rely on execution order
* Run quickly (unit tests < 100ms each)
* Clean up resources (files, connections, etc.)
* Include assertions that verify expected behavior

### **Test Documentation**

* Add docstrings explaining test purpose
* Document complex test setups
* Include examples of expected behavior
* Note any special requirements or dependencies

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
  - Include coverage requirements and thresholds (80%+ target)
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
- [ ] Code coverage meets minimum thresholds (80%+)
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
* Write tests that describe behavior, not implementation
* Keep tests simple and focused on one thing
* Use meaningful assertion messages
* Avoid test interdependencies
* Mock external dependencies consistently
* Run tests frequently during development
* Update tests when code changes
* Treat test code with same quality standards as production code

### **Preventing Test Skipping**

**Root Causes of Skipped Tests:**
* **Flakiness** - Use proper waits, avoid sleep(), fix race conditions
* **Environment Issues** - Use docker, test containers, or proper setup/teardown
* **Slow Tests** - Optimize or move to separate suite (nightly/weekly runs)
* **External Dependencies** - Mock APIs, use test doubles, avoid real network calls
* **Missing Data** - Create reliable fixtures, use factories, seed test databases
* **Unclear Failures** - Add detailed error messages, logs, and debugging info

**Prevention Strategies:**
* Make tests deterministic (no random data, fixed time/dates)
* Isolate tests completely (no shared state)
* Use proper test fixtures and cleanup
* Document test requirements clearly
* Add retry logic only for truly unavoidable flakiness
* Fix failing tests immediately, don't skip them
* Require documented reason + issue tracking for any skip
* Regular test maintenance and cleanup sprints

---

## **Usage Instructions**

Run this prompt when:

* Starting a new project needing test infrastructure
* Adding tests to legacy code without coverage
* Improving existing test suites
* Implementing test-driven development (TDD)
* Preparing for production deployment
* Meeting quality assurance requirements