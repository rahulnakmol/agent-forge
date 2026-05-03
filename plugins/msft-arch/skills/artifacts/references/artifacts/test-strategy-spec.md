---
category: artifacts
loading_priority: 2
tokens_estimate: 1400
keywords:
  - test strategy
  - test plan
  - workbook
  - xlsx
  - test type
  - acceptance criteria
  - automation
  - UAT
  - test scenario
version: "1.0"
last_updated: "2026-03-21"
---

# Test Strategy Workbook Specification

This document defines the complete specification for the Test Strategy Excel workbook. The workbook is generated during Phase 4 (Validation) and captures all test scenarios, acceptance criteria, priority levels, environment targets, and automation approach for the solution.

## Sheet 1: "Test Strategy"

### Column Specifications

#### Column A: Test ID (width: 12)
- Unique identifier for each test entry.
- Format: `TST-[NNN]` where NNN is a zero-padded sequential number.
- Examples: `TST-001`, `TST-002`, `TST-015`.

#### Column B: Epic/Module (width: 30)
- Links to the Epic/Module/Work stream from the Effort Estimation workbook.
- Must use the same grouping labels for traceability.
- Examples: "Customer Service AI", "Identity & Access", "Data Migration", "Integration Layer".

#### Column C: Test Type (width: 18)
- Data validation dropdown:
  - **Unit**: Individual component or function tests
  - **Integration**: Tests verifying interaction between components
  - **E2E**: End-to-end workflow tests spanning multiple systems
  - **Performance**: Load, stress, and scalability tests
  - **Security**: Penetration, vulnerability, and compliance tests
  - **UAT**: User acceptance tests driven by business stakeholders

#### Column D: Test Scenario (width: 55, wrap text enabled)
- Description of what is being tested.
- Use clear, testable statements that describe the scenario and expected behavior.
- Start with "Verify that..." or "Validate that..." for consistency.

#### Column E: Acceptance Criteria (width: 55, wrap text enabled)
- Pass/fail criteria for the test.
- Use measurable, unambiguous statements.
- Bullet-point format for multiple criteria:
  ```
  • Response returned within 2 seconds
  • AI suggestion accuracy >= 85%
  • No PII exposed in response payload
  ```

#### Column F: Priority (width: 12)
- Data validation dropdown:
  - **Critical**: Must pass for go-live; blocks release
  - **High**: Must pass; workaround acceptable temporarily
  - **Medium**: Should pass; does not block release
  - **Low**: Nice to have; can be deferred

