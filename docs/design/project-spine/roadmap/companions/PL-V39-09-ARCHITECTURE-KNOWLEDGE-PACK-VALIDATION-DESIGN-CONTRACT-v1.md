# PL-V39-09 Architecture Knowledge Pack / Validation Design Contract v1

## Authority, scope, and canonical status

```text
PARENT_AUTHORITY:
docs/design/project-spine/roadmap/ROADMAP.md / PL-V39-09 / 09-B

SLICE_ID:
09-B-PACK-VALIDATION-DESIGN

OWNER:
PL-V39-09 / 09-B Ideal Scaffold Knowledge

WORK_CLASS:
BOUNDED_DESIGN

09_B_PACK_VALIDATION_DESIGN:
OWNER_ACCEPTED / CANONICAL_V1

OWNER_ACCEPTED_09_B_PACK_VALIDATION_DESIGN:
YES

CANONICAL_ACCEPTED:
YES
```

This companion is the owner-accepted canonical V1 output of the 09-B design
slice. It is subordinate to `ROADMAP.md` and consumes, without changing, the
frozen Ideal Scaffold Knowledge skeleton and Architecture Knowledge topology.
It contracts future content, paths, and field validation; it is not pack
content, a consumer scaffold, field evidence, a registry, a store, a schema, a
runtime, or implementation authority.

```text
ISK-01..ISK-21:
FROZEN / UNCHANGED

ARCHITECTURE_KNOWLEDGE_TOPOLOGY:
FROZEN_CANONICAL / UNCHANGED

UNIVERSAL_CORE:
FROZEN

DOMAIN_COMPUTATION_LENSES:
FROZEN_4

CROSS_CUTTING_OVERLAYS:
FROZEN_3

OWNERSHIP_SEAMS:
FROZEN

IDEAL_FIRST_INDEPENDENCE:
FROZEN

MONOTONIC_MATERIAL_COMPOSITION:
FROZEN
```

The fingerprint selects candidate knowledge and questions only. It never
selects technology, pattern, project architecture, or project authority.
Architecture Knowledge remains reusable framework guidance. Only accepted
project intent, drivers, constraints, and decisions on their existing owner
surfaces can become project authority.

## Inputs and bounded convention inspection

The execution read the required start contract, independent review, review
findings, selected-slice adjudication, current authority, Roadmap, four named
PL09 companions, PL08 completion review, and the three permitted ownership /
path-convention files in full. No web or external-source retrieval occurred.

Two additional canonical owner documents were indispensable and read under the
start contract's express allowance:

| Additional input | Reason for reading |
|---|---|
| `docs/design/project-spine/checkpoints/PL-V39-06-CONTEXT-MEMORY-HANDOFF-CHANGE-DEFINITION-v1.md` | Confirm the existing five storage classes, the consumer-owned canonical-state boundary, and that derived context/handoff objects do not create a second persistent authority. |
| `docs/design/project-spine/checkpoints/PL-V39-08-PROPOSED-CHANGE-DEFINITION-v1.md` | Bind the exact existing ownership of Attempt identity, observed results, verifier/evaluation evidence, findings, supersession, and owner disposition used by the field-validation handoff. |

Directory and filename inspection was limited to existing companion paths and
the managed `.planning/framework/**`, `.planning/project/**`, and
`.planning/templates/project/**` trees. No live consumer was inspected.

## Pack-content contract

### Contract form shared by all eight modules

The topology contains exactly the eight modules below: one Universal Core,
four domain/computation lenses, and three cross-cutting overlays. Future pack
materialization must satisfy every per-module obligation. The clauses specify
content classes and behavior, not final prose or final question inventories.

For each module:

- `questions to ask` means bounded question subjects and triggers, not fixed
  wording or a mandatory questionnaire;
- `checks` means reasoning/quality obligations, not an evaluator implementation;
- `scenarios` means scenario families the content must help elicit or examine,
  not project claims or preselected architectures;
- provenance binds every material guidance unit to source identity and the
  applicable edition/version/date when available;
- freshness binds a last-reviewed date and `DURABLE` or `CHANGEABLE` class;
- composition preserves every independently material concern and all explicit
  conflicts; and
- owner correction may change selection, applicability, or guidance use but
  cannot silently rewrite source content or grant project authority.

### 1. Universal Core

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Supply genuinely cross-domain materiality detection and shared scaffold reasoning once for every material Ideal Scaffold exercise; keep domain and overlay deltas with their owners. |
| Questions to ask | Cover only material unknowns about purpose, value, actors, critical capabilities and flows, responsibility/data/trust boundaries, interfaces, quality scenarios, hard constraints, risks, decisions, assumptions, and maturity depth. Apply the frozen system-known / derivable / defaultable / must-ask / optional-refinement discipline. |
| Checks | Check that goals and drivers precede structure, defaults are reversible/low-risk/non-architecture-determining, unknowns remain visible, and deeper questioning can materially change the next I0-I4 layer. |
| Scenarios | Require cross-domain success, failure/degradation, boundary, evolution, and recovery scenario families only where material. |
| Trade-off prompts | Expose conflicts among goals, quality attributes, hard constraints, risk, cost, operability, and change without resolving them by precedence. |
| Failure modes | Guard against a universal mega-pack, ceremonial questionnaire, premature structure, silent defaults, missing boundary concerns, and Core absorption of domain depth. |
| Provenance requirements | Bind shared guidance to exact source identity and distinguish framework source claims from project facts or owner decisions. |
| Freshness expectations | Give each guidance unit a review date and justified freshness class; keep time-sensitive shared guidance `CHANGEABLE`, otherwise `DURABLE`. |
| Composition rules | Load shared reasoning once; merge equivalent contributions while retaining every domain/overlay delta and explicit conflict. |
| Selection / exclusion behavior | Universal Core is the bounded common base; exclude specialist depth, mechanisms, vendors, stacks, and questions whose answers cannot affect materiality or the next scaffold layer. |
| Owner correction behavior | Let the project owner correct inferred materiality, defaultability, and question depth; preserve the correction reason and re-evaluate affected module selection without changing the framework source. |
| Project-authority boundary | Core guidance and candidate questions remain non-authoritative until project facts/decisions are explicitly accepted on existing project owner surfaces. |

