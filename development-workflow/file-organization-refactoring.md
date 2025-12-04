# File & Folder Organization Refactoring

## **Objective**

Systematically reorganize project files and folders to establish clear structure, remove obsolete files, standardize naming conventions, and improve codebase maintainability while ensuring the application continues to function correctly throughout the process.

---

## **Assessment Phase**

### 1. **Current State Analysis**

**Discover Existing Structure**:
```bash
# Generate complete directory tree
tree -L 4 -I 'node_modules|vendor|dist|build|__pycache__|.git' > current-structure.txt

# Find all files by type
find . -type f -not -path "*/node_modules/*" -not -path "*/vendor/*" \
  -not -path "*/.git/*" | sed 's|^\./||' | sort > all-files.txt

# Identify file extensions
find . -type f -not -path "*/node_modules/*" -not -path "*/vendor/*" | \
  sed 's/.*\.//' | sort | uniq -c | sort -rn

# Find potential issues
find . -maxdepth 1 -type f -name "*.js" -o -name "*.py" -o -name "*.java"  # Source in root
find . -type f -name "*.bak" -o -name "*.old" -o -name "*_old.*" -o -name "*.tmp"
find . -type f -name "test_*" -o -name "*_test.*" | grep -v "/tests/"  # Tests outside test dirs
```

**Analyze Project Type**:
- Detect programming language and framework
- Identify project structure pattern (MVC, layered, feature-based, monorepo)
- Review package manager files (package.json, requirements.txt, etc.)
- Check existing documentation for architecture decisions

### 2. **Problem Identification**

**Structural Issues**:
- [ ] **Flat Structure** - Too many files in root or top-level directories
- [ ] **Mixed Concerns** - Business logic, tests, and utilities mixed together
- [ ] **Unclear Hierarchy** - No clear separation of modules or features
- [ ] **Inconsistent Depth** - Some areas deeply nested, others completely flat
- [ ] **Scattered Files** - Related files spread across multiple directories

**File Issues**:
- [ ] **Orphaned Files** - Files with no clear purpose or ownership
- [ ] **Duplicate Files** - Same content or functionality in multiple files
- [ ] **Obsolete Files** - Backup files, old versions, deprecated code
- [ ] **Misplaced Files** - Files in wrong directories (tests in src, configs in root)
- [ ] **Naming Inconsistencies** - Mixed conventions (camelCase, snake_case, kebab-case)

**Common Anti-Patterns**:
```
❌ BAD Structure:
project/
├── app.js
├── utils.js
├── helper.js
├── database.js
├── auth.js
├── user.js
├── test_app.js
├── config.json
├── old_app.js.bak
├── README.md
└── [50+ more files in root]

✅ GOOD Structure:
project/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── app.js
├── tests/
│   ├── unit/
│   └── integration/
├── config/
├── docs/
└── README.md
```

### 3. **Target Structure Definition**

**Standard Project Structure by Type**:

**Web Application** (Node.js/Python/Ruby):
```
project/
├── src/                    # Source code
│   ├── controllers/        # Request handlers
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── middleware/        # Middleware functions
│   ├── routes/            # Route definitions
│   ├── utils/             # Utility functions
│   ├── config/            # Configuration loaders
│   └── app.js             # Application entry point
├── tests/                 # All tests
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data
├── config/                # Configuration files
│   ├── development.json
│   ├── production.json
│   └── test.json
├── docs/                  # Documentation
├── scripts/               # Build/deployment scripts
├── public/                # Static assets (if web app)
└── package.json
```

**Library/Package**:
```
library/
├── src/                   # Source code
│   ├── core/             # Core functionality
│   ├── utils/            # Utilities
│   └── index.js          # Main export
├── tests/                # All tests
├── examples/             # Usage examples
├── docs/                 # Documentation
├── scripts/              # Build scripts
└── package.json
```

**CLI Tool**:
```
cli-tool/
├── src/
│   ├── commands/         # CLI commands
│   ├── utils/            # Utilities
│   ├── config/           # Configuration
│   └── cli.js            # CLI entry point
├── tests/
├── docs/
└── bin/                  # Executable scripts
```

**Microservices**:
```
microservices/
├── services/
│   ├── auth/
│   │   ├── src/
│   │   ├── tests/
│   │   └── package.json
│   ├── users/
│   │   ├── src/
│   │   ├── tests/
│   │   └── package.json
│   └── payments/
├── shared/               # Shared utilities
├── config/
└── docs/
```

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
grep -r "require\|import\|from" --include="*.js" --include="*.ts" \
  --include="*.py" . > imports.txt

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

**Step 1: Create New Directory Structure**:
```bash
# Create all target directories
mkdir -p src/{controllers,models,services,middleware,routes,utils,config}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p config docs scripts

# Verify structure
tree -L 2 src/ tests/
```

