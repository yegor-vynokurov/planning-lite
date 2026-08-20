# Project Spine / Direction Workflows design track

**Status:** tracked design source for the next Planning Lite direction work
**Implementation status:** PL-V38-01 through PL-V38-04 plus PL-V38-PREP-01 (`c7a8cce`) implemented and locally verified; repaired Poker migration/materialization passed; Attempt 001 completed as a valid Branch-B reconciliation detour with no Change/production mutation; owner-aware Attempt-002 readiness is next; not released
**Current alignment:** v3.8.7

This directory preserves the Project Spine design work derived from the Poker field pilot and aligns it with the actual Planning Lite architecture and existing research assets.

The earlier generated v3.8.1 package was never applied. v3.8.2 was the tracked design/research-asset alignment; v3.8.7 is the current roadmap after PL-V38-PREP-01 and points next to a repaired non-scored migration preview, then Poker Field Pilot 2.

## Current lineage

```text
Planning Lite roadmap v3.6.2
→ v3.7 Direction Memory addendum
→ REC-PL-DIRECTION-001 v2
→ Poker Project Spine field pilot
→ v3.8 promotion
→ W0 architecture inspection
→ PL-V38-00 central reconciliation
→ v3.8.2 implementation + research-asset reuse alignment
→ PL-V38-01 Direction Foundation
→ PL-V38-02 Current Capability Assessment + causal Gap Map
→ PL-V38-03 recommendation/history reconciliation
→ PL-V38-04 Roadmap synthesis + Change handoff
→ PL-V38-PREP-01 local-only consumer update safety
→ v3.8.7 / repaired migration + PILOT_READY PASS → Attempt 001 Branch-B reconciliation PASS → REC-PL-DIRECTION-002 v1 → Attempt 002
```

## Files

- `REC-PL-DIRECTION-001-v2.md` — consolidated Project Spine recommendation.
- `REC-PL-DIRECTION-002-v1.md` — field-derived authority-owned consistency, readiness, and bounded-handoff recommendation.
- `PL-V38-CURRENT.md` — compact operational handoff; read first after a context reset.
- `PLANNING-LITE-ROADMAP-v3.8.7.ru.md` — current implementation-facing roadmap.
- `DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md` — normalized workflow semantics aligned to `template/.planning/control` and research-asset reuse boundaries.
- `POKER-PILOT-OPERATOR-COMMANDS-v1.md` — normalized operator commands from the field pilot; source/design evidence, not verbatim runtime mega-prompts.
- `PL-V38-IMPLEMENTATION-PLAN-v3.8.7.md` — bounded implementation sequence.
- `RESEARCH-ASSET-OWNERSHIP-v1.md` — explicit roles for central product, Lab, Context Pilot/Eval Harness, Poker and Campaign Core.
- `PL-V38-ALIGNMENT-REVIEW-v3.8.2.md` — anti-drift review.
- `PL-V38-PREP-01-LOCAL-ONLY-UPDATE-SAFETY.md` — corrective local-only updater contract.
- `PILOT-PL-DIRECTION-002-PREP-FINDING-001.md` — field-preparation defect record.
- `PL-V38-PREP-01-POKER-REPLAY.md` — offline replay against the actual post-CHG-0008 Poker snapshot.

## Important boundary

```text
design tracked in central repo
!=
behavior released in Planning Lite
```

Likewise:

```text
research asset referenced by roadmap
!=
consumer runtime dependency
```
