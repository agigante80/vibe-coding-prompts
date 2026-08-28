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

* **Short, focused prompts (1 to 3 paragraphs)** work best for simple generation tasks (e.g., "generate a Python script to sort a CSV file").
* **Medium prompts (300 to 800 words)** are ideal for structured or multi-step outputs (e.g., CI/CD pipelines, Dockerfiles, documentation).
* **Long prompts (1,000 to 3,000 words)** are for **meta-prompts**, like the one you're building, which describe multi-stage pipelines, validation, and conditional logic.

---

<a name="technical-limits"></a>

## ⚙️ Hard Technical Limits (Approximate)

Model context windows change every generation, so treat these as ORDERS OF MAGNITUDE and check your platform's current documentation for exact limits:

| Platform | Typical context scale | Notes |
| -------- | --------------------- | ----- |
| **ChatGPT (frontier models)** | Very large (100k+ tokens) | Multi-thousand-word meta-prompts are safe. |
| **GitHub Copilot (inline)** | Small (single-digit k tokens) | Long prompts get truncated; keep under ~1,500 words, prefer Copilot Chat. |
| **Claude (frontier models)** | Very large (hundreds of k tokens) | Can process long prompts or entire repos. |
| **Gemini (frontier models)** | Very large to huge (up to millions) | Entire codebases plus documentation. |

> 🔹 *1 token ≈ 4 characters (average), or roughly ¾ of a word.*

---

<a name="optimal-prompt-length"></a>

## 📏 Optimal Prompt Length for Copilot

Because you mentioned GitHub Actions and Copilot-like usage, **the sweet spot** for Copilot and similar code assistants is:

> 🧩 **Between 300 and 700 words (2k to 5k characters)**
> That’s long enough to provide detail and structure, but short enough to not get truncated or ignored.

If your prompt (like your CI/CD meta-prompt) is longer than ~1,000 words:

* Consider **splitting it into sections** (“Core Requirements”, “Docker Section”, “Release Section”) and referencing only the relevant parts when you generate specific code.
* Or **save it as a reusable file** (e.g., `PROMPT.md`) and feed it incrementally.

---

<a name="practical-guidelines"></a>

## 💡 Practical Guidelines

| Use Case                                     | Ideal Prompt Length | Example                                                                  |
| -------------------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| Simple Code Generation                       | 1 to 2 paragraphs   | “Generate a Python script to convert JSON to CSV.”                       |
| Multi-step workflow                          | 300 to 600 words    | “Generate a CI/CD pipeline for Node.js with Docker build and release.”   |
| Meta-Prompt (Reusable Template)              | 800 to 1500 words   | Your universal CI/CD generator prompt.                                   |
| Entire Specification (Copilot Chat or frontier chat models) | 2k to 5k words      | Can include detailed rules, multiple registry configs, validations, etc. |

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

* There's **no fixed word limit**, but clarity always matters more than size:

  * **Copilot inline:** keep within 700 to 800 words; use Copilot Chat for longer prompts
  * **ChatGPT, Claude, Gemini:** handle full prompts of any length in this collection easily

* **This repository's prompts** target under 1600 words each; the current per-prompt word counts live in the [generated index in the root README](../README.md), the single source of truth
* For prompts near the cap, feed Copilot the relevant sections rather than the whole file

---

## 📦 How This Repository's Prompts Are Structured

### Prompt Length Distribution

Per-prompt word counts are generated into the [root README's prompt index](../README.md) and verified by CI; that table is the single source of truth (hard-coded copies here rotted repeatedly, which is why none remain).

### Recommendations by Platform

#### For GitHub Copilot Users
- Use **Copilot Chat** for these prompts; most exceed comfortable inline-completion length
- Check a prompt's current word count in the [README index](../README.md) before feeding it inline

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

- [Main Repository README](../README.md)
- [All Prompts](../prompts/)

