# CHG-PL-V39-05-A-SHAPING-FOUNDATION-001 — Definition Draft

**Status:** `APPROVED / CENTRAL DEFINITION / NO IMPLEMENTATION AUTHORITY`
**Roadmap source:** `PL-V39-05 — Project Shaping and Target Reality`
**Slice:** `PL-V39-05-A — Shaping Foundation: Survey + Clarification`
**Definition baseline:** `4fbfb317991e06e7d431470501b97039ed707d0c`
**Branch at definition review:** `reconcile/current-design-spine-2026-08-25`
**Canonical repository:** `D:\documents\planning-lite`

---

## 1. Purpose

Add the smallest reusable Project Shaping foundation that is genuinely new after the
existing Project Spine Direction foundation:

1. preserve the already-implemented PL-V39-05 entry-contract semantics without
   creating a second entry workflow;
2. add a bounded **Project Survey** as optional AS-IS evidence for material
   brownfield/current-state work;
3. add a bounded **Clarification Sweep** to Target calibration for materially
   ambiguous Target text;
4. preserve existing ownership, routing, Change lifecycle, and update-safety
   architecture.

This Change must make Project Shaping more evidence-grounded and less ambiguous
without multiplying workflow stages or project truth authorities.

---

## 2. Problem statement

The existing Project Spine already implements:

```text
PW-DIR-001 DIRECTION_INVENTORY
PW-DIR-002 TARGET_STATE_EXPLORER
PW-DIR-003 TARGET_BASELINE_CALIBRATION
PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT
PW-DIR-005 CAUSAL_GAP_DERIVATION
...
```

The PL-V39-05 entry-contract review found that direction-authority discovery,
deliverable-class-first behavior, unresolved-question ownership, and Target
convergence semantics are already substantially implemented.

The genuinely open foundation gaps for this first shaping slice are narrower:

### Gap A — material brownfield AS-IS evidence has no dedicated bounded survey schema

Current capability assessment has repository/current-state evidence, but PL-V39-05
requires an optional current architecture snapshot that can explicitly record:

- the revision/snapshot it reflects;
- system boundaries;
- components/modules;
- datastores/state;
- external integrations;
- main execution paths;
- build/test/run commands;
- important conventions with source evidence;
- material constraints;
- relevant debt;
- reusable assets.

The survey must remain evidence, not a second Current State, Capability Assessment,
Gap, or Target authority.

### Gap B — Target clarification rules are not yet explicit enough

PL-V39-05 requires a bounded Clarification Sweep for material ambiguity, including
the determinacy test:

> Can two reasonable implementers build materially different things while both
> satisfying the text?

Material ambiguity should be clarified before downstream execution, while
`CAPABILITY_DESIGN_QUESTION` and `RESEARCH_QUESTION` remain owned downstream and
must not hold Target convergence open.

---

## 3. Architectural decisions

### AD-01 — No new entry workflow

Do **not** create:

```text
PROJECT_SHAPING_ENTRY.md
SHAPING_READY lifecycle state
CONVERGED Target state
new root/mode router branch for "Project Shaping"
```

Reuse the existing Direction chain.

### AD-02 — Project Survey is an assessment artifact, not project truth authority

Add one managed pristine template:

```text
.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
```

A project may materialize the current survey only when needed as:

```text
.planning/assessments/current/PROJECT_SURVEY.md
```

The current survey is project-owned runtime evidence under the existing
assessment ownership model.

Normative invariant:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

Survey does not become a second owner of:

```text
CURRENT_STATE
CURRENT_CAPABILITY_ASSESSMENT
CAPABILITY_MODEL
GAP_MAP
TARGET_STATE
ROADMAP
```

### AD-03 — Survey invocation belongs to CURRENT_CAPABILITY_ASSESSMENT

`PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT` remains the authoritative workflow.

It conditionally requires a Project Survey when all of the following are true:

```text
material brownfield/current-state work
AND
the capability assessment depends on repository/runtime structure
AND
existing current evidence is not sufficiently bounded/fresh
```

Routine/small work may bypass Survey.

No new router mutation is required.

### AD-04 — Survey freshness is explicit but lightweight

A usable Survey must record:

```text
reflects_revision
survey_scope
evidence_sources
```

`reflects_revision` should be an exact VCS revision when available, otherwise an
explicit equivalent source snapshot identity.

Refresh or narrow the Survey when:

```text
material repository/runtime drift occurs
OR
the active work leaves the surveyed scope
```

Minor unrelated drift does not automatically invalidate the whole survey.

### AD-05 — Clarification Sweep belongs to TARGET_BASELINE_CALIBRATION

Do not add another lifecycle stage or generic clarification engine in this Change.

Extend `PW-DIR-003 TARGET_BASELINE_CALIBRATION` with a bounded conditional sweep
that checks material:

- goal / non-goal conflict;
- unstated assumptions;
- edge cases that alter Target boundary;
- term ambiguity;
- acceptance/evidence ambiguity;
- semantic-owner ambiguity.

Use the determinacy test only for material ambiguity:

```text
Can two reasonable implementers build materially different things
while both satisfying the text?
```

If `YES` and the ambiguity changes accepted Target boundary, keep or create a
`TARGET_BOUNDARY_QUESTION`.

If the ambiguity belongs to capability design or research, classify and defer it
to that owner rather than keeping Target open.

### AD-06 — No mandatory Project Lexicon in this slice

Existing `project/GLOSSARY.md` remains the terminology home.

Use it only when meaningful term drift exists. Do not require glossary population
for ordinary vocabulary and do not create a second lexicon artifact.

### AD-07 — Existing question identity/ownership remains canonical

This Change must not create a second unresolved-question ledger.

Canonical project question identity/state remains in the existing Target/Project
Spine ownership model. Capability/Gap artifacts may preserve downstream references
without becoming competing question-state authorities.

### AD-08 — No generic research execution workflow

`RESEARCH_QUESTION` classification and preservation are in scope only to the
extent needed for Target clarification semantics.

A generic governed research execution workflow is explicitly deferred to a later
execution/routing design if field evidence justifies it.

---

## 4. Proposed exact product write surface

### ADD

```text
template/.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
tests/test_project_shaping_foundation.py
```

### MODIFY

```text
template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
template/.planning/assessments/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
```

### CONDITIONAL MODIFY

Only if current integrity/update tests prove the new managed assessment template
requires an explicit ownership declaration rather than being covered by existing
assessment ownership globs:

```text
template/.planning/framework/OWNERSHIP.yml
```

Default expectation: **no ownership-manifest semantic change is needed**.

### MUST NOT MODIFY in this Change

```text
template/.planning/control/ROOT_ROUTER.md
template/.planning/control/MODE_ROUTER.md
template/.planning/control/PROJECT_BOOTSTRAP.md
template/.planning/control/PROJECT_STATE_REFRESH.md

template/.planning/project/CURRENT_STATE.md
template/.planning/project/TARGET_STATE.md
template/.planning/project/CAPABILITY_MODEL.md
template/.planning/project/GAP_MAP.md
template/.planning/project/ROADMAP.md

template/.planning/prompts/**
template/.planning/skills/**

src/planning_lite/cli.py
src/planning_lite/local_update.py
```

Exception: a Definition amendment is required before touching any MUST-NOT-MODIFY
surface.

---

## 5. Project Survey minimum schema

`PROJECT_SURVEY_TEMPLATE.md` must remain compact and evidence-oriented.

Minimum sections/fields:

```text
# Project Survey

Status
Reflects revision
Survey scope
Evidence sources

## System boundaries
## Components / modules
## Datastores / durable state
## External integrations
## Main execution paths
## Build / test / run commands
## Important conventions and source evidence
## Material constraints
## Relevant debt
## Reusable assets
## Unknown / not yet observed
```

