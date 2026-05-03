# OWASP ASI Top-10 for AI Agents

The OWASP Agent Security Initiative (ASI) Top-10 identifies the most critical security risks in agentic AI systems: systems where a language model is given tools, memory, and the ability to take autonomous actions. This list is distinct from the OWASP Top-10 for LLM Applications (which focuses on prompt injection and model risks at the API layer) and from the OWASP Top-10 for traditional web applications. The ASI Top-10 addresses the unique risks that arise when an LLM is granted agency: the ability to read, write, call, and decide.

Reference: OWASP Agentic AI Threats and Mitigations: https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/

Microsoft guidance on agentic AI threat modeling: https://learn.microsoft.com/security/zero-trust/sfi/threat-modeling-ai

---

## The ASI Top-10

### ASI-01: Prompt Injection in Agentic Contexts

**Summary:** Malicious instructions embedded in data the agent processes (documents, emails, search results, API responses, database records) override the agent's intended behaviour, causing it to take actions the operator did not authorise.

**Why agents amplify this risk:** A traditional LLM API processes a single request and returns text. An agent processes external data and then *acts*: sending emails, calling APIs, writing to databases, or invoking downstream agents. A successful injection in an agent context can have irreversible real-world consequences, not just an unexpected text output.

**Attack scenarios:**
- User uploads a PDF containing a hidden instruction. The agent summarises the PDF and simultaneously calls its email tool with the PII it retrieved.
- A product review in a database record the agent indexes contains adversarial text that causes the agent to call an unintended tool.
- An indirect injection in a retrieved web page causes a search-and-summarise agent to expose its system prompt.

**Azure mitigations:**
- Azure AI Content Safety Prompt Shields (GA 2025): real-time detection and blocking at the API layer
- Azure AI Foundry Spotlighting (GA May 2025): marks retrieved external content as untrusted before it enters the model context
- Structural channel separation: retrieved external content in `role: user` messages only, never concatenated into `role: system`
- Output schema validation: reject any model response that does not conform to the expected JSON schema before executing tool calls

**Validation gate:** Can an injected instruction in a test document cause the agent to invoke a tool it should not? If yes: mitigations incomplete.

---

### ASI-02: Excessive Agency (Over-Privileged Tool Grants)

**Summary:** The agent is granted more tools, permissions, or capabilities than its intended task requires. An attacker who achieves prompt injection or triggers an unexpected reasoning path can exploit the excess capabilities to cause harm.

**Why this is a systemic risk:** Tool lists are often designed for maximum capability during development and never pruned before production. An agent designed to answer customer questions does not need an email-send tool, a database-write tool, or an HTTP-POST tool. Every unnecessary tool is an attack surface.

**Attack scenarios:**
- A customer service agent with CRM read-write access is manipulated to update account records belonging to a different customer.
- A document-processing agent with blob storage read access is also granted storage account key access for convenience, enabling exfiltration of the entire storage account.
- An agent given a shell execution tool for file processing is prompted to run network commands to exfiltrate data.

**Azure mitigations:**
- Enumerate the minimum tool list for the agent's intended task. Start with zero tools and add only what is proven necessary.
- Microsoft Entra Agent ID: define agent permissions as a first-class identity object (GA November 2025)
- Conditional Access for Agent ID: apply Zero Trust controls to agent identities as to human users
- Require human approval (human-in-the-loop) for any tool call with write, delete, send, or HTTP-POST semantics
- Apply RBAC at the narrowest scope for each tool's underlying identity

**Validation gate:** Remove the agent's write tools. Does it still accomplish its stated purpose? If yes: those write tools were not necessary.

---

### ASI-03: Trust Boundary Violations Between Agents

**Summary:** In multi-agent pipelines, agents implicitly trust messages from other agents. An attacker who compromises one agent in the pipeline, or injects content that one agent passes downstream, can subvert the entire chain.

**Why this is specific to agentic systems:** Multi-agent architectures (orchestrator + sub-agents, planner + executor, human-in-the-loop + automation) create implicit trust relationships. A message from "the orchestrator" is typically accepted as authoritative without cryptographic verification.

**Attack scenarios:**
- An orchestrator agent passes a task to a sub-agent that includes user-controlled content without sanitisation; the sub-agent executes the embedded instructions.
- An attacker compromises a low-trust auxiliary agent (e.g., a web-search agent) and uses it to inject instructions into messages it passes to the high-trust decision-making agent.
- An agent accepts tool results from another agent as ground truth without validation, enabling a data-poisoning attack on the agent's knowledge state.

