# PL-V39-05-B — Implementation Start Contract

- Status: `READY FOR USER AUTHORIZATION / NOT AUTHORIZED`
- Date: `2026-08-28`
- Planning Lite revision: `c9deee6f24c3e4a4ab37ebb01ad80ba6d4b03c0e`
- Definition authority: `docs/design/project-spine/checkpoints/PL-V39-05-B-BROWNFIELD-RECOVERY-OUTCOME-LADDER-DEFINITION-v1.md`
- Definition SHA256: `05bb7ed1dba08111d60065f7a114b65d622470cb88aa83c7ca6cece7ac242758`
- Slice: `PL-V39-05-B`
- Subject: `Brownfield Recovery + Outcome Ladder`
- Implementation authorization: `NO`
- Change activation: `NO`
- Release/tag/push authorization: `NO`

## 1. Start gate

Implementation MAY begin only after explicit user authorization clearly referring to PL-V39-05-B implementation.

Definition review PASS does not authorize implementation.
This contract does not authorize implementation.

## 2. Authorized implementation scope after future approval

### Brownfield Recovery

Implementation may add only the bounded managed contracts/templates/validation needed to:

- bypass recovery when sufficient accepted direction already exists;
- recover only material direction/provenance when current direction is insufficient;
- emit `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`;
- distinguish accepted/current authority, historical residue, conflict, and unknown;
- enforce BR-STOP-01 through BR-STOP-04;
- surface unresolved material conflict without silently resolving it.

### Outcome Ladder

Implementation may add only the bounded managed contracts/templates/validation needed to:

- derive observable outcome levels from accepted or provisional recovered direction;
- preserve the grounding authority ceiling;
- distinguish outcomes from tasks/components/sequencing;
- identify a minimum useful stopping level;
- preserve material constraints/non-goals;
- provide later-slice handoff without implementing those later slices.

## 3. Explicit exclusions

Authorization for PL-V39-05-B does NOT include:

- Adaptive Engagement;
- Strategy Portfolio;
- Target Skeleton;
- Executable Target Contract;
- broad Roadmap synthesis;
- generic research workflow;
- execution/change orchestration;
- automatic Target acceptance;
- automatic Gap/Roadmap rewriting;
- release, tag, push, or public export.

## 4. Authority invariants

```text
accepted direction
→ remains accepted unless explicitly changed

recovered direction
→ RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL

recovery
→ cannot accept Target by itself

Outcome Ladder
→ inherits grounding authority ceiling

Outcome Ladder
→ cannot accept Target or authorize work
```

Any violation is blocking.

## 5. Trigger / bypass invariants

### Accepted direction

When a sufficient accepted direction exists:

`REUSE_CURRENT_ACCEPTED_DIRECTION`

must be available.

### Recoverable direction

When current accepted direction is insufficient but bounded prior direction is recoverable:

- recover only necessary evidence;
- preserve provenance;
- emit a provisional candidate;
- do not promote authority.

### Unresolved conflict

When material live authorities conflict and existing rules cannot order them:

- stop;
- expose conflict;
- route to clarification/user decision;
- do not manufacture a merged baseline.

## 6. Outcome Ladder invariants

Each ladder level must answer primarily:

> What observable project outcome is true at this level?

It must not primarily answer:

> What should we implement next?

Task lists, component decompositions, Roadmap sequences, and execution DoD are not valid ladder substitutes.

## 7. Required acceptance coverage

Implementation must demonstrate:

- `AC-BR-01` through `AC-BR-05`;
- `AC-OL-01` through `AC-OL-06`;
- `AC-INT-01` through `AC-INT-02`.

## 8. Required scenarios

Implementation must cover:

- `S1` accepted brownfield Target;
- `S2` no accepted Target, recoverable direction;
- `S3` unresolved material conflict;
- `S4` history-heavy but irrelevant;
- `S5` Outcome Ladder anti-task test.

## 9. Managed-surface constraint

Prefer:

- small managed templates/contracts;
- bounded validators;
- explicit trigger/bypass behavior;
- deterministic checks where practical.

Avoid:

- general-purpose archaeology;
- repository-wide history scans by default;
- second Target or second Roadmap authorities;
- hidden authority promotion;
- mandatory fixed ladder depth.

## 10. Consumer safety / field validation

Before slice closure:

- central Doctor must pass;
- managed update behavior must remain safe;
- at least one meaningful consumer field validation must pass;
- field validation must demonstrate Brownfield Recovery or safe accepted-direction bypass plus Outcome Ladder;
- no unwanted Target/Gap/Roadmap churn may occur;
- no silent authority promotion may occur.

A second brownfield consumer is preferable if Poker would only repeat the already-proven accepted-Target bypass case.

## 11. Completion boundary

Implementation completion is not slice closure.

Closure additionally requires:

1. all applicable acceptance criteria PASS;
2. required scenario coverage;
3. managed update safety;
4. consumer Doctor PASS;
5. meaningful field validation;
6. no unresolved material product defect;
7. deferred scope remains deferred.

## 12. Stop conditions

Stop and return for adjudication if implementation discovers a necessary dependency on:

- Adaptive Engagement;
- Strategy Portfolio;
- Target Skeleton;
- Executable Target Contract;
- material parent-Roadmap semantic rewrite;
- automatic Target acceptance;
- a material inconsistency in the Definition.

Do not expand scope silently.

## 13. Working-tree / commit boundary

This contract does not prescribe an automatic commit.

After separate user authorization:

- keep changes bounded to PL-V39-05-B;
- inspect exact file delta before any commit;
- no release/tag/push;
- no public export;
- no unrelated merge.

## 14. Authorization record

```text
Definition review:       PASS
Implementation contract: READY
User authorization:      NOT YET GIVEN
Implementation started:  NO
Release authorized:      NO
```

The next state transition requires explicit user authorization.
