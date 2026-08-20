# Planning Lite Roadmap v3.8.7 — local-only update safety gate before Poker Field Pilot 2

**Status:** Current implementation-facing roadmap; operational checkpoint lives in `PL-V38-CURRENT.md`
**Date:** 2026-08-20
**Parent:** Planning Lite Roadmap v3.8.6 (Git history)
**Evidence:** Poker Project Spine pilot + W0/PL-V38-00 + v3.8.2 alignment + PL-V38-01..04 + PILOT-PL-DIRECTION-002 PREP-FINDING-001 + PL-V38-PREP-01 Poker snapshot replay

---

# 1. Why v3.8.7 exists

v3.8 promoted Project Spine from a field-pilot hypothesis to a bounded implementation candidate.
W0 then established that Planning Lite is **template/workflow-first**, not Python-domain-model-first.

A second asset review found two existing research systems that overlap directly with later v3.8 work:

```text
planning-lite-lab
→ research/evidence/governance control plane

planning_lite_tools / step-16.4.1
→ Context Pilot + Eval Harness reference implementation
```

v3.8.2 aligned Project Spine with the real template/workflow architecture and existing research assets.

v3.8.7 preserves completion of `PL-V38-04` and inserts one evidence-driven corrective gate before the scored Poker field pilot. PL-V38-04 established that Planning Lite can now synthesize coherent Roadmap outcomes from the accepted Project Spine, compare credible alternatives without fake numeric precision or inherited historical order, accept exactly one current `NOW` direction under explicit human authority, and hand that accepted outcome to the existing Change-definition lifecycle without auto-creating work.

The planned "catch Planning Lite up to Poker" semantic sequence remains complete. During non-scored pilot preparation, `PREP-FINDING-001` showed that ordinary Copier update is unsafe when a consumer intentionally keeps `.planning/.agents` Git-ignored. `PL-V38-PREP-01` fixes that compatibility boundary. The corrective change is locally verified and published as remote pilot ref `pilot/pl-direction-002` at exact commit `c7a8cced0020e1e87e17f9567a5037fb44a1279f`. The repaired disposable preview, canonical local-only migration, Doctor/idempotence gates, deterministic Project Spine materialization, and final `PILOT_READY` validation have now all passed. The canonical scored fixture is local branch `planning/continuation-baseline` at metadata-only commit `920dad303f8750b5bc65b38f3bace4f72cb2819c`, whose scientific parent remains `f88a7fb...`. Scored Attempt 001 is now closed at a valid Branch-B reconciliation boundary: the agent detected stale durable provenance, performed fact-only `PROJECT_STATE_REFRESH`, preserved `RM-PKR-001`, created no Change, and changed no production code. The next operation is an owner-aware Attempt-002 readiness gate followed by a fresh scored Attempt 002 with the unchanged entry prompt. Field findings are consolidated in `REC-PL-DIRECTION-002-v1.md`; PL-V38-05+ remains stopped pending Attempt-002 reconciliation.

---

# 2. Current central source boundary

Released baseline:

```text
v4.3.0
0e66941d33e192938ab848e3c046699cf5ab92a2
```

Completed central preparation before PL-V38-01:

```text
0d7c923  campaign: reconcile legacy attempt suite evidence
0681b86  campaign: add strict attempt budget admission
57eb5bd  docs: record post-v4.3 campaign repairs
40ca8cf  docs: preserve Project Spine v3.8.2 design track
8d2026d  feat: add Project Spine direction foundation
782c785  test: make template SHA receipt EOL-stable
3306d7a  feat: add Project Spine current and gap foundation
61fe59a  feat: preserve recommendation semantic residue
PL-V38-04 commit: fafe133
PL-V38-PREP-01 local-only update safety: c7a8cced0020e1e87e17f9567a5037fb44a1279f
```

Verified local boundary before PL-V38-01:

```text
main HEAD: 40ca8cf95f983262e01d01a77cbad0d89d54002b
working tree clean
114/114 tests pass
v4.3.0 tag remains on 0e66941
no new release tag
```

