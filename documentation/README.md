# Documentation Prompts

This folder contains prompts focused on creating, maintaining, and standardizing project documentation.

## Available Prompts

### 📄 Documentation Standardization
**File**: `documentation-standardization.md`

**Purpose**: Establishes a comprehensive, synchronized documentation ecosystem for any project.

### 📝 README Generator
**File**: `readme-generator.md`

**Purpose**: Generates or updates comprehensive, professional README.md files following industry best practices, including Docker Hub descriptions.

**Key Features**:
- Defines standardized documentation structure
- Automates documentation updates with code changes  
- Enforces local testing before commits
- Maintains living refactoring and security tracking
- Provides detailed requirements for each document type

**Best For**:
- New projects needing documentation standards
- Existing projects with inconsistent documentation
- Teams wanting to automate documentation maintenance
- Projects requiring strict documentation compliance

**Usage Tips**:
- Customize the 9 required document types for your project
- Adjust automation rules based on your CI/CD setup
- Review agent task flow requirements before implementation
- Ensure your team understands the local testing requirements
- ✅ **Platform-friendly**: At ~940 words, this prompt works well with all AI platforms. Best with Copilot Chat, excellent with ChatGPT/Claude/Gemini. See [Prompt Creation Guide](../PROMPT_CREATION_GUIDE.md)

**Key Features**:
- Follows industry-standard README guidelines (16 sections)
- Generates professional badges (build, version, license, downloads)
- Preserves existing screenshots, images, and GIFs
- Creates Docker Hub short description (≤100 characters validated)
- Creates Docker Hub long description with markdown
- Includes character count validation for Docker limits
- Provides copy-paste ready code examples
- Ensures accessibility and SEO optimization

**Best For**:
- Creating professional READMEs for new projects
- Updating outdated or incomplete documentation
- Preparing for public release or open source
- Docker image documentation (Hub descriptions)
- Improving project discoverability
- Meeting professional documentation standards

**Usage Tips**:
- Specify if Docker descriptions are needed
- Mention existing screenshots to preserve
- Provide project metadata (name, purpose, features)
- Review generated badges and customize as needed
- Validate Docker short description is ≤100 characters
- ✅ **Platform-friendly**: At ~2065 words, works great with ChatGPT, Claude, and Gemini. For Copilot, use Copilot Chat

## When to Use Documentation Prompts

Use these prompts when:
- Starting a new project that needs professional documentation
- Inheriting a project with poor or outdated documentation  
- Implementing documentation-as-code practices
- Establishing documentation standards for a team or organization
- Automating documentation updates in CI/CD pipelines

## Integration with Other Prompts

Documentation prompts work well with:
- **DevOps Automation**: Integrate documentation updates into CI/CD workflows
- **Project Management**: Use documentation standards in project assessments
- **Development Workflow**: Make documentation updates part of the development process

## Customization Guidelines

When adapting these prompts:
1. **Document Types**: Modify the required document list for your project needs
2. **Automation Rules**: Adjust triggers and enforcement based on your workflow
3. **Quality Gates**: Customize testing and validation requirements
4. **Tool Integration**: Adapt for your specific documentation tools and platforms

## Quality Standards

Documentation prompts in this folder emphasize:
- **Synchronization**: Keeping docs aligned with code
- **Automation**: Reducing manual documentation overhead
- **Completeness**: Ensuring comprehensive coverage
- **Maintainability**: Making documentation easy to update
- **Compliance**: Meeting organizational standards