Required rules:

1. distinguish `OBSERVED` from inference;
2. do not claim historical intent from observed implementation;
3. use `UNKNOWN` rather than inventing evidence;
4. keep scope bounded;
5. state when the survey must be refreshed;
6. never treat Survey completion as capability completeness or Target acceptance.

This slice does **not** introduce the full Brownfield Recovery provenance ontology
(`OBSERVED_IN_CODE`, `OBSERVED_AT_RUNTIME`, etc.). That belongs to the later
brownfield/archaeology slice unless implementation proves a tiny subset is
strictly required here.

---

## 6. Clarification Sweep stop rule

The sweep is conditional, not conversationally endless.

Stop clarification when all material Target-boundary ambiguity has either:

```text
RESOLVED
or
represented by an explicit TARGET_BOUNDARY_QUESTION
```

Do not continue asking merely because implementation design/research uncertainty
exists.

Hard invariant:

```text
TARGET_BOUNDARY_QUESTION > 0
→ Target remains DRAFT

TARGET_BOUNDARY_QUESTION = 0
→ Target may be eligible for PROVISIONAL_TARGET_BASELINE

ACCEPTED
→ still requires explicit human acceptance
```

`Target convergence` must not become a new lifecycle/status value.

---

## 7. Non-goals / explicitly deferred

This Change does **not** implement:

```text
Brownfield Recovery / archaeology capsules
characterization-test workflow
full behavior-provenance ontology

Outcome Ladder

FAST_WITH_LEDGER
SOCRATIC
BATCH_CLARIFICATION
HUMAN_GATES_ONLY
or other adaptive engagement mode machinery

mandatory Project Lexicon

Strategy Portfolio / strategy cards / switch triggers

Target Skeleton / placeholder semantics

Executable Target Contract
System Claims
Target Scenarios

Roadmap synthesis enrichment for Outcome Level / active strategy / skeleton /
implementation gap / evidence gap

generic governed research execution workflow

Context Compiler
model/effort routing
new checklist control plane
```

These remain later PL-V39-05 / PL-V39-07 / PL-V39-08 work as appropriate.

---

## 8. Acceptance criteria

### AC-01 — Survey placement

A material brownfield/current-state fixture can be routed through existing
`CURRENT_CAPABILITY_ASSESSMENT` semantics and conditionally require a bounded
Project Survey without adding a router or lifecycle stage.

### AC-02 — Survey honesty

The Survey contract explicitly says:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

and cannot be interpreted as a second Current State / Capability / Gap / Target
authority.

### AC-03 — Survey schema

The managed Survey template includes every minimum field/section in Section 5 and
requires `reflects_revision`.

### AC-04 — Survey freshness

The workflow specifies refresh/narrowing on material drift or scope escape while
avoiding automatic invalidation for unrelated minor drift.

### AC-05 — Routine bypass

Small/routine work is not forced to create a Project Survey.

### AC-06 — Clarification boundedness

`TARGET_BASELINE_CALIBRATION` includes the material determinacy test and a stop
rule. Clarification does not become a new lifecycle stage.

### AC-07 — Owner preservation

The three unresolved-question owner classes remain:

```text
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION
```

Only Target-boundary questions block eligibility for
`PROVISIONAL_TARGET_BASELINE`.

### AC-08 — No duplicate statuses

No new `CONVERGED`, `SHAPING_READY`, or equivalent Target/lifecycle state is
introduced.

### AC-09 — Glossary remains conditional

Existing `GLOSSARY.md` is reused only for meaningful term drift; no mandatory
always-on Project Lexicon artifact is added.

### AC-10 — Routing boundary

`ROOT_ROUTER.md`, `MODE_ROUTER.md`, prompts, and skills remain unchanged.

### AC-11 — Ownership/update safety

