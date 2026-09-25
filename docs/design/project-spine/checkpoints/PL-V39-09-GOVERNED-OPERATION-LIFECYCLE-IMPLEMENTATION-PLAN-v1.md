# PL09 Governed Operation Lifecycle ? Implementation Plan v1

```text
TITLE: PL09 Governed Operation Lifecycle ? Implementation Plan v1
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
PLAN_STATUS: APPROVED_BY_OWNER
OWNER_PLAN_DECISION: APPROVE
SOURCE_CANDIDATE_PATH: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLAN_CANDIDATE.md
SOURCE_CANDIDATE_ORDINARY_SHA256: 970A168A158D1F3157A4860CA41646583626E3788A5E122429CAC887AC895A60
SOURCE_CANDIDATE_SELF_EXCLUDING_SHA256: 3217928FAE90E271B652395E832B7DFD6C48ECA09C0A6581DF80F54127009AFE
APPROVING_REVIEW_PATH: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_TARGETED_CONVERGENCE_REPAIR_FRESH_REVIEW.md
APPROVING_REVIEW_SHA256: BCF8E4FE2DCFBADAA4BB300D94D5981D1793DE6F4E4EECC7DC3D2DFB2EBB2FD8
APPROVING_REVIEW_VERDICT: PASS_INDEPENDENT_GOVERNED_OPERATION_LIFECYCLE_TARGETED_CONVERGENCE_REPAIR
FORMAL_READINESS: NOT_RUN
IMPLEMENTATION_AUTHORIZED: NO
```

The Plan below is the normative technical Plan body materialized from the
independently reviewed candidate. Candidate-only repair receipts and internal
review narration are not current Plan authority and are omitted here.

## 2. Live fact ledger captured before editing

The following facts were read from the entry checkout before this file was
rewritten. They are the binding facts for the plan; any later implementation
must rerun the listed checks and stop on drift.

| Surface | Live fact | Consequence frozen here |
|---|---|---|
| `src/planning_lite/execution_guidance.py` | `OperationGuidanceV1` has top-level keys `schema_version`, `outcome`, `reason_code`, `operation`, `authority`, `capabilities`, `guidance`, `provenance` | The envelope consumes the complete mapping, not a hand-picked subset |
| Successful implementation guidance | top-level `outcome=MATCHED`, top-level `reason_code=EXACT_OPERATION_BINDING` | The reason code is not the predicate result |
| Nested guidance predicate | `authority.predicate_result=AUTHORIZED_FOR_THIS_OPERATION` | Predicate authorization remains nested and distinct |
| Guidance serializer | `json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))` | The guidance digest uses the live serializer byte-for-byte |
| Guidance nested collections | guidance has 15 keys; provenance has 6 keys; authority has 3 keys; capabilities has 8 entries | Every scalar, mapping, and array is included in the digest vector |
| `src/planning_lite/attempt_evaluation.py` | `evaluate_technical` has 3 required positional-or-keyword parameters, 2 required keyword-only parameters, 6 optional parameters, 11 total parameters | Lifecycle supplies all 11 named carriers explicitly; no signature-count shortcut is used |
| `ObservedResultV1` | exactly `result_id`, `attempt_id`, `execution_status`, `changed_paths`, `fact_refs`, `artifact_refs` | Receipt, supersession, evaluation, and freshness are separate carriers |
| `src/planning_lite/attempt_runtime.py` | `load_attempt_store` exists and returns `AttemptStoreV1`; Attempt records carry observed-result and verifier references but no telemetry receipt field | Runtime remains the state owner; status cannot promise a missing receipt field |
| `src/planning_lite/telemetry.py` | `collect_governed_receipt` validates, injects identities, persists, and reads back one supplied receipt | Lifecycle calls this owner once and consumes its exact readback |
| `src/planning_lite/cli.py` | `adopt` supports `--template-source`, `--vcs-ref`, `--agent`, and `--allow-dirty`; target cleanliness is enforced unless explicitly allowed | V-24 uses a disposable committed source snapshot, not the dirty central checkout |
| Entry test tree | `tests/test_governed_executor.py` and `tests/test_operation_lifecycle.py` are absent; the other four authorized test paths exist | T-02 creates all future files and named nodes before later tasks read them |
| Current test ownership | `tests/test_run_receipts.py` already contains receipt collector coverage | New lifecycle receipt nodes extend that owner test; telemetry source is not rewritten |
| Supersession owner | `_effective_evidence` uses relation key `(prior_evidence_ref, successor_evidence_ref, current_acceptance_scope_ref, rechecked_claim_refs)`, rejects duplicate relations/overlap/cycles, and owns sorted traversal | Lifecycle passes the evidence and supersession carriers unchanged and never sorts them |

The ledger is private planning evidence. It is not a new repository artifact
and is not written to disk by this correction.

## 3. Closed authority and ownership model

The effective Definition and coordinated amendments are already closed. The
following owners are not changed:

| Responsibility | Existing owner | Lifecycle behavior |
|---|---|---|
| Attempt lookup, admissibility, claim, `IN_FLIGHT`, terminalization | Attempt Runtime | call existing owner directly |
| one operation guidance and route predicate | PL07 execution guidance | consume one supplied mapping unchanged |
| envelope, one synchronous binding occurrence, completion, result | Governed Executor | provide typed bounded contract only |
| receipt validation, identity injection, persistence, readback | existing telemetry collector | call once with authoritative identities |
| ordering and coordination | Governed Operation Lifecycle | coordinate only |
| technical evaluation and supersession resolution | existing PL08 evaluator | pass typed carriers directly; do not reimplement |
| next permitted action and gate truth | Project Spine / owner | quote existing value; never select or authorize it |
| semantic chat interpretation | Chat Agent | labels only; typed action is required |

Pattern B remains the only route: prepare, one bounded execution occurrence,
completion validation, receipt/evidence readback, Runtime terminalization,
then PL08 handoff and Spine projection. There is no lifecycle store, queue,
worker, scheduler, retry owner, callback, hook, daemon, registry, database,
post-turn continuation, parser authority, external host, or new receipt host.
RunReceipt schema, Attempt Runtime schema, PL07 authority, PL08 authority,
Change 2, Change 3, and the major PL09 gate remain outside this implementation.

## 4. Frozen contract and semantic corrections

### 4.1 Canonical codecs and identity

New governed contracts use UTF-8 canonical JSON with `sort_keys=True`,
`separators=(",", ":")`, `ensure_ascii=False`, `allow_nan=False`, no final
newline, NFC normalization before validation, and rejection of floats and
duplicate object members. Relative repository paths use POSIX separators.
Collections declare whether order is semantic; no implementation may silently
sort a semantically ordered collection.

`GovernedExecutionEnvelopeV1` contains exactly:
`schema_version`, `contract_version`, `attempt_id`, `operation_id`,
`task_or_operation_id`, `guidance_ref`, `guidance_digest`, `authority_refs`,
`bounded_payload_digest`, and `payload_schema_ref`. `execution_invocation_id`
and `envelope_digest` are derived, never caller-selected. The envelope digest
is uppercase SHA-256 of the canonical ten-field projection. The invocation ID
is uppercase SHA-256 of:

```text
ASCII("planning-lite:governed-operation-execution-envelope:v1") + NUL + canonical_projection
```

Fixed envelope projection vector:

```text
{"attempt_id":"CHG-TEST-001/T-01/A1","authority_refs":["AUTH-A","AUTH-B"],"bounded_payload_digest":"0000000000000000000000000000000000000000000000000000000000000002","contract_version":"GovernedExecutionEnvelopeV1","guidance_digest":"0000000000000000000000000000000000000000000000000000000000000001","guidance_ref":"GUIDANCE-1","operation_id":"OP-TEST","payload_schema_ref":"payload.v1","schema_version":1,"task_or_operation_id":"T-01"}
```

Expected fixed values: `envelope_digest=D2E8370C6024A14E2864DEA05AB02CA0E08678497F4E33370BC3CF35657FA829` and `execution_invocation_id=A7DE0328ADF1DEC38496F8A9B3740B91672D7ACAC49662FFD7803229E820A1D1`.

### 4.2 Complete live guidance vector

The implementation must compute the digest from the exact mapping returned by
PL07 and the live `serialize_guidance` codec. The following fixture is the
complete successful implementation mapping, including every scalar and nested
array. It is not a projection:

```json
{"authority":{"authority_refs":[{"path":".planning/control/APPROVAL_GATES.md","sha256":"ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789"}],"predicate_id":"IMPLEMENTATION_ROUTE_PREDICATE","predicate_result":"AUTHORIZED_FOR_THIS_OPERATION"},"capabilities":[{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"READ","state":"ALLOWED"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"GOVERNANCE_WRITE","state":"ALLOWED"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"PRODUCT_WRITE","state":"ALLOWED"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"GIT_STAGE","state":"REQUIRES_SEPARATE_AUTHORIZATION"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"GIT_COMMIT","state":"REQUIRES_SEPARATE_AUTHORIZATION"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"NETWORK_EXTERNAL","state":"REQUIRES_SEPARATE_AUTHORIZATION"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"DISPOSABLE_CONSUMER","state":"REQUIRES_SEPARATE_AUTHORIZATION"},{"authority_ref":".planning/control/APPROVAL_GATES.md","capability_id":"LIVE_CONSUMER","state":"REQUIRES_SEPARATE_AUTHORIZATION"}],"guidance":{"discipline_refs":[],"escalation_ref":".planning/control/CHANGE_AMENDMENT.md","evidence_refs":[".planning/active/progress.md"],"mode_ref":".planning/modes/EXECUTE.md","next_gate_owner_ref":"change-owner","next_gate_ref":".planning/ACTIVE.md#Active change","policy_refs":[".planning/control/APPROVAL_GATES.md",".planning/control/STATE_OWNERSHIP.md"],"precondition_refs":[".planning/control/CHANGE_PLANNING.md",".planning/control/APPROVAL_GATES.md"],"procedure_ref":".planning/control/CHANGE_EXECUTION.md","result_contract_refs":["OperationGuidanceV1"],"scope_refs":[".planning/active/demo"],"skill_ref":".planning/skills/planning-execute/SKILL.md","stop_condition_refs":[".planning/control/CHANGE_AMENDMENT.md",".planning/control/CHANGE_EXECUTION.md"],"task_binding_refs":[".planning/changes/templates/tasks.md"],"verification_refs":[".planning/control/CHANGE_EXECUTION.md"]},"operation":{"operation_class":"EXECUTE_CHANGE_TASK","operation_id":"EXECUTE_CHANGE_TASK","route_id":"CHANGE_EXECUTION_V1"},"outcome":"MATCHED","provenance":{"authority_refs":[{"path":".planning/control/APPROVAL_GATES.md","sha256":"ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789"}],"candidate_set_id":"PL_V39_07_OPERATION_GUIDANCE_V1","resume_schema_version":1,"resume_status":"CURRENT","selection_reason":"EXACT_OPERATION_BINDING:EXECUTE_AUTHORIZED_TASK","source_revision":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"reason_code":"EXACT_OPERATION_BINDING","schema_version":1}
```

