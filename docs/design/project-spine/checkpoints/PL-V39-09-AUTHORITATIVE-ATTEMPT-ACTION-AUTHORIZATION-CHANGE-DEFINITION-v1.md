# PL-V39-09 Authoritative Attempt Action Authorization - Approved Definition v1

Status: APPROVED_BY_OWNER

This canonical Definition is the approved scope authority for
CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001. It preserves
the approved semantics of the corrected candidate and does not authorize
Implementation Planning, Formal Readiness, implementation, Attempt Runtime
work, executor work, lifecycle resumption, staging, commit, or push.

Canonicalization semantic delta: NONE. Only canonical metadata, lineage,
status, and mechanical document framing are added; the approved semantic body
is preserved.

## 1. CHANGE IDENTITY AND APPROVAL

```text
DOCUMENT_ID: PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-DEFINITION-001
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001
CHANGE_NAME: Authoritative Attempt Action Authorization
STATUS: APPROVED_BY_OWNER
OWNER_APPROVAL: APPROVE_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_CHANGE_DEFINITION
DEFINITION_DECISION: APPROVE_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_CHANGE_DEFINITION
INDEPENDENT_REVIEW: PASS
MATERIAL_FINDINGS: 0
NONBLOCKING_FINDINGS: 0
IMPLEMENTATION_AUTHORIZED: NO
PLANNING_AUTHORIZED: NO
IMPLEMENTATION_PLAN: NOT_CREATED
FORMAL_READINESS: NOT_RUN
SOURCE_CANDIDATE: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_CHANGE_DEFINITION_CANDIDATE_CORRECTED.md
SOURCE_CANDIDATE_SHA256: 6B8150E185F3AE45073C4957DB54B59AB455D3C25883DB5DCD717CECA32DF443
CORRECTED_FRESH_REVIEW: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_CORRECTED_CHANGE_DEFINITION_FRESH_REVIEW.md
CORRECTED_FRESH_REVIEW_SHA256: DD6DDD4E3AFB82F576AEC00F1B42A0244B284E16CE4D04128ACF723F603D41DF
ORIGINAL_CANDIDATE_SHA256: F031B189571DEA890CCF8BC9EA50CB3970D17088DA169F1B4D07CF7EA17BC50D
FIRST_FRESH_REVIEW_SHA256: C57830540C706F6A3A311A24C00F9B47301EAA665476D740FA1934AD998CE550
TRUST_BOUNDARY_ADJUDICATION_SHA256: FB786E2D4B275E56A4A961A49431DCC07503788A6D8F3A08771C517B226250FC
BASELINE_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
CANONICALIZATION_SEMANTIC_DELTA: NONE
ACTIVATION: DEFINITION_APPROVED / PLANNING_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED
NEXT_GATE: OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLANNING
```

This Definition freezes the bounded PL09 prerequisite. Its activation does not
authorize Planning or implementation.

## 2. APPROVED SEMANTIC DEFINITION

## CHANGE IDENTITY

CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001

CHANGE_TITLE: Authoritative Attempt Action Authorization

CHANGE_CLASS: BOUNDED PL09 PREREQUISITE

SEMANTIC_OWNER: PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_AUTHORITY

ACTION_AUTHORIZATION_GAP: WIRING_GAP

DEFINITION_CORRECTION_MODE: CORRECT_DEFINITION_IN_PLACE

This corrected candidate preserves the original Change identity and all
previously passing semantic decisions. It corrects only the adjudicated
trusted-local control-plane issuance boundary. It is not canonical and does
not authorize Planning or implementation.

## AUTHORITY AND LINEAGE

Correction authorization:

`OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_DEFINITION_CORRECTION`

Owner decision:

`AUTHORIZE_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_DEFINITION_CORRECTION`

Historical lineage:

- original candidate, self-excluding SHA256
  `F031B189571DEA890CCF8BC9EA50CB3970D17088DA169F1B4D07CF7EA17BC50D`;
- fresh independent review, self-excluding SHA256
  `C57830540C706F6A3A311A24C00F9B47301EAA665476D740FA1934AD998CE550`;
- trust-boundary adjudication, self-excluding SHA256
  `FB786E2D4B275E56A4A961A49431DCC07503788A6D8F3A08771C517B226250FC`.

The original candidate remains historical failed-review evidence and is not
mutated or overwritten. The fresh review remains historical review evidence.

MF-01:
`CLOSED_BY_TRUSTED_LOCAL_OWNER_CONTROL_PLANE`

This candidate carries the adjudication's binding resolution:

- `TRUST_ROOT: TRUSTED_LOCAL_OWNER_CONTROL_PLANE`;
- `LOCAL_CONTROL_PLANE_TRUST_BOUNDARY: DEFINED`;
- `OWNER_DECISION_EVENT: EXPLICIT_LOCAL_CONTROL_PLANE_ISSUANCE`;
- `HUMAN_AUTHENTICATION_SUBSYSTEM_REQUIRED: NO`;
- `UNBOUND_ARCHITECTURE_CHOICES: 0`;
- `UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0`.

## CAUSAL INPUT

The upstream findings adjudication established `AUTHORITY_SOURCE_CLASS: C`:
owner/gate authority semantics exist, but no durable typed machine-resolvable
authorization record/resolver exists. The fresh review found exactly one
material omission: the local trust root for explicit issuance.

