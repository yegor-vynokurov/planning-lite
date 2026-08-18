# Planning Lite Roadmap v3.8.2 — Project Spine + research-asset reuse alignment

**Status:** Current implementation-facing design roadmap
**Date:** 2026-08-18
**Parent:** Planning Lite Roadmap v3.8 / un-applied v3.8.1 alignment draft
**Evidence:** Poker Project Spine pilot + W0 architecture inspection + PL-V38-00 reconciliation + review of `planning-lite-lab` and `planning_lite_tools`

---

# 1. Why v3.8.2 exists

v3.8 promoted Project Spine from a field-pilot hypothesis to a bounded implementation candidate.
W0 then established that Planning Lite is **template/workflow-first**, not Python-domain-model-first.

A second asset review found two existing research systems that overlap directly with later v3.8 work:

```text
planning-lite-lab
→ research/evidence/governance control plane

planning_lite_tools / step-16.4.1
→ Context Pilot + Eval Harness reference implementation
```

The earlier v3.8.1 design package was never applied to the central repository.
This v3.8.2 document supersedes that package and folds both corrections into one current roadmap.

The semantic direction is unchanged. The implementation and reuse boundaries are now explicit.

---

# 2. Current central source boundary

Released baseline:

```text
v4.3.0
0e66941d33e192938ab848e3c046699cf5ab92a2
```

Completed local reconciliation:

```text
0d7c923  campaign: reconcile legacy attempt suite evidence
0681b86  campaign: add strict attempt budget admission
57eb5bd  docs: record post-v4.3 campaign repairs
```

Verified local state after PL-V38-00:

```text
main HEAD: 57eb5bd797fd96269bc6a4a03eef70c2f893a4b5
main ahead of origin/main by 3
working tree clean
114/114 tests pass
v4.3.0 tag remains on 0e66941
no new release tag
```

PL-V38-00 is a completed prerequisite reconciliation, not Project Spine implementation.

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
ROADMAP OUTCOMES
    ↓
RECOMMENDATIONS / DISCOVERIES / DECISIONS
    ↓
GOVERNED CHANGE
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

The exact minimal artifact set remains a bounded PL-V38-01/02 design decision.

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

## NOW — PL-V38-01

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

The two external research assets are reference material only at this stage.

---

## NEXT — PL-V38-02

### Current Capability Assessment + causal Gap Map

Add managed workflows for:

```text
CURRENT_CAPABILITY_ASSESSMENT
CAUSAL_GAP_DERIVATION
```

Core semantics:

```text
Coverage:
  SATISFIED / PARTIAL / NOT_SATISFIED / UNCERTAIN

EvidenceConfidence:
  HIGH / MEDIUM / LOW

PARTIAL:
  satisfied target properties
  missing target properties
  evidence limitations

Gap:
  missing Target property
  causal consolidation
  PRIMARY / DEPENDENT capability effect
  outcome-oriented closure condition
```

No broad recommendation/history reads by default.

---

## NEXT — PL-V38-03

### Recommendation semantic residue + historical direction reconciliation

Extend `RECOMMENDATION_LIFECYCLE.md` rather than replacing it.

Add semantic-unit accounting, future seeds, carry-forward and parent reconciliation states.

Invariant:

```text
all original recommendation semantic units are accounted for
```

This is the workflow stage where broad recommendation/Roadmap history is intentionally allowed.

---

## NEXT — PL-V38-04

### Roadmap synthesis + qualitative prioritization

Produce a compact outcome-oriented direction proposal.

Support:

```text
one RoadmapOutcome → several Gap refs
```

while keeping independent Gap closure identities.

Require:

```text
credible-alternative comparison
no inherited historical priority
human direction acceptance
protocol-first composition for research-heavy outcomes
```

No automatic Change creation before acceptance.

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
APPROVED FOR PL-V38-03

Context routing:
REUSE VALIDATED PILOT IDEAS AT PL-V38-05, NOT WHOLESALE CODE COPY

Context Compiler:
EXPERIMENTAL / PL-V38-07

PL-V38-01:
CURRENT NEXT IMPLEMENTATION CANDIDATE
```
