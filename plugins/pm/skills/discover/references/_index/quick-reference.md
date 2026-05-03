# PM Discovery Quick Reference

## Workflow Phases

| Phase | Name | Purpose | Key Action |
|-------|------|---------|------------|
| 1 | **Intake** | Determine entry mode and gather initial context | AskUserQuestion: problem statement, mode |
| 2 | **Clarify** | Progressive questioning across 5 dimensions | AskUserQuestion: batches of 2-3 questions |
| 3 | **Analyze** | Decompose problem, identify root causes | Load methodology references |
| 4 | **Classify** | Categorize initiative type | Apply classification framework |
| 5 | **Map** | Build persona profiles and process flows | Generate Mermaid diagrams |
| 6 | **Document** | Assemble Business Understanding Document | Use business understanding template |
| 7 | **Handoff** | Route to downstream skill | Mode A -> pm-prd-generator, Mode B -> tom-architect |

## Entry Modes

| Mode | Context | Focus | Handoff Target |
|------|---------|-------|----------------|
| **A (SaaS PM)** | Product company | User personas, behaviors, journeys, pain points | `/pm-prd-generator` |
| **B (Consulting PM)** | Transformation engagement | Business processes, org actors, operational flows | `/tom-architect` |

## Initiative Classification Types

| Type | Description | Example |
|------|-------------|---------|
| **Product Development** | New product or feature | Build a customer self-service portal |
| **Process Improvement** | Optimize existing process | Reduce invoice approval cycle time |
| **Process Automation** | Automate manual process | Auto-generate purchase orders from demand signals |
| **AI/Agent-Based Automation** | Leverage AI/ML/agents | AI agent for first-level customer support triage |

## Five Discovery Dimensions

1. **Business Context** -- Industry, business model, strategic objectives, competitive landscape
2. **Stakeholder Landscape** -- Decision-makers, influencers, end users, affected parties
3. **Problem Definition** -- Problem statement, impact, root cause, scope, prior attempts
4. **Constraints & Dependencies** -- Budget, timeline, technical/org constraints, dependencies
5. **Success Criteria** -- KPIs, qualitative goals, acceptance criteria, risk thresholds

## Deliverables

- **Business Understanding Document** (markdown) -- Complete problem analysis with embedded diagrams
- **BPMN Process Flows** (Mermaid) -- Current-state and target-state process diagrams
- **Swimlane Diagrams** (Mermaid) -- Actor-based process views showing handoffs
- **State Machine Diagrams** (Mermaid) -- Entity lifecycle diagrams

## Reference File Paths

```
references/
  _index/
    discovery-framework-overview.md    # Framework overview, modes, dimensions
    diagram-patterns.md                # Quick Mermaid pattern reference
    quick-reference.md                 # This file
  methodology/
    discovery-questioning.md           # Question bank by dimension
    stakeholder-analysis.md            # Stakeholder identification framework
    problem-framing.md                 # Problem framing techniques
    persona-mapping.md                 # Persona identification and templates
    initiative-classification.md       # Initiative type classification
  process-flows/
    bpmn-mermaid-patterns.md           # BPMN flowchart patterns
    swimlane-patterns.md               # Swimlane diagram patterns
    state-machine-patterns.md          # State machine diagram patterns
  contexts/
    saas-product-context.md            # SaaS PM context guide
    consulting-delivery-context.md     # Consulting PM context guide
  templates/
    business-understanding-template.md # Business Understanding Document template
    process-flow-template.md           # Process flow documentation template
```

## Key Conventions

- **Questions in batches**: Always ask 2-3 questions per AskUserQuestion call, never more
- **Progressive disclosure**: Surface -> Structure -> Detail -> Deliverable
- **Diagram styling**: Gray = current state, Blue = target state, Red border = pain point
- **Persona naming**: Use role-based names (e.g., "Procurement Manager") not personal names
- **Process IDs**: Format as `{Domain}-{Type}-{Number}` (e.g., `FIN-AP-001`)
- **Never skip Intake**: Always determine entry mode before loading context-specific references
- **Context budget**: Load only what the current phase requires

## Suite Skills

| Skill | Invoke | When |
|-------|--------|------|
| `/pm-discovery` | This skill | Business problem understanding and process mapping |
| `/pm-prd-generator` | `pm-prd-generator` | Generate PRD from discovery output (Mode A handoff) |
| `/pm-prd-reviewer` | `pm-prd-reviewer` | Review and critique an existing PRD |
| `/tom-architect` | `tom-architect` | Design Target Operating Model (Mode B handoff) |
| `/enterprise-architect` | `enterprise-architect` | Solution architecture and technology selection |
