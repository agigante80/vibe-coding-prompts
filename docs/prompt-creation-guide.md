# Prompt Creation Guidelines

A comprehensive guide for creating effective, reusable prompts that follow this repository's standards and philosophy.

---

## ⚠️ START HERE: Documentation Review

**BEFORE writing your prompt**, review and update repository documentation:

### **Step 1: Review `/docs/` Directory**

This repository follows a standardized documentation structure (see [Documentation Standardization](./documentation/documentation-standardization.md)):

```
/docs/
├── README.md                  # Entry point and doc index
├── PROJECT_OVERVIEW.md        # Goals, features, technology
├── ARCHITECTURE.md            # System structure and prompts
├── AI_INTERACTION_GUIDE.md    # AI agent usage patterns
├── REFACTORING_PLAN.md        # Ongoing improvements
├── TESTING_AND_RELIABILITY.md # Testing strategies
├── IMPROVEMENT_AREAS.md       # Known gaps and tech debt
├── SECURITY_AND_PRIVACY.md    # Security policies
└── ROADMAP.md                 # Future plans
```

### **Step 2: Check for Relevant Context**

Before creating your prompt, check:

- [ ] **Is this prompt already planned?** → Check `ROADMAP.md` and `IMPROVEMENT_AREAS.md`
- [ ] **Does it address a known gap?** → Review `IMPROVEMENT_AREAS.md`
- [ ] **Does it change the architecture?** → Note updates needed for `ARCHITECTURE.md`
- [ ] **Does it introduce new workflows?** → Plan updates for `AI_INTERACTION_GUIDE.md`
- [ ] **Is there existing documentation?** → Review all `/docs/` files for context

### **Step 3: Update Documentation First**

Update relevant `/docs/` files BEFORE writing your prompt:

- Remove completed items from `IMPROVEMENT_AREAS.md` and `ROADMAP.md`
- Add new features to `PROJECT_OVERVIEW.md`
- Document new workflows in `AI_INTERACTION_GUIDE.md`
- Update `ARCHITECTURE.md` with new prompt categories or structures

**Why this matters**: Your prompt should integrate with existing documentation and generate outputs that align with the standardized `/docs/` structure.

---

## 🎯 Core Principles

Every prompt in this repository follows these fundamental principles:

1. **Generic but Actionable** - Works across different projects while producing specific results
2. **Comprehensive** - Covers the complete workflow, not just isolated tasks
3. **Quality-Focused** - Includes testing, security, and documentation requirements
4. **Automation-Ready** - Designed to work with minimal human intervention
5. **Iterative** - Can be run multiple times to improve results
6. **Vibe-Coding Friendly** - Conversational, creative, and context-aware
7. **Documentation-Aligned** - Generates outputs that follow `/docs/` standardization

---

## � Understanding the `/docs/` Structure

This repository uses a **standardized 9-file documentation system** (from [Documentation Standardization](./documentation/documentation-standardization.md)):

| File | Purpose | Update When |
|------|---------|-------------|
| **`README.md`** | Entry point, setup, usage | New features or setup changes |
| **`PROJECT_OVERVIEW.md`** | Goals, features, tech stack | New capabilities or scope changes |
| **`ARCHITECTURE.md`** | System structure, components | New categories or structural changes |
| **`AI_INTERACTION_GUIDE.md`** | AI agent rules, automation | New prompt workflows or patterns |
| **`REFACTORING_PLAN.md`** | Task checklist, ongoing work | Completing planned improvements |
| **`TESTING_AND_RELIABILITY.md`** | Testing strategy, CI/CD | New testing approaches |
| **`IMPROVEMENT_AREAS.md`** | Known gaps, tech debt | Filling documented gaps |
| **`SECURITY_AND_PRIVACY.md`** | Security policies | Security-related prompts |
| **`ROADMAP.md`** | Future plans, priorities | Completing roadmap items |

### **Your Prompt's Responsibility**

When your prompt generates outputs, it should:

1. **Specify which `/docs/` files to update**
2. **Describe what content to add**
3. **Maintain consistency** with existing documentation
4. **Trigger updates automatically** when code changes

**Example from Test Suite Generator**:
```markdown
After generating test suite, update:
- `/docs/TESTING_AND_RELIABILITY.md` → Add test framework details
- `/docs/ARCHITECTURE.md` → Document test directory structure
- `/docs/README.md` → Add "Running Tests" section
```

---

## �📐 Structure Template

### Standard Prompt Structure

