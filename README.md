# Generic Coding Prompts Repository

A curated collection of reusable AI prompts designed to streamline software development workflows, improve code quality, and automate common development tasks.

## 🎯 Purpose

This repository contains battle-tested prompts that help developers and AI assistants work together more effectively on coding projects. Each prompt is designed to be generic enough to apply to various projects while being specific enough to produce actionable results.

## 🎧 The Philosophy: Vibe Coding

This repository is built around the concept of **"vibe coding"** — a creative, conversational, exploratory way of programming where you collaborate with AI to build by intuition and iteration, rather than rigid planning.

### What is Vibe Coding?

**Vibe coding** is like **"jamming with code"** — similar to how musicians improvise to discover melodies. Instead of writing detailed specifications, you:

- 💬 **Describe intent in natural language** ("make this more secure", "add comprehensive tests")
- 🎨 **Iterate rapidly** based on AI suggestions and output quality
- 🔁 **Refine through feedback** until the solution "feels right"
- ⚡ **Move fast** with minimal boilerplate and maximum creativity
- 🧠 **Let AI understand context** and adapt to your project's style

**Traditional approach**: "Implement a test suite with Jest, covering these specific edge cases..."  
**Vibe coding approach**: "Add solid test coverage that catches the important stuff" → Use our [Test Suite Generator](./development-workflow/test-suite-generator.md)

### Meta-Prompts: The Foundation

This repository uses **meta-prompts** — prompts that don't just solve one specific problem, but define *how to solve entire categories of problems*.

**Meta-prompt** = A prompt framework that adapts to any project, language, or stack by:
- Auto-detecting project context and requirements
- Applying universal best practices
- Generating customized, production-ready solutions
- Being reusable across your entire organization

**Example**: Our [GitHub Actions CI/CD Generator](./devops-automation/github-actions-cicd-generator.md) doesn't just create *one* pipeline — it detects your tech stack and generates the *right* pipeline for your specific project.

### Learn More

- 📖 [Vibe Coding Deep Dive](./docs/vibe-coding.md) - Full explanation with examples
- 🧠 [Universal Meta-Level Prompt System](./docs/universal-meta-Level-prompt-system.md) - How meta-prompts work

---

> 💡 **New to AI prompts?** Check out our [**Prompt Engineering Guide**](./PROMPT_ENGINEERING_GUIDE.md) to understand optimal prompt lengths and platform-specific recommendations for ChatGPT, GitHub Copilot, Claude, and Gemini.

## ⚡ Quick Selection Guide

| Need to... | Use This Prompt | Category |
|-----------|----------------|----------|
| **Understand the philosophy** | [What is Vibe Coding?](./docs/vibe-coding.md) | 📚 Concepts |
| **Learn about meta-prompts** | [Universal Meta-Prompt System](./docs/universal-meta-Level-prompt-system.md) | 📚 Concepts |
| **Create your own prompt** | [Prompt Creation Guide](./PROMPT_CREATION_GUIDE.md) | 📚 Guides |
| Set up project documentation | [Documentation Standardization](./documentation/documentation-standardization.md) | 📖 Documentation |
| Create/update README | [README Generator](./documentation/readme-generator.md) | 📖 Documentation |
| Update Docker descriptions | [README Generator](./documentation/readme-generator.md) | 📖 Documentation |
| Create CI/CD pipeline | [GitHub Actions CI/CD Generator](./devops-automation/github-actions-cicd-generator.md) | 🚀 DevOps |
| Audit project security | [Security Audit Generator](./security/security-audit-generator.md) | 🔐 Security |
| Update dependencies safely | [Dependency Update Manager](./security/dependency-update-manager.md) | 🔐 Security |
| Assess existing project | [Project Reassessment](./project-management/project-reassessment.md) | 📊 Management |
| Prepare for GitHub | [GitHub Ready Preparation](./project-management/github-ready-preparation.md) | 📊 Management |
| Add comprehensive tests | [Test Suite Generator](./development-workflow/test-suite-generator.md) | 🔄 Workflow |
| Fix skipped/failing tests | [Test Suite Generator](./development-workflow/test-suite-generator.md) | 🔄 Workflow |
| Improve code quality | [Code Refactoring Plan Generator](./development-workflow/code-refactoring-plan.md) | 🔄 Workflow |
| Analyze technical debt | [Code Refactoring Plan Generator](./development-workflow/code-refactoring-plan.md) | 🔄 Workflow |

---

## � Available Prompts

### 📖 Documentation

#### [Documentation Standardization](./documentation/documentation-standardization.md)
**Word Count**: ~940 words | **Platform**: All

**What it does**: Establishes a comprehensive, synchronized documentation ecosystem for any project.

