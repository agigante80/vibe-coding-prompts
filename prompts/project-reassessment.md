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

### 2.1. **Documentation Sanitization & Conflict Resolution**

**Audit All `/docs` Files**:
- List all documentation files and their stated purposes
- Identify duplicate documentation covering the same topics
- Flag contradictory information across different documents
- Find outdated documentation that no longer reflects current code

**Standardization Requirements**:
- **Single Source of Truth**: Each topic should have ONE authoritative document
- **Clear Ownership**: Each document should have a clearly defined scope
- **Consistent Naming**: Follow standardized naming conventions (`UPPERCASE_WITH_UNDERSCORES.md`)
- **Cross-Reference Validation**: Ensure all internal links between docs are valid
- **Version Consistency**: All docs should reflect the same version of the project

**Conflict Resolution Process**:
```bash
# Find duplicate or similar documentation
find docs/ -name "*.md" -exec basename {} \; | sort | uniq -d

# Check for contradictory statements (manual review needed)
grep -r "architecture" docs/
grep -r "framework" docs/
grep -r "version" docs/
```

**Common Conflict Patterns to Resolve**:
- **Architecture Descriptions**: Multiple files describing system architecture differently
- **API Documentation**: Scattered endpoint documentation vs. centralized API docs
- **Setup Instructions**: Conflicting installation/configuration steps in different files
- **Feature Lists**: Inconsistent feature status (planned vs. implemented)
- **Configuration**: Different default values or settings documented in multiple places
- **Dependencies**: Conflicting version requirements or package lists

**Consolidation Strategy**:
1. **Identify Authoritative Document**: Choose the most complete, accurate, and current version
2. **Merge Information**: Consolidate unique information from duplicates into authoritative doc
3. **Remove Duplicates**: Delete redundant files after merging content
4. **Update References**: Fix any links pointing to removed documents
5. **Add Redirects**: If needed, add notes in README about removed docs

**Required Standard Documents** (from Documentation Standardization prompt):
- `README.md` - Entry point with setup, usage, and doc index
- `PROJECT_OVERVIEW.md` - High-level project description and status
- `ARCHITECTURE.md` - System architecture and design decisions
- `AI_INTERACTION_GUIDE.md` - Agent behavior and automation rules
- `REFACTORING_PLAN.md` - Planned code improvements and roadmap
- `TESTING_AND_RELIABILITY.md` - Testing strategy and quality gates
- `IMPROVEMENT_AREAS.md` - Technical debt and areas needing work
- `SECURITY_AND_PRIVACY.md` - Security policies and data protection
- `ROADMAP.md` - Priority-based future improvement plan

**Note**: `/docs/` must contain exactly these 9 files. Any other documentation should be deleted, merged into these files, or archived to `docs/archive/docs-backup-YYYY-MM-DD/`.

**Detect Contradictions**:
- Compare version numbers across all docs
- Check for conflicting technology choices (e.g., "we use MySQL" vs. "we use PostgreSQL")
- Identify inconsistent terminology or naming conventions
- Flag different workflow descriptions (e.g., conflicting branching strategies)
- Find contradictory configuration instructions

**Documentation Quality Checks**:
- [ ] No duplicate files covering the same topic
- [ ] No contradictory information across documents
- [ ] All cross-references and internal links are valid
- [ ] Consistent terminology and naming conventions
- [ ] All docs reflect current codebase (no outdated information)
- [ ] Clear document hierarchy and organization
- [ ] Each document has a clear, unique purpose
- [ ] Standard documents from Documentation Standardization prompt exist
- [ ] Deprecated documents are removed or clearly marked

### 3. **Quality Assurance**

* Run all tests and security checks locally
* Record any test failures, vulnerabilities, or refactoring needs
* Validate that all CI/CD pipelines are functional
* Check code quality and adherence to standards

### 4. **.gitignore Review**

* Verify `.gitignore` is not excluding files that are needed for the project
* Check for missing patterns that should ignore build artifacts, temporary files, or sensitive data
* Organize entries into logical sections with comments (Dependencies, Build Output, IDE, OS, etc.)
* Identify obsolete patterns that no longer match project structure
* Ensure environment-specific files (`.env.example`) are tracked while secrets (`.env`) are ignored
* Validate that documentation, configuration, and source files are not accidentally ignored

### 5. **File Organization Verification**

* Audit all files in the repository to identify their purpose and relevance
* Document the purpose of any ambiguous or unclear files
* Flag files that are most probably not needed anymore (old scripts, deprecated code, unused configurations)
* Identify duplicate files or functionality
* Verify logical directory structure aligns with documented architecture
* Check for orphaned files that should be organized into appropriate directories
* Ensure file naming conventions are consistent across the project

### 6. **Reporting & Planning**

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
6. `.gitignore` audit results with recommended changes
7. File organization analysis with flagged obsolete files
8. **Documentation sanitization report** - Duplicates removed, contradictions resolved, standard docs enforced

### **Updated Documentation**
9. All `/docs` files synchronized with current codebase
10. Consolidated documentation with conflicts resolved
11. Architecture documentation reflecting actual structure
12. Updated feature list and capabilities
13. Current dependency list and versions

### **Action Plan**
14. Prioritized next steps with effort estimates
15. Risk assessment for identified issues
16. Quick wins vs. long-term improvements
17. Resource requirements and timeline

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