# Prompt Engineering Guide

> A comprehensive guide to crafting effective AI prompts and understanding platform limitations.

## Table of Contents
- [General Best Practices](#general-best-practice)
- [Technical Limits by Platform](#technical-limits)
- [Optimal Prompt Lengths](#optimal-prompt-length)
- [Practical Guidelines](#practical-guidelines)
- [Platform-Specific Tips](#platform-specific-tips)

---

## 🧠 General Best Practice

For AI systems like **ChatGPT, Copilot, Claude, or Gemini**, the *effective* prompt length depends on:

* **Complexity of the task**
* **How structured the output should be**
* **How much context the model can handle in a single request (context window)**

As a rule of thumb:

* **Short, focused prompts (1–3 paragraphs)** work best for simple generation tasks (e.g., "generate a Python script to sort a CSV file").
* **Medium prompts (300–800 words)** are ideal for structured or multi-step outputs (e.g., CI/CD pipelines, Dockerfiles, documentation).
* **Long prompts (1,000–3,000 words)** are for **meta-prompts**, like the one you're building — describing multi-stage pipelines, validation, and conditional logic.

---

<a name="technical-limits"></a>

## ⚙️ Hard Technical Limits (Approximate)

| Platform / Model                | Max Prompt Size                | Notes                                                                                   |
| ------------------------------- | ------------------------------ | --------------------------------------------------------------------------------------- |
| **OpenAI GPT-5 (ChatGPT)**      | ~128k tokens (~80k–100k words) | Huge — you can safely use multi-thousand-word system or meta-prompts.                   |
| **GitHub Copilot**              | ~4k–8k tokens                  | Much smaller; long prompts get truncated. You should keep prompts <1,500 words ideally. |
| **Anthropic Claude 3.5 / Opus** | 200k tokens                    | Extremely large context; can process long prompts or even entire repos.                 |
| **Gemini 1.5 Pro**              | 1M tokens                      | Can handle entire codebases and documentation together.                                 |

> 🔹 *1 token ≈ 4 characters (average), or roughly ¾ of a word.*

---

<a name="optimal-prompt-length"></a>

## 📏 Optimal Prompt Length for Copilot

Because you mentioned GitHub Actions and Copilot-like usage, **the sweet spot** for Copilot and similar code assistants is:

> 🧩 **Between 300–700 words (2–5k characters)**
> That’s long enough to provide detail and structure, but short enough to not get truncated or ignored.

If your prompt (like your CI/CD meta-prompt) is longer than ~1,000 words:

* Consider **splitting it into sections** (“Core Requirements”, “Docker Section”, “Release Section”) and referencing only the relevant parts when you generate specific code.
* Or **save it as a reusable file** (e.g., `PROMPT.md`) and feed it incrementally.

---

<a name="practical-guidelines"></a>

## 💡 Practical Guidelines

| Use Case                                     | Ideal Prompt Length | Example                                                                  |
| -------------------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| Simple Code Generation                       | 1–2 paragraphs      | “Generate a Python script to convert JSON to CSV.”                       |
| Multi-step workflow                          | 300–600 words       | “Generate a CI/CD pipeline for Node.js with Docker build and release.”   |
| Meta-Prompt (Reusable Template)              | 800–1500 words      | Your universal CI/CD generator prompt.                                   |
| Entire Specification (Copilot Chat or GPT-5) | 2k–5k words         | Can include detailed rules, multiple registry configs, validations, etc. |

---

<a name="platform-specific-tips"></a>

## 🚨 Platform-Specific Tips

### If You're Using Copilot in VS Code

Copilot truncates long prompts when used inline.
If your goal is to feed a **meta-prompt** like your universal CI/CD builder:

* Use **Copilot Chat** instead of inline suggestions.
* Or store your meta-prompt in a file (`prompt.md`) and use `/prompt` or “Custom instruction” features.
* Or feed just the **relevant subset** of the prompt (e.g., only the Docker-related parts).

---

---

## ✅ Quick Reference Summary

* There's **no fixed word limit**, but:

  * **Copilot:** keep ≤700–800 words (~5k characters) - ✅ All prompts in this repo comply!
  * **ChatGPT (GPT-4/5):** can handle 50k+ words, but clarity matters more than size
  * **Claude 3.5:** excellent for 1k-5k word prompts with full context
  * **Gemini 1.5 Pro:** handles extremely long contexts (entire codebases)

* **This repository's prompts (390-940 words)** work perfectly across all platforms
* For very long CI/CD meta-prompts (2,000+ words), consider modular sections for Copilot

---

## 📦 How This Repository's Prompts Are Structured

### Prompt Length Distribution

Most prompts in this repository fall into these categories:

| Category | Typical Length | Best Platform | Notes |
|----------|---------------|---------------|-------|
| **Documentation** | ~940 words | All platforms | Comprehensive yet concise documentation systems |
| **DevOps Automation** | ~640 words | All platforms | Focused CI/CD pipelines with clear structure |
| **Project Management** | ~390 words | All platforms | Concise assessments and planning prompts |
| **Development Workflow** | ~460 words | All platforms | Efficient process automation with clear boundaries |

### Recommendations by Platform

#### For GitHub Copilot Users
- ✅ **All prompts in this repository are Copilot-friendly!** (all under 1000 words)
- Can use **inline completions** or **Copilot Chat** - both work well
- **Development Workflow** (~460 words) and **Project Management** (~390 words) are especially efficient
- **Documentation** (~940 words) works best in Copilot Chat

#### For ChatGPT / Claude / Gemini Users
- ✅ All prompts in this repository work excellently
- Can handle complete prompts in single conversations
- May want to add more context since these platforms can handle 10x-100x more
- Ideal for generating comprehensive implementations
- Best for initial project setup and major refactoring

#### For Team Environments
- Store prompts in project documentation
- Reference sections as needed rather than full prompts
- Create platform-specific variations for different team members
- Document which AI platform works best for which prompt

---

## 🎯 Tips for Adapting Repository Prompts

1. **Assess Your Platform**: Know your AI tool's context limits
2. **Start Complete**: Use full prompts first to understand intent
3. **Modularize if Needed**: Break into sections for smaller context windows
4. **Test and Iterate**: Adjust based on actual output quality
5. **Document Changes**: Keep track of what works for your use case

---

## 🔗 Related Resources

- [Main Repository README](./README.md)
- [Documentation Prompts](./documentation/)
- [DevOps Automation Prompts](./devops-automation/)
- [Project Management Prompts](./project-management/)
- [Development Workflow Prompts](./development-workflow/)

