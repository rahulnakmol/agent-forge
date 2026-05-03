Score the output 1-5 on each criterion. Return the AVERAGE.

1. **Tier Decision Accuracy** — Applies correct tier selection logic: Hyperscale for >1TB or fast restore needs, Business Critical for sub-ms IO/in-memory OLTP, General Purpose for standard OLTP. Justifies the recommendation against stated NFRs. Score 5 if tier reasoning is accurate; 1 if recommendation contradicts the decision rules.

2. **Encryption Classification Correctness** — Correctly distinguishes deterministic (searchable PII) vs randomized (non-searchable) vs enclave (range/LIKE queries) Always Encrypted. Does not recommend randomized for equality-searched columns. Score 5 if classification is correct for all columns; 1 if fundamental mistakes are made.

3. **Partition Strategy Soundness** — Recommends date-based sliding window for time-series data, never random hash for partitioning. Addresses archival (switch out/switch in) for retention requirements. Score 5 if partition design is sound; 1 if random hash or inappropriate partition key is recommended.

4. **Operational Depth** — Covers Query Store configuration (read-write mode, capture mode Auto, retention), failover group auto-failover caveats (soak testing), or connection resilience (SqlClient retry + circuit breaker) as appropriate to the scenario. Score 5 if operational guidance is detailed; 1 if surface-level only.

5. **Codified Opinions Applied** — Applies the skill's non-negotiable opinions: read-only routing over app-side splitting, Query Store on every prod DB, Always Encrypted for PII, auto-failover disabled until soak test. Score 5 if opinions are consistently applied; 1 if contrary advice is given.
