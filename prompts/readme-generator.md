# README Generator

## **Objective**

Generate or update a comprehensive, professional README.md file following industry best practices, including optional Docker Hub descriptions (short description must be ≤100 characters), while preserving existing screenshots and images.

---

## **Assessment Phase**

### 1. **Project Analysis**

**Discover Project Identity**:
- Read existing README.md (if present) to preserve screenshots, images, and unique content
- Detect project type (library, CLI tool, web app, API, Docker image, etc.)
- Identify programming language and framework
- Analyze package.json, requirements.txt, pom.xml, Cargo.toml, etc. for metadata
- Review repository structure to understand features and capabilities
- Check for existing CI/CD workflows (.github/workflows/)
- Identify if Docker images are published (Dockerfile, docker-compose.yml)

**Extract Key Information**:
- Project name and version
- Main purpose and problem it solves
- Key features and capabilities
- Dependencies and requirements
- Installation methods available
- Configuration options
- Testing infrastructure
- License information

### 2. **Docker Description Detection**

**Check for Docker Descriptions**:
```bash
# Look for Docker description files
find . -name "short.md" -o -name "description.md" -o -name "docker-description.md"

# Common locations
./docker/description/short.md      # Short description (≤100 chars)
./docker/description/long.md       # Long description
./.docker/short.md
./.docker/description.md
```

**Validate Short Description**:
- Must be ≤100 characters (Docker Hub requirement)
- Should be clear, concise tagline
- No line breaks or special formatting
- Complements the README title

### 3. **Existing Content Preservation**

**Identify Content to Preserve**:
- Screenshots and images (![alt](path))
- GIFs and video embeds
- Custom diagrams and architecture visuals
- Unique examples or demos
- Specific configuration snippets user has added
- Custom badges or shields

---

## **README Structure Guidelines**

### 📋 **Required Sections** (Every README)

1. **Project Identity**: Title with logo, tagline, badges (build, version, license)
2. **Table of Contents**: For READMEs >200 lines, linked navigation
3. **About/Description**: What it does, problem solved, key value proposition
4. **Features**: Bullet list of capabilities, unique points (use emojis)
5. **Installation/Setup**: Prerequisites, installation commands (npm/pip/docker), quick start, env vars
6. **Usage/Quick Start**: Basic examples, common commands/API calls, screenshots/GIFs
7. **License**: Clear statement, link to LICENSE file

### 🔧 **Conditional Sections** (Include if Relevant)

8. **Configuration**: Config options, env vars, examples
9. **Docker Usage**: `docker run`, compose examples, volumes, links to registries
10. **API Documentation**: Endpoints, examples, auth, rate limits
11. **Security**: Secrets handling, .env practices, vulnerability reporting
12. **Testing/Development**: Run tests, dev setup, build commands
13. **CI/CD**: GitHub Actions, workflows, deployment, releases
14. **Contributing**: Guidelines, code style, branch strategy, PR process
15. **Roadmap**: Planned features, limitations, improvements
16. **Acknowledgments**: Contributors, inspirations, resources
17. **AI Integration** (AI/MCP): Agent roles, MCP server info, requirements

### 🎨 **Best Practices**

**Formatting**: Emojis for headers (sparingly), short paragraphs (2-3 sentences), code blocks with syntax highlighting, tables for data, blockquotes for notes

**Badges**: Build status, Docker pulls, license, version, stars (shields.io)

**Visual Hierarchy**: `#` main title, `##` major sections, `###` subsections

**Code Examples**: Realistic runnable examples, expected output, copy-paste ready, proper syntax highlighting

---

## **Docker Descriptions**

### **Short Description** (`./docker/description/short.md`)

**Requirements**:
- **Maximum 100 characters** (strict limit)
- Single line, no formatting
- Clear, concise project tagline
- Complements the README title
- No markdown, just plain text

**Character Count Validation**:
```bash
# Check character count
wc -m ./docker/description/short.md

# Should output: ≤100
```

**Examples**:
```
A lightweight VPN monitoring tool that ensures connection reliability and security.
Automated CI/CD pipeline generator for GitHub Actions with Docker publishing support.
Secure financial data API with MCP integration for AI assistants.
```

### **Long Description** (`./docker/description/long.md`)

**Requirements**:
- Supports markdown formatting
- 2-5 paragraphs typically
- Expands on short description
- Include key features
- Installation hints
- Link to full documentation

**Structure**:
```markdown
[Project Name] is a [type] that [main purpose].

## Features
- Feature 1
- Feature 2
- Feature 3

## Quick Start
[Basic usage example]

## Documentation
Full documentation: [link]
```

---

## **Content Preservation Rules**

### **Always Preserve**:
1. **Images and Screenshots**:
   ```markdown
   ![Screenshot](./assets/screenshot.png)
   ![Demo](https://example.com/demo.gif)
   ```

2. **Custom Diagrams**:
   ```markdown
   ![Architecture](./docs/architecture.svg)
   ```

3. **Embedded Videos**:
   ```markdown
   [![Video Title](thumbnail.jpg)](https://youtube.com/watch?v=xxx)
   ```

4. **User-Added Examples**:
   - Custom configuration examples
   - Specific use cases
   - Real-world deployment scenarios

### **Update/Replace**:
1. Outdated version numbers
2. Broken badge URLs
3. Deprecated installation instructions
4. Old API examples
5. Incorrect feature descriptions

### **Enhancement Strategy**:
- Insert preserved images in appropriate sections
- Update image alt text for accessibility
- Add new badges while keeping custom ones
- Improve organization without losing content

---

