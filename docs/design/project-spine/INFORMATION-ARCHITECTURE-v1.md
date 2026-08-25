# Planning Lite development information architecture v1

**Status:** `CURRENT DESIGN ORGANIZATION`
**Date:** `2026-08-21`

This change reorganizes Planning Lite's own development/design documents only.

It does **not**:
- change the installed consumer `.planning/` schema;
- change runtime behavior;
- change the Planning Lite software release version;
- authorize PL-V39 implementation.

## Stable locations

| Meaning | Stable location |
|---|---|
| Start / current navigation | `CURRENT.md` |
| Current development Roadmap | `roadmap/ROADMAP.md` |
| Old Roadmaps | `roadmap/archive/` |
| New untriaged Recommendations | `recommendations/inbox/` |
| Accepted/unabsorbed Recommendations | `recommendations/active/` |
| Deferred/future residue | `recommendations/FUTURE-RESERVE.md` |
| Absorbed/superseded Recommendation sources | `recommendations/archive/` |
| Discoveries / observations | `discoveries/` |
| Recommendation absorption rules | `governance/RECOMMENDATION-ABSORPTION.md` |
| Evidence/playbooks/reviews/code seeds | `support/` |

## Key semantic distinctions

```text
Discovery
= observed fact/evidence

Recommendation
= proposed action/direction

Roadmap
= accepted dependency/priority structure

Future Reserve
= useful deferred residue, no scheduling promise

Contingency Route
= compact alternate strategy, not a second Roadmap

Support
= evidence/reusable material, not direction authority
```

## Migration map

```text
docs/design/project-spine/PLANNING-LITE-ROADMAP-v3.8.7.ru.md
→ roadmap/archive/PLANNING-LITE-ROADMAP-v3.8.7.ru.md

versioned recommendation source documents
→ recommendations/archive/absorbed/ or archive/superseded/

root REC-PL-DIRECTION-001 predecessor
→ recommendations/archive/superseded/

code seeds
→ support/code-seeds/

playbooks/operator sources
→ support/playbooks/

field pilot findings/replays
→ support/field-evidence/

alignment/absorption reviews
→ support/reviews/

research asset ownership
→ support/research/
```

`PL-V38-CURRENT.md` intentionally remains at its legacy path for current field
compatibility and maintainer tests. A stable navigation wrapper now exists as
`CURRENT.md`.

## Lab cleanup

The old:

```text
.planning-lab/recommendations/active/
```

contained historical roadmap/recommendation packages rather than truly active
current recommendations.

It was moved to:

```text
.planning-lab/archive/legacy-recommendation-package-2026-08-21/
```

The Lab is explicitly non-canonical for current Planning Lite development
direction.

## Why no product-version bump

This is a documentation/design information-architecture normalization.

The software package remains on its existing `v4.3.0` lineage until a governed
product Change explicitly modifies released behavior.

<!-- PL_PROJECT_SPINE_AUTHORITY_PRECEDENCE_V1:BEGIN -->
## Authority precedence

When current-looking sources disagree, use this precedence:

1. **live Git checkout identity** establishes which repository/version is being inspected;
2. `docs/design/project-spine/CURRENT.md` is the sole current resume/navigation authority;
3. `docs/design/project-spine/roadmap/ROADMAP.md` is the current direction/sequencing authority;
4. a tracked active Change or transition receipt explicitly referenced by `CURRENT.md` has bounded Change-specific authority;
5. `checkpoints/**` and `support/**` provide evidence and historical rationale;
6. `roadmap/archive/**` and `recommendations/archive/**` are historical lineage;
7. `.planning-lab/**` is explicitly non-canonical research/experimental state.

Lower layers **must not silently override** a higher authority. A higher layer
may explicitly delegate a bounded decision to a referenced receipt. Missing
referenced authority fails closed; do not fall back to a similarly named file.

Dynamic Git facts are derived live and are not duplicated as mutable semantic
state in `CURRENT.md`.
<!-- PL_PROJECT_SPINE_AUTHORITY_PRECEDENCE_V1:END -->