### 2. Application Delivery

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover application-level delivery concerns through one lens with independently selectable Interaction/Client and Service/API profiles and their conditional seam. |
| Questions to ask | Elicit material interaction channels, client/service responsibilities, public/internal interaction contracts, state placement, trust boundaries, degraded behavior, and evolution constraints without choosing a frontend/backend stack. |
| Checks | Check profile independence, Client-to-Service seam materiality, responsibility/interface clarity, failure behavior, and that frontend/backend remain descriptors rather than new lenses. |
| Scenarios | Cover materially relevant user/system interaction, request/response or event exchange, partial failure, compatibility/change, offline/degraded, and boundary-abuse families. |
| Trade-off prompts | Surface responsiveness, consistency, coupling, evolvability, accessibility/usability, boundary protection, and delivery-cost tensions without selecting a solution. |
| Failure modes | Guard against always loading both profiles, collapsing application concerns into Product or Operations, splitting descriptors into new modules, and assuming a deployment or protocol mechanism. |
| Provenance requirements | Bind guidance to identifiable application/client/service sources and mark the profile and seam to which each unit applies. |
| Freshness expectations | Mark stable interaction/boundary principles `DURABLE`; mark changing platform, protocol, compatibility, or client constraints `CHANGEABLE` with review date. |
| Composition rules | Compose shared Application material once, add selected Client and/or Service/API deltas, and preserve seams with AI, Product, Operations, and SPA. |
| Selection / exclusion behavior | Select the lens when application delivery is material; select each profile independently. Exclude unneeded profiles and all technology/stack selection. |
| Owner correction behavior | Permit correction of channel, profile, interface, and responsibility assumptions; re-run bounded selection and retain the reason for additions/removals. |
| Project-authority boundary | The lens proposes concerns and questions only; accepted application boundaries, interfaces, and technology choices remain project-owned. |

### 3. Data / Knowledge Systems

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover shared data/knowledge authority, state/lifecycle, consistency, evolution, quality, lineage/provenance, and serving concerns, with Graph/Knowledge as a selectable sublens. |
| Questions to ask | Elicit material data authority, semantics, lifecycle, quality, consistency, lineage, access/serving, retention, change, and graph/knowledge relation needs without selecting a datastore. |
| Checks | Check owner/source-of-truth clarity, lifecycle and evolution effects, consistency expectations, provenance, quality failure visibility, and whether Graph/Knowledge depth is independently material. |
| Scenarios | Cover ingest/create, update, read/serve, correction, deletion/retention, schema/meaning evolution, inconsistency, provenance loss, and conditional graph-relation families. |
| Trade-off prompts | Surface consistency, availability, freshness, quality, lineage, query/serving fitness, evolution cost, and operational burden without prescribing a data architecture. |
| Failure modes | Guard against database-first reasoning, treating graph as a mandatory or top-level lens, conflating data truth with runtime realization, and losing provenance through deduplication. |
| Provenance requirements | Bind data guidance to identifiable sources, scoped lifecycle/semantic claims, and the shared foundation or Graph/Knowledge sublens it supports. |
| Freshness expectations | Treat enduring authority/lineage principles as `DURABLE`; changing regulatory, ecosystem, serving, or interoperability guidance as `CHANGEABLE`, each with review date. |
| Composition rules | Compose the shared data foundation once, add Graph/Knowledge only when material, and preserve Data-to-Operations, Product, SPA, Application, and AI seams. |
| Selection / exclusion behavior | Select for material data/knowledge lifecycle or truth concerns; exclude Graph/Knowledge when relations/semantics do not warrant its depth and exclude datastore/product selection throughout. |
| Owner correction behavior | Allow owners to correct authority, lifecycle, consistency, quality, lineage, or sublens applicability; preserve resulting conflicts and selection rationale. |
| Project-authority boundary | Framework data guidance cannot define the project's canonical data model, retention rule, source of truth, datastore, or accepted constraint. |

### 4. AI / ML Systems

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover one shared AI foundation plus independently conditional Predictive/Trained ML and GenAI/Foundation Model profiles, including LLM, RAG/Grounding, and Agentic depth only when material. |
| Questions to ask | Elicit material model/system purpose, data and evaluation dependency, uncertainty/error impact, lifecycle/change, human/control boundary, grounding/tool/action exposure, and profile-specific risks without assuming every AI profile. |
| Checks | Check profile applicability, AI-to-Application/Operations/Data/Product/SPA seams, evaluation need, uncertainty visibility, failure containment, and that GenAI is not promoted to a top-level V1 lens. |
| Scenarios | Cover quality/error, drift/change, unavailable/degraded dependency, unsafe or ungrounded output, human escalation, tool/action boundary, and profile-appropriate misuse/failure families. |
| Trade-off prompts | Surface quality, explainability, latency, cost, autonomy, adaptability, privacy/security, operational burden, and evaluation confidence without selecting a model/provider. |
| Failure modes | Guard against AI label over-selection, always loading Predictive and GenAI profiles, model/provider prescription, evidence claims outside PL08, and temporary-profile self-promotion. |
| Provenance requirements | Bind each guidance unit to source identity, profile scope, evidence confidence, and applicability limits; do not turn cited guidance into project evidence. |
| Freshness expectations | Review fast-moving model, evaluation, safety, and ecosystem guidance as `CHANGEABLE`; retain stable statistical/assurance principles as justified `DURABLE`. |
| Composition rules | Load shared AI foundation once, add only material profiles, and preserve all domain/overlay contributions and explicit conflicts with no last-writer-wins. |
| Selection / exclusion behavior | Select AI/ML only when computational learning/model behavior is material; select profiles independently and exclude unrelated GenAI, RAG, agentic, or predictive depth. |
| Owner correction behavior | Permit owner correction of AI materiality, profile labels, autonomy/control assumptions, and guidance applicability; recompose without deleting material concerns. |
| Project-authority boundary | The module cannot select a model, provider, RAG/agent pattern, evaluation verdict, or accepted AI architecture; those require existing project and PL08 authorities. |