The original candidate's accepted semantics remain unchanged: exact two
actions, exact scopes, immutable records, no v1 revocation, downstream
single-use enforcement, no cross-store transaction, and independent closure.

## PROBLEM STATEMENT

Planning Lite can carry `authorization_ref` provenance and humans can perform
owner/gate actions, but runtime cannot prove that a supplied reference exists
in one authoritative source, represents an explicit decision, authorizes the
requested action, and applies to the exact Change/task or Attempt scope.

The corrected Definition additionally makes the issuance trust model explicit:
the supported authority event is a deliberate local owner/control-plane
invocation with explicit target, action, and exact scope. This does not claim
to authenticate a human against an already-compromised equivalent-authority
local environment.

`AUTHORIZATION_REF_PROVENANCE != AUTHORIZATION_PROOF`

`DECISION_PROVENANCE_REF_ALONE != AUTHORIZATION`

## PURPOSE

Define the smallest bounded PL09 capability that:

- materializes an explicit owner/control decision through one trusted local
  production control-plane issuance path;
- persists one durable strict typed authorization record;
- returns a stable `authorization_ref`;
- binds one exact supported action and exact scope;
- resolves that record deterministically;
- proves action/scope applicability;
- fails closed for invalid, absent, malformed, conflicting, mismatched, or
  implicitly requested authority; and
- does not become a human-authentication, policy, identity, execution, or
  orchestration subsystem.

## SCOPE

This Change owns:

- the trusted-local control-plane trust root for v1 issuance;
- one explicit owner-facing production issuance adapter contract;
- one bounded authoritative record source;
- strict versioned authorization records and stable opaque references;
- exactly two Attempt-related action types;
- exact action-specific scope contracts;
- shared decode/resolution with action-specific validators;
- immutable/no-revocation v1 semantics;
- a single-successful-use contract enforced downstream by Attempt Runtime;
- explicit no-default, no-implicit, no-runtime-self-issuance boundaries;
- local adversary and cryptographic-authenticity boundaries; and
- independent closure proof for this bounded issuance-to-resolution seam.

## OUT OF SCOPE

This Change does not create or own:

- login, passwords, MFA, OAuth, certificates, cryptographic identities,
  signatures, MACs, remote identity providers, user/account/role databases, or
  process sandboxes;
- protection against malicious equivalent-OS-principal processes,
  compromised local interpreters, administrators/root, hostile direct edits by
  trusted local principals, or stolen OS accounts;
- Attempt identity allocation, persistence, state, claim, materialization,
  terminalization, or recovery mutation;
- execution authority, executor invocation, RunReceipt, lifecycle sequencing,
  retry, scheduling, route/guidance selection, or PL08 orchestration;
- RBAC, ACLs, roles, wildcard resources, policy languages, generic capability
  tokens, generalized workflow authorization, or arbitrary action extension;
- Change-2 semantic operation traces, Change-3 measurements, or a new Roadmap
  vertebra.

## DEPENDENCY POSITION

The frozen topology remains:

`CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001`

-> `CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001` Plan correction and implementation

-> `CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001`

-> `CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001` Planning resume.

No split, new prerequisite, security subsystem, policy subsystem, or Roadmap
vertebra is introduced.

## DECISION AUTHORITY

DECISION_AUTHORITY_PREPARATION:
`EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY`

DECISION_AUTHORITY_RECOVERY:
`EXISTING_OWNER/LIFECYCLE_CONTROL_AUTHORITY`

These existing authorities decide whether the exact preparation or recovery
action should happen. The trusted local control plane enacts that decision; it
does not transfer decision authority to the machine record owner.

## MACHINE RECORD AUTHORITY

MACHINE_AUTHORIZATION_RECORD_AUTHORITY:
`PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_AUTHORITY`

`AUTHORIZATION_RECORD_AUTHORITY != AUTHORIZATION_DECISION_AUTHORITY`

The machine authority may validate, persist, resolve, and enforce exact
applicability. It may not decide whether preparation, recovery, execution, or
retry should occur, and it may not use ordinary runtime calls to mint a new
authorization.

## AUTHORIZATION_REF CONTRACT

`authorization_ref` is stable, durable, opaque with respect to authority
semantics, unique within the one authoritative source, and resolvable only
through that source:

`ONE_AUTHORIZATION_REF -> AT_MOST_ONE_AUTHORITATIVE_ACTION_AUTHORIZATION_RECORD`

The existing `AttemptRecordV1.authorization_ref` field is reused. “Reusable”
means reusable as immutable provenance/binding in the Attempt record; it does
not mean reusable for multiple successful mutations.

ATTEMPT_AUTHORIZATION_REF_REUSABLE: YES

## SUPPORTED ACTION TYPES

V1 supports exactly two closed-enum actions:

1. `OWNER_AUTHORIZED_ATTEMPT_PREPARATION`;
2. `OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION`.

Unknown values and arbitrary caller-provided action strings fail closed. Adding
a third materially different action requires a governed Definition change.

SUPPORTED_ACTION_TYPE_COUNT: 2

## PREPARATION ACTION SCOPE

`OWNER_AUTHORIZED_ATTEMPT_PREPARATION` binds exactly:

- `change_id`;
- `task_or_operation_id`;
- the preparation action type.

The scope is intentionally operation-scoped under existing owner/gate
semantics. Candidate identity, acceptance contract, baseline, and other
immutable Attempt provenance remain separately validated materialization inputs;
this authorization is not silently candidate-version-specific.

No wildcard, latest, current, inferred, or omitted scope is permitted.

PREPARATION_ACTION: OWNER_AUTHORIZED_ATTEMPT_PREPARATION

PREPARATION_SCOPE: exact change_id + exact task_or_operation_id

## RECOVERY ACTION SCOPE

`OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION` binds exactly:

- `attempt_id`;
- the action `IN_FLIGHT -> TERMINAL(INTERRUPTED)`.

There is no wildcard, latest Attempt, Change-wide, or task-wide recovery
authorization.

RECOVERY_ACTION: OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION

RECOVERY_SCOPE: exact attempt_id

## AUTHORIZATION ISSUANCE

The semantic creation event is:

`EXPLICIT_OWNER_ACTION_AUTHORIZATION_ISSUANCE`

The corrected v1 trust binding gives that event the precise authority meaning:

OWNER_DECISION_EVENT: `EXPLICIT_LOCAL_CONTROL_PLANE_ISSUANCE`

A deliberate invocation of the dedicated owner-facing production control-plane
adapter, against an explicit target/project, with one exact supported action
and its complete exact scope, is the owner/control decision event itself. The
adapter persists the typed immutable record and returns its stable reference.

The issuance event is not merely a low-level persistence call and does not
require another machine authorization. It is the bounded control-plane root
action; requiring prior authorization for issuance would create infinite
regress.

## TRUST ROOT AND LOCAL ENVIRONMENT

TRUST_ROOT: `TRUSTED_LOCAL_OWNER_CONTROL_PLANE`

`TRUSTED_LOCAL_CONTROL_PLANE` is the explicit human-facing Planning Lite
control surface used for owner-authority actions against a deliberately
selected target/project. It is distinct from normal runtime/domain APIs,
startup/resume behavior, derived routing, and persistence internals.

LOCAL_CONTROL_PLANE_TRUST_BOUNDARY: DEFINED

LOCAL_ENVIRONMENT_TRUST_ANCHOR:
`OS_ACCOUNT + LOCAL_PLANNING_LITE_CONTROL_ENVIRONMENT + TARGET_ACCESS`

Planning Lite v1 assumes that the human/process deliberately invoking this
surface operates within the trusted local OS account, local Planning Lite
control environment, and selected target/project access boundary. Planning Lite
does not independently authenticate that human.

This means the supported product authority path is explicit control-plane
issuance. It does not mean that every process able to write a file or call an
internal function is a supported owner authority.

## HUMAN IDENTITY AND ADVERSARY BOUNDARY

PLANNING_LITE_HUMAN_IDENTITY_AUTHENTICATION: OUT_OF_SCOPE_V1

HUMAN_AUTHENTICATION_SUBSYSTEM_REQUIRED: NO

V1 does not add login, passwords, MFA, OAuth, certificates, cryptographic
identity, remote IdP, user/account/role databases, signatures, MACs, or process
isolation.

LOCAL_ADVERSARY_EXCLUSIONS: DEFINED

V1 does not claim to defend authorization authenticity against:

- malicious processes already running with equivalent OS/project permissions;
- a compromised local Python/runtime environment;
- root/administrator-equivalent actors;
- direct hostile modification by an already-trusted local OS principal; or
- theft/impersonation of the trusted local OS account.

Those are Architecture STOP conditions if later made v1 requirements. They do
not create alternate authority in this Definition.

CRYPTOGRAPHIC_RECORD_AUTHENTICITY: OUT_OF_SCOPE_V1

Strict decoding, uniqueness, integrity, and corruption checks provide
deterministic product behavior, not cryptographic authorship proof against an
equivalent-authority local actor.

## EXPLICIT ISSUANCE REQUIREMENTS

Every production issuance must deliberately provide or confirm:

- explicit target/project using normal explicit target conventions;
- one supported action type;
- complete action-specific exact scope.

Preparation explicitly provides `change_id` and `task_or_operation_id`.
Recovery explicitly provides `attempt_id`.

AUTHORIZATION_ACTION_DEFAULT: NONE

AUTHORIZATION_SCOPE_DEFAULT: NONE

No action, target, Change, task, operation, Attempt, latest, current, or
wildcard value is inferred from mutable routing or runtime state.

## AUTHORITATIVE SOURCE

Exactly one durable, deterministic, target/project-scoped source is
machine-authoritative. It is inspectable, strictly decoded, conflict-failing,
and safe to materialize. Storage carrier, serialization, path, locking, and
write mechanics remain Plan-level.

Each immutable record contains only:

- schema version;
- `authorization_ref`;
- exact closed-enum action type;
- discriminated exact scope;
- action-appropriate decision authority class;
- `decision_outcome: AUTHORIZED`;
- `decision_provenance_ref`.

No status, consumption state, Attempt state, execution state, receipt, trace,
lifecycle continuation, or evaluation data belongs in this source.

AUTHORITATIVE_AUTHORIZATION_SOURCE_REQUIRED: YES

## MACHINE RESOLUTION

