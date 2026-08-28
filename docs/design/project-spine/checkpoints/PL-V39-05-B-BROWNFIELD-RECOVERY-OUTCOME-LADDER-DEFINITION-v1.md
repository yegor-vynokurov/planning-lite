# PL-V39-05-B — Brownfield Recovery + Outcome Ladder

- Status: `DEFINED / NOT STARTED`
- Date: `2026-08-28`
- Planning Lite revision: `c9deee6f24c3e4a4ab37ebb01ad80ba6d4b03c0e`
- Parent roadmap outcome: `PL-V39-05 / Shaping`
- Prior validated slice: `PL-V39-05-A / Survey + Clarification`
- Consumer field evidence: Poker PL-V39-05-A field-pilot verdict `52125eb2397fbc47f274b214cabfdacdeaedc100f8aa4e39f958ce8e46eb4e2e`
- Implementation authorization: `NO`
- Release/public export authorization: `NO`

## 1. Purpose

PL-V39-05-B adds the next bounded shaping layer after Survey + Clarification.

The slice has two responsibilities:

1. **Brownfield Recovery** — recover only the material prior direction, authority, provenance, and unresolved historical conflicts needed to shape an existing project safely.
2. **Outcome Ladder** — express success as a bounded sequence of observable outcome levels without turning that sequence into a task plan, architecture prescription, Roadmap, or Definition of Done.

This slice must remain usable on existing projects with uneven or stale history while preserving already accepted authority whenever sufficient current direction already exists.

## 2. Why this slice exists

PL-V39-05-A established and field-validated that Planning Lite can:

- gather bounded AS-IS evidence through Project Survey;
- keep `SURVEY = AS-IS EVIDENCE` separate from accepted Target intent;
- distinguish Target-boundary, capability-design, and research questions;
- avoid rewriting Target/Gap/Roadmap merely because evidence became fresher.

The next unresolved shaping problem is not more repository inspection.

It is:

```text
What prior direction still matters?
What authority does it have?
What conflicts remain unresolved?
What observable outcomes would count as progressively stronger success?
```

These questions must be answered before later adaptive depth/strategy selection can operate reliably.

## 3. Scope

### 3.1 In scope — Brownfield Recovery

Brownfield Recovery MAY inspect bounded historical/project evidence needed to recover material direction, including:

- accepted current Target/direction artifacts;
- Project Charter or equivalent intent authority;
- Project Survey findings that reveal stale or conflicting current-state caches;
- prior accepted decisions/checkpoints;
- superseded or migrated direction artifacts when provenance matters;
- historical conflicts that materially affect present shaping;
- explicit user decisions;
- existing authority ordering or ownership rules.

Brownfield Recovery MUST:

- distinguish current authority from historical residue;
- preserve provenance;
- label unresolved conflict rather than silently normalize it;
- stop when sufficient current direction already exists;
- avoid importing irrelevant project history;
- avoid treating age, location, or document volume as authority;
- avoid promoting repository evidence into user intent.

### 3.2 In scope — Outcome Ladder

Outcome Ladder MUST express successive observable outcome levels for the shaped project/direction.

A ladder MAY include levels such as:

- minimum useful outcome;
- credible/complete bounded outcome;
- stronger outcome;
- stretch/optional outcome.

The exact number of levels is not mandatory.

Each level MUST describe an observable state of success, not a set of implementation tasks.

The ladder MUST:

- remain grounded in accepted or recovered direction;
- preserve material non-goals and constraints;
- make stronger levels cumulative only when that is actually true;
- allow a bounded project to stop at a useful lower level where appropriate;
- remain compatible with later Target shaping;
- remain distinct from Roadmap sequencing.

## 4. Explicitly out of scope

PL-V39-05-B MUST NOT implement or define the full behavior of:

- Adaptive Engagement;
- Strategy Portfolio;
- Target Skeleton;
- Executable Target Contract;
- broad Roadmap synthesis enrichment;
- generic research workflow;
- execution/change orchestration;
- PromptOps/evaluation infrastructure;
- release/public export.

It MUST NOT:

- activate a Change merely because recovery found historical debt;
- rewrite accepted Target automatically;
- repair stale project documents automatically;
- create implementation tasks from Outcome Ladder levels;
- infer missing user intent from repository structure alone;
- collapse research questions into Target decisions;
- select implementation strategy.