### 5. Solver / Optimization / Scientific Compute

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover optimization, numerical/scientific, stochastic/heuristic, and conditional computational/HPC concerns while Solver owns computational truth and Operations owns runtime realization. |
| Questions to ask | Elicit objective/problem formulation, scientific/numerical truth, constraints, approximation/tolerance meaning, reproducibility, uncertainty, workload shape, verification/validation need, and conditional scale/resource characteristics. |
| Checks | Check problem/constraint correctness, numerical or scientific validity, reproducibility, uncertainty/error treatment, result fitness, and the Solver-to-Operations ownership seam. |
| Scenarios | Cover valid/invalid inputs, infeasible/unbounded or nonconvergent behavior, approximation/error, stochastic repeatability, resource pressure, and recovery/restart families where material. |
| Trade-off prompts | Surface fidelity, optimality, robustness, reproducibility, time/resource cost, scalability, and operational complexity without prescribing algorithms or infrastructure. |
| Failure modes | Guard against algorithm-first selection, false precision, silent infeasibility/nonconvergence, treating HPC as top-level, and assigning runtime mechanics to Solver. |
| Provenance requirements | Bind computational guidance to exact scientific/optimization source identity, applicable problem class, and stated validity limits. |
| Freshness expectations | Classify enduring mathematical/verification principles as `DURABLE`; evolving libraries, methods, hardware-dependent or practice guidance as `CHANGEABLE`. |
| Composition rules | Compose only material computational profiles and retain Solver-owned truth requirements alongside Operations-owned realization, SPA, Product, and Data concerns. |
| Selection / exclusion behavior | Select when optimization, numerical/scientific, or stochastic computation is material; select HPC depth conditionally and exclude algorithm, library, hardware, or platform choice. |
| Owner correction behavior | Permit correction of problem class, validity criteria, uncertainty, reproducibility, or scale assumptions; preserve unresolved computational/operational conflicts. |
| Project-authority boundary | Framework guidance cannot accept a model, formulation, tolerance, algorithm, infrastructure, or scientific validity claim for the project. |

### 6. Product / Distribution

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover consumer-facing promise and public meaning across Consumer Control, Delivery Ownership, Public Contract Exposure, Update Control, and Distribution Rights, plus conditional Support Lifecycle and Tenant/Customer Isolation promises. |
| Questions to ask | Elicit material consumer, custody/transfer, public contract, compatibility/update, rights, support, and isolation promises without treating delivery descriptors as exclusive architecture categories. |
| Checks | Check accountable delivery ownership, public promise clarity, compatibility/support commitment, update authority, rights constraints, and whether isolation is a promised product property. |
| Scenarios | Cover adoption/delivery, update/rollback, compatibility break, support end, rights/distribution conflict, custody transfer, and conditional customer-isolation failure families. |
| Trade-off prompts | Surface provider/consumer control, compatibility versus evolution, distribution reach versus rights, support burden, isolation strength, and delivery accountability. |
| Failure modes | Guard against equating Product with UI, collapsing Product into Operations, treating SaaS/library/CLI/open-source/commercial/internal as exclusive categories, and assigning technical realization to Product. |
| Provenance requirements | Bind guidance to source identity and the exact promise axis/conditional profile; distinguish external policy guidance from an accepted project promise. |
| Freshness expectations | Treat stable ownership/contract principles as `DURABLE`; changing compatibility, distribution, rights, support, and market/ecosystem guidance as `CHANGEABLE`. |
| Composition rules | Preserve Product ownership of public meaning while Application/Data/AI/Operations/SPA own relevant realization; keep all five frozen Product seams explicit. |
| Selection / exclusion behavior | Select when a consumer-facing, delivery, public contract, update, distribution, support, or isolation promise is material; exclude nonmaterial conditional profiles and runtime mechanics. |
| Owner correction behavior | Allow correction of consumer, custody, promise, support, rights, and isolation assumptions; require affected domain/overlay selection to be reconsidered visibly. |
| Project-authority boundary | Guidance cannot create a public promise, compatibility policy, support term, distribution right, or isolation commitment; only the project/product owner can accept them. |

### 7. Operations / Deployment

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover runtime ownership, deployment, health, observation, recovery, capacity, and realized resource/cost operation across material systems. |
| Questions to ask | Elicit runtime operator/custody, environments, deployment/change, health, observability, failure/recovery, capacity, dependency, resource, and cost-operation needs without assuming cloud or orchestration mechanisms. |
| Checks | Check runtime ownership, observable health, recoverability, capacity/resource assumptions, operational change, domain-to-runtime seams, and Product delivery-custody distinction. |
| Scenarios | Cover deploy/change, dependency degradation, overload, partial outage, data/model/solver operational failure, recovery, scaling/capacity, and operator handoff families where material. |
| Trade-off prompts | Surface availability, recoverability, complexity, operability, performance, capacity, resource/cost, and change speed without choosing a platform. |
| Failure modes | Guard against cloud/container/Kubernetes/GitOps/autoscaling/failover/multi-region becoming categories, unowned runtime, invisible failure, and absorption of domain truth or public promises. |
| Provenance requirements | Bind operational guidance to exact source identity and scope; distinguish normative framework guidance from observed project/runtime evidence. |
| Freshness expectations | Treat stable reliability/operability principles as `DURABLE`; platform, service, practice, and threat-sensitive operational guidance as `CHANGEABLE`. |
| Composition rules | Compose runtime realization with every selected domain/overlay concern; preserve AI/Data/Solver/Product/SPA seams and explicit conflicts. |
| Selection / exclusion behavior | Select whenever runtime/deployment operation is independently material; exclude named mechanisms and nonmaterial advanced deployment profiles. |
| Owner correction behavior | Permit operator/project-owner correction of custody, environment, reliability, recovery, scale, and cost assumptions; recompose all affected seams. |
| Project-authority boundary | Guidance cannot choose hosting, deployment, observability, recovery, capacity, or cost architecture and cannot substitute for observed runtime evidence. |

