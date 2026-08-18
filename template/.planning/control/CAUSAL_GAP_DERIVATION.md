# Causal Gap Derivation

- Workflow ID: `PW-DIR-005`
- Workflow version: `1.0.0`
- Source lineage: `REC-PL-DIRECTION-001-v2` / Poker Project Spine pilot
- Mode: Planning

Use after `CURRENT_CAPABILITY_ASSESSMENT.md` has a defensible assessment boundary and `Formal-Gap derivation readiness: READY`.

This workflow converts demonstrated missing Target properties into a small causal Gap Map. It does not reconcile recommendation/history, rank Gaps, synthesize Roadmap outcomes, create a Change, or implement fixes.

## Preconditions

Require:

```text
Direction Inventory gate = PASS and still current
TARGET_STATE status = ACCEPTED
CAPABILITY_MODEL status = CURRENT_BASELINE
CURRENT_CAPABILITY_ASSESSMENT status = CURRENT for those baselines
Formal-Gap derivation readiness = READY
```

If assessment evidence is stale relative to material repository changes, return to `CURRENT_CAPABILITY_ASSESSMENT.md` first.

## Allowed write scope

May update only:

- `.planning/project/GAP_MAP.md`;
- `.planning/ACTIVE.md` for the next direction gate.

Current assessment, Target, Capability Model, Roadmap, recommendations, Changes, and production code are read-only in this workflow.

## Required starting reads

Start with:

1. `.planning/ACTIVE.md`;
2. `.planning/project/TARGET_STATE.md`;
3. `.planning/project/CAPABILITY_MODEL.md`;
4. `.planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md`;
5. the current `.planning/project/GAP_MAP.md`, if it contains prior accepted identities.

Do not reopen repository code/evidence by default. The assessment is the evidence boundary for this synthesis. Read targeted evidence only when a specific assessment statement cannot be interpreted safely.

Do not load broad recommendation, decision, old Roadmap, or completed-Change history in this workflow. Historical reconciliation belongs to PL-V38-03.

## Gap definition

A formal Gap is a **causal missing condition between the demonstrated Current state and an accepted Target capability property**.

A Gap is not:

- a symptom list;
- a task or file to edit;
- a proposed implementation;
- a recommendation;
- a Roadmap outcome;
- a Change;
- an evidence limitation by itself;
- a stronger capability than the accepted Target requires.

Use stable project-local IDs such as `GAP-001`, `GAP-002`, ... . Preserve an existing accepted Gap ID when the causal meaning is materially the same.

## Causal compression

Start from assessment entries with demonstrated missing Target properties (`PARTIAL` or `NOT_SATISFIED`).

Compress symptoms when one missing causal condition explains several observed deficits.

Example shape:

```text
symptom A: labels are ambiguous
symptom B: alternatives expose evidence inconsistently
symptom C: CLI terminology conflicts with docs

→ one possible causal Gap:
  no explicit end-to-end recommendation/evidence contract
```

Do not merge independent causal deficits merely because one implementation Change might address both.

## Capability effects

Each Gap records:

```text
Primary capability effects
Dependent capability effects
```

- `PRIMARY`: the Gap directly represents a missing required property of that capability.
- `DEPENDENT`: closing the Gap materially supports another capability, but the Gap is not that capability's primary missing property.

One Gap may have several primary or dependent capability refs.

A capability assessed `SATISFIED` must not be silently reopened through a new primary Gap. If causal reasoning appears to require that, return to Current Capability Assessment and reconcile the contradiction first.

## Evidence uncertainty rule

```text
evidence limitation != automatic Gap
```

If Coverage is `UNCERTAIN`, or the only basis for a missing property is weak/missing evidence, do not mint a Gap for that property. Route to bounded evidence acquisition or reassessment.

A Target may itself require evidence/reproducibility as a completed-state property. In that case, absence of the required evidence can be a real Gap because the evidence is part of the Target, not merely because the assessor is uncertain.

## Gap record contract

For each proposed Gap record:

```text
Gap ID
Gap statement
Gap class (project-local descriptive label, optional)
Primary capability refs
Dependent capability refs
Current evidence from the capability assessment
Missing Target property / causal condition
Closure condition
Evidence required for closure
Dependencies on other Gap identities, if logically required
Owned downstream CAPABILITY_DESIGN_QUESTION / RESEARCH_QUESTION
Known implementation candidates or historical signals, only if already present in current evidence
```

### Outcome-oriented closure

Closure describes **what must become true**, not what task must be performed.

Good:

```text
A documented and contract-tested supported API boundary exists with explicit responsibilities and failure behavior.
```

Bad:

```text
Edit __init__.py and add three tests.
```

`Change completion != Gap closure`.

A later reconciliation must inspect evidence against the Gap closure condition. Completing a Change does not automatically close any Gap.

## Gap Map status and human authority

Canonical map statuses:

```text
DRAFT
CURRENT_BASELINE
```

- `DRAFT`: agent-derived causal synthesis not yet explicitly accepted.
- `CURRENT_BASELINE`: the user explicitly accepts this Gap set/identity structure as the current direction baseline.

An agent may derive and revise a `DRAFT` Gap Map but must not promote it to `CURRENT_BASELINE` without explicit user authority.

Individual newly derived Gaps start `OPEN`. This workflow defines closure conditions but does not close Gaps.

## Procedure

1. Verify current accepted Target/Capability baselines and assessment readiness.
2. Extract only demonstrated missing Target properties from `PARTIAL` and `NOT_SATISFIED` capabilities.
3. Separate true missing properties from evidence limitations and unresolved uncertainty.
4. Group symptoms by causal missing condition.
5. Split groups when closure conditions differ materially even if one implementation could touch both.
6. Assign stable Gap IDs and primary/dependent capability effects.
7. Define outcome-oriented closure conditions and required closure evidence.
8. Check whether any proposed Gap silently reopens a `SATISFIED` capability; if so, stop and reassess.
9. Preserve downstream design/research questions without answering or ranking them.
10. Write `.planning/project/GAP_MAP.md` as `DRAFT` and present it for explicit acceptance.
11. Only after explicit user acceptance may status become `CURRENT_BASELINE` and the next permitted action advance to recommendation/history reconciliation.

## Hard checks

- `CHK-GAP-001`: every Gap traces to at least one demonstrated missing Target property in the current capability assessment.
- `CHK-GAP-002`: no Gap is created solely from an evidence limitation or `UNCERTAIN` Coverage.
- `CHK-GAP-003`: symptom-level deficits sharing one causal condition are consolidated where closure meaning is the same.
- `CHK-GAP-004`: independent causal conditions remain separate even if one implementation Change could address both.
- `CHK-GAP-005`: every Gap distinguishes PRIMARY and DEPENDENT capability effects.
- `CHK-GAP-006`: no `SATISFIED` capability is silently reopened by a primary Gap.
- `CHK-GAP-007`: every closure condition is outcome-oriented and does not prescribe files/tasks/Changes.
- `CHK-GAP-008`: Gap identity remains distinct from RoadmapOutcome and Change identity.
- `CHK-GAP-009`: `CURRENT_BASELINE` has explicit user acceptance evidence.
- `CHK-GAP-010`: broad recommendation/Roadmap history is deferred to the later reconciliation workflow.

## Stop conditions

Stop without a formal Gap baseline when:

- current assessment readiness is `BLOCKED`;
- a missing property depends on unresolved evidence uncertainty;
- causal grouping cannot distinguish materially different closure conditions;
- a proposed Gap contradicts a `SATISFIED` capability judgment;
- current evidence produces a material `TARGET_STATE_SIGNAL`;
- explicit user acceptance is required to promote the map.

## Output contract

Report Gap Map status, Gap count, primary/dependent capability coverage, evidence-uncertainty items deliberately excluded from the Gap Map, explicit acceptance state, and the next permitted action. Do not rank Gaps, synthesize Roadmap outcomes, or create a Change.
