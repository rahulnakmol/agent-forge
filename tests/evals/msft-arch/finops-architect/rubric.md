Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Mandatory Tagging Enforcement** — Requires all 5 mandatory tags (cost-center, environment, owner, project, expiry) on every resource. Enforces via Azure Policy with Audit ramp-up followed by Deny effect. No exceptions. Score 5 if all 5 tags are required and Policy enforcement is specified; 1 if tags are optional or enforcement is missing.

2. **Commitment Vehicle Selection** — Applies the correct decision rule: Reserved Instances for >60% stable workloads with fixed VM family/region; Compute Savings Plans for flexible compute; on-demand for spikes. Azure Hybrid Benefit assessed for Windows Server. Covers at least 70% of baseline compute. Score 5 if commitment vehicles are correctly selected for the scenario; 1 if all workloads are recommended as on-demand or the rule is not applied.

3. **Showback Before Chargeback** — Recommends showback as the minimum (weekly cost report for all teams); chargeback only after tagging compliance exceeds 90% and teams have budget authority. Never charges teams for shared platform costs they cannot control. Score 5 if showback/chargeback decision is correctly sequenced; 1 if chargeback is recommended before tagging compliance is established.

4. **Anomaly Detection Configuration** — Configures anomaly alerts at subscription and resource group scope with >20% week-over-week threshold. Routes to action groups connected to the team's incident channel. Does not rely solely on budget alerts. Score 5 if anomaly detection is comprehensively configured; 1 if only budget alerts are recommended.

5. **Right-Sizing Methodology** — Requires a 30-day P95 baseline before any SKU downsize recommendation. Does not rely solely on Azure Advisor. Plans for quarterly re-evaluation. Score 5 if right-sizing follows the baseline-first methodology; 1 if immediate downsizing is recommended based on Advisor alone without a baseline period.