The shared resolver receives `authorization_ref`, exact requested action type,
and exact requested action-specific scope. It returns `AUTHORIZED` or a small
objective fail-closed rejection set:

- `INVALID_REFERENCE`;
- `NOT_FOUND`;
- `CORRUPT_CONFLICT`;
- `WRONG_ACTION`;
- `WRONG_SCOPE`.

`AUTHORIZED` means issued, decoded, exact-action, exact-scope applicability.
It does not mean unused. Downstream Attempt Runtime owns the separate prior-use
conjunct.

AUTHORITY_VALIDATION_SHAPE: SHARED_CORE_WITH_ACTION_SPECIFIC_VALIDATION

## ACTION APPLICABILITY

Applicability requires:

1. authoritative typed-record resolution; and
2. downstream consumer single-use admissibility.

Preparation and recovery authorizations cannot substitute for one another. A
preparation record for another Change/task or a recovery record for another
Attempt fails closed.

## REPLAY / REUSE SEMANTICS

PREPARATION_AUTHORIZATION_REUSE:
SINGLE_USE_PER_SUCCESSFUL_ATTEMPT_MATERIALIZATION

RECOVERY_AUTHORIZATION_REUSE:
SINGLE_USE_PER_SUCCESSFUL_INTERRUPTED_TERMINALIZATION

The authorization source remains immutable. The downstream Attempt Runtime
checks prior use and performs its intended mutation within one authoritative
Attempt-store boundary. A failed validation or crash before downstream commit
does not consume the reference; a committed successful mutation makes reuse
detectable and forbidden.

AUTHORIZATION_USE_ENFORCEMENT_OWNER:
PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY

## REVOCATION SEMANTICS

AUTHORIZATION_RECORD_MUTABILITY: IMMUTABLE

REVOCATION_REQUIRED_IN_V1: NO

No canonical withdrawal/current-state semantics exist. The owner exercises
agency by deciding whether to issue the exact authorization. Once issued, the
record remains valid for its exact scope until one successful downstream use.
Deleting, overwriting, or shadowing an immutable record is not revocation.
Future owner-withdrawal semantics require a separately governed Definition.

OWNER_AGENCY_PRESERVED: YES

## CROSS-STORE TRANSACTION BOUNDARY

CROSS_STORE_ATOMIC_TRANSACTION_REQUIRED: NO

The authorization source is read-only during consumption. The resolver proves
record validity and applicability; Attempt Runtime atomically checks its own
prior-use records and mutates its own store. No distributed transaction,
mutable authorization consumption state, or compensation protocol is required.

## DECISION PROVENANCE

DECISION_PROVENANCE_REQUIRED: YES

`decision_provenance_ref` provides audit lineage to the owner decision, gate,
or governance context. It does not authorize anything by itself:

`DECISION_PROVENANCE_REF_ALONE != AUTHORIZATION`

The typed authoritative record created through explicit trusted-local issuance
is required. Runtime does not reparse arbitrary provenance prose.

RUNTIME_PROSE_PARSING: FORBIDDEN

## IMPLICIT ISSUANCE PROHIBITION

IMPLICIT_ISSUANCE: FORBIDDEN

No authorization may be minted automatically from `CURRENT.md`,
`.planning/ACTIVE.md`, Definition or Plan approval, startup, resume, Attempt
preparation, Attempt recovery, error fallback, test fixtures, resolver, lookup,
or any other runtime/domain consumer. Missing action, missing scope,
unsupported action, malformed request, and inferred/current/latest scope write
no record.

## RUNTIME SELF-ISSUANCE PROHIBITION

RUNTIME_SELF_ISSUANCE: FORBIDDEN

Attempt Runtime, lifecycle, executor, resolver, lookup, claim, preparation,
recovery, and terminalization consumers may resolve/consume valid records but
may not invoke the issuer or persistence writer to mint authorization.

UNATTENDED_RUNTIME_AUTO_ISSUANCE: FORBIDDEN

V1 has no scheduler, watcher, lifecycle hook, unattended runtime issuer, or
hidden alternate production issuer.

PROCESS_ISOLATION_REQUIRED: NO

The Definition does not claim that hostile same-principal local Python code
cannot technically call an internal function. Product authority is conferred
only by the supported explicit control-plane path under the declared trusted
local model.

## CURRENT / ACTIVE / LOCAL ARTIFACT BOUNDARIES

`CURRENT.md` and `.planning/ACTIVE.md` are mutable routing/current-state
pointers, not historical authorization sources. `.local/work/experiments/**`
is noncanonical evidence and cannot issue or resolve runtime authority.

Runtime must not search Git history, arbitrary checkpoint prose, chat
transcripts, Attempt state, RunReceipt, or evidence stores for authorization.

CURRENT_IS_RUNTIME_AUTHORIZATION_SOURCE: NO

ACTIVE_IS_RUNTIME_AUTHORIZATION_SOURCE: NO

LOCAL_ARTIFACTS_CAN_AUTHORIZE_RUNTIME: NO

## ATTEMPT RUNTIME BOUNDARY

The downstream Attempt Runtime consumes preparation authorization before identity
allocation/materialization and recovery authorization before
`IN_FLIGHT -> TERMINAL(INTERRUPTED)`. It owns successful-mutation use
enforcement.

