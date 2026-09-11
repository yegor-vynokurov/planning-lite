# PL-V39-09 Ideal Scaffold Knowledge Architectural Skeleton v1

## Authority and status

```text
PARENT AUTHORITY:
docs/design/project-spine/roadmap/ROADMAP.md
PL-V39-09 / 09-B

AUTHORITY CLASS:
SUBORDINATE DETAILED DIRECTION AUTHORITY

SCOPE:
PL-V39-09 Ideal Scaffold Knowledge architectural skeleton only

IDEAL_SCAFFOLD_KNOWLEDGE_SKELETON:
FROZEN

V1_PACK_TOPOLOGY:
FROZEN_CANONICAL

PACK_CONTENT:
NOT_FROZEN

FIELD_VALIDATION:
REQUIRED

PRODUCTION_IMPLEMENTATION:
NOT_AUTHORIZED
```

`ROADMAP.md` remains the single canonical direction authority. This companion
is subordinate detailed design for the explicitly bounded skeleton scope. It
cannot change the macro sequence, authorize implementation, define a
project-specific architecture, or override the Roadmap.

## Canonical Architecture Knowledge topology freeze

This bounded freeze records topology and ownership semantics only. It does not
freeze final pack prose, question inventories, routing implementation or field
validation.

```text
UNIVERSAL CORE

+ 4 DOMAIN / COMPUTATION LENSES
  1. Application Delivery
  2. Data / Knowledge Systems
  3. AI / ML Systems
  4. Solver / Optimization / Scientific Compute

+ 3 CROSS-CUTTING OVERLAYS
  5. Product / Distribution
  6. Operations / Deployment
  7. Security / Privacy / Assurance
```

### Universal Core

Universal Core contains genuinely cross-domain concerns, detects materiality
and may trigger deeper modules. Shared reasoning is loaded once; domain and
cross-cutting deltas stay in their owning modules. Core does not absorb
domain-specific depth merely to avoid routing. Final Core question wording is
not frozen.

### Domain / computation lenses

- **Application Delivery:** one top-level lens. Interaction / Client and
  Service / API are independently selectable profiles; Client ↔ Service is a
  conditional seam. Frontend/backend are descriptors, not separate V1 lenses.
- **Data / Knowledge Systems:** one top-level lens with shared authority,
  state/lifecycle, consistency, schema/evolution, quality, lineage/provenance,
  and serving foundation. Graph / Knowledge is an explicit selectable
  sublens, not a standalone V1 lens.
- **AI / ML Systems:** one top-level lens with Shared AI Foundation,
  Predictive / Trained ML, and conditional GenAI / Foundation Model profiles
  (LLM, RAG / Grounding, Agentic). Selecting AI/ML does not imply loading all
  profiles. GenAI is not standalone V1; a future split requires repeated field
  evidence and no numeric threshold is frozen.
- **Solver / Optimization / Scientific Compute:** one top-level lens with
  Mathematical Optimization, Numerical / Scientific Compute,
  Stochastic / Heuristic Search, and a conditional computational/HPC profile.
  Solver owns computational requirements and scientific/numerical truth;
  Operations owns runtime realization. HPC is not a top-level V1 lens.

### Cross-cutting overlays

- **Product / Distribution:** cross-cutting overlay with stable axes
  Consumer Control, Delivery Ownership, Public Contract Exposure, Update
  Control, and Distribution Rights. Compatibility / Support Lifecycle is an
  explicit conditional Product commitment. Tenant / Customer Isolation
  Promise is a conditional Product profile; generic universal TENANCY is not
  used. Delivery Ownership means which party is accountable for placing a
  usable service or artifact at the consumption boundary and where custody
  transfers between provider and consumer. Provider-operated versus
  consumer-installed may be evidence for this dimension; runtime operating
  mechanics remain in Operations. Product descriptors such as open-source,
  library, CLI, commercial, internal and SaaS are not mutually exclusive
  architecture categories.
- **Operations / Deployment:** cross-cutting overlay for runtime ownership,
  deployment, health, observation, recovery, capacity and realized resource or
  cost operation. Cloud, containers, Kubernetes, GitOps, autoscaling,
  failover and multi-region remain conditional mechanisms, not architecture
  categories.
- **Security / Privacy / Assurance:** conditional cross-cutting overlay with
  Shared Protection / Trust Foundation and independently selectable Security,
  Privacy and Assurance profiles. Privacy is not reducible to confidentiality
  or security. SPA owns what protection/privacy claims matter and how strong
  assurance must be; PL08 owns evidence, observed results, applicability,
  review and supersession governance. No second evidence lifecycle is created.

### Routing and composition semantics

