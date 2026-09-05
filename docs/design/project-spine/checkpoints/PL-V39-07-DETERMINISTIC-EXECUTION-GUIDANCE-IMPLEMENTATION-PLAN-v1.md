# PL-V39-07 Deterministic Execution Guidance — Implementation Plan v1

## 1. Plan Identity and Authority Binding

- Change: `CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001`
- Plan status: `APPROVED_BY_OWNER`
- Prepared on: `2026-09-05`
- Execution baseline HEAD: `e6618cb974991a9e298615af3dec9a2467464ac0`
- Active lifecycle: `PLANNING_IN_PROGRESS`
- Implementation authorization: `NO`
- Formal Readiness: `NOT RUN`
- Implementation tasks: `NOT STARTED`

Owner Plan decision recorded by this governance step:

```text
OWNER_PLAN_DECISION: APPROVE
P-01: SEMANTIC_CLARIFICATION / APPLIED
P-02: SEMANTIC_CLARIFICATION / APPLIED
P-03: SEMANTIC_CLARIFICATION / APPLIED
P-04: SEMANTIC_CLARIFICATION / APPLIED
P-05: SEMANTIC_CLARIFICATION / APPLIED
```

Frozen scope authority:

```text
docs/design/project-spine/checkpoints/PL-V39-07-PROPOSED-CHANGE-DEFINITION-v1.md
SHA256 654c854311dc69a4444cc019aa50f49a18c86eeb5d01ac8225196c8c20a8e627
```

Activation authority:

```text
docs/design/project-spine/checkpoints/PL-V39-07-DEFINITION-ACTIVATION-v1.md
```

Bounded planning also used the frozen discovery artifact and the current
resume-contract block in `CURRENT.md`. The pre-plan dirty tree contained only
those three PL-V39-07 governance/shaping artifacts plus `CURRENT.md`; there was
no source, test, template, or unrelated dirt. This known planning state is not
an implementation candidate.

```text
DEFINITION_BINDING: PASS
scope change: NO
goal change: NO
AC count: 9 UNCHANGED
implementation_authorized: NO
```

## 2. Definition / AC Binding

The Plan implements the approved seam only:

```text
valid ResumeContextV1/current authority
+ finite existing managed guidance set
-> deterministic exact selection
-> one derived guidance result
   OR one explicit non-executing result
```

The four approved tightenings bind every implementation task:

1. candidates come only from a finite in-code mapping of fixed managed paths;
2. action class is derived only from an exact canonical action identity;
3. existing workflow, skill, discipline, gate, envelope, and evidence surfaces
   are reused; and
4. matched provenance is inspectable, derived, non-authoritative, and not
   persisted by default.

All nine approved ACs are implementable within this boundary. No AC is added,
removed, or weakened.

## 3. Existing Seam Findings

- `src/planning_lite/context.py::build_resume_context` already performs bounded,
  read-only authority selection, validates active/handoff identity and
  authorization non-elevation, applies path/root/reparse/forbidden-read guards,
  and returns the exact `ResumeContextV1` mapping. It must remain the only
  context builder.
- `src/planning_lite/cli.py::command_resume` is the existing operator seam for
  JSON/YAML resume output. Its default output and exit behavior are already
  tested.
- `CHANGE_EXECUTION.md` is the existing execution procedure and already owns
  authorization gates, Plan/task ordering, Execution Envelope, local blocker,
  verification, evidence, and stop behavior.
- `planning-execute/SKILL.md` is the existing thin execution skill. It routes to
  `EXECUTE.md`, `CHANGE_EXECUTION.md`, `ACTIVE.md`, active `context.md`, and
  `APPROVAL_GATES.md`; it does not authorize.
- `CONTRACT_CLOSURE.md` is the smallest existing conditional discipline that
  can prove a checklist-bearing pilot. It is applicable only when the approved
  action identity explicitly says contract closure is material.
- `requirements-checklist.md` is AC traceability, not a reusable execution
  checklist, and must not be repurposed.
- `STATE_OWNERSHIP.md` already classifies resume/ContextTrace as derived. It is
  the nearest policy surface for one concise clarification that execution
  guidance and provenance have the same non-authoritative/non-persistent role.