PL-V38-00 and PL-V38-01..04 are complete. PL-V38-PREP-01 is complete at `c7a8cce` and locally verified, including the local-only v4.2.0 → current smoke. The exact candidate is published only on `pilot/pl-direction-002`; `origin/main` is intentionally not advanced by the pilot preparation. The repaired Poker migration/materialization reached `PILOT_READY: PASS`. Attempt 001 then produced a valid Branch-B reconciliation detour and closed without Change creation or production mutation. Attempt 002 is next after owner-aware readiness validation. Release remains unperformed; PL-V38-05 remains stopped pending scored field reconciliation.

---

# 3. Direction architecture remains unchanged

```text
TARGET STATE
    ↓
CAPABILITY MODEL
    ↓
CURRENT CAPABILITY ASSESSMENT
    ↓
CURRENT ↔ TARGET
    ↓
CAUSAL GAP MAP
    ↓
RECOMMENDATION + HISTORICAL ROADMAP RECONCILIATION
    ↓
CURRENT ROADMAP OUTCOMES
    ↓
DISCOVERIES / DECISIONS / GOVERNED CHANGE
    ↓
EVIDENCE
    ↓
RECONCILIATION
```

Field findings preserved from Poker:

- authority/freshness discovery before Target inference;
- deliverable class as an early Target variable;
- repository-clean != planning-consistent;
- explicit target/design/research question ownership;
- capability coverage != evidence confidence;
- causal Gap compression rather than symptom enumeration;
- Gap != RoadmapOutcome != Change;
- recommendation semantic residue and future-seed preservation;
- historical Roadmap order does not inherit current priority;
- stage-dependent context depth;
- research protocol completion != model result != production adoption;
- material direction decisions remain human-authority gates.

---

# 4. Product implementation route

## 4.1 Existing `control/*.md` is the first Playbook layer

Planning Lite already has authoritative workflow documents such as:

```text
PROJECT_BOOTSTRAP.md
CHANGE_DEFINITION.md
CHANGE_PLANNING.md
CHANGE_READINESS.md
CHANGE_CLOSURE.md
WAYFINDING.md
RECOMMENDATION_LIFECYCLE.md
```

They already encode applicability, reads, procedure, guards, write boundary, outputs and authorization.

Therefore:

```text
DO:
extend template/.planning/control with Direction workflows

DO NOT:
create a parallel PlaybookEngine first
```

## 4.2 Project-specific direction truth remains project-owned

Managed framework files define **how direction work is performed**.
Project-specific direction truth belongs in project-owned artifacts such as future:

```text
.planning/project/TARGET_STATE.md
.planning/project/CAPABILITY_MODEL.md
.planning/project/GAP_MAP.md
```

The first artifact boundary is now implemented: accepted Target/Capability truth is project-owned, Current Capability Assessment is a project-owned evidence snapshot under `assessments/current/`, and the causal Gap Map is project-owned durable direction truth.

## 4.3 Checklist extraction remains later

Released Planning Lite has embedded hard checks and per-change `requirements-checklist.md`, but not a mature central Checklist Control Plane.

First:

```text
stable inline Direction check IDs
```

Later, if repetition/eval evidence justifies it:

```text
first-class reusable checklist artifacts
```

## 4.4 Context Compiler remains experimental

No AgentWorkPacket/Context Compiler runtime is part of PL-V38-01..04.
Progressive context rules must prove their semantics first.

---

# 5. Research asset ownership and reuse

These assets are **development/research dependencies**, not runtime or installation dependencies of Planning Lite.
They must not be copied wholesale into consumer repositories.

## 5.1 Central Planning Lite repository

Owner of:

```text
released installer/template/runtime behavior
managed control workflows
project artifact templates
small deterministic validators
Campaign Core
central tests/docs/releases
```

## 5.2 `planning-lite-lab`

Role:

```text
research/evidence/governance control plane
```

Reuse for:

```text
source identity / hashing
fixture qualification receipts
controlled evidence manifests
experiment checkpoints
archive/relocation governance
Campaign/eval evidence lineage
```

Important current-state caveat:

```text
planning-lite-lab/state/CURRENT_STATE.md
is stale relative to the later closeout checkpoint
```

