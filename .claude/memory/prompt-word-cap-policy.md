---
name: prompt-word-cap-policy
description: Every prompt body stays under 1600 words; compress in the same edit that adds content.
metadata:
  type: project
---

All prompts stay **under 1600 words of body text** (front matter excluded; the generated index Words column is the measurement). As of 2026-08-28 all fourteen comply, most sitting at 1590 to 1599.

**Why:** the collection targets platforms with small context windows (Copilot inline especially), and an earlier deliberate trim (commit a809d63) set the policy. Prompts drift over the cap on almost every edit, so every content change needs a compensating compression.

**How to apply:** check with the index (`python3 scripts/update_prompt_index.py` then read the Words column) rather than raw `wc -w`, which counts front matter. When a fix pushes a prompt over, compress bullet lists into prose sentences in the same edit rather than deferring it. Linked: [[prompt-versioning-system]].
