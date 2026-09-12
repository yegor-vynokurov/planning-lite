# PL-V39-09 Engineering Basis and Rationale Lineage Semantic Contract v1

## Authority and status

```text
PARENT_AUTHORITY:
ROADMAP.md / PL-V39-09

ENGINEERING_BASIS_RATIONALE_LINEAGE_SEMANTIC_CONTRACT:
CANONICAL_V1

FIELD_VALIDATION:
REQUIRED

SERIALIZATION:
NOT_FROZEN

STORAGE_MODEL:
NOT_FROZEN

PRODUCTION_IMPLEMENTATION:
NOT_AUTHORIZED

EXPLANATION_CLOSURE:
FIELD_HYPOTHESIS_ONLY
```

This companion is the canonical V1 semantic contract for Engineering Basis
and Rationale Lineage within PL-V39-09. It is subordinate to
[`ROADMAP.md`](../ROADMAP.md), references existing owner contracts for facts
they own, and freezes semantics only. It does not activate PL-V39-09, grant
execution or implementation authority, or freeze representation, carrier,
serialization, storage, traversal, or enforcement.

## Engineering Basis

`ENGINEERING_BASIS` is an optional, source-bound, explanatory,
non-authoritative assertion attached to a material target. Its default
placement is inline with that target.

A basis may be separately addressable only when doing so prevents material
duplication, rationale drift, or lost change impact. Before creating separate
identity, prefer a sufficient existing requirement, constraint, invariant, or
canonical decision identity. Every separately addressable basis must reside on,
or be governed through, an existing owner surface and gate. If no legitimate
existing owner surface exists, keep the explanation inline with each owning
target or leave the shared abstraction unaccepted.

The owner of a separately addressable basis accepts and changes the shared
explanatory assertion. Each target independently accepts its adoption of that
basis through the target's existing authority. Basis acceptance and target
adoption are distinct propositions. Changing a shared basis triggers bounded
impact review for materially dependent adopters, but does not silently mutate
or revoke an adoption or rewrite its historical acceptance. Each target owner
decides whether current adoption remains accepted.

Engineering Basis grants no decision, acceptance, evidence, execution,
implementation, or lifecycle authority. It creates no new owner, acceptance
lifecycle, board, or registry.

## Seven rationale-core relations

The rationale core contains exactly these seven directed relations.
`MOTIVATED_BY` and `ADDRESSES` are both retained and have different meanings.

```text
RATIONALE_CORE_RELATION_COUNT:
7
```

| Relation | Direction | Bounded meaning | Does not imply | Owner boundary where material |
|---|---|---|---|---|
| `DERIVED_FROM` | derived proposition or artifact -> exact source | Records explicit derivation and provenance. | Semantic similarity, relevance, plausibility, acceptance, correctness, proof, or authority. | The owner of the derived semantic mutation accepts the derivation; source ownership remains unchanged. |
| `JUSTIFIED_BY` | material target -> admitted Engineering Basis | Records the protected-property explanation for the target. | Motivation, evidence support, proof, verification, target acceptance, or authority. | The basis owner governs the basis; the target owner independently accepts its use. |
| `MOTIVATED_BY` | decision or task -> goal, need, risk, finding, or gap | Records why the decision or work exists. | That the source is addressed, closed, satisfied, verified, or implemented. | The existing owner of the decision or task accepts the rationale edge; referenced source authority remains with its owner. |
| `CONSTRAINED_BY` | decision, alternative, or design -> accepted constraint | Records an owner-governed, non-tradable choice boundary. | Creation or acceptance of the constraint, evidence of compliance, or satisfaction of the constraint. | The constraint's existing owner governs its meaning and acceptance; the target owner accepts the edge. |
| `DEPENDS_ON` | validity-bearing target -> material premise, assumption, or decision | Records bounded change-impact sensitivity. | A generic technical dependency, automatic invalidation, causality, execution order, or lifecycle authority. | Premise and target owners retain their own authority; a material change requests review rather than mutating the target. |
| `IMPLEMENTS` | task, design, or code identity -> decision or requirement | Records a realization attachment. | `SATISFIES`, verification, completion, conformance, acceptance, or authority. | Requirement, decision, completion, and acceptance owners retain their existing gates. |
| `ADDRESSES` | plan, design, or claim -> requirement, risk, finding, or gap | Records a bounded downstream disposition. | `MOTIVATED_BY`, closure, satisfaction, `VERIFIES`, evidence sufficiency, or implementation completion. | Requirement, finding, gap, evidence, and closure owners retain their existing gates. |

