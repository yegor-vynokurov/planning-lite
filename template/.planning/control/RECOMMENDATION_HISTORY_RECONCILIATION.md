# Recommendation + historical Roadmap reconciliation

**Workflow ID:** `PW-DIR-006`
**Mode:** Planning

Use after an accepted Target, current Capability Model, current capability assessment, and accepted/current Gap Map exist. This is the first Project Spine stage where broad recommendation and historical Roadmap reads are intentionally allowed.

This workflow reconciles meaning and lineage. It does **not** prioritize Gaps, synthesize the next Roadmap, select a Change, or authorize implementation.

## Preconditions

Formal reconciliation requires all of the following:

- `project/TARGET_STATE.md` status = `ACCEPTED`;
- `project/CAPABILITY_MODEL.md` status = `CURRENT_BASELINE`;
- `assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md` status = `CURRENT`;
- `project/GAP_MAP.md` status = `CURRENT_BASELINE`;
- no unresolved material Current-State consistency failure.

If a prerequisite is stale or missing, stop and route to the owning earlier workflow. Do not compensate by treating recommendation or Roadmap wording as Target/Current truth.

## Context profile

Start from the accepted Project Spine artifacts, recommendation index/items, and current Roadmap. Then intentionally expand only the historical recommendation/Roadmap/Change evidence needed to account for semantic units and resolve lineage.

Broad history is justified here because historical reconciliation is the task. Even here:

- do not reopen completed Change packets when recommendation/item evidence is already sufficient;
- use exact completed Change evidence when a unit's implemented/remaining meaning depends on scope or closure;
- do not rescan unrelated repository code merely because history is open;
- record missing evidence as `UNCERTAIN` instead of inventing completion.

## Recommendation semantic units

A recommendation may contain several independently meaningful claims, obligations, constraints, future ideas, or dependencies. Decompose that durable meaning into stable unit IDs:

```text
REC-NNNN/U1
REC-NNNN/U2
...
```

Preserve existing unit IDs when the meaning is unchanged. Never renumber merely for presentation.

Each semantic unit has exactly one reconciliation state:

- `IMPLEMENTED`: the unit's intended outcome is evidenced as satisfied;
- `STILL_OPEN`: the unit remains a current bounded-Target obligation;
- `CARRIED_FORWARD`: the unit remains relevant but its current owner is another durable artifact such as a Gap, accepted direction, or explicit gate;
- `FUTURE_SEED`: optional future meaning preserved with a real trigger; it is not current priority;
- `DEFERRED`: intentionally postponed by explicit authority;
- `REJECTED`: intentionally declined by explicit authority;
- `SUPERSEDED`: replaced by a newer authoritative meaning while lineage is retained;
- `NEEDS_REFRAME`: useful source intent survives, but the historical wording conflicts with or overstates current Target semantics;
- `UNCERTAIN`: available evidence cannot support a stronger state.

Each unit also gets one primary lineage classification:

- `GAP_ANCHORED`;
- `TARGET_STATE_SIGNAL`;
- `LOCAL_TACTIC`;
- `OPTIONAL_FUTURE`;
- `OUTSIDE_BOUNDED_TARGET`;
- `UNANCHORED`.

A unit may reference several Gaps/capabilities/evidence records, but it must have one primary lineage class and one unit state.

### Residue invariant

```text
all original recommendation semantic units are accounted for
```

"Accounted for" means every durable piece of recommendation meaning is represented by a stable unit, state, lineage, evidence or uncertainty, and destination/trigger where applicable. A completed Change is evidence only for its approved scope.

Hard guards:

```text
Change completion != Recommendation completion
Converted != Completed
no evidence != rejected
future seed != current Gap
CARRIED_FORWARD != implemented
historical wording != current Target authority
```

## Parent reconciliation state

Keep the existing recommendation lifecycle `Status` separate from reconciliation state. Derive one parent reconciliation state from the accepted unit ledger:

- `OPEN`: current required meaning remains open and no stronger state below applies;
- `COMPLETED`: intended current outcome is fully realized and no residue needs carry-forward;
- `PARTIALLY_REALIZED`: some intended current outcome is implemented and some remains open;
- `CLOSED_WITH_CARRYFORWARD`: the recommendation's bounded delivered scope may be complete, while explicit residue/future seeds remain represented elsewhere;
- `DEFERRED`;
- `SUPERSEDED`;
- `REJECTED`;
- `UNANCHORED`;
- `NEEDS_REFRAME`;
- `UNCERTAIN`.

Parent reconciliation state does not silently change lifecycle `Status`. User-authorized lifecycle transitions still follow `RECOMMENDATION_LIFECYCLE.md`.

## Historical Roadmap reconciliation

Reconcile historical/current Roadmap statements against the accepted Project Spine without changing Roadmap priority or rewriting the canonical Roadmap in this workflow.

For each meaningful historical Roadmap item, record a source locator/local analysis ID and exactly one disposition:

- `KEEP`;
- `REFRAME`;
- `SPLIT`;
- `MERGE_CANDIDATE`;
- `DEFER`;
- `COMPLETE`;
- `RETIRE_FROM_BOUNDED_TARGET`;
- `UNCERTAIN`.

Record Target/Gap relation, recommendation-unit/Change lineage, rationale, and any surviving meaning. Local analysis IDs do not create canonical Roadmap identities.

Historical Roadmap order is prior intent, **not inherited current priority**.

## Orphan and residue audit

Check at least:

- apparently completed/converted recommendations with unresolved semantic units;
- semantic units with no current destination or explicit `UNANCHORED` classification;
- current Gaps with no direct recommendation lineage;
- current Gaps with no meaningful historical Roadmap coverage;
- historical Roadmap items with no current Target support;
- overlapping/duplicate semantic units;
- optional future ideas accidentally treated as required Gaps;
- residue that disappeared because a linked Change completed;
- source text that changed after a previously accepted unit ledger.

An orphan finding is not automatically an error and does not create work. It is input to PL-V38-04.

## Durable outputs

Use `.planning/assessments/DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md` to write:

```text
.planning/assessments/current/DIRECTION_HISTORY_RECONCILIATION.md
```

During analysis:

- assessment status = `DRAFT`;
- recommendation `Reconciliation review` = `DRAFT` for items being updated;
- lifecycle `Status` remains unchanged unless separately authorized.

Stop for explicit user acceptance of the semantic decomposition/reconciliation. On a later authorized turn:

- mark accepted item ledgers `Reconciliation review: CURRENT`;
- set the assessment status to `CURRENT`;
- synchronize the recommendation index bookkeeping that the project uses;
- preserve all unit IDs and source wording/lineage;
- do not edit the canonical Roadmap yet.

## Readiness verdict

The assessment ends with exactly one:

- `READY_FOR_ROADMAP_SYNTHESIS`: all material recommendation meaning is accounted for and uncertainty is explicitly bounded;
- `BLOCKED`: residue accounting, source authority, or Project Spine prerequisites are materially incomplete.

`READY_FOR_ROADMAP_SYNTHESIS` does not select or prioritize a Roadmap outcome.

## Stop boundary

Stop after the `DRAFT` reconciliation assessment, or after an explicitly authorized acceptance update. Do not continue into PL-V38-04 in the same turn. Do not rank Gaps, synthesize a Roadmap, create a Change, or edit production code.
