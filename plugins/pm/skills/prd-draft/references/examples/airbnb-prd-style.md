# Airbnb-Style PRD Example

## About This Style

Airbnb PRDs are experience-focused, narrative-driven, and customer-centric. They approach requirements through journey-based thinking, emphasizing how the user feels at every touchpoint. The 11-star experience framework pushes teams to imagine far beyond functional requirements toward transformative experiences.

Key characteristics:
- Narrative framing: the user's story, not the system's behavior
- 11-star experience thinking: what would a magical version look like?
- Journey maps as the backbone of requirements
- Emotional design: how the user feels matters as much as what they do
- Community and trust as foundational design principles

---

## The 11-Star Experience Framework

Before writing stories, map the feature across the star spectrum to calibrate ambition:

| Stars | Experience Level | Example (Guest Booking) |
|-------|-----------------|------------------------|
| 1 | Broken | Guest searches but gets no relevant results |
| 2 | Frustrating | Results exist but are slow, poorly filtered, hard to compare |
| 3 | Functional | Guest finds listings, can filter by dates and price, books successfully |
| 4 | Good | Results are relevant, photos are clear, booking is smooth |
| 5 | Great | Personalized results, instant booking, transparent pricing |
| 6 | Delightful | Trip recommendations, neighborhood guides, host intro video |
| 7 | Memorable | Curated itinerary based on interests, local experience suggestions |
| 8 | Remarkable | Host sends personalized welcome guide, pre-stocked fridge with favorites |
| 9 | Shareable | Experience so good the guest tells 5 friends unprompted |
| 10 | Legendary | Elon Musk personally drives you to the listing in a Tesla |
| 11 | Impossible | You teleport to the destination; listing is your dream home |

**PRD calibration**: Most features target 5-7 stars. The 8-11 range is aspirational thinking that informs the direction. The Features table Star Level column captures where each feature lands.

---

## Example: Guest Trip Planning Experience

```markdown
# Guest Trip Planning Experience -- PRD

**Author**: Maya Rodriguez, PM -- Guest Experience
**Date**: 2026-03-10
**Status**: Draft
**Experience Target**: 7-star (Memorable)

---

## The Story

### Today (3-Star Experience)

Priya is planning a week in Lisbon with her partner. She opens Airbnb, types "Lisbon",
picks dates, and scrolls through 2,400 listings. She opens 30 tabs. She cross-references
Google Maps for neighborhood safety. She reads 200 reviews across 8 listings. She texts
screenshots to her partner. They go back and forth for 3 days. She books a place that
turns out to be 40 minutes from everything they wanted to do.

Priya spent 6 hours planning and still got it wrong. The product failed her.

### Tomorrow (7-Star Experience)

Priya opens Airbnb and says "Week in Lisbon, walkable to restaurants and history,
quiet at night, under $150/night." Airbnb shows her 5 curated listings, each with a
one-paragraph story about why it matches her preferences. She taps "Compare" and sees
a side-by-side of neighborhood vibe, walkability score, guest satisfaction for couples,
and host responsiveness. She picks one in 15 minutes. Before she arrives, she receives
a personalized Lisbon guide based on the interests in her profile -- food tours, fado
houses, and tile workshops. Her host sends a voice note welcoming her.

Priya spent 15 minutes planning and the trip exceeded her expectations.

---

## Who Is This For?

### Persona: The Intentional Traveler (Priya)

**Who she is**: 32, UX designer, travels 3-4 times per year with her partner. Values
experiences over luxury. Researches extensively before committing. Trusts peer reviews
more than marketing. Uses Airbnb because hotels feel generic.

**How she feels today**: Overwhelmed by choice. Anxious about picking the wrong
neighborhood. Distrustful of listing photos (they all look the same). Frustrated that
her past trips do not inform future recommendations.

**What success feels like**: Confident in her choice within 20 minutes. Excited about
the trip before she arrives. Surprised by a recommendation she would not have found herself.

**Journey moments that matter**:
1. First search -- does Airbnb understand what she actually wants?
2. Comparison -- can she decide without 30 browser tabs?
3. Booking -- does she feel confident, not just hopeful?
4. Pre-trip -- does anticipation build, or does anxiety creep in?
5. Arrival -- does reality match expectations?

### Persona: The Spontaneous Explorer (Marco)

**Who he is**: 26, remote software engineer, travels monthly for 1-2 week stays. Books
within 48 hours of deciding to go. Prioritizes wifi speed and workspace over aesthetics.
Repeat Airbnb user (40+ stays).

**How he feels today**: Efficient but unimpressed. He knows how to filter and book fast.
But Airbnb never surprises him -- it is a utility, not an experience.

**What success feels like**: Airbnb suggests a destination he had not considered. The
listing has verified fast wifi and a desk photo. He books in 5 minutes and discovers a
neighborhood he loves.

---

## Epic Definition

As a guest planning a trip,
I want Airbnb to understand my travel style and surface the right listings with context,
So that I can book confidently in minutes instead of hours.

### In Scope
- Intent-based search (natural language trip description)
- Curated listing results (5-10 instead of 2,400)
- Neighborhood context cards (vibe, walkability, safety, highlights)
- Side-by-side comparison (up to 3 listings)
- Pre-trip personalized guide (based on profile + destination)

### Out of Scope
- Price negotiation or dynamic pricing changes
- Host matching algorithm (separate initiative)
- In-trip concierge features (post-booking, different epic)
- Group trip coordination (multi-guest planning)

---

## User Stories

### TP-001: Intent-Based Search (Must Have, M)

As Priya,
I want to describe my ideal trip in my own words,
So that Airbnb shows me listings that match my intent, not just my filters.

Given I type "Week in Lisbon, walkable, quiet, couples, under $150" in the search bar
When I submit the search
Then I see 5-10 listings ranked by match to my described intent
  And each listing shows a match summary ("Walkable: 9/10, Quiet neighborhood,
    couples love this place")
  And traditional filters are still available to refine further

Given I type a vague query like "somewhere warm next month"
When I submit the search
Then the system asks one clarifying question (e.g., "Beach or city?")
  And after my answer, shows curated results

### TP-002: Neighborhood Context Cards (Must Have, M)

As Priya,
I want to understand the neighborhood before I read a single review,
So that I do not book a place that is technically nice but practically wrong.

Given I am viewing search results
When I tap a listing
Then I see a neighborhood card showing: vibe tags (e.g., "Lively evenings, quiet mornings"),
  walkability score, transit proximity, top 3 guest-recommended spots nearby, safety rating
  And the data comes from aggregated guest reviews and local data, not the host

### TP-003: Smart Comparison (Should Have, M)

As Priya,
I want to compare my top 3 listings side by side,
So that I can decide without switching between tabs and losing context.

Given I have saved 3+ listings to my trip wishlist
When I tap "Compare"
Then I see a comparison table with: price/night, neighborhood vibe, guest rating,
  host response time, walkability score, key amenities, and "Best for you because..." summary
  And I can book directly from the comparison view

### TP-004: Pre-Trip Personalized Guide (Should Have, L)

As Priya,
I want a personalized guide for my destination before I arrive,
So that anticipation builds and I discover things I would not find on my own.

Given I have a confirmed booking for Lisbon arriving in 7 days
When I open the Airbnb app
Then I see a "Your Lisbon Guide" section with: curated experiences matching my profile interests,
  neighborhood walking routes near my listing, local restaurant recommendations from guests
  with similar taste profiles, and a welcome note from my host

### TP-005: Rapid Booking for Repeat Travelers (Could Have, S)

As Marco,
I want Airbnb to remember my workspace requirements and suggest listings that match,
So that I can book my monthly work trip in under 5 minutes.

Given I have booked 10+ work trips with wifi speed and desk as recurring preferences
When I search for a new destination
Then "Remote work ready" listings are boosted in results
  And each shows verified wifi speed and workspace photo
  And I see "Based on your work trip history" as the recommendation reason

---

## Features & Star Rating

| # | Feature | Stories | Star Level | Business Value |
|---|---------|---------|-----------|---------------|
| 1 | Intent-based search | TP-001 | 7 | Reduces search-to-book from 6 hours to 20 minutes; 40% conversion lift |
| 2 | Neighborhood context | TP-002 | 6 | Reduces post-booking regret; 15% improvement in "location" review scores |
| 3 | Smart comparison | TP-003 | 6 | Eliminates tab-switching friction; 25% faster decision-making |
| 4 | Pre-trip guide | TP-004 | 8 | Builds anticipation; 20% increase in Experience booking attachment rate |
| 5 | Repeat traveler boost | TP-005 | 5 | Reduces booking friction for power users; 10% increase in monthly booking frequency |

---

## Success Metrics

| Metric | Baseline | Target | Method | Frequency |
|--------|----------|--------|--------|-----------|
| Search-to-book time | 6.2 hours | 1.5 hours | Funnel analytics | Weekly |
| Guest "location" review score | 4.1/5 | 4.5/5 | Post-stay review | Monthly |
| Booking conversion rate | 2.8% | 4.0% | Funnel analytics | Weekly |
| Pre-trip guide engagement | N/A | 60% open rate | In-app analytics | Weekly |
| NPS (trip planning) | 38 | 55 | In-app survey | Monthly |

---

## Open Questions

| Question | Owner | Due |
|----------|-------|-----|
| Can we use guest review text for neighborhood vibe tagging at scale? | Data Science | 2026-03-20 |
| Legal review on aggregated safety ratings from third-party data | Legal | 2026-03-25 |
| Host opt-in required for voice welcome notes? | Trust & Safety | 2026-03-22 |
```

---

## Style Principles to Apply

When generating Airbnb-style PRDs, follow these principles:

1. **Lead with narrative**: Start with a story about a real person, not a feature list
2. **Name your personas**: Give them lives, feelings, and travel histories -- not just job titles
3. **Journey moments matter**: Identify the 3-5 moments where the experience is won or lost
4. **11-star calibration**: Rate every feature on the star scale; aim for 6-8 in shipped product
5. **Neighborhood over listing**: Context matters more than the thing itself -- apply this to any domain
6. **Emotional metrics**: Track how users feel (NPS, satisfaction), not just what they do (conversion)
7. **Less is more in results**: Curation (5-10 good options) beats exhaustive lists (2,400 options)
8. **Anticipation is a feature**: The experience starts before the user begins the core action

---

*pm-prd-generator v1.0 | Airbnb-Style PRD Example*
