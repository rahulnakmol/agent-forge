# Feature Ambition Mapping

## Purpose

Feature ambition mapping plots every PRD feature on the 11-star spectrum to produce a visual portfolio view. This reveals clustering patterns, identifies anchor features, and highlights the balance between table-stakes and differentiators.

---

## The Mapping Process

### Step 1: List All Features

Extract every distinct feature, user story, or capability described in the PRD. Include:
- Explicit features (named in the PRD)
- Implicit features (assumed but not detailed, such as authentication, settings, onboarding)
- Non-functional requirements (performance, security, accessibility)

### Step 2: Assign Star Levels

For each feature, assign a star level (1-11) based on the criteria in `references/eleven-star/star-levels-*.md`. Use the following quick-assignment guide:

| If the feature... | Assign |
|-------------------|--------|
| Is missing from the PRD but needed for the user journey | Star 1 |
| Is mentioned but would be painful to use as described | Star 2-3 |
| Meets basic expectations, nothing surprising | Star 4 |
| Matches what the best competitors offer | Star 5 |
| Proactively helps the user without being asked | Star 6 |
| Would make users tell someone about it | Star 7 |
| Changes how users think about the problem | Star 8 |
| Feels magical or impossibly smart | Star 9 |
| Transforms the workflow beyond the feature's scope | Star 10 |
| Makes the problem cease to exist | Star 11 |

### Step 3: Create the Spectrum Map

Lay out features on a horizontal spectrum from 1 to 11:

```
Star:  1    2    3    4    5    6    7    8    9   10   11
       |    |    |    |    |    |    |    |    |    |    |
       |----|----|----|----|----|----|----|----|----|----|
                           [A] [B]  [C]  [D]
                           [E] [F]  [G]
                           [H]
```

Where each letter represents a feature. This visual immediately reveals the distribution.

---

## Clustering Analysis

### Pattern 1: The 5-Star Cluster

```
Star:  1    2    3    4    5    6    7    8    9   10   11
                      [A] [B]
                      [C] [D]
                      [E] [F]
                           [G]
                           [H]
```

**Diagnosis**: Most features cluster at star 4-5. The PRD describes a competent product that matches competitors. No features create differentiation.

**Recommendation**: Identify 1-2 features that should be anchor features. Apply the sweet-spot analysis (Steps 3-4 from `references/eleven-star/sweet-spot-analysis.md`) to push them to star 7-8.

### Pattern 2: The Balanced Portfolio

```
Star:  1    2    3    4    5    6    7    8    9   10   11
                           [A]  [B]  [C]
                           [D]  [E]
                           [F]
                           [G]
```

**Diagnosis**: Healthy distribution. Table-stakes features at star 5, enhanced features at star 6, anchor features at star 7-8. This is the target state.

**Recommendation**: Validate that the star 7-8 features are feasible and that the star 5 features are genuinely polished (not under-specified star 4s).

### Pattern 3: The Ambition Cluster

```
Star:  1    2    3    4    5    6    7    8    9   10   11
                                     [A]  [B]  [C]
                                     [D]  [E]
                                          [F]
```

**Diagnosis**: Most features aim for star 7-9. The PRD is ambitious but may lack grounding. Table-stakes features are under-specified, creating a fragile foundation.

**Recommendation**: Apply the grounding test to star 9+ features. Ensure star 5 table-stakes features are present and well-specified. A beautiful anchor feature on a broken foundation fails.

### Pattern 4: The Bimodal Split

```
Star:  1    2    3    4    5    6    7    8    9   10   11
            [A]       [B] [C]            [D]
            [E]       [F]                [G]
```

**Diagnosis**: Some features are broken (star 2-3) while others are highly ambitious (star 8-9). The PRD is inconsistent -- some sections received deep thought while others were neglected.

**Recommendation**: Priority 1 is bringing star 2-3 features up to star 5. Priority 2 is validating feasibility of star 8-9 features. The inconsistency itself should be flagged.

### Pattern 5: The Flat Line

```
Star:  1    2    3    4    5    6    7    8    9   10   11
                           [A]
                           [B]
                           [C]
                           [D]
                           [E]
                           [F]
```

**Diagnosis**: Every feature is at exactly the same level (usually star 5). No feature stands out. The PRD is uniformly adequate.

**Recommendation**: This is the most common pattern for AI-generated PRDs. The product needs spikes -- 1-2 features elevated to star 7-8 -- to create identity and differentiation.

---

## Identifying Anchor Features

Anchor features are the 1-2 features that define the product's identity. They are what users would describe if asked "What does this product do that's special?"

### Selection Criteria

An anchor feature should:
1. **Solve the core problem** (not a peripheral concern)
2. **Be visible to users** (not a backend optimization)
3. **Create an emotional response** (surprise, delight, relief)
4. **Be describable in one sentence** (if it requires a paragraph to explain, it is too abstract)
5. **Be feasible to deliver at star 7-8** (ambitious but buildable)

### Common Mistakes

- **Too many anchors**: If everything is special, nothing is special. Maximum 2 anchor features.
- **Infrastructure as anchor**: "Scalable microservices architecture" is not an anchor. Users do not experience architecture.
- **Parity as anchor**: "Best-in-class search" is not an anchor if competitors also have good search. It must be genuinely different.
- **Future anchor**: "In v3, we will have..." is not an anchor. The anchor must be in the current scope.

---

## Balancing the Portfolio

The ideal feature portfolio for a PRD:

| Feature Type | Star Level | % of Features | Description |
|-------------|------------|---------------|-------------|
| Table stakes | 5 | 40-50% | Features users expect. Must be polished. Not differentiating. |
| Enhanced | 6 | 20-30% | Features that show intelligence and proactivity. Noticed but not remarkable. |
| Anchor | 7-8 | 15-25% | The product's identity features. What users talk about. |
| Aspirational | 9-11 | 0% | Not features -- design exercises to inspire anchors. |

### Imbalance Flags

| Condition | Flag | Review Action |
|-----------|------|---------------|
| No features above star 5 | **Ambition deficit** | Conduct sweet-spot analysis for top 2 features |
| More than 30% of features above star 7 | **Feasibility risk** | Apply grounding test to each star 7+ feature |
| Any feature below star 4 | **Quality defect** | Flag as P0 improvement, must reach star 5 minimum |
| All features at same star level | **No identity** | Select anchor features and elevate |
| Anchor features not in Activation/Retention stage | **Misplaced ambition** | Ambition should be where users experience core value |

---

## Documenting the Mapping

Include the following in the review report:

1. **Feature list with star assignments**: Table showing each feature, its star level, and a one-line justification
2. **Spectrum visualization**: The horizontal distribution map
3. **Cluster assessment**: Which pattern does this PRD match?
4. **Anchor identification**: Which features should be anchors? Are they at star 7-8?
5. **Portfolio balance assessment**: Is the distribution healthy or imbalanced?
6. **Specific elevation opportunities**: For anchor features below star 7, what would the star 7-8 version look like?