**Azure mitigations:**
- Microsoft Entra Agent ID: define and enforce trust relationships between agents; each agent-to-agent call is an authenticated identity action
- Agent Registry (Microsoft Entra, November 2025): inventory all agents; detect unauthorised or unexpected agents in the pipeline
- Validate all inter-agent messages as untrusted external input. Apply the same schema validation and content safety checks to agent-to-agent messages as to user inputs.
- Principle of least privilege applies per agent identity, not per pipeline

**Validation gate:** Can a sub-agent cause the orchestrator to take an action outside its authorised scope by crafting a malicious message?

---

### ASI-04: Inadequate Human Oversight for High-Impact Actions

**Summary:** The agent is permitted to take irreversible, high-impact actions (deleting data, sending communications, executing financial transactions, modifying production configuration) autonomously, without a human approval gate.

**Why irreversibility matters:** A traditional application failure is usually recoverable. An agent that sends bulk communications, deletes a production database, or transfers funds to the wrong account has caused harm that may be impossible or extremely costly to reverse.

**Attack scenarios:**
- An agent with access to a customer communication tool is manipulated into sending an unauthorised bulk message to all customers.
- A configuration-management agent modifies a firewall rule to allow inbound traffic on a sensitive port based on an injected instruction.
- An AI-powered incident response agent deletes log files it believes are causing a disk-full alert; the log files were the only forensic evidence of an active breach.

**Azure mitigations:**
- Define "high-impact" actions explicitly in the agent policy. Any action that is irreversible, financially material, or operationally destructive requires human confirmation.
- Azure AI Foundry Task Adherence Evaluation and Mitigation (GA May 2025): continuously validates that agent tasks stay within their defined scope
- Implement a confirmation step in the tool interface: the agent proposes the action and a human approves or denies before execution
- Apply timeout and retry limits: an agent that cannot complete its task without human approval should fail safely, not escalate autonomously

**Validation gate:** What is the most destructive action this agent can take? Can it take that action without a human seeing it first?

---

### ASI-05: Uncontrolled Agent Memory and State Persistence

**Summary:** Agent memory systems (vector stores, conversation histories, external databases used as persistent state) are writable by the agent and, in some architectures, by external inputs. An attacker who can write to agent memory can poison the agent's long-term behaviour without leaving a trace in any individual prompt.

**Attack scenarios:**
- A RAG-based agent writes summaries of processed documents into its memory store. An attacker plants a document with adversarial content; the summary is stored and influences all future agent responses.
- A planner agent stores its task history in a database. An attacker who can write to the database plants a "completed" task, causing the agent to skip a critical security check.
- A user manipulates the agent's conversation memory to make it believe the user has elevated permissions; the memory persists across sessions and grants permanent escalation.

**Azure mitigations:**
- Treat all agent memory writes as sensitive write operations. Apply the same RBAC, audit logging, and anomaly detection as any other data store write.
- Do not store raw user input in memory without sanitisation and schema validation
- Implement memory TTL (time-to-live) and expiry. Agent memory should not accumulate indefinitely.
- Monitor memory content for anomalous insertions using the same content-safety pipeline as input validation
- Separate read-only reference memory (static knowledge base) from read-write session memory; minimise what is read-write

**Validation gate:** Can an attacker cause the agent's future behaviour to change by controlling what it writes to memory today?

---

### ASI-06: Sensitive Data Exposure Through Agent Outputs

**Summary:** The agent retrieves, summarises, or forwards sensitive data to callers or downstream tools that should not have access to it. The agent's retrieval scope and output filtering may be more permissive than the original access controls on the underlying data.

**Attack scenarios:**
- A document Q&A agent retrieves HR records when asked a question about salary; the user asking the question is not authorised to view salary data.
- An agent summarises a Cosmos DB query result that includes records belonging to multiple tenants; the summary leaks cross-tenant data to the requesting user.
- An agent logs its full context window (including system prompt, tool results, and retrieved PII) to an observability tool accessible to all developers.