Every prompt should follow this proven structure:

```markdown
# [Prompt Name]

## **Objective**
Clear, concise statement of what this prompt accomplishes.

---

## **Assessment Phase**
### 1. **Project Analysis**
- Auto-detection requirements
- Context gathering
- Technology stack identification

### 2. **[Specific Analysis]**
- Domain-specific assessment
- Standards and frameworks to apply

---

## **[Main Content Sections]**
### [Feature/Area 1]
**What to check/generate**:
- Specific items
- With details

**Code examples** (if applicable):
```language
// Example code
```

### [Feature/Area 2]
[Continue with logical sections]

---

## **Deliverables**
Generate the following:

1. **[Primary Output]** - Description
2. **[Secondary Output]** - Description
3. **[Configuration/Setup]** - Description
4. **[Documentation]** - Description

### **Documentation Updates**

Update the following files in `/docs/`:

- **`/docs/[RELEVANT_FILE].md`**:
  - Specific updates required
  - What to add or modify
  - Links to maintain

---

## **Success Criteria**
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2
- [ ] Quality gates passed
- [ ] Documentation complete

---

## **Best Practices**
* Industry-standard recommendations
* Common pitfalls to avoid
* Optimization strategies

---

## **Usage Instructions**
Run this prompt when:
* Specific scenario 1
* Specific scenario 2
* Regular maintenance cycles
```

---

## 📝 Writing Guidelines

### **Title and Objective**

**Title**: Clear, descriptive, action-oriented
- ✅ "Test Suite Generator"
- ✅ "Security Audit Generator"
- ❌ "Testing Stuff"
- ❌ "Security Things"

**Objective**: One clear sentence explaining the purpose
```markdown
## **Objective**

Generate a comprehensive, production-ready test suite for the current project 
that ensures code quality, catches regressions, and provides confidence for 
continuous deployment.
```

### **Assessment Phase**

Always start with discovery and analysis:

**Good Assessment**:
```markdown
### 1. **Project Analysis**

* Detect project type and language (Python, JavaScript/TypeScript, Java, Go, Rust, etc.)
* Identify existing testing framework or recommend appropriate ones
* Analyze project structure and critical components
* Review existing tests (if any) and assess coverage gaps
```

**Why it works**:
- Auto-detects context (universal/meta-prompt approach)
- Identifies what exists vs. what's needed
- Adapts to any project type

### **Main Content Sections**

Organize by logical groupings:

**For Technical Prompts**: Group by feature/technology
```markdown
## **Security Audit Areas**

### 🔐 **Authentication & Authorization**
[Details...]

### 🛡️ **Input Validation & Injection**
[Details...]

### 🌐 **Web Security Headers**
[Details...]
```

**For Process Prompts**: Group by workflow stages
```markdown
## **Update Strategy**

### **Prioritization Framework**
[Details...]

### **Update Batching**
[Details...]

### **Rollback Strategy**
[Details...]
```

### **Use Concrete Examples**

Always include practical examples:

**Code Examples**:
```markdown
### **Mocking and Fixtures**

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_happy_path(sample_data):
    # Test implementation
```
```

**Command Examples**:
```markdown
```bash
# Node.js vulnerability scanning
npm audit --production
npm outdated

# Python vulnerability scanning
pip-audit
safety check
```
```

**Configuration Examples**:
```markdown
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```
```

### **Multi-Language Support**

Include support for multiple ecosystems:

```markdown
| Language | Tool/Framework | Command |
|----------|---------------|---------|
| **Python** | pytest | `pytest --cov` |
| **JavaScript** | Jest | `npm test` |
| **Java** | JUnit | `mvn test` |
| **Go** | testing | `go test ./...` |
| **Rust** | cargo | `cargo test` |
```

### **Deliverables Section**

Be specific about outputs AND documentation requirements:

**Good Deliverables** (with documentation):
```markdown
## **Deliverables**

Generate the following:

1. **Complete test suite** organized by test type (new + fixed existing)
2. **Test configuration files** (pytest.ini, jest.config.js, etc.)
3. **Fixtures and test data** for reusable components
4. **CI/CD test integration** in existing workflows
5. **Test documentation** explaining how to run and maintain tests

### **Documentation Updates**

Update the following files in `/docs/`:

- **`/docs/TESTING_AND_RELIABILITY.md`**:
  - Add test framework configuration
  - Document test execution commands
  - Include coverage requirements
  - Add CI/CD integration details

- **`/docs/README.md`**:
  - Add link to testing section
  - Include test setup instructions

- **`/docs/ARCHITECTURE.md`** (if needed):
  - Document test organization structure
  - Add test fixture locations
```