The SHA-256 of these exact UTF-8 bytes is
`f36d5fba7d210b60eb278a8dc8b8509daeafa2143fba89e4fc3fe5588b5fa4fe`.
The top-level reason is `EXACT_OPERATION_BINDING`; the nested predicate result
is `AUTHORIZED_FOR_THIS_OPERATION`. A test must assert both locations and the
complete top-level, authority, capability, guidance, and provenance key sets.

### 4.3 Completion, result, and observation carriers

Completion copies and validates `attempt_id`, `execution_invocation_id`,
`envelope_digest`, `operation_id`, and `task_or_operation_id` from the envelope.
It carries a typed `result_id`, exact execution status, changed paths, fact
references, artifact references, acceptance-contract reference and object,
verifier contracts/evidence, findings, evaluation scope, supersession, and
receipt identity fields. Receipt identity is paired: either both the supplied
receipt ID and persisted receipt mapping are present or neither is present.
Receipt-free completion is valid only as an evidence-incomplete result and
cannot terminalize an Attempt or invoke PL08.

`GovernedExecutionResultV1` exposes typed facts and references, not storage
paths, runtime JSON, receipt files, retry controls, or next-gate operations.
`ObservedResultV1` remains exactly the six live fields
`result_id`, `attempt_id`, `execution_status`, `changed_paths`, `fact_refs`,
and `artifact_refs`. A receipt is collected and read back separately; it is
not added to `ObservedResultV1`.

The lifecycle calls `evaluate_technical` with these exact named carriers:
`attempt`, `contracts`, `evidence`, `acceptance_contract_ref`,
`evaluation_scope_ref`, `findings`, `acceptance_contract`, `supersession`,
`evaluation_id`, `evaluation_run`, and `candidate_quality`. The five required
and six optional signature categories are an inspection fact only; the call
site supplies all eleven semantic inputs explicitly and uses live dataclasses.

The following is the one normative source map for that call. It distinguishes
Python parameter kind from semantic requiredness and names the exact carrier
source. No row may be resolved later from a reference string, receipt, text,
or `ObservedResultV1`.

| Parameter | Python kind | Required/optional | Exact typed source | Source type | Source field/object | Acquisition point | Default allowed | Transformation | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| `attempt` | positional-or-keyword | required | `AttemptLookupResultV1.attempt` returned by `lookup_attempt` and retained through admissibility/claim | `AttemptRecordV1` | authoritative Attempt object | lifecycle preparation before claim | no | identity-preserving object pass-through | missing, wrong-type, or cross-Attempt input reaches `_validate_evaluation_fixture`, is caught by `evaluate_technical`, and returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `contracts` | positional-or-keyword | required | `GovernedExecutionCompletionV1.verifier_contracts` | `tuple[VerifierContractV1, ...]` | direct completion carrier | completion validation | no | tuple pass-through; no reference resolution | missing, wrong-type, incomplete, duplicate, or Attempt-mismatched contracts fail in `validate_verifier_set`, then `evaluate_technical` returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `evidence` | positional-or-keyword | required | `GovernedExecutionCompletionV1.verifier_evidence` | `tuple[VerifierEvidenceV1, ...]` | direct completion carrier | completion validation | no | tuple pass-through; no receipt inference | wrong-type or duplicate-identity evidence fails in `_validate_evaluation_fixture`, then the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `findings` | positional-or-keyword | optional in Python; governed result supplied | `GovernedExecutionCompletionV1.findings` | `tuple[FindingV1, ...]` | direct completion carrier | completion validation | no; empty tuple is explicitly supplied when none | tuple pass-through | wrong-type, missing applicability, or duplicate finding identity fails in `_validate_evaluation_fixture`, then the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `acceptance_contract_ref` | keyword-only | required | `attempt.acceptance_contract_ref` | `str` | exact Attempt scalar field | authoritative Attempt acquisition | no | scalar pass-through | empty value fails `_nonempty`; mismatch against the typed acceptance contract or Attempt fails `validate_verifier_set`; the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `evaluation_scope_ref` | keyword-only | required | `GovernedExecutionCompletionV1.evaluation_scope_ref` | `str` | exact completion scalar field | completion validation | no | scalar pass-through | empty value fails `_nonempty`; malformed or unknown supersession lineage fails `_effective_evidence`; the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `acceptance_contract` | keyword-only | optional in Python; required by governed route | `GovernedExecutionCompletionV1.acceptance_contract` | `AcceptanceContractV1` | direct typed completion field; `None` is not legal for the governed call | completion validation | no; the live `validate_verifier_set` rejects missing or wrong-type carrier | exact object pass-through | missing, wrong-type, incomplete, or reference-mismatched contract fails `validate_verifier_set`; the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `supersession` | keyword-only | optional in Python; governed result supplied | `GovernedExecutionCompletionV1.supersession` | `tuple[EvidenceSupersessionV1, ...]` | direct typed completion carrier | completion validation | no; empty tuple is explicitly supplied when none | tuple pass-through; evaluator owns resolution | wrong-type relation, unknown reference, incompatible lineage, duplicate relation, overlap, or cycle fails `_validate_evaluation_fixture`/`_effective_evidence`; the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `evaluation_id` | keyword-only | optional in Python; governed result supplied | `GovernedExecutionCompletionV1.evaluation_id` | `str` | exact completion scalar field | completion validation | no | scalar pass-through | empty or invalid identity fails `_nonempty` in `_validate_evaluation_fixture`; the evaluator returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE` |
| `evaluation_run` | keyword-only | optional in Python; governed result supplied | `GovernedExecutionCompletionV1.evaluation_run` | `bool` | exact completion scalar field | completion validation | no | boolean pass-through | non-boolean input fails `_validate_evaluation_fixture` and returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE`; explicit `False` follows the live `NOT_EVALUATED` branch |
| `candidate_quality` | keyword-only | optional in Python; governed result supplied | `GovernedExecutionCompletionV1.candidate_quality` | `bool` | exact completion scalar field | completion validation | no | boolean pass-through | non-boolean input fails `_validate_evaluation_fixture` and returns `_not_evaluated` with `INVALID_CONTRACT_OR_FIXTURE`; explicit `False` follows the live `NOT_EVALUATED` branch |

```text
PL08_REQUIRED_POSITIONAL_OR_KEYWORD_WITHOUT_DEFAULT_COUNT: 3
PL08_REQUIRED_KEYWORD_ONLY_WITHOUT_DEFAULT_COUNT: 2
PL08_OPTIONAL_PARAMETER_COUNT: 6
PL08_TOTAL_PARAMETER_COUNT: 11
PL08_EXPLICIT_ARGUMENT_COUNT: 11
PL08_INTENTIONALLY_DEFAULTED_ARGUMENT_COUNT: 0
PL08_ARGUMENT_SOURCE_UNBOUND_COUNT: 0
PL08_CALL_SOURCE_PROOF: PASS
PL08_PARAMETER_FAILURE_BEHAVIOR_ROW_COUNT: 11
PL08_FAILURE_BEHAVIOR_UNBOUND_COUNT: 0
PL08_REFERENCE_STRING_RECONSTRUCTION_COUNT: 0
```

The existing node
`tests/test_operation_lifecycle.py::test_lifecycle_supplies_all_evaluation_carriers`
must assert all eleven keyword identities, exact runtime types, scalar values,
and tuple/object identity against the validated Completion and authoritative
Attempt fixture. It must also assert that the mocked evaluator receives no
omitted optional parameter and no reference-string reconstruction occurs.

### 4.4 Supersession and lifecycle order

`EvidenceSupersessionV1` is passed to the existing evaluator unchanged. Its
relation identity is exactly:

```text
(prior_evidence_ref, successor_evidence_ref,
 current_acceptance_scope_ref, rechecked_claim_refs)
```

`reason` is explanatory and is not relation identity. Lifecycle does not sort,
deduplicate, serialize, or resolve supersession. `_effective_evidence` is the
single serializer/resolution owner: it rejects duplicate relation keys,
overlap, and cycles, traverses successor and evidence IDs in its live sorted
order, and preserves claim order inside the relation. Any lifecycle trace
copies the typed carrier or calls its live mapping method; it does not invent a
second canonical representation.

The sole normative order is:

```text
lookup authoritative Attempt
-> check admissibility
-> claim the same Attempt
-> obtain one supplied OperationGuidanceV1
-> construct and validate GovernedExecutionEnvelopeV1
-> invoke one synchronous binding occurrence
-> validate typed Completion and GovernedExecutionResultV1
-> collect one governed receipt through existing telemetry
-> read back the exact supplied receipt ID and verify the identity triangle
-> construct ObservedResultV1 and validate evidence/supersession carriers
-> terminalize the same Attempt through Attempt Runtime
-> call PL08 once with the eleven typed carriers
-> project downstream facts to existing Spine/resume machinery
```

No branch may terminalize or call PL08 before receipt readback and identity
validation. Failure returns the first broken seam and performs no invented
retry or recovery action.

### 4.5 Semantic action and compact status

The only semantic actions are typed `EXECUTE_AUTHORIZED_TASK`, typed finish
intent `FINISH_CURRENT_CYCLE`, and read-only `SHOW_COMPACT_PROJECT_STATUS`.
Natural-language labels, including `подведём итоги` and `какие итоги
исследования?`, are not authorization and cannot bypass typed validation.

`SHOW_COMPACT_PROJECT_STATUS` returns exactly these six owner-language fields:

| Owner label | Machine key | Source and exact rule | Unavailable rule |
|---|---|---|---|
| `Где мы` | `where_we_are` | `build_resume_context`: project identity, status, active change, lifecycle stage, stage status | `DISPLAY_UNAVAILABLE` |
| `Что сделано` | `what_is_done` | `load_attempt_store` -> terminal `AttemptEnvelopeV1.runtime_state`, `attempt.observed_result_ref`, `observed_result.result_id`, `observed_result.execution_status`, `observed_result.fact_refs`, `observed_result.artifact_refs`, and `attempt.verifier_contract_refs` | no terminal row or any referenced observed result -> `DISPLAY_UNAVAILABLE`; never add a receipt field |
| `Что сейчас` | `what_is_current` | `build_resume_context` fields `status`, `bootstrap.active_change`, `bootstrap.lifecycle_stage`, `bootstrap.stage_status`, `bootstrap.active_context_path`, plus Runtime `AttemptEnvelopeV1.runtime_state`, `AttemptRecordV1.task_or_operation_id`, and `AttemptRecordV1.operation_guidance_ref` | missing source -> `DISPLAY_UNAVAILABLE`; current invocation is not a live Runtime field and is explicitly unavailable |
| `Что дальше` | `what_next` | Spine `bootstrap.next_permitted_action`, quoted exactly | `DISPLAY_UNAVAILABLE`; no recommendation |
| `Ресурсы` | `resources` | `build_observed_resume_context` fields `context_trace.selected`, `selected_artifact_count`, `selected_section_count`, `selected_character_count`, `explicit_expansion_count`, `bounds`, `git_identity`; `OperationDepthObservationV1.start`, `.expansions`, `.overall_completeness`, `.unavailable_reasons` | producer unavailable/stale/missing -> `DISPLAY_UNAVAILABLE`; only producer-marked exact/approximate observations |
| `Состояние` | `state` | `build_resume_context.status`, `bootstrap.implementation_authorized`, and Runtime `AttemptEnvelopeV1.runtime_state` | either owner source absent -> `DISPLAY_UNAVAILABLE` |

