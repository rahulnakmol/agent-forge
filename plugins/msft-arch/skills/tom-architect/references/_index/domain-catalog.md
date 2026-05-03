---
category: index
loading_priority: 2
tokens_estimate: 2200
keywords:
  - domain catalog
  - section availability
  - domain coverage
  - file counts
  - token estimates
  - finance
  - HR
  - procurement
  - SCM
  - cyber
  - sustainability
  - cross-reference
version: "1.0"
last_updated: "2026-03-23"
---

# Domain Catalog

Matrix showing which TOM sections are available per functional domain, with file counts and token estimates.

---

## Section Availability by Domain

| Section | Name | Finance | HR | Procurement | SCM | Cyber | Sustainability |
|---------|------|:-------:|:--:|:-----------:|:---:|:-----:|:--------------:|
| 1.1 | Process Taxonomies | Y | Y | Y | Y | Y | Y |
| 1.2 | Maturity Models | Y | Y | Y | Y | Y | Y |
| 1.3 | Process Flows | Y | Y | Y | Y | Y | Y |
| 1.4 | Leading Practices | Y | Y | Y | Y | Y | Y |
| 2.1 | Global Process Owners | Y | Y | Y | Y | Y | Y |
| 2.2 | Role Mapping & Sizing | Y | Y | Y | Y | Y | Y |
| 2.3 | Job Profiles | Y | Y | Y | Y | Y | Y |
| 3.1 | Service Delivery Model | Y | Y | Y | Y | Y | Y |
| 3.2 | Service Management | Y | Y | Y | Y | Y | Y |
| 4.1 | AI Augmentation | Y | Y | Y | Y | Y | Y |
| 4.2 | Technology Overlay | Y | Y | Y | Y | Y | Y |
| 4.3 | App Architecture | Y | Y | Y | Y | Y | Y |
| 4.4 | Environment Architecture | Y | Y | Y | Y | Y | Y |
| 5.1 | KPIs & Benchmarks | Y | Y | Y | Y | Y | Y |
| 5.2 | Reporting & Dashboards | Y | Y | Y | Y | Y | Y |
| 5.3 | MDM & Governance | Y | Y | Y | Y | N | N |
| 6.1 | Security & Controls | Y | Y | Y | Y | Y | Y |
| 6.2 | Policies | Y | Y | Y | Y | Y | Y |

**Legend**: Y = Available, N = Not applicable for this domain

**Notes**:
- Section 5.3 (MDM & Governance) is not applicable to Cyber and Sustainability as these domains do not manage traditional master data entities
- All other sections are fully covered across all six domains

---

## File Counts per Domain

| Domain | Section Files | Intro Files | Total Files |
|--------|:------------:|:-----------:|:-----------:|
| Finance | 18 | 0 | 18 |
| HR | 18 | 0 | 18 |
| Procurement | 18 | 0 | 18 |
| SCM | 18 | 0 | 18 |
| Cyber | 16 | 0 | 16 |
| Sustainability | 16 | 0 | 16 |
| Intro (shared) | 0 | 2 | 2 |
| **Total** | **104** | **2** | **106** |

---

## Estimated Token Counts per Domain

| Domain | Avg Tokens/File | Total Tokens (est.) |
|--------|:--------------:|:------------------:|
| Finance | ~3,000 | ~54,000 |
| HR | ~2,800 | ~50,400 |
| Procurement | ~2,800 | ~50,400 |
| SCM | ~2,800 | ~50,400 |
| Cyber | ~2,500 | ~40,000 |
| Sustainability | ~2,500 | ~40,000 |

---

## File Path Convention

All domain files follow this path pattern:

```
references/domains/{domain}/{section_number}-{section_slug}.md
```

Examples:
- `references/domains/finance/1.1-process-taxonomies.md`
- `references/domains/hr/2.2-role-mapping.md`
- `references/domains/procurement/4.1-ai-augmentation.md`
- `references/domains/scm/5.1-kpis-benchmarks.md`

Shared intro files:
- `references/domains/_intro/0.1-intro-powered.md`
- `references/domains/_intro/0.2-intro-tom.md`

---

## Cross-Domain Reference Loading

When a request spans multiple domains, load in this priority order:

1. **Primary domain**: load all relevant sections for the main domain
2. **Cross-reference sections only**: for secondary domains, load only the sections that differ or are explicitly requested
3. **Shared methodology**: methodology files apply equally to all domains; load once

**Common cross-domain scenarios**:

| Scenario | Primary Domain | Secondary Domains | Key Cross-References |
|----------|---------------|-------------------|---------------------|
| ERP transformation | Finance | Procurement, SCM | 4.2, 4.3 (shared platform) |
| GBS design | Finance | HR, Procurement | 2.1, 2.2, 3.1 (shared org model) |
| Integrated KPIs | Finance | All | 5.1, 5.2 (cross-domain dashboards) |
| Security overlay | Cyber | Finance, HR | 6.1 (controls apply to all) |
| ESG reporting | Sustainability | Finance, SCM | 5.2, 6.2 (reporting & policy) |
