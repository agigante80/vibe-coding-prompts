---
name: file-organization-refactoring
category: development-workflow
version: 1.1.1
updated: 2026-08-28
description: Reorganize project files and folders safely with tested, incremental migrations.
platforms: [chatgpt, claude, gemini, copilot-chat]
---

# File & Folder Organization Refactoring

## **Objective**

Systematically reorganize project files and folders to establish clear structure, remove obsolete files, standardize naming, and improve maintainability while ensuring correct functionality throughout.

---

## **Assessment Phase**

### 1. **Current State Analysis**

- Directory tree: `tree -L 4 -I 'node_modules|vendor|dist|build|__pycache__|.git'`; file list via `find . -type f -not -path "*/node_modules/*" | sort`
- Find issues: source files in root, `.bak`/`.old` files, tests outside test dirs
- Detect language, framework, project pattern (MVC/layered/feature-based)

### 2. **Problem Identification**

**Issues to Check**:
- [ ] Flat structure, mixed concerns, unclear hierarchy
- [ ] Orphaned/duplicate/obsolete or misplaced files (tests in src, configs in root)
- [ ] Naming inconsistencies (camelCase/snake_case/kebab-case mix)

### 3. **Documentation File Cleanup**

Run **[Documentation Standardization](./documentation-standardization.md)** to ensure:
- Root has 2-6 `.md` files (README, LICENSE required)
- `/docs/` has exactly 9 standard `.md` files
- Obsolete docs archived to `docs/archive/docs-backup-YYYY-MM-DD/`

---

### 4. **Target Structure Definition**

**Standard Project Structure**:
```
project/
├── src/                    # Source code (controllers, models, services, utils)
├── tests/                 # All tests (unit, integration, fixtures)
├── config/                # Configuration files
├── docs/                  # Documentation
├── scripts/               # Build/deployment scripts
├── public/                # Static assets (web apps)
└── [package manager files]
```

Adjust for project type (library, CLI, microservices) by adding/removing directories as needed.

---

## **Refactoring Process**

### **Phase 1: Planning (No Changes Yet)**

**1. Create Organization Plan**:
```bash
# Document current → target mappings
cat > file-organization-plan.md << 'EOF'
# File Organization Plan

## Files to Move
- `app.js` → `src/app.js`
- `database.js` → `src/config/database.js`
- `test_app.js` → `tests/unit/app.test.js`

## Files to Rename
- `utils.js` → `src/utils/helpers.js`
- `auth.js` → `src/middleware/authentication.js`

## Files to Delete
- `old_app.js.bak` - Old backup file
- `temp.js` - Temporary test file
- `config.old.json` - Deprecated config

## Directories to Create
- `src/controllers/`
- `src/models/`
- `src/services/`
- `tests/unit/`
- `tests/integration/`

## Import Path Updates Required
- All imports of `./app.js` → `./src/app.js`
- All imports of `../utils.js` → `../utils/helpers.js`
EOF
```

**2. Analyze Dependencies**:
```bash
# Find all import/require statements
# Anchored import statements only (adapt per language); -I skips
# binaries; exclude noise dirs and the output file itself (bash)
grep -rnEI "^\s*(import |from .+ import|const .+ = require|require\()" \
  --exclude-dir={node_modules,.git,dist,build,vendor} \
  --exclude=imports.txt . > imports.txt

# Identify what needs updating when files move
```

**3. Safety Checklist**:
- [ ] All tests passing before starting
- [ ] Branch created for reorganization work
- [ ] Backup of current state
- [ ] Team notified of upcoming changes
- [ ] Documentation of current import paths
- [ ] Plan reviewed and approved

### **Phase 2: Safe Execution**

**Critical Rules**:
- Small repos: move ONE file at a time, test after each
- Large repos: batch moves by cohesive module (one directory per batch), run the affected test subset per move and the full suite per batch; per-file full-suite runs do not scale past a few dozen files
- Use `git mv`, and keep moves in move-only commits (no content edits in the same commit): git detects renames heuristically, and mixing heavy edits into a move can break detection. Verify with `git log --follow <file>`
- Update all import paths immediately
- Run tests before committing
- Commit with clear message: `refactor: move X to Y`

**Process**:
1. Create target directories
2. Move file with `git mv source target`
3. Update imports/references across codebase
4. Run full test suite
5. If tests pass: commit; if fail: revert with `git reset --hard`
6. Repeat for next file

**For deleting obsolete files**: Search for references across ALL files first; an extension whitelist misses Dockerfiles, Makefiles, CI YAML and shell scripts, so exclude noise directories instead (`grep -rn "filename" --exclude-dir={node_modules,.git,dist,build,vendor} .`), and delete only if unreferenced:

```bash
# Delete only confirmed obsolete files (git rm stages the deletion)
git rm old_app.js.bak temp.js config.old.json
git commit -m "refactor: remove obsolete files"
```

### **Phase 3: Verification**

**1. Test Suite Validation**:
```bash
npm test && npm run test:integration && npm run test:e2e   # or pytest etc.
npm run test:coverage   # verify coverage maintained
```

**2. Import Path Verification**:
```bash
# Check for broken imports (language-specific)

# JavaScript/TypeScript
npx tsc --noEmit           # TypeScript check
npm run lint

# Python
find . -name "*.py" -not -path "*/.venv/*" -exec python3 -m py_compile {} +
pylint **/*.py

# Check for common issues
grep -r "require.*\.\./\.\./\.\." --include="*.js"  # Excessive relative paths
```

**3. Build Verification**:
```bash
# Clean build
rm -rf dist/ build/ node_modules/
npm install                 # or pip install, mvn clean install
npm run build

# Verify build succeeds
ls -la dist/
```