This Change does not implement an Attempt store, `AttemptRuntimeRecordV1`,
identity allocation, materialization, claim, terminalization, or owner recovery.

ATTEMPT_RUNTIME_IMPLEMENTATION_INCLUDED: NO

ATTEMPT_RUNTIME_INDEPENDENT_CLOSURE: YES

## EXECUTOR / LIFECYCLE BOUNDARY

No executor, RunReceipt, execution-end fact, callable binding, lifecycle
continuation, retry, or scheduler is required for closure.

EXECUTOR_DEPENDENCY: NO

LIFECYCLE_DEPENDENCY: NO

## PL08 BOUNDARY

PL08 remains evaluation/contract context only. No PL08 runtime orchestration,
measurement authority, or pump is created.

PL08_RUNTIME_ORCHESTRATION_CREATED: NO

## CHANGE-2 / CHANGE-3 BOUNDARIES

CHANGE2_SCOPE_SEPARATION: HARD_BOUNDARY

CHANGE3_REQUIRED: NO

Authorization records are not semantic operation traces, generalized history,
or evaluation measurements.

## SYSTEM TRAVERSABILITY OBLIGATION

The bounded seam is:

explicit trusted local owner/control-plane issuance

-> typed immutable authorization record

-> machine resolver

-> exact action/scope applicability result.

Closure must use the real production control-plane issuer and real resolver,
plus negative proof that resolver, lookup, startup/resume, malformed/incomplete
requests, unsupported actions, and runtime consumers do not issue records.

The seam closes independently of Attempt Runtime. It does not close Attempt
materialization, recovery, executor, or lifecycle traversal.

## EXPECTED GAP DELTA

Before:

`HUMAN/GOVERNANCE_AUTHORITY_ONLY / MACHINE_UNRESOLVABLE`

After:

`MACHINE_RESOLVABLE_SCOPED_ATTEMPT_ACTION_AUTHORIZATION_AVAILABLE`

The next broken seam remains the downstream Attempt Runtime Plan correction and
implementation binding. No Attempt-access claim is made.

## FALSE-DONE RESISTANCE

The following are insufficient:

- accepting a non-empty or syntactically plausible reference;
- parsing CURRENT/ACTIVE/local artifacts or arbitrary governance prose;
- using a library persistence helper as authority;
- directly seeding records or constructing fixtures without real issuance;
- omitting action or scope or defaulting either value;
- implicit, startup, resume, error, unattended, or runtime issuance;
- runtime consumers self-issuing while consuming;
- generic action strings, wildcard/latest scope, or cross-action reuse;
- cryptographic-authenticity claims not in v1;
- requiring Attempt Runtime to close this prerequisite; or
- claiming downstream Attempt access is closed.

LOW_LEVEL_HELPER_OR_SEEDED_RECORD_WITHOUT_REAL_CONTROL_PLANE_ISSUANCE:
INCOMPLETE

## DEFINITION-LEVEL SURFACE

The maximum semantic surface is:

1. `TRUSTED LOCAL OWNER/CONTROL-PLANE TRUST ROOT`
2. `LOCAL ENVIRONMENT TRUST ANCHOR`
3. `OWNER DECISION EVENT`
4. `AUTHORIZATION DECISION PROJECTION`
5. `DURABLE ACTION AUTHORIZATION SOURCE`
6. `STABLE AUTHORIZATION REF`
7. `EXACT ACTION TYPE`
8. `EXACT SCOPE`
9. `PRODUCTION ISSUANCE`
10. `MACHINE RESOLUTION`
11. `ACTION-SPECIFIC APPLICABILITY`
12. `REPLAY/REUSE CONTRACT`
13. `REVOCATION CONTRACT: IMMUTABLE / NO V1 REVOCATION`
14. `EXPLICIT NO-DEFAULT / NO-IMPLICIT / NO-RUNTIME-SELF-ISSUANCE`
15. `LOCAL THREAT AND CRYPTOGRAPHIC-AUTHENTICITY BOUNDARY`
16. `FAIL-CLOSED VALIDATION`

Planning may select only mechanically equivalent implementation details within
this surface and may not silently enlarge it.

## ACCEPTANCE CRITERIA

The original 22 criteria are preserved with the following exact mapping:

| Original | Corrected treatment |
|---|---|
| AC-01 | unchanged: existing decision authorities remain authoritative |
| AC-02 | strengthened: record authority cannot self-authorize or self-issue |
| AC-03 | unchanged: one durable authoritative source |
| AC-04 | unchanged: stable reusable opaque reference |
| AC-05 | unchanged: exactly two closed-enum actions |
| AC-06 | unchanged: exact preparation scope |
| AC-07 | unchanged: exact recovery scope |
| AC-08 | strengthened: real trusted production issuer; helper is not authority |
| AC-09 | strengthened: explicit action/scope, no defaults or implicit issuance |
| AC-10 | unchanged: minimum strict typed record |
| AC-11 | unchanged: shared resolver/action-specific validation |
| AC-12 | unchanged: invalid, absent, malformed, conflict rejection |
| AC-13 | unchanged: wrong action rejection |
| AC-14 | unchanged: wrong scope rejection |
| AC-15 | strengthened: routing/local/prose are not authority and cannot issue |
| AC-16 | unchanged: immutable/no-revocation v1 |
| AC-17 | unchanged: preparation single-use contract |
| AC-18 | unchanged: recovery single-use contract |
| AC-19 | unchanged: downstream use owner/no cross-store transaction |
| AC-20 | strengthened: no authentication/security/policy/Roadmap expansion |
| AC-21 | strengthened: real issuer/resolver and trust-boundary proof |
| AC-22 | unchanged: bounded issuance-to-resolution traversability delta |