Authoritative reactivation source:

```text
checkpoints/2026-08-14-r3-closeout-budget-admission-validated/
```

That checkpoint records:

```text
R3 research complete
3/3 valid production-independent attempts
Campaign stopped at sequence 13
budget admission validated, not claimed released at checkpoint time
new Campaign unauthorized
Planning Lite work deferred until explicit resumption
```

Before the Lab is used for new v3.8 experiments, its compact current state must be reconciled from this checkpoint.
Do not rerun R3.

## 5.3 `planning_lite_tools`

Role:

```text
Context Pilot + Eval Harness lineage
```

Current reference candidate:

```text
step-16.4.1/
planning-lite-context-pilot-0.1.1-step-16.4.1
```

Relevant validated behavior includes:

```text
status snapshot / lifecycle fast path
stage-aware targeted context
safe insufficient-context deferral
least-privilege fallback
file-access observation
immutable raw evidence
balanced eval suites
routing vs resolution success separation
context-route verification
metrics / aggregation / pairwise reports
```

Recorded 16.4.1 evidence:

```text
36/36 routing success on reclassified immutable 16.4.0 evidence
routing-policy-ready
snapshot recommended for exact active/blocker cases
targeted-context recommended for incomplete/stale cases
124 unit/integration tests passed in the recorded distribution validation
```

### Historical tool versions

Older `16.1..16.4.0` and `*_old*` trees are **lineage/archive candidates**, not current product dependencies.

Do not delete them yet.
Before deletion or relocation:

```text
recursive manifest
→ dependency/lineage review
→ qualification receipt
→ archive under Lab if safe
```

The roadmap does not require keeping all versions as active working tools forever.

## 5.4 Poker

Role:

```text
real field source / controlled-realistic fixture source
```

Poker remains a consumer project, not a permanent Planning Lite test runtime.
Its Project Spine artifacts and CHG-0008 episode are fixture sources to be qualified later.

## 5.5 Campaign Core

Role:

```text
optional repeated-evidence governor
```

Campaign Core does not own Project Spine, Lab, or Context Pilot semantics.
Use it only after deterministic suites are stable and repeated runs are justified.

---

# 6. Current roadmap sequence

## COMPLETED — PL-V38-00

### Central working-tree reconciliation

Result:

```text
post-v4.3 Campaign repairs reconstructed and verified
88 EOL/BOM-only tracked changes excluded
central local main clean
114 tests pass locally
no Project Spine behavior implemented
```

---

## COMPLETED — PL-V38-01

### Direction foundation: authority inventory + Target/Capability contracts

Goal:

> replace the first manually-authored Poker direction prompts with managed Planning Lite workflows and durable project-owned direction artifacts.

Candidate managed workflows:

```text
DIRECTION_INVENTORY.md
TARGET_STATE_EXPLORER.md
TARGET_BASELINE_CALIBRATION.md
```

Candidate project-owned artifact/templates:

```text
TARGET_STATE.md
CAPABILITY_MODEL.md
```

Required semantics:

```text
direction authority + freshness classification
Current-State Consistency Gate
deliverable_class
Target claim provenance
Target status:
  DRAFT
  PROVISIONAL_TARGET_BASELINE
  ACCEPTED
question ownership:
  TARGET_BOUNDARY_QUESTION
  CAPABILITY_DESIGN_QUESTION
  RESEARCH_QUESTION
Target flow-back only through explicit authority / TARGET_STATE_SIGNAL
```

Explicit exclusions:

```text
Gap derivation
RecommendationUnit
Roadmap prioritization
Context Compiler
new Python Playbook runtime
Lab/Harness integration
new LLM campaign
```

The two external research assets remain reference material only at this stage.

Implemented product boundary:

```text
PW-DIR-001 DIRECTION_INVENTORY
PW-DIR-002 TARGET_STATE_EXPLORER
PW-DIR-003 TARGET_BASELINE_CALIBRATION
project-owned TARGET_STATE.md
project-owned CAPABILITY_MODEL.md
managed pristine copies
stage-specific context profiles
Doctor presence checks
```

No Gap/reconciliation/prioritization behavior is included.