The exact status source contract is therefore:

| Owner label | Machine key | Source symbol | Source field paths | Transformation | `DISPLAY_UNAVAILABLE` condition |
|---|---|---|---|---|---|
| `Где мы` | `where_we_are` | `build_resume_context` | `status`; `project_identity.project_id`; `bootstrap.active_change`; `bootstrap.lifecycle_stage`; `bootstrap.stage_status` | copy those five values; no inferred phase | any required resume field absent |
| `Что сделано` | `what_is_done` | `load_attempt_store` | `attempts[*].runtime_state`; `attempts[*].attempt.observed_result_ref`; `attempts[*].observed_result.result_id`; `.execution_status`; `.fact_refs`; `.artifact_refs`; `attempts[*].attempt.verifier_contract_refs` | select exactly one terminal envelope; expose only existing result/evidence fields; receipt is never synthesized | no terminal envelope, missing observed result, or broken result reference |
| `Что сейчас` | `what_is_current` | `build_resume_context`, `lookup_attempt`, `check_activation_admissibility` | `status`; `bootstrap.active_change`; `bootstrap.lifecycle_stage`; `bootstrap.stage_status`; `bootstrap.active_context_path`; `AttemptEnvelopeV1.runtime_state`; `AttemptRecordV1.task_or_operation_id`; `AttemptRecordV1.operation_guidance_ref` | copy current values; omit invocation value and return `DISPLAY_UNAVAILABLE` for that unavailable sub-observation | resume/Runtime source absent; invocation has no authoritative live field |
| `Что дальше` | `what_next` | `build_resume_context` / Project Spine projection | `bootstrap.next_permitted_action` | quote exact string; never choose it | field absent |
| `Ресурсы` | `resources` | `build_observed_resume_context`, `OperationDepthObservationV1.from_produced_context` | `ProducedResumeContextV1` and `OperationDepthObservationV1`: `context_trace.selected`; four trace counts; `bounds`; `git_identity`; `start`; `expansions`; `overall_completeness`; `unavailable_reasons` | retain producer output; use `AVERAGE_OBSERVED_CONTEXT_DEPTH` only for producer-marked current-cycle observation | producer output missing, stale, or marked unavailable |
| `Состояние` | `state` | `build_resume_context`, `load_attempt_store` | `status`; `bootstrap.implementation_authorized`; `AttemptEnvelopeV1.runtime_state` | copy exact status and boolean/state | either source absent |

No receipt reference is claimed by status. No second status authority or new
persistence is introduced. The existing nodes
`test_compact_status_has_exact_six_fields`, `test_status_uses_next_permitted_action_as_quote`,
`test_unavailable_status_source_is_explicit`, and `test_status_route_is_read_only`
must assert unavailable invocation, no fabricated receipt, exact evidence-field
selection, and no mutation.

Resource depth uses the existing `AVERAGE_OBSERVED_CONTEXT_DEPTH` with scope
`CURRENT_CYCLE` only when the producer marks it as observed/approximate.
Status performs no claim, terminalization, write, recommendation, next-gate
selection, callback, or post-turn continuation.

## 5. Authorized implementation surface and first-write inventory

The following twelve product paths are the complete authorized write set. A
path is first writable only in its listed task. All other repository paths,
including telemetry source, manifest source, governance records, `CURRENT.md`,
and all pre-existing dirty paths, are read-only.

| Path | Entry state | First write | Owner purpose |
|---|---|---|---|
| `src/planning_lite/governed_executor.py` | absent | T-03 | typed bounded executor |
| `src/planning_lite/operation_lifecycle.py` | absent | T-04 | Pattern B coordinator |
| `src/planning_lite/context.py` | present | T-05 | typed action and six-field status |
| `src/planning_lite/cli.py` | present | T-06 | thin execute/status route |
| `template/.planning/adapters/codex/README.md` | present | T-07 | semantic binding documentation |
| `tests/test_governed_executor.py` | absent | T-02 | executor tests |
| `tests/test_operation_lifecycle.py` | absent | T-02 | lifecycle tests |
| `tests/test_cli.py` | present | T-02 | exact CLI nodes appended |
| `tests/test_context_resume.py` | present | T-02 | exact context/status nodes appended |
| `tests/test_run_receipts.py` | present | T-02 | exact collector-binding nodes appended |
| `tests/test_system_traversability.py` | present | T-02 | exact route/integrity nodes appended |
| `template/.planning/framework/SHA256SUMS.txt` | present | T-07 | regenerate only for the adapter README change |

Excluded from the implementation surface: `src/planning_lite/telemetry.py`,
`src/planning_lite/attempt_runtime.py`, `src/planning_lite/attempt_evaluation.py`,
`src/planning_lite/execution_guidance.py`, `pyproject.toml`, Copier answers,
all project-spine records, all Change records, all consumer projects, and all
source manifests except the listed checksum update.

At entry, the following future files/nodes are absent and must not be read by
an earlier task. T-02 creates them before T-03 and later tasks may read them:

| Test path | Exact nodes created by T-02 |
|---|---|
| `tests/test_governed_executor.py` | `test_envelope_identity_vector`, `test_complete_guidance_digest_vector`, `test_executor_negative_identity_matrix`, `test_executor_has_no_forbidden_owner_calls`, `test_executor_projects_typed_result` |
| `tests/test_operation_lifecycle.py` | `test_pattern_b_order_and_identity_triangle`, `test_lifecycle_supplies_all_evaluation_carriers`, `test_lifecycle_reentry_uses_runtime`, `test_lifecycle_negative_receipt_matrix`, `test_lifecycle_terminalization_is_runtime_owned`, `test_lifecycle_false_done_and_next_gate_boundaries` |
| `tests/test_cli.py` | `test_execute_prepare_complete_route`, `test_finish_requires_typed_current_cycle`, `test_status_route_is_read_only` |
| `tests/test_context_resume.py` | `test_compact_status_has_exact_six_fields`, `test_status_uses_next_permitted_action_as_quote`, `test_status_token_and_depth_contract`, `test_unavailable_status_source_is_explicit` |
| `tests/test_run_receipts.py` | `test_lifecycle_uses_supplied_receipt_id`, `test_lifecycle_reads_back_persisted_receipt`, `test_cross_attempt_receipt_is_rejected`, `test_cross_invocation_receipt_is_rejected`, `test_legacy_v1_receipt_is_not_governed_fallback` |
| `tests/test_system_traversability.py` | `test_real_self_hosted_execute_entrypoint_reaches_lifecycle`, `test_system_traversability_preserves_closed_boundaries`, `test_template_checksum_matches_authorized_surface` |

## 6. Rebuilt task graph

Every dependency below names an exact path, symbol, field, or output. No task
reads a future test node; no category-level phrase such as “all outputs” is a
dependency. T-01 and T-02 are the only preparation tasks; product source is
not changed before the complete test-node skeleton exists.

| ID | Work and exact reads | Exact writes | Verification rows |
|---|---|---|---|
| T-01 | Read the 14 authority records in §7, `CURRENT.md`, `copier.yml`, `template/.planning/framework/OWNERSHIP.yml`, live source symbols in §2, entry HEAD/index/status | ignored `.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_FIFTH_PLAN_BASELINE.json` only; no product write | V-01,V-02 |
| T-02 | Read the six entry test paths listed in §5 and their existing owners; create every exact future file/node listed in §5 with failing or pending assertions tied to named contracts | six test paths in §5 only | V-03 |
| T-03 | Read `tests/test_governed_executor.py` nodes from T-02, `src/planning_lite/execution_guidance.py`, live Attempt/result/telemetry definitions, and §4.1–4.3 | `src/planning_lite/governed_executor.py`; executor test bodies | V-04,V-05,V-06 |
| T-04 | Read `tests/test_operation_lifecycle.py` nodes from T-02, T-03 executor API, `attempt_runtime.py`, `telemetry.py`, `attempt_evaluation.py`, and §4.4 | `src/planning_lite/operation_lifecycle.py`; lifecycle test bodies | V-07,V-08,V-09,V-10,V-11 |
| T-05 | Read T-04 lifecycle call site, live `ObservedResultV1`, `evaluate_technical` definition, `context.py` resume/depth producers, and status matrix §4.5 | `src/planning_lite/context.py`; lifecycle/context tests | V-12,V-13,V-14 |
| T-06 | Read T-04/T-05 public typed actions, current `cli.py::main`, existing script entry from `pyproject.toml`, and T-02 CLI nodes | `src/planning_lite/cli.py`; CLI tests | V-15,V-16 |
| T-07 | Read T-06 action names, current adapter README, ownership rules, and checksum generation convention | `template/.planning/adapters/codex/README.md`; `template/.planning/framework/SHA256SUMS.txt`; adapter tests | V-17,V-18 |
| T-08 | Read all twelve product paths, every exact test node from T-02, and the real package/CLI entrypoint; exercise integration and static ownership boundaries | no product source write; test bodies may be completed only within the twelve paths | V-19,V-20,V-21 |
| T-09 | Read T-03–T-08 source/test outputs and existing owner tests; run the focused suite, then the full suite from the central checkout | ignored execution evidence output only | V-22,V-23 |
| T-10 | Read committed `HEAD` tree plus the exact authorized current worktree bytes; construct a disposable source snapshot, overlay the authorized bytes, commit only inside the disposable snapshot, and adopt into a fresh target | disposable temp source/target only; no central write | V-24 |
| T-11 | Read T-01 baseline manifest, T-09 evidence, Git status and hashes after all implementation work; classify every byte-level delta | ignored execution evidence output only | V-25 |
| T-12 | Read the exact T-01 baseline fields, T-08/T-09/T-10/T-11 evidence paths and named result fields; assemble the fixed JSON receipt schema in §9.2 | `.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json` only | V-26 |