**Ideal for**:
- ✅ New projects needing professional documentation standards
- ✅ Existing projects with inconsistent or outdated documentation
- ✅ Teams wanting to automate documentation maintenance
- ✅ Projects requiring strict compliance and audit trails
- ✅ Establishing living documentation that evolves with code

**Outputs**: 9 standardized documentation files, automation rules, quality gates, agent task flows

#### [README Generator](./documentation/readme-generator.md)
**Word Count**: ~2065 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Generates or updates comprehensive, professional README.md files following industry best practices, including Docker Hub descriptions.

**Ideal for**:
- ✅ Creating professional READMEs for new projects
- ✅ Updating outdated or incomplete documentation
- ✅ Preparing for public release or open source
- ✅ Generating Docker Hub short (≤100 chars) and long descriptions
- ✅ Preserving existing screenshots and images while updating content
- ✅ Improving project discoverability and SEO
- ✅ Meeting documentation standards for professional projects

**Outputs**: Complete README.md with 16 sections, badges, Docker descriptions (short ≤100 chars, long markdown), preserved images/screenshots, character count validation

---

### 🚀 DevOps Automation

#### [GitHub Actions CI/CD Generator](./devops-automation/github-actions-cicd-generator.md)
**Word Count**: ~642 words | **Platform**: All

**What it does**: Creates or modernizes GitHub Actions workflows with full CI/CD capabilities.

**Ideal for**:
- ✅ Setting up CI/CD for new projects from scratch
- ✅ Modernizing legacy deployment processes
- ✅ Implementing Docker Hub + GHCR publishing
- ✅ Adding security scanning (Trivy, SARIF uploads)
- ✅ Establishing automated release processes
- ✅ Multi-stage pipelines (lint, test, build, deploy)

**Outputs**: Complete `.github/workflows/ci-cd.yml`, secrets documentation, manual trigger support

---

### 📊 Project Management

#### [Project Reassessment](./project-management/project-reassessment.md)
**Word Count**: ~390 words | **Platform**: All

**What it does**: Performs comprehensive project analysis and documentation synchronization.

**Ideal for**:
- ✅ Taking over inherited or existing projects
- ✅ Periodic project health checks (monthly/quarterly)
- ✅ Pre-release quality assurance and validation
- ✅ Team onboarding and knowledge transfer
- ✅ Compliance audits and gap analysis
- ✅ Preparing for major releases or handovers

**Outputs**: Assessment report, updated documentation, test results, prioritized action plan

#### [GitHub Ready Preparation](./project-management/github-ready-preparation.md)
**Word Count**: ~2610 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Prepares projects for professional GitHub publication with proper structure, documentation, automation, security, and community guidelines.

**Ideal for**:
- ✅ First-time public GitHub release preparation
- ✅ Converting private repositories to public
- ✅ Open source project setup and best practices
- ✅ Job application portfolio preparation
- ✅ Pre-release quality and security audits
- ✅ Establishing community contribution guidelines
- ✅ CI/CD and automation setup for GitHub

**Outputs**: Essential files (LICENSE, .gitignore, README, CONTRIBUTING), CI/CD workflows, security configuration, issue/PR templates, comprehensive documentation, GitHub-ready structure

---

### 🔄 Development Workflow

#### [Test Suite Generator](./development-workflow/test-suite-generator.md)
**Word Count**: ~2561 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Generates comprehensive test suites with unit, integration, and E2E tests, including extensive variable validation testing.

**Ideal for**:
- ✅ Adding tests to legacy projects without coverage
- ✅ Establishing test infrastructure for new projects
- ✅ Fixing projects with many skipped/disabled tests
- ✅ Implementing test-driven development (TDD)
- ✅ Meeting quality assurance requirements
- ✅ Improving existing test suites with best practices
- ✅ Creating reliable CI/CD test pipelines
- ✅ Comprehensive variable validation testing (defaults, valid values, error handling)

**Outputs**: Complete test suite, fixtures, mocking infrastructure, CI/CD integration, skipped test analysis, comprehensive variable validation tests

#### [Code Refactoring Plan Generator](./development-workflow/code-refactoring-plan.md)
**Word Count**: ~2485 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Analyzes codebase to identify code smells, technical debt, and architectural issues, generating a prioritized refactoring roadmap.

**Ideal for**:
- ✅ Legacy codebase modernization
- ✅ Addressing accumulated technical debt
- ✅ Quarterly code quality assessments
- ✅ Improving developer velocity through better code
- ✅ Pre-planning major architectural changes
- ✅ Onboarding teams to complex codebases
- ✅ Establishing code quality baselines

**Outputs**: Code quality metrics, code smell analysis, prioritized refactoring roadmap, effort estimates, risk assessments, automated linting setup

---

### 🔐 Security

