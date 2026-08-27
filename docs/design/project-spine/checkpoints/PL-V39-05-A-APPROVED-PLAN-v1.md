# PL-V39-05-A Approved Central Implementation Plan

**Plan ID:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001-CENTRAL-PLAN-001`
**Approval:** `EXPLICIT USER APPROVAL`
**Approval date:** `2026-08-27`
**Source Plan SHA256:** `d265fc85bb559df05c2f19d5ca551ae79301bcb327187728809bfcba214dde41`
**Implementation authorization:** `NO`

The body below is the user-approved Plan, normalized only for terminal Markdown
whitespace so repository whitespace verification remains deterministic.

---

# CHG-PL-V39-05-A-SHAPING-FOUNDATION-001
## Central Implementation Plan v1.0

**Plan ID:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001-CENTRAL-PLAN-001`
**Version:** `v1.0`
**Date:** `2026-08-27`
**Status:** `READY FOR USER PLAN APPROVAL`
**Definition:** `APPROVED`
**Active Change:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001`
**Implementation authorized:** `NO`
**Target repository:** Planning Lite central source
**Target live worktree:** `D:\documents\planning-lite`
**Baseline branch:** `reconcile/current-design-spine-2026-08-25`
**Baseline HEAD:** `b7f7c2602787afff60bf56c219a208b1a288d779`
**Source approved Definition SHA256:** `5944dcc47b13f59ffcb99f1ee084a2f321ae7ecddb0133a160920162c79c1bda`
**Canonical normalized Definition SHA256:** `4c0a2c288e5b1e063fe6534c826e851fc7faf0074e2ec2a1ea9ee7a1a2fde558`

---

# 1. Objective

Implement the first genuinely new PL-V39-05 shaping foundation without rebuilding
the existing Project Spine entry contract.

The Change delivers exactly two product capabilities:

```text
A. bounded Project Survey
   = optional AS-IS evidence for material brownfield/current-state work

B. bounded Clarification Sweep
   = conditional Target-boundary ambiguity resolution inside
     TARGET_BASELINE_CALIBRATION
```

Plus the minimum documentation/integrity/test seam required to make those
capabilities safe, updateable, and verifiable.

This Plan does not introduce a new workflow engine, lifecycle stage, router branch,
project truth authority, mandatory lexicon, research execution subsystem, Target
Skeleton, Strategy Portfolio, or Executable Target Contract.

---

# 2. Planning authority and lifecycle

Current central state:

```text
active_change:
CHG-PL-V39-05-A-SHAPING-FOUNDATION-001

lifecycle_gate:
PLANNING_IN_PROGRESS

implementation_authorized:
NO

next_permitted_action:
prepare_pl_v39_05_a_implementation_plan
```

Approval sequence:

```text
Plan approval
    ↓
Formal Readiness
    ↓
Readiness PASS
    ↓
separate explicit user Execution authorization
    ↓
T-01 / T-02 implementation may begin
```

Important:

```text
Plan approval != implementation authorization
Readiness PASS != implementation authorization
```

No product write is permitted by this Plan alone.

---

# 3. Final Definition-constrained write surface

## 3.1 ADD

```text
template/.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
tests/test_project_shaping_foundation.py
```

## 3.2 MODIFY

```text
template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
template/.planning/assessments/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
```

## 3.3 CONDITIONAL MODIFY

Only if Formal Readiness proves the current ownership rules do not already cover
the new managed assessment template / project-owned materialized Survey:

```text
template/.planning/framework/OWNERSHIP.yml
```

Default expectation:

```text
OWNERSHIP.yml semantic edit = NOT REQUIRED
```

If it is required, Readiness must state exactly why and what ownership invariant
is otherwise violated.

## 3.4 MUST NOT MODIFY without returning to Planning / Definition amendment

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

copier.yml
pyproject.toml
uv.lock
```

No implementation convenience may silently widen this boundary.

---

# 4. Implementation strategy

Use two independent semantic tracer slices first:

```text
T-01 Survey semantics
T-02 Clarification semantics
```

They converge only after their individual contracts are stable:

```text
T-01 ─┐
      ├→ T-03 integrity/docs seam
T-02 ─┘
        ↓
       T-04 focused deterministic acceptance
        ↓
       T-05 update-safety acceptance
        ↓
       T-06 completion review
```

This ordering allows a defect in Survey behavior to be adjudicated without
entangling Clarification behavior, and vice versa.

---

# 5. T-01 — Project Survey contract + managed template

## Purpose

Add the smallest honest Project Survey capability.

## Product writes

### ADD

```text
template/.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
```

### MODIFY

```text
template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md
```

No other product file is permitted in T-01.