T-01 creates the baseline carrier before any implementation write. Its JSON
schema is fixed: `{schema_version:1, entry_head, entry_index_empty,
authorized_paths:[{path,exists,kind,sha256,git_state}],
preexisting_dirty_paths:[{path,exists,kind,sha256,git_state}],
central_status_z, captured_at_for_diagnostics}`. `captured_at_for_diagnostics`
is not used for equality. `sha256` is the actual file-byte hash; for a
pre-existing absent tracked file, it is the hash of `git show HEAD:path` bytes.
Both authorized paths and every pre-existing dirty path are captured, including
object kind and Git state. T-11 compares content, existence, kind, and Git
state; path names alone are insufficient.

## 7. Authority inventory and verification matrix

V-01 hashes exactly these authority records and verifies HEAD/index; no count
substitution is permitted.

| Authority path | Entry SHA-256 |
|---|---|
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md` | `56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-ACTIVATION-v1.md` | `F21B8DC151507EB0B937EEFE36CFD35012305808174C3067A4ABC9D0C7C1A53B` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v1.md` | `2C5FFB3D1902424ACBCCA41505CF5113E6C7365AD632831B80C859795B249DA6` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v1.md` | `DA55C416AFCC4933D05F2459773C56CAA10C639242AA71D1040A7CE9C671E84B` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v2.md` | `E1D979F2E5219A2042611033455E95F0E2024B53741D048D08EBFD938FB5EABA` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v2.md` | `004331DF581880BDBA57AE8FD782132EDCED2D841829E5B6BF4A08BC7E4D8A93` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md` | `127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md` | `2CDE29CA69D29FF3FC327B82C05EAF6A3CCB54143F1B30B8953B2FC07BFAD4C7` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md` | `AC012052CCCE524FD9770EEEF94D87181C320ABE0D863C2DC930928740F9B886` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v1.md` | `59797EFD9F2FDDA8E7A1B4A478F7985A8E43C66956F5BFBD3420F0F7531511D4` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md` | `444BC880E112F070FB5A3E6B29B3ED1FDD35DDF5E637905A8AB4094D0A9AC510` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v2.md` | `33597F3B40E1B06F8D7B6EF601764100DD7C1F7E8CC64635F03C8171759325F1` |
| `docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-CLOSURE-v1.md` | `40D998EF9FE11EF5D56A927917208D4711FD860BA4A4121FF5573B96553973F2` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md` | `3E96782EC6F70DB5F6835CDEB90F4E2EE2AEF4E92AC8CC21F463E639CC101A6E` |

| V-ID | Exact command/probe | Required evidence and failure |
|---|---|---|
| V-01 | exact PowerShell command in §7.1 | exact hashes, HEAD, and empty index; stop on any drift |
| V-02 | exact `uv run --frozen python -c` command in §7.2 | live matched guidance, complete vector digest, and distinct reason/predicate; stop on any drift |
| V-03 | `uv run --frozen pytest --collect-only -q` for all nodes in §5 after T-02 | all named nodes collect; no regex selector or future read; stop on missing node |
| V-04 | `uv run --frozen pytest tests/test_governed_executor.py::test_envelope_identity_vector -q` | exact projection, digest, domain, and invocation vector |
| V-05 | `uv run --frozen pytest tests/test_governed_executor.py::test_complete_guidance_digest_vector -q` | complete mapping, nested predicate/reason distinction, and digest `f36d5fba7d210b60eb278a8dc8b8509daeafa2143fba89e4fc3fe5588b5fa4fe` |
| V-06 | `uv run --frozen pytest tests/test_governed_executor.py::test_executor_negative_identity_matrix tests/test_governed_executor.py::test_executor_projects_typed_result -q` | cross-Attempt, invalid result, unavailable host, and typed result failures are closed |
| V-07 | exact alias-resolving AST script in §7.3, executed with `uv run --frozen python -` | complete owner proof for both modules; stop on aliases, dynamic lookup, unresolved owner, missing direct call, or forbidden reference |
| V-08 | `uv run --frozen pytest tests/test_operation_lifecycle.py::test_pattern_b_order_and_identity_triangle tests/test_operation_lifecycle.py::test_lifecycle_reentry_uses_runtime -q` | one Attempt identity, bounded Pattern B order, Runtime reentry, and exact event order |
| V-09 | `uv run --frozen pytest tests/test_run_receipts.py::test_lifecycle_uses_supplied_receipt_id tests/test_run_receipts.py::test_lifecycle_reads_back_persisted_receipt tests/test_operation_lifecycle.py::test_lifecycle_negative_receipt_matrix -q` | supplied ID, persisted raw readback, identity triangle, and fail-closed negatives |
| V-10 | `uv run --frozen pytest tests/test_operation_lifecycle.py::test_lifecycle_supplies_all_evaluation_carriers -q` | all 11 named evaluator carriers are typed and direct; supersession is unchanged |
| V-11 | `uv run --frozen pytest tests/test_operation_lifecycle.py::test_lifecycle_terminalization_is_runtime_owned tests/test_operation_lifecycle.py::test_lifecycle_false_done_and_next_gate_boundaries -q` | Runtime terminalization, no PL08-before-readback, no status authority, no retry/callback/next-gate mutation |
| V-12 | `uv run --frozen pytest tests/test_context_resume.py::test_compact_status_has_exact_six_fields tests/test_context_resume.py::test_status_uses_next_permitted_action_as_quote -q` | exact six keys and owner labels; Spine action quoted rather than selected |
| V-13 | `uv run --frozen pytest tests/test_context_resume.py::test_status_token_and_depth_contract tests/test_context_resume.py::test_unavailable_status_source_is_explicit -q` | exact/marked-approximate observation or explicit unavailable; no fabricated metrics |
| V-14 | `uv run --frozen pytest tests/test_cli.py::test_finish_requires_typed_current_cycle tests/test_cli.py::test_status_route_is_read_only -q` | typed finish/status only; status causes no write and semantic text is nonauthorizing |
| V-15 | `uv run --frozen pytest tests/test_cli.py::test_execute_prepare_complete_route -q` | real thin CLI path reaches the lifecycle and preserves exit/error contract |
| V-16 | `uv run --frozen pytest tests/test_operation_lifecycle.py::test_lifecycle_negative_receipt_matrix tests/test_run_receipts.py::test_legacy_v1_receipt_is_not_governed_fallback -q` | missing, stale, cross-Attempt, cross-invocation, external-identity, latest/time/task, and legacy-v1 substitutions fail closed |
| V-17 | `uv run --frozen pytest tests/test_system_traversability.py::test_real_self_hosted_execute_entrypoint_reaches_lifecycle -q` | real package/adapter entry reaches the production route, not a helper-only fake |
| V-18 | `uv run --frozen pytest tests/test_system_traversability.py::test_template_checksum_matches_authorized_surface -q` | adapter documentation and checksum agree; no unrelated manifest delta |
| V-19 | `uv run --frozen pytest tests/test_governed_executor.py::test_executor_has_no_forbidden_owner_calls tests/test_operation_lifecycle.py::test_lifecycle_false_done_and_next_gate_boundaries -q` | no lifecycle/Runtime/receipt/PL08 authority in Executor and no Chat/Spine authority in lifecycle |
| V-20 | `uv run --frozen pytest tests/test_system_traversability.py::test_system_traversability_preserves_closed_boundaries -q` | no persistent store, worker, callback, Change absorption, or post-turn behavior |
| V-21 | `uv run --frozen pytest tests/test_operation_lifecycle.py::test_lifecycle_supplies_all_evaluation_carriers tests/test_context_resume.py::test_compact_status_has_exact_six_fields -q` | PL08 receives direct typed carriers and status remains a six-field projection |
| V-22 | `uv run --frozen pytest tests/test_governed_executor.py tests/test_operation_lifecycle.py tests/test_cli.py tests/test_context_resume.py tests/test_run_receipts.py tests/test_system_traversability.py -q` | focused authorized suite passes before broader regression |
| V-23 | `uv run --frozen pytest -q` from the central checkout | full regression passes; if failure is unrelated, adjudicate and stop rather than weakening a proof |
| V-24 | exact disposable snapshot/adoption script in §8 | target adopts exact authorized current bytes from a locally committed disposable source; target sync, frozen pytest, diff check, doctor, and source-preservation checks pass |
| V-25 | exact content-sensitive baseline/delta script in §9 | every pre-existing dirty entry is byte-identical before/after; every changed path is authorized; unknown or extra mutation fails |
| V-26 | exact JSON validator in §9.2, executed with `uv run --frozen python -c` | fixed T-12 receipt schema validates entry identity, candidate hashes, 12 task receipts, 26 verification receipts, AC/CC results, mutation audit, boundaries, and terminal verdict |

### 7.1 Executable V-01 authority command

```powershell
$ErrorActionPreference='Stop'
$expected=[ordered]@{
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md'='56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-ACTIVATION-v1.md'='F21B8DC151507EB0B937EEFE36CFD35012305808174C3067A4ABC9D0C7C1A53B'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v1.md'='2C5FFB3D1902424ACBCCA41505CF5113E6C7365AD632831B80C859795B249DA6'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v1.md'='DA55C416AFCC4933D05F2459773C56CAA10C639242AA71D1040A7CE9C671E84B'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v2.md'='E1D979F2E5219A2042611033455E95F0E2024B53741D048D08EBFD938FB5EABA'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v2.md'='004331DF581880BDBA57AE8FD782132EDCED2D841829E5B6BF4A08BC7E4D8A93'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md'='127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md'='2CDE29CA69D29FF3FC327B82C05EAF6A3CCB54143F1B30B8953B2FC07BFAD4C7'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md'='AC012052CCCE524FD9770EEEF94D87181C320ABE0D863C2DC930928740F9B886'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v1.md'='59797EFD9F2FDDA8E7A1B4A478F7985A8E43C66956F5BFBD3420F0F7531511D4'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md'='444BC880E112F070FB5A3E6B29B3ED1FDD35DDF5E637905A8AB4094D0A9AC510'
'docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v2.md'='33597F3B40E1B06F8D7B6EF601764100DD7C1F7E8CC64635F03C8171759325F1'
'docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-CLOSURE-v1.md'='40D998EF9FE11EF5D56A927917208D4711FD860BA4A4121FF5573B96553973F2'
'docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md'='3E96782EC6F70DB5F6835CDEB90F4E2EE2AEF4E92AC8CC21F463E639CC101A6E'
}
if($expected.Count -ne 14){throw 'authority inventory count mismatch'}
if((git rev-parse HEAD) -ne '407f4daef02227145a0c807ca182925c76888b60'){throw 'HEAD mismatch'}
git diff --cached --quiet
if($LASTEXITCODE -ne 0){throw 'index is not empty'}
foreach($path in $expected.Keys){
  if(!(Test-Path -LiteralPath $path -PathType Leaf)){throw "missing authority path: $path"}
  $actual=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToUpperInvariant()
  if($actual -ne $expected[$path]){throw "authority hash mismatch: $path"}
}
'PASS V-01 AUTHORITY_COUNT=14 INDEX_EMPTY=YES'
```

### 7.2 Executable V-02 guidance command

```powershell
uv run --frozen python -c "import hashlib; from planning_lite.execution_guidance import select_operation_guidance,serialize_guidance; c={'schema_version':1,'status':'CURRENT','bootstrap':{'active_change':'CHG-TEST-001','active_context_path':'.planning/active/demo','lifecycle_stage':'Implementation','stage_status':'In progress','next_permitted_action':'EXECUTE_AUTHORIZED_TASK','implementation_authorized':True,'open_blocker':None,'source_revision':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'},'selected_sources':[{'path':'.planning/control/APPROVAL_GATES.md','sha256':'ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789'}]}; r=select_operation_guidance(c); s=serialize_guidance(r); assert r['outcome']=='MATCHED'; assert r['reason_code']=='EXACT_OPERATION_BINDING'; assert r['authority']['predicate_result']=='AUTHORIZED_FOR_THIS_OPERATION'; assert hashlib.sha256(s.encode('utf-8')).hexdigest()=='f36d5fba7d210b60eb278a8dc8b8509daeafa2143fba89e4fc3fe5588b5fa4fe'; assert set(r)=={'schema_version','outcome','reason_code','operation','authority','capabilities','guidance','provenance'}; print('PASS V-02 GUIDANCE_VECTOR_SHA256='+hashlib.sha256(s.encode('utf-8')).hexdigest())"
```

### 7.3 Executable V-07 owner-resolution command

The command resolves relative imports, module aliases, imported-symbol aliases,
attribute calls, assignment aliases, definitions, and dynamic calls. It checks
both production modules and fails before printing success on any unresolved or
forbidden owner reference.

```powershell
@'
import ast
import subprocess
from pathlib import Path

REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
ROOT = REPO / "src/planning_lite"
FILES = {
    "executor": ROOT / "governed_executor.py",
    "lifecycle": ROOT / "operation_lifecycle.py",
}
FORBIDDEN_EXECUTOR_MODULES = {
    "planning_lite.attempt_runtime",
    "planning_lite.execution_guidance",
    "planning_lite.telemetry",
    "planning_lite.operation_lifecycle",
    "planning_lite.attempt_evaluation",
}
FORBIDDEN_EXECUTOR_NAMES = {
    "lookup_attempt", "check_activation_admissibility", "claim_attempt",
    "terminalize_attempt", "collect_governed_receipt", "evaluate_technical",
    "select_operation_guidance", "_select_operation_guidance", "serialize_guidance",
}
REQUIRED_LIFECYCLE_CALLS = {
    "planning_lite.attempt_runtime.lookup_attempt",
    "planning_lite.attempt_runtime.check_activation_admissibility",
    "planning_lite.attempt_runtime.claim_attempt",
    "planning_lite.attempt_runtime.terminalize_attempt",
    "planning_lite.telemetry.collect_governed_receipt",
    "planning_lite.attempt_evaluation.evaluate_technical",
}
DYNAMIC_NAMES = {"getattr", "globals", "eval", "exec", "__import__"}

missing_files = sorted(str(path) for path in FILES.values() if not path.is_file())
if missing_files:
    raise SystemExit({"required_files_missing": missing_files})

def absolute_module(current, module, level):
    if not level:
        return module or ""
    parts = current.split(".")[:-level]
    if module:
        parts.append(module)
    return ".".join(parts)