**Step 2: Move Files Incrementally**:

**⚠️ CRITICAL: Move one file at a time, test after each move**

```bash
#!/bin/bash
# safe-move.sh - Move file and update imports

move_file() {
  local source="$1"
  local target="$2"
  
  echo "Moving: $source → $target"
  
  # Create target directory
  mkdir -p "$(dirname "$target")"
  
  # Move file
  git mv "$source" "$target"
  
  # Update imports in all files
  # (example for JavaScript - adjust for your language)
  find . -type f -name "*.js" -exec sed -i \
    "s|require('$source')|require('$target')|g" {} \;
  
  # Run tests
  npm test
  
  if [ $? -eq 0 ]; then
    echo "✅ Move successful, tests passing"
    git add -A
    git commit -m "refactor: move $source to $target"
  else
    echo "❌ Tests failed, reverting"
    git reset --hard
    exit 1
  fi
}

# Execute moves one by one
move_file "app.js" "src/app.js"
move_file "database.js" "src/config/database.js"
# ... continue for each file
```

**Step 3: Update Import Paths**:

**For JavaScript/TypeScript**:
```bash
# Find all imports of moved file
grep -r "require.*app\.js" --include="*.js"
grep -r "from.*app\.js" --include="*.js"

# Use find/replace or automated tool
npx codemod --transform update-imports.js
```

**For Python**:
```bash
# Find all imports
grep -r "^import\|^from" --include="*.py"

# Update systematically
sed -i 's/from app import/from src.app import/g' **/*.py
```

**Step 4: Rename Files**:
```bash
#!/bin/bash
# Rename with import updates

rename_file() {
  local old_name="$1"
  local new_name="$2"
  
  # Use git mv to preserve history
  git mv "$old_name" "$new_name"
  
  # Update all references
  find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
    -exec sed -i "s|$old_name|$new_name|g" {} \;
  
  # Test and commit
  npm test && git add -A && git commit -m "refactor: rename $old_name to $new_name"
}

rename_file "src/utils.js" "src/utils/helpers.js"
```

**Step 5: Delete Obsolete Files**:
```bash
#!/bin/bash
# Only delete after confirming not in use

delete_file() {
  local file="$1"
  
  echo "Checking if $file is referenced..."
  
  # Search for any references
  if grep -r "$file" --include="*.js" --include="*.py" --include="*.json" . ; then
    echo "⚠️  File is still referenced, cannot delete safely"
    return 1
  fi
  
  # Check git history usage
  if git log --all --full-history --source -- "$file" | grep -q "commit"; then
    echo "📝 File has history, documenting in CHANGELOG"
  fi
  
  # Safe delete with git
  git rm "$file"
  git commit -m "refactor: remove obsolete file $file"
  
  echo "✅ Deleted $file"
}

# Delete only confirmed obsolete files
delete_file "old_app.js.bak"
delete_file "temp.js"
delete_file "config.old.json"
```

### **Phase 3: Verification**

**1. Test Suite Validation**:
```bash
# Run complete test suite
npm test                    # or pytest, mvn test, etc.
npm run test:integration
npm run test:e2e

# Verify coverage maintained
npm run test:coverage
```

**2. Import Path Verification**:
```bash
# Check for broken imports (language-specific)

# JavaScript/TypeScript
npx tsc --noEmit           # TypeScript check
npm run lint

# Python
python -m py_compile **/*.py
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

Add new section or create file if it doesn't exist:

```markdown
## File Organization Refactoring

### Current Issues
- [List identified structural problems]
- [List obsolete files]
- [List naming inconsistencies]

### Target Structure
```
[Show target directory tree]
```

### File Migration Plan

#### Phase 1: Core Files (Week 1)
| Current Path | Target Path | Reason | Status |
|--------------|-------------|--------|--------|
| `app.js` | `src/app.js` | Move source to src/ | ⬜ |
| `database.js` | `src/config/database.js` | Clarify purpose | ⬜ |

#### Phase 2: Test Files (Week 2)
| Current Path | Target Path | Reason | Status |
|--------------|-------------|--------|--------|
| `test_app.js` | `tests/unit/app.test.js` | Organize tests | ⬜ |

#### Phase 3: Cleanup (Week 3)
| File | Action | Reason | Status |
|------|--------|--------|--------|
| `old_app.js.bak` | Delete | Obsolete backup | ⬜ |
| `temp.js` | Delete | Temporary file | ⬜ |

### Import Path Updates Required
- Update all imports of `./app.js` to `./src/app.js` (23 files)
- Update all imports of `../utils.js` to `../utils/helpers.js` (15 files)

### Risk Assessment
- **Risk Level**: Medium
- **Estimated Time**: 3 weeks
- **Testing Required**: Full regression test suite
- **Rollback Plan**: Git revert commits, restore from backup