## 5. Inputs

Required input is one of:

### Path A — Existing accepted direction

An accepted Target or equivalent current direction authority exists and is sufficiently determinate.

Brownfield Recovery should be minimal or bypassed.

### Path B — Recoverable brownfield direction

No sufficient current accepted direction exists, but bounded historical/user/project authority can recover a usable direction candidate.

A recovered direction in Path B is **not accepted Target authority by recovery alone**.

Its default status is:

`RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`

It may ground bounded clarification and provisional Outcome Ladder work, but it MUST NOT be treated as accepted TO-BE intent unless an existing authority rule or explicit user decision promotes it.

### Path C — Insufficient/conflicted direction

Material direction remains unresolved after bounded recovery.

The slice must stop and expose the unresolved authority/Target-boundary question rather than manufacture a baseline.

Optional supporting inputs:

- Project Survey;
- Project Charter;
- current Target;
- prior Target/direction artifacts;
- accepted checkpoints/decisions;
- Current Capability Assessment;
- project ownership/authority rules.

## 6. Brownfield Recovery evidence model

Every recovered direction claim MUST be classifiable as one of:

- `CURRENT_ACCEPTED_AUTHORITY`
- `EXPLICIT_USER_DECISION`
- `PRIOR_ACCEPTED_AUTHORITY`
- `EXISTING_DIRECTION`
- `HISTORICAL_RESIDUE`
- `CONFLICTED_AUTHORITY`
- `UNKNOWN`

The names may be refined during implementation, but the semantic distinction is required.

The recovery result MUST NOT flatten these classes into one undifferentiated narrative.

## 7. Brownfield Recovery stop rules

Recovery MUST stop when any of the following is true:

### BR-STOP-01 — Sufficient current authority

A current accepted Target/direction is materially sufficient for downstream shaping.

Historical recovery is not required merely because older artifacts exist.

### BR-STOP-02 — Bounded provenance sufficient

Enough provenance has been recovered to explain the current direction and material conflicts.

Additional historical reading would not materially change shaping.

### BR-STOP-03 — Material unresolved conflict

Two or more materially different authorities remain live and cannot be safely ordered under existing rules.

The recovery result must expose the conflict and hand off to clarification/user decision.

### BR-STOP-04 — Evidence exhaustion

Available bounded evidence cannot establish a safe direction baseline.

Do not invent one.

## 8. Brownfield Recovery output contract

A successful recovery output MUST contain:

1. current usable direction authority or explicit statement that existing accepted direction is reused;
2. if no accepted direction exists, a `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`, never an implicitly accepted replacement Target;
3. authority/provenance classification for material direction claims;
4. material historical conflicts, if any;
5. historical residue explicitly excluded from current authority;
6. unresolved questions that still block downstream shaping;
7. freshness/reuse decision;
8. bounded evidence references.

### Authority ceiling

Brownfield Recovery may **preserve or lower confidence/authority**, but it may not silently raise authority.

In particular:

```text
historical/project evidence
→ may support a recovered candidate

recovered candidate
→ does NOT become accepted Target intent without an acceptance authority
```

Where an accepted Target already exists, that accepted authority remains the ceiling and governing TO-BE source unless explicitly changed.

It MUST NOT become:

- a project history essay;
- a second Current State;
- a second Target;
- a second Gap Map;
- a repository archaeology dump.

## 9. Outcome Ladder semantic contract

Outcome Ladder represents:

```text
increasingly stronger observable success
```

It does NOT represent:

```text
task ordering
implementation phases
module decomposition
change sequencing
release plan
```

A valid ladder level answers:

> What would be observably true if this level of the project outcome were achieved?

A task-shaped statement such as:

```text
Implement API
Add tests
Write docs
```

is invalid as a ladder level.

An outcome-shaped statement such as:

```text
A reviewer can use the supported boundary, observe deterministic failures,
and reproduce representative evidence from documented setup.
```

is valid.

## 10. Outcome Ladder authority inheritance

Outcome Ladder MUST inherit the authority ceiling of the direction that grounds it.

Rules:

- ladder grounded in an accepted Target/direction may be treated as derived shaping evidence under that accepted authority;
- ladder grounded in `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL` is itself `PROVISIONAL`;
- ladder generation MUST NOT promote a recovered candidate into accepted intent;
- ladder strength levels describe stronger observable outcomes, not stronger authority;
- a ladder cannot authorize Target mutation, Roadmap work, Change execution, or release.

