# Direction history reconciliation

- Status: `DRAFT / CURRENT`
- Date:
- Repository revision:
- Target baseline:
- Capability baseline:
- Current capability assessment:
- Gap Map baseline:
- Recommendation sources reviewed:
- Roadmap/history sources reviewed:
- Evidence limits:
- Acceptance evidence:

## Recommendation parent summary

| Recommendation | Lifecycle status | Reconciliation review | Parent reconciliation state | Current Gap/Target relation | Notes |
|---|---|---|---|---|---|

## Semantic-unit accounting

| Unit | Source recommendation | Statement | Unit state | Primary lineage | Gap(s) / Target signal | Capability(s) | Evidence | Trigger / destination |
|---|---|---|---|---|---|---|---|---|

Allowed unit states:
`IMPLEMENTED`, `STILL_OPEN`, `CARRIED_FORWARD`, `FUTURE_SEED`, `DEFERRED`, `REJECTED`, `SUPERSEDED`, `NEEDS_REFRAME`, `UNCERTAIN`.

Allowed primary lineage classes:
`GAP_ANCHORED`, `TARGET_STATE_SIGNAL`, `LOCAL_TACTIC`, `OPTIONAL_FUTURE`, `OUTSIDE_BOUNDED_TARGET`, `UNANCHORED`.

## Residue invariant audit

```text
all original recommendation semantic units are accounted for
```

- Result: `PASS / FAIL`
- Apparently closed/converted recommendations audited:
- Missing or ambiguous units:
- Residue loss findings:

## Future-seed register

| Unit | Idea | Supported trigger | Current bounded-Target status |
|---|---|---|---|

A future seed has no implementation date or priority unless separate authority creates one.

## Historical Roadmap reconciliation

| Source / local ID | Original intended outcome | Target/Gap relation | Recommendation-unit / Change lineage | Disposition | Rationale / surviving meaning |
|---|---|---|---|---|---|

Allowed dispositions:
`KEEP`, `REFRAME`, `SPLIT`, `MERGE_CANDIDATE`, `DEFER`, `COMPLETE`, `RETIRE_FROM_BOUNDED_TARGET`, `UNCERTAIN`.

Historical order is not current priority.

## Orphan and overlap audit

### Current Gaps without direct recommendation lineage

### Current Gaps without meaningful historical Roadmap coverage

### Recommendation units without a current anchor

### Historical Roadmap items without current Target support

### Duplicate / overlapping semantic units

### Apparently completed recommendations with unresolved residue

## Source changes since prior reconciliation

## Reconciliation readiness

- Verdict: `READY_FOR_ROADMAP_SYNTHESIS / BLOCKED`
- Blockers or bounded uncertainties:

## Context trace

### Recommendation / Roadmap records opened

### Completed-Change evidence opened

### Reads later judged unnecessary

### Missing-context recovery

## Next permitted action

If `CURRENT` and `READY_FOR_ROADMAP_SYNTHESIS`, proceed in a later turn to the Roadmap synthesis/prioritization workflow. Otherwise repair only the stated reconciliation blockers.
