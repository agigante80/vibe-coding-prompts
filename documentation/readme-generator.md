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

1. **Project Identity**
   - Title with optional emoji/logo
   - Tagline (one-liner description)
   - Badges (build status, version, license, downloads, etc.)

2. **Table of Contents**
   - For READMEs >200 lines
   - Linked navigation to all major sections

3. **About/Description**
   - What the project does
   - Problem it solves
   - Key value proposition
   - Optional: Brief architecture overview

4. **Features**
   - Bullet list of key capabilities
   - Highlight what makes it unique
   - Use emojis for visual appeal

5. **Installation/Setup**
   - Prerequisites and dependencies
   - Installation commands (npm, pip, docker, etc.)
   - Quick start minimal setup
   - Environment variables (reference .env.example)

6. **Usage/Quick Start**
   - Basic usage examples
   - Common commands or API calls
   - CLI output examples
   - Screenshots or GIFs (if available)

7. **License**
   - Clear license statement
   - Link to LICENSE file

### 🔧 **Conditional Sections** (Include if Relevant)

8. **Configuration/Advanced Setup**
   - Detailed configuration options
   - Environment variables documentation
   - Config file examples
   - Integration notes

9. **Docker Usage**
   - `docker run` examples
   - `docker-compose.yml` example
   - Environment variables for containers
   - Volume mounts and port mappings
   - Links to Docker Hub/GHCR

10. **API Documentation**
    - Endpoint list
    - Request/response examples
    - Authentication
    - Rate limiting

11. **Security/Credentials**
    - How to handle secrets securely
    - .env best practices
    - Security policies
    - Vulnerability reporting

12. **Testing/Development**
    - How to run tests
    - Development setup
    - Build commands
    - Debugging tips

13. **CI/CD and Deployment**
    - GitHub Actions or other CI/CD info
    - Automated workflows description
    - Deployment process
    - Release strategy

14. **Contributing**
    - Contribution guidelines
    - Code style requirements
    - Branch strategy
    - Pull request process
    - Link to CONTRIBUTING.md

15. **Roadmap**
    - Planned features
    - Known limitations
    - Future improvements

16. **Acknowledgments/Credits**
    - Contributors
    - Inspirations
    - Third-party resources

17. **AI Integration** (for AI/MCP projects)
    - Agent roles and capabilities
    - MCP server information
    - AI model requirements
    - Security/sandboxing

### 🎨 **Best Practices**

**Formatting**:
- Use emojis for section headers (sparingly)
- Keep paragraphs short (2-3 sentences max)
- Use code blocks with language syntax highlighting
- Use tables for structured data
- Use blockquotes for important notes

**Badges** (from shields.io):
```markdown
![Build](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/USER/IMAGE)
![License](https://img.shields.io/github/license/USER/REPO)
![Version](https://img.shields.io/github/v/release/USER/REPO)
![Stars](https://img.shields.io/github/stars/USER/REPO?style=social)
```

**Visual Hierarchy**:
- Use `#` for main title
- Use `##` for major sections
- Use `###` for subsections
- Use `####` for minor subsections (sparingly)

**Code Examples**:
- Show realistic, runnable examples
- Include expected output
- Provide copy-paste ready commands
- Use proper syntax highlighting

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

* Creating a new project and need a professional README
* Existing README is outdated or incomplete
* Preparing for public release or open source
* After major feature additions or breaking changes
* Documentation audit requirements
* Updating Docker Hub descriptions
* Improving project discoverability and SEO

### **Initial Setup**
1. Review the PROMPT_CREATION_GUIDE.md to understand documentation requirements
2. Examine existing README.md (if present) and identify preserved content
3. Check for Docker description files in `./docker/description/`
4. Ensure project metadata files exist (package.json, etc.)
5. Have project repository information ready (GitHub URL, license)

### **Execution**
```
I need a comprehensive README for my project.

Project name: [name]
Project type: [library/CLI/web app/API/Docker image/etc.]
Programming language: [JavaScript/Python/Java/etc.]
Main purpose: [brief description]
Key features: [list 3-5 main features]
Docker published: [yes/no, Docker Hub username if yes]
Existing README: [yes/no - if yes, preserve screenshots]
Target audience: [developers/DevOps/end-users/etc.]
```

### **Expected Outcome**
The AI will analyze your project structure, read existing documentation, identify and preserve all screenshots/images/GIFs, extract key features and capabilities, generate a comprehensive README.md following all 16 guidelines with proper formatting and badges, create or update Docker short description (≤100 chars) and long description if Docker is used, validate all links and code examples, ensure professional language and formatting, and document all changes in `/docs/` files. You'll receive a production-ready README that improves project discoverability and provides clear documentation for users.

---

## **Example README Template**

```markdown
# 🚀 Project Name

> One-line tagline describing what the project does

![Build](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/github/v/release/user/repo)
![License](https://img.shields.io/github/license/user/repo)
![Docker Pulls](https://img.shields.io/docker/pulls/user/image)

## 📚 Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)

## 🧠 About

[Project Name] solves [specific problem] by [solution approach].

Built with [technology stack], it provides [key value proposition] for [target audience].

## ✨ Features

- 🎯 **Feature One** - Description
- 🔒 **Feature Two** - Description
- ⚡ **Feature Three** - Description
- 🛠️ **Feature Four** - Description

## 📦 Installation

### Prerequisites
- Node.js 18+ / Python 3.9+ / etc.
- Docker (optional)

### Quick Start

\`\`\`bash
npm install project-name
# or
pip install project-name
\`\`\`

## 🚀 Usage

Basic example:

\`\`\`javascript
const project = require('project-name');

project.doSomething({
  option: 'value'
});
\`\`\`

## ⚙️ Configuration

Create a `.env` file:

\`\`\`env
API_KEY=your_key_here
PORT=8080
\`\`\`

## 🐳 Docker

Pull and run:

\`\`\`bash
docker pull user/image:latest
docker run -d -p 8080:8080 -e API_KEY=xxx user/image
\`\`\`

Docker Compose:

\`\`\`yaml
version: '3.8'
services:
  app:
    image: user/image:latest
    ports:
      - "8080:8080"
    environment:
      - API_KEY=${API_KEY}
\`\`\`

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/amazing\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing\`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## 🙏 Acknowledgments

- [Dependency Name](https://example.com) - Description
- Inspired by [Project](https://example.com)

---

Made with ❤️ by [Your Name](https://github.com/username)
```

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