**Color coding:**
| Priority | Background Color  |
| -------- | ----------------- |
| Critical | Red (#FF0000)     |
| High     | Orange (#FFA500)  |
| Medium   | Yellow (#FFFF00)  |
| Low      | Green (#00B050)   |

#### Column G: Environment (width: 12)
- Data validation dropdown:
  - **Dev**: Development environment
  - **Test**: QA/Test environment
  - **Staging**: Pre-production staging environment
  - **Prod**: Production environment

#### Column H: Automation (width: 18)
- Data validation dropdown:
  - **Automated**: Fully automated test execution
  - **Manual**: Requires manual test execution
  - **Semi-automated**: Partially automated with manual verification steps

#### Column I: Status (width: 15)
- Data validation dropdown:
  - **Not Started**: Test not yet begun
  - **In Progress**: Test is currently being executed
  - **Passed**: Test executed and passed all acceptance criteria
  - **Failed**: Test executed and did not meet acceptance criteria
  - **Blocked**: Test cannot proceed due to a dependency or issue

### Sheet 1 Formatting

- **Header row:** Bold, dark blue background (#003366), white text (#FFFFFF), freeze pane on row 1.
- **Alternating row colors:** Odd rows white (#FFFFFF), even rows light gray (#F2F2F2).
- **Conditional formatting:** Applied to Column F (Priority) with the color coding above.
- **Wrap text:** Enabled on Columns D and E.
- **Auto-filter:** Enabled on all columns (A through I).
- **Font:** Calibri 10pt for data rows, Calibri 11pt bold for headers.

---

## Sheet 2: "Test Summary"

A dashboard sheet providing aggregated test metrics.

### Section 1: Count by Test Type (rows 2-9)
| Test Type    | Count          | Percentage   |
| ------------ | -------------- | ------------ |
| Unit         | =COUNTIFS(...) | =.../Total   |
| Integration  | =COUNTIFS(...) | =.../Total   |
| E2E          | =COUNTIFS(...) | =.../Total   |
| Performance  | =COUNTIFS(...) | =.../Total   |
| Security     | =COUNTIFS(...) | =.../Total   |
| UAT          | =COUNTIFS(...) | =.../Total   |
| **Total**    | =COUNTA(...)   |              |

### Section 2: Count by Priority (rows 11-16)
| Priority  | Count          |
| --------- | -------------- |
| Critical  | =COUNTIFS(...) |
| High      | =COUNTIFS(...) |
| Medium    | =COUNTIFS(...) |
| Low       | =COUNTIFS(...) |

### Section 3: Count by Status (rows 18-24)
| Status       | Count          |
| ------------ | -------------- |
| Not Started  | =COUNTIFS(...) |
| In Progress  | =COUNTIFS(...) |
| Passed       | =COUNTIFS(...) |
| Failed       | =COUNTIFS(...) |
| Blocked      | =COUNTIFS(...) |

### Section 4: Pass Rate (row 26)
```
Pass Rate = Passed / (Passed + Failed) * 100
```
Displayed as a percentage with conditional formatting: >=90% Green, 70-89% Yellow, <70% Red.

---

## Security Testing Patterns

When the Test Type is **Security**, apply these automated security testing patterns:

| Pattern | Tool Category | When to Run | What It Finds |
|---------|--------------|-------------|---------------|
| **SAST** (Static Application Security Testing) | SonarQube, Roslyn Analyzers, Semgrep | Every CI build | Code-level vulnerabilities, injection flaws, hardcoded secrets |
| **DAST** (Dynamic Application Security Testing) | OWASP ZAP, Burp Suite | Pre-release in staging | Runtime vulnerabilities, auth bypass, XSS, CSRF |
| **IAST** (Interactive Application Security Testing) | Contrast Security, Hdiv | Integration test phase | Runtime code path analysis with real traffic |
| **SCA** (Software Composition Analysis) | Dependabot, Snyk, Trivy | Every CI build | Vulnerable dependencies, license compliance |
| **Container Scanning** | Trivy, Azure Defender | Image build + registry | Image vulnerabilities, misconfigurations |
| **IaC Scanning** | Checkov, tfsec, Terrascan | Terraform plan phase | Insecure infrastructure configurations |
| **Penetration Testing** | Manual + automated | Quarterly or pre-major-release | Business logic flaws, complex attack chains |

**Security Test Automation Pipeline**:
```
Code Commit → SAST + SCA (CI) → Build → Container Scan → Deploy to Staging → DAST → IAST (with integration tests) → Pen Test (quarterly)
```

**Security Test Scenarios to Include**:
- Authentication bypass attempts (invalid tokens, expired tokens, forged tokens)
- Authorization escalation (user accessing admin endpoints, cross-tenant data access)
- Injection attacks (SQL injection, command injection, XSS via all input fields)
- Data exposure (sensitive data in error messages, API responses, logs)
- Rate limiting verification (brute force protection, API throttling)
- Certificate validation (expired certs, self-signed certs, TLS version downgrade)

---

## Example Data Rows (Sheet 1)

| Test ID | Epic/Module         | Test Type   | Test Scenario                                                                                          | Acceptance Criteria                                                                                                     | Priority | Environment | Automation     | Status      |
| ------- | ------------------- | ----------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------- | ----------- | -------------- | ----------- |
| TST-001 | Customer Service AI | E2E         | Verify that the AI Copilot returns a relevant response when an agent submits a customer query           | • Response within 2 seconds\n• Accuracy >= 85%\n• No PII in payload                                                    | Critical | Test        | Automated      | Not Started |
| TST-002 | Customer Service AI | Unit        | Verify that the RAG retrieval pipeline returns top-5 relevant documents from the knowledge base         | • Top-5 docs returned\n• Relevance score >= 0.7\n• Response under 500ms                                                 | High     | Dev         | Automated      | Not Started |
| TST-003 | Identity & Access   | Security    | Validate that Conditional Access blocks sign-in from non-compliant devices                              | • Non-compliant device blocked\n• Audit log entry created\n• User receives clear error message                           | Critical | Staging     | Semi-automated | Not Started |
| TST-004 | Data Migration      | Integration | Verify that customer records migrated from on-prem SQL match the Dataverse schema and row counts         | • Row count matches source ± 0\n• All required fields populated\n• No orphaned references                               | Critical | Test        | Automated      | Not Started |
| TST-005 | Integration Layer   | Performance | Validate that Azure Service Bus handles 10,000 messages per minute under peak load                       | • Throughput >= 10k msg/min\n• No message loss\n• P99 latency < 200ms                                                   | High     | Staging     | Automated      | Not Started |
| TST-006 | Customer Service AI | UAT         | Validate that service agents can use the Copilot to resolve a sample set of 20 historical tickets        | • 18/20 tickets resolved using Copilot\n• Agent satisfaction score >= 4/5\n• No escalations due to incorrect suggestions | High     | Staging     | Manual         | Not Started |

---

## xlsx Skill Invocation Pattern

```
Invoke the xlsx skill to create an Excel workbook with:
- Sheet 1 name: "Test Strategy"
  - Columns: [A: "Test ID" (12), B: "Epic/Module" (30), C: "Test Type" (18),
    D: "Test Scenario" (55, wrap), E: "Acceptance Criteria" (55, wrap),
    F: "Priority" (12), G: "Environment" (12), H: "Automation" (18), I: "Status" (15)]
  - Data validation on C: ["Unit", "Integration", "E2E", "Performance", "Security", "UAT"]
  - Data validation on F: ["Critical", "High", "Medium", "Low"]
  - Data validation on G: ["Dev", "Test", "Staging", "Prod"]
  - Data validation on H: ["Automated", "Manual", "Semi-automated"]
  - Data validation on I: ["Not Started", "In Progress", "Passed", "Failed", "Blocked"]
  - Conditional formatting on F: Critical=Red, High=Orange, Medium=Yellow, Low=Green
  - Header formatting: bold, #003366 background, white text
  - Freeze top row, auto-filter enabled
- Sheet 2 name: "Test Summary"
  - COUNTIFS tables by Test Type, Priority, Status
  - Pass rate formula
- Data: [provide rows]
```
