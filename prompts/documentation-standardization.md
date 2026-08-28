---
name: documentation-standardization
category: documentation
version: 2.0.0
updated: 2026-08-28
description: Standardize project documentation into the 9-file /docs/ structure with auditing and cleanup.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

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

**All other root `.md` files are CANDIDATES for merging or archiving, never silent deletion.** Community health files GitHub recognizes (`SUPPORT.md`, `GOVERNANCE.md`, issue/PR templates in `.github/`) always stay. **Approval gate: present the full plan (every merge, move, archive, delete with its reason) and act only after the user approves it.** This gate covers root, `/docs/` and subdirectories alike.

Common obsolete files to remove:
- `TODO.md`, `NOTES.md`, `SCRATCH.md`
- `OLD_README.md`, `README.old.md`, `README_backup.md`
- `INSTALL.md` (merge into README.md)
- `USAGE.md` (merge into README.md)
- `API.md` (merge into `/docs/ARCHITECTURE.md`)
- `DEPLOYMENT.md` (operational content: merge into `/docs/ARCHITECTURE.md` or the README's setup section, never into planning docs)
- Any dated or versioned docs: `README_2023.md`, `ARCHITECTURE_v1.md`

---

### **`/docs/` Directory - Standard Documentation Set**

After initialization, `/docs/` contains **9 required markdown files**, optional VERSIONING.md, and any declared extensions:

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

**Summary: `/docs/` holds the 9 required files, optional `VERSIONING.md`, plus DECLARED EXTENSIONS: any additional file is allowed if it is listed with one line of purpose in `docs/README.md`'s index.** An undeclared extra is the finding; the fix is declaring it or merging it, chosen at the approval gate.

**Archive Location**: obsolete files go to `docs/archive/docs-backup-YYYY-MM-DD/`.

**Scope note**: this standard covers MAINTAINER documentation (plans, architecture, policies). User-facing tutorials and how-to guides (Diataxis' learning and task quadrants) are out of scope; keep them wherever the project publishes docs and declare a pointer in `docs/README.md`.

---

## ⚙️ **Agent Task Flow**

### **Step 1. Audit and Clean Existing Documentation**

**Root Directory**:
- List all `.md` files, identify files NOT in allowed list
- For each non-allowed file: merge useful content into standard file, move obsolete to `docs/archive/docs-backup-YYYY-MM-DD/`, or delete if trivial

**`/docs/` Directory**:
- List all files; identify files neither in the 9-file set, nor VERSIONING.md, nor declared in the `docs/README.md` index
- **VERSIONING.md**: if it exists, keep and review it; do not create it
- For each undeclared file: propose (at the approval gate) declaring it as an extension, merging its content, or archiving it
- Final `/docs/`: 9 required files, optional VERSIONING.md, declared extensions, optional `archive/`

**Subdirectories (Outside Root and `/docs/`)**:
- Scan for UPPERCASE `.md` files (e.g., `src/ARCHITECTURE.md`, `lib/CONTRIBUTING.md`, `scripts/DEPLOYMENT.md`)
- **Exception**: `README.md` files are allowed in subdirectories (e.g., `docker/README.md`, `scripts/README.md`)
- For each UPPERCASE `.md` file found:
  - **Review purpose**: Is it general project documentation (belongs in `/docs/` or root)?
  - **Assess placement**: Is it component-specific and legitimately placed (e.g., `docker/TROUBLESHOOTING.md` for Docker-specific troubleshooting)?
  - **Decision**: Move to `/docs/archive/` if obsolete/duplicate, or migrate to appropriate location in `/docs/` or root if still relevant
- Present findings to user for approval before moving/deleting

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

1. The approved cleanup plan, then its execution: root reduced to allowed files, `/docs/` to the standard set plus declared extensions
2. All files following the template structure, cross-referenced, synchronized with the codebase
3. `docs/archive/docs-backup-YYYY-MM-DD/` holding archived material; references to moved docs updated
4. Subdirectory ALL-CAPS `.md` files reviewed and relocated or archived per the approved plan
5. Agent rules configured in `/docs/AI_INTERACTION_GUIDE.md`

---

## 📋 **Success Criteria**

- [ ] Root has ONLY allowed `.md` files (2-6)
- [ ] `/docs/` has the 9 required files; every extra is VERSIONING.md or a declared extension
- [ ] No misplaced UPPERCASE `.md` files in subdirectories (except README.md)
- [ ] Archive folder created if needed
- [ ] All documents complete and current
- [ ] Tests pass, security scan clean
- [ ] Agent rules configured
- [ ] Commit message documents all deleted/archived files

---

## 📋 **Best Practices**

- **Synchronized**: docs update with code changes; pre-commit validation; regular audits
- **Discoverable**: consistent naming, README as entry point, cross-links, TOCs in long docs
- **Quality**: documentation reviewed like code, templates for consistency, rendering validated
- **Living**: version-controlled, obsolete content archived, plans and roadmap kept current

---

## 📋 **Usage Instructions**

### **Initial Setup**
1. Review the [Prompt Creation Guide](../docs/prompt-creation-guide.md) to understand documentation requirements
2. Examine current documentation structure (if any exists)
3. Identify which content needs migration vs. deletion
4. Ensure project has basic testing and CI/CD in place

### **Pre-Execution Validation**
```bash
# Count root .md files (LICENSE may have no extension; check it separately)
find . -maxdepth 1 -name "*.md" | wc -l

# Count /docs/ .md files (9 required + VERSIONING.md + declared extensions)
find docs/ -maxdepth 1 -name "*.md" | wc -l

# Find potentially obsolete files (root and docs/, archive excluded)
find . docs/ -maxdepth 1 \( -iname "*old*.md" -o -iname "*backup*.md" -o -iname "*deprecated*.md" \) 2>/dev/null

# Find ALL-CAPS .md files in subdirectories (README.md and docs/ excluded)
find . -mindepth 2 -type f -name "*.md" ! -name "README.md" \
  ! -path "./docs/*" ! -path "./.git/*" ! -path "./node_modules/*" \
  | grep -E '/[A-Z0-9_]+\.md$' 
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
# Root: allowed files only (max 6 .md plus extensionless LICENSE)
find . -maxdepth 1 -name "*.md"

# /docs/: the 9 required files, optional VERSIONING.md, and every extra
# declared in docs/README.md's index; archive/ excluded
find docs/ -maxdepth 1 -name "*.md"
```

### **Expected Outcome**
After the approved plan executes: root holds only allowed files, `/docs/` holds the standard set plus declared extensions, useful content from removed files is merged, obsolete files sit in the dated archive, agent rules are configured, and the commit message documents every change.

**Output:** Standardized, synchronized documentation ready for development workflow.