- Existing context, CLI, field-control/template, and central-resume tests own
  the nearest regression seams. Campaign Core, recommendation routing, and
  model/effort routing have different ownership and remain untouched.

## 4. Selected Architecture

```text
SELECTED_IMPLEMENTATION_SEAM:
one focused downstream module, src/planning_lite/execution_guidance.py,
which applies a pure selector to one existing ResumeContextV1 mapping;
existing planning-lite resume exposes it only via an opt-in flag
```

The invocation sequence is exact:

```text
one resume --guidance invocation
  -> build ResumeContext once
  -> preserve that exact mapping
  -> pure select_execution_guidance(ResumeContextV1)
  -> return resume + guidance wrapper
```

```text
GUIDANCE_INPUT_IDENTITY: SAME_RESUME_SNAPSHOT
```

The module is downstream of `context.py`; it never calls the context builder,
rescans the repository, reads history, or implements another path resolver.
Fixed managed pointers are emitted as references; the only dynamic path pointer
is the already validated `active_context_path` from ResumeContext. The existing
`ResumeContextV1` top-level and bootstrap schemas stay unchanged.

The default production candidate set is an immutable tuple/map in the focused
module. It contains one execution contract family and two exact action
bindings. There is no filesystem registry, configuration registry, discovery
walk, plugin scan, or decision log.

### Rejected alternatives

- **Extend `context.py` with routing:** rejected because bounded context
  acquisition and execution-procedure selection have different ownership; it
  would enlarge the exact PL-V39-06 contract and make later 08 evolution harder.
- **Template-only clarification:** rejected because prose cannot produce a
  deterministic inspectable ambiguity/no-match result for two implementers.
- **New top-level CLI command:** rejected because it would duplicate target,
  include, handoff, JSON/YAML, and read-only behavior already owned by `resume`.
- **General router/registry:** rejected as overbroad and as a second routing
  subsystem/state surface.

```text
PERSISTENT_NEW_REGISTRY_REQUIRED: NO
NEW_SKILL_REQUIRED: NO
NEW_CHECKLIST_REQUIRED: NO
```

## 5. CLI Decision

```text
CLI_DECISION:
extend the existing `planning-lite resume` parser with opt-in `--guidance`;
plain `planning-lite resume` remains byte/schema compatible
```

With `--guidance`, the command returns an exact wrapper containing the unchanged
resume result and one execution-guidance decision. JSON/YAML selection continues
to use the existing `--json` behavior. No file is written.

Exit behavior is explicit:

```text
MATCHED structured result                    -> 0
structured non-executing guidance outcome   -> 3
malformed invocation / existing CLI error   -> 2 (existing behavior)
plain resume without --guidance              -> existing behavior
```

Returning a structured non-match with a non-zero code prevents shell callers
from treating absence of legal guidance as permission to continue. The
structured body remains available for inspection.

## 6. Guidance Result and Failure Semantics

The exact JSON-compatible logical result is `ExecutionGuidanceV1`:

```text
schema_version: 1
outcome: MATCHED | NO_APPLICABLE_CONTRACT | AMBIGUOUS_ROUTE |
         NOT_AUTHORIZED | MISSING_OR_UNUSABLE_CONTEXT
reason_code: <finite exact value>
guidance: null | {
  guidance_id,
  action_class,
  procedure_ref,
  mode_ref,
  skill_ref,
  checklist_refs[],
  authorization_ref,
  precondition_refs[],
  scope_refs[],
  verification_refs[],
  stop_condition_refs[],
  evidence_ref,
  escalation_ref,
  next_gate_ref
}
provenance: {
  candidate_set_id,
  resume_schema_version,
  resume_status,
  source_revision,
  authority_refs[] {path, sha256},
  selection_reason
}
```

`guidance` is non-null only for `MATCHED`. Arrays preserve fixed declaration
order; duplicates are rejected/removed by construction; JSON uses the existing
sorted-key compact serializer. Authority references are a bounded subset of the
already selected ResumeContext sources, never loaded anew. `source_revision`
is copied as identity, not treated as approval.

Outcome/reason pairs use this finite precedence-ordered vocabulary:

| Condition | Outcome | `reason_code` |
|---|---|---|
| resume shape/schema is unusable | `MISSING_OR_UNUSABLE_CONTEXT` | `INVALID_RESUME_CONTEXT` |
| resume status is not `CURRENT` | `MISSING_OR_UNUSABLE_CONTEXT` | `RESUME_NOT_CURRENT` |
| active Change is absent | `MISSING_OR_UNUSABLE_CONTEXT` | `MISSING_ACTIVE_CHANGE` |
| active context pointer is absent | `MISSING_OR_UNUSABLE_CONTEXT` | `MISSING_ACTIVE_CONTEXT` |
| open blocker is present | `NOT_AUTHORIZED` | `OPEN_BLOCKER` |
| implementation authorization is not exactly true | `NOT_AUTHORIZED` | `IMPLEMENTATION_NOT_AUTHORIZED` |
| finite candidate-set integrity fails | `MISSING_OR_UNUSABLE_CONTEXT` | `INVALID_CANDIDATE_SET` |
| no exact action binding exists | `NO_APPLICABLE_CONTRACT` | `UNMAPPED_ACTION` |
| multiple exact bindings exist | `AMBIGUOUS_ROUTE` | `MULTIPLE_EXACT_BINDINGS` |
| one exact legal binding exists | `MATCHED` | `EXACT_ACTION_BINDING` |

Fields are classified as follows:

| Class | Fields | Owner |
|---|---|---|
| identities/pointers | guidance/action IDs; workflow/mode/skill/checklist/gate/envelope/evidence/escalation refs | finite managed mapping and existing managed files |
| derived projections | outcome, reason, active context scope pointer, next-gate pointer, source revision, bounded source hashes, selection reason | current invocation only |
| small fixed guidance metadata | candidate-set identity and ordered reference lists | focused module |
| authority not copied | approval, authorized task/scope contents, Plan, Execution Envelope body, workflow/checklist body, task status | `ACTIVE`, approved Plan, active context, existing workflow/evidence files |

The result is never accepted as handoff/current-state input and no CLI/API writes
it. Supplying prior provenance cannot change the authorization value produced by
`build_resume_context` or satisfy a missing authority prerequisite.

`authority_refs` are only hashes and identities already present in the exact
ResumeContext snapshot. Procedure/mode/skill/checklist references are guidance
pointers, not authority provenance. Route-time hashing or reading of those
guidance files is forbidden:

```text
PROVENANCE_EXTRA_FILE_READS: NONE
```

`next_gate_ref` is only a pointer to the existing gate authority. It is not a
predicted lifecycle state, newly asserted next action, or route-owned
transition. The selector never parses unrelated Plan/history content to infer a
future gate.

## 7. Deterministic Precedence

The selector evaluates in this exact order:

1. resume object/schema/bootstrap required facts invalid, resume status other
   than `CURRENT`, active Change absent, or active context pointer absent ->
   `MISSING_OR_UNUSABLE_CONTEXT`, using the first reason in the §6 table;
2. open blocker present or implementation authorization not exactly `true` ->
   `NOT_AUTHORIZED`, with blocker taking precedence over the flag;
3. default candidate set fails its fixed bound/schema/integrity check ->
   `MISSING_OR_UNUSABLE_CONTEXT`;
4. zero exact action bindings -> `NO_APPLICABLE_CONTRACT`;
5. more than one materially valid exact binding -> `AMBIGUOUS_ROUTE`;
6. exactly one binding with all fixed references -> `MATCHED`.

The first applicable outcome is final. No later condition upgrades it. Stale,
superseded, or missing owner evidence therefore outranks a superficially true
authorization flag; absent authorization outranks skill availability; and no
candidate or ambiguity can be repaired heuristically.

## 8. Candidate Set and Exact Classification Contract

```text
CANDIDATE_SET_MECHANISM:
one immutable finite ordered tuple of managed bindings in
execution_guidance.py; duplicate identities are validated before lookup;
no disk discovery and no persisted registry

ACTION_CLASS_MAPPING:
FINITE_EXACT
```

The initial mapping is deliberately a two-binding pilot. The exact action
identities are values of the existing canonical `next_permitted_action` field;
they are not a new action-state authority and are never derived from free
prose:

| Exact canonical `next_permitted_action` | Derived action class | Guidance family | Existing checklist/discipline |
|---|---|---|---|
| `EXECUTE_AUTHORIZED_TASK` | `EXECUTE_CHANGE_TASK` | `CHANGE_EXECUTION_V1` | `NONE` |
| `EXECUTE_AUTHORIZED_CONTRACT_TASK` | `EXECUTE_CONTRACT_CLOSURE_TASK` | `CHANGE_EXECUTION_V1` | `.planning/disciplines/CONTRACT_CLOSURE.md` |

Both bindings reference:

```text
procedure: .planning/control/CHANGE_EXECUTION.md
mode: .planning/modes/EXECUTE.md
skill: .planning/skills/planning-execute/SKILL.md
authorization: .planning/control/APPROVAL_GATES.md
scope/verification: <validated active_context_path>#Execution Envelope
stops: .planning/control/CHANGE_EXECUTION.md
escalation: .planning/control/CHANGE_AMENDMENT.md
evidence: sibling progress.md under the validated active Change folder
next gate: .planning/ACTIVE.md#Active change
```

`CHANGE_EXECUTION.md` receives a bounded producer clarification for these two
optional canonical action identities. The contract-closure identity is legal
only when the approved Plan explicitly makes the existing discipline material;
otherwise the ordinary identity with `checklist_refs=[]` is used. Other existing
human next-action text remains legal lifecycle text but intentionally returns
`NO_APPLICABLE_CONTRACT` from this minimum pilot.

The producer clarification does not turn `CHANGE_EXECUTION.md` into current
state. It only documents how an existing lifecycle producer may emit the exact
value already owned by `next_permitted_action`.

Comparison is exact Unicode string equality after the existing markdown-value
cleanup performed by ResumeContext. There is no case folding, prefix/substring
match, regex, tokenization, edit distance, alias, fuzzy/semantic/model fallback,
or best match.

The production candidate set cannot be supplied through CLI, config, handoff,
provenance, or repository contents. A private bounded test seam may inject a
candidate tuple of at most eight entries solely to prove ambiguity and
candidate-integrity behavior; the public builder always uses the immutable
two-entry default. Duplicate exact action identities are detected while still
in the ordered tuple, before any dictionary/index construction. A non-tuple or
a tuple above that test bound is invalid.

## 9. Authority, Skill, Checklist, Path, and Provenance Boundary

- `MATCHED` reports that the current authoritative input passed the finite rule;
  it is not a durable permission token. `ACTIVE` and explicit owner authority
  remain controlling at the moment of execution.
- The `planning-execute` skill supplies procedure routing only. Presence of the
  skill never affects authorization precedence.
- `CONTRACT_CLOSURE.md` is reused as the only checklist-bearing pilot; no new
  skill/checklist artifact or corpus is created.
- The ordinary matched route proves that `checklist_refs=[]` is a valid exact
  result rather than an omitted decision.
- Fixed references are repository-relative literals under `.planning/`.
  Dynamic active-context/evidence pointers are derived only from
  ResumeContext's already root-contained, no-glob, no-parent, no-reparse-safe
  path. The selector performs no additional file read.
- A missing required active-context pointer fails before matching. No path is
  searched, guessed, recursively expanded, or taken from history.
- Provenance contains only bounded identities/hashes already emitted by resume.
  It is returned in memory/stdout, is not written, and is not accepted as
  current state, authorization, candidate configuration, or a future input.

## 10. Planned Write Surface

Ten implementation/evidence paths are permitted after later Readiness and
Execution authorization. The current Plan artifact is not counted as an
implementation path.

| Path | Class | Planned responsibility |
|---|---|---|
| `src/planning_lite/execution_guidance.py` | `RUNTIME` | new focused finite model, selector, precedence, provenance, and read-only builder |
| `src/planning_lite/cli.py` | `CLI` | opt-in `resume --guidance` wrapper and exit behavior; plain resume unchanged |
| `template/.planning/control/CHANGE_EXECUTION.md` | `MANAGED_TEMPLATE_POLICY` | document the two exact optional producer identities and existing-surface binding |
| `template/.planning/control/STATE_OWNERSHIP.md` | `MANAGED_TEMPLATE_POLICY` | classify guidance/provenance as derived, non-authoritative, non-persistent |
| `template/.planning/framework/SHA256SUMS.txt` | `MANAGED_TEMPLATE_POLICY` | regenerate managed template hashes |
| `tests/test_execution_guidance.py` | `TEST` | focused model, selection, precedence, provenance, path, and consumer-shape cases |
| `tests/test_cli.py` | `TEST` | parser, output wrapper, exit codes, plain-resume compatibility, read-only behavior |
| `tests/test_field_control_pack_foundation.py` | `TEST` | policy/ownership boundary, existing skill/discipline reuse, no new universal router/skill/checklist |
| `docs/design/project-spine/checkpoints/PL-V39-07-EXECUTION-LEDGER-v1.md` | `GOVERNANCE_EVIDENCE` | one cumulative T-01…T-08 record |
| `docs/design/project-spine/checkpoints/PL-V39-07-COMPLETION-REVIEW-v1.md` | `GOVERNANCE_EVIDENCE` | T-09 final review only |

