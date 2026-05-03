# Product Constitution Framework Overview

## What is a Product Constitution?

A Product Constitution is a living document that captures the fundamental beliefs, strategies, and operating principles of a product team. It serves as the single alignment mechanism for every product decision -- from roadmap prioritization to individual feature design choices.

## The 7-Section Framework

The constitution is organized into seven sections, each answering a distinct strategic question:

| # | Section | Core Question |
|---|---------|---------------|
| 1 | **Product Principles** | What do we believe? What tradeoffs have we already decided? |
| 2 | **Core Value Propositions** | What value do we deliver, to whom, and for which jobs? |
| 3 | **Product Positioning** | How do we want the market to perceive us relative to alternatives? |
| 4 | **Customer Experience Philosophy** | What quality bar do we hold ourselves to, and where do we invest in delight? |
| 5 | **Product Building Approach** | How do we build? What methodology, craft standards, and release practices do we follow? |
| 6 | **Prioritization Framework** | How do we decide what to build next? |
| 7 | **Product Research Bets** | What are we exploring, at what conviction level, and how do we validate? |

### Why these seven?

Each section resolves a different category of recurring debate. Principles resolve value conflicts. Positioning resolves "who are we for?" arguments. The building approach resolves process disagreements. Together, they eliminate the need to re-litigate foundational decisions in every sprint planning or design review.

### How the sections relate

The sections form a dependency chain. Principles inform value propositions (what you believe shapes what value you deliver). Value propositions inform positioning (you position around the value you actually deliver). CX philosophy sets the quality bar for delivering that value. The building approach defines how you meet that bar. Prioritization decides the sequence. Research bets represent the frontier -- where you are testing whether to extend the constitution.

## Two-Tier Output Architecture

The framework produces two layers of documentation:

**Tier 1: Compact Summary** (`product-constitution.md`)
A single file, roughly one page, containing 1-2 sentence summaries for each of the 7 sections. This is the file you share widely, pin in Slack, and reference in every PRD. Any team member should be able to read it in under 3 minutes.

**Tier 2: Detailed Section Files** (`constitution/{section-name}.md`)
Seven individual files with the full rationale, examples, and operational detail for each section. These are reference documents -- consulted when someone needs to understand the "why" behind a summary statement or when onboarding new team members.

The compact summary always links to the detailed files. The detailed files always link back to the summary. Neither layer is complete without the other.

## The Agent-Ready Vision

In an agent-based product team, the Product Constitution becomes the primary alignment mechanism for AI agents. When an agent writes a PRD, it loads the constitution to understand positioning and principles. When an agent reviews a design, it checks against the CX philosophy. When an agent proposes a roadmap, it applies the prioritization framework.

This is why the constitution must be:
- **Machine-readable**: clear structure, consistent formatting, no ambiguity
- **Self-contained**: each section must make sense without oral tradition or tribal knowledge
- **Opinionated**: vague constitutions produce vague agent outputs
- **Versioned**: agents need to know which version of the constitution they are operating under

The constitution is not a bureaucratic artifact. It is the operating system for product decision-making -- whether those decisions are made by humans, agents, or both.

## Review Cadence

Constitutions should be reviewed quarterly. Principles and positioning change slowly (annually). Prioritization frameworks and research bets change faster (quarterly). The compact summary is updated whenever any section file changes.