def scan(path, current):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    aliases = {}
    imported = set()
    definitions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                local = item.asname or item.name.split(".")[0]
                value = item.name if item.asname else item.name.split(".")[0]
                aliases[local] = value
                imported.add(value)
        elif isinstance(node, ast.ImportFrom):
            base = absolute_module(current, node.module, node.level)
            for item in node.names:
                if item.name == "*":
                    continue
                local = item.asname or item.name
                value = ".".join(part for part in (base, item.name) if part)
                aliases[local] = value
                imported.add(value)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(f"{current}.{node.name}")
            aliases.setdefault(node.name, f"{current}.{node.name}")
    for _ in range(4):
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Assign):
                targets = [x for x in node.targets if isinstance(x, ast.Name)]
                value = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target]
                value = node.value
            else:
                continue
            if value is None:
                continue
            resolved = resolve(value, aliases)
            if resolved:
                for target in targets:
                    aliases[target.id] = resolved
    refs = set()
    calls = set()
    dynamic = []
    def visit(node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_NAMES:
                dynamic.append(node.lineno)
            resolved = resolve(node.func, aliases)
            if resolved:
                calls.add(resolved)
        if isinstance(node, (ast.Name, ast.Attribute)):
            resolved = resolve(node, aliases)
            if resolved:
                refs.add(resolved)
        for child in ast.iter_child_nodes(node):
            visit(child)
    visit(tree)
    return imported, definitions, refs, calls, dynamic

def resolve(node, aliases):
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        base = resolve(node.value, aliases)
        return f"{base}.{node.attr}" if base else None
    return None

scans = {name: scan(path, f"planning_lite.{path.stem}") for name, path in FILES.items()}
executor_imports, executor_defs, executor_refs, executor_calls, executor_dynamic = scans["executor"]
lifecycle_imports, lifecycle_defs, lifecycle_refs, lifecycle_calls, lifecycle_dynamic = scans["lifecycle"]
def owner_name(value):
    return value.rsplit(".", 1)[-1]
def forbidden(value):
    return any(value == module or value.startswith(module + ".") for module in FORBIDDEN_EXECUTOR_MODULES) or owner_name(value) in FORBIDDEN_EXECUTOR_NAMES
executor_bad = sorted(value for value in executor_imports | executor_defs | executor_refs | executor_calls if forbidden(value))
missing = sorted(REQUIRED_LIFECYCLE_CALLS - lifecycle_calls)
lifecycle_bad = sorted(value for value in lifecycle_refs | lifecycle_calls if value.startswith("planning_lite.execution_guidance.") or value.startswith("planning_lite.cli."))
if executor_bad or executor_dynamic or missing or lifecycle_dynamic or lifecycle_bad:
    raise SystemExit({"executor_bad": executor_bad, "executor_dynamic": executor_dynamic, "missing_lifecycle_calls": missing, "lifecycle_dynamic": lifecycle_dynamic, "lifecycle_bad": lifecycle_bad})
print("PASS V-07 OWNER_RESOLUTION=PASS ALIAS_ESCAPE_UNCHECKED=NO DYNAMIC_ESCAPE_UNCHECKED=NO")
'@ | uv run --frozen python -
```

## 8. V-24 disposable-source adoption proof

The central checkout is intentionally dirty and cannot be made clean for this
proof. V-24 therefore creates an independent source snapshot from committed
`HEAD`, overlays the exact authorized current worktree bytes, computes an
overlay manifest, initializes a local Git identity inside that disposable
source only, and commits there. `planning-lite adopt` receives the disposable
source and its disposable commit ref. The central repository is never used as
the adoption source after overlay and is never committed.

The exact PowerShell procedure is:

```powershell
$ErrorActionPreference='Stop'
$central=(Resolve-Path '.').Path
$head=(git -C $central rev-parse HEAD)
$centralStatus=@(git -C $central status --porcelain=v1 --untracked-files=all)
$centralIndex=(git -C $central diff --cached --name-status | Out-String)
$snapshot=Join-Path ([IO.Path]::GetTempPath()) ('pl09-source-'+[guid]::NewGuid().ToString('N'))
$target=Join-Path ([IO.Path]::GetTempPath()) ('pl09-target-'+[guid]::NewGuid().ToString('N'))
$allowed=@('src/planning_lite/governed_executor.py','src/planning_lite/operation_lifecycle.py','src/planning_lite/context.py','src/planning_lite/cli.py','template/.planning/adapters/codex/README.md','tests/test_governed_executor.py','tests/test_operation_lifecycle.py','tests/test_cli.py','tests/test_context_resume.py','tests/test_run_receipts.py','tests/test_system_traversability.py','template/.planning/framework/SHA256SUMS.txt')
function Get-Vector($root,$rel){
  $q=Join-Path $root $rel
  if(Test-Path -LiteralPath $q -PathType Leaf){$kind='file';$exists=$true;$sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $q -ErrorAction Stop).Hash.ToLowerInvariant()}
  elseif(Test-Path -LiteralPath $q -PathType Container){$kind='directory';$exists=$true;$sha=$null}
  else{$kind='absent';$exists=$false;$sha=$null}
  [ordered]@{path=$rel;exists=$exists;kind=$kind;sha256=$sha}
}
$centralVector=@{}; foreach($rel in $allowed){$centralVector[$rel]=Get-Vector $central $rel}
try {
  git clone --no-hardlinks --no-local $central $snapshot
  if($LASTEXITCODE -ne 0){throw 'snapshot clone failed'}
  git -C $snapshot checkout --detach $head
  if($LASTEXITCODE -ne 0){throw 'snapshot checkout failed'}
  foreach($rel in $allowed){
    $from=Join-Path $central $rel; $to=Join-Path $snapshot $rel
    if(Test-Path -LiteralPath $from -PathType Leaf){
      New-Item -ItemType Directory -Force -Path (Split-Path -Parent $to) | Out-Null
      Copy-Item -LiteralPath $from -Destination $to -Force -ErrorAction Stop
    } elseif(Test-Path -LiteralPath $to){Remove-Item -LiteralPath $to -Force -ErrorAction Stop}
  }
  $snapshotVector=@{}; foreach($rel in $allowed){$snapshotVector[$rel]=Get-Vector $snapshot $rel}
  $mismatch=@($allowed | Where-Object { ($centralVector[$_].path -ne $snapshotVector[$_].path) -or ($centralVector[$_].exists -ne $snapshotVector[$_].exists) -or ($centralVector[$_].kind -ne $snapshotVector[$_].kind) -or ($centralVector[$_].sha256 -ne $snapshotVector[$_].sha256) })
  if($mismatch.Count -ne 0){throw "authorized source/snapshot hash mismatch: $($mismatch -join ',')"}
  $overlay=@($allowed | ForEach-Object { $snapshotVector[$_] })
  $overlay | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 (Join-Path $snapshot 'pl09-overlay-manifest.json')
  git -C $snapshot config user.name 'Planning Lite disposable verification'
  git -C $snapshot config user.email 'planning-lite-disposable-verification@invalid'
  git -C $snapshot add --all
  git -C $snapshot commit -m 'disposable PL09 implementation verification snapshot'
  if($LASTEXITCODE -ne 0){throw 'disposable snapshot commit failed'}
  $snapshotHead=(git -C $snapshot rev-parse HEAD)
  New-Item -ItemType Directory -Force -Path $target | Out-Null
  git -C $target init | Out-Null
  uv run --project $snapshot planning-lite adopt $target --template-source $snapshot --vcs-ref $snapshotHead --agent codex
  if($LASTEXITCODE -ne 0){throw 'adoption failed'}
  uv sync --project $target
  uv run --project $target --frozen pytest
  git -C $target diff --check
  uv run --project $target planning-lite doctor $target
  if((git -C $central rev-parse HEAD) -ne $head){throw 'central HEAD changed'}
  $centralIndexAfter=(git -C $central diff --cached --name-status | Out-String)
  $centralStatusAfter=@(git -C $central status --porcelain=v1 --untracked-files=all)
  if($centralIndexAfter -ne $centralIndex){throw 'central index changed'}
  if((($centralStatusAfter -join "`n") -ne ($centralStatus -join "`n"))){throw 'central dirty state changed'}
  "DISPOSABLE_SOURCE_AUTHORIZED_PATH_HASH_MISMATCH_COUNT: $($mismatch.Count)"
  'PASS V-24 SOURCE_BYTES_OVERLAID_AND_COMMITTED_IN_DISPOSABLE_SNAPSHOT'
} finally {
  $cleanupFailure=$false
  foreach($q in @($target,$snapshot)){if($q -and (Test-Path -LiteralPath $q)){try{Remove-Item -LiteralPath $q -Recurse -Force -ErrorAction Stop}catch{$cleanupFailure=$true}}}
  if($cleanupFailure){'CLEANUP_FAILURE_CHANGES_PRODUCT_VERDICT: NO'}
}
```

The target directory is fresh, target-scoped, and never pre-existing. No
`--allow-dirty` is used. Cleanup failure is recorded as disposable residue and
does not rewrite or invalidate the source-preservation assertion, but it is a
verification failure requiring owner adjudication before any readiness claim.

## 9. V-25 content-sensitive write-boundary proof

T-01 captures the baseline in the same implementation session before T-02.
The baseline includes every authorized path and every path reported by
`git status --porcelain=v1 -z --untracked-files=all`, with existence, object
kind, SHA-256 bytes, and Git state. T-11 recomputes the same manifest and
classifies deltas as `AUTHORIZED_NEW_OR_CHANGED`, `PREEXISTING_UNCHANGED`, or
`UNAUTHORIZED`. A pre-existing authorized path must remain byte-identical
unless the task that owns it is the documented first writer; path-only
exclusion is not evidence.

The exact T-01 baseline capture is:

```powershell
$ErrorActionPreference='Stop'
$repo=(Resolve-Path '.').Path
$authorized=@('src/planning_lite/governed_executor.py','src/planning_lite/operation_lifecycle.py','src/planning_lite/context.py','src/planning_lite/cli.py','template/.planning/adapters/codex/README.md','tests/test_governed_executor.py','tests/test_operation_lifecycle.py','tests/test_cli.py','tests/test_context_resume.py','tests/test_run_receipts.py','tests/test_system_traversability.py','template/.planning/framework/SHA256SUMS.txt')
git diff --cached --quiet
if($LASTEXITCODE -ne 0){throw 'entry index is not empty'}
$statusLines=@(git -c core.quotepath=false status --porcelain=v1 --untracked-files=all)
$dirty=@($statusLines | ForEach-Object {if($_.Length -ge 3){$_.Substring(3)}} | Sort-Object -Unique)
$paths=@($authorized+$dirty | Sort-Object -Unique)
function Read-Entry($rel){
  $q=Join-Path $repo $rel
  if(Test-Path -LiteralPath $q -PathType Leaf){$exists=$true;$kind='file';$sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $q -ErrorAction Stop).Hash.ToLowerInvariant()}
  elseif(Test-Path -LiteralPath $q -PathType Container){$exists=$true;$kind='directory';$sha=$null}
  else{$exists=$false;$kind='absent';$sha=$null}
  $status=$statusLines | Where-Object { $_.Length -ge 3 -and $_.Substring(3) -eq $rel } | Select-Object -First 1
  if($null -ne $status){$code=$status.Substring(0,2);$gitState=if($code -eq '??'){'untracked'}else{'tracked'}; $statusCode=$code}
  else{$null=git ls-files --error-unmatch -- $rel 2>$null; if($LASTEXITCODE -eq 0){$gitState='tracked-clean'}else{$null=git check-ignore --quiet -- $rel 2>$null; $gitState=if($LASTEXITCODE -eq 0){'ignored'}else{'absent'}}; $statusCode='  '}
  [ordered]@{path=$rel;exists=$exists;kind=$kind;sha256=$sha;git_state=$gitState;status_code=$statusCode}
}
$manifest=[ordered]@{
  schema_version=1
  entry_head=(git rev-parse HEAD)
  entry_index_empty=$true
  authorized_paths=@($authorized | ForEach-Object {Read-Entry $_})
  preexisting_dirty_paths=@($dirty | ForEach-Object {Read-Entry $_})
  central_status_porcelain_v1=$statusLines
}
$out='.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_FIFTH_PLAN_BASELINE.json'
$manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 -LiteralPath $out
if(!(Test-Path -LiteralPath $out -PathType Leaf)){throw 'baseline output missing'}
'PASS T-01 BASELINE_CAPTURED_CONTENT_KIND_GIT_STATE_INDEX'
```

The exact post-write checks are:

```powershell
$baseline=Get-Content -Raw '.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_FIFTH_PLAN_BASELINE.json' | ConvertFrom-Json
$repo=(Resolve-Path '.').Path
$authorized=@('src/planning_lite/governed_executor.py','src/planning_lite/operation_lifecycle.py','src/planning_lite/context.py','src/planning_lite/cli.py','template/.planning/adapters/codex/README.md','tests/test_governed_executor.py','tests/test_operation_lifecycle.py','tests/test_cli.py','tests/test_context_resume.py','tests/test_run_receipts.py','tests/test_system_traversability.py','template/.planning/framework/SHA256SUMS.txt')
$statusLines=@(git -c core.quotepath=false status --porcelain=v1 --untracked-files=all)
$dirty=@($statusLines | ForEach-Object {if($_.Length -ge 3){$_.Substring(3)}} | Sort-Object -Unique)
$observed=@($authorized + @($baseline.preexisting_dirty_paths | ForEach-Object path) | Sort-Object -Unique)
function Read-Entry($rel){
  $q=Join-Path $repo $rel
  if(Test-Path -LiteralPath $q -PathType Leaf){$exists=$true;$kind='file';$sha=(Get-FileHash -Algorithm SHA256 -LiteralPath $q -ErrorAction Stop).Hash.ToLowerInvariant()}
  elseif(Test-Path -LiteralPath $q -PathType Container){$exists=$true;$kind='directory';$sha=$null}
  else{$exists=$false;$kind='absent';$sha=$null}
  $status=$statusLines | Where-Object { $_.Length -ge 3 -and $_.Substring(3) -eq $rel } | Select-Object -First 1
  if($null -ne $status){$code=$status.Substring(0,2);$gitState=if($code -eq '??'){'untracked'}else{'tracked'}; $statusCode=$code}
  else{$null=git ls-files --error-unmatch -- $rel 2>$null; if($LASTEXITCODE -eq 0){$gitState='tracked-clean'}else{$null=git check-ignore --quiet -- $rel 2>$null; $gitState=if($LASTEXITCODE -eq 0){'ignored'}else{'absent'}}; $statusCode='  '}
  [ordered]@{path=$rel;exists=$exists;kind=$kind;sha256=$sha;git_state=$gitState;status_code=$statusCode}
}
$after=@($observed | ForEach-Object {Read-Entry $_})
$baselineMap=@{}; foreach($e in @($baseline.authorized_paths)+@($baseline.preexisting_dirty_paths)){$baselineMap[$e.path]=$e}
$afterMap=@{}; foreach($e in $after){$afterMap[$e.path]=$e}
$unknown=@($dirty | Where-Object {$_ -notin $authorized -and $_ -notin @($baseline.preexisting_dirty_paths.path)})
if($unknown.Count -ne 0){throw "unauthorized paths: $($unknown -join ',')"}
git diff --cached --quiet
if($LASTEXITCODE -ne 0){throw 'index changed'}
foreach($e in @($baseline.preexisting_dirty_paths)){$n=$afterMap[$e.path];if($null -eq $n -or $n.exists -ne $e.exists -or $n.kind -ne $e.kind -or $n.sha256 -ne $e.sha256 -or $n.git_state -ne $e.git_state -or $n.status_code -ne $e.status_code){throw "pre-existing state changed: $($e.path)"}}
if(!(Test-Path -LiteralPath '.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json' -PathType Leaf)){throw 'T-12 evidence missing'}
'CONTENT_SENSITIVE_BASELINE: YES'; 'DETECTS_SECOND_MUTATION_OF_ALREADY_DIRTY_PATH: YES'; 'UNKNOWN_CHANGED_PATH_FAILS: YES'; 'PASS V-25 CONTENT_SENSITIVE_BOUNDARY_AND_PREEXISTING_DIRT_PRESERVED'
```

The ignored T-12 JSON evidence file is not a product path and is checked by
exact name. Any extra product mutation, changed pre-existing byte, changed
object kind, changed tracked/untracked state, changed index, changed central
Git state, source/snapshot hash mismatch, or missing evidence file stops the
plan. Cleanup failure is reported after the product/source assertions and does
not change the product verdict.

### 9.2 Exact T-12 evidence schema and executable V-26 validator

T-12 writes exactly one UTF-8 JSON object to
`.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json`.
Its top-level key set is exactly:

```text
schema_version
entry_identity
candidate_identity
task_receipts
verification_receipts
acceptance_result
closure_result
mutation_audit
change_boundaries
terminal
```

The exact value schemas are:

```text
entry_identity = {head, index_empty, preexisting_dirty_path_count}
candidate_identity = {path, ordinary_sha256, self_excluding_sha256}
task_receipts[] = {task_id, status, evidence_ref}
verification_receipts[] = {verification_id, status, evidence_ref}
acceptance_result = {total, mapped, unmapped, weak}
closure_result = {total, mapped, unmapped, weak, v2_overlays}
mutation_audit = {planned_product_path_count, unknown_changed_paths,
                   preexisting_dirty_preserved, index_empty}
change_boundaries = {change_2, change_3, major_pl09_next_slice_gate}
terminal = {verdict, implementation, formal_readiness}
```

The receipt arrays must contain exactly `T-01` through `T-12` and `V-01`
through `V-26`, in numeric order. Every status is `PASS`; every
`evidence_ref` is the exact JSON Pointer to its own receipt array item
(`#/task_receipts/0` through `#/task_receipts/11`, or
`#/verification_receipts/0` through `#/verification_receipts/25`). This is the
deterministic carrier for every task and verification receipt; no phrase such
as “all task receipts” is an input.

The exact V-26 validator is:

```powershell
$ErrorActionPreference='Stop'
@'
import hashlib, json, re
from pathlib import Path

evidence = Path(".local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json")
candidate = Path(".local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLAN_CANDIDATE.md")
data = json.loads(evidence.read_text(encoding="utf-8"))
assert set(data) == {"schema_version","entry_identity","candidate_identity","task_receipts","verification_receipts","acceptance_result","closure_result","mutation_audit","change_boundaries","terminal"}
assert data["schema_version"] == 1
assert data["entry_identity"] == {"head":"407f4daef02227145a0c807ca182925c76888b60","index_empty":True,"preexisting_dirty_path_count":23}
raw = candidate.read_bytes()
text = raw.decode("utf-8")
ordinary = hashlib.sha256(raw).hexdigest().upper()
self_bytes = re.sub(r"(?m)^FIFTH_CORRECTED_PLAN_SELF_EXCLUDING_SHA256:.*\r?\n", "", text).encode("utf-8")
self_excluding = hashlib.sha256(self_bytes).hexdigest().upper()
assert data["candidate_identity"] == {"path":".local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLAN_CANDIDATE.md","ordinary_sha256":ordinary,"self_excluding_sha256":self_excluding}
tasks = data["task_receipts"]
assert [x["task_id"] for x in tasks] == [f"T-{i:02d}" for i in range(1,13)]
assert all(set(x)=={"task_id","status","evidence_ref"} and x["status"]=="PASS" and x["evidence_ref"]==f"#/task_receipts/{i}" for i,x in enumerate(tasks))
verifications = data["verification_receipts"]
assert [x["verification_id"] for x in verifications] == [f"V-{i:02d}" for i in range(1,27)]
assert all(set(x)=={"verification_id","status","evidence_ref"} and x["status"]=="PASS" and x["evidence_ref"]==f"#/verification_receipts/{i}" for i,x in enumerate(verifications))
assert data["acceptance_result"] == {"total":52,"mapped":52,"unmapped":0,"weak":0}
assert data["closure_result"] == {"total":20,"mapped":20,"unmapped":0,"weak":0,"v2_overlays":9}
assert data["mutation_audit"] == {"planned_product_path_count":12,"unknown_changed_paths":[],"preexisting_dirty_preserved":True,"index_empty":True}
assert data["change_boundaries"] == {"change_2":"BLOCKED / VALID / PAUSED","change_3":"NOT_ABSORBED","major_pl09_next_slice_gate":"PRESERVED / UNCONSUMED"}
assert data["terminal"] == {"verdict":"PASS_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION","implementation":"COMPLETE","formal_readiness":"NOT_RUN"}
print("PASS V-26 T12_SCHEMA_AND_TERMINAL_EVIDENCE")
'@ | uv run --frozen python -
```

## 10. Exact 52-row acceptance traceability

The effective acceptance inventory is 52 individual rows: 12 Executor
predecessor rows, 10 Executor Amendment-v1 rows, 18 Lifecycle predecessor
rows, and 12 Lifecycle Amendment-v1 rows. V2 criteria are attached to the
affected effective rows in §11 and are not silently omitted. Every row below
has an exact requirement, task, surface, verification, expected evidence, and
failure disposition.

| AC ID | Source authority | Exact requirement | Task IDs | Write paths | Read-only surfaces | Verification | Expected evidence | Failure disposition |
|---|---|---|---|---|---|---|---|---|
| E-AC-01 | Executor Definition §30 | importable `invoke_governed_operation` exists | T-03,T-08 | executor + executor test | package entry | V-15,V-17 | import and real route trace | stop; no helper-only claim |
| E-AC-02 | Executor Definition §30 | real current-host path invokes callable and returns typed deterministic result | T-03,T-08 | executor/tests | CLI/package | V-06,V-17 | production binding trace | stop; no mock closure |
| E-AC-03 | Executor Definition §30 | supplied Attempt ID is preserved; cross-Attempt facts reject | T-03,T-04 | executor/lifecycle tests | Runtime types | V-06,V-08,V-16 | identity negative corpus | fail closed |
| E-AC-04 | Executor Definition §30 | supplied OperationGuidance is consumed unchanged | T-03,T-04 | executor/lifecycle | guidance producer | V-05,V-08 | complete guidance object | stop on reselection |
| E-AC-05 | Executor Definition §30 | existing execution authority is consumed, not granted or broadened | T-03,T-04 | executor/lifecycle tests | approval/guidance | V-05,V-19 | predicate/reason separation | stop on authority transfer |
| E-AC-06 | Executor Definition §30 | one call yields one bounded typed result with accepted/rejected and terminal classes | T-03 | executor/tests | contract definitions | V-04,V-06 | typed result matrix | stop on ambiguity |
| E-AC-07 | Executor Definition §30 | same invocation yields exact receipt references without post-hoc matching | T-03,T-04 | executor/lifecycle tests | telemetry | V-09,V-16 | supplied ID/readback trace | stop on latest/time/task lookup |
| E-AC-08 | Executor Definition §30 | missing, invalid, or mismatched receipt fails closed | T-04 | lifecycle/receipt tests | telemetry validator | V-09,V-16 | negative receipt matrix | stop before terminalization |
| E-AC-09 | Executor Definition §30 | no retry, background work, persistence, scheduler, registry, queue, or callback | T-03,T-04,T-08 | executor/lifecycle/tests | Runtime/telemetry | V-07,V-19,V-20 | AST and route evidence | stop and adjudicate |
| E-AC-10 | Executor Definition §30 | Lifecycle can construct ObservedResult and terminalize without moving Runtime authority | T-03,T-04 | executor/lifecycle | Runtime/result types | V-08,V-11 | six-field projection and Runtime call | stop on duplicate owner |
| E-AC-11 | Executor Definition §30 | unavailable host, rejected request, mismatch, invalid result, missing/invalid receipt, association mismatch are covered | T-03,T-04 | executor/lifecycle tests | live owners | V-06,V-09,V-16 | named negative cases | fail closed |
| E-AC-12 | Executor Definition §30 | public result exposes typed facts/references, not storage or next-gate operations | T-03 | executor/tests | telemetry/Spine | V-06,V-19 | field inspection | stop on leakage |
| E1-AC-01 | Executor Amendment-v1 §10 | preparation rejects missing, stale, contradictory, cross-Attempt, unauthorized inputs without facts | T-03,T-04 | executor/lifecycle tests | Runtime/guidance | V-06,V-08,V-16 | precondition matrix | fail before occurrence |
| E1-AC-02 | Executor Amendment-v1 §10 | exact supplied binding is used once | T-03 | executor/tests | guidance | V-05,V-08 | call-count trace | stop on reselection |
| E1-AC-03 | Executor Amendment-v1 §10 | invocation identity is recomputable from envelope | T-03 | executor/tests | canonical codec | V-04 | fixed domain vector | stop on nondeterminism |
| E1-AC-04 | Executor Amendment-v1 §10 | Completion and Result remain typed and identity-bound | T-03,T-04 | executor/lifecycle tests | Result/ObservedResult | V-04,V-10 | typed field assertions | stop on string-only carrier |
| E1-AC-05 | Executor Amendment-v1 §10 | Executor does not call lifecycle, Runtime, receipt, PL08, retry, or callback authority | T-03,T-04 | executor/tests | live owner modules | V-07,V-19 | complete AST proof | stop on forbidden owner |
| E1-AC-06 | Executor Amendment-v1 §10 | Executor has no durable store and uses existing collector only downstream | T-03,T-04 | executor/lifecycle tests | telemetry | V-07,V-09 | owner/import proof | stop on second store |
| E1-AC-07 | Executor Amendment-v1 §10 | exact result/readback/identity triangle is preserved | T-03,T-04 | executor/lifecycle/tests | telemetry | V-09,V-16 | persisted bytes and identities | fail closed |
| E1-AC-08 | Executor Amendment-v1 §10 | invalid receipt fails before accepting downstream context | T-04 | lifecycle/receipt tests | telemetry | V-09,V-16 | negative matrix | stop before terminal |
| E1-AC-09 | Executor Amendment-v1 §10 | false finish is not a typed current-cycle completion | T-05,T-06 | context/CLI/tests | Spine/context | V-14 | semantic negative corpus | reject raw chat authority |
| E1-AC-10 | Executor Amendment-v1 §10 | Pattern B remains a thin bounded route | T-04,T-06,T-08 | lifecycle/CLI/tests | package entry | V-11,V-15,V-20 | route event trace | stop on expansion |
| L-AC-01 | Lifecycle Definition §32 | bounded lifecycle has explicit authorized start and fact-handoff/fail-closed end | T-04,T-08 | lifecycle/tests | Runtime/Spine | V-08,V-17 | real route trace | stop on incomplete end |
| L-AC-02 | Lifecycle Definition §32 | real self-hosted path invokes lifecycle for authorized guidance and existing Attempt | T-04,T-08,T-10 | lifecycle/tests | adapter/package | V-15,V-17,V-24 | adoption and route evidence | no mock closure |
| L-AC-03 | Lifecycle Definition §32 | Attempt ID is sole canonical identity across chain | T-03,T-04 | executor/lifecycle/tests | Runtime/telemetry | V-08,V-09 | identity triangle | stop on second identity |
| L-AC-04 | Lifecycle Definition §32 | existing guidance/authorization is used without authority movement | T-03,T-04 | executor/lifecycle | guidance/approval | V-05,V-19 | complete guidance and AST | stop on transfer |
| L-AC-05 | Lifecycle Definition §32 | execution authority is activated while execution semantics remain outside lifecycle | T-03,T-04 | executor/lifecycle | binding contract | V-08,V-19 | owner call trace | stop on semantic duplication |
| L-AC-06 | Lifecycle Definition §32 | receipt existence, same-Attempt association, and validation are separate facts | T-04 | lifecycle/receipt tests | telemetry | V-09,V-16 | readback/validation evidence | fail first broken seam |
| L-AC-07 | Lifecycle Definition §32 | valid facts reach PL08 without making PL08 a pump | T-04 | lifecycle/tests | evaluator | V-10,V-11,V-21 | direct typed call | stop on evaluation ownership |
| L-AC-08 | Lifecycle Definition §32 | downstream facts reach Spine without lifecycle selecting next gate | T-05,T-06 | context/CLI/tests | CURRENT/resume | V-12,V-14 | exact quote | stop on recommendation |
| L-AC-09 | Lifecycle Definition §32 | missing/broken/unavailable/inadmissible facts stop at first seam | T-04,T-05,T-06 | lifecycle/context/CLI tests | all existing owners | V-09,V-13,V-14,V-16 | fail-closed corpus | stop on invented fallback |
| L-AC-10 | Lifecycle Definition §32 | lifecycle success means coordination/handoff, not Target/Change/PL08/journey PASS | T-04,T-06 | lifecycle/context/tests | Spine/PL08 | V-11,V-14 | semantic result assertions | reject false done |
| L-AC-11 | Lifecycle Definition §32 | Runtime state is bounded in-process; no lifecycle persistence | T-04,T-08 | lifecycle/tests | Runtime | V-07,V-20 | static and integration proof | stop on new store |
| L-AC-12 | Lifecycle Definition §32 | no scheduler, worker, coordinator, or subsystem boundary | T-04,T-07,T-08 | lifecycle/adapter/tests | package/adapter | V-07,V-18,V-20 | owner and path audit | stop on boundary expansion |
| L-AC-13 | Lifecycle Definition §32 | authority matrix unchanged; transfer none | T-01,T-04,T-08 | lifecycle/tests | all authority docs | V-01,V-07,V-19 | hash and AST evidence | stop for owner adjudication |
| L-AC-14 | Lifecycle Definition §32 | retry identity, single-active concurrency, synchronous boundary, and host/process rules follow model without auto-retry | T-04,T-08 | lifecycle/tests | Runtime | V-08,V-11,V-20 | concurrency/order proof | stop on retry owner |
| L-AC-15 | Lifecycle Definition §32 | Change 2 remains blocked/valid/paused and semantic trace persistence stays out of scope | T-07,T-08 | adapter/tests | Spine/checkpoints | V-18,V-20 | boundary scan | stop on absorption |
| L-AC-16 | Lifecycle Definition §32 | Change 3 measurement correction is not a prerequisite | T-01,T-08 | tests/evidence | roadmap/checkpoints | V-01,V-20 | authority inventory | stop on dependency drift |
| L-AC-17 | Lifecycle Definition §32 | local and System Traversability proof reaches required wired delta without premature PASSING | T-07,T-08,T-10 | adapter/system tests | package/doctor | V-17,V-18,V-24 | real adoption/doctor trace | stop on mock-only proof |
| L-AC-18 | Lifecycle Definition §32 | helper without production binding, continuity, receipt, PL08, and next-gate proof is not accepted | T-04,T-08,T-09,T-10 | lifecycle/system/tests | all owners | V-17,V-22,V-24,V-26 | complete receipt | stop closure |
| L1-AC-01 | Lifecycle Amendment-v1 §11 | same `IN_FLIGHT` Attempt continues across bounded agent interactions | T-04 | lifecycle/tests | Runtime | V-08,V-11 | reentry trace | stop on new identity |
| L1-AC-02 | Lifecycle Amendment-v1 §11 | completion is explicit before final human-facing claim | T-04,T-06 | lifecycle/CLI/tests | context/Spine | V-11,V-14 | order trace | reject premature finish |
| L1-AC-03 | Lifecycle Amendment-v1 §11 | exact prepare/work/completion/readback/terminal/PL08/continuation sequence is enforced | T-04 | lifecycle/tests | Runtime/telemetry/PL08 | V-08,V-09,V-10,V-11 | single order assertion | stop on branch reorder |
| L1-AC-04 | Lifecycle Amendment-v1 §11 | missing, stale, cross-Attempt, invalid, incomplete facts fail at first seam | T-04 | lifecycle/receipt tests | owners | V-09,V-16 | negative matrix | fail closed |
| L1-AC-05 | Lifecycle Amendment-v1 §11 | lifecycle does not authorize, reselect guidance, allocate Attempt, redefine receipt, evaluate, or choose gate | T-04,T-05 | lifecycle/context tests | owners | V-07,V-11,V-12,V-19 | AST/order/quote evidence | stop on authority movement |
| L1-AC-06 | Lifecycle Amendment-v1 §11 | no persistent process, scheduler, worker, queue, daemon, or callback is required | T-04,T-07,T-08 | lifecycle/adapter/tests | package/adapter | V-07,V-18,V-20 | static/path proof | stop on host dependency |
| L1-AC-07 | Lifecycle Amendment-v1 §11 | finish intent is semantic and nonauthorizing; raw owner chat is not lifecycle state | T-05,T-06 | context/CLI/tests | Spine | V-14,V-20 | semantic negative corpus | reject chat authorization |
| L1-AC-08 | Lifecycle Amendment-v1 §11 | status is read-only and uses existing resume/project-state projection | T-05,T-06 | context/CLI/tests | resume/Runtime | V-12,V-13,V-14 | no-diff status probe | stop on mutation |
| L1-AC-09 | Lifecycle Amendment-v1 §11 | token/depth use exact, explicit approximation, or unavailable truth | T-05 | context/tests | PL06 observation producer | V-13 | source-marked values | stop on invented precision |
| L1-AC-10 | Lifecycle Amendment-v1 §11 | Change 2/3 remain separate and Stop hook has no production role | T-07,T-08 | adapter/system tests | checkpoints/adapter | V-18,V-20 | boundary scan | stop on absorption/hook |
| L1-AC-11 | Lifecycle Amendment-v1 §11 | Executor closure remains dependent on integrated Lifecycle proof | T-08,T-09,T-10 | system/tests | executor/lifecycle | V-22,V-24,V-26 | integrated receipt | no isolated closure |
| L1-AC-12 | Lifecycle Amendment-v1 §11 | Changes remain distinct; merge is not required | T-01,T-07,T-08 | adapter/evidence | authority records | V-01,V-18,V-20 | boundary evidence | stop and ask owner |