### 8. Security / Privacy / Assurance

| Required dimension | Contractual obligation |
|---|---|
| Purpose / applicability | Cover a shared protection/trust foundation with independently selectable Security, Privacy, and Assurance profiles and the material strength of required assurance. |
| Questions to ask | Elicit material assets/harms, trust and threat boundaries, privacy purposes/subjects/lifecycle, security properties, assurance claims/strength, abuse/misuse, and applicable obligations without reducing Privacy to confidentiality. |
| Checks | Check independent profile materiality, protection/privacy claim ownership, assurance-strength need, cross-module realization seams, and the PL08 evidence-governance boundary. |
| Scenarios | Cover unauthorized action/access, misuse/abuse, data/privacy harm, boundary failure, dependency compromise, recovery, and claim/assurance failure families where material. |
| Trade-off prompts | Surface protection, privacy, usability, autonomy, observability, performance, cost, and assurance-strength tensions without resolving legal or project decisions. |
| Failure modes | Guard against always loading all three profiles, conflating privacy/security/assurance, checklist compliance as proof, a second evidence lifecycle, and security mechanism prescription. |
| Provenance requirements | Bind every material claim/guidance unit to exact source identity, scope/jurisdiction or applicability limit where relevant, and evidence confidence; never treat source presence as verification. |
| Freshness expectations | Mark threat-, law-, policy-, and ecosystem-sensitive guidance `CHANGEABLE`; stable protection/assurance principles may be `DURABLE`, always with review date. |
| Composition rules | Compose independently material profiles and preserve SPA seams with Application, Data, AI, Operations, and Product; PL08 remains the evidence owner. |
| Selection / exclusion behavior | Select the overlay or individual profiles only when independently material; exclusion of one profile must not erase a concern owned by another. Exclude mechanism and compliance-result selection. |
| Owner correction behavior | Allow authorized owners to correct applicability, claim strength, profile selection, and source use; route evidence corrections/disposition to PL08 rather than changing them here. |
| Project-authority boundary | SPA guidance cannot accept project protection/privacy obligations, legal conclusions, assurance claims, controls, evidence, verification, or risk disposition. |

### Cross-module rules

1. **Deduplication without deletion.** Equivalent questions, checks, scenario
   prompts, or guidance units may share one rendered expression only when each
   contributing owner and applicability remains traceable. Deduplication may
   never remove an independently material driver, constraint, failure mode,
   quality concern, protection/privacy concern, scenario, or trade-off effect.
2. **Explicit conflict preservation.** No fixed precedence or last-writer-wins
   rule exists. Conflicting material contributions remain an explicit trade-off
   or unresolved architecture driver for project-owner adjudication.
3. **Smallest material module set.** Begin with Universal Core and select the
   smallest set of materially relevant lenses, overlays, profiles, and
   sublenses. The `prefer 1-3 modules` heuristic is not a cap; broader material
   sets use staged loading, never omission.
4. **Selection explainability.** Every inclusion and exclusion must be
   inspectable as a bounded relation from known fingerprint signals, material
   unknowns, and correction state to candidate module/profile references and a
   plain-language reason. Exact predicates and representation remain unfrozen.
5. **Owner correction.** An owner may correct facts, applicability, defaults,
   or selection. The correction preserves source and prior selection identity,
   identifies affected concerns, triggers bounded recomposition, and cannot
   self-promote temporary content or rewrite project authority.
6. **Provenance and freshness.** Every material guidance unit retains source
   identity, edition/version/date where available, last-reviewed date, and one
   justified freshness class (`DURABLE` or `CHANGEABLE`). Unknown or stale
   mandatory provenance remains visible; it is not silently refreshed.
7. **Monotonic cross-lens composition.** Adding a materially applicable lens,
   overlay, profile, or sublens can add or merge concerns and expose conflicts;
   it cannot make an existing independently material concern disappear.
8. **Framework/project separation.** Selection selects reusable guidance and
   questions. Accepted requirements, drivers, constraints, scaffold semantics,
   decisions, evidence, and implementation stay with their existing project,
   PL06, PL08, and lifecycle owners.

```text
FINAL_PACK_PROSE_WRITTEN:
NO

FINAL_QUESTION_INVENTORIES_WRITTEN:
NO

TECHNOLOGY_RECOMMENDATIONS_MADE:
NO

PROJECT_ARCHITECTURE_DECISIONS_MADE:
NO
```

## Exact path and ownership contract

### Resolved paths

```text
FRAMEWORK_PACK_CANONICAL_PATH:
template/.planning/framework/architecture-knowledge/

CONSUMER_SCAFFOLD_PERSISTENCE_PATH:
.planning/project/ARCHITECTURE_OVERVIEW.md
```

The first path is the exact central-repository canonical root for later pack
materialization. The second is the exact consumer-root-relative path for the
accepted project scaffold. This contract chooses paths and existing ownership
classes only. It does not create either content, choose a multi-file layout,
freeze representation, or authorize a template/consumer write.

### Framework pack resolution

| Property | Resolution |
|---|---|
| Selected path | `template/.planning/framework/architecture-knowledge/` |
| Canonical owner | `PL-V39-09 / 09-B Ideal Scaffold Knowledge` under the central framework owner/change lifecycle |
| Ownership class | `TRACKED_CANONICAL` + `FRAMEWORK GUIDANCE`; rendered consumer path is centrally `managed` by the existing `.planning/framework/**` rule |
| Lifecycle authority | Existing central Planning Lite framework change, review, owner-acceptance, integrity, and release/update authorities |
| Update behavior | Future separately authorized central materialization is tracked here and projects receive it as managed framework content through existing Copier update behavior; it is not covered by `_skip_if_exists` project-state protection. Exact update mechanics/content layout remain downstream. |
| Why selected | The repository already reserves `.planning/framework/**` for centrally managed framework artifacts, while `template/` is the central source of rendered target files. The path gives the eight-module library one canonical root without creating a registry, store, service, runtime, schema, or owner. |