**Azure mitigations:**
- Apply the same access controls on agent retrievals as on direct API calls. The agent's identity (Managed Identity or Agent ID) should only query data the requesting user is authorised to see.
- Implement retrieval-time authorisation: filter retrieved records by the authenticated user's permissions before passing to the model
- Apply data-minimisation to tool results: return only the fields the agent needs for its task, not full document bodies
- Treat agent observability logs as sensitive. PII in agent context windows must be masked or excluded from telemetry.
- Output filtering: validate agent responses for PII patterns before delivering to the user

**Validation gate:** As User A, can you get the agent to return data that belongs to User B?

---

### ASI-07: Insufficient Audit Trails for Agent Actions

**Summary:** Agent actions (tool calls, decisions, memory writes, inter-agent messages) are not logged in sufficient detail to support incident investigation, regulatory audit, or debugging. When something goes wrong, there is no forensic record of what the agent did and why.

**Why this is a compliance risk:** GDPR Article 5(2) (accountability principle), HIPAA §164.312(b) (audit controls), and the EU AI Act (logging requirements for high-risk AI systems) all require that automated decisions be attributable and auditable.

**Attack scenarios:**
- An agent sends an unauthorised message to a customer. Without a tool-call audit log, it is impossible to determine whether the action was triggered by a prompt injection or a model error.
- An agent deletes records from a database. The database audit log shows the deletion by the agent's service identity but provides no context (which user triggered the agent, what the agent's reasoning was, what the tool call arguments were).
- An agent operating under prompt injection takes a series of actions over multiple turns. Without a per-turn log of tool calls and arguments, investigators cannot reconstruct the attack chain.

**Azure mitigations:**
- Log every tool call: tool name, arguments, result, timestamp, correlation ID, requesting user identity
- Log every agent decision step. Use structured log entries, not free-text.
- Correlate agent logs with the user's Entra ID session and the original request. Use a distributed trace ID that spans the full agentic pipeline.
- Send agent audit logs to a separate, immutable Log Analytics workspace with restricted write access
- Microsoft Foundry Agent Control Plane (November 2025): observe and operate agents with built-in audit trail
- Set minimum retention: 90 days for standard; WORM for regulated workloads

**Validation gate:** Given only the logs from a 30-minute agent session, can you reconstruct exactly what the agent did, which user triggered each action, and what data it accessed?

---

### ASI-08: Model Supply Chain and Dependency Risks

**Summary:** The AI model itself (the weights, fine-tuning datasets, and model dependencies) is a supply-chain attack surface. A compromised or backdoored model can be deployed into production as a trusted component.

**Attack scenarios:**
- A fine-tuned model downloaded from a third-party registry contains an embedded backdoor that causes the model to output sensitive information when a specific trigger phrase is used.
- A model uploaded to Azure Machine Learning workspace contains malware in its serialised weights format.
- A RAG pipeline ingests a poisoned dataset that was altered by an attacker who had write access to the data source; the poisoning gradually shifts the model's retrieval and summarisation behaviour.

**Azure mitigations:**
- Microsoft Defender for AI Services: AI model security (preview 2025) scans models for embedded malware, unsafe operators, and exposed secrets before production deployment
- AI model scanning integrates with Azure ML workspaces and CI/CD pipelines. Trigger model scans at build/release stage before promoting to production.
- Apply data provenance tracking on all RAG corpus sources. Know the origin, last-modified timestamp, and integrity hash of every document in the retrieval index.
- Only use models from trusted, audited registries (Azure AI Foundry Model Catalog); document the supply chain in the SBOM
- Monitor for output drift. Statistical deviation in model outputs over time can indicate ongoing poisoning.

**Validation gate:** If the model used in production today was replaced with a backdoored model tomorrow, would you detect it before it caused harm?

---

### ASI-09: Lack of Rate Limiting and Resource Governance

**Summary:** The agent has no limits on the number of tool calls, external API requests, or tokens consumed per session or per user. An attacker can abuse the agent to exhaust downstream resource quotas, trigger large compute bills, or use the agent as an amplification vector for attacks on external systems.

**Attack scenarios (wallet attacks and amplification):**
- A prompt injection causes the agent to loop, exhausting the Azure OpenAI TPM deployment limit in minutes and blocking legitimate users.
- A user crafts a prompt that causes the agent to make hundreds of web search tool calls per session, exhausting a paid search API quota and generating significant per-request costs.
- An attacker uses the agent's HTTP tool to send requests to a third-party API, using the agent as an amplification vector.