Why the new runtime file is smaller than extending `context.py`: it keeps the
frozen resume schema and authority/read-selection responsibility unchanged,
has one-way dependency on resume, contains the finite candidate table in one
inspectable place, and can be removed or evolved during PL-V39-08 without
rewriting context acquisition.

Explicitly unchanged: `context.py`, `ROOT_ROUTER.md`, `MODE_ROUTER.md`, skills,
checklist/discipline bodies, lifecycle/gates, change templates, `copier.yml`,
`OWNERSHIP.yml`, product registry/update/Doctor/Campaign code, operator docs,
Roadmap, live consumers, and release files. No unrelated refactor or broad
router/lifecycle/skill/checklist rewrite is permitted.

If implementation requires any unlisted path or changes `ResumeContextV1`, the
affected task stops for amendment/adjudication.

## 11. Task Graph

### T-01 — Exact result contract and failure precedence

- Outcome: implement the closed `ExecutionGuidanceV1` shape, finite outcomes,
  reason codes, candidate bounds, and precedence skeleton; keep the selector
  pure over one preserved ResumeContext snapshot.
- Dependencies: approved Plan, planning-authority checkpoint, Formal Readiness
  `READY`, and separate owner Execution authorization.
- Write surface: `execution_guidance.py`, focused tests, cumulative ledger.
- Verification seam: canonical-positive exact shape; unknown/extra/malformed
  internal candidate definitions rejected; each first-applicable failure wins.
- Stop: any need to mutate ResumeContext schema or persist a result.

### T-02 — Finite candidate set and exact action mapping

- Outcome: implement the one-family/two-action immutable map and exact equality
  semantics; zero, one, and injected-two candidate behavior is deterministic.
- Dependencies: T-01 PASS.
- Write surface: `execution_guidance.py`, focused tests, ledger.
- Verification seam: both exact identities match their declared projection;
  case/prefix/suffix/whitespace alias/unknown values do not; candidate outside
  the fixed set cannot enter production.
- Stop: a registry, scan, regex/fuzzy/semantic interpretation, or configuration
  candidate source becomes necessary.

### T-03 — Selector, authorization guard, and bounded provenance

- Outcome: bind one preserved resume snapshot to the finite map, implement
  precedence, fixed/dynamic references, and bounded provenance without new
  reads or a second context construction.
- Dependencies: T-02 PASS.
- Write surface: `execution_guidance.py`, focused tests, ledger.
- Verification seam: authorized exact match; absent auth, stale/superseded/
  missing context, open blocker, no match, ambiguity, and forged prior
  provenance all remain non-executing; repeated input is byte-equivalent; the
  returned resume and guidance contain the same source revision/authority
  identities.
- Stop: path discovery, Plan/envelope body copying, or a new authority source is
  required.

### T-04 — Existing procedure/skill/checklist producer contract

- Outcome: add only the exact action-identity producer clarification to
  `CHANGE_EXECUTION.md`, clarify derived ownership, regenerate SHA receipts,
  and prove no new skill/checklist/router/mode/lifecycle surface was added.
- Dependencies: T-02 PASS; may proceed independently of T-03.
- Write surface: the three listed managed/integrity files, foundation test,
  ledger.
- Verification seam: contract route selects existing `planning-execute` and
  `CONTRACT_CLOSURE`; ordinary route has explicit empty checklist; template
  manifest coverage remains unchanged and hash/ownership integrity passes.