#### [Security Audit Generator](./security/security-audit-generator.md)
**Word Count**: ~1286 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Performs comprehensive security audit with vulnerability scanning and compliance validation.

**Ideal for**:
- ✅ Pre-production security assessments
- ✅ Quarterly security review cycles
- ✅ Compliance audit preparation (GDPR, HIPAA, PCI-DSS)
- ✅ Vulnerability scanning and remediation
- ✅ Post-incident security reviews
- ✅ Penetration testing preparation
- ✅ Security baseline for new projects

**Outputs**: Security audit report, CVSS risk scoring, remediation plan, CI/CD security integration, compliance checklist

#### [Dependency Update Manager](./security/dependency-update-manager.md)
**Word Count**: ~1630 words | **Platform**: ChatGPT, Claude, Gemini (use Copilot Chat)

**What it does**: Automates dependency updates with breaking change detection, automated testing, and safe rollback.

**Ideal for**:
- ✅ Responding to security vulnerabilities in dependencies
- ✅ Setting up automated dependency management (Dependabot/Renovate)
- ✅ Major version upgrade planning with impact analysis
- ✅ Reducing technical debt from outdated packages
- ✅ Establishing regular update cycles (weekly/monthly)
- ✅ Multi-ecosystem projects (npm, pip, Maven, Cargo, etc.)
- ✅ CI/CD integration for dependency checks

**Outputs**: Dependency audit report, prioritized update plan, breaking change analysis, automation config (Dependabot/Renovate), rollback procedures

---

## 🚧 TODO: Upcoming Prompts

The following prompts are planned for future releases. Contributions welcome!

### 🔐 Security & Compliance
- [x] **Security Audit Generator** - Comprehensive security review with vulnerability scanning ✅
- [x] **Dependency Update Manager** - Automated dependency updates with breaking change analysis ✅
- [ ] **GDPR/Compliance Documentation** - Generate privacy policies and compliance docs

### 🏗️ Code Quality
- [x] **Code Refactoring Plan Generator** - Identify code smells and generate refactoring roadmap ✅
- [ ] **API Documentation Generator** - Auto-generate OpenAPI/Swagger specs from code
- [ ] **Code Review Checklist** - Customizable code review guidelines and automation

### 📊 Monitoring & Observability
- [ ] **Logging & Monitoring Setup** - Configure structured logging, metrics, and alerts
- [ ] **Performance Optimization** - Identify bottlenecks and generate optimization plan
- [ ] **Error Tracking Integration** - Set up Sentry, Datadog, or similar tools

### 🗄️ Database & Data
- [ ] **Database Migration Generator** - Create safe, reversible database migrations
- [ ] **Data Validation Layer** - Generate input validation and sanitization
- [ ] **Database Optimization** - Index recommendations, query optimization

### 🎨 Frontend & UI
- [ ] **Component Library Setup** - Bootstrap design system and component library
- [ ] **Accessibility Audit** - WCAG compliance checking and remediation
- [ ] **Responsive Design Testing** - Multi-device testing strategy

### 📦 Project Setup
- [ ] **Monorepo Setup** - Configure monorepo with proper tooling (Nx, Turborepo, Lerna)
- [ ] **Microservices Architecture** - Design and scaffold microservices structure
- [ ] **Docker Compose Environment** - Local development environment with all services

### 📖 Documentation Specialized
- [ ] **API Client Generator** - Generate client libraries with documentation
- [ ] **Tutorial & Guide Creator** - Step-by-step tutorials from code examples
- [ ] **Changelog Generator** - Semantic versioning and automated changelogs

### 🤖 AI/ML Specific
- [ ] **Model Training Pipeline** - MLOps setup with training, validation, deployment
- [ ] **Dataset Preparation** - Data cleaning, augmentation, and validation
- [ ] **Model Monitoring** - Drift detection and performance tracking

---

## 📁 Repository Structure

## 🚀 How to Use These Prompts

### For Individual Projects
1. Choose a relevant prompt from the appropriate category
2. Copy the prompt content to your AI assistant
3. Customize any project-specific details mentioned in the prompt
4. Execute the prompt in the context of your project

### For Team Adoption
1. Review prompts with your team to ensure alignment
2. Customize prompts to match your team's standards and tools
3. Create project-specific versions in your repositories
4. Document which prompts are used for different scenarios

### Best Practices
- **Read the full prompt** before using it to understand its scope and requirements
- **Customize as needed** for your specific technology stack and requirements  
- **Test prompts** on non-critical projects first to understand their behavior
- **Version control** your customized prompts alongside your code
- **Share improvements** back to this repository when beneficial
- **Consider prompt length** based on your AI platform - see [Prompt Engineering Guide](./PROMPT_ENGINEERING_GUIDE.md)

## 🎯 Prompt Design Philosophy

