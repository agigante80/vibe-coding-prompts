# Documentation Standardization Prompt

## 🎯 **Goal**

Maintain a **comprehensive, synchronized, and secure documentation ecosystem** for this project.
The AI agent must:

1. Generate and standardize all project documentation in `/docs/`
2. Keep every document up-to-date with code changes
3. Enforce local testing before **any commit or GitHub push**
4. Maintain a living **refactoring and security tracking system**

---

## 📁 **Required File Structure**

### **Root Directory - Allowed `.md` Files**

The project root must contain **only** these markdown files:

| Filename                 | Purpose                                      | Required |
| ------------------------ | -------------------------------------------- | -------- |
| `README.md`              | Project overview, setup, and usage           | ✅ Yes    |
| `LICENSE`                | Project license (can be .md or no extension) | ✅ Yes    |
| `CONTRIBUTING.md`        | Contribution guidelines                      | ⚠️ Recommended |
| `CODE_OF_CONDUCT.md`     | Community behavior standards                 | ⚠️ Recommended |
| `CHANGELOG.md`           | Version history and changes                  | ⚠️ Recommended |
| `SECURITY.md`            | Security policy and vulnerability reporting  | ⚠️ Recommended |

**All other `.md` files in root must be deleted or archived.**

Common obsolete files to remove:
- `TODO.md`, `NOTES.md`, `SCRATCH.md`
- `OLD_README.md`, `README.old.md`, `README_backup.md`
- `INSTALL.md` (merge into README.md)
- `USAGE.md` (merge into README.md)
- `API.md` (move to `/docs/API_DOCUMENTATION.md`)
- `DEPLOYMENT.md` (move to `/docs/`)
- Any dated or versioned docs: `README_2023.md`, `ARCHITECTURE_v1.md`

---

### **`/docs/` Directory - Standard Documentation Set**

After initialization, `/docs` must contain **only** the following files:

| Filename                     | Purpose                                                   |
| ---------------------------- | --------------------------------------------------------- |
| `README.md`                  | Entry point with setup, usage, and doc index              |
| `PROJECT_OVERVIEW.md`        | Goals, features, and technology summary                   |
| `ARCHITECTURE.md`            | System structure and component flow                       |
| `AI_INTERACTION_GUIDE.md`    | AI agent rules, automation, and local testing enforcement |
| `REFACTORING_PLAN.md`        | Task checklist for ongoing refactors                      |
| `TESTING_AND_RELIABILITY.md` | Testing and CI policies, reliability strategy             |
| `IMPROVEMENT_AREAS.md`       | Known gaps, missing elements, and tech debt               |
| `SECURITY_AND_PRIVACY.md`    | Security rules, privacy policy, and AI safety             |
| `ROADMAP.md`                 | Priority-based future improvement plan                    |

Any other documents in `/docs` should be **deleted or merged** into one of these.

---

## ⚙️ **Agent Task Flow**

### **Step 1. Audit and Clean Existing Documentation**

**Root Directory Audit:**
1. List all `.md` files in project root
2. Identify files NOT in the allowed list above
3. For each non-allowed `.md` file:
   - If contains useful content: merge into appropriate standard file
   - If obsolete/redundant: move to `/archive/docs-backup-YYYY-MM-DD/` folder
   - If empty or trivial: delete permanently
4. Ensure only allowed `.md` files remain in root

**`/docs/` Directory Audit:**
1. List all files under `/docs/`
2. Identify files NOT in the standard 9-file set
3. For each non-standard file:
   - If contains useful content: merge into appropriate standard document
   - If obsolete/outdated: move to `/archive/docs-backup-YYYY-MM-DD/` folder
   - If duplicate/redundant: consolidate and delete
4. Ensure final `/docs/` contains ONLY the 9 standard files

**Archive Process:**
```bash
# Create timestamped archive folder
mkdir -p archive/docs-backup-$(date +%Y-%m-%d)

# Move obsolete files (examples)
mv OLD_README.md archive/docs-backup-$(date +%Y-%m-%d)/
mv docs/DEPRECATED_GUIDE.md archive/docs-backup-$(date +%Y-%m-%d)/
mv docs/OLD_ARCHITECTURE.md archive/docs-backup-$(date +%Y-%m-%d)/

# Document what was archived
echo "Archived on $(date)" > archive/docs-backup-$(date +%Y-%m-%d)/ARCHIVED_FILES.txt
ls -la archive/docs-backup-$(date +%Y-%m-%d)/ >> archive/docs-backup-$(date +%Y-%m-%d)/ARCHIVED_FILES.txt
```

**Deletion Guidelines:**
- Delete empty or nearly-empty files without hesitation
- Delete obvious duplicates (e.g., `README_old.md`, `README_backup.md`)
- Delete scratch files (e.g., `NOTES.md`, `TODO.md`, `SCRATCH.md`)
- Archive files with potentially useful content for review
- Document all deletions/archives in commit message

---

### **Step 2. Generate or Update Each Document**

