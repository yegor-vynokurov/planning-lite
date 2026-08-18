# Direction inventory and current-state consistency

- Workflow ID: `PW-DIR-001`
- Workflow version: `1.0.0`
- Source lineage: `REC-PL-DIRECTION-001-v2` / Poker Project Spine pilot
- Mode: Audit

Use when project direction may be stale, fragmented, inherited from historical planning, or unknown. Run before Target-State exploration unless a current direction inventory with a passing consistency gate already exists.

This workflow is read-only for production code and does not authorize a Target, Roadmap, recommendation, or Change.

## Allowed write scope

May update only:

- `.planning/assessments/current/direction-inventory.md`;
- `.planning/ACTIVE.md` when the audit itself changes the next permitted planning action or records a blocker.

`CURRENT_STATE.md`, Roadmap, Changes, recommendations, and project direction files are read-only in this workflow. If stale facts require repair, stop and route to `PROJECT_STATE_REFRESH.md` as a separate operation.

## Required starting reads

Start with:

1. `.planning/ACTIVE.md`;
2. `.planning/project/CURRENT_STATE.md`;
3. `.planning/project/PROJECT_CHARTER.md`;
4. `.planning/project/PROJECT_COMPLETION_CRITERIA.md`;
5. `.planning/project/ROADMAP.md`;
6. `.planning/project/PROJECT_INSTRUCTIONS.md` and `PROJECT_RULES.md` only where they carry direction authority;
7. `.planning/project/REPOSITORY_MAP.md` before broad repository inspection;
8. bounded Git identity/status and the active/completed Change indexes needed to verify lifecycle claims.

Do not load all recommendations, completed Changes, decisions, or archived assessments by default. Expand history only to resolve a concrete authority, freshness, or lifecycle conflict.

## Direction-source classification

For every material source or claim used in the inventory, distinguish:

- `EXPLICIT_USER_DECISION`: a current direct user decision;
- `CURRENT_PROJECT_DIRECTION`: a current durable charter, accepted Target, completion criterion, decision, or Roadmap claim;
- `REPOSITORY_EVIDENCE`: current code, tests, configuration, data, documentation, or Git evidence about what exists now;
- `HISTORICAL_DIRECTION`: superseded or stale planning that may explain lineage but does not automatically govern current direction;
- `INFERRED`: agent synthesis not yet accepted as project direction;
- `UNRESOLVED`: authority or meaning cannot be established safely.

Freshness and authority are separate. A recently edited historical file does not become authoritative merely because its timestamp is newer.

## Current-State Consistency Gate

Before Target exploration, compare at minimum:

```text
Git / repository boundary
+
ACTIVE
+
CURRENT_STATE
+
active/completed Change lifecycle
+
current Roadmap claims
```

Return exactly one gate state:

- `PASS`: no material contradiction blocks direction work;
- `FAIL`: at least one material contradiction must be reconciled first;
- `UNCERTAIN`: required evidence is unavailable or ambiguous.

`git clean` is not sufficient evidence for `PASS`.

### Hard checks

- `CHK-DIR-CONSISTENCY-001`: active Change identity and lifecycle state agree across `ACTIVE`, current Change records, and `CURRENT_STATE`.
- `CHK-DIR-CONSISTENCY-002`: Git/repository revision claims in durable state do not materially contradict observed repository evidence.
- `CHK-DIR-CONSISTENCY-003`: current Roadmap does not claim completion or active work that conflicts with authoritative lifecycle evidence.
- `CHK-DIR-CONSISTENCY-004`: known stale or historical direction is not silently treated as current authority.

On `FAIL` or material `UNCERTAIN`, stop before Target exploration. Report the exact conflict and route to a bounded reconciliation or project-state refresh. Do not repair the conflict implicitly.

## Procedure

1. Confirm repository root, Git boundary, and planning lifecycle boundary.
2. Identify current direction-bearing sources and classify their authority/freshness.
3. Separate current direction, repository facts, historical context, inference, and unresolved questions.
4. Run the Current-State Consistency Gate.
5. Identify the strongest known deliverable-class evidence without deciding a missing deliverable class in Audit mode.
6. Record only direction questions that materially affect Target exploration.
7. Write or refresh `.planning/assessments/current/direction-inventory.md`.
8. If the gate passes, set the next permitted planning action to Target-State exploration when appropriate. If it fails, record the blocker instead.

## Assessment output contract

The current direction inventory should contain:

```text
Repository boundary
Evidence scope and limits
Current authoritative direction sources
Historical/stale direction sources
Repository evidence relevant to direction
Authority/freshness conflicts
Current-State Consistency Gate: PASS | FAIL | UNCERTAIN
Deliverable-class evidence
Material unresolved direction questions
History expansion performed and why
Next permitted action
```

## Stop conditions

Stop without Target inference when:

- current-state consistency is `FAIL`;
- a material authority conflict cannot be resolved from existing evidence;
- the repository root or active lifecycle boundary is ambiguous;
- the user must decide between materially different deliverable classes.

## Output contract

Lead with the consistency verdict. Report the authoritative direction sources, conflicts, bounded history expansion, assessment path, unresolved decisions, and next permitted action. Do not propose implementation tasks.