Each prompt in this collection follows these principles:

- **Generic but Actionable** - Works across different projects while producing specific results
- **Comprehensive** - Covers the complete workflow, not just isolated tasks
- **Quality-Focused** - Includes testing, security, and documentation requirements
- **Automation-Ready** - Designed to work with minimal human intervention
- **Iterative** - Can be run multiple times to improve results

## 🤝 Contributing

This repository welcomes contributions of new prompts and improvements to existing ones!

### Want to Create a Prompt?

📖 **Read the [Prompt Creation Guide](./PROMPT_CREATION_GUIDE.md)** - Comprehensive guidelines covering:
- Prompt structure template
- Writing best practices
- Length guidelines (400-2000 words)
- Formatting standards
- Multi-language support
- Testing and validation
- File organization
- Publication process

### Adding New Prompts
1. **Read the guide** - Follow [Prompt Creation Guide](./PROMPT_CREATION_GUIDE.md)
2. **Choose category** - Select appropriate folder or propose new one
3. **Use the template** - Follow standard structure
4. **Test thoroughly** - Run on at least one real project
5. **Update READMEs** - Category and main README
6. **Submit PR** - With clear description and testing notes

### Improving Existing Prompts
1. Test the existing prompt and identify areas for improvement
2. Make targeted changes that enhance clarity or effectiveness
3. Update any related documentation
4. Submit a pull request explaining the benefits of your changes

## 📋 Prompt Categories Explained

### Documentation
Focus on creating maintainable, synchronized documentation that evolves with your codebase. These prompts help establish documentation standards and automate updates.

### DevOps Automation  
Streamline your deployment and integration processes with prompts that generate robust CI/CD pipelines, automate testing, and manage infrastructure as code.

### Project Management
Keep projects organized and aligned with prompts that help assess current state, plan improvements, and maintain quality standards throughout development.

### Development Workflow
Establish efficient development processes that maintain high code quality while enabling rapid iteration and continuous improvement.

## � Prompt Engineering Guide

**New to prompt engineering or wondering about optimal prompt length?**

Check out our [**Prompt Engineering Guide**](./PROMPT_ENGINEERING_GUIDE.md) for:
- Optimal prompt lengths for different AI platforms (ChatGPT, Copilot, Claude, Gemini)
- Technical limits and context windows
- Platform-specific recommendations
- How to structure prompts for maximum effectiveness

### Quick Reference: Prompt Length Guidelines

| AI Platform | Optimal Length | Max Context | Best For |
|------------|---------------|-------------|----------|
| **ChatGPT (GPT-4/5)** | 800-3000 words | ~100k words | Complex meta-prompts, full specifications |
| **GitHub Copilot** | 300-700 words | ~4-8k tokens | Focused, modular prompts |
| **Claude 3.5** | 1000-5000 words | ~200k tokens | Large context, entire codebases |
| **Gemini 1.5 Pro** | Unlimited practical | 1M+ tokens | Complete documentation sets |

✅ *All prompts in this repository (390-940 words) are optimized for **all platforms** - they work perfectly with Copilot, ChatGPT, Claude, and Gemini!*

---

## �🔧 Requirements

Most prompts in this repository assume:

- Access to an AI assistant with code generation capabilities
- Basic familiarity with software development concepts
- Ability to customize prompts for your specific technology stack
- Understanding of version control and collaborative development

## 📄 License

This repository is provided under an open license to encourage widespread use and contribution. See LICENSE file for details.

## 🌟 Getting Started

1. **Understand the philosophy** - Read about [vibe coding](./docs/vibe-coding.md) and [meta-prompts](./docs/universal-meta-Level-prompt-system.md)
2. **Browse the categories** to find prompts relevant to your current needs
3. **Start with documentation prompts** if you're beginning a new project
4. **Use DevOps prompts** to establish reliable deployment processes  
5. **Apply workflow prompts** to establish sustainable development practices
6. **Embrace the vibe** - Iterate, refine, and let AI help you discover solutions

## 📚 Additional Resources

### Understanding the Philosophy
- [Vibe Coding Explained](./docs/vibe-coding.md) - Understanding the creative, conversational approach
- [Meta-Prompt System](./docs/universal-meta-Level-prompt-system.md) - How universal prompts work

### Technical Guides
- [Prompt Engineering Guide](./PROMPT_ENGINEERING_GUIDE.md) - Technical limits and best practices
- [Prompt Creation Guide](./PROMPT_CREATION_GUIDE.md) - How to create effective prompts for this repository

---

**Note**: These prompts are designed to work with AI assistants and should be adapted to your specific context, technology stack, and requirements. Always review and test generated code before deploying to production environments.

*Built for vibe coding — where creativity meets automation.* 🎧✨