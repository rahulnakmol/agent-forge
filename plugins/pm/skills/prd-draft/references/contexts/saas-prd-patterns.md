# SaaS PRD Patterns

## How PRDs Differ in SaaS Product Companies

SaaS PRDs are metric-driven, user-centric, and growth-oriented. They focus on engagement, activation, retention, and expansion rather than deliverable milestones and client approvals. The PRD is a living document that evolves with data.

---

## Product-Led Growth (PLG) Metrics in PRDs

SaaS PRDs must tie every epic to measurable product metrics. Use the pirate metrics framework (AARRR) to classify where each epic contributes.

| Stage | Metric Focus | PRD Section Impact |
|-------|-------------|-------------------|
| **Acquisition** | Sign-up rate, channel conversion, cost per acquisition | Success Metrics: track acquisition funnel |
| **Activation** | Time-to-value, onboarding completion, first key action | Success Metrics: activation rate as leading indicator |
| **Retention** | DAU/WAU/MAU, churn rate, session frequency | Success Metrics: retention cohorts as lagging indicator |
| **Revenue** | ARPU, conversion to paid, expansion revenue, LTV | Business Context: quantify revenue impact |
| **Referral** | NPS, viral coefficient, invite conversion | Features: social and sharing stories if applicable |

### Metric Selection Rules

- Every SaaS epic PRD must include at least one activation metric and one retention metric
- Acquisition metrics only if the epic directly affects the signup or onboarding flow
- Revenue metrics if the epic touches pricing, billing, or premium features
- Referral metrics only if the epic includes sharing or collaboration features

---

## Feature Flags and Phased Rollouts

SaaS PRDs should specify feature flag strategy in Section 11 (Release & Rollout).

### Feature Flag Patterns

| Pattern | Use Case | PRD Guidance |
|---------|----------|-------------|
| **Kill switch** | Safety valve for new features | Default for all MH stories -- specify rollback trigger |
| **Percentage rollout** | Gradual exposure to user base | Specify rollout stages: 1% -> 10% -> 50% -> 100% |
| **Segment targeting** | Different experience per user tier | Specify which segments see the feature first |
| **A/B test** | Compare variants for optimization | Define control and variant, success metric, sample size |
| **Beta flag** | Early adopter access | Define opt-in mechanism and feedback channel |

### Rollout Section Adaptation

For SaaS PRDs, Section 11 should include:

```markdown
### Feature Flag Configuration
- Flag name: `{feature-flag-name}`
- Default state: OFF
- Rollout plan: Internal (1 week) -> Beta 5% (2 weeks) -> GA 100%
- Kill criteria: Error rate > 0.5% OR p95 latency > 2s OR negative NPS delta > 5 points
- Metrics to monitor during rollout: {list}
```

---

## User Behavior and Engagement Metrics

SaaS persona sections (Section 2) emphasize behavior data over organizational charts.

### Persona Enrichment for SaaS

| Attribute | Purpose | Example |
|-----------|---------|---------|
| **Behavior patterns** | How they use the product today | "Logs in 3x/week, primarily uses reporting module" |
| **Engagement tier** | Power user vs casual vs dormant | "Power user: >20 sessions/month, uses 5+ features" |
| **Feelings & frustrations** | Emotional drivers for churn or expansion | "Frustrated by manual CSV export for monthly reports" |
| **Activation milestone** | What made them a retained user | "Completed first custom dashboard within 7 days" |
| **Expansion signals** | What indicates they need more | "Hitting storage limits, inviting team members" |
| **Churn signals** | What predicts they will leave | "Login frequency dropped 50% over 30 days" |

### Journey-Based Stories

SaaS user stories often map to the user journey:

1. **First-run stories**: What happens the first time (onboarding, guided setup)
2. **Core loop stories**: The repeated action that delivers ongoing value
3. **Aha moment stories**: Features that create the "this is worth paying for" realization
4. **Expansion stories**: Capabilities that drive seat growth or tier upgrades
5. **Win-back stories**: Re-engagement features for dormant users

---

## Competitive Positioning

SaaS PRDs should reference competitive context in Section 1 (Business Context) when relevant.

### Competitive Context Template

```markdown
### Competitive Landscape

| Competitor | Approach | Our Differentiation |
|-----------|----------|-------------------|
| {name} | {how they solve this problem} | {why our approach is better for our persona} |

**Parity features** (must match market): {list}
**Differentiating features** (where we lead): {list}
**Concession features** (where we intentionally lag): {list with rationale}
```

---

## Growth Stage Adaptations

PRD emphasis shifts based on product maturity.

### Early Stage (0-1, PMF seeking)

| PRD Adaptation | Rationale |
|---------------|-----------|
| Fewer stories per epic (3-5) | Speed over comprehensiveness |
| Higher tolerance for CH deprioritization | Ship fast, learn, iterate |
| Success metrics focused on activation | Prove the value hypothesis |
| Simpler rollout (ship to all) | Audience too small for staged rollout |
| Open Questions section is larger | More unknowns are acceptable |

### Growth Stage (1-N, scaling)

| PRD Adaptation | Rationale |
|---------------|-----------|
| Medium story count (5-10) | Balance speed and quality |
| Feature flags mandatory | Protect existing user base during changes |
| Success metrics include retention + revenue | Prove sustainable growth |
| A/B testing in rollout strategy | Data-driven feature optimization |
| Persona engagement tiers differentiated | Power users vs new users have different needs |

### Mature Product (optimization)

| PRD Adaptation | Rationale |
|---------------|-----------|
| Full story count (8-15) | Comprehensive coverage, less tolerance for gaps |
| Performance and reliability stories included | Scale demands NFR attention |
| Success metrics include efficiency and cost | Optimize unit economics |
| Backward compatibility explicitly scoped | Large installed base to protect |
| Migration stories for existing users | Cannot break current workflows |

---

## SaaS-Specific Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| No activation metric | Cannot prove the feature delivers value | Add time-to-first-value measurement |
| Feature-first, persona-second | Building solutions without validated problems | Start from persona pain, derive features |
| No rollback criteria | Risky deployment without safety net | Every feature flag needs a kill criteria |
| Vanity metrics only | Tracking page views instead of value delivery | Use engagement depth metrics (completion, repeat use) |
| Ignoring existing users | New feature breaks established workflows | Include migration and backward compatibility stories |
| No competitive context | Building in a vacuum | Reference market expectations even briefly |

---

*pm-prd-generator v1.0 | SaaS PRD Patterns*