Bounded rejected alternatives:

| Alternative | Why rejected |
|---|---|
| `docs/design/project-spine/roadmap/companions/` | Owns subordinate design contracts/evidence, not rendered reusable framework guidance; pack content here would blur design authority and the distributable framework owner. |
| `template/.planning/docs/architecture-knowledge/` | Is centrally managed but is the documentation class; using it for the canonical pack library would blur reference documentation and framework guidance ownership. |
| `template/.planning/project/**` | Is explicitly project-owned and update-protected; central packs there would invert authority and could become a consumer-side framework copy. |
| `src/planning_lite/**` | Owns distribution CLI implementation, not rendered guidance; placement would couple pack authority to runtime/product code. |

### Consumer scaffold resolution

| Property | Resolution |
|---|---|
| Selected path | `.planning/project/ARCHITECTURE_OVERVIEW.md` in each consumer root; its central seed counterpart is `template/.planning/project/ARCHITECTURE_OVERVIEW.md` |
| Canonical owner | The consumer/project owner through existing Project Spine and project decision authorities |
| Ownership class | `CONSUMER-OWNED TRACKED_CANONICAL`; explicitly `project_owned` by `OWNERSHIP.yml` and covered by Copier `_skip_if_exists: .planning/project/**` |
| Lifecycle authority | Existing consumer Project Spine, project-owner acceptance, governed Change/decision, and project Git authorities |
| Update behavior | Planning Lite may seed the file only when absent. Once present, framework updates do not overwrite it. The consumer owner accepts and changes scaffold state. Managed templates may evolve separately but never replace accepted content. |
| Why selected | It is the existing exact project-owned architecture path and therefore can hold the accepted structured semantic scaffold as primary architecture authority without creating a second project path, state class, or lifecycle. This path decision does not freeze the internal representation or require every derived view to persist. |

Bounded rejected alternatives:

| Alternative | Why rejected |
|---|---|
| `.planning/templates/project/ARCHITECTURE_OVERVIEW.md` | Is a managed scaffold template, not accepted consumer state; making it canonical would let framework updates compete with project authority. |
| `.planning/project/TARGET_STATE.md` | Owns target intent; making it the architecture-scaffold authority would blur Target and Architecture ownership. References may be composed without merging authorities. |
| `.planning/assessments/current/**` | Owns current assessment/snapshot material, not the accepted target Ideal Scaffold; it would turn evidence into project architecture authority. |
| A new `.planning/project/IDEAL_SCAFFOLD.*` path | Is unnecessary while the existing architecture owner path is sufficient and would risk a parallel/shadow architecture authority. |

### Path invariants

```text
ONE_CANONICAL_OWNER_PER_OWNED_ARTIFACT_CLASS:
YES

ONE_CANONICAL_PATH_PER_OWNED_ARTIFACT_CLASS:
YES

DUPLICATE_AUTHORITY_CREATED:
NO

SHADOW_REGISTRY_CREATED:
NO

SECOND_KNOWLEDGE_STORE_CREATED:
NO

CONSUMER_SIDE_COPY_BECOMES_FRAMEWORK_AUTHORITY:
NO

PACK_SELECTION_BECOMES_PROJECT_AUTHORITY:
NO
```

Framework pack materialization and consumer scaffold mutation remain separately
unauthorized. A consumer may reference the managed pack path, but its accepted
scaffold at `.planning/project/ARCHITECTURE_OVERVIEW.md` wins for project facts
and decisions. A copied/exported pack is never a second canonical pack.

## Minimum schedulable field-validation design

### Authorization boundary

```text
FIELD_VALIDATION_DESIGN:
SCHEDULABLE

FIELD_VALIDATION_EXECUTED:
NO

FIELD_VALIDATION_COMPLETE:
NO

ACTUAL_FIELD_RUNS_AUTHORIZED:
NO
```

This section defines a later campaign that can be scheduled after its
prerequisites and separate owner gate are satisfied. It neither selects live
projects nor creates Attempts, evidence, findings, or acceptance.

### Admissible materially distinct project classes

A future case is admissible only when its controlling project/fixture owner
permits the use, exact input/source identity can be bound, the case has enough
accepted intent/domain truth to exercise Ideal-first reasoning, and no live
mutation occurs beyond separately authorized scope.

| Class | Material distinction the case must expose | Intended topology pressure |
|---|---|---|
| FV-PC-01: interaction/service application | User/system interaction plus a material client/service boundary and at least one public promise or protection concern | Universal Core; Application profiles; conditional Product, Operations, and SPA seams |
| FV-PC-02: stateful data/knowledge system | Material authority, lifecycle, consistency, provenance, serving, and a case variant where graph/knowledge depth is either clearly material or clearly excludable | Universal Core; Data/Knowledge foundation and sublens selection; Operations/Product/SPA seams |
| FV-PC-03: AI-enabled system | A material AI function with a case variant distinguishing Predictive/Trained ML from GenAI/grounding/agentic depth, including data, evaluation, and control boundaries | Universal Core; selected AI profiles; Application/Data/Operations/Product/SPA seams |
| FV-PC-04: solver/scientific delivery | Material optimization/numerical/stochastic truth plus resource/runtime and delivery concerns, with computational/HPC depth conditionally material | Universal Core; Solver profiles; Solver-to-Operations seam; conditional Product and SPA |

Cases may be synthetic, qualified historical fixtures, or separately permitted
projects. They must remain materially distinct; renaming one scenario or stack
does not create a new class. No particular current consumer is selected here.

### Hypotheses and qualitative expected observations

