---
name: documentation-standardization
category: documentation
version: 2.0.0
updated: 2026-08-28
description: Standardize project documentation into the required /docs/ set plus declared extensions, with approval-gated cleanup.
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

The project root contains only these markdown files, plus any GitHub-recognized community health files (`SUPPORT.md`, `GOVERNANCE.md`), which always stay:

| Filename                 | Purpose                                      | Keep in Root? |
| ------------------------ | -------------------------------------------- | ------------- |
| `README.md`              | Project overview, setup, and usage           | ✅ YES - Required |
| `LICENSE` or `LICENSE.md`| Project license                              | ✅ YES - Required |
| `CONTRIBUTING.md`        | Contribution guidelines                      | ✅ YES - Recommended |
| `CODE_OF_CONDUCT.md`     | Community behavior standards                 | ✅ YES - Recommended |
| `CHANGELOG.md`           | Version history and changes                  | ✅ YES - Recommended |
| `SECURITY.md`            | Security policy and vulnerability reporting  | ✅ YES - Recommended |

**Summary: 2 required + 4 recommended files, plus community health files.**

**All other root `.md` files are CANDIDATES for merging or archiving, never silent deletion.** Community health files GitHub recognizes (`SUPPORT.md`, `GOVERNANCE.md`, issue/PR templates in `.github/`) always stay. **Approval gate: present the full plan (every merge, move, archive, delete with its reason) and act only after the user approves it.** This gate covers root, `/docs/` and subdirectories alike.

Typical CANDIDATES to propose at the approval gate:
- `TODO.md`, `NOTES.md`, `SCRATCH.md`; `OLD_README.md`, `README_backup.md`; dated copies (`README_2023.md`)
- `INSTALL.md` (propose merging into the README's setup section)
- `USAGE.md`, `API.md`: user-facing content per the scope note below; if trivial, propose merging usage into the README; substantial guides and reference stay with the project's published docs, declared as extensions or pointers
- `DEPLOYMENT.md` (operational: propose merging into `/docs/ARCHITECTURE.md` or the README, never planning docs)

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
- For each non-allowed file, PROPOSE at the approval gate: merge useful content into a standard file, archive to `docs/archive/docs-backup-YYYY-MM-DD/`, or delete only trivially empty files

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

**Deletion Guidelines** (within the approved plan only): empty files and byte-identical duplicates may be proposed for deletion; anything with potentially useful content is archived, never deleted. The commit message documents every action.

---

### **Step 2. Generate or Update Each Document**

Below are requirements for each required file (if VERSIONING.md exists, review and update it as needed):

| File | Must contain | Update when |
|------|--------------|-------------|
| README.md | Name, overview, setup with validation commands, usage, doc links | Setup or features change |
| PROJECT_OVERVIEW.md | Mission, features, stack, audience, status | Capabilities change |
| ARCHITECTURE.md | Diagram, components, data flow, decisions; reflects actual code | Major refactors |
| AI_INTERACTION_GUIDE.md | Agent boundaries, testing enforcement, doc triggers | Workflow changes |
| REFACTORING_PLAN.md | Priorities, task breakdown, tracking | Each task |
| TESTING_AND_RELIABILITY.md | Frameworks, coverage floors, CI, pre-commit policy | Testing changes |
| IMPROVEMENT_AREAS.md | Limitations, debt, enhancement opportunities | Regular review |
| SECURITY_AND_PRIVACY.md | Practices, data handling, access, vulnerability process | Security changes |
| ROADMAP.md | Short/medium/long goals, milestones | Progress |

---

## 🚨 **Critical Automation Rules**

**Before any commit or push**: full test suite passes locally, security scan clean, docs synchronized, refactoring plan current.

**Update triggers**: the "update when" column above binds each doc to its code events.

**Failure handling**: test failures block the commit; security issues halt for manual review; documentation gaps generate missing sections; on sync conflicts, code is truth and docs follow.

---

## 📋 **Deliverables**

1. The approved cleanup plan, then its execution: root reduced to allowed files, `/docs/` to the standard set plus declared extensions
2. All files following the template structure, cross-referenced, synchronized with the codebase
3. `docs/archive/docs-backup-YYYY-MM-DD/` holding archived material; references to moved docs updated
4. Subdirectory ALL-CAPS `.md` files reviewed and relocated or archived per the approved plan
5. Agent rules configured in `/docs/AI_INTERACTION_GUIDE.md`

---

## 📋 **Success Criteria**

- [ ] Root has only allowed files plus community health files
- [ ] `/docs/` has the 9 required files; every extra is VERSIONING.md or a declared extension
- [ ] No misplaced UPPERCASE `.md` files in subdirectories (except README.md)
- [ ] Archive folder created if needed
- [ ] All documents complete and current
- [ ] Tests pass, security scan clean
- [ ] Agent rules configured
- [ ] Commit message documents all deleted/archived files

---

## 📋 **Best Practices**

Docs update with code (pre-commit validation, regular audits); README as entry point with cross-links; documentation reviewed like code; obsolete content archived, plans kept current.

---

## 📋 **Usage Instructions**

### **Initial Setup**
1. Examine the current documentation structure and identify migration candidates
2. Ensure basic testing and CI/CD exist (the automation rules depend on them)

### **Pre-Execution Checks**
```bash
# List root .md files: expect the allowed set plus community health files
# (LICENSE may have no extension; check it separately)
find . -maxdepth 1 -name "*.md"

# Count /docs/ .md files (9 required + VERSIONING.md + declared extensions)
find docs/ -maxdepth 1 -name "*.md" | wc -l

# Find potentially obsolete files: root (top level) and ALL of docs/
# except the archive
find . -maxdepth 1 \( -iname "*old*.md" -o -iname "*backup*.md" -o -iname "*deprecated*.md" \)
find docs/ -path docs/archive -prune -o -type f \
  \( -iname "*old*.md" -o -iname "*backup*.md" -o -iname "*deprecated*.md" \) -print 2>/dev/null

# Find ALL-CAPS .md files in subdirectories. README.md, docs/, .github/
# (community/template files stay) and dependency trees are excluded;
# `|| true` keeps a clean tree exiting 0.
find . -mindepth 2 -type f -name "*.md" ! -name "README.md" \
  ! -path "./docs/*" ! -path "./.git/*" ! -path "./.github/*" \
  ! -path "*/node_modules/*" ! -path "*/vendor/*" \
  | grep -E '/[A-Z0-9_-]+\.md$' || true
```

### **Execution**
```
Standardize my project documentation using the /docs/ structure.
Current documentation: [what exists]
Project type: [web app/API/library/CLI/etc.]
Compliance needs: [GDPR/HIPAA/PCI-DSS/none]
```

### **Post-Execution Validation**
```bash
# Every required file exists (assertable pass condition)
for f in README PROJECT_OVERVIEW ARCHITECTURE AI_INTERACTION_GUIDE \
         REFACTORING_PLAN TESTING_AND_RELIABILITY IMPROVEMENT_AREAS \
         SECURITY_AND_PRIVACY ROADMAP; do
  [ -f "docs/$f.md" ] || echo "MISSING docs/$f.md"
done

# Root and /docs/ inventories match the approved plan
find . -maxdepth 1 -name "*.md"
find docs/ -maxdepth 1 -name "*.md"

# If the plan archived anything, the dated folder must exist
ls -d docs/archive/docs-backup-* 2>/dev/null
```

### **Expected Outcome**
After the approved plan executes: root and `/docs/` match the contract, merged content preserved, archives dated, agent rules configured, every change documented in the commit.

**Output:** Standardized, synchronized documentation ready for development workflow.