The managed template is centrally updateable while a project's materialized
`.planning/assessments/current/PROJECT_SURVEY.md` is preserved as project-owned
state under existing ownership/update semantics.

### AC-12 — Template integrity

`MANIFEST_V4.md` and `SHA256SUMS.txt` exactly reflect the resulting managed
template source.

### AC-13 — Focused verification

At minimum:

```text
pytest -q tests/test_project_shaping_foundation.py
pytest -q tests/test_current_capability_gap_foundation.py
pytest -q tests/test_direction_foundation.py
pytest -q tests/test_local_only_update.py
```

must pass.

Broader suite is reserved for the Change completion gate unless an affected
existing owner test requires earlier expansion.

---

## 9. Required focused test contract

New `tests/test_project_shaping_foundation.py` should prove at least:

1. `PROJECT_SURVEY_TEMPLATE.md` exists;
2. required Survey schema markers exist;
3. `reflects_revision` is required;
4. Current Capability Assessment contains the conditional materiality/freshness
   trigger;
5. routine work can bypass Survey;
6. Survey is explicitly evidence-only and non-authoritative;
7. Target Baseline Calibration contains the determinacy test;
8. three question-owner classes are preserved;
9. only Target-boundary questions block provisional Target eligibility;
10. no new Target convergence status is introduced;
11. existing Glossary is conditional terminology owner;
12. no new Project Survey router branch is required;
13. manifest/SHA integrity remains consistent through existing integrity tests.

The test should verify product semantics, not formatting trivia.

---

## 10. Verification economy

Use:

```text
existing owner/product tests
→ one focused new PL-V39-05-A acceptance test
→ Git/write-boundary verification
→ broader suite at meaningful completion gate
```

If a custom verifier fails, classify it first as:

```text
PRODUCT_DEFECT
or
VERIFIER_DEFECT
```

Do not patch product code merely to satisfy a defective verifier.

---

## 11. Proposed implementation tasks after authorization

### T-01 — Survey contract + template

Add the Survey template and extend Current Capability Assessment with bounded
invocation/freshness semantics.

### T-02 — Clarification semantics

Extend Target Baseline Calibration with bounded Clarification Sweep,
determinacy/stop rule, and explicit convergence mapping.

### T-03 — Documentation / integrity seam

Update assessment documentation, manifest, and SHA receipt. Modify ownership only
if exact current glob semantics require it.

### T-04 — Focused product acceptance

Add and pass `test_project_shaping_foundation.py` plus directly affected owner
tests.

### T-05 — Update-safety acceptance

Verify a consumer update/check preserves a materialized project-owned
`PROJECT_SURVEY.md` while updating the centrally managed Survey template.

### T-06 — Completion review

Confirm:

```text
Survey works as bounded AS-IS evidence
Clarification is bounded
no second authority
no new workflow stage
no router growth
no unexpected ownership drift
```

Then decide whether the Change is `Completed` and whether PL-V39-05-B may begin.
Change completion does not imply completion of PL-V39-05.

---

## 12. Definition readiness

Current definition verdict:

```text
DEFINITION_DRAFT_READY_FOR_HUMAN_REVIEW
```

This document does not:

```text
create an active Change
authorize implementation
authorize staging/commit
authorize release
authorize merge/push
```

If explicitly accepted, the next permitted action should be a bounded canonical
Change-definition activation that records this scope and updates central resume
state to the governed Definition/Planning boundary.

---

## Central-source approval record

```text
Definition:
APPROVED BY EXPLICIT USER CONFIRMATION

Central Change:
ACTIVE FOR PLANNING

Implementation:
NOT AUTHORIZED

T-01:
NOT STARTED

Consumer-style root .planning scaffold:
NOT APPLICABLE TO CENTRAL SOURCE
```

The central authoritative active-state carrier is
`docs/design/project-spine/CURRENT.md`.

Durable transition evidence is stored under
`docs/design/project-spine/checkpoints/`.