The distinctions are normative:

```text
JUSTIFIED_BY != MOTIVATED_BY
MOTIVATED_BY != ADDRESSES
IMPLEMENTS != SATISFIES
ADDRESSES != VERIFIES
DEPENDS_ON != generic technical dependency
DERIVED_FROM != semantic similarity / plausibility
```

## External supersession

```text
SUPERSEDES:
EXTERNAL_OWNER_OWNED_RELATION
```

`SUPERSEDES` is explicit, scoped, owner-owned, never inferred, and is not one
of the seven rationale-core relations. Rationale history, current-governing,
and impact queries may consume an exact owner-recorded supersession fact.
Rationale acceptance cannot create, infer, or accept supersession, and no
rationale-owned synonym replaces it.

PL-V39-08 evidence supersession remains PL08-owned. Decision and lifecycle
supersession remain with their existing owners. Recency, chronology,
contradiction, similarity, or apparent replacement never imply supersession.

## No unsupported rationale edge

```text
NO_UNSUPPORTED_RATIONALE_EDGE
```

Every accepted rationale edge must bind:

```text
exact source identity
exact target identity
relation type
direction
provenance
epistemic / authority status
```

Co-occurrence, chronology, semantic similarity, model plausibility, or
retrospective explanation may produce only `PROPOSED_INFERENCE` until the
existing authority that owns each asserted semantic mutation accepts it.
Shared-basis content and a target's adoption are separately owner-accepted
propositions.

`PROPOSED_INFERENCE` cannot:

```text
close an orphan
establish PL08 support
make validity CURRENT
mutate requirements, constraints, or decisions
authorize execution
authorize implementation
```

Transitive rationale paths are derived query results. Path composition cannot
strengthen constituent relations into causality, proof, verification,
satisfaction, authority, invalidation, or supersession.

## Historical rationale binding

```text
HISTORICAL_RATIONALE_BINDING:
ACCEPTANCE_TIME_IMMUTABLE
```

Every accepted historical rationale assertion binds the exact source and
target content used at acceptance, or an existing immutable owner/evidence
identity for that content. The acceptance-time binding is permanent for that
assertion.

`CANONICAL_CURRENT` may supplement the historical binding for a
current-governing query, but cannot replace, edit, rewrite, or reinterpret the
acceptance-time binding.

```text
What justified the accepted decision at acceptance time?
-> resolve the immutable acceptance-time binding

What governs this target now?
-> preserve that history and optionally add current owner resolution
```

Local, ignored, session, or attachment paths alone are insufficient durable
canonical identity. Portable-anchor mechanics across renames remain unfrozen.

## Applicability and current validity

The enclosing query applies this gate before current-validity projection:

```text
KNOWN_OUT_OF_SCOPE
-> NOT_APPLICABLE at enclosing query level
-> do not enter CURRENT_VALIDITY projection
```

Unknown mandatory applicability is not `NOT_APPLICABLE`; it fails closed as
`UNKNOWN` in the applicable-query resolution. The internal derived values are
exactly:

```text
CURRENT
REVIEW_REQUIRED
SUPERSEDED
INVALIDATED_BY_AUTHORITY
UNKNOWN
```

`CURRENT_VALIDITY` is derived, scoped, operation-relative, and
non-authoritative. Rationale Lineage consumes owner lifecycle facts but does
not own them or create a lifecycle state machine.

```text
CURRENT_VALIDITY_PRECEDENCE:
OWNER_DEFINED_OR_UNKNOWN
```

```text
EXPLICIT_OWNER_PRECEDENCE:
USE_IF_DEFINED

NO_OWNER_PRECEDENCE:
PRESERVE_ALL_APPLICABLE_SCOPED_HISTORICAL_FACTS

CURRENT_GOVERNING_RESULT:
UNKNOWN
```

The resolution rules are:

1. Consume only explicit, resolvable, scope-applicable facts from their
   existing owners. Never infer invalidation, supersession, or precedence.
2. Same-scope conflicting owner lifecycle facts receive only an applicable,
   unambiguous precedence rule from an existing owner. Without such a rule,
   preserve all applicable scoped historical facts and return `UNKNOWN` for
   current governance. Contradictory owner precedence claims also yield
   `UNKNOWN` unless a higher existing authority resolves them.
3. Chronology, recency, last-writer-wins, file order, source type, and model
   confidence are not precedence.
4. A lone applicable, resolvable explicit invalidation yields
   `INVALIDATED_BY_AUTHORITY`.
5. Owner-recorded supersession yields `SUPERSEDED` only when the required exact
   successor and its current owner resolution are resolvable and usable. An
   unresolvable successor preserves historical supersession but yields current
   `UNKNOWN`.
6. An invalidated successor does not silently reactivate its predecessor.
   Preserve both historical facts and use an explicit owner fallback/current
   governor if one exists; otherwise return `UNKNOWN`.
7. Non-overlapping scopes are evaluated independently.
8. A known material premise, source, basis, scope, challenge, expiry, or revisit
   change may yield `REVIEW_REQUIRED` without revoking authority. Other
   unresolved mandatory identity, status, applicability, or conflict yields
   `UNKNOWN`; an otherwise applicable and resolved target may yield `CURRENT`.

This projection grants no decision, acceptance, evidence, execution,
implementation, current-state, or lifecycle authority and rewrites no owner
fact or historical rationale assertion.

## Orphan diagnostics and bounded exceptions

`ORPHAN_DECISION`, `ORPHAN_TASK`, and `ORPHAN_REQUIREMENT` are structural,
maturity-dependent diagnostics. They indicate that lineage required by the
applicable existing maturity/owner gate is missing; they do not create a new
gate or decide semantic acceptance.

Only accepted typed lineage or an exact semantically eligible bounded
exception authority may resolve an orphan. `PROPOSED_INFERENCE` cannot close
one. The closed exception classes are:

```text
ORPHAN_EXCEPTION_ELIGIBILITY:
BOUNDED_PREDICATES
```

```text
HOUSEKEEPING_OR_CLERICAL
REPAIR_OR_MAINTENANCE_WITH_EXISTING_AUTHORITY
INCIDENT_OR_EMERGENCY_WITH_EXISTING_AUTHORITY
OWNER_APPROVED_DEFERRED
OWNER_APPROVED_OUT_OF_SCOPE
```

Every exception identifies exact existing authority, scope, reason, and class;
an owner label alone is insufficient. Admission is bounded as follows:

- `HOUSEKEEPING_OR_CLERICAL` cannot materially change product or runtime
  behavior, a public or internal contract, accepted requirement or decision
  meaning, a security/safety boundary, or other accepted semantic behavior.
- `REPAIR_OR_MAINTENANCE_WITH_EXISTING_AUTHORITY` identifies the accepted
  baseline or authority being restored or preserved, remains restorative or
  maintenance-only, and introduces no lasting new behavior without ordinary
  authority.
- `INCIDENT_OR_EMERGENCY_WITH_EXISTING_AUTHORITY` identifies current incident
  or emergency authority and remains bounded to containment, restoration, or
  emergency action. Lasting new behavior requires ordinary authority.
- `OWNER_APPROVED_DEFERRED` records owner, scope, reason, unresolved consequence
  or obligation, and a mandatory revisit or expiry. A defer without revisit or
  expiry is ineligible.
- `OWNER_APPROVED_OUT_OF_SCOPE` is an explicit owner scope decision. It is not
  satisfaction, verification, completion, or evidence.

A material semantic change makes the exception ineligible and requires
ordinary authority. Orphan resolution is structural only:

```text
ORPHAN_CLOSED
!= REQUIREMENT_SATISFIED
!= VERIFIED
!= IMPLEMENTATION_COMPLETE
```

## Existing owner boundaries

This contract references rather than duplicates the existing owner contracts.

PL06, through
[`PL-V39-06-CONTEXT-MEMORY-HANDOFF-CHANGE-DEFINITION-v1.md`](../../checkpoints/PL-V39-06-CONTEXT-MEMORY-HANDOFF-CHANGE-DEFINITION-v1.md),
exclusively owns:

```text
Memory
Context
Current State
Handoff
bounded context selection
source/current/freshness resolution
resume
handoff
```

Rationale Lineage may provide typed explanatory dependencies and portable
identities only. It does not select, rewrite, or become PL06 context, memory,
current-state, resume, or handoff authority.

PL08, through
[`PL-V39-08-PROPOSED-CHANGE-DEFINITION-v1.md`](../../checkpoints/PL-V39-08-PROPOSED-CHANGE-DEFINITION-v1.md),
exclusively owns:

```text
Attempt identity
observed results
SUPPORTS
CHALLENGES
VERIFIES
evidence applicability/completeness
technical evaluation
technical acceptance
findings
evidence supersession
owner disposition
```

Rationale edges are not evidence. They cannot establish support, challenge,
verification, evidence applicability/completeness, technical acceptance,
finding disposition, or evidence supersession.

The Architecture Knowledge boundary is:

```text
Architecture Knowledge:
reusable framework guidance

Engineering Basis:
project-specific applicability / protected-property bridge
```

Selecting Architecture Knowledge does not make it project authority. It
becomes project rationale only through explicit applicability and existing
project authority. The detailed Architecture Knowledge topology remains owned
by
[`PL-V39-09-IDEAL-SCAFFOLD-KNOWLEDGE-SKELETON-v1.md`](PL-V39-09-IDEAL-SCAFFOLD-KNOWLEDGE-SKELETON-v1.md).

Tradeoff Reasoning remains `SEPARATE_FUTURE_ATTACHMENT`. This contract does not
reserve or freeze `CHOSEN_OVER` or `ACCEPTS_DOWNSIDE`, and freezes no Tradeoff
Reasoning schema.

Explanation Closure remains `FIELD_HYPOTHESIS_ONLY`. It defines no runtime
traversal, caching, token budgets, completeness authority, or context-loading
behavior and does not alter the two-path Context Compilation skeleton in
[`PL-V39-09-CONTEXT-COMPILATION-CONDITIONAL-SKELETON-v1.md`](PL-V39-09-CONTEXT-COMPILATION-CONDITIONAL-SKELETON-v1.md).

## V1 invariants

```text
RL-V1-01
ENGINEERING_BASIS is optional, source-bound, explanatory, non-authoritative,
and inline by default. Any separately addressable basis is governed by an
existing owner surface, while each target's adoption remains independently
target-owned.

RL-V1-02
Every accepted rationale edge has exact source and target identities, one of
the seven rationale-core relation types, direction, provenance, and epistemic /
authority status.

RL-V1-03
Co-occurrence, chronology, similarity, model plausibility, or retrospective
explanation produces only PROPOSED_INFERENCE until the existing owner of each
asserted semantic mutation acts. Shared-basis content and target adoption are
separately owner-accepted propositions.

RL-V1-04
Transitive rationale paths are derived query results. Path composition cannot
strengthen constituent semantics into causality, proof, verification,
satisfaction, authority, invalidation, or supersession.

RL-V1-05
Rationale Lineage references existing owner artifacts and consumes their owned
facts. It cannot create a duplicate authority, evidence, memory/current,
basis-governance, or supersession registry.

RL-V1-06
Every material assumption on a rationale validity path is explicit,
source/status/scope-bound, and has a meaningful revisit discriminator where one
can exist; absent observability remains visible.

RL-V1-07
A material source, premise, basis, scope, or challenge change triggers bounded
impact review. It does not silently mutate adopters, revoke, rewrite,
supersede, or authorize anything, and historical acceptance remains immutable.

RL-V1-08
After the explicit applicability gate, CURRENT_VALIDITY is a derived,
operation-relative five-value projection over existing owner, PL06, and PL08
inputs. Only applicable explicit owner precedence may resolve conflicting
same-scope lifecycle facts; otherwise all history is preserved and current
governance is UNKNOWN. The projection is non-authoritative, and an
unresolvable mandatory current successor also yields UNKNOWN.

RL-V1-09
PL06 exclusively owns Memory, Context, Current State, Handoff, bounded context
selection, source/current/freshness resolution, resume, and handoff.
Explanation Closure remains a field hypothesis only.

RL-V1-10
PL08 exclusively owns Attempt and observed-result identity, SUPPORTS,
CHALLENGES, VERIFIES, evidence applicability/completeness, technical
evaluation/acceptance, findings, evidence supersession, and owner disposition.

RL-V1-11
Architecture Knowledge remains reusable framework guidance. It becomes project
rationale only through explicit project applicability and existing project
authority.

RL-V1-12
Material ORPHAN_DECISION, ORPHAN_TASK, and ORPHAN_REQUIREMENT diagnostics are
maturity-dependent. Only accepted typed lineage or an exact semantically
eligible bounded exception resolves them; defer is revisit/expiry-bound, and
orphan closure is structural rather than satisfaction, verification, evidence,
or implementation completion.

RL-V1-13
SUPERSEDES is external, explicit, scoped, owner-owned, and never inferred.
Historical supersession remains visible. Current successor resolution must be
usable; conflicting same-scope owner facts use owner precedence only and
otherwise yield UNKNOWN. Successor invalidation never silently reactivates the
predecessor.

RL-V1-14
V1 requires no graph database, knowledge graph, vector database, RAG,
ontology, automatic causal inference, universal provenance capture,
rationale-only skill, or new top-level subsystem.

RL-V1-15
An accepted historical rationale assertion binds the source/target content or
immutable owner/evidence identity used at acceptance. CANONICAL_CURRENT may be
an additional current-governing resolution, but it cannot replace or rewrite
that historical binding.
```

## Field validation and unfrozen negative space

```text
FIELD_VALIDATION_REQUIRED:
YES

FIELD_VALIDATION_BLOCKS_SEMANTIC_MATERIALIZATION:
NO
```

Field validation remains required before any stronger operational or runtime
freeze. It must calibrate usefulness, authoring cost, materiality, exception
admission, impact-review behavior, and any future operational thresholds. This
canonical semantic materialization is not evidence that field validation is
complete or that the contract is implementation-ready or production-ready.

The following remain explicitly unfrozen or unauthorized:

```text
carrier field schema
serialization format
storage model
portable-anchor mechanics across renames
runtime traversal
impact-analysis implementation
query engine
caching
token budgets
automatic inference
automatic rationale extraction
new acceptance lifecycle
new owner role
new registry
new service
CLI/API
production enforcement
Tradeoff Reasoning schema
Explanation Closure algorithm
field-calibration thresholds
production implementation
```

V1 requires no graph database, ontology, RAG, vector database, or new
top-level subsystem. No representation or implementation choice is implied by
these semantics.

## Non-normative provenance

This contract was derived through bounded shaping, synthesis, independent
review, repair, and independent verification. Those local artifacts remain
evidence only; this companion contains the owner-adjudicated normative
semantics.