**Why it works**:
- Numbered and prioritized
- Specific file types mentioned
- Actionable and measurable
- **Includes `/docs/` update requirements**
- **Specifies which docs to update and what to add**

### **Success Criteria**

Use checkboxes for measurable outcomes:

```markdown
## **Success Criteria**

- [ ] All generated tests pass successfully
- [ ] Code coverage meets minimum thresholds (80%+)
- [ ] Tests run in CI/CD pipeline automatically
- [ ] No flaky or intermittent test failures
- [ ] Documentation explains test structure and maintenance
```

### **Best Practices Section**

Include industry wisdom:

```markdown
## **Best Practices**

### **General Testing**
* Write tests that describe behavior, not implementation
* Keep tests simple and focused on one thing
* Use meaningful assertion messages
* Avoid test interdependencies

### **Preventing Test Skipping**
* Make tests deterministic (no random data, fixed time/dates)
* Isolate tests completely (no shared state)
* Fix failing tests immediately, don't skip them
```

### **Usage Instructions**

Tell users when to apply the prompt:

```markdown
## **Usage Instructions**

Run this prompt when:

* Starting a new project needing test infrastructure
* Adding tests to legacy code without coverage
* Improving existing test suites
* Implementing test-driven development (TDD)
* Preparing for production deployment
```

---

## 📏 Length Guidelines

### **Target Word Count**

Based on our platform compatibility guidelines:

| Prompt Complexity | Word Count | Platform Compatibility |
|------------------|------------|----------------------|
| **Simple** | 300-500 words | All platforms (perfect for Copilot) |
| **Standard** | 600-1000 words | All platforms |
| **Comprehensive** | 1000-1500 words | ChatGPT, Claude, Gemini (Copilot Chat) |
| **Complex** | 1500-2000 words | ChatGPT, Claude, Gemini (Copilot Chat) |
| **Extensive** | 2000-5000 words | ChatGPT, Claude, Gemini |

**Current Repository Range**: 1500-4800 words (comprehensive prompts optimized for major platforms)

### **How to Optimize Length**

**If too short** (< 400 words):
- Add more examples
- Include multi-language support
- Expand best practices
- Add troubleshooting section

**If too long** (> 2000 words):
- Remove redundancy
- Consolidate similar sections
- Move detailed examples to code blocks
- Consider splitting into multiple prompts

---

## 🎨 Formatting Standards

### **Headers**

Use consistent header hierarchy:
```markdown
# Prompt Title (H1 - only once)

## **Major Section** (H2 - bold)

### **Subsection** (H3 - bold)

#### Detail Level (H4 - if needed)
```

### **Lists**

**Unordered lists** for features, checks, items:
```markdown
* First item
* Second item
* Third item
```

**Ordered lists** for steps, deliverables, priorities:
```markdown
1. First step
2. Second step
3. Third step
```

**Checkboxes** for success criteria:
```markdown
- [ ] Criterion 1
- [ ] Criterion 2
```

### **Emphasis**

Use emphasis strategically:
- **Bold** for important terms and section headers
- *Italics* for subtle emphasis or examples
- `Code formatting` for commands, functions, file names
- > Blockquotes for important notes or warnings

### **Tables**

Use tables for structured comparisons:
```markdown
| Category | Description | Example |
|----------|-------------|---------|
| Item 1 | Details | Sample |
| Item 2 | Details | Sample |
```

### **Code Blocks**

Always specify language for syntax highlighting:
````markdown
```bash
# Shell commands
npm test
```

```python
# Python code
def example():
    pass
```

```yaml
# YAML configuration
key: value
```
````

### **Emojis**

Use emojis sparingly for visual scanning:
```markdown
### 🔐 **Security Section**
### 📦 **Dependencies**
### ⚡ **Performance**
```

**Approved emojis**:
- 🔐 Security
- 📦 Dependencies
- ⚡ Performance
- 🧪 Testing
- 📖 Documentation
- 🚀 Deployment
- 🔄 Workflow
- ✅ Success/Complete
- ❌ Failure/Error
- 💡 Tip/Idea
- ⚠️ Warning

---

## 🧪 Testing Your Prompt

### **Validation Checklist**

Before submitting a prompt, verify:

**Structure**:
- [ ] Follows standard template
- [ ] Has all required sections (Objective, Assessment, Deliverables, Success Criteria)
- [ ] Proper header hierarchy (H1 → H2 → H3)
- [ ] Consistent formatting throughout

**Content**:
- [ ] Clear, actionable objective
- [ ] Comprehensive assessment phase
- [ ] Concrete examples (code, commands, configs)
- [ ] Multi-language/platform support
- [ ] Specific deliverables
- [ ] Measurable success criteria
- [ ] Practical best practices
- [ ] Clear usage instructions

**Quality**:
- [ ] Word count within guidelines (400-2000)
- [ ] No spelling or grammar errors
- [ ] Code examples are syntactically correct
- [ ] Commands are tested and working
- [ ] Tables render properly
- [ ] Links are valid

**Meta-Prompt Qualities**:
- [ ] Works across different projects
- [ ] Auto-detects context
- [ ] Adapts to existing setup
- [ ] Provides universal solution
- [ ] Reusable without modification

### **Test with AI**

Before finalizing:

1. **Run the prompt** with ChatGPT/Claude/Copilot
2. **Test on a real project** or sample repository
3. **Verify outputs** match deliverables
4. **Check quality** of generated code/configs
5. **Iterate** based on results

---

## 📂 File Organization

### **Choosing a Category**

Place your prompt in the appropriate folder:

- **`documentation/`** - Creating, maintaining, standardizing docs
- **`devops-automation/`** - CI/CD, deployment, infrastructure
- **`project-management/`** - Assessment, planning, coordination
- **`development-workflow/`** - Development processes, testing, automation
- **`security/`** - Security audits, compliance, vulnerability management

**Not sure?** Consider:
- What's the **primary purpose**?
- What **problem** does it solve?
- What **role** would use it most?

### **Naming Convention**

**Filename**: `kebab-case-descriptive-name.md`

Examples:
- ✅ `test-suite-generator.md`
- ✅ `security-audit-generator.md`
- ✅ `dependency-update-manager.md`
- ❌ `TestSuiteGenerator.md`
- ❌ `test_suite.md`

### **README Updates**

When adding a prompt, update:

1. **Category README** (`[category]/README.md`)
   - Add prompt to "Available Prompts"
   - Include description and usage tips

2. **Main README** (`README.md`)
   - Add to "Available Prompts" section
   - Add to "Quick Selection Guide"
   - Update TODO list (mark as complete)
   - Update word count if showing stats

---

## 💡 Tips for Great Prompts

### **Think Universal**

❌ **Too Specific**:
> "Create a React app with Redux, Material-UI, and specific folder structure"

✅ **Universal**:
> "Detect frontend framework and generate appropriate component library setup with state management"

### **Enable Auto-Detection**

Always start with detection logic:
```markdown
### 1. **Project Analysis**

* Detect project type from files:
  - `package.json` → Node.js
  - `requirements.txt` → Python
  - `pom.xml` → Java
```

### **Provide Fallbacks**

Handle cases where detection fails:
```markdown
* If framework cannot be detected, prompt user for:
  - Project type
  - Preferred tools
  - Existing conventions
```

### **Make It Iterative**

Design prompts that can run multiple times:
```markdown
If [feature] exists:
  - Review and improve
  - Add missing components
  - Update to best practices

If [feature] doesn't exist:
  - Generate from scratch
  - Apply recommended structure
```

### **Include Safety**

Add validation and rollback:
```markdown
### **Rollback Strategy**

If update causes issues:
- Restore from backup
- Revert specific changes
- Document what went wrong
```

### **Write for Humans and AI**

Remember: humans read it first, AI executes it

**For Humans**:
- Clear explanations
- Motivating examples
- Helpful context

**For AI**:
- Specific instructions
- Concrete examples
- Measurable criteria

---

## � Documentation Requirements

Every prompt must align with the repository's documentation standards defined in [Documentation Standardization](./documentation/documentation-standardization.md).

### **Required Documentation Review**

**BEFORE creating your prompt**, review and update `/docs/` if needed:

#### **Step 1: Review Existing Documentation**

Check these files in `/docs/`:

| File | What to Check | Update If |
|------|---------------|-----------|
| `README.md` | Entry point and doc index | Adding new concepts or categories |
| `PROJECT_OVERVIEW.md` | Goals and features | New prompt changes project scope |
| `ARCHITECTURE.md` | Prompt system structure | Adding new category or workflow |
| `REFACTORING_PLAN.md` | Ongoing improvements | Your prompt addresses planned work |
| `IMPROVEMENT_AREAS.md` | Known gaps | Your prompt fills a documented gap |
| `ROADMAP.md` | Future plans | Your prompt aligns with roadmap |