This rule is mandatory because Outcome Ladder is a shaping derivative, not an authority-elevation mechanism.

## 11. Outcome Ladder minimum content

Each level MUST include:

- `Outcome statement`
- `Observable evidence`
- `Material constraints / non-goals`
- `What stronger level adds` when applicable

A ladder MUST also include:

- grounding authority;
- whether levels are cumulative;
- minimum useful stopping level;
- unresolved Target-boundary questions, if any;
- hand-off note for later shaping.

## 12. Outcome Ladder anti-duplication rules

The ladder MUST NOT duplicate:

### Target

Target answers what accepted TO-BE intent governs the project.

Outcome Ladder expresses gradations of observable success under that direction.

### Gap Map

Gap Map compares current capability to Target.

Outcome Ladder does not assess current satisfaction.

### Roadmap

Roadmap orders intended work/outcomes over time.

Outcome Ladder does not select order or timing.

### Definition of Done

Definition of Done is an execution/closure contract.

Outcome Ladder describes success strength, not task completion mechanics.

## 13. Existing accepted Target bypass rule

When an accepted, determinate Target already exists:

- Brownfield Recovery MAY return `REUSE_CURRENT_ACCEPTED_DIRECTION`;
- historical recovery SHOULD be bounded to material provenance/conflict only;
- no replacement Target is created;
- Outcome Ladder is derived from accepted direction plus material constraints;
- open capability-design/research questions remain owned by their proper later workflows.

This bypass rule is mandatory.

The Poker field pilot demonstrated why: stale AS-IS caches did not make its accepted Target invalid.

## 14. Conflict handling rule

Brownfield Recovery MUST NOT silently choose between conflicting material authorities.

A material conflict is one where two reasonable downstream shapers could produce materially different project outcomes depending on which authority they treat as governing.

Such conflict MUST be:

1. recorded;
2. provenance-labeled;
3. classified by ownership where possible;
4. handed to clarification/user decision when existing authority rules cannot resolve it.

## 15. Acceptance contract

PL-V39-05-B is `PASS` only when all acceptance criteria below are demonstrated.

### AC-BR-01 — Bounded recovery

Given a brownfield project with mixed historical evidence, recovery reads only evidence materially necessary to recover direction/provenance.

Pass condition:

- no full-history sweep is required by default;
- bounded stop rule is demonstrated.

### AC-BR-02 — Authority preservation

Given current accepted direction plus stale historical residue, recovery preserves current accepted authority.

Pass condition:

- stale residue is not promoted;
- accepted Target/direction is not rewritten merely because history differs.

### AC-BR-03 — Conflict honesty

Given materially conflicting direction artifacts with no existing resolution rule, recovery exposes the conflict.

Pass condition:

- no silent reconciliation;
- unresolved conflict is explicit and blocks only the appropriate downstream boundary.

### AC-BR-04 — Safe bypass

Given a sufficient accepted Target, recovery returns a bounded reuse/bypass result.

Pass condition:

- no unnecessary brownfield archaeology;
- provenance may be retained without creating a replacement Target.

### AC-BR-05 — No silent authority promotion

Given recoverable historical/project direction but no accepted Target, recovery produces a provisional candidate rather than accepted intent.

Pass condition:

- result is explicitly `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`;
- no recovered claim becomes accepted Target authority without an existing acceptance rule or explicit user decision.

### AC-OL-01 — Outcome, not tasks

Given recovered/accepted direction, generated ladder levels describe observable success states.

Pass condition:

- no level is primarily a task list, component list, or implementation sequence.

### AC-OL-02 — Useful strength gradient

The ladder distinguishes at least:

- a minimum useful bounded outcome;
- a materially stronger outcome.

Pass condition:

- stronger level adds observable value, not just more implementation detail.

### AC-OL-03 — Proper authority grounding

Every ladder is traceable to accepted/recovered direction and material constraints.

Pass condition:

- repository evidence alone does not create new TO-BE intent.

### AC-OL-04 — Anti-duplication

The ladder remains distinguishable from Target, Gap Map, Roadmap, and execution DoD.

Pass condition:

- it neither assesses current satisfaction nor selects execution order.