- Stop: existing surfaces cannot express the pilot without a new artifact or
  taxonomy.

### T-05 — Opt-in resume CLI integration

- Outcome: expose the public builder through `resume --guidance` with exact
  wrapper and exit semantics while preserving plain resume.
- Dependencies: T-03 PASS and T-04 PASS.
- Write surface: `cli.py`, `test_cli.py`, focused test file, ledger.
- Verification seam: JSON/YAML matched and non-matched outputs; exit `0/3/2`;
  plain resume output equivalence; no target/home/status mutation.
- Stop: a new command or writable operational state is required.

### T-06 — Central integration and candidate verification

- Outcome: run the complete bounded central evidence stack, audit exact paths,
  and establish a reviewable implementation tree.
- Dependencies: T-01…T-05 PASS.
- Write surface: cumulative ledger only; verification may regenerate only the
  already-listed SHA receipt file if its deterministic check requires it.
- Verification seam: focused tests, resume regression, template/foundation
  integrity, full suite, clean temporary adoption + Doctor, read-only and scope
  audit, `git diff --check`.
- Stop: any regression, unexpected path, semantic routing, authority leak, or
  manifest mismatch.

### Central Implementation Candidate Review Gate

After T-06, stop. Independent/bounded review must find no material defect. A
separate owner authorization is required before a checkpoint commit. Only that
commit creates the clean central implementation candidate used by T-07/T-08.

### T-07 — Mature Poker-shaped disposable proof

- Outcome: on the exact committed candidate, create a disposable mature fixture
  with an active authorized task and exact contract-closure action; prove one
  bounded match, existing procedure/skill/discipline binding, preserved
  envelope/stops/next-gate references, no history scan, and read-only behavior.
- Dependencies: clean committed central candidate and separate owner
  authorization for disposable proofs.
- Write surface: disposable temp directory plus cumulative ledger; live Poker
  has no write surface.
- Verification seam: targeted Poker-shaped test/proof plus before/after fixture
  Git status and file hashes.
- Stop: proof needs live migration, live control-home placement, or a source
  change after the candidate commit.

### T-08 — Early mood-shaped disposable proof

- Outcome: on the same committed candidate, create an early/unborn fixture with
  no active implementation/authorization; prove the deterministic safe
  non-executing outcome and absence of invented Change/skill/procedure.
- Dependencies: same gate as T-07; independent of T-07 once candidate exists.
- Write surface: disposable temp directory plus cumulative ledger; live mood has
  no write surface.
- Verification seam: targeted mood-shaped test/proof, exit code, output, and
  before/after filesystem/Git evidence.
- Stop: the route matches, any state is written, or live consumer access becomes
  necessary.

### T-09 — Completion Review

- Outcome: independently reconcile implementation and field evidence against
  all nine ACs, both review passes, Definition/Plan drift, candidate identity,
  scope, and 07/08/09 exclusions.
- Dependencies: T-01…T-08 PASS and no open material finding.
- Write surface: `PL-V39-07-COMPLETION-REVIEW-v1.md` only, plus final ledger
  status update if required by the existing lifecycle.
- Verification seam: AC 9/9 matrix, spec/standards conformance, exact candidate
  SHA, live-consumer unchanged evidence, and no persistent new authority.
- Stop: any AC lacks direct evidence or source differs from the proven candidate.

## 12. Acceptance Criteria Traceability

| AC | Implementation seam | Primary discriminators | Tasks |
|---|---|---|---|
| AC-01 | downstream pure selector consuming one unchanged ResumeContext snapshot | one invocation/build; plain resume unchanged; no scan/read/write; stale/missing context | T-01, T-03, T-05, T-06 |
| AC-02 | immutable candidate/action map and exact result | repeated byte-equivalent match; exact case; zero/two matches; provenance | T-01, T-02, T-03 |
| AC-03 | fixed precedence using current resume authorization | same route auth true/false; blocker; stale/contradictory handoff; skill present without auth | T-01, T-03, T-05 |
| AC-04 | one referenced `CHANGE_EXECUTION_V1` projection | all procedure/scope/check/stop/evidence/escalation refs present; `next_gate_ref` points to existing authority and does not predict transition; no bodies copied | T-03, T-04 |
| AC-05 | four non-executing outcomes and exact exit behavior | no match, ambiguity, missing/unusable, unknown action, candidate outside set | T-01, T-02, T-03, T-05 |
| AC-06 | existing `planning-execute` plus conditional `CONTRACT_CLOSURE` | contract action selects discipline; ordinary action returns checklist `[]`; auth remains external | T-02, T-04, T-07 |
| AC-07 | existing resume/CLI/policy/evidence surfaces | no new registry/skill/checklist/router; one ledger + one review; scope audit | T-04, T-05, T-06, T-09 |
| AC-08 | two disposable fixtures on committed candidate | mature exact match and early non-execution; read-only; live repos unchanged | T-07, T-08 |
| AC-09 | fixed-map and structural exclusion tests/review | no scoring/learning/semantic/model routing/Campaign/orchestration/release/compiler paths | T-04, T-06, T-09 |

