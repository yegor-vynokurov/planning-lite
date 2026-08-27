# Current Capability Assessment

- Workflow ID: `PW-DIR-004`
- Workflow version: `1.0.0`
- Source lineage: `REC-PL-DIRECTION-001-v2` / Poker Project Spine pilot
- Mode: Audit

Use after Target calibration has produced an `ACCEPTED` `.planning/project/TARGET_STATE.md` and an explicitly accepted `CURRENT_BASELINE` `.planning/project/CAPABILITY_MODEL.md`.

This workflow assesses what the repository currently demonstrates against that accepted capability baseline. It does not revise the Target or Capability Model, derive formal Gaps, reconcile recommendations/history, rank work, create a Roadmap outcome, or authorize a Change.

## Preconditions

Before assessment, verify:

```text
Direction Inventory gate = PASS and still current
TARGET_STATE status = ACCEPTED
CAPABILITY_MODEL status = CURRENT_BASELINE
repository/lifecycle boundary = known
```

If the accepted Target or Capability Model changed after the current direction inventory, refresh the inventory first. If either baseline lacks the required explicit acceptance evidence, stop and return to `TARGET_BASELINE_CALIBRATION.md`.

## Allowed write scope

May update only:

- `.planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md`;
- `.planning/assessments/current/PROJECT_SURVEY.md` only when the conditional Survey trigger below is satisfied;
- `.planning/assessments/archive/` when an older current assessment or Survey must be preserved before replacement;
- `.planning/ACTIVE.md` for the next permitted direction action or a blocker.

Target, Capability Model, Gap Map, Roadmap, recommendations, Changes, and production code are read-only in this workflow.

## Required starting reads

Start with:

1. `.planning/ACTIVE.md`;
2. the current `.planning/assessments/current/direction-inventory.md`;
3. `.planning/project/TARGET_STATE.md`;
4. `.planning/project/CAPABILITY_MODEL.md`;
5. `.planning/project/CURRENT_STATE.md`;
6. `.planning/project/REPOSITORY_MAP.md`;
7. targeted repository/code/test/data/documentation/Git evidence for the capability currently being assessed.

Use `CONTEXT_POLICY.md`. Do not load broad recommendation history, old Roadmaps, or all completed Changes by default. Historical Change evidence may be opened only when a current capability claim depends on that exact evidence or provenance.

## Conditional Project Survey

Project Survey is optional bounded AS-IS evidence, not another Project Spine
authority.

Use or refresh `.planning/assessments/current/PROJECT_SURVEY.md` from
`.planning/assessments/PROJECT_SURVEY_TEMPLATE.md` only when **all three** are
true:

```text
material brownfield/current-state work
AND
the assessment depends on repository/runtime structure
AND
existing current evidence is not sufficiently bounded/fresh
```

Routine or small work may bypass Project Survey.

The Survey must preserve this boundary:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

It must not become a second owner of `CURRENT_STATE`,
`CURRENT_CAPABILITY_ASSESSMENT`, `CAPABILITY_MODEL`, `GAP_MAP`, `TARGET_STATE`,
or `ROADMAP`.

A usable Survey records:

```text
Reflects revision
Survey scope
Evidence sources
```

Reuse it only while those fields remain adequate for the active assessment.
Refresh or narrow it when material repository/runtime drift occurs or active work
leaves the surveyed scope. Unrelated minor drift does not automatically invalidate
the whole Survey.

Within the Survey, distinguish `OBSERVED` evidence from `INFERRED` interpretation
and use `UNKNOWN` when evidence is absent or outside scope. Do not infer historical
intent from observed implementation.

Survey completion does not imply capability completeness, formal Gap readiness,
or Target acceptance.

## Two-axis assessment model

Every capability receives **two independent judgments**.

### Coverage

Allowed values:

```text
SATISFIED
PARTIAL
NOT_SATISFIED
UNCERTAIN
```

Interpretation:

- `SATISFIED`: all material completed-state properties required by this capability are demonstrated within the accepted Target boundary.
- `PARTIAL`: at least one material required property is demonstrated and at least one material required property is not demonstrated.
- `NOT_SATISFIED`: the required completed-state capability is materially absent; supporting/preparatory assets may exist but do not satisfy the capability.
- `UNCERTAIN`: available evidence is insufficient or contradictory to determine coverage safely.

Do not use `UNCERTAIN` as a softer synonym for `PARTIAL` or `NOT_SATISFIED`.

### EvidenceConfidence

Allowed values:

```text
HIGH
MEDIUM
LOW
```

Interpretation:

- `HIGH`: direct, current, reproducible or otherwise strong evidence supports the coverage judgment.
- `MEDIUM`: relevant evidence exists but has meaningful scope, freshness, provenance, or representativeness limits.
- `LOW`: the judgment rests on weak, indirect, stale, sampled, or incomplete evidence.

`Coverage != EvidenceConfidence`.

Examples:

```text
SATISFIED + LOW
→ capability appears present, but proof is weak

NOT_SATISFIED + HIGH
→ absence is directly established

UNCERTAIN + HIGH
→ strong evidence establishes that the available state is genuinely indeterminate/contradictory
```

## PARTIAL decomposition

For every `PARTIAL` capability record separately:

```text
satisfied target properties
missing target properties
evidence limitations
```

Do not compress these into a generic "partially implemented" sentence.

Evidence limitations describe limitations of the proof. They are not themselves missing Target properties.

## Assessment record per capability

For each accepted Capability ID record:

```text
Capability ID and target summary
Coverage
EvidenceConfidence
Current assets / satisfied target properties
Target properties not yet demonstrated
Evidence limitations
Owned downstream design/research questions, if relevant
Evidence references
```

Use repository paths, symbols, tests, commands, artifact identities, decisions, or bounded Git evidence where useful. Distinguish current evidence from historical closure evidence.

## Evidence rules

- A file name or planned Change is not proof that a capability exists.
- A completed Change is evidence only for what its closure/evidence actually demonstrates.
- Documentation claims are evidence of documented intent/semantics, not automatically of runtime behavior.
- Missing search hits alone do not prove non-existence when the repository boundary or naming is uncertain.
- Preparatory infrastructure does not satisfy a capability whose defining outcome is absent.
- Explicit non-goals in the accepted Target must not be scored as missing properties.
- A `SATISFIED` capability must not be silently reopened because a stronger but unrequired implementation is imaginable.

## Assessment status and verdict

Canonical assessment statuses:

```text
DRAFT
CURRENT
```

- `DRAFT`: capability-by-capability evidence work is incomplete.
- `CURRENT`: every baseline Capability ID has a recorded Coverage/EvidenceConfidence judgment and the snapshot is bound to the stated repository/Target/Capability baseline. `CURRENT` does not imply Gap readiness.

The assessment must record:

```text
Assessment status
Target baseline reference/status
Capability baseline reference/status
Repository revision/boundary
Evidence scope and limits
Per-capability judgments
Capabilities requiring evidence acquisition
Formal-Gap derivation readiness: READY | BLOCKED
```

`READY` means every capability has a defensible Coverage judgment and any `UNCERTAIN` items are either resolved or explicitly determined not to permit formal Gap derivation for those properties.

`BLOCKED` means causal Gap derivation would require treating missing evidence as missing capability or otherwise guessing.

## Procedure

1. Verify the accepted Target, current Capability Model baseline, and direction-inventory consistency boundary.
2. Freeze the assessment repository revision/scope.
3. Evaluate the conditional Project Survey trigger. If all three conditions are true, create, reuse, refresh, or narrow the bounded Survey before capability-by-capability inspection. Otherwise bypass it.
4. For each Capability ID, identify the exact completed-state properties to test.
5. Inspect only the evidence needed for that capability, expanding history only for concrete provenance questions.
6. Assign Coverage independently from EvidenceConfidence.
7. For `PARTIAL`, separate satisfied properties, missing properties, and evidence limitations.
8. Record bounded evidence references and downstream design/research questions without answering them unless required for coverage.
9. Check cross-capability consistency: the same demonstrated property should not be simultaneously treated as present and absent without explanation.
10. Write/refresh `.planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md`, archiving a superseded snapshot when needed. Set status `CURRENT` only when every baseline capability has a complete judgment bound to the stated assessment boundary.
11. Set `Formal-Gap derivation readiness` and the next permitted action. Do not derive formal Gaps in the same turn.

## Hard checks

- `CHK-CAP-ASSESS-001`: accepted Target and `CURRENT_BASELINE` Capability Model with explicit authority evidence exist.
- `CHK-CAP-ASSESS-002`: every baseline Capability ID has exactly one Coverage value and one EvidenceConfidence value.
- `CHK-CAP-ASSESS-003`: Coverage and EvidenceConfidence are recorded independently.
- `CHK-CAP-ASSESS-004`: every `PARTIAL` entry separates satisfied properties, missing properties, and evidence limitations.
- `CHK-CAP-ASSESS-005`: evidence limitation alone is not recorded as a missing Target property.
- `CHK-CAP-ASSESS-006`: explicit Target non-goals are not scored as missing capabilities.
- `CHK-CAP-ASSESS-007`: `SATISFIED` is judged against the accepted bounded Target, not an imagined stronger project.
- `CHK-CAP-ASSESS-008`: broad recommendation/Roadmap history was not loaded without a concrete evidence/provenance reason.
- `CHK-CAP-ASSESS-009`: formal Gap derivation is `BLOCKED` if a proposed missing property depends only on unresolved evidence uncertainty.
- `CHK-CAP-ASSESS-010`: `CURRENT` assessment status covers every accepted baseline Capability ID and is bound to the stated repository/Target/Capability baseline.
- `CHK-CAP-ASSESS-011`: Project Survey is created/used only when all three conditional trigger terms are satisfied; routine/small work may bypass it.
- `CHK-CAP-ASSESS-012`: any Project Survey records revision, scope, evidence sources, and remains evidence-only rather than a competing Project Spine authority.
- `CHK-CAP-ASSESS-013`: Survey refresh is required for material drift or scope escape, not unrelated minor drift.

## Stop conditions

Stop and do not derive or imply formal Gaps when:

- Target or Capability Model authority is not current;
- Direction Inventory consistency is no longer reliable;
- repository/lifecycle boundary is ambiguous;
- material capability coverage remains `UNCERTAIN` and the uncertainty would control a Gap claim;
- the user must resolve a Target-boundary issue exposed by current evidence.

A discovery that materially invalidates the accepted Target is a `TARGET_STATE_SIGNAL`; route back to `TARGET_BASELINE_CALIBRATION.md` rather than forcing the evidence into a Gap.

## Output contract

Lead with assessment readiness and the highest-impact evidence limitation, if any. Report the assessment path/revision, Coverage + EvidenceConfidence for every capability, unresolved evidence acquisition, and the next permitted action. Do not rank work, propose Roadmap outcomes, or create a Change.
