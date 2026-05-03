# Intercom-Style PRD Example

## About This Style

Intercom PRDs are metric-heavy, hypothesis-driven, and focused on business impact measurement. Every feature starts with a problem hypothesis and ends with a measurement plan. The format is lean, avoids ceremony, and emphasizes the "why" over the "what."

Key characteristics:
- Problem-first framing with data-backed evidence
- Explicit success/failure criteria before building
- Bet sizing (Small/Medium/Large) tied to confidence level
- Shipping mindset: what is the smallest thing we can ship to learn?

---

## Example: Smart Inbox Prioritization

```markdown
# Smart Inbox Prioritization -- PRD

**Author**: Sarah Chen, PM -- Inbox Team
**Date**: 2026-03-15
**Status**: In Review
**Bet Size**: Medium (4-6 weeks, 3 engineers + 1 designer)

---

## Problem

### Evidence

Support reps spend 35% of their time triaging inbox conversations before responding.
Source: Time-motion study, Q4 2025, n=42 reps across 8 customers.

Average first-response time is 4.2 hours. Industry benchmark is 1.5 hours.
Source: Intercom benchmark report, 2025.

23% of conversations are misprioritized (urgent marked as normal, or vice versa).
Source: QA audit of 500 random conversations, Feb 2026.

### Hypothesis

If we automatically prioritize inbox conversations using signal analysis (sentiment,
customer tier, topic urgency, SLA proximity), support reps will spend less time
triaging and more time responding, reducing first-response time by 40%.

### What Happens If We Do Nothing

- First-response time stays at 4.2 hours (3x industry benchmark)
- Customer satisfaction continues to decline (CSAT dropped 8 points in 6 months)
- Churn risk for Enterprise customers increases (3 Enterprise accounts cited response
  time in churn exit interviews last quarter)

---

## Solution

### How It Works

1. Every incoming conversation is scored on 4 signals:
   - Sentiment (negative/neutral/positive from message text)
   - Customer tier (Enterprise/Growth/Starter from account data)
   - Topic urgency (billing, outage, bug > feature request, question)
   - SLA proximity (time remaining before SLA breach)

2. Conversations are ranked in the inbox by composite priority score
3. Reps see a priority badge (Critical/High/Normal/Low) on each conversation
4. Reps can override priority with one click (feedback loop for model improvement)

### What We Are NOT Building

- Automated responses (that is a separate initiative)
- Custom priority rules per team (v2 consideration)
- Integration with external ticketing systems (out of scope)

---

## User Stories

### Story 1: Prioritized Inbox View (Must Have)

As a support rep, I want my inbox sorted by AI-determined priority,
so that I work on the most critical conversations first without manual triage.

Given I open my inbox with 50 unassigned conversations
When the inbox loads
Then conversations are sorted by priority score (highest first)
  And each conversation displays a priority badge (Critical/High/Normal/Low)
  And the sort order updates in real-time as new conversations arrive

### Story 2: Priority Override (Must Have)

As a support rep, I want to override the AI priority with one click,
so that I can correct misclassifications based on my domain knowledge.

Given I am viewing a conversation marked as "Normal" priority
When I click the priority badge and select "Critical"
Then the conversation moves to the top of the queue
  And the override is logged for model retraining
  And a brief toast confirms "Priority updated to Critical"

### Story 3: Priority Explanation (Should Have)

As a support rep, I want to see why a conversation was prioritized,
so that I trust the system and can identify patterns.

Given I am viewing a Critical-priority conversation
When I hover over the priority badge
Then I see the contributing signals: "Enterprise customer, negative sentiment,
  billing topic, SLA breach in 45 minutes"

### Story 4: Team Priority Dashboard (Could Have)

As a support manager, I want a dashboard showing priority distribution and
override rates, so that I can assess triage efficiency and model accuracy.

Given I navigate to the Priority Analytics dashboard
When the page loads
Then I see: priority distribution (pie chart), override rate (%), avg time-to-first-response
  by priority tier, model accuracy trend (weekly)

---

## Success Metrics

### Primary (must hit for this bet to succeed)

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| First-response time | 4.2 hours | 2.5 hours (-40%) | 8 weeks post-launch |
| Triage time per rep | 35% of shift | 15% of shift | 8 weeks post-launch |

### Secondary (signals health but not bet-defining)

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| Priority accuracy (1 - override rate) | N/A | > 85% | 4 weeks post-launch |
| CSAT score | 72 | 78 | 12 weeks post-launch |
| Rep NPS for inbox tool | 32 | 50 | 8 weeks post-launch |

### Failure Criteria (kill the feature if)

- Override rate exceeds 40% after 4 weeks (model is wrong more than it is right)
- First-response time does not improve by at least 15% after 6 weeks
- Rep complaints about priority noise exceed 10 tickets/week

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Model accuracy too low at launch | Medium | High | Launch with override and feedback loop; retrain weekly |
| Reps ignore priority and sort manually | Medium | Medium | Default sort is priority; manual sort requires explicit action |
| Enterprise customers game the system | Low | Medium | Priority uses multiple signals; single-signal gaming has limited effect |

---

## Rollout

1. **Week 1-2**: Internal dogfooding (Intercom support team)
2. **Week 3-4**: Beta with 10 opted-in customers
3. **Week 5**: GA with feature flag, default ON for new workspaces
4. **Week 8**: Evaluate primary metrics, decide on continued investment

Kill switch: Feature flag `smart_inbox_priority` -- disable reverts to chronological sort.

---

## Open Questions

| Question | Owner | Due |
|----------|-------|-----|
| Can we use existing sentiment model or need to train a new one? | ML team | 2026-03-22 |
| Do we need SOC2 review for conversation content analysis? | Security | 2026-03-25 |
```

---

## Style Principles to Apply

When generating Intercom-style PRDs, follow these principles:

1. **Evidence before solution**: Always present data (or the absence of data) that justifies the feature
2. **Explicit bet sizing**: State the investment (weeks, headcount) and confidence level
3. **Failure criteria are mandatory**: Define what "this did not work" looks like
4. **Lean sections**: No section should be longer than it needs to be
5. **Shipping cadence**: Include a concrete rollout timeline with evaluation gates
6. **Override culture**: Trust users to correct the system; build feedback loops
7. **Metric pairs**: Every primary metric has a secondary metric to prevent gaming (e.g., faster response time without quality degradation)

---

*pm-prd-generator v1.0 | Intercom-Style PRD Example*