AC-01. Existing owner/gate governance remains the preparation decision
authority and existing lifecycle control remains the recovery decision
authority.

AC-02. The machine record authority owns only the bounded record/source/
resolution capability and cannot self-authorize or self-issue.

AC-03. Exactly one durable target/project-scoped authoritative source owns the
typed records and one reference maps to at most one record.

AC-04. Production issuance returns a stable opaque reference that is
machine-resolvable and reusable in `AttemptRecordV1.authorization_ref`.

AC-05. V1 accepts exactly two closed-enum action types and rejects unknown or
arbitrary actions.

AC-06. Preparation authorization binds exact action, `change_id`, and
`task_or_operation_id` without wildcard/current/latest scope.

AC-07. Recovery authorization binds exact action, exact `attempt_id`, and only
`IN_FLIGHT -> TERMINAL(INTERRUPTED)`.

AC-08. A real trusted local owner/control-plane production adapter issues the
typed record; a low-level helper or direct test seeding is not authority.

AC-09. Issuance requires explicit target/action/scope and is never inferred,
defaulted, implicit, unattended, or runtime-generated.

AC-10. The strict versioned record contains reference, action, discriminated
scope, decision-authority class, authorized outcome, and provenance only.

AC-11. A shared resolver with action-specific validators returns deterministic
`AUTHORIZED` or bounded fail-closed rejection outcomes.

AC-12. Invented, absent, malformed, duplicate/conflicting, and corrupt records
are rejected.

AC-13. A valid record presented for the wrong action is rejected.

AC-14. A valid record presented for the wrong Change/task or Attempt scope is
rejected.

AC-15. CURRENT, ACTIVE, local artifacts, arbitrary prose, Git history, Attempt
state, and evidence stores are not authorization sources or issuers.

AC-16. Records are immutable once issued; v1 has no revocation or
delete/overwrite/shadow-revocation semantics.

AC-17. Preparation authorization is single-use per successful Attempt
materialization; failed/no-commit attempts do not consume it.

AC-18. Recovery authorization is single-use per successful exact-Attempt
interrupted terminalization; failed/no-commit attempts do not consume it.

AC-19. Attempt Runtime owns the atomic prior-use check with its own mutation;
no cross-store transaction or mutable source consumption state is required.

AC-20. This Change contains no authentication/security/policy subsystem,
Attempt implementation, executor/lifecycle/PL08 dependency, Change-2/3
mutation, or new Roadmap vertebra.

AC-21. Production-equivalent positive/negative proof uses the real issuer and
resolver, including trust-boundary and no-alternate-issuer evidence.

AC-22. Traversability evidence proves only the bounded issuance-to-resolution
seam and names downstream Attempt integration as the next broken seam.

AC-23. The trust root is `TRUSTED_LOCAL_OWNER_CONTROL_PLANE` with environment
anchor `OS_ACCOUNT + LOCAL_PLANNING_LITE_CONTROL_ENVIRONMENT + TARGET_ACCESS`;
the owner decision event is explicit local issuance; human authentication and
cryptographic record authorship are out of v1 scope; and the defined local
adversary exclusions are recorded.

AC-24. Issuance requires no prior machine authorization, has no action/scope
defaults, and is forbidden when implicit, unattended, runtime-self-issued, or
issued by a resolver/consumer/helper/test seed without the real control-plane
path.

ACCEPTANCE_CRITERIA_COUNT: 24

## CLOSURE CRITERIA

The original 12 criteria are preserved and strengthened as follows:

| Original | Corrected treatment |
|---|---|
| CC-01 | strengthened: real trusted control-plane issuer and helper insufficiency |
| CC-02 | unchanged: exact preparation issuance/resolution |
| CC-03 | strengthened: missing/default/implicit issuance negatives included |
| CC-04 | unchanged: exact recovery issuance/resolution |
| CC-05 | strengthened: missing/default/implicit issuance negatives included |
| CC-06 | unchanged: strict source/conflict proof |
| CC-07 | unchanged: synthetic single-use contract proof, not runtime enforcement |
| CC-08 | unchanged: immutable/no-revocation proof |
| CC-09 | strengthened: no routing/local/prose authority or issuer path |
| CC-10 | unchanged: no Attempt/executor/lifecycle dependency |
| CC-11 | strengthened: no authentication/security/policy expansion |
| CC-12 | strengthened: bounded trusted issuance traversability proof |

CC-01. One real trusted local owner/control-plane issuance path materializes a
strictly decoded durable immutable typed record and returns its stable ref;
helper-only and seeded-only paths do not satisfy closure.

CC-02. Production-equivalent preparation issuance resolves the exact action,
Change, and task/operation scope as `AUTHORIZED`.

