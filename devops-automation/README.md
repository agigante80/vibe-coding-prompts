# DevOps Automation Prompts

This folder contains prompts for automating CI/CD pipelines, deployments, and infrastructure management.

## Available Prompts

### 🚀 GitHub Actions CI/CD Generator
**File**: `github-actions-cicd-generator.md`

**Purpose**: Creates or improves comprehensive GitHub Actions workflows with full CI/CD capabilities.

**Key Features**:
- Auto-detects project type and configures appropriate toolchain
- Implements modular pipeline stages (lint, test, build, deploy)
- Includes Docker Hub and GitHub Container Registry publishing
- Provides security scanning with SARIF upload
- Supports manual workflow dispatch with parameters
- Validates Docker descriptions and performs test builds

**Pipeline Stages**:
- **Lint**: Static analysis and code formatting
- **Test**: Unit and integration testing
- **Build**: Compilation and bundling
- **Security Scan**: Vulnerability detection with trivy
- **Docker Operations**: Test builds and multi-registry publishing
- **Release**: Automated versioning and GitHub releases

**Best For**:
- Projects needing robust CI/CD from scratch
- Modernizing existing GitHub Actions workflows
- Implementing Docker-based deployment pipelines
- Adding comprehensive security scanning
- Establishing automated release processes

**Usage Tips**:
- Ensure required secrets are configured (Docker Hub, GitHub tokens)
- Customize branch strategy and tagging rules for your workflow
- Review security scanning thresholds before implementation
- Test with a non-production repository first
- ✅ **Platform-friendly**: At ~640 words, this prompt works great with all AI platforms including GitHub Copilot. See [Prompt Engineering Guide](../PROMPT_ENGINEERING_GUIDE.md)

## When to Use DevOps Automation Prompts

Use these prompts when:
- Setting up CI/CD for new projects
- Modernizing legacy deployment processes
- Implementing security scanning in existing pipelines
- Standardizing workflows across multiple repositories
- Adding Docker publishing and container scanning
- Establishing automated release processes

## Integration with Other Prompts

DevOps automation prompts work well with:
- **Documentation**: Include pipeline documentation in standardization efforts
- **Project Management**: Use CI/CD setup as part of project assessments
- **Development Workflow**: Integrate automated testing into development processes

## Customization Guidelines

When adapting these prompts:
1. **Technology Stack**: Modify detection and build commands for your languages/frameworks
2. **Registry Configuration**: Adjust Docker registry settings and authentication
3. **Security Thresholds**: Customize vulnerability scanning sensitivity
4. **Branch Strategy**: Adapt branching and tagging rules to your workflow
5. **Deployment Targets**: Configure deployment steps for your infrastructure

## Prerequisites

Before using these prompts, ensure:
- GitHub repository with appropriate permissions
- Docker Hub account and access tokens (if using Docker features)
- Understanding of your project's build and test requirements
- Familiarity with GitHub Actions syntax and limitations

## Security Considerations

DevOps prompts in this folder emphasize:
- **Secure Secret Management**: Proper handling of tokens and credentials
- **Vulnerability Scanning**: Automated security analysis
- **Least Privilege**: Minimal permissions for automated processes
- **Audit Trails**: Comprehensive logging and monitoring
- **Compliance**: Meeting security standards and regulations