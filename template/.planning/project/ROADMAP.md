# Roadmap

- Status: `DRAFT / CURRENT_BASELINE`
- Baseline date:
- Accepted by:
- Acceptance evidence:
- Current preferred outcome: `None`

`CURRENT_BASELINE` requires explicit user acceptance of the current direction proposal.

Roadmap outcomes are durable project results, not implementation tasks. A Roadmap outcome may address several Gaps while every Gap keeps an independent identity and closure check. Roadmap items are not implementation authorization.

## Now

### RM-NNNN — Outcome title

- State: `OPEN / COMPLETED / DEFERRED / RETIRED / UNCERTAIN`
- Target capabilities: `[]`
- Direct Gap refs: `[]`
- Dependent Gap refs: `[]`
- Recommendation-unit / accepted-direction lineage: `[]`
- Outcome:
- Exit condition:
- Logical dependencies / gates:
- Explicit exclusions:
- Likely delivery shape: `ONE_CHANGE / MULTI_CHANGE / PROTOCOL_FIRST / UNKNOWN`
- Governed Changes: `[]`

## Next

Use only when evidence supports a real successor relation. Do not fill this section merely to create a total order.

## Later

Required outcomes without a justified total order belong here.

## Final gate

Review/acceptance outcomes that logically depend on preceding required outcomes belong here. A final gate must not absorb implementation work.

## Deferred or retired

Preserve explicitly deferred or retired current-direction outcomes here when they still need durable visibility. Optional future seeds remain in their owning recommendation/direction records unless explicitly promoted by authority.

## Invariants

```text
historical Roadmap order != current priority
RoadmapOutcome != Gap != Change
Change completion != RoadmapOutcome completion
RoadmapOutcome completion != automatic Gap closure
Gap closure != automatic RoadmapOutcome completion
```