`EFFECTIVE_AC_TOTAL: 52`; `EFFECTIVE_AC_MAPPED: 52`;
`EFFECTIVE_AC_UNMAPPED: 0`; `EFFECTIVE_AC_WEAK: 0`.

## 11. Closure criteria and amendment overlays

The twenty closure rows are individually mapped below. The nine v2 overlays
are then mapped to exact base rows; each has its own evidence and failure
disposition.

| CC ID | Exact closure chain |
|---|---|
| E-CC-01 | callable plus real host path -> T-03,T-08 -> V-15,V-17 -> import and route trace |
| E-CC-02 | envelope and invocation identity -> T-03 -> V-04 -> fixed vector |
| E-CC-03 | invalid preparation and admissibility -> T-03,T-04 -> V-06,V-08,V-16 -> negative evidence |
| E-CC-04 | one guidance and bounded occurrence -> T-03,T-04 -> V-05,V-08 -> call-count trace |
| E-CC-05 | forbidden authority negatives -> T-03,T-04,T-08 -> V-07,V-19,V-20 -> AST and route proof |
| E-CC-06 | typed completion/result/evidence -> T-03,T-04 -> V-04,V-10 -> field and carrier proof |
| E-CC-07 | collector ownership and readback -> T-04 -> V-09,V-16 -> persisted bytes |
| E-CC-08 | identity triangle and order -> T-04 -> V-08,V-09,V-11 -> event trace |
| E-CC-09 | false-done and status boundaries -> T-05,T-06 -> V-12,V-13,V-14 -> semantic/no-diff proof |
| E-CC-10 | focused and full regression -> T-09 -> V-22,V-23 -> test receipts |
| L-CC-01 | closed authority and prerequisites -> T-01 -> V-01,V-02 -> ledger |
| L-CC-02 | real self-hosted traversal -> T-08,T-10 -> V-17,V-24 -> adoption/doctor |
| L-CC-03 | Runtime continuity/state owner -> T-04 -> V-07,V-08,V-11 -> direct calls |
| L-CC-04 | PL07 guidance owner -> T-03,T-04 -> V-05,V-07 -> complete vector/AST |
| L-CC-05 | telemetry receipt owner -> T-04 -> V-09,V-16 -> supplied ID/readback |
| L-CC-06 | Spine next-action owner -> T-05,T-06 -> V-12,V-14 -> exact quote |
| L-CC-07 | six-field read-only status -> T-05,T-06 -> V-12,V-13,V-14 -> matrix/no-diff |
| L-CC-08 | evidence before terminal and PL08 -> T-04 -> V-08,V-09,V-10,V-11 -> order |
| L-CC-09 | exact depth/token or unavailable -> T-05 -> V-13 -> producer evidence |
| L-CC-10 | scope, dirt, adoption boundaries -> T-09,T-10,T-11,T-12 -> V-24,V-25,V-26 -> byte receipt |

| Overlay | Base rows | Exact requirement | Tasks/surface | Verification/evidence | Failure |
|---|---|---|---|---|---|
| AC-E2-01 | E-AC-03,E1-AC-03 | recomputable domain-separated invocation anchors downstream receipt binding | T-03 / executor | V-04 fixed projection/domain/NUL vector | reject random/guessed identity |
| AC-E2-02 | E-AC-06,E-AC-10,E1-AC-04 | Result exposes exact Attempt and invocation identities and typed observation | T-03,T-04 / executor+lifecycle | V-04,V-08,V-10 six-field/identity assertions | reject substitution or string-only carrier |
| AC-E2-03 | E-AC-07,E-AC-09,E1-AC-06 | Executor produces result before receipt collection and has no receipt authority | T-03,T-04 / executor+lifecycle | V-07,V-09 owner and readback proof | stop on Executor collection/persistence |
| AC-L2-01 | L-AC-02,L-AC-17 | governed terminalization uses only governed receipt v2; v1 is not fallback | T-04,T-08,T-10 / lifecycle/system | V-16,V-17,V-24 legacy negative and real route | fail closed on v1 fallback |
| AC-L2-02 | L-AC-03,L-AC-06 | lifecycle supplies authoritative Attempt and verified invocation separately to collector | T-04 / lifecycle | V-09 supplied identity/readback trace | reject external override |
| AC-L2-03 | L-AC-03,L-AC-06 | receipt has schema v2 and exact Attempt identity | T-04 / lifecycle+receipt tests | V-09,V-16 same-Attempt checks | reject cross-Attempt |
| AC-L2-04 | L-AC-03,E1-AC-03 | receipt invocation equals recomputed canonical envelope identity | T-03,T-04 / envelope+lifecycle | V-04,V-09 identity triangle | reject cross-invocation |
| AC-L2-05 | L-AC-06,L1-AC-03 | append is followed by exact stored readback and result/Attempt consistency | T-04 / lifecycle | V-09,V-11 persisted bytes/order | reject pre-readback terminalization |
| AC-L2-06 | L-AC-09,L1-AC-03 | cross-identity, legacy, external, latest/time/task, and pre-readback substitutions fail closed | T-04,T-05 / lifecycle/context | V-09,V-11,V-16 negative corpus | stop at first broken seam |

`EFFECTIVE_CC_TOTAL: 20`; `EFFECTIVE_CC_MAPPED: 20`;
`EFFECTIVE_CC_UNMAPPED: 0`; `CC_V2_OVERLAY_ROWS: 9`;
`CC_V2_OVERLAY_UNMAPPED: 0`; `V2_OVERLAY_CC_DOUBLE_COUNTING: NO`.

## Canonicalization provenance

```text
CANONICAL_PLAN_SEMANTIC_DELTA_FROM_REVIEWED_CANDIDATE: NONE
NORMATIVE_BODY_SOURCE_RANGE: CANDIDATE_SECTIONS_2_THROUGH_11
FORMAL_READINESS: NOT_RUN
IMPLEMENTATION_AUTHORIZED: NO
```