**4. Application Verification**:
```bash
# Start application
npm start &
APP_PID=$!

# Wait for startup
sleep 5

# Basic health check
curl http://localhost:3000/health || echo "❌ App failed to start"

# Smoke tests
npm run test:smoke

# Cleanup
kill $APP_PID
```

---

## **Integration with Refactoring Plan**

### **Update `/docs/REFACTORING_PLAN.md`**

Add file organization section with:
- Current issues identified
- Target structure diagram
- File migration table (current path, target path, status)
- Import path updates required
- Risk assessment and success criteria

---

## **Deliverables**

1. **Current Structure Report** - Directory tree and file inventory
2. **File Organization Plan** - Detailed file migration mapping
3. **Migration Scripts** - Safe file operation automation
4. **Test Results Log** - Post-change verification
5. **Updated Documentation** - `/docs/REFACTORING_PLAN.md`, `/docs/ARCHITECTURE.md`, `/docs/README.md`, root `README.md`
6. **Documentation Cleanup** - Run **[Documentation Standardization](./documentation-standardization.md)** for 9-file `/docs/` structure
7. **Verification Reports** - Import validation, test suite, build, application health

---

## **Success Criteria**

- [ ] Clear logical directory structure (src/, tests/, config/, docs/), no source in root
- [ ] All obsolete files removed, consistent naming, imports updated
- [ ] Full test suite passing, application builds/runs
- [ ] Git history preserved (`git mv`), documentation updated

---

## **Best Practices**

**Safety**: small move-only commits via `git mv`, commit frequently, keep a backup branch and snapshot non-git state (schemas, configs)

**Incremental**: start with least-coupled leaf files, update imports progressively, validate with the test suite as you go

**Communication**: notify the team first, clear commit messages, document new conventions, post-change team walkthrough

---

## **Usage Instructions**

### **When to Run This Refactoring**

* Project grew organically: unclear structure, cluttered root, tests mixed with source
* Hard to find files; onboarding new developers is challenging
* Preparing for major refactoring or feature development
* Before transitioning to monorepo or microservices

### **Initial Setup**
1. Review current structure; ensure a comprehensive test suite exists (add tests first if needed)
2. Create a feature branch for the reorganization work
3. Review the target structure with the team and get approval
4. Schedule the work during a low-activity period

### **Execution**
```
I need to reorganize the files and folders in my project.

Project type: [web app/library/CLI/microservices]
Programming language: [JavaScript/Python/Java/etc.]
Current structure issues: [flat structure/mixed concerns/unclear hierarchy]
Number of files to move: [approximate]
Test coverage: [percentage]
Team size: [number of developers]
Urgency: [low/medium/high]
```

### **Expected Outcome**
The AI analyzes the current structure, proposes a target layout for your project type, generates a tested migration plan (moves, renames, deletions, import updates), verifies the application throughout, and documents everything in `/docs/REFACTORING_PLAN.md`.

---

## **Common Pitfalls & Solutions**

### **Pitfall 1: Breaking Imports**
**Problem**: Moving files breaks import paths throughout codebase
**Solution**: 
- Use automated tools (codemod, sed) for bulk updates
- Test after each file move
- Use IDE refactoring tools when available
- Consider gradual migration with aliasing

### **Pitfall 2: Losing Git History**
**Problem**: rename detection is a similarity heuristic, not recorded metadata
**Solution**: `git mv` in move-only commits, verify with `git log --follow`, avoid bulk operations mixing moves and edits

### **Pitfall 3: Circular Dependencies**
**Problem**: Moving files reveals or creates circular dependencies
**Solution**:
- Map dependencies before moving
- Break circular deps before reorganizing
- Consider dependency injection or interface extraction

### **Pitfall 4: Test Failures**
**Problem**: Tests break due to incorrect paths or assumptions
**Solution**:
- Update test imports alongside source imports
- Check for hard-coded paths in tests
- Update test fixtures and mocks
- Run full test suite, not just unit tests

### **Pitfall 5: Build System Confusion**
**Problem**: Build tools can't find files in new locations
**Solution**:
- Update build configuration (webpack, tsconfig, etc.)
- Check include/exclude patterns
- Verify entry points and output paths
- Test build in CI environment

---

## **Example Migration Script**

```bash
#!/bin/bash
# comprehensive-file-migration.sh

set -e  # Exit on any error

echo "🚀 Starting File Organization Refactoring"

# Phase 1: Create Structure
echo "📁 Creating directory structure..."
mkdir -p src/{controllers,models,services,middleware,routes,utils,config}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p config docs scripts

# Phase 2: Move files safely
move_and_test() {
  local source=$1
  local target=$2
  
  echo "📦 Moving: $source → $target"
  
  # Create target dir
  mkdir -p "$(dirname "$target")"
  
  # Move with git
  git mv "$source" "$target"
  
  # Run tests
  echo "🧪 Running tests..."
  npm test
  
  if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
    git commit -m "refactor: move $source to $target"
  else
    echo "❌ Tests failed, reverting"
    git reset --hard HEAD  # discard the staged move; nothing was committed yet
    exit 1
  fi
}

# Execute moves
move_and_test "app.js" "src/app.js"
move_and_test "database.js" "src/config/database.js"
move_and_test "test_app.js" "tests/unit/app.test.js"

# Phase 3: Delete obsolete
echo "🗑️  Removing obsolete files..."
git rm old_app.js.bak temp.js config.old.json
git commit -m "refactor: remove obsolete files"

# Phase 4: Final verification
echo "✨ Running final verification..."
npm test
npm run build
npm run lint

echo "🎉 File organization refactoring complete!"
echo "📊 Summary:"
find src/ tests/ config/ -type f | wc -l | xargs echo "Total organized files:"
git diff --stat HEAD~5 HEAD
```