CC-03. Preparation negatives reject malformed, invented, absent,
duplicate/conflicting, wrong-action, wrong-Change, wrong-task, missing-scope,
and implicit/defaulted issuance inputs.

CC-04. Production-equivalent recovery issuance resolves the exact action and
Attempt scope as `AUTHORIZED`.

CC-05. Recovery negatives reject preparation-for-recovery, malformed,
invented/absent, wrong-action, other-Attempt, missing-scope, and
implicit/defaulted issuance inputs.

CC-06. Strict source proof rejects malformed schemas, unknown action values,
wrong action/scope combinations, and conflicting reference reuse.

CC-07. Replay/reuse conformance proves both single-use contracts, retry before
successful consumer commit, and rejection after simulated successful use,
without claiming downstream Attempt integration exists.

CC-08. Revocation-boundary proof demonstrates immutable records and no
delete/overwrite/shadow current-state interpretation.

CC-09. Boundary proof demonstrates that CURRENT, ACTIVE, local artifacts,
arbitrary prose, Git history, Attempt state, and evidence stores neither issue
nor resolve authorization.

CC-10. Closure requires no Attempt store, materialization, claim, recovery
transition, executor, RunReceipt, lifecycle, or PL08 runtime.

CC-11. Inspection proves no transfer of decision authority, authentication or
security subsystem, generic policy, multiple source, wildcard permission, or
new Roadmap vertebra.

CC-12. Bounded system proof traverses explicit trusted issuance -> durable
record -> real resolver -> exact applicability for both actions and leaves
downstream Attempt access unclosed.

CC-13. Review evidence verifies the declared trusted-local control-plane root,
environment anchor, explicit root decision event, no recursive authorization,
no action/scope defaults, no implicit/runtime/unattended issuer, explicit
adversary exclusions, and `CRYPTOGRAPHIC_RECORD_AUTHENTICITY: OUT_OF_SCOPE_V1`.

CLOSURE_CRITERIA_COUNT: 13

Closure remains independent of Attempt Runtime. It requires a real production
issuer, exact action/scope capture, stable reference, real resolver, positive
and negative issuance/resolution proof, and trust-boundary evidence. It does
not require Attempt store, materialization, claim, terminalization, executor,
or lifecycle.

## PLAN-TIME ARCHITECTURE STOP

Planning must STOP for owner architecture adjudication if it discovers a need
for:

- authentication/login, MFA, cryptographic signatures/MACs, remote IdP, RBAC,
  policy engine, user/role database, or process sandbox for v1 correctness;
- runtime self-issuance, unattended issuance, or a hidden alternate issuer;
- issuance inferred from CURRENT/ACTIVE, startup, resume, approval, Attempt,
  lifecycle, resolver, lookup, error fallback, or tests;
- arbitrary/defaulted action or scope;
- protection against malicious equivalent-OS-principal actors as a v1
  requirement;
- mutable authorization consumption state or cross-store transaction;
- Attempt Runtime, executor, lifecycle, Change-2/3, or Roadmap expansion.

PLAN_TIME_ARCHITECTURE_STOP: PRESENT

## DEFINITION / PLAN BOUNDARY

Definition freezes trust root, environment anchor, threat model, owner decision
event, explicit issuer, no recursive authorization, no defaults, issuance
prohibitions, adversary exclusions, cryptographic boundary, semantic owners,
two actions, exact scopes, source cardinality, record immutability,
no-revocation, resolver semantics, single-use owner, transaction boundary,
false-done resistance, acceptance, and closure proof.

Plan may choose only module, store carrier, file path, CLI spelling,
serialization, lock/write mechanics, function names, and test layout. Plan may
not introduce another issuer, defaults, authentication, security subsystem,
policy system, or runtime self-issuance.

## OPEN QUESTIONS

UNBOUND_ARCHITECTURE_CHOICES: 0

UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0

The only local derived-artifact convention is the self-excluding candidate
hash. Canonicalization must later use ordinary full-file hashing recorded
externally.

CANDIDATE_HASH_CONVENTION: LOCAL_DERIVED_ARTIFACT_ONLY

## APPROVED DEFINITION STATUS

OVERALL: PASS_CANONICAL_DEFINITION_CREATED

The owner-approved corrected candidate resolves MF-01 in place and preserves
all previously passed semantics. This canonical Definition authorizes no
Planning, implementation, executor work, lifecycle resume, staging, commit, or
push.