```text
AC_PLAN_COVERAGE: 9/9
orphan tasks: NONE
implementation task after T-09: NONE
```

## 13. Verification Strategy

### Focused model / route / CLI

```text
uv run --frozen pytest tests/test_execution_guidance.py tests/test_cli.py -rA
```

Required named test groups cover:

- `MATCHED` authorized exact route;
- same route without authorization;
- zero/two routes and candidate-bound failure;
- stale, superseded, missing, blocked, malformed, and contradictory context;
- exact-only action mapping and unknown action;
- checklist present versus explicit empty list;
- stable ordered provenance and no provenance feedback;
- fixed repo-relative pointers and safe dynamic active-context reference; and
- JSON/YAML wrapper, `0/3/2` exits, no writes, and plain resume compatibility.

### PL-V39-06 resume regression

```text
uv run --frozen pytest tests/test_context_resume.py tests/test_central_resume_contract.py -rA
```

No 06 schema change is expected. Existing determinism, bounded sources, path
safety, freshness, handoff non-elevation, and central-resume behavior must pass.

### Managed template / foundation integrity

```text
uv run --frozen pytest tests/test_field_control_pack_foundation.py tests/test_template.py -rA
```

The tests must prove exact producer identities, derived ownership, existing
skill/discipline references, no new universal mode/skill/checklist/router, and
manifest/SHA coverage of the entire template tree.

### Central candidate integration

```text
uv sync
uv run --frozen pytest
git diff --check
git status --short --untracked-files=all
```

Then adopt the exact candidate template into a temporary clean Git repository
and run `planning-lite doctor` there. The adoption/Doctor probe must use the
same checked candidate source and leave no unexplained generated path. Update
behavior is not changed, so a two-tag update migration is not required by this
Change unless implementation drift touches update/ownership behavior.

### Nearest-wrong matrix

| Case | Expected primary outcome |
|---|---|
| authorized exact ordinary route | `MATCHED`, checklist `[]` |
| authorized exact contract route | `MATCHED`, existing Contract Closure ref |
| same otherwise valid route without authorization | `NOT_AUTHORIZED` |
| valid current context with unmapped action | `NO_APPLICABLE_CONTRACT` |
| case/prefix/suffix/fuzzy near-match | `NO_APPLICABLE_CONTRACT` |
| two injected materially valid exact bindings | `AMBIGUOUS_ROUTE` |
| missing/malformed/stale/superseded resume authority | `MISSING_OR_UNUSABLE_CONTEXT` |
| open blocker with otherwise valid route | `NOT_AUTHORIZED` |
| skill files present but authorization false | `NOT_AUTHORIZED` |
| candidate not in immutable production set | `NO_APPLICABLE_CONTRACT` |
| candidate set malformed or exceeds fixed bound | `MISSING_OR_UNUSABLE_CONTEXT` |
| prior matched provenance supplied as handoff/authority | rejected by existing exact handoff/current authority contract |

No test asserts help prose, formatting trivia, pytest rendering, or other
non-contractual presentation text.

## 14. Consumer Proof Strategy

T-07 and T-08 run only after a separately authorized clean committed central
candidate. Their reusable assertions may live in `test_execution_guidance.py`,
but the formal proof reruns against disposable repositories created for the
gate and records exact candidate SHA, commands, output, hashes/status, and
cleanup disposition in the single ledger.

