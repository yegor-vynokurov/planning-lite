# Capture or triage recommendations

Mode: Dialogue / Planning.

Follow `.planning/control/RECOMMENDATION_LIFECYCLE.md` as the authoritative workflow. Recommendations are durable hypotheses, not tasks or implementation authority.

A newly captured recommendation may remain simple. If it already contains several independently durable claims, preserve them without forcing unit IDs unless unit-level conversion/reconciliation is needed. Existing `REC-NNNN/Ux` IDs are stable and must not be renumbered.

Do not run broad Project Spine historical reconciliation from this prompt; use `RECOMMENDATION_HISTORY_RECONCILIATION.md`. Do not create or activate a change from this prompt.

<!-- PL_FCP_RECOMMENDATION_TRIAGE_V1:BEGIN -->
## Field Control Pack triage

Before creating or rewriting a Recommendation, classify the input:

```text
observation without proposed action
→ capture as Discovery

new durable proposed action
→ use the existing Recommendation lifecycle

existing Recommendation with material unit-level residue
→ use Recommendation Absorption
```

For Absorption, read:

```text
.planning/control/RECOMMENDATION_ABSORPTION.md
.planning/control/RECOMMENDATION_LIFECYCLE.md
```

Do not silently discard residue, invent semantic ownership, auto-prioritize the
Roadmap, or create an executable Change.
<!-- PL_FCP_RECOMMENDATION_TRIAGE_V1:END -->
