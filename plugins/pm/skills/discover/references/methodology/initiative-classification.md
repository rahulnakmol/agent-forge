# Initiative Classification Framework

## Purpose

Classifying the initiative type during Phase 4 determines the downstream approach: what deliverables to produce, which skill to hand off to, what level of process analysis is needed, and how the Business Understanding Document is structured. Every initiative maps to exactly one primary type, though hybrid characteristics are common.

---

## Four Initiative Types

### 1. Product Development

**Definition**: Creating a new product, feature, or capability that does not exist today.

**Characteristics**:
- Net-new functionality for users
- Requires market/user research to validate demand
- Involves design, engineering, and go-to-market planning
- Success measured by adoption, revenue, and user satisfaction

**Examples**:
- Building a customer self-service portal
- Launching a mobile app for field workers
- Adding AI-powered search to an existing platform
- Creating a partner integration marketplace

**Discovery emphasis**:
- User personas and JTBD (what job are they hiring this product to do?)
- Competitive analysis (what alternatives exist?)
- Market sizing and business case
- User journey mapping for the new experience

**Downstream routing**:
- Mode A -> `/pm-prd-generator` (always)
- Mode B -> `/pm-prd-generator` after initial process discovery, or `/tom-architect` if the product is part of a larger transformation

**Process flow focus**: User interaction flows, system sequence diagrams, feature state machines

---

### 2. Process Improvement

**Definition**: Optimizing an existing business process to reduce cost, time, errors, or improve quality.

**Characteristics**:
- Process already exists but is suboptimal
- Focus on removing waste, bottlenecks, and unnecessary handoffs
- Often involves reorganizing roles or responsibilities
- Success measured by cycle time, error rate, cost per transaction

**Examples**:
- Reducing invoice approval cycle time from 15 days to 3 days
- Standardizing procurement processes across 5 regions
- Eliminating duplicate data entry between CRM and ERP
- Improving change management approval workflows

**Discovery emphasis**:
- Current-state process mapping (as-is flows)
- Bottleneck identification and root cause analysis
- Role/RACI analysis for process actors
- Benchmarking against industry standards

**Downstream routing**:
- Mode A -> `/pm-prd-generator` (if improvement is product-driven)
- Mode B -> `/tom-architect` (typically -- process improvement usually requires TOM context)

**Process flow focus**: Current-state BPMN with pain point annotations, target-state BPMN with improvements highlighted, swimlane diagrams showing changed responsibilities

---

### 3. Process Automation

**Definition**: Automating manual steps in an existing process using technology (RPA, workflow engines, integrations).

**Characteristics**:
- Manual process steps are replaced by system-driven execution
- Rules are well-defined and codifiable
- Human judgment is minimal or can be bounded by business rules
- Success measured by automation rate, processing speed, error elimination

**Examples**:
- Auto-generating purchase orders from approved requisitions
- Automated invoice matching against receipts and POs (3-way match)
- Scheduled report generation and distribution
- Automated employee onboarding provisioning (accounts, access, equipment)

**Discovery emphasis**:
- Detailed current-state process mapping (every manual step)
- Decision logic documentation (what rules govern each decision?)
- Exception handling (what happens when automation cannot proceed?)
- Integration requirements (what systems need to connect?)

**Downstream routing**:
- Mode A -> `/pm-prd-generator` (automation as a product feature)
- Mode B -> `/tom-architect` (automation within operational transformation)

**Process flow focus**: Detailed BPMN with manual vs automated step annotations, state machines for automated entity lifecycle, integration flow diagrams

---

### 4. AI/Agent-Based Automation

**Definition**: Leveraging artificial intelligence, machine learning, or autonomous agents to handle tasks that require judgment, pattern recognition, or natural language understanding.

**Characteristics**:
- Tasks require cognitive capabilities beyond simple rule-based logic
- Involves training data, model selection, or agent orchestration
- Human-in-the-loop patterns for confidence thresholds
- Success measured by accuracy, autonomy rate, cost savings, user satisfaction

**Examples**:
- AI agent for first-level customer support triage and resolution
- Intelligent document processing for unstructured invoices
- Predictive maintenance alerts based on IoT sensor data
- AI-assisted contract review and risk flagging
- Autonomous procurement agent that negotiates with pre-approved vendors

**Discovery emphasis**:
- Current decision-making process (how do humans make these decisions today?)
- Data availability and quality (what data exists to train/inform the AI?)
- Confidence thresholds (when should AI act autonomously vs escalate?)
- Ethical and compliance considerations (bias, explainability, audit trail)
- Change management (how will humans adapt to AI colleagues?)

**Downstream routing**:
- Mode A -> `/pm-prd-generator` (AI as a product feature)
- Mode B -> `/tom-architect` (AI augmentation overlay is a core TOM layer)

**Process flow focus**: Human-AI interaction flows, escalation state machines, confidence-based routing diagrams, agent orchestration flows

---

## Classification Decision Framework

Use this decision tree to classify the initiative:

```
1. Does the capability exist today?
   |
   +-- NO --> Does it require AI/ML/agent capabilities?
   |          |
   |          +-- YES --> AI/Agent-Based Automation
   |          +-- NO  --> Product Development
   |
   +-- YES --> Is the goal to automate manual steps?
              |
              +-- YES --> Does automation require cognitive judgment?
              |          |
              |          +-- YES --> AI/Agent-Based Automation
              |          +-- NO  --> Process Automation
              |
              +-- NO  --> Process Improvement
```

## Hybrid Initiatives

Many initiatives span multiple types. When this happens:

1. **Identify the primary type** based on the dominant characteristic
2. **Note secondary types** as sub-themes in the Business Understanding Document
3. **Route based on primary type** but flag hybrid nature for downstream skills

### Common Hybrids

| Primary | Secondary | Example |
|---------|-----------|---------|
| Process Improvement | Process Automation | "Streamline procurement, then automate PO generation" |
| Product Development | AI/Agent-Based | "Build a support portal with AI triage" |
| Process Automation | AI/Agent-Based | "Automate invoice processing including unstructured document reading" |
| Process Improvement | Product Development | "Standardize the process, then build a tool to support it" |

## How Classification Drives Downstream Deliverables

| Initiative Type | Business Understanding Doc Emphasis | Process Flow Types | Handoff Skill |
|----------------|-------------------------------------|-------------------|---------------|
| Product Development | User personas, JTBD, competitive analysis, user journeys | User flows, feature states | pm-prd-generator |
| Process Improvement | Current vs target process, bottleneck analysis, RACI | BPMN (as-is + to-be), swimlane | tom-architect |
| Process Automation | Decision logic, exception handling, integration requirements | BPMN with automation annotations, state machines | tom-architect |
| AI/Agent-Based | Decision patterns, data landscape, confidence thresholds, ethics | Human-AI interaction, escalation flows, agent orchestration | tom-architect |

## Classification Validation Checklist

Before finalizing classification, verify:

- [ ] The primary type is supported by evidence from discovery (not assumed)
- [ ] Hybrid characteristics are acknowledged and documented
- [ ] The downstream routing makes sense given the organizational context
- [ ] Stakeholders agree with the classification (present it for validation)
- [ ] The classification has not been influenced by solution preferences ("we want to use AI" does not make it AI/Agent-Based if the problem is process improvement)