Below are detailed requirements for each file.

---

### **`README.md`**

**Goal**: Primary entry point for developers and users.

**Content:**
* Project name and tagline
* Quick overview (1-2 paragraphs)
* Installation/setup steps
* Basic usage examples
* Link to complete documentation index
* License and contribution info

**Requirements:**
* Must include setup validation commands
* Must reference all documents in `/docs`
* Must be updated automatically on significant changes

---

### **`PROJECT_OVERVIEW.md`**

**Goal**: High-level project summary for stakeholders.

**Content:**
* Project mission and objectives
* Key features and capabilities
* Technology stack overview
* Target audience
* Current status and maturity

**Requirements:**
* Update when features are added/removed
* Sync with actual implemented capabilities
* Include version or milestone information

---

### **`ARCHITECTURE.md`**

**Goal**: Technical system design and component relationships.

**Content:**
* System architecture diagram
* Component descriptions and responsibilities
* Data flow and interaction patterns
* Key design decisions and rationale
* Technology choices explanation

**Requirements:**
* Must reflect actual code structure
* Update when major refactors occur
* Include dependency relationships
* Reference actual file/module names

---

### **`AI_INTERACTION_GUIDE.md`**

**Goal**: Rules and policies for AI agent behavior.

**Content:**
* Agent automation boundaries
* Required testing before commits
* Documentation update triggers
* Security and safety constraints
* Human intervention requirements

**Requirements:**
* Must enforce local testing policy
* Must prevent untested GitHub pushes
* Must maintain security standards
* Must be consulted before all agent actions

---

### **`REFACTORING_PLAN.md`**

**Goal**: Living task list for ongoing improvements.

**Content:**
* Current refactoring priorities
* Task breakdown with estimates
* Completion tracking
* Dependency relationships
* Risk assessment for each task

**Requirements:**
* Update after each completed task
* Maintain current status
* Link to related GitHub issues/PRs
* Track time investment

---

### **`TESTING_AND_RELIABILITY.md`**

**Goal**: Testing strategy and reliability policies.

**Content:**
* Testing framework and tools
* Test coverage requirements
* CI/CD pipeline configuration
* Local testing procedures
* Performance benchmarks

**Requirements:**
* Must enforce pre-commit testing
* Must define coverage thresholds
* Must document all test types
* Must include reliability metrics

---

### **`IMPROVEMENT_AREAS.md`**

**Goal**: Technical debt and enhancement tracking.

**Content:**
* Known limitations and gaps
* Performance optimization opportunities
* Technical debt items
* Feature enhancement ideas
* Third-party dependency updates

**Requirements:**
* Regular review and updates
* Prioritization scoring
* Effort estimation
* Impact assessment

---

### **`SECURITY_AND_PRIVACY.md`**

**Goal**: Security policies and privacy protection.

**Content:**
* Security best practices
* Data handling policies
* Access control requirements
* Vulnerability management
* Privacy compliance

**Requirements:**
* Must be reviewed before security changes
* Must comply with applicable regulations
* Must address AI safety concerns
* Must include incident response procedures

---

### **`ROADMAP.md`**

**Goal**: Future development planning and priorities.

**Content:**
* Short-term goals (next 1-3 months)
* Medium-term objectives (3-12 months)
* Long-term vision (1+ years)
* Resource requirements
* Milestone definitions

**Requirements:**
* Regular updates based on progress
* Stakeholder input incorporation
* Realistic timeline estimates
* Clear success criteria

---

## 🚨 **Critical Automation Rules**

### **Before Any Commit or Push:**

1. **Run Full Test Suite** → All tests must pass locally
2. **Security Scan** → No new vulnerabilities introduced
3. **Documentation Sync** → All docs reflect current code state
4. **Refactoring Plan Update** → Mark completed tasks, add new ones

### **Documentation Update Triggers:**

* Code structure changes → Update `ARCHITECTURE.md`
* New features → Update `PROJECT_OVERVIEW.md`, `README.md`
* Security changes → Update `SECURITY_AND_PRIVACY.md`
* Testing changes → Update `TESTING_AND_RELIABILITY.md`
* Task completion → Update `REFACTORING_PLAN.md`

### **Failure Handling:**

* **Test failures** → Block commit, fix issues first
* **Security issues** → Immediate halt, manual review required
* **Documentation gaps** → Generate missing sections automatically
* **Sync conflicts** → Prioritize code truth, update docs to match

---

## 📋 **Deliverables**

### **Standardized Documentation Set**
1. Complete `/docs/` directory with exactly 9 files (no more, no less)
2. All files following the template structure and requirements above
3. Cross-referenced documentation with accurate internal links
4. Synchronized content reflecting current codebase state

### **Root Directory Cleanup**
5. Root directory contains only allowed `.md` files (6 max: README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY)
6. All obsolete/redundant `.md` files removed from root
7. Useful content from removed root files merged into standard docs