---

## COMPLETED — PL-V38-02

### Current Capability Assessment + causal Gap Map

Implemented managed workflows:

```text
PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT [Audit]
PW-DIR-005 CAUSAL_GAP_DERIVATION [Planning]
```

Implemented artifact boundary:

```text
assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md
→ evidence snapshot created only when the Audit runs

project/GAP_MAP.md
→ durable project-owned causal direction truth
→ DRAFT / CURRENT_BASELINE
→ explicit user acceptance required for CURRENT_BASELINE
```

Core semantics implemented:

```text
Coverage:
  SATISFIED / PARTIAL / NOT_SATISFIED / UNCERTAIN

EvidenceConfidence:
  HIGH / MEDIUM / LOW

PARTIAL:
  satisfied target properties
  missing target properties
  evidence limitations

evidence limitation != automatic Gap
causal symptom compression
PRIMARY / DEPENDENT capability effects
SATISFIED capability cannot be silently reopened
outcome-oriented Gap closure condition
Change completion != Gap closure
Gap != RoadmapOutcome != Change
```

Broad recommendation/Roadmap history is now owned by PL-V38-03 rather than earlier Current/Gap stages.

---

## COMPLETE — PL-V38-03

### Recommendation semantic residue + historical direction reconciliation

Implemented:

```text
PW-DIR-006 RECOMMENDATION_HISTORY_RECONCILIATION [Planning]
stable REC-NNNN/Ux semantic-unit identity
unit state + primary lineage classification
lifecycle Status != reconciliation state
future-seed + carry-forward preservation
parent reconciliation states including OPEN
DIRECTION_HISTORY_RECONCILIATION assessment snapshot
historical Roadmap disposition ledger
orphan/overlap/residue audit
exact Source recommendation units on bounded Changes
```

Invariant:

```text
all original recommendation semantic units are accounted for
Change completion != Recommendation completion
historical Roadmap order != current priority
```

Compatibility rule: legacy/simple recommendations remain valid until unit-level reconciliation is actually needed. `CURRENT` reconciliation requires explicit user acceptance; the workflow does not rewrite canonical `ROADMAP.md`.

---

## COMPLETE — PL-V38-04

### Roadmap synthesis + qualitative prioritization + Change handoff

Implemented `PW-DIR-007 ROADMAP_SYNTHESIS_PRIORITIZATION` in the existing managed workflow layer.

Artifact split:

```text
assessments/current/ROADMAP_SYNTHESIS.md
→ DRAFT/CURRENT decision-evidence snapshot
→ candidate outcomes + alternatives + qualitative prioritization

project/ROADMAP.md
→ project-owned accepted current Roadmap truth
→ CURRENT_BASELINE requires explicit user acceptance
```

Implemented semantics:

```text
RoadmapOutcome != Gap != Change
one RoadmapOutcome may address several Gaps
Gap closure checks remain independent
historical Roadmap order != current priority
credible alternatives before preferred outcome
no weighted/fake numeric ranking by default
NOW / NEXT / unordered LATER / FINAL_GATE / DEFERRED
human acceptance before canonical Roadmap mutation
Change completion != RoadmapOutcome completion
Change completion != Gap closure
```

Roadmap synthesis normally consumes the accepted/current Spine plus the current direction-history reconciliation snapshot. Broad history is not reopened by default.

Research-heavy outcomes explicitly consider protocol-first composition. The workflow preserves `study_complete != production_integrated` and does not force production adoption after a successful study.

The accepted `NOW` outcome may be handed to existing `CHANGE_DEFINITION` **only on a later turn**. Change proposal lineage can now record the exact source Roadmap outcome, source Gaps, recommendation units, and whether the Change is a partial or outcome-completing contribution. No Change is auto-created by PW-DIR-007.

---

## COMPLETE CORRECTIVE GATE — PL-V38-PREP-01

**Local-only consumer update safety**

Triggered by `PILOT-PL-DIRECTION-002 / PREP-FINDING-001`, where a disposable Poker preview using ordinary Copier update lost 96 ignored managed files even though those files remained in the central template. The scored field attempt had not started.

Implemented contract:

```text
local-only managed roots detected
→ check = ownership-aware file plan, no writes
→ ordinary update = FAIL CLOSED
→ explicit update --local-only = atomic ownership-aware apply
→ project-owned existing files preserved byte-for-byte
→ unknown/unsafe ownership transition = STOP
```

Before the field gate can start, repeat the non-scored Poker migration preview and require:

```text
zero unintended managed removals
Doctor OK
project-owned hash preservation
idempotent second check
PILOT_READY receipt
```

## NEXT FIELD GATE — PILOT-PL-DIRECTION-002

### Poker continuation / next-Change derivation

Poker was intentionally frozen while PL-V38-01 through PL-V38-04 were implemented. PL-V38-PREP-01 and the repaired migration/materialization path passed. Attempt 001 then correctly failed closed on stale durable provenance and completed a fact-only `PROJECT_STATE_REFRESH`; the accepted Roadmap did not change. The primary handoff hypothesis therefore remains to be tested in Attempt 002 from the reconciled fixture. Before Attempt 002, readiness validation must follow authority ownership rather than require duplicate Git facts across planning artifacts or ban historical tokens globally.

Expected semantic test:

```text
CHG-0008 completed
RM-PKR-001 still NOW
GAP-PKR-002 open
GAP-PKR-003 open
protocol evidence exists
study implementation absent
→ derive the next bounded implementation Change
```

Failure modes to observe:

```text
repeating the protocol
premature Gap/Roadmap closure
returning to stale API priority
production integration before study evidence
over-broad implementation Change
unnecessary history reload
loss of completed-Change lineage
```

Field findings from this pilot must be reconciled before PL-V38-05/06/07 design is treated as stable. `REC-PL-DIRECTION-002-v1.md` is the active field-derived recommendation; its U6 bounded-handoff observation remains explicitly `TO_TEST` in Attempt 002.

---

## LATER — PL-V38-05

### Direction-aware context policy + visibility + ContextTrace

Extend existing `CONTEXT_POLICY.md` with workflow-stage depth profiles.

Reuse from Context Pilot 16.4.1 where semantically compatible:

```text
status/snapshot fast path concepts
least-privilege targeted context
safe insufficient-context deferral
file-access observation model
routing-vs-resolution distinction
```

Do **not** copy the Pilot wholesale into product runtime.

Add Planning Lite direction semantics:

```text
ACTIVE_DIRECTION
DEFERRED_VISIBLE
ARCHIVE_INDEXED
UNANCHORED_BACKLOG
ContextTrace
```

Expected output of this stage is still deterministic/progressive context policy, not a Context Compiler.

---

## LATER — PL-V38-06

### Research asset reactivation + qualified Poker eval suite

This stage has two bounded subphases.

### PL-V38-06A — Research asset reconciliation

`planning-lite-lab`:

```text
reconcile compact CURRENT_STATE from the 2026-08-14 closeout checkpoint
preserve R3 as terminal historical evidence
no R3 rerun
```

`planning_lite_tools`:

```text
qualify step-16.4.1 as current reference baseline
create recursive lineage/dependency manifest
classify older versions as archive-required / archive-safe / still-required
no deletion before receipt
```

### PL-V38-06B — Poker-derived fixture qualification

Create controlled-realistic fixtures with:

```text
CanonicalSourceBundle
ExpectedSemanticProjection
ScenarioOverlay only where needed
FixtureQualificationReceipt
source hashes
```

P0 cases:

```text
current-state consistency
target question ownership
coverage vs confidence
causal Gap compression
recommendation residue
historical priority override
Change completion != Gap closure
```

Use Lab for evidence governance and Eval Harness mechanisms where they fit.
Do not make Poker itself the permanent regression runtime.

---

## EXPERIMENTAL — PL-V38-07

### Context Compiler experiment

Comparator arms should reuse the validated measurement machinery rather than rebuilding a new harness:

```text
A raw canonical docs
B status snapshot
C snapshot + authoritative workflow
D Project Spine + workflow compiled AgentWorkPacket
```

Use/reconcile Context Pilot/Eval Harness concepts for:

```text
immutable run evidence
file reads
routing success
resolution success
safe deferral
retries/tokens/timing
balanced attempts
pairwise reports
```

Use Lab for qualification/provenance.
Use Campaign Core only if repeated governed evidence is needed after the deterministic suite is stable.

Promotion condition:

```text
non-inferior semantic/authorization correctness
+
material context-discipline improvement
```

Token reduction alone is insufficient.

---

## FINAL — PL-V38-08

### Safe direction bootstrap orchestration + release decision

Automate only proven deterministic/read-only transitions:

```text
inventory
→ consistency
→ target draft
→ target calibration
[HUMAN TARGET ACCEPTANCE]
→ current assessment
→ causal gaps
→ reconciliation
→ roadmap synthesis
[HUMAN DIRECTION ACCEPTANCE]
```

Existing governed Change lifecycle follows.

Never automate:

```text
Target acceptance
Roadmap acceptance
plan approval
execution authorization
closure authorization
semantic adjudication
destructive/promotion decisions
```

Regression requirement:

```text
small routine bugfix/docs work must remain lightweight
```

---

# 7. Relationship to Skill/Prompt architecture

Do not grow the root prompt and do not deploy the Poker mega-prompts verbatim.

Initial runtime routing remains:

```text
ROOT_ROUTER
→ MODE_ROUTER
→ one authoritative control workflow
→ optional discipline
```

The normalized Poker operator commands are tracked design evidence.
Their semantic rules should be localized into the matching managed workflow and loaded progressively.

A dedicated `planning-direction` skill remains optional and evidence-gated.

---

# 8. Anti-drift rules

The implementation has drifted if it starts to:

```text
build a graph database before typed lineage needs prove it
use embeddings before deterministic lineage routing is evaluated
create a large Python domain model duplicating Markdown state
create a second workflow engine beside control/*.md
copy planning-lite-lab into consumer installations
copy the whole Context Pilot into production without a bounded reuse decision
rerun completed R3 just to obtain new evidence
keep every historical tools version active forever
silently delete historical tools before lineage qualification
auto-accept Target/Roadmap changes
turn every PARTIAL capability into a Gap
turn every durable idea into current Roadmap work
auto-close Gap/Roadmap/Recommendation when a linked Change closes
build Context Compiler before Direction workflows pass fixtures
make small routine changes require full Project Spine bootstrap
```

---

# 9. Current disposition

```text
Project Spine semantics:
APPROVED FOR BOUNDED IMPLEMENTATION

Direction workflows:
IMPLEMENT THROUGH EXISTING control/*.md ARCHITECTURE FIRST

planning-lite-lab:
PRESERVE; REACTIVATE/RECONCILE AT PL-V38-06A

planning_lite_tools step-16.4.1:
PRESERVE AS CURRENT REFERENCE CANDIDATE; QUALIFY AT PL-V38-06A

older planning_lite_tools versions:
PRESERVE FOR NOW; ARCHIVE/DELETE ONLY AFTER LINEAGE RECEIPT

Recommendation residue:
IMPLEMENTED THROUGH PW-DIR-006 / PL-V38-03

Context routing:
REUSE VALIDATED PILOT IDEAS AT PL-V38-05, NOT WHOLESALE CODE COPY

Context Compiler:
EXPERIMENTAL / PL-V38-07

PL-V38-01:
IMPLEMENTED DIRECTION FOUNDATION

PL-V38-02:
IMPLEMENTED CURRENT CAPABILITY ASSESSMENT + CAUSAL GAP FOUNDATION

PL-V38-03:
IMPLEMENTED RECOMMENDATION SEMANTIC RESIDUE + HISTORICAL RECONCILIATION

PL-V38-04:
IMPLEMENTED ROADMAP SYNTHESIS + QUALITATIVE PRIORITIZATION + BOUNDED-CHANGE HANDOFF

Poker:
NEXT — PILOT-PL-DIRECTION-002 SCORED ATTEMPT 001 (FROZEN ENTRY PROMPT)

Planning Lite feature expansion:
STOP BEFORE PL-V38-05 UNTIL FIELD FINDINGS ARE RECONCILED
```