## Required Survey contract

The Survey must state:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

It is not a second owner of:

```text
CURRENT_STATE
CURRENT_CAPABILITY_ASSESSMENT
CAPABILITY_MODEL
GAP_MAP
TARGET_STATE
ROADMAP
```

## Minimum schema

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

Normative field names may vary minimally if existing assessment conventions
require it, but the semantics may not be weakened.

## Invocation trigger

`CURRENT_CAPABILITY_ASSESSMENT` conditionally requires Survey only when:

```text
material brownfield/current-state work
AND
the assessment depends on repository/runtime structure
AND
existing current evidence is not sufficiently bounded/fresh
```

Routine/simple work may bypass Survey.

## Freshness

A usable Survey records:

```text
reflects_revision
survey_scope
evidence_sources
```

Refresh or narrow it when:

```text
material repository/runtime drift occurs
OR
the active work leaves surveyed scope
```

Unrelated minor drift must not automatically invalidate the Survey.

## Evidence honesty

The Survey must:

- distinguish observed evidence from inference;
- use `UNKNOWN` where evidence is absent;
- not rewrite observed behavior as historical intent;
- remain bounded to its stated scope;
- not equate Survey completeness with capability or Target completeness.

## T-01 stop conditions

Stop and return to Planning if implementation appears to require:

- a new root/mode router branch;
- a new project-state authority;
- Python runtime changes;
- a new generalized provenance ontology;
- mandatory Survey creation for all work.

---

# 6. T-02 — Bounded Clarification Sweep semantics

## Purpose

Make Target clarification explicit enough to prevent materially divergent
implementations without creating a new workflow stage.

## Product writes

### MODIFY only

```text
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
```

No additional product file is permitted in T-02.

## Conditional sweep

For material ambiguity, check:

- goal / non-goal conflict;
- unstated assumptions;
- edge cases that change Target boundary;
- term ambiguity;
- acceptance/evidence ambiguity;
- semantic-owner ambiguity.

Use the determinacy test:

```text
Can two reasonable implementers build materially different things
while both satisfying the text?
```

## Question ownership

Preserve exactly:

```text
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION
```

If ambiguity changes accepted Target boundary:

```text
→ TARGET_BOUNDARY_QUESTION
```

If it belongs to downstream capability design:

```text
→ CAPABILITY_DESIGN_QUESTION
```

If it requires downstream research:

```text
→ RESEARCH_QUESTION
```

The latter two do not hold Target convergence open merely because downstream
resolution is incomplete.

## Stop rule

Clarification stops when every material Target-boundary ambiguity is:

```text
RESOLVED
or
represented by an explicit TARGET_BOUNDARY_QUESTION
```

Do not continue clarification merely because implementation design or research
uncertainty exists.

## Existing Target status mapping

Preserve:

```text
TARGET_BOUNDARY_QUESTION > 0
→ DRAFT

TARGET_BOUNDARY_QUESTION = 0
→ may be eligible for PROVISIONAL_TARGET_BASELINE

ACCEPTED
→ explicit human acceptance required
```

Do not introduce:

```text
CONVERGED
TARGET_CONVERGED
SHAPING_READY
```

or equivalent new lifecycle/status values.

## Terminology

Existing `project/GLOSSARY.md` remains the conditional terminology home when
meaningful term drift exists.

T-02 must not create a mandatory Project Lexicon artifact.

## T-02 stop conditions

Stop and return to Planning if implementation appears to require:

- a new clarification workflow;
- router changes;
- prompt/skill changes;
- a second unresolved-question ledger;
- a generic research execution subsystem.

---

# 7. T-03 — Documentation, ownership and integrity seam

## Dependency

```text
T-01 = semantically stable
T-02 = semantically stable
```

## Product writes

### MODIFY

```text
template/.planning/assessments/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
```

### CONDITIONAL

```text
template/.planning/framework/OWNERSHIP.yml
```

only if Formal Readiness or implementation evidence proves it is required.

## Purpose

Make the new managed Survey discoverable and preserve repository integrity/update
semantics.

## Required outcomes

- assessment documentation explains when Survey is optional/material;
- manifest records the new managed template;
- SHA receipt is exact;
- ownership remains consistent with managed pristine template vs project-owned
  materialized assessment;
- no new state authority is implied by documentation.

## T-03 stop condition

Any ownership-model ambiguity that cannot be resolved from existing rules returns
the Change to Planning before editing `OWNERSHIP.yml`.

---

# 8. T-04 — Focused deterministic product acceptance

## ADD

```text
tests/test_project_shaping_foundation.py
```

## Required focused assertions

At minimum prove:

1. Survey template exists;
2. minimum Survey schema exists;
3. `reflects_revision` contract exists;
4. Survey is evidence-only / non-authoritative;
5. Survey invocation is conditional on materiality + structural dependence +
   freshness/evidence insufficiency;
6. routine work may bypass Survey;
7. Survey refresh is tied to material drift or scope escape;
8. Clarification determinacy test exists;
9. Clarification has a bounded stop rule;
10. the three question owner classes remain present;
11. only Target-boundary questions block provisional Target eligibility;
12. no `CONVERGED` / `SHAPING_READY` state is introduced;
13. Glossary remains conditional terminology owner;
14. ROOT_ROUTER / MODE_ROUTER do not gain a Project Survey / Shaping entry branch;
15. manifest/SHA integrity is consistent.

Tests should assert product semantics and structural invariants, not Markdown
spacing trivia.

## Focused owner tests

Run at minimum:

```powershell
uv run --frozen pytest -q tests/test_project_shaping_foundation.py
uv run --frozen pytest -q tests/test_current_capability_gap_foundation.py
uv run --frozen pytest -q tests/test_direction_foundation.py
```

Formal Readiness may add directly affected existing tests if ownership inspection
shows they are required.

---

# 9. T-05 — Consumer update-safety acceptance

## Purpose

Prove the managed/project-owned split works in a realistic disposable consumer
fixture.

Required property:

```text
central managed:
.planning/assessments/PROJECT_SURVEY_TEMPLATE.md

consumer project-owned materialization:
.planning/assessments/current/PROJECT_SURVEY.md
```

A consumer update must:

```text
update managed template when central source changes
AND
preserve project-owned materialized PROJECT_SURVEY.md
```

## Minimum verification

Run the repository-owned local-only update regression:

```powershell
uv run --frozen pytest -q tests/test_local_only_update.py
```

plus one bounded disposable consumer fixture if the current regression does not
already exercise the new Survey path.

No canonical external consumer project may be mutated for this acceptance.

If the new template causes destructive or ambiguous ownership behavior, classify
the issue before changing ownership metadata.

---

# 10. T-06 — Completion review

T-06 is review/verification, not new feature implementation.

## Required completion evidence

Confirm all of:

```text
Project Survey is optional/bounded
Project Survey is AS-IS evidence
Survey has exact revision/scope/evidence identity
Survey does not create second authority

Clarification Sweep is conditional/bounded
determinacy test is explicit
question owner classes are preserved
Target status model is unchanged

no root/router growth
no prompt/skill expansion
no generic research workflow
no mandatory Lexicon
no ownership drift
```

## Completion verification

At completion gate:

```powershell
uv run --frozen pytest -q tests/test_project_shaping_foundation.py
uv run --frozen pytest -q tests/test_current_capability_gap_foundation.py
uv run --frozen pytest -q tests/test_direction_foundation.py
uv run --frozen pytest -q tests/test_local_only_update.py
```

Then run the broader repository suite once:

```powershell
uv run --frozen pytest -q
```

plus repository-owned template-integrity/update checks identified by Formal
Readiness.

Run:

```powershell
git diff --check
git status --short
```

and exact changed-path / MUST-NOT-MODIFY audit.

## Completion verdict

Allowed:

```text
Completed
Needs bounded revision
Blocked
Rejected
```

`Completed` for this Change means only `PL-V39-05-A` is complete.

It does not mean the full `PL-V39-05` Roadmap outcome is complete.

---

# 11. Acceptance-criteria ownership map

| AC | Meaning | Primary task | Final proof |
|---|---|---|---|
| AC-01 | Survey placement | T-01 | T-04 |
| AC-02 | Survey honesty | T-01 | T-04 |
| AC-03 | Survey schema | T-01 | T-04 |
| AC-04 | Survey freshness | T-01 | T-04 |
| AC-05 | Routine bypass | T-01 | T-04 |
| AC-06 | Clarification boundedness | T-02 | T-04 |
| AC-07 | Question owner preservation | T-02 | T-04 |
| AC-08 | No duplicate statuses | T-02 | T-04 |
| AC-09 | Glossary conditional | T-02 | T-04 |
| AC-10 | Routing boundary | T-01/T-02 | T-04/T-06 |
| AC-11 | Ownership/update safety | T-03 | T-05 |
| AC-12 | Template integrity | T-03 | T-04/T-06 |
| AC-13 | Focused verification | T-04/T-05 | T-06 |

---

# 12. Formal Readiness requirements after Plan approval

Formal Readiness must be read-only and must resolve the live repository against the
approved Plan before Execution authority is requested.

At minimum:

## R-00 Git identity

Verify exact central root, branch, live HEAD and clean tree.

