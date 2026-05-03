---
name: standards
description: >-
  Canonical standards reference for the Microsoft Architecture skill suite.
  Contains the preferred coding stack, functional programming paradigm, DDD
  principles, security-by-design checklists, review checklists, and C4 diagram
  guides. This skill is a reference library: other skills Read its references/
  directory. DO NOT TRIGGER directly. Loaded by specialist skills on demand.
version: 1.0.0
license: Complete terms in LICENSE.txt
allowed-tools:
  - Read
---

# Microsoft Architecture Standards

**Version**: 1.0 | **Role**: Shared knowledge foundation for all architecture skills

This skill is the canonical source of truth for cross-cutting knowledge used by every specialist skill in the Microsoft Architecture suite. It exists to eliminate duplication. No other skill should inline this content.

## Contents

| Reference | Path | Used By |
|-----------|------|---------|
| Preferred Coding Stack | `references/coding-stack/preferred-stack.md` | All specialist and output skills |
| AWS-to-Azure Conversion | `references/coding-stack/aws-to-azure.md` | azure-architect |
| Functional Programming Paradigm | `references/paradigm/functional-programming.md` | odin, spec, all specialists |
| Domain-Driven Design | `references/paradigm/domain-driven-design.md` | odin, spec, all specialists |
| Security by Design | `references/security/security-by-design.md` | All specialist skills |
| Security Checklist | `references/security/security-checklist.md` | odin, validate |
| Review Checklist | `references/quality/review-checklist.md` | odin, validate |
| Quality Standards | `references/quality/quality-standards.md` | validate |
| C4 Diagram Guide | `references/diagrams/c4-diagram-guide.md` | spec, all specialists |
| Mermaid Diagram Patterns | `references/diagrams/mermaid-diagram-patterns.md` | spec, docs |
| LLD Process Diagrams | `references/diagrams/lld-process-diagrams.md` | spec, docs |
| C# Coding Standards | `references/coding-stack/csharp-standards.md` | dotnet-architect, all specialists |
| EF Core Checklist | `references/coding-stack/ef-core-checklist.md` | dotnet-architect |
| STRIDE-A Threat Worksheet | `references/security/stride-a-worksheet.md` | security-architect, threat-model |
| Identity Decision Tree | `references/security/identity-decision-tree.md` | identity-architect, security-architect |
| Cloud Design Patterns | `references/patterns/cloud-design-patterns.md` | All specialist skills |
| Repository Baseline | `references/tooling/repo-baseline.md` | All specialist skills |
| Microsoft Learn MCP Patterns | `references/research/learn-mcp-patterns.md` | All specialist skills |
| FinOps Framework | `references/operations/finops-framework.md` | finops-architect |
| Accessibility WCAG 2.2 AA | `references/quality/accessibility-wcag.md` | accessibility, all output skills |

## How Other Skills Use This

Other skills reference these files via relative path:
- `Read standards/references/coding-stack/preferred-stack.md`
- `Read standards/references/paradigm/functional-programming.md`

No skill should duplicate the content in these files. If you need to update a standard, update it here. All skills inherit the change.