```text
intent / domain truth
→ layered fingerprint
→ Universal Core + candidate material lenses/overlays
→ system-known candidate drivers + material unknowns
→ derive / safely default / ask
→ accepted architecture drivers
→ scaffold reasoning
```

The fingerprint selects candidate knowledge and questions, not technology,
pattern or architecture. Candidate module selection is provisional knowledge
selection; accepted drivers are not required before loading questions needed to
discover them. Composition is monotonic for material concerns: equivalent
questions may be deduplicated, but independently material concerns may not
disappear. There is no fixed precedence or last-writer-wins behavior.

`prefer 1–3 modules` is a context-economy heuristic only — not a cap,
invariant or correctness rule. Broader material combinations use staged
loading rather than omission. Measured context/token benefit is unproven.

### Required ownership seams

```text
Application ↔ AI
AI ↔ Operations
Data ↔ Operations
Solver ↔ Operations

Product ↔ Application
Product ↔ Data
Product ↔ Operations
Product ↔ SPA
Product ↔ AI

SPA ↔ Application
SPA ↔ Data
SPA ↔ AI
SPA ↔ Operations
```

Product owns consumer-facing promise and public meaning. SPA owns
protection/privacy requirements and required assurance strength. Domain lenses
and Operations own technical realization and domain-specific evidence
semantics. PL08 owns the evidence-governance lifecycle. Seams prevent
duplication and dropped concerns; they do not create another subsystem.

### Classification topology

The old exclusive ladder is rejected. Classification separates at least:

```text
SCOPE: UNIVERSAL | DOMAIN | SUBDOMAIN
APPLICABILITY: GENERALLY_APPLICABLE_WITHIN_SCOPE | DRIVER_CONDITIONAL
SPECIALIZATION: GENERAL | SPECIALIZED
MATURITY: ESTABLISHED | EMERGING | LEGACY_DECLINING
EVIDENCE_CONFIDENCE: HIGH | MEDIUM | LOW
ADOPTION_FREQUENCY: UNKNOWN unless representative empirical evidence exists
```

Final classification schema and presentation wording remain unfrozen.

## Frozen architectural invariants

```text
ISK-01  Ideal first, Reality second, reconciliation third.

ISK-02  Ideal reasoning is implementation-blind but domain-informed.

ISK-03  Project/workload characterization uses a layered multi-label
        fingerprint.

ISK-04  The fingerprint selects candidate knowledge and questions, not
        architecture.

ISK-05  Accepted architecture drivers own structural choices.

ISK-06  Ideal Scaffold reasoning uses Universal Core plus the smallest
        material composable lens set.

ISK-07  Architecture Knowledge Packs improve questions, checks, scenarios and
        trade-off reasoning; they do not prescribe a concrete architecture.

ISK-08  User questioning is progressive and limited to materially necessary
        unknowns.

ISK-09  A default is allowed only when reversible, low-risk and not silently
        architecture-determining.

ISK-10  Goals, critical flows, quality scenarios, accepted constraints and
        risks precede detailed structural choices.

ISK-11  A project-specific Ideal Scaffold has one structured semantic model as
        its primary architecture authority.

ISK-12  Narratives, diagrams, checklists, C4-like views and other
        representations are derived views, not separate authorities.

ISK-13  Architecture Knowledge Packs require source provenance and bounded
        freshness metadata.

ISK-14  Architecture Knowledge Packs are tracked framework guidance. They are
        not project requirements, project architecture, implementation,
        user-intent or memory authority.

ISK-15  Pack/lens composition is monotonic for material concerns:
        deduplication may merge equivalent concerns but may not delete a
        material driver, constraint, failure mode, quality concern or
        trade-off.

ISK-16  Material cross-lens conflicts remain explicit trade-offs or unresolved
        architecture drivers.

ISK-17  Pack selection is bounded, explainable and deterministic in
        architectural form. No opaque learned router is part of V1.

ISK-18  V1 requires no RAG, vector store, knowledge graph or specialized
        architecture model.

ISK-19  Unknown domains use Universal Core plus bounded source-backed research
        and temporary nonauthoritative lens candidates where material.

ISK-20  Temporary lenses cannot self-promote. Promotion requires evidence,
        recommendation and owner adjudication.

ISK-21  No new top-level Planning Lite subsystem is created. This is framework
        knowledge supporting the existing 09-B Ideal Scaffold responsibility.
```

```text
SKELETON_INVARIANTS_MATERIALIZED:
21/21
```

## Ideal and Reality boundary

The Conceptual Ideal may consume user intent, domain truth, workload
properties, intrinsic legal/regulatory/physical constraints and explicitly
accepted hard constraints. It must not consume current packages, frameworks,
dependencies, file layout, cloud/vendor products, legacy topology or
historical shortcuts merely because they exist.

