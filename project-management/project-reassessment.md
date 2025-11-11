# Project Reassessment & Synchronization

## **Objective**

Perform a full reassessment of the current repository against its documentation to ensure complete alignment between code, documentation, and project policies.

---

## **Assessment Process**

### 1. **Comprehensive Analysis**

* Analyze the entire codebase and all files under `/docs`
* Cross-check architecture, dependencies, features, and configuration
* Identify inconsistencies or missing documentation
* Compare current implementation with documented specifications

### 2. **Documentation Synchronization**

* Update `/docs` to match the current code and policies
* Ensure all architectural decisions are properly documented
* Verify that feature documentation reflects actual implementation
* Update dependency lists and configuration examples

### 3. **Quality Assurance**

* Run all tests and security checks locally
* Record any test failures, vulnerabilities, or refactoring needs
* Validate that all CI/CD pipelines are functional
* Check code quality and adherence to standards

### 4. **Reporting & Planning**

* Generate or update `/docs/PROJECT_REASSESSMENT_REPORT.md`
* Update relevant `/docs` files as needed
* Propose the **next logical step** for continued development
* Identify priority items for immediate attention

---

## **Compliance Requirements**

Maintain strict compliance with:

* `/docs/AI_INTERACTION_GUIDE.md` - Agent behavior and automation rules
* `/docs/SECURITY_AND_PRIVACY.md` - Security policies and data protection
* `/docs/TESTING_AND_RELIABILITY.md` - Testing standards and reliability metrics

---

## **Safety Protocol**

⚠️ **Critical**: Do not push to GitHub unless all tests pass locally.

### Pre-commit Checklist:

- [ ] All unit tests pass
- [ ] Integration tests complete successfully  
- [ ] Security scans show no new vulnerabilities
- [ ] Code coverage meets minimum requirements
- [ ] Documentation is synchronized with code
- [ ] No breaking changes without proper versioning

---

## **Deliverables**

### **Assessment Report**
1. Comprehensive analysis of current repository state
2. Gap analysis between code and documentation
3. Test results and quality metrics
4. Security scan results and vulnerability report
5. Performance benchmarks and bottlenecks

### **Updated Documentation**
6. All `/docs` files synchronized with current codebase
7. Architecture documentation reflecting actual structure
8. Updated feature list and capabilities
9. Current dependency list and versions

### **Action Plan**
10. Prioritized next steps with effort estimates
11. Risk assessment for identified issues
12. Quick wins vs. long-term improvements
13. Resource requirements and timeline

### **Documentation Updates**
All reassessment findings and updates must be documented in `/docs/`:

- **`/docs/PROJECT_OVERVIEW.md`**: Update current status, implemented features, and project maturity level
- **`/docs/IMPROVEMENT_AREAS.md`**: Add identified gaps, technical debt items, and optimization opportunities with priority scoring
- **`/docs/REFACTORING_PLAN.md`**: Update task list with newly discovered refactoring needs and mark completed items
- **`/docs/ROADMAP.md`**: Adjust timeline based on reassessment findings, update priorities, and add new milestones

---

## **Success Criteria**

- [ ] Complete alignment between code and documentation
- [ ] All tests passing with adequate coverage (80%+)
- [ ] No outstanding critical or high-severity security vulnerabilities
- [ ] Clear development roadmap established with priorities
- [ ] Automated workflows (CI/CD, testing) functioning properly
- [ ] Architecture documentation matches actual implementation
- [ ] All `/docs/` files are current and accurate
- [ ] Action plan includes specific, measurable next steps
- [ ] **`/docs/` files updated** with reassessment findings and action items

---

## **Best Practices**

### **Regular Assessment Cadence**
- Perform comprehensive reassessments monthly or quarterly
- Quick reassessments after major features or refactors
- Pre-release reassessments to validate readiness
- Post-incident reassessments to capture lessons learned

### **Evidence-Based Analysis**
- Run actual tests and security scans, don't assume
- Compare documentation against actual code (grep, file structure)
- Use metrics and data to support findings
- Document all assumptions and limitations

### **Actionable Recommendations**
- Provide specific, implementable next steps
- Include code examples or references where helpful
- Estimate effort realistically (hours/days, not vague terms)
- Prioritize using impact vs. effort framework

### **Collaborative Process**
- Share findings with team for validation
- Incorporate feedback into action plan
- Use reassessment as learning opportunity
- Celebrate progress and completed work

---

## **Usage Instructions**

### **When to Run This Assessment**

* Starting work on an existing project
* After major feature implementations
* Before important releases
* When documentation feels outdated
* After team changes or handovers
* Periodically (monthly/quarterly) for maintenance
* After security incidents or production issues

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine all existing `/docs/` files to understand documented state
3. Ensure local development environment is properly configured
4. Have access to run tests and security scans

### **Execution**
```
I need a comprehensive project reassessment.

Project context: [brief description of project and current state]
Last assessment: [date or "never"]
Major changes since last assessment: [list recent major changes]
Specific concerns: [any particular areas to focus on]
```

### **Expected Outcome**
The AI will perform a thorough analysis of your entire codebase and documentation, run all available tests and security scans, identify gaps and inconsistencies, update all `/docs/` files to reflect current reality, and provide a prioritized action plan with specific next steps. You'll receive a complete picture of your project's health with clear recommendations for improvement.