**Azure mitigations:**
- APIM rate-limiting policies: per-user, per-session, and per-deployment limits on Azure OpenAI calls
- Azure OpenAI deployment-level TPM and RPM limits: set conservatively and monitor consumption dashboards
- Per-agent session budget: maximum tool calls per turn, maximum tokens per session, maximum session duration
- Require user authentication before agent access. Unauthenticated agent endpoints are a non-negotiable blocker.
- Alert at 80% budget consumption; auto-terminate sessions that hit 100% budget
- Azure AI Foundry continuous monitoring and evaluation: detect anomalous consumption patterns

**Validation gate:** Can a single malicious user exhaust the agent's downstream resource budget and block all other users?

---

### ASI-10: Insecure Plugin and Tool Interfaces

**Summary:** External tools and plugins registered with the agent accept inputs without validation, trust the agent's claims without authentication, or expose unsafe operations without authorisation checks. The agent is only as secure as its weakest tool.

**Attack scenarios:**
- An agent's email-send tool accepts the recipient address as a parameter; an attacker injects a different recipient address via prompt injection, sending sensitive data to an attacker-controlled inbox.
- An agent's web-fetch tool does not restrict the URLs it can retrieve, allowing prompt injection to redirect it to internal IP ranges (SSRF: Server-Side Request Forgery against the VNet).
- A third-party plugin registered with the agent handles authentication tokens insecurely, logging them to its own telemetry and exposing them to the plugin vendor.

**Azure mitigations:**
- Apply schema validation and allowlist filtering on all tool inputs at the tool interface layer. Do not rely solely on the model to produce safe tool arguments.
- Restrict URL-fetching tools to an allowlist of approved domains; block RFC 1918 and link-local ranges (SSRF prevention)
- Do not pass authentication tokens as tool arguments. The tool should acquire its own identity context via Managed Identity or Agent ID.
- Audit every third-party plugin for its data handling practices; require a BAA for plugins handling PHI; require SOC 2 Type II for plugins handling PII
- Apply RBAC at the tool's backend: the tool's service identity should have narrowest-scope permissions, independent of the agent's identity

**Validation gate:** Given only tool-call arguments, can a tool safely execute the requested action without trusting any agent-supplied identity claims?

---

## Mapping ASI Top-10 to Azure Controls

| ASI Item | Primary Azure platform control | Application / architecture control |
|---|---|---|
| ASI-01 Prompt Injection | AI Content Safety Prompt Shields; Foundry Spotlighting | Structural channel separation; output schema validation |
| ASI-02 Excessive Agency | Microsoft Entra Agent ID; Conditional Access for agents | Minimum tool list; human approval for writes |
| ASI-03 Trust Boundary Violations | Entra Agent ID + Agent Registry; authenticated inter-agent calls | Schema validation on inter-agent messages |
| ASI-04 Insufficient Human Oversight | Foundry Task Adherence Evaluation | Human-in-the-loop confirmation for irreversible actions |
| ASI-05 Memory Poisoning | Defender for AI supply chain detection | Memory TTL; sanitise writes; read-only reference memory |
| ASI-06 Data Exposure | Managed Identity + RBAC on retrieval; APIM output filter | Retrieval-time authorisation; data minimisation on tool results |
| ASI-07 Insufficient Audit | Foundry Agent Control Plane; Log Analytics immutable retention | Tool-call audit log per turn; distributed trace ID |
| ASI-08 Supply Chain | Defender for AI model scanning; AI model security (preview) | Data provenance; SBOM; output drift monitoring |
| ASI-09 Resource Governance | APIM rate limiting; Azure OpenAI TPM/RPM limits | Per-session budget; authenticated access required |
| ASI-10 Insecure Tool Interfaces | Managed Identity for tool backends; APIM schema validation | URL allowlists; tool-input schema validation; no token in args |

---

## When to Use the OWASP ASI Top-10

Apply the ASI Top-10 to every system that includes:
- An LLM with access to tools (function calling, MCP tools, plugin calls)
- An autonomous agent or multi-agent pipeline
- A RAG (Retrieval-Augmented Generation) pipeline that retrieves external, untrusted content
- A Copilot Studio agent or Azure AI Foundry agent with connectors

The ASI Top-10 supplements the Abuse (A) category of STRIDE-A; it does not replace it. STRIDE-A gives the per-threat-vector analysis; the ASI Top-10 gives the systemic agentic architecture assessment.

Reference `references/mitre-atlas-ai.md` for the corresponding MITRE ATLAS tactic and technique coverage.