The approved Plan baseline is:

```text
HEAD = b7f7c2602787afff60bf56c219a208b1a288d779
```

If Planning state is committed after Plan approval, Readiness may accept the exact
reviewed successor HEAD.

## R-01 Definition + Plan authority

Verify:

```text
Definition = approved
Plan = approved
implementation_authorized = NO
```

## R-02 Write-surface closure

Resolve every planned ADD/MODIFY/CONDITIONAL path and prove no current repository
fact requires a Definition MUST-NOT-MODIFY path.

## R-03 Ownership closure

Inspect current `OWNERSHIP.yml` and local update semantics to answer conclusively:

```text
Does existing ownership already classify
assessments/PROJECT_SURVEY_TEMPLATE.md as managed
and assessments/current/PROJECT_SURVEY.md as project-owned?
```

No assumption may survive Readiness on this point.

## R-04 Integrity closure

Resolve the exact repository mechanism for:

```text
MANIFEST_V4.md
SHA256SUMS.txt
```

including how hashes are regenerated/verified and which existing tests own that
contract.

## R-05 Test-command closure

Resolve exact current commands for:

```text
focused shaping test
current capability owner test
direction owner test
local-only update test
broader completion suite
```

## R-06 Consumer fixture closure

Resolve a disposable fixture strategy for T-05.

No canonical Poker or other live consumer is required.

## R-07 MUST-NOT-MODIFY closure

Record exact baseline hashes or equivalent changed-path controls for the protected
surfaces, especially:

```text
ROOT_ROUTER.md
MODE_ROUTER.md
PROJECT_BOOTSTRAP.md
PROJECT_STATE_REFRESH.md
project/*.md authorities
prompts/**
skills/**
src/**
```

## R-08 Contract/determinacy closure

Confirm the Survey materiality trigger and Clarification stop rule are
implementation-determinate enough that two reasonable implementers would not
produce materially different contracts.

If not, Readiness blocks before implementation.

## R-09 Execution authorization boundary

Readiness PASS must end with:

```text
Implementation authorized: NO
Next gate: explicit user authorization to execute T-01/T-02
```

---

# 13. Verification economy

During implementation use:

```text
task-local owner test
→ focused PL-V39-05-A acceptance
→ changed-path / Git boundary
→ broader suite only at completion/integration gate
```

Do not run the full suite after every Markdown contract edit unless an actual
integration concern requires it.

If a custom verifier fails:

```text
classify
PRODUCT_DEFECT
vs
VERIFIER_DEFECT
```

before modifying product semantics.

A verifier failure must not be "fixed" by hand-tuning unrelated product text.

---

# 14. Cost / complexity profile

| Task | Complexity | Blast radius | Main risk |
|---|---|---|---|
| T-01 Survey | Medium | Low | accidental second authority / over-triggering |
| T-02 Clarification | Medium | Low | endless clarification / new status semantics |
| T-03 integrity seam | Low–Medium | Medium | ownership/update drift |
| T-04 focused tests | Medium | Low | formatting-heavy brittle tests |
| T-05 update safety | Medium | Medium | project-owned Survey overwritten |
| T-06 completion | Low | None | incomplete evidence / scope creep |

The highest-risk seam is not the Markdown schema itself. It is the managed vs
project-owned update boundary in T-03/T-05.

---

# 15. Explicit exclusions

No task in this Plan may implement:

```text
Brownfield Recovery / archaeology capsules
full behavior provenance ontology
Outcome Ladder
FAST_WITH_LEDGER / SOCRATIC / BATCH_CLARIFICATION / HUMAN_GATES_ONLY
Strategy Portfolio
Target Skeleton
Executable Target Contract
System Claims / Target Scenarios
generic governed research execution
Context Compiler
model/effort routing
new checklist control plane
```

If one becomes necessary to complete T-01..T-05, stop and return to Planning.

---

# 16. Plan approval boundary

Current state:

```text
Definition approved: YES
Central Change active: YES
Plan prepared: YES
Plan approved: NO
Formal Readiness run: NO
Implementation authorized: NO
T-01 started: NO
T-02 started: NO
```

Explicit user approval of this Plan authorizes only:

```text
persist Plan approval / Planning checkpoint as needed
→ perform read-only Formal Readiness
```

It does not authorize product/template/test implementation.

After Plan approval, the next permitted action is:

```text
run PL-V39-05-A Formal Readiness
```

After a Readiness PASS, obtain a separate explicit user authorization before
executing T-01 or T-02.

---

## Approval boundary

```text
Plan approved: YES
Formal Readiness: AUTHORIZED
Implementation: NOT AUTHORIZED
T-01/T-02: NOT STARTED
```