| ID | Discriminator / hypothesis | Qualitative observation expected if supported | Challenge signal requiring correction or adjudication |
|---|---|---|---|
| FV-H01 | Question economy | The trace asks only unknowns able to change materiality, an accepted driver, boundary, constraint, or next scaffold layer. | Ceremonial/repeated questions, questions answerable from admitted inputs, or omitted material unknowns. |
| FV-H02 | Progressive questioning | I0-I4 depth advances only when the next layer is justified by prior answers and case materiality. | Deep structural questioning before purpose/drivers or failure to deepen after a material trigger. |
| FV-H03 | Lens/overlay selection usefulness | Selected modules expose material concerns not already covered by Core while nonmaterial modules stay excluded. | Selected module adds no case-relevant value or an excluded module contains a material concern. |
| FV-H04 | Selection explainability | A reviewer and owner can reconstruct each inclusion/exclusion from admitted fingerprint facts, material unknowns, and corrections. | Opaque, circular, technology-derived, or irreproducible selection rationale. |
| FV-H05 | Monotonic cross-lens composition | Adding a materially applicable module adds/merges concerns and exposes conflicts without removing an existing material contribution. | A material concern disappears, is weakened by precedence, or becomes untraceable after composition. |
| FV-H06 | Preservation of material concerns | Deduplication reduces repetition while retaining independently material drivers, constraints, failure modes, scenarios, quality/protection concerns, and trade-off effects. | Semantic loss is hidden by a shared phrase or owner/seam identity disappears. |
| FV-H07 | Scaffold quality | The accepted candidate scaffold is coherent, decision-useful, driver-bound, honest about unknowns, and sufficient to derive useful views without creating a second architecture authority. | Structure is generic, technology-led, internally contradictory, falsely complete, or dependent on a separate authoritative view. |
| FV-H08 | Ideal-first independence | Conceptual Ideal uses accepted goals/domain truth/intrinsic constraints and excludes current implementation until owner-accepted constraints form the Constrained Target Ideal. | Current packages, file layout, vendor, legacy topology, or historical shortcuts silently determine the Ideal. |
| FV-H09 | Source/provenance handling | Material guidance remains traceable to exact source identity and scope while project facts/decisions remain separately owned. | Missing/misattributed source, pack citation treated as project evidence, or framework/project provenance conflated. |
| FV-H10 | Freshness handling | Review date and `DURABLE`/`CHANGEABLE` class make stale or uncertain guidance visible and route it for correction rather than silent use. | Missing review identity, unsupported freshness claim, hidden staleness, or an invented update scheduler. |
| FV-H11 | User/owner correction behavior | A correction visibly updates selection/applicability or scaffold reasoning, preserves prior/source identity, and does not erase unrelated material concerns. | Correction is ignored, silently rewrites source/history, broadens authority, or destabilizes unrelated composition. |
| FV-H12 | Authoring cost | The case record identifies where effort was spent and whether each cost was necessary for material reasoning, correction, provenance, or review. | Repeated manual duplication, unexplained overhead, or cost hidden by omitting required provenance/correction work. |

These are qualitative design discriminators. The PL08 owner determines evidence
applicability/completeness and whether observations `SUPPORT`, `CHALLENGE`, or
`VERIFY` an owning claim. This contract freezes no score, threshold, quota,
minimum count, calibration cutoff, or acceptance algorithm.

### Minimum case procedure and evidence channels

Each future case is schedulable as the following bounded, owner-authorized
sequence; this sequence is a validation design, not runtime orchestration:

1. Bind the separately authorized Attempt, case/fixture/project identity,
   candidate pack identity, pack-content revision, accepted intent/domain-truth
   inputs, baseline/current-implementation identity kept outside Conceptual
   Ideal, operator/owner role, and applicable verifier contracts.
2. Capture the admitted input boundary and a bounded question/answer trace,
   including system-known, derivable, defaultable, must-ask, and
   optional-refinement treatment.
3. Record candidate module/profile inclusions and exclusions with reasons;
   preserve the before-correction selection.
4. Produce a candidate Ideal Scaffold through the separately authorized
   consumer path, then introduce current implementation only through the
   Reality/reconciliation boundary. Persistence is optional per case but, if
   used, is only at `.planning/project/ARCHITECTURE_OVERVIEW.md` under consumer
   authority.
5. Exercise at least one material owner correction and, when applicable, one
   cross-module conflict/deduplication probe. Do not manufacture a correction
   whose premise is not material to the case.
6. Capture observations through the minimum applicable channels and hand them
   to PL08-owned evaluation; no case self-accepts or self-promotes content.

Admissible evidence channels are bounded question/selection traces, exact
input/source references, candidate and accepted scaffold diffs or references,
review observations, owner-correction records, provenance/freshness inspection,
and qualitative authoring-cost notes. Existing Git references may identify
tracked bytes. No evidence serialization, carrier schema, instrumentation, or
production evaluator is frozen.

### Source/input identity and authoring-cost capture

Every run must bind enough existing identity to distinguish:

- the owner authorization and PL08 Attempt;
- the materially distinct case and admissible fixture/project source;
- candidate pack content and source/provenance/freshness state;
- accepted project intent/domain truth and explicitly accepted hard constraints;
- current implementation/baseline withheld from Conceptual Ideal and later used
  for Reality reconciliation;
- the candidate/accepted scaffold state, correction event, applicable review,
  and evidence scope.

The identity contract does not prescribe fields or serialization. Missing,
stale, conflicting, or non-portable mandatory identity makes the relevant
observation inapplicable or causes a non-executing STOP through PL08/owner
governance; it is never filled by inference.

Authoring cost is captured qualitatively by activity class: input preparation,
question answering, selection explanation, scaffold authoring, provenance and
freshness work, correction/recomposition, independent review, and evidence
handoff. Record avoidable repetition and necessary material work separately.
Do not freeze time/token budgets, numeric thresholds, instrumentation, or a
universal cost scalar.

### Correction paths and stop behavior