```text
PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_DEFINITION_CANONICALIZATION
OVERALL: PASS_CANONICAL_DEFINITION_CREATED
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
ORIGINAL_CANDIDATE_SHA256: F031B189571DEA890CCF8BC9EA50CB3970D17088DA169F1B4D07CF7EA17BC50D
FRESH_REVIEW_SHA256: C57830540C706F6A3A311A24C00F9B47301EAA665476D740FA1934AD998CE550
TRUST_BOUNDARY_ADJUDICATION_SHA256: FB786E2D4B275E56A4A961A49431DCC07503788A6D8F3A08771C517B226250FC
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001
MF_01: CLOSED
TRUST_ROOT: TRUSTED_LOCAL_OWNER_CONTROL_PLANE
LOCAL_CONTROL_PLANE_TRUST_BOUNDARY: DEFINED
LOCAL_ENVIRONMENT_TRUST_ANCHOR: OS_ACCOUNT + LOCAL_PLANNING_LITE_CONTROL_ENVIRONMENT + TARGET_ACCESS
OWNER_DECISION_EVENT: EXPLICIT_LOCAL_CONTROL_PLANE_ISSUANCE
HUMAN_AUTHENTICATION_SUBSYSTEM_REQUIRED: NO
ISSUANCE_REQUIRES_PRIOR_MACHINE_AUTHORIZATION: NO
AUTHORIZATION_ACTION_DEFAULT: NONE
AUTHORIZATION_SCOPE_DEFAULT: NONE
IMPLICIT_ISSUANCE: FORBIDDEN
RUNTIME_SELF_ISSUANCE: FORBIDDEN
UNATTENDED_RUNTIME_AUTO_ISSUANCE: FORBIDDEN
PROCESS_ISOLATION_REQUIRED: NO
LOCAL_ADVERSARY_EXCLUSIONS: DEFINED
CRYPTOGRAPHIC_RECORD_AUTHENTICITY: OUT_OF_SCOPE_V1
OWNER_AGENCY_PRESERVED: YES
REAL_PRODUCTION_CONTROL_PLANE_ISSUER_REQUIRED: YES
LOW_LEVEL_PERSISTENCE_HELPER_IS_AUTHORITY: NO
ACTION_AUTHORIZATION_GAP: WIRING_GAP
DECISION_AUTHORITY_PREPARATION: EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY
DECISION_AUTHORITY_RECOVERY: EXISTING_OWNER/LIFECYCLE_CONTROL_AUTHORITY
MACHINE_AUTHORIZATION_RECORD_AUTHORITY: PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_AUTHORITY
SUPPORTED_ACTION_TYPE_COUNT: 2
PREPARATION_ACTION: OWNER_AUTHORIZED_ATTEMPT_PREPARATION
PREPARATION_SCOPE: exact change_id + exact task_or_operation_id
RECOVERY_ACTION: OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION
RECOVERY_SCOPE: exact attempt_id
AUTHORITY_VALIDATION_SHAPE: SHARED_CORE_WITH_ACTION_SPECIFIC_VALIDATION
AUTHORIZATION_RECORD_MUTABILITY: IMMUTABLE
REVOCATION_REQUIRED_IN_V1: NO
PREPARATION_AUTHORIZATION_REUSE: SINGLE_USE_PER_SUCCESSFUL_ATTEMPT_MATERIALIZATION
RECOVERY_AUTHORIZATION_REUSE: SINGLE_USE_PER_SUCCESSFUL_INTERRUPTED_TERMINALIZATION
AUTHORIZATION_USE_ENFORCEMENT_OWNER: PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY
CROSS_STORE_ATOMIC_TRANSACTION_REQUIRED: NO
ATTEMPT_RUNTIME_INDEPENDENT_CLOSURE: YES
ATTEMPT_RUNTIME_IMPLEMENTATION_INCLUDED: NO
EXECUTOR_DEPENDENCY: NO
LIFECYCLE_DEPENDENCY: NO
PL08_RUNTIME_ORCHESTRATION_CREATED: NO
CHANGE2_SCOPE_SEPARATION: PASS
CHANGE3_REQUIRED: NO
NEW_AUTHENTICATION_PREREQUISITE_REQUIRED: NO
NEW_SECURITY_SUBSYSTEM_REQUIRED: NO
NEW_POLICY_SUBSYSTEM_REQUIRED: NO
NEW_ROADMAP_VERTEBRA_REQUIRED: NO
ACCEPTANCE_CRITERIA_COUNT: 24
CLOSURE_CRITERIA_COUNT: 13
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0
PLAN_TIME_ARCHITECTURE_STOP: PRESENT
CANONICAL_DEFINITION_APPROVED: YES
SOURCE_MUTATIONS: 0
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
ATTEMPT_RUNTIME_CHANGE: DEFINITION_APPROVED / PLANNING_BLOCKED_BY_AUTHORIZATION_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED
EXECUTOR_PREREQUISITE: NOT_STARTED
LIFECYCLE_CHANGE: DEFINITION_APPROVED / PLANNING_BLOCKED_BY_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
SOURCE_CANDIDATE: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_CHANGE_DEFINITION_CANDIDATE_CORRECTED.md
CORRECTED_CANDIDATE_SHA256: 6B8150E185F3AE45073C4957DB54B59AB455D3C25883DB5DCD717CECA32DF443
SOURCE_CANDIDATE_HASH_CONVENTION: LOCAL_DERIVED_ARTIFACT_ONLY
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLANNING
RESULT_DIGEST: The owner-approved corrected candidate remains unmodified historical evidence. MF-01 is closed by the trusted-local owner/control-plane root. The local environment trust anchor is the OS account, Planning Lite control environment, and explicit target access. Deliberate issuance is the owner decision event and requires no prior machine authorization. Human authentication, cryptographic authorship, and process isolation remain outside v1. Action and scope have no defaults. Implicit, runtime, and unattended issuance are forbidden. Low-level persistence helpers and seeded records are not production authority. The immutable/no-revocation, single-use, downstream-consumption, no-transaction, and independent-closure semantics are preserved. Acceptance criteria remain 24 and closure criteria remain 13. The canonical Definition is approved with Planning still unauthorized.
```
