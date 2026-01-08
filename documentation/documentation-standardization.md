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

The project root must contain **only** these markdown files (maximum 6):

| Filename                 | Purpose                                      | Keep in Root? |
| ------------------------ | -------------------------------------------- | ------------- |
| `README.md`              | Project overview, setup, and usage           | ✅ YES - Required |
| `LICENSE` or `LICENSE.md`| Project license                              | ✅ YES - Required |
| `CONTRIBUTING.md`        | Contribution guidelines                      | ✅ YES - Recommended |
| `CODE_OF_CONDUCT.md`     | Community behavior standards                 | ✅ YES - Recommended |
| `CHANGELOG.md`           | Version history and changes                  | ✅ YES - Recommended |
| `SECURITY.md`            | Security policy and vulnerability reporting  | ✅ YES - Recommended |

**Summary: Root should have 2-6 `.md` files maximum (2 required + 4 optional recommended).**

**All other `.md` files in root must be deleted or archived.**

Common obsolete files to remove:
- `TODO.md`, `NOTES.md`, `SCRATCH.md`
- `OLD_README.md`, `README.old.md`, `README_backup.md`
- `INSTALL.md` (merge into README.md)
- `USAGE.md` (merge into README.md)
- `API.md` (merge into `/docs/ARCHITECTURE.md`)
- `DEPLOYMENT.md` (merge into `/docs/ROADMAP.md` or `/docs/ARCHITECTURE.md`)
- Any dated or versioned docs: `README_2023.md`, `ARCHITECTURE_v1.md`

---

### **`/docs/` Directory - Standard Documentation Set**

After initialization, `/docs/` must contain **9 required markdown files** (plus optional VERSIONING.md if it already exists):

| # | Filename                     | Purpose                                                   | Keep in /docs/? |
|---|------------------------------|-----------------------------------------------------------|----------------|
| 1 | `README.md`                  | Entry point with setup, usage, and doc index              | ✅ YES - Required |
| 2 | `PROJECT_OVERVIEW.md`        | Goals, features, and technology summary                   | ✅ YES - Required |
| 3 | `ARCHITECTURE.md`            | System structure and component flow                       | ✅ YES - Required |
| 4 | `AI_INTERACTION_GUIDE.md`    | AI agent rules, automation, and local testing enforcement | ✅ YES - Required |
| 5 | `REFACTORING_PLAN.md`        | Task checklist for ongoing refactors                      | ✅ YES - Required |
| 6 | `TESTING_AND_RELIABILITY.md` | Testing and CI policies, reliability strategy             | ✅ YES - Required |
| 7 | `IMPROVEMENT_AREAS.md`       | Known gaps, missing elements, and tech debt               | ✅ YES - Required |
| 8 | `SECURITY_AND_PRIVACY.md`    | Security rules, privacy policy, and AI safety             | ✅ YES - Required |
| 9 | `ROADMAP.md`                 | Priority-based future improvement plan                    | ✅ YES - Required |
| 10 | `VERSIONING.md`             | Version management strategy and release process           | ⚠️ OPTIONAL - Keep if exists, do not create if missing |

**Summary: `/docs/` must have 9 required `.md` files (plus optional VERSIONING.md if it already exists). Any other documents should be deleted, merged, or archived.**

**Archive Location**: Obsolete files from `/docs/` go to `docs/archive/docs-backup-YYYY-MM-DD/`

Any other documents in `/docs/` should be **deleted or merged** into one of these 9 files.

---

## ⚙️ **Agent Task Flow**

### **Step 1. Audit and Clean Existing Documentation**

**Root Directory**:
- List all `.md` files, identify files NOT in allowed list
- For each non-allowed file: merge useful content into standard file, move obsolete to `docs/archive/docs-backup-YYYY-MM-DD/`, or delete if trivial

**`/docs/` Directory**:
- List all files, identify files NOT in standard 9-file set (plus VERSIONING.md if present)
- **VERSIONING.md**: If exists, keep it and review content; if missing, do not create it
- For each non-standard file: merge useful content, move obsolete to archive, consolidate duplicates
- Final `/docs/` must contain 9 required files (plus optional VERSIONING.md if it exists, plus optional `archive/` folder)

**Archive Command**: `mkdir -p docs/archive/docs-backup-$(date +%Y-%m-%d)`