A legacy fact enters the Constrained Target Ideal only when explicitly accepted
as a compatibility, migration, economic, operational or delivery constraint.

```text
CONCEPTUAL IDEAL:
best implementation-blind response to accepted goals, domain truth and
intrinsic constraints

CONSTRAINED TARGET IDEAL:
Conceptual Ideal after owner-accepted hard constraints
```

## Fingerprint, drivers and lenses

```text
FINGERPRINT:
coarse layered multi-label characterization used to select relevant framework
knowledge and questions

ARCHITECTURE DRIVERS:
accepted project-specific facts that actually constrain architecture
```

Conceptual fingerprint layers may distinguish domain/problem, product/delivery
context, execution model, data/workload characteristics and
operations/deployment context. Actors, quality, security/privacy/IP,
scale/performance, state/consistency, change/evolution and maturity may be
derived or promoted into architecture drivers as appropriate. Exact labels,
enums and schema are not frozen.

The frozen topology above is composable. The smallest materially relevant
combination is selected. A lens selects concerns, questions, scenarios, views,
failure modes and trade-off families; it does not select vendors, frameworks,
products, stacks, package layouts or database engines.

## Universal Core and progressive questions

The Universal Core retains these concerns without becoming a mandatory long
questionnaire:

1. purpose, goals, actors and system context;
2. critical capabilities and flows;
3. responsibility, data/state and trust boundaries;
4. material interfaces and dependencies;
5. quality scenarios and accepted hard constraints;
6. runtime, failure, operability and evolution when material;
7. risks, decisions, assumptions and unknowns.

Input classes are `SYSTEM-KNOWN`, `DERIVABLE`, `DEFAULTABLE`, `MUST-ASK` and
`OPTIONAL-REFINEMENT`. `DEFAULTABLE` is only reversible, low-risk and
non-architecture-determining. `MUST-ASK` is limited to information that can
materially change a goal, driver, trust boundary, hard constraint or current
scaffold maturity layer. Ask the smallest coherent batch for the next layer.

```text
I0: purpose, actors, value and qualitative stakes
I1: capabilities and critical flows
I2: responsibility, ownership, domain, data and trust boundaries
I3: interfaces, interactions and material architecture scenarios
I4: execution-oriented virtual scaffold where justified
```

Deeper questions are not asked unless their answers can materially change the
next scaffold layer.

## Architecture alternatives policy

Alternative generation and alternative storage are separate policies.

```text
I0-I1:
Do not generate alternative architectures ceremonially.
Prioritize goal clarity, actors, critical capabilities, flows, material
architecture drivers and major uncertainty.

I2-I3:
Generate alternatives only around material unresolved architecture drivers,
boundaries or trade-offs. Do not generate multiple whole-system alternatives
when only one bounded decision is unresolved.

I4:
Bind the accepted target where a decision has been made. Preserve an
unresolved alternative only when a later owner decision or a bounded
spike/evidence step remains required.
```

Alternative generation is decision-driven, not a mandatory scaffold stage.
Unaccepted alternatives remain `LOCAL_OPERATIONAL` or `EPHEMERAL`; accepted
decision content becomes canonical only through existing planning, decision and
evidence mechanisms. No ADR subsystem is introduced.

## Semantic model and derived views

```text
ARCHITECTURE MODEL != ARCHITECTURE VIEW
```

The primary representation is one `STRUCTURED_SEMANTIC_MODEL`. Human narrative,
system-context, C4-like, data-flow, runtime, trust-boundary, ML-lifecycle,
graph-relation, solver-pipeline and risk/checklist views are derived only when
decision-useful. No diagram is mandatory and no view is a second authority.

Architecture decisions reuse existing Planning, Change, decision and evidence
semantics; no ADR subsystem is introduced by this skeleton.

## Persistence and framework guidance

Only existing PL06 storage classes apply:

```text
accepted I0-I2 semantic model       CONSUMER-OWNED TRACKED_CANONICAL
accepted material I3/I4 decisions   TRACKED_CANONICAL
rendered/regenerable views           RECONSTRUCTABLE unless accepted
review/reconciliation evidence      TRACKED_EVIDENCE_HISTORY
unaccepted alternatives/brainstorms  LOCAL_OPERATIONAL or EPHEMERAL
```

Exact consumer paths are not frozen.

Architecture Knowledge Packs use:

```text
TRACKED_CANONICAL storage class
+ FRAMEWORK GUIDANCE semantics
```

Canonicality covers pack identity, content, version and provenance. Tracking
does not elevate a pack into project requirements, project architecture,
implementation, user-intent or memory authority. Accepted project requirements
and owner decisions win; conflicting pack guidance remains a visible trade-off.

