---
name: prompt-forge-agent
description: >-
  Intelligent prompt engineering agent. Comprehends context, auto-selects
  techniques (Zero-Shot, CoT, ReAct, ToT, and 7 more), auto-applies hardening
  patterns (Anchor, Confidence Gate, Assumption Audit, and 7 more), and
  assembles production-grade prompts. Follows UNIX philosophy.
  TRIGGER when: user invokes /prompts:prompt-forge-agent
allowed-tools:
  - prompt-forge-agent
---

# Prompt Forge Agent

Launch the **prompt-forge-agent** to intelligently build a high-quality prompt.

The agent will:
1. **Comprehend** your intent and read relevant context from your environment
2. **Ask** only the questions it cannot infer (2-4 max)
3. **Select** the optimal technique and hardening patterns automatically
4. **Assemble** a production-grade prompt with all layers composed
5. **Deliver** the prompt with options to execute, refine, or save

Invoke the `prompt-forge-agent` agent with the user's full input.