#### **Step 2: Update Documentation**

If your prompt introduces:
- **New category** → Update `ARCHITECTURE.md` with category structure
- **New workflow** → Update `AI_INTERACTION_GUIDE.md` with usage patterns
- **Fills a gap** → Remove from `IMPROVEMENT_AREAS.md` and `ROADMAP.md`
- **New capability** → Add to `PROJECT_OVERVIEW.md` features list

#### **Step 3: Document Your Prompt**

Within your prompt, ensure outputs include:
- Generated files follow `/docs/` structure
- Clear documentation for AI agent usage
- Links to related documentation
- Update triggers for affected `/docs/` files

**Example from existing prompts**:
```markdown
## **Deliverables**

Generate the following:

1. **Complete test suite** organized by test type
2. **Test configuration files** (pytest.ini, jest.config.js, etc.)
3. **Test documentation** explaining how to run and maintain tests
   - Add to `/docs/TESTING_AND_RELIABILITY.md`
   - Update `/docs/README.md` with testing section link
```

### **Documentation Update Triggers**

Your prompt should specify when `/docs/` needs updates:

```markdown
### **Documentation Synchronization**

After generating [feature], update:
- `/docs/ARCHITECTURE.md` → Add [component] structure
- `/docs/TESTING_AND_RELIABILITY.md` → Document test strategy
- `/docs/README.md` → Add setup instructions
```

---

## �🚀 Publishing Your Prompt

### **Pre-Publication Checklist**

**Documentation**:
- [ ] Reviewed `/docs/` for relevant content
- [ ] Updated `/docs/` files as needed
- [ ] Prompt specifies documentation outputs
- [ ] Prompt includes update triggers for `/docs/`

**Prompt Quality**:
- [ ] Prompt tested on real project
- [ ] Word count within guidelines (400-2000)
- [ ] All sections complete per template
- [ ] Code examples verified
- [ ] Multi-language support included
- [ ] Success criteria measurable

**Repository Integration**:
- [ ] Category README updated
- [ ] Main README updated
- [ ] Quick Selection Guide entry added
- [ ] TODO list updated (if applicable)
- [ ] Links all working
- [ ] No TODOs or placeholders

**Review**:
- [ ] Self-reviewed against this guide
- [ ] Tested with AI assistant
- [ ] Reviewed by at least one other person

### **Contribution Process**

1. **Review documentation first**: Check `/docs/` for context and updates needed
2. **Update `/docs/` if needed**: Keep project documentation synchronized
3. **Create branch**: `git checkout -b prompts/add-[prompt-name]`
4. **Add prompt file**: Place in appropriate category folder
5. **Include doc requirements**: Specify `/docs/` updates in deliverables
6. **Update READMEs**: Category and main README
7. **Test thoroughly**: Run on sample projects, verify doc generation
8. **Verify `/docs/` compliance**: Ensure outputs follow standardization
9. **Create PR**: With description of prompt purpose, testing, and doc changes
10. **Respond to feedback**: Iterate based on review

---

## 📖 Examples from This Repository

### **Well-Structured Prompt**

[Test Suite Generator](./development-workflow/test-suite-generator.md) (~1571 words)
- ✅ Clear objective
- ✅ Comprehensive assessment
- ✅ Multi-language support
- ✅ Concrete examples
- ✅ Handles edge cases (skipped tests)
- ✅ Measurable success criteria

### **Concise Yet Complete**

[Project Reassessment](./project-management/project-reassessment.md) (~390 words)
- ✅ Short but actionable
- ✅ Clear deliverables
- ✅ All required sections
- ✅ Perfect for quick audits

### **Comprehensive with Automation**

[Dependency Update Manager](./security/dependency-update-manager.md) (~1630 words)
- ✅ Multi-ecosystem coverage
- ✅ Automation configs included
- ✅ Detailed workflows
- ✅ Safety mechanisms

---

## 🎓 Learning Resources

- [Vibe Coding Philosophy](./docs/vibe-coding.md) - Creative approach to prompting
- [Meta-Prompt System](./docs/universal-meta-Level-prompt-system.md) - Universal prompt design
- [Prompt Creation Guide](./PROMPT_CREATION_GUIDE.md) - This guide (technical limits and best practices)

---

*Remember: Great prompts are iterative. Start simple, test thoroughly, and refine based on real usage.* ✨