Minimum pack provenance is source identity, edition/version/date where
available, last reviewed date and freshness class. V1 freshness classes are
`DURABLE` and `CHANGEABLE`; no update scheduler is introduced and project
scaffolds do not require a bibliography by default.

## Composition, selection and unknown domains

Semantic merge may deduplicate equivalent questions or checks, but may never
silently delete a material driver, hard constraint, quality concern, failure
mode, trust/safety concern or trade-off effect contributed by a lens. Material
cross-lens conflicts remain explicit.

Pack selection is bounded, explainable and deterministic in predicate or
decision-table form. A reasoning executor may interpret intent and propose or
disambiguate labels, while selected packs and reasons remain inspectable. The
entire framework library is never autoloaded by default.

## Pack runtime loading

```text
project/workload fingerprint
→ selected pack references
→ operation-conditional bounded Context Compilation
→ scaffold reasoning
```

Fingerprint and pack selection identify potentially relevant framework
knowledge. Context Compilation controls the bounded runtime projection under
its own already-frozen operation-conditional contract. Ideal Scaffold
reasoning consumes only that bounded selected context. Architecture Knowledge
does not redefine Context Compilation authority.

This is an architectural context-economy rule. It establishes no provider token,
cache, wall-clock or economic savings claim.

When framework knowledge is insufficient:

```text
Universal Core
→ mark lens gap
→ bounded source-backed research when material
→ temporary nonauthoritative lens candidate
→ smallest material user/owner questions
```

If uncertainty remains, stay coarse or record the unknown. Temporary lenses
promote only through bounded field use, PL08-compatible evaluation,
recommendation and owner adjudication. No automatic promotion is allowed.

## Explicit V1 exclusions and unfrozen surfaces

V1 does not require RAG, a vector store, a knowledge graph, a specialized
architecture model, an ontology, a formal architecture DSL, mandatory diagrams,
mandatory project citations, large questionnaires or automatic pack promotion.

```text
SPECIALIZED_ARCHITECTURE_MODEL:
DEFERRED
```

No accepted corpus yet binds the project/workload fingerprint, selected
packs/lenses, material questions, user/owner corrections, accepted Ideal
Scaffold, Reality reconciliation or later architecture/implementation
outcomes. Training or fine-tuning now would encode unvalidated architectural
assumptions rather than learned Planning Lite evidence. A specialized model
may be reconsidered later if sufficient accepted field evidence demonstrates a
material advantage over normal reasoning capability plus curated framework
knowledge.

```text
NOT FROZEN BY THIS SKELETON:
final pack prose and question inventories
pack-content examples and complete source-backed guidance text
pack, fingerprint, driver, selection, scaffold and view schemas
exact pack predicates and decision-table rows
framework-pack canonical path
consumer-scaffold exact path
field-validation design and evidence serialization
Human Guidance schema
Context Compiler pack rendering
future RAG/retrieval contract
future specialized-model contract
production implementation
```

```text
V1_PACK_TOPOLOGY:
FROZEN_CANONICAL

SOURCE_RESEARCH_REQUIRED_BEFORE_SKELETON_FREEZE:
NO

SOURCE_RESEARCH_REQUIRED_BEFORE_PACK_CONTENT_FREEZE:
YES

FRAMEWORK_PACK_CANONICAL_PATH:
NOT_FROZEN

CONSUMER_SCAFFOLD_EXACT_PATH:
NOT_FROZEN

FIELD_VALIDATION_REQUIRED:
YES
```

```text
FRAMEWORK_PACK_CANONICAL_PATH_RESOLUTION:
after the Ideal Scaffold Knowledge skeleton checkpoint and before pack-content
materialization; therefore before field validation depends on canonical packs

CONSUMER_SCAFFOLD_EXACT_PATH_RESOLUTION:
before the first field validation that persists consumer-specific scaffold state
```

The exact consumer scaffold path is not required for skeleton freeze, skeleton
checkpoint or source-backed pack research. Neither path is selected by this
skeleton.

Field validation must eventually discriminate question economy, lens-selection
usefulness, cross-lens composition, scaffold quality, Ideal-first independence
and behavior across materially distinct project classes. This skeleton does
not design or run that validation.

## Roadmap relationship

The bounded skeleton remains within PL-V39-09 / 09-B. It introduces no new
phase, skill, service, registry, database, router, planner or lifecycle stage.
The macro sequence and `CURRENT.md` are unchanged. Production implementation,
pack materialization, source research and field validation remain separately
gated.

```text
IDEAL_SCAFFOLD_KNOWLEDGE_SKELETON:
MATERIALIZED / FROZEN CANONICAL TOPOLOGY

PL-V39-09:
SHAPING ACTIVE
```