**Deletion Guidelines**: Delete empty files, obvious duplicates (`README_old.md`), scratch files (`NOTES.md`, `TODO.md`). Archive files with potentially useful content. Document all changes in commit.

---

### **Step 2. Generate or Update Each Document**

Below are requirements for each required file (if VERSIONING.md exists, review and update it as needed):

**`README.md`**: Project name/tagline, overview, setup, usage examples, link to `/docs`, license. Must include setup validation commands.

**`PROJECT_OVERVIEW.md`**: Mission, features, tech stack, target audience, status. Update when features change.

**`ARCHITECTURE.md`**: System diagram, component descriptions, data flow, design decisions. Must reflect actual code, update on major refactors.

**`AI_INTERACTION_GUIDE.md`**: Agent automation boundaries, testing requirements, documentation triggers, security constraints. Must enforce local testing policy.

**`REFACTORING_PLAN.md`**: Current priorities, task breakdown with estimates, completion tracking, dependencies. Update after each task.

**`TESTING_AND_RELIABILITY.md`**: Testing framework/tools, coverage requirements, CI/CD config, local procedures. Must enforce pre-commit testing.

**`IMPROVEMENT_AREAS.md`**: Known limitations, performance optimization, technical debt, feature enhancements. Regular review and prioritization.

**`SECURITY_AND_PRIVACY.md`**: Security best practices, data handling, access control, vulnerability management, privacy compliance.

**`ROADMAP.md`**: Short/medium/long-term goals, milestones, resource requirements. Regular updates based on progress.

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
1. Complete `/docs/` directory with 9 required files (plus VERSIONING.md if it already exists)
2. All files following the template structure and requirements above
3. Cross-referenced documentation with accurate internal links
4. Synchronized content reflecting current codebase state

### **Root Directory Cleanup**
5. Root contains only allowed `.md` files (6 max)
6. Obsolete files removed/archived

### **Cleanup & Migration**
7. Created `docs/archive/docs-backup-YYYY-MM-DD/` if needed
8. Merged useful content from removed files
9. Updated references to moved/removed docs

### **Automation Configuration**
10. AI agent rules configured in `/docs/AI_INTERACTION_GUIDE.md`

### **Documentation Updates**
All 9 `/docs/` files regenerated/updated to match current state, cross-references validated.

---

## 📋 **Success Criteria**

- [ ] Root has ONLY allowed `.md` files (2-6)
- [ ] `/docs/` has 9 required files (plus VERSIONING.md if it existed)
- [ ] Archive folder created if needed
- [ ] All documents complete and current
- [ ] Tests pass, security scan clean
- [ ] Agent rules configured
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

# List all files in /docs/ (should be 9 required, plus VERSIONING.md if it exists)
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

# Verify /docs/ has 9 required files (10 if VERSIONING.md exists)
ls -la docs/*.md | wc -l
# Should output: 9 or 10 (if VERSIONING.md exists)

# List /docs/ files to confirm standard set
ls -1 docs/
# Should show these 9 required files:
# README.md
# PROJECT_OVERVIEW.md
# ARCHITECTURE.md
# AI_INTERACTION_GUIDE.md
# REFACTORING_PLAN.md
# TESTING_AND_RELIABILITY.md
# IMPROVEMENT_AREAS.md
# SECURITY_AND_PRIVACY.md
# ROADMAP.md
# Plus VERSIONING.md (optional, only if it existed before)

# Verify archive folder created (if applicable)
ls -la docs/archive/docs-backup-*/

# Verify 9 required .md files in docs/ (plus VERSIONING.md if it exists, excluding archive folder)
find docs/ -maxdepth 1 -name "*.md" | wc -l
# Should output: 9 or 10 (10 only if VERSIONING.md existed before)
```

### **Expected Outcome**
AI will audit/archive/delete `.md` files, merge useful content, create/update all 9 required `/docs/` files, clean root to 2-6 allowed files, and configure AI agent rules.

You'll receive:
- **Root**: 2-6 `.md` files (README, LICENSE, optional: CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, SECURITY)
- **`/docs/`**: 9 required files (plus VERSIONING.md if it existed)
- **`docs/archive/`**: Timestamped backup folder (if needed)
- **Commit message**: Documentation of all changes

---

**Output:** Standardized, synchronized documentation ready for development workflow.