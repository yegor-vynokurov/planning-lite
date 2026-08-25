# Recommendation Absorption
## Rules for accepting unanchored recommendations into Planning Lite

**Status:** `CURRENT DESIGN GOVERNANCE / SELF-HOSTED PILOT RULE`
**Date:** `2026-08-21`
**Stable path:** `docs/design/project-spine/governance/RECOMMENDATION-ABSORPTION.md`

This process is designed for Planning Lite itself and as a future reusable
pattern for consumer projects.

It does not authorize implementation.

---

# 1. Separate input types first

## Discovery

A **Discovery** is an observation/fact/evidence statement.

Examples:

```text
"Readiness stopped after the first blocker."
"Three tasks required historical context reload."
"Current tests are green but contain no meaningful assertion."
```

A Discovery does not imply action.

Store Planning Lite development Discoveries under:

```text
docs/design/project-spine/discoveries/
```

One Discovery may produce:
- no Recommendation;
- one Recommendation;
- several Recommendations.

Never silently rewrite a Discovery into an action proposal.

## Recommendation

A **Recommendation** proposes action, policy, capability, or a durable change in
direction.

New untriaged Planning Lite recommendations go to:

```text
docs/design/project-spine/recommendations/inbox/
```

An unanchored Recommendation is legal.

---

# 2. Preconditions for an absorption pass

Before absorbing recommendations:

```text
[ ] identify the current Roadmap;
[ ] identify current Target/Project Spine authority;
[ ] establish current-state consistency;
[ ] inventory new/unanchored Recommendations;
[ ] identify relevant Future Reserve entries;
[ ] identify superseded predecessors where lineage matters;
[ ] separate Discoveries from Recommendations.
```

Do not use an old Roadmap's order as current priority.

---

# 3. Work unit: RecommendationUnit, not document

A recommendation document is only a container.

Decompose only as far as durable meaning requires:

```text
REC-X/U1
REC-X/U2
...
```

Do not invent units for formatting convenience.

Stable units preserve:
- semantic statement;
- evidence/source;
- current disposition;
- lineage/destination;
- trigger if future.

---

# 4. First challenge: overlap before placement

For every unit ask:

```text
Does this already exist as:
- current Roadmap semantics?
- existing workflow/skill/checklist?
- current invariant?
- Future Reserve item?
- superseding Recommendation?
- already-realized capability?
```

Classify the relation:

```text
DUPLICATE
REFINEMENT
NEW_CAPABILITY
CROSS_CUTTING
FUTURE_OPTION
CONTRADICTION
SUPERSEDED
NO_MATCH
```

Do not create a new Roadmap branch merely because the source file has a new title.

---

# 5. Placement determinacy test

Use the Poker-derived determinacy rule:

> Can this RecommendationUnit be placed in two materially different locations
> or owners while both placements still satisfy the written Roadmap?

If **YES**, ask whether the difference changes:
- authority;
- sequencing;
- evidence;
- lifecycle;
- ownership;
- dependency boundaries.

If material, the absorption is underdetermined.

Resolve ownership/placement before declaring the unit absorbed.

---

# 6. New-vertebra / anti-hair test

A RecommendationUnit gets a new major Roadmap item only when all three are true:

```text
1. distinct dependency boundary;
2. distinct semantic owner;
3. distinct evidence-bearing exit gate.
```

If not, prefer:

```text
ABSORB_EXISTING
CROSS_CUTTING
FUTURE_RESERVE
UNANCHORED
REJECT / SUPERSEDE
```

The Roadmap is a dependency structure, not a catalog of ideas.

---

# 7. Allowed dispositions

Each durable unit must end with one explicit disposition.

```text
ALREADY_REALIZED
ABSORB_EXISTING
ADD_VERTEBRA
CROSS_CUTTING
FUTURE_RESERVE
CONTINGENCY_ROUTE
UNANCHORED
DEFER
REJECT
SUPERSEDE
NEEDS_REFRAME
UNCERTAIN
```

---

# 8. No silent residue

Invariant:

```text
all source RecommendationUnits
=
absorbed
+ already realized
+ future/deferred
+ unanchored
+ rejected
+ superseded
+ explicitly uncertain
```

No unit may disappear because:
- a Change completed;
- a parent Recommendation was marked completed;
- a new Roadmap was written;
- a newer recommendation superseded the old document.

---

# 9. Supersede-residue check

When `B supersedes A`:

```text
A units
→ compare with B
→ compare with current Roadmap
→ compare with Future Reserve
→ recover useful residue
→ explicit disposition
```

Only then archive A.

Rule:

```text
SUPERSEDED
!=
SEMANTICALLY EXHAUSTED
```

---

# 10. Future Reserve vs Contingency Route

## Future Reserve

Use when one RecommendationUnit is useful but not current work.

It requires:
- identity;
- reason not now;
- trigger or explicit unknown trigger;
- source lineage.

It has no scheduling promise.

## Contingency Route

Use when several Future Seeds form a coherent alternate strategy with:
- common premise;
- coupled triggers;
- dependency order;
- rollback/mainline return rule.

A contingency route is **not** a second Roadmap.

Keep one active Roadmap.

---

# 11. Three recommendation operations

## TRIAGE

For rough/unanchored inputs:

```text
deduplicate
cluster
merge/split
challenge
classify
anchor only where justified
preserve unanchored residue
```

## RECONCILE

After a Change or material design pass:

```text
what was realized?
what remains?
what moved to Future Reserve?
which Gap/Target signal changed?
```

## CONVERGE

Periodically:

```text
future trigger became true?
partial recommendation became stale?
accepted recommendation never anchored?
completed recommendation has open residue?
superseded chain has missing residue?
duplicate authority emerged?
```

Do not run full convergence after every tiny edit.

---

# 12. Absorption outputs

A complete absorption pass produces:

```text
1. updated current Roadmap;
2. updated Future Reserve;
3. source/disposition ledger;
4. archived absorbed/superseded source Recommendations;
5. unresolved inbox/active Recommendations, if any;
6. Discovery lineage preserved separately;
7. review receipt.
```

Do not leave the only surviving meaning in chat history.

---

# 13. Acceptance checklist

```text
RECOMMENDATION_ABSORPTION_ACCEPTANCE

COVERAGE
[ ] every source Recommendation/Unit has a disposition

DISCOVERY SEPARATION
[ ] observations were not automatically converted into work

PLACEMENT DETERMINACY
[ ] no material unit has two competing owners/locations

ANTI-HAIR
[ ] no Roadmap item exists only because a Recommendation had a title

CONTRADICTIONS
[ ] incompatible semantics are resolved or explicitly bounded

FUTURE PRESERVATION
[ ] useful non-current residue is in Future Reserve with trigger/lineage

CONTINGENCY
[ ] alternate route, if any, is compact and not a second Roadmap

SUPERSEDE RESIDUE
[ ] superseded predecessors were checked unit-by-unit where material

NO SILENT RESIDUE
[ ] nothing useful disappeared

LINEAGE
[ ] archived sources point to their destination/receipt

AUTHORITY
[ ] the pass did not authorize implementation or silently reprioritize
```

---

# 14. Minimal Recommendation template

```markdown
# REC-PL-XXXX — title

- Status: Proposed
- Anchor: UNANCHORED
- Source discovery/evidence:
- Created:
- Last reviewed:

## Recommendation

## Why it may matter

## Evidence

## Semantic units
| Unit | Statement | Current disposition | Destination / trigger |
|---|---|---|---|
```

---

# 15. Minimal Discovery template

```markdown
# DISC-PL-XXXX — title

- Status: OBSERVED / VALIDATED / SUPERSEDED / ARCHIVED
- Observed:
- Source/evidence:
- Scope:

## Observation

## Evidence

## Interpretation limits

## Linked recommendations
- none
```

A Discovery remains a Discovery even after it spawns a Recommendation.

---

# 16. Safe automation boundary

Current status is manual/checklist-governed.

Future tooling may assist:
- inventory;
- overlap search;
- unit extraction candidates;
- trigger detection;
- orphan checks.

But it must not automatically:
- promote Future Seeds to Roadmap;
- activate contingency routes;
- accept semantic-unit boundaries;
- archive source Recommendations without residue review;
- change Target/priority without authority.