## **Deliverables**

### **Primary Outputs**
1. **Updated README.md** - Complete, professional, follows all guidelines
2. **Version Comparison** - Summary of what changed and why
3. **Badge Recommendations** - Suggested shields.io badges with URLs
4. **Content Audit** - What was preserved, updated, or added

### **Docker Descriptions** (if applicable)
5. **`./docker/description/short.md`** - ≤100 character description
6. **`./docker/description/long.md`** - Extended markdown description
7. **Character Count Report** - Verification that short description is valid

### **Quality Checklist**
8. **Spelling and Grammar** - Professional language throughout
9. **Link Validation** - All links working and relevant
10. **Code Examples** - Tested and accurate
11. **Formatting Consistency** - Uniform style throughout

### **Documentation Updates**
All README updates must be documented in `/docs/`:

- **`/docs/README.md`**: Update with current project status, new features documented, setup instructions changes, and links to README sections
- **`/docs/PROJECT_OVERVIEW.md`**: Sync feature list, capabilities, target audience, and current maturity level with README content
- **`/docs/AI_INTERACTION_GUIDE.md`**: If README includes AI/MCP sections, document agent integration details and usage patterns
- **`/docs/ROADMAP.md`**: If README includes roadmap section, ensure alignment between public roadmap and internal planning

---

## **Success Criteria**

- [ ] README follows all 16 section guidelines (required + conditional)
- [ ] Project identity clear (title, tagline, badges)
- [ ] Table of contents present for READMEs >200 lines
- [ ] Installation and usage sections complete and accurate
- [ ] All existing screenshots and images preserved
- [ ] Code examples are copy-paste ready and tested
- [ ] Links validated and working
- [ ] Proper markdown formatting and syntax highlighting
- [ ] Badges added (build, version, license, downloads)
- [ ] Docker short description ≤100 characters (if applicable)
- [ ] Docker long description complete with markdown (if applicable)
- [ ] No spelling or grammatical errors
- [ ] Professional tone and clear language throughout
- [ ] **`/docs/` files updated** with README changes and feature documentation

---

## **Best Practices**

### **Audience-First Writing**
- Write for your target user (developer, DevOps, end-user)
- Assume minimal prior knowledge for installation sections
- Use progressive disclosure (simple first, advanced later)
- Provide context for technical decisions

### **Maintainability**
- Use relative links for in-repo files
- Keep code examples up-to-date with actual code
- Version-pin installation commands when necessary
- Document breaking changes in releases

### **Accessibility**
- Use descriptive alt text for images
- Avoid ASCII art or complex Unicode
- Provide text alternatives for visual information
- Use semantic heading hierarchy

### **SEO and Discoverability**
- Use clear, searchable keywords in title and description
- Include relevant technology names
- Add topics/tags (GitHub repository settings)
- Use descriptive commit messages when updating

### **Visual Appeal**
- Break up long text with lists and code blocks
- Use horizontal rules (`---`) to separate major sections
- Add emojis strategically (not excessively)
- Include screenshots/GIFs for visual features
- Use syntax highlighting for all code blocks

### **Docker-Specific Best Practices**
- Short description should work standalone (appears in search)
- Long description should motivate users to try the image
- Include docker pull command prominently
- Document all environment variables clearly
- Provide docker-compose example for complex setups
- Link to image tags/versions available

---

## **Usage Instructions**

### **When to Run This Prompt**

* Creating new project, existing README outdated/incomplete
* Preparing for public release or after major feature changes
* Documentation audit, updating Docker Hub descriptions

### **Initial Setup**
1. Review PROMPT_CREATION_GUIDE.md, examine existing README.md
2. Check for Docker description files in `./docker/description/`
3. Have project metadata ready (package.json, GitHub URL, license)

### **Execution**
```
I need a comprehensive README for my project.

Project: [name], Type: [library/CLI/web/API/Docker], Language: [JS/Python/etc.]
Purpose: [brief description], Key features: [3-5 features]
Docker: [yes/no, username if yes], Existing README: [yes/no]
Target audience: [developers/DevOps/end-users]
```

**Expected Outcome**: AI analyzes project, preserves screenshots/images/GIFs, generates comprehensive README.md with formatting/badges, creates/updates Docker descriptions (≤100 chars short), validates links/code, provides production-ready README

---

## **Example README Template**

Structure: Title with badges, TOC, About (problem/solution), Features (bullet list with emojis), Installation (prerequisites/quick start), Usage (examples), Configuration (.env), Docker (pull/run/compose), Contributing (fork/branch/commit/PR process), License, Acknowledgments

---

## **Character Count Validator**

Use this to validate Docker short description:

```bash
# Create validation script
cat > validate-docker-desc.sh << 'EOF'
#!/bin/bash
SHORT_DESC_FILE="./docker/description/short.md"

if [ ! -f "$SHORT_DESC_FILE" ]; then
  echo "❌ Short description file not found: $SHORT_DESC_FILE"
  exit 1
fi

CHAR_COUNT=$(wc -m < "$SHORT_DESC_FILE" | tr -d ' ')
MAX_CHARS=100

echo "Docker Short Description: $(cat $SHORT_DESC_FILE)"
echo "Character count: $CHAR_COUNT / $MAX_CHARS"

if [ "$CHAR_COUNT" -gt "$MAX_CHARS" ]; then
  echo "❌ FAILED: Description exceeds $MAX_CHARS characters"
  exit 1
else
  echo "✅ PASSED: Description is within limit"
  exit 0
fi
EOF

chmod +x validate-docker-desc.sh
./validate-docker-desc.sh
```