| Observed condition | Bounded correction path |
|---|---|
| Wrong or unexplained module/profile selection | Owner corrects admitted fact/applicability; preserve prior selection and reason; recompose the smallest material set. |
| Duplicate wording with preserved material meaning | Deduplicate the expression while retaining contributing owners, scopes, and concern identities. |
| Material concern lost or conflict hidden | Restore the concern/conflict; classify the contract or pack content issue through PL08 findings; do not change frozen topology in the run. |
| Guidance is stale, unsupported, or outside source scope | Mark it unusable/unknown for the case and route to separately authorized source research/content correction. |
| Scaffold became technology-led or current-state-led | Return to accepted intent/domain truth and the Ideal-first boundary; preserve the failed observation for PL08 evaluation. |
| Owner rejects proposed guidance or scaffold content | Preserve the project-owner decision and its scope; framework guidance remains unchanged unless a later governed content correction is authorized. |

A future run stops without execution/acceptance when authority, case identity,
mandatory provenance, pack revision, consumer ownership, or evidence
applicability cannot be resolved; when a frozen topology/invariant would need
to change; when material selection becomes project authority; or when safe
correction would require a new owner, lifecycle, registry, store, schema,
runtime, 09-E, or 09-F semantic. A stopped run preserves the exact conflict and
source identities for PL08 findings and owner disposition.

### PL08-owned evidence handoff

09-B owns hypotheses, case distinctions, expected qualitative observations,
pack/scaffold inputs, and correction/stop design. It hands the actual run to
the existing PL08 owner without absorbing any of these semantics:

```text
PL08 EXCLUSIVELY OWNS:
Attempt identity
observed results
SUPPORTS
CHALLENGES
VERIFIES
evidence applicability/completeness
technical evaluation/acceptance
findings
evidence supersession
owner disposition
```

An observation, green check, reviewer statement, or completed case is evidence,
not authorization or owner acceptance. Historical failures remain visible.
Corrective execution requires separate authority and a PL08-compatible Attempt
identity; this document creates neither.

### Non-absorbing Engineering Basis / Rationale Lineage seam

The Engineering Basis / Rationale Lineage semantic contract remains canonical
for its meanings. 09-B may co-schedule compatible cases and supply Architecture
Knowledge/scaffold inputs only. It does not redefine rationale relations,
orphan exceptions, current-validity projection, impact-review semantics, or
project rationale authority.

| Owner-contract hypothesis | Compatible case observation to schedule | Ownership preserved |
|---|---|---|
| Usefulness | Whether an optional, source-bound Engineering Basis helps explain a material scaffold target without turning pack guidance into project authority or duplicating rationale. | Hypothesis and semantics remain Engineering Basis / Rationale Lineage-owned; observations/evaluation remain PL08-owned. |
| Exception admission | Whether the existing bounded orphan-exception predicates admit only cases with exact existing authority, scope, reason, and required revisit/expiry where applicable. | Exception classes and admission semantics remain Rationale Lineage-owned; 09-B invents no class or threshold. |
| Impact-review behavior | Whether a material source/premise/basis/scope/challenge change requests bounded review while preserving acceptance-time history and avoiding silent adopter mutation. | Impact-review semantics remain Rationale Lineage-owned; findings, supersession evidence, and disposition remain PL08-owned. |

Engineering Basis field runs require their own owner gate. A shared case does
not merge the contracts, establish `JUSTIFIED_BY`, prove a rationale edge,
close an orphan, or claim Explanation Closure.

## Downstream dependency ledger

Classifications are limited to the authorized closed set. `NOT_REQUIRED` is
exclusive; no row below uses it because every named downstream item has at
least one real dependency or separate gate. The ledger exposes prerequisites
and grants no permission or new sequence.

| Downstream item | Prerequisites | Classification(s) | Owner | Current authorization | Next gate | Reason |
|---|---|---|---|---|---|---|
| Final pack prose | Accepted 09-B design; resolved framework path; governed sources/provenance and freshness basis | `REQUIRES_SOURCE_RESEARCH`; `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 / 09-B pack-content owner | `NO` | Owner authorization for bounded source research and pack-content authoring | This slice defines obligations only; trustworthy final prose requires source-backed content work. |
| Final question inventories | Accepted 09-B design; resolved framework path; source-backed module content; field feedback before final freeze | `REQUIRES_SOURCE_RESEARCH`; `REQUIRES_FIELD_VALIDATION`; `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 / 09-B pack-content owner | `NO` | Owner authorization for research/content drafting, then separately authorized validation/finalization | Fixed inventories would prematurely freeze question economy and progressive-question behavior. |
| Source-backed guidance | Accepted design; bounded research question/scope; exact source/provenance/freshness handling; canonical framework path | `REQUIRES_SOURCE_RESEARCH`; `REQUIRES_CONTENT_MATERIALIZATION`; `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 / 09-B with existing source/review owners | `NO` | Owner authorization for bounded source research, followed by content materialization review | Source-backed claims cannot be produced by this source-research-free design slice. |
| Pack materialization | Owner-accepted design; `template/.planning/framework/architecture-knowledge/`; source-backed content; ownership/integrity/update acceptance | `REQUIRES_CONTENT_MATERIALIZATION`; `REQUIRES_SEPARATE_OWNER_GATE` | Central Planning Lite framework / PL-V39-09 09-B | `NO` | Owner authorization for bounded pack materialization | Path resolution is not permission to create the pack or mutate template/manifest/integrity surfaces. |
| Consumer scaffold persistence | Owner-accepted design; `.planning/project/ARCHITECTURE_OVERVIEW.md`; consumer permission and accepted scaffold content | `REQUIRES_PERSISTED_CONSUMER_PATH`; `REQUIRES_SEPARATE_OWNER_GATE` | Individual consumer/project owner | `NO` | Consumer-owner authorization for a bounded scaffold write or field run | The exact path is resolved, but project-owned state cannot be written by framework authority. |
| Architecture Knowledge field runs | Materialized source-backed candidate packs; admissible cases; exact pack and input identity; consumer permission/path where persisted; PL08 contracts | `REQUIRES_SOURCE_RESEARCH`; `REQUIRES_CONTENT_MATERIALIZATION`; `REQUIRES_PERSISTED_CONSUMER_PATH`; `REQUIRES_FIELD_VALIDATION`; `REQUIRES_SEPARATE_OWNER_GATE` | 09-B hypothesis/case owner + PL08 evidence owner + consumer owner | `NO` | Owner authorization for a bounded Architecture Knowledge field-validation campaign | The design is schedulable, but actual runs and validation-completion claims are separate. |
| Engineering Basis / Rationale Lineage field runs | Canonical semantic contract; admissible cases; existing project authority; PL08 evidence handoff | `REQUIRES_FIELD_VALIDATION`; `REQUIRES_SEPARATE_OWNER_GATE` | Engineering Basis / Rationale Lineage semantic owner + PL08 evidence owner | `NO` | Owner authorization for its bounded field-validation campaign | 09-B may co-schedule cases but cannot absorb usefulness, exception, or impact-review semantics. |
| 09-E capability/executor contract | Separate owner-selected 09-E slice/start contract; accepted inputs as that owner determines | `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 / 09-E | `NO` | Owner decision/start contract for 09-E | Canonical authority does not prove 09-B is a hard prerequisite; this ledger neither invents nor starts 09-E. |
| 09-F Context Compiler / AgentWorkPacket contract | Accepted 09-E capability/executor requirements plus separate 09-F contract authority; frozen conditional skeleton boundary | `REQUIRES_09_E`; `REQUIRES_09_F`; `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 / 09-F | `NO` | Owner decision/start contract for 09-F after its accepted prerequisites | 09-F owns applicability/optional bounded compilation; no packet/schema/runtime semantics are supplied here. |
| Context Compiler comparator preparation | Fair comparator scope including arm D; accepted 09-E requirements and sufficient 09-F/AgentWorkPacket contract; qualified PL08 evaluation boundary | `REQUIRES_09_E`; `REQUIRES_09_F`; `REQUIRES_SEPARATE_OWNER_GATE` | Roadmap PL-V39-09 comparator experiment owner + PL08 evidence owner | `NO` | Owner authorization for bounded comparator preparation after prerequisite acceptance | Generic arms do not make a fair four-arm comparator; this design grants no preparation or run authority. |
| Safe Orchestration field proof | Separately accepted orchestration contract; proven deterministic/read-only transitions; PL08-qualified behavioral evidence; human gates preserved | `REQUIRES_FIELD_VALIDATION`; `REQUIRES_SEPARATE_OWNER_GATE` | PL-V39-09 Safe Orchestration owner + PL08 evidence owner | `NO` | Owner authorization for a separately bounded Safe Orchestration proof | Compiler promotion is optional, so this ledger does not invent 09-E/09-F as hard prerequisites for the validated non-compiler path. |
| Release/promotion decision | Required Roadmap release evidence, field proofs, implementation/rollback state, research disposition, residue accounting, and explicit owner decision | `REQUIRES_FIELD_VALIDATION`; `REQUIRES_SEPARATE_OWNER_GATE` | Existing Planning Lite release/promotion owner | `NO` | Explicit release/promotion owner gate after all applicable prerequisites | A candidate design, pack, or field result cannot authorize release; Context Compiler promotion is not mandatory. |

## Explicit non-goals

This candidate does not and must not:

- reopen the frozen topology, ISK-01..ISK-21, ownership seams, Ideal-first
  independence, or monotonic material composition;
- run web/source research, retrieve external sources, or promote temporary
  lenses;
- write final pack prose, final question inventories, or source-backed guidance;
- materialize pack files or persist consumer scaffold state;
- run field validation, inspect live field consumers, or claim validation
  completeness;
- design or execute 09-E, full 09-F, a Context Compiler comparator, or Safe
  Orchestration;
- freeze schema, serialization, storage, portable anchors, retrieval, runtime,
  evidence carriers, instrumentation, thresholds, evaluators, or technology;
- mutate product, template, source, tests, `.planning/**`, Roadmap, CURRENT, or
  any existing companion; or
- stage, commit, tag, push, merge, release, promote, or authorize production
  implementation.

## Mandatory STOP conditions

Any later use of this contract must stop and preserve the exact conflict and
source identities if:

- a frozen topology item or invariant would need to change;
- a new owner or lifecycle is required;
- pack selection would become project authority;
- a path decision would imply storage/runtime architecture or require a
  registry, service, schema, serialization, or representation authority;
- a numeric threshold would need to be frozen;
- 09-E or 09-F semantics would need to be invented;
- source research or a field run would be required to complete this design;
- the authorized tracked write surface would need to exceed this companion; or
- canonical owner documents conflict materially.

The blocker route is exactly:

```text
NEXT_SINGLE_GATE:
OWNER_ADJUDICATION_PL_V39_09_09-B-PACK-VALIDATION-DESIGN_BLOCKER
```

No such STOP condition was encountered during this bounded design execution.

## Definition of done and status

```text
PACK_CONTENT_CONTRACT:
COMPLETE

FRAMEWORK_PACK_PATH_CONTRACT:
RESOLVED

CONSUMER_SCAFFOLD_PATH_CONTRACT:
RESOLVED

FIELD_VALIDATION_DESIGN:
SCHEDULABLE

DEPENDENCY_LEDGER:
COMPLETE

FROZEN_TOPOLOGY_CHANGED:
NO

PL08_EVIDENCE_OWNERSHIP_PRESERVED:
YES

PROJECT_AUTHORITY_BOUNDARY_PRESERVED:
YES

09_E_OR_09_F_SEMANTICS_INVENTED:
NO

SOURCE_RESEARCH_EXECUTED:
NO

FIELD_VALIDATION_EXECUTED:
NO

PRODUCTION_IMPLEMENTATION_AUTHORIZED:
NO
```

This design contract is owner-accepted and canonical V1. The 09-B design slice
exit gate is satisfied. Acceptance does not execute or authorize source
research, pack materialization, consumer scaffold writes, field validation,
09-E, 09-F, implementation, release, promotion, or any dependency in the
ledger.

```text
SLICE_EXIT_GATE_SATISFIED:
YES

DOWNSTREAM_WORK_AUTHORIZED_BY_ACCEPTANCE:
NO
```