### Success Criteria
- [ ] All files in logical directories
- [ ] No files in root except essential project files
- [ ] Consistent naming conventions
- [ ] All tests passing
- [ ] Build successful
- [ ] Application starts and runs correctly
- [ ] All obsolete files removed
- [ ] Documentation updated
```

---

## **Deliverables**

### **Planning Documents**
1. **Current Structure Report** - Complete directory tree and file inventory
2. **File Organization Plan** - Detailed mapping of all moves, renames, deletions
3. **Dependency Analysis** - List of import paths requiring updates
4. **Risk Assessment** - Potential issues and mitigation strategies

### **Execution Tracking**
5. **Migration Scripts** - Automated scripts for safe file operations
6. **Progress Tracker** - Status of each file operation (completed, pending, blocked)
7. **Test Results Log** - Test outcomes after each change
8. **Rollback Procedures** - Steps to undo changes if issues arise

### **Updated Documentation**
9. **Updated `/docs/REFACTORING_PLAN.md`** - File organization section added/updated
10. **Updated `/docs/ARCHITECTURE.md`** - Reflect new directory structure
11. **Updated `/docs/DEVELOPMENT_WORKFLOW.md`** - New file locations and import conventions
12. **Updated README.md** - Project structure section updated

### **Verification Reports**
13. **Import Verification Report** - Confirmation all imports updated correctly
14. **Test Suite Report** - All tests passing post-reorganization
15. **Build Verification Report** - Successful build with new structure
16. **Application Health Report** - App runs correctly with new structure

---

## **Success Criteria**

- [ ] Clear, logical directory structure established
- [ ] All source files in appropriate directories (src/, lib/, etc.)
- [ ] All tests in dedicated test directory with clear organization
- [ ] Configuration files centralized in config/ directory
- [ ] Documentation files in docs/ directory
- [ ] No source code files in project root
- [ ] All obsolete files removed (backups, temp files, old versions)
- [ ] Consistent naming conventions across all files
- [ ] All import paths updated and working
- [ ] Complete test suite passing (100% green)
- [ ] Application builds successfully
- [ ] Application runs correctly in all environments
- [ ] No increase in complexity or coupling
- [ ] Git history preserved (used git mv, not rm + add)
- [ ] Team trained on new structure
- [ ] Documentation updated to reflect new structure

---

## **Best Practices**

### **Safety First**
- **Never move multiple files simultaneously** - One file at a time with testing
- **Always use `git mv`** - Preserves file history
- **Test after every change** - Catch issues immediately
- **Commit frequently** - Small, atomic commits for easy rollback
- **Keep backup** - Branch or tag before starting major reorganization

### **Communication**
- **Notify team before starting** - Avoid merge conflicts
- **Document every change** - Clear commit messages
- **Update team during process** - Progress reports
- **Conduct team walkthrough** - Review new structure together

### **Incremental Approach**
- **Start with least-coupled files** - Build confidence
- **Move leaf nodes first** - Files with no dependencies
- **Update imports progressively** - Systematic approach
- **Defer risky moves** - Save complex files for later

### **Validation**
- **Automated tests are essential** - Can't refactor safely without them
- **Add tests if missing** - Before reorganizing
- **Run full test suite** - After each significant change
- **Verify in all environments** - Dev, staging, production

### **Documentation**
- **Update docs in same commit** - Keep in sync
- **Explain reasoning** - Why files moved
- **Document new conventions** - Help team adopt new structure
- **Update onboarding materials** - New developer guide

---

## **Usage Instructions**

### **When to Run This Refactoring**

* Project has grown organically with unclear structure
* Files scattered across directories with no organization
* Root directory cluttered with many files
* Tests mixed with source code
* Difficult to find files or understand project layout
* Onboarding new developers is challenging
* Preparing for major refactoring or feature development
* Before transitioning to monorepo or microservices

### **Initial Setup**
1. Review current project structure and identify issues
2. Ensure comprehensive test suite exists (add tests if needed)
3. Create feature branch for reorganization work
4. Back up current state (tag or branch)
5. Review with team and get approval for target structure
6. Schedule reorganization during low-activity period

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
The AI will analyze your current project structure, identify organizational issues and obsolete files, propose a clear target structure aligned with best practices for your project type, generate a detailed migration plan with file moves/renames/deletions, provide safe execution scripts that test after each change, update all import paths automatically, verify the application works correctly throughout, integrate the plan into `/docs/REFACTORING_PLAN.md`, and provide complete documentation of the new structure. You'll have a well-organized codebase with logical file placement, consistent naming, and no obsolete files, while maintaining full application functionality.

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
**Problem**: Using `rm` + `add` instead of `git mv` loses file history
**Solution**:
- Always use `git mv` for moves and renames
- Use `git log --follow` to verify history preserved
- Avoid bulk operations without git awareness

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
    git reset --hard HEAD~1
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