The Poker-shaped fixture includes many irrelevant completed/evidence files to
prove no history/corpus discovery, but only the ResumeContext-bounded sources
participate. It uses `EXECUTE_AUTHORIZED_CONTRACT_TASK`, current authorization,
an active context pointer, and the existing Contract Closure discipline.

The mood-shaped fixture is unborn/minimal with no active Change and no
authorization. It must return the precedence-defined non-executing result and
must not create or select a Change, procedure, skill, checklist, registry, home,
or control repository.

`D:\documents\poker` and `D:\documents\mood` remain outside every write surface.
No live read is necessary unless a later proof authorization explicitly asks
for a before/after unchanged check.

## 15. Gate / Checkpoint Topology

```text
Plan PREPARED
-> owner Plan review/approval
-> separate owner-authorized PLANNING AUTHORITY CHECKPOINT
-> read-only Formal Readiness
-> separate owner Execution authorization
-> T-01…T-06 central implementation and verification
-> CENTRAL IMPLEMENTATION CANDIDATE REVIEW GATE
-> separate owner checkpoint-commit authorization
-> clean committed central implementation candidate
-> separate owner authorization for disposable proofs
-> T-07 / T-08
-> T-09 Completion Review
-> separate owner closure decision
```

The planning-authority checkpoint binds approved Definition, activation,
`CURRENT`, approved Plan, and required governance surfaces. It is not an
implementation candidate. Formal Readiness requires that bound authority but
must not require a pre-existing clean committed implementation candidate.

The central candidate gate requires T-01…T-06 PASS, focused and full regression
PASS, template adoption/Doctor PASS, scope and `git diff --check` PASS,
independent/bounded review with no material finding, and separate owner
authorization before commit. T-07/T-08 cannot run from an uncommitted or dirty
central source.

```text
Plan approval != implementation authorization
Formal Readiness READY != implementation authorization
```

## 16. Deferred / Routed Work

PL-V39-08 retains quality scoring, eval-system extraction, success metrics,
learning, adaptive/semantic/model routing, PromptOps, optimization, and
evidence-backed scale-out beyond this two-action pilot.

PL-V39-09/later retains production Context Compiler, multi-agent orchestration,
delegation, scheduling, automatic workflow/release chaining, and release
orchestration. Recommendation automation, embeddings/RAG/vector retrieval,
Campaign Core generalization, skill analytics, live Poker/mood migration, and
external control-home placement remain outside the Change.

## 17. Risks and Stop Conditions

Stop the affected task and use the existing amendment/adjudication path if:

- the Definition hash or active Change/current authority drifts;
- any implementation requires changing `ResumeContextV1` or accepting a
  caller-supplied authority/guidance decision;
- exact action identities cannot be produced without semantic/fuzzy/model
  interpretation;
- a registry, discovery scan, persistent decision/provenance log, new skill,
  new checklist, new lifecycle/router/mode, or unlisted path becomes necessary;
- the selected result would copy Plan/Envelope/workflow/checklist bodies or
  broaden authorization/write scope;
- a failure condition cannot obey the frozen precedence;
- template integrity requires update/ownership semantics outside the listed SHA
  regeneration and unchanged-manifest verification;
- full/focused verification or disposable proof finds a material regression;
- live Poker/mood mutation, production Context Compiler, Campaign,
  recommendation, evaluation/learning, orchestration, or release responsibility
  becomes necessary; or
- any source differs after the committed candidate used for T-07/T-08.

## 18. Owner Plan Review Gate

```text
PL_V39_07_IMPLEMENTATION_PLAN: APPROVED_BY_OWNER
Plan status: APPROVED_BY_OWNER
OWNER_PLAN_DECISION: APPROVE
Plan tightenings: 5/5 APPLIED / SEMANTIC_CLARIFICATION
AC_PLAN_COVERAGE: 9/9
task count: 9
planning authority checkpoint: NOT AUTHORIZED / NOT PERFORMED
Formal Readiness: NOT RUN
implementation_authorized: NO
T-01…T-09: NOT STARTED
next owner gate: OWNER_AUTHORIZATION_PL_V39_07_PLANNING_AUTHORITY_CHECKPOINT
```

Owner approval of this Plan would not authorize implementation. A later
owner-authorized planning checkpoint, separate read-only Formal Readiness, and
separate owner Execution authorization remain required.