### AC-OL-05 — Minimum useful stop

The ladder identifies a level at which the bounded project can legitimately stop if stronger outcomes are unnecessary.

Pass condition:

- shaping does not imply maximal ambition by default.

### AC-OL-06 — Authority inheritance

Outcome Ladder never has greater authority than its grounding direction.

Pass condition:

- accepted grounding remains accepted-derived;
- provisional grounding produces a provisional ladder;
- ladder generation itself cannot accept a Target or authorize downstream work.

### AC-INT-01 — A → B integration

Project Survey and PL-V39-05-A clarification output can feed PL-V39-05-B without changing their authority roles.

Pass condition:

- Survey remains AS-IS evidence;
- Target remains accepted TO-BE authority where present.

### AC-INT-02 — Later-slice handoff

PL-V39-05-B outputs are consumable by later Adaptive Engagement / strategy shaping without implementing those systems now.

Pass condition:

- output includes explicit downstream hand-off semantics;
- no Adaptive Engagement policy is embedded.

## 16. Required test scenarios

Implementation must demonstrate at least these bounded scenarios:

### Scenario S1 — Accepted brownfield Target

A project has:

- accepted Target;
- stale Current State;
- historical conflicting residue;
- fresh Survey.

Expected:

- reuse accepted direction;
- recover only material provenance/conflict;
- no replacement Target;
- produce Outcome Ladder.

### Scenario S2 — No accepted Target, recoverable direction

A project has:

- Project Charter / prior accepted decisions;
- historical but coherent direction;
- no current accepted Target.

Expected:

- recover bounded `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`;
- provenance-label it;
- do not promote it to accepted Target authority;
- expose any unresolved boundary question;
- produce only a provisional ladder when direction is sufficiently determinate;
- require separate acceptance authority before the recovered candidate can become accepted TO-BE intent.

### Scenario S3 — Material unresolved conflict

A project has two live, materially different direction authorities.

Expected:

- conflict surfaced;
- no silent merge;
- ladder generation blocked if the conflict changes outcome meaning.

### Scenario S4 — History-heavy but irrelevant

A project has extensive historical material that does not materially affect current shaping.

Expected:

- bounded recovery stops early;
- history volume does not force history reading.

### Scenario S5 — Ladder anti-task test

Input direction can tempt implementation decomposition.

Expected:

- ladder outputs observable outcomes;
- tasks/components are rejected or rephrased as evidence-bearing outcomes.

## 17. Non-goals / deferrals

The following remain deferred beyond PL-V39-05-B:

- deciding how much shaping depth to apply dynamically;
- choosing among competing strategies;
- synthesizing final Target skeleton;
- compiling executable Target contract;
- full Roadmap synthesis;
- research workflow design;
- execution-plan generation.

## 18. Implementation constraints

Implementation SHOULD prefer:

- small managed templates/contracts;
- explicit trigger/bypass behavior;
- deterministic validation where practical;
- text-first artifacts;
- bounded evidence references;
- clear ownership separation.

Implementation MUST avoid:

- mandatory heavyweight archaeology;
- hidden inference of user intent;
- auto-rewrite cascades across Project Spine;
- coupling Brownfield Recovery to one specific repository layout;
- coupling Outcome Ladder to one fixed number of levels.

## 19. Field validation requirement

PL-V39-05-B is not considered fully closed by unit/template checks alone.

Before final closure, it MUST receive at least one bounded consumer field validation demonstrating:

- either safe accepted-direction bypass or real bounded recovery;
- Outcome Ladder generation;
- no unwanted Target/Gap/Roadmap churn;
- no silent authority promotion.

Poker MAY be reused only if it still exercises a meaningful scenario.

A second brownfield consumer is preferable if Poker would only repeat the already-proven bypass case.

## 20. Completion rule

PL-V39-05-B can be closed when:

1. implementation satisfies all applicable acceptance criteria;
2. required scenarios are covered;
3. managed update behavior is safe;
4. consumer Doctor remains healthy;
5. at least one meaningful field validation passes;
6. no material product defect remains unresolved;
7. deferred later-slice scope remains unimplemented.

## 21. Release boundary

Definition approval, implementation completion, and field-pilot PASS do not by themselves authorize:

- release;
- tag;
- push;
- public export;
- migration of internal R&D history.

Those remain separately governed decisions.