### **Cleanup & Migration**
8. Created `/archive/docs-backup-YYYY-MM-DD/` folder with archived files
9. Removed or merged redundant/outdated documentation files from `/docs/`
10. Migrated useful content from deprecated docs into standard files
11. Updated all references to moved/removed documentation
12. Documented all deletions and archives in commit message

### **Automation Configuration**
8. AI agent rules configured in `/docs/AI_INTERACTION_GUIDE.md`
9. Documentation update triggers documented and active
10. Pre-commit testing enforcement in place

### **Documentation Updates**
This prompt creates the entire `/docs/` structure, so all documentation is generated fresh. However, when using this prompt to update existing documentation:

- **All 9 `/docs/` files** will be regenerated or updated to match current project state
- **Cross-references** between files will be validated and corrected
- **Deprecated documentation** outside `/docs/` will be archived or removed

---

## 📋 **Success Criteria**

- [ ] Root directory contains ONLY allowed `.md` files (max 6 files)
- [ ] All obsolete `.md` files removed from root or archived
- [ ] `/docs/` contains ONLY the 9 specified files (no more, no less)
- [ ] `/archive/docs-backup-YYYY-MM-DD/` folder created if files were archived
- [ ] All documents are complete and current
- [ ] Cross-references between documents are accurate
- [ ] All tests pass locally
- [ ] Security scan shows no new issues
- [ ] Agent rules are properly configured in `/docs/AI_INTERACTION_GUIDE.md`
- [ ] Refactoring plan is up-to-date in `/docs/REFACTORING_PLAN.md`
- [ ] Documentation triggers automated updates on code changes
- [ ] Commit message documents all deleted/archived files

---

## 📋 **Best Practices**

### **Keep Documentation Synchronized**
- Update documentation automatically with code changes
- Use pre-commit hooks to validate documentation completeness
- Run documentation audits regularly (weekly/monthly)
- Link documentation updates to feature branches

### **Make Documentation Discoverable**
- Use clear, consistent file naming
- Maintain comprehensive README.md as entry point
- Cross-link related documentation sections
- Include table of contents in longer documents

### **Enforce Quality Standards**
- Define minimum documentation requirements for features
- Review documentation in code review process
- Use templates for consistency
- Validate documentation builds/renders correctly

### **Maintain Living Documentation**
- Treat documentation as code (version control, reviews)
- Archive outdated documentation properly
- Keep refactoring plan current
- Update roadmap based on actual progress

---

## 📋 **Usage Instructions**

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine current documentation structure (if any exists)
3. Identify which content needs migration vs. deletion
4. Ensure project has basic testing and CI/CD in place

### **Pre-Execution Validation**
```bash
# List all .md files in root (should be max 6)
ls -la *.md | wc -l

# List all files in /docs/ (should be exactly 9 after cleanup)
ls -la docs/*.md | wc -l

# Find potentially obsolete files
find . -maxdepth 1 -name "*old*.md" -o -name "*backup*.md" -o -name "*deprecated*.md"
find docs/ -name "*old*.md" -o -name "*backup*.md" -o -name "*deprecated*.md"
```

### **Execution**
```
I need to standardize my project documentation using the /docs/ structure.

Current documentation: [describe what exists, if anything]
Project type: [web app/API/library/CLI tool/etc.]
Team size: [solo/small team/large team]
Compliance needs: [GDPR/HIPAA/PCI-DSS/none]
```

### **Post-Execution Validation**
```bash
# Verify root has only allowed .md files
ls -la *.md
# Should show: README.md, LICENSE(.md), CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md, SECURITY.md (max 6)

# Verify /docs/ has exactly 9 files
ls -la docs/*.md | wc -l
# Should output: 9

# List /docs/ files to confirm standard set
ls -1 docs/
# Should show exactly:
# README.md
# PROJECT_OVERVIEW.md
# ARCHITECTURE.md
# AI_INTERACTION_GUIDE.md
# REFACTORING_PLAN.md
# TESTING_AND_RELIABILITY.md
# IMPROVEMENT_AREAS.md
# SECURITY_AND_PRIVACY.md
# ROADMAP.md

# Verify archive folder created (if applicable)
ls -la archive/docs-backup-*/
```

### **Expected Outcome**
The AI will:
1. **Audit** all `.md` files in root and `/docs/` directories
2. **Archive** obsolete files to `/archive/docs-backup-YYYY-MM-DD/`
3. **Delete** empty, duplicate, or trivial markdown files
4. **Merge** useful content from removed files into standard documents
5. **Create or update** all 9 required `/docs/` files with complete content
6. **Clean root directory** to contain only allowed `.md` files (max 6)
7. **Configure** AI agent rules for automated updates
8. **Establish** a living documentation system synchronized with codebase

You'll receive a clean, standardized documentation structure with:
- Root directory: max 6 `.md` files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY)
- `/docs/` directory: exactly 9 standard files
- `/archive/` folder: timestamped backup of removed files
- Commit message: documentation of all changes

---

**Output:** Updated `/docs` directory with standardized, synchronized documentation ready for development workflow.