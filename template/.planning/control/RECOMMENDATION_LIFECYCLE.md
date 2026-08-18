# Recommendation lifecycle

Recommendations hold durable hypotheses, opportunities, risks, or direction ideas. They do not contain executable tasks and do not authorize implementation.

## Capture

Create a recommendation only when the idea is durable enough to revisit. Search the index and relevant items for overlap first. Record evidence separately from interpretation and preserve user wording when it matters.

A recommendation may be captured in the legacy/simple form first. Semantic-unit decomposition is required only when the recommendation participates in Project Spine historical reconciliation, conversion/closure requires unit-level coverage, or composite meaning would otherwise be lost.

## Lifecycle statuses

- `Proposed`: recorded for discussion; no direction approved.
- `Accepted`: direction approved; no approved change yet.
- `Converted`: one or more linked changes exist; outcome may still be partial.
- `Deferred`: intentionally postponed by user decision.
- `Rejected`: intentionally declined with rationale.
- `Completed`: intended outcome is fulfilled; any optional/carry-forward residue is explicitly accounted for and no incomplete required linked work remains.

The agent may create `Proposed`, recommend transitions, and set `Converted` as bookkeeping when an approved linked change is created. Acceptance, deferral, rejection, and abandonment require user decisions. `Completed` is set only during authorized closure/reconciliation with full required-outcome coverage.

## Semantic units

A recommendation can be semantically composite. When unit-level reconciliation is needed, preserve its durable meaning as stable IDs:

```text
REC-NNNN/U1
REC-NNNN/U2
...
```

Do not renumber an existing unit merely because wording/order changes. Add a new unit only for genuinely new durable meaning.

Canonical unit reconciliation states:

- `IMPLEMENTED`;
- `STILL_OPEN`;
- `CARRIED_FORWARD`;
- `FUTURE_SEED`;
- `DEFERRED`;
- `REJECTED`;
- `SUPERSEDED`;
- `NEEDS_REFRAME`;
- `UNCERTAIN`.

Canonical primary lineage classes:

- `GAP_ANCHORED`;
- `TARGET_STATE_SIGNAL`;
- `LOCAL_TACTIC`;
- `OPTIONAL_FUTURE`;
- `OUTSIDE_BOUNDED_TARGET`;
- `UNANCHORED`.

Each unit has exactly one state and one primary lineage class. It may reference several Gaps/capabilities/evidence records. `FUTURE_SEED` requires a source-supported trigger or an explicit statement that no trigger is known; do not invent a schedule.

## Reconciliation review and parent state

Keep lifecycle `Status` separate from semantic reconciliation.

`Reconciliation review` is:

- `NOT_RECONCILED`;
- `DRAFT`;
- `CURRENT`.

When `CURRENT`, derive one parent reconciliation state:

- `OPEN`;
- `COMPLETED`;
- `PARTIALLY_REALIZED`;
- `CLOSED_WITH_CARRYFORWARD`;
- `DEFERRED`;
- `SUPERSEDED`;
- `REJECTED`;
- `UNANCHORED`;
- `NEEDS_REFRAME`;
- `UNCERTAIN`.

A parent reconciliation state summarizes the unit ledger; it does not silently change lifecycle `Status`. For example, a lifecycle-`Completed` recommendation may be `CLOSED_WITH_CARRYFORWARD` when its delivered scope is complete but optional future/carry-forward meaning remains explicitly represented.

## Conversion to change

A recommendation may map to several changes, and a change may originate from several recommendations. Update both directions:

- recommendation `Converted changes`;
- change `Source recommendations`;
- exact `Source recommendation units` when unit IDs exist and scope depends on them;
- recommendation item and `INDEX.md` bookkeeping used by the project.

Do not make the whole parent recommendation the scope of a Change when only specific semantic units were selected.

## Coverage at closure

When semantic units exist, reconcile closure at unit level first. A completed Change changes only the referenced units for which its accepted scope supplies evidence. Unreferenced units remain untouched.

For legacy items without semantic units, use `Full`, `Partial`, or `None` until the item is decomposed:

| Coverage and remaining work | Result |
|---|---|
| Full and no incomplete required linked work | eligible for `Completed` after authorized reconciliation |
| Full but other incomplete required linked work remains | `Converted` |
| Partial | `Converted` |
| None | preserve status and explain |

A completed Change does not automatically complete its source recommendation.

## Residue invariant

For any recommendation marked `Reconciliation review: CURRENT`:

```text
all original recommendation semantic units are accounted for
```

No durable unit may disappear because a Change completed, a historical Roadmap item was retired, or a new Target narrowed the bounded project. Preserve it as implemented, open, carried forward, future seed, deferred, rejected, superseded, needing reframe, uncertain, or explicitly outside/unanchored through its lineage classification.

## Historical reconciliation

Use `RECOMMENDATION_HISTORY_RECONCILIATION.md` for broad recommendation + Roadmap reconciliation against the accepted Project Spine. That workflow may draft unit ledgers and parent states, but `CURRENT` reconciliation requires explicit user acceptance. It does not prioritize the Roadmap.

## Integrity

The individual recommendation item is authoritative. The index is a discovery summary. Resolve missing items, duplicate IDs/unit IDs, invalid transitions, item/index disagreements, unaccounted semantic residue, and source-text changes that invalidate a prior unit ledger before using reconciliation as current direction evidence.
