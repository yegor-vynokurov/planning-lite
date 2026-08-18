# Project Spine / Direction Workflows design track

**Status:** tracked design source for the next Planning Lite direction work
**Implementation status:** PL-V38-01 and PL-V38-02 implemented in the template; not released
**Current alignment:** v3.8.4

This directory preserves the Project Spine design work derived from the Poker field pilot and aligns it with the actual Planning Lite architecture and existing research assets.

The earlier generated v3.8.1 package was never applied. v3.8.2 was the tracked design/research-asset alignment; v3.8.4 is the current roadmap after PL-V38-02.

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
→ v3.8.4 + Poker Field Pilot 2 gate
```

## Files

- `REC-PL-DIRECTION-001-v2.md` — consolidated Project Spine recommendation.
- `PL-V38-CURRENT.md` — compact operational handoff; read first after a context reset.
- `PLANNING-LITE-ROADMAP-v3.8.4.ru.md` — current implementation-facing roadmap.
- `DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md` — normalized workflow semantics aligned to `template/.planning/control` and research-asset reuse boundaries.
- `POKER-PILOT-OPERATOR-COMMANDS-v1.md` — normalized operator commands from the field pilot; source/design evidence, not verbatim runtime mega-prompts.
- `PL-V38-IMPLEMENTATION-PLAN-v3.8.4.md` — bounded implementation sequence.
- `RESEARCH-ASSET-OWNERSHIP-v1.md` — explicit roles for central product, Lab, Context Pilot/Eval Harness, Poker and Campaign Core.
- `PL-V38-ALIGNMENT-REVIEW-v3.8.2.md` — anti-drift review.

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
