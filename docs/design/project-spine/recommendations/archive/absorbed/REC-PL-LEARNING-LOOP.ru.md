# Recommendation: Evidence-Based Learning Loop for Planning Lite

**Suggested ID:** `REC-PL-LEARNING-LOOP`
**Status:** Draft / Private
**Scope:** Central Planning Lite repository only
**Target release:** Not assigned
**Implementation status:** Recommendation only. No framework files should be changed yet.

---

## 1. Summary

Introduce a small, evidence-based learning loop that allows Planning Lite to learn from real work across multiple projects without automatically rewriting itself, creating unnecessary skills, or adding a database to every installed repository.

The proposed loop is:

```text
real project work
→ change evidence
→ completion review
→ reusable-learning candidate
→ portable feedback packet
→ cross-project comparison
→ central change
→ Planning Lite release
```

The system should remain conservative:

- no feedback packet is created by default;
- no new skill is created merely because a request is frequent;
- no framework rule is changed directly from a project;
- every accepted framework improvement goes through an ordinary central `CHG`;
- every promoted rule retains provenance linking it to the feedback and changes that motivated it.

This recommendation combines two related goals:

1. make completed changes easier to navigate as a lightweight linked knowledge base;
2. create a safe route by which useful experience from poker, labeling, mathematical-exercise, and future projects can improve the central Planning Lite framework.

---

## 2. Problem

Planning Lite already records substantial evidence:

- proposal and specification;
- plan and tasks;
- readiness audit;
- progress and amendments;
- completion review;
- decisions and recommendations;
- checkpoints and project state.

However, the current model has several gaps.

### 2.1. Changes are mostly isolated records

A completed change explains what happened inside itself, but relationships between changes are weak or implicit.

It is difficult to answer questions such as:

- Which change introduced the behavior that a later change corrected?
- Which change depends on an earlier migration?
- Which work is a follow-up rather than a separate idea?
- Which decision informed several changes?
- Which change superseded an earlier approach?

### 2.2. Framework learning is mostly manual and conversational

Useful lessons already emerge during real work. Examples include:

- pristine bootstrap templates should be materialized in full rather than patched;
- a complete change scaffold should be created at Definition, while content matures by stage;
- readiness and closure need clearer operator language;
- some workflow terms improve agent routing and reduce ambiguous execution.

At present, these lessons can be lost in chat history unless the operator manually converts them into a central framework change.

### 2.3. Automatic self-improvement would be unsafe

A naive self-learning system could:

- treat one unusual incident as a universal rule;
- create too many narrow skills;
- duplicate existing instructions;
- increase runtime prompt size;
- preserve project-specific assumptions in the general framework;
- expose proprietary or private project details;
- silently change framework behavior without approval.

Therefore, Planning Lite should not be self-modifying. It should be **self-observing and evidence-guided**, with human-controlled promotion.

---

## 3. Goals

### 3.1. Linked change history

Provide lightweight, stable relationships between changes without introducing a graph database or RAG system.

### 3.2. Durable project learning

Allow completion reviews to record whether a change produced a reusable lesson for Planning Lite.

### 3.3. Portable cross-project feedback

Allow a project agent to prepare a small, privacy-checked feedback packet that the operator can manually copy into the central Planning Lite repository.

### 3.4. Conservative promotion

Require cross-project evidence, a clear behavioral benefit, and a normal central change before modifying the framework.

### 3.5. Provenance

Preserve the path:

```text
source project evidence
→ feedback packet
→ central recommendation or change
→ framework rule
→ release version
```

### 3.6. Low complexity

Use Markdown, stable identifiers, existing lifecycle workflows, and optional local files. Do not require SQLite, embeddings, background services, or automatic synchronization.

---

## 4. Non-goals

This recommendation does not propose:

- autonomous prompt rewriting;
- automatic creation of skills;
- sharing project repositories with each other;
- copying private project data into the central repository;
- a central server or telemetry service;
- SQLite in installed Planning Lite projects;
- embeddings or semantic search;
- reading every completed change on every agent turn;
- replacing the existing change lifecycle;
- bypassing human approval or central `CHG` review.

---

## 5. Proposed architecture

The architecture has three layers.

### Layer A: Project evidence

Each installed project continues to use normal Planning Lite artifacts:

```text
proposal
specification
plan
tasks
readiness
progress
amendments
review
decisions
recommendations
Git and test evidence
```

No new service is required.

### Layer B: Portable learning candidate

Only when a completion review finds a durable, transferable lesson, the project may create a portable feedback packet.

The packet contains:

- the observed friction;
- evidence references;
- the reusable lesson;
- the proposed destination;
- applicability and limitations;
- a privacy check;
- source framework version;
- anonymized source-project type.

The operator manually copies the packet to the central repository.

### Layer C: Central promotion

The central Planning Lite repository periodically reviews accumulated feedback.

A candidate may be:

```text
Rejected
Kept local
Deferred
Merged with another candidate
Superseded
Promoted to central CHG
```

Only `Promoted to central CHG` may lead to framework changes.

The central `CHG` then follows the ordinary lifecycle:

```text
Definition
→ Planning
→ Readiness
→ Execution
→ Verification
→ Closure
→ Release
```

---

## 6. Proposed framework changes

These are the changes to consider in a future central `CHG`. They are not authorized by this recommendation alone.

---

### 6.1. Add `Relations` to `proposal.md`

Each change proposal should contain a small typed-relations section.

Suggested structure:

```markdown
## Relations

- Depends on: `[]`
- Blocks: `[]`
- Follow-up of: `[]`
- Supersedes: `[]`
- Related changes: `[]`
- Informed by decisions: `[]`
- Source recommendations: `[]`
- Source feedback: `[]`
```

Use stable identifiers such as:

```text
CHG-0002
ADR-0004
REC-0012
FBK-2026-003
```

Do not use relative file paths as the primary identity, because a change moves from `active/` to `completed/`.

#### Meaning of relations

- **Depends on**: this change cannot be completed correctly without the referenced change or artifact.
- **Blocks**: the referenced work should not proceed until this change is complete.
- **Follow-up of**: this change continues or repairs earlier work but is not necessarily blocked by it.
- **Supersedes**: this change replaces the approach or result of an earlier change.
- **Related changes**: relevant context without a strict dependency.
- **Informed by decisions**: architectural or product decisions that constrain the change.
- **Source recommendations**: recommendations that led to this change.
- **Source feedback**: cross-project feedback packets that motivated a central framework change.

#### Design rule

Relations should remain few and meaningful. They are navigation aids and provenance, not a demand to link every document to every other document.

---

### 6.2. Add `.planning/changes/INDEX.md`

Introduce a lightweight navigation index for changes.

Suggested columns:

| Change | Title | Status | Location | Depends on | Follow-up of | Supersedes |
|---|---|---|---|---|---|---|

The index should:

- contain one row per change;
- use stable change IDs;
- point to the current active or completed location;
- summarize only high-value relations;
- be updated at change creation and closure;
- be treated as a navigation index, not the source of truth.

The source of truth remains:

- the actual change folder;
- the proposal relations;
- the lifecycle state recorded in canonical files.

A future `doctor` check may detect:

- missing index rows;
- duplicate change IDs;
- stale active/completed locations;
- references to unknown IDs.

#### Expected benefit

The agent can first inspect `INDEX.md`, then selectively open only relevant completed changes.

This provides a lightweight wiki-like navigation model:

```text
stable IDs
→ typed relations
→ compact index
→ selective reading
→ evidence drill-down
```

---

### 6.3. Add `Planning-system learning` to `review.md`

The completion review should explicitly decide whether the change produced a reusable lesson for Planning Lite.

Suggested section:

```markdown
## Planning-system learning

- Reusable lesson: `None | Candidate`
- Observed friction:
- Likely cause:
- Workaround used:
- Proposed reusable rule:
- Applicable scope:
- Evidence:
- Suggested destination:
- Privacy concerns:
```

The default must be:

```text
Reusable lesson: None
```

A completion review is not incomplete merely because it produced no framework lesson.

#### Suggested destinations

```text
No framework change
Project instructions
Existing workflow
Template
Operator guide
Discipline
Skill
Doctor or static check
Central recommendation
```

This destination list prevents the reflex of turning every repeated behavior into a new skill.

---

### 6.4. Add `Workflow experience` to `review.md`

Suggested section:

```markdown
## Workflow experience

- Skills invoked:
- Unexpected retries:
- Manual corrections by operator:
- Confusing lifecycle or approval point:
- Missing capability:
- Instructions that were ignored or ambiguous:
- Useful instruction that should be reused:
```

This section should record only material observations.

It should not become a transcript of the session.

#### Relationship to skill statistics

If `SKILL_USAGE.csv` is enabled, it provides approximate frequency data.

`Workflow experience` provides qualitative evidence:

- whether the skill worked;
- whether the operator corrected it;
- where the lifecycle was confusing;
- whether an instruction caused retries.

Frequency alone must not trigger a new skill.

---

### 6.5. Add an optional `feedback/TEMPLATE.md`

A future installed-project template may include an optional feedback packet template, but the directory should remain empty unless a durable lesson exists.

Suggested packet:

```markdown
# FBK-YYYY-NNN: Short title

- Source framework version:
- Source project type:
- Source changes:
- Category:
- Status: Candidate
- Scope:
- Confidence:
- Recurrence observed:

## Observed friction

## Evidence

## Proposed reusable lesson

## Applicability

## Known limits

## Suggested destination

## Existing rule comparison

## No-op test

What observable agent behavior would change if this proposal were adopted?

## Privacy check

- [ ] No secrets
- [ ] No proprietary code
- [ ] No personal data
- [ ] No project-specific implementation details required
```

#### Packet creation rule

The agent may create a packet only when explicitly asked by the operator or when the completion workflow authorizes it after finding a genuine candidate.

The agent must not create a packet merely to make the review appear productive.

---

### 6.6. Add `LEARNING_PROMOTION.md` as a central-only workflow

`LEARNING_PROMOTION.md` should not be part of the installed project template.

It belongs to the central framework-maintenance layer.

Its job:

1. inspect feedback packets in the central inbox;
2. group duplicates and contradictions;
3. compare candidates with current workflows, skills, disciplines, templates, and checks;
4. evaluate evidence and transferability;
5. apply the no-op test;
6. recommend Reject, Keep local, Defer, Merge, Supersede, or Promote;
7. create no framework change directly;
8. propose a bounded central `CHG` for accepted improvements.

This workflow should be rarely loaded and invoked through an existing audit or maintainer process. A new public runtime skill is not required initially.

---

### 6.7. Require a no-op default

The learning loop should be biased toward doing nothing.

A feedback candidate should not be created unless the lesson is:

- durable;
- evidenced;
- transferable;
- behavior-changing;
- not already covered;
- placed in the correct artifact type.

The review should ask:

```text
Does this repeat?
Is it supported by evidence?
Would it apply outside this one project?
Would adopting it change observable agent behavior?
Is it better than the current rule?
Is a prompt rule the right solution?
Could a test, template, doctor check, or project rule solve it better?
```

If the answer is weak, record:

```text
Reusable lesson: None
```

and stop.

---

### 6.8. Promote framework changes only through a central `CHG`

No project feedback packet may directly edit:

- central prompts;
- lifecycle rules;
- templates;
- skills;
- disciplines;
- router behavior;
- doctor checks.

The only permitted path is:

```text
feedback candidate
→ central review
→ accepted recommendation
→ central CHG
→ ordinary approval gates
→ release
```

This ensures that Planning Lite uses its own lifecycle to improve itself.

---

### 6.9. Preserve provenance for every promoted rule

Every central framework change based on project feedback should record:

```text
Source feedback IDs
Source change IDs
Anonymized source project types
Central recommendation ID
Central change ID
Framework version introduced
Rules or files changed
Supersedes
Superseded by
Framework version retired, if applicable
```

Minimum implementation:

- include `Source feedback` in the central proposal relations;
- preserve those references in the completed central change;
- include the resulting release version in closure or release notes.

A richer provenance index may be added later if the number of promoted rules becomes large.

#### Provenance principle

A future maintainer should be able to answer:

```text
Why does this rule exist?
Which real failures or frictions motivated it?
Which framework version introduced it?
What earlier rule did it replace?
```

---

## 7. Private placement in the central repository

Raw recommendations and incoming feedback should not be stored inside:

```text
template/.planning/
```

Anything under that path risks being shipped into installed projects.

They also should not initially be committed to GitHub.

### Recommended local-only layout

At the root of the central Planning Lite working tree:

```text
planning-lite/
├── template/
│   └── .planning/               # shipped framework template
├── maintainer/                  # possible future tracked central-only workflows
│   └── LEARNING_PROMOTION.md
└── .planning-lab/               # local-only and ignored
    ├── recommendations/
    │   ├── inbox/
    │   ├── active/
    │   └── archived/
    ├── feedback/
    │   ├── inbox/
    │   ├── reviewed/
    │   └── promoted/
    └── synthesis/
```

### Purpose of `.planning-lab/`

`.planning-lab/` is:

- central-repository local workspace;
- private;
- not part of the shipped template;
- not part of the public repository;
- suitable for raw recommendations, copied feedback packets, and unfinished synthesis.

### How to ignore it

Preferred initial option:

```text
.git/info/exclude
```

Add:

```text
/.planning-lab/
```

Advantages:

- no raw files are committed;
- GitHub does not receive them;
- the public `.gitignore` does not even need to advertise the local workspace;
- installed projects cannot receive them through template copying.

Limitation:

- `.git/info/exclude` is local to one clone.

For use across several machines, use a global Git excludes file. A committed `.gitignore` entry may be considered later if consistent team-wide behavior becomes more important than keeping the workspace invisible.

---

## 8. Central-only tracked material

Not everything related to learning must remain private forever.

A future implementation may distinguish:

### Private and untracked

```text
.planning-lab/recommendations/
.planning-lab/feedback/
.planning-lab/synthesis/
```

These contain raw observations, uncertain ideas, and project-derived material.

### Central-only but potentially tracked

```text
maintainer/LEARNING_PROMOTION.md
maintainer/feedback-schema.md
maintainer/prompt-quality-checklist.md
```

These are mature maintainer procedures. They should live outside `template/`, so they are not copied to installed projects.

### Shipped to projects only after approval

Examples:

```text
proposal.md Relations section
changes/INDEX.md template
review.md learning sections
optional feedback/TEMPLATE.md
```

These enter `template/.planning/` only through a normal central change and release.

---

## 9. Promotion criteria

A candidate should normally be promoted only when at least one of the following is true:

1. the same friction appears in two or more independent projects;
2. one incident reveals a severe safety, data-loss, or lifecycle failure;
3. an operator repeatedly needs the same correction across sessions;
4. a missing deterministic check causes recurring ambiguity;
5. a new term or workflow measurably reduces repeated explanation and misrouting.

A candidate should not be promoted when:

- it reflects one project's domain;
- it is merely frequent;
- it duplicates an existing rule;
- the proposed instruction would not change behavior;
- the real solution is a test or static check;
- it increases prompt size more than it reduces ambiguity;
- evidence depends on private project details that cannot be generalized safely.

---

## 10. Destination decision table

| Observation | Preferred destination |
|---|---|
| One project-specific convention | Project instructions |
| One short reusable rule | Existing workflow |
| Repeated operator confusion | Operator guide or router wording |
| Repeated document shape | Template |
| Stable engineering vocabulary | Discipline or glossary |
| Deterministic invariant | Doctor or test |
| Repeated multi-step reasoning procedure | Skill |
| Uncertain but promising idea | Central recommendation |
| Duplicate or weak signal | No framework change |

### Skill creation rule

A new skill is justified only when:

- it has a clear trigger;
- it performs a repeatable multi-step procedure;
- it has an observable completion criterion;
- it is useful across projects;
- it cannot be expressed compactly in an existing workflow;
- it is not better implemented as deterministic code;
- its saved effort exceeds its context and routing cost.

---

## 11. Suggested operator prompts

### 11.1. Project-level learning reflection

```text
$planning-audit

Review the completed change for Planning Lite learning.

Do not invent a reusable lesson.

Check:
- unexpected retries;
- operator corrections;
- ambiguous lifecycle or approval points;
- missing instructions;
- repeated manual analysis;
- workarounds that may generalize.

Return:
- Reusable lesson: None or Candidate;
- evidence;
- likely scope;
- best destination;
- no-op test.

Do not change framework files.
Do not create a feedback packet unless I approve the candidate.
```

### 11.2. Prepare a portable feedback packet

```text
Prepare one privacy-safe Planning Lite feedback packet
for the approved reusable-learning candidate.

Use stable IDs for source changes.
Do not include proprietary code, secrets, personal data,
or implementation details unnecessary to understand the lesson.

Write only the feedback packet.
Do not modify project workflows or framework files.
```

### 11.3. Central cross-project review

```text
$planning-audit

Review feedback packets in the central private inbox.

For each candidate:
- verify evidence;
- find duplicates and contradictions;
- compare with current framework rules;
- determine the correct destination;
- apply the no-op test;
- assess prompt-size cost;
- recommend Reject, Keep local, Defer, Merge,
  Supersede, or Promote.

Do not modify Planning Lite.
For Promote candidates, propose one bounded central CHG.
```

---

## 12. Phased rollout

### Phase 1: Private recommendation only

- Store this recommendation in `.planning-lab/recommendations/active/`.
- Add no shipped files.
- Collect examples from the poker, labeling, and mathematical-exercise projects.
- Manually create feedback packets only for strong candidates.

### Phase 2: Central pilot

- Add a private feedback inbox.
- Run one cross-project synthesis.
- Decide whether relations and review learning sections remain minimal enough.
- Draft one central `CHG`.

### Phase 3: Minimal framework release

A future release may include:

- `Relations` in `proposal.md`;
- `.planning/changes/INDEX.md`;
- learning sections in `review.md`;
- optional feedback template;
- updated closure and doctor rules.

### Phase 4: Maintainer workflow

- Add central-only `maintainer/LEARNING_PROMOTION.md`.
- Keep it outside the shipped template.
- Add provenance conventions.

### Phase 5: Optional derived tooling

Only if evidence volume justifies it:

- static index generation;
- doctor checks for relations;
- feedback deduplication;
- derived SQLite or FTS index in the central repository.

Markdown remains the source of truth.

---

## 13. Risks and mitigations

### Risk: prompt and skill proliferation

**Mitigation:** no-op default, destination decision table, skill as last resort.

### Risk: project-specific rules becoming global

**Mitigation:** require transferability and cross-project evidence.

### Risk: private information leaks

**Mitigation:** manual export, privacy checklist, anonymized source-project type.

### Risk: index drift

**Mitigation:** treat proposals as source of truth and add future doctor checks.

### Risk: agents create feedback for every change

**Mitigation:** `Reusable lesson: None` is the expected default.

### Risk: framework silently changes itself

**Mitigation:** central `CHG` is mandatory for every promoted change.

### Risk: learning files are copied into user projects

**Mitigation:** keep raw material in root `.planning-lab/`, never under `template/`.

### Risk: raw plans appear on GitHub

**Mitigation:** exclude `.planning-lab/` through `.git/info/exclude` or a global excludes file.

---

## 14. Acceptance criteria for a future implementation change

A central implementation `CHG` based on this recommendation should not be considered complete unless:

1. change relations use stable IDs;
2. `changes/INDEX.md` distinguishes navigation from source of truth;
3. creation and closure workflows define when the index is updated;
4. `review.md` supports `Reusable lesson: None`;
5. feedback packets are optional and privacy-checked;
6. no workflow creates a feedback packet automatically by default;
7. learning promotion cannot directly modify framework files;
8. promoted changes require a central `CHG`;
9. provenance from feedback to release is preserved;
10. central-only maintainer material is outside `template/`;
11. raw recommendations and feedback are not included in distributed archives;
12. runtime prompt growth is measured and justified;
13. no new public skill is added without satisfying the skill creation rule;
14. existing lifecycle and approval gates remain intact;
15. tests verify that project template installation does not copy central private material.

---

## 15. Open decisions

Before implementation, the central change should decide:

1. exact stable ID format for feedback packets;
2. whether `changes/INDEX.md` is manually maintained or deterministically generated;
3. whether `feedback/TEMPLATE.md` ships to every project or is created only on demand;
4. whether accepted provenance is stored only in completed central changes or also in a dedicated index;
5. whether `LEARNING_PROMOTION.md` should be tracked under `maintainer/` or remain private during the pilot;
6. whether skill usage logging should be referenced in review but remain disabled by default;
7. minimum evidence threshold for promotion after the pilot.

---

## 16. Recommendation

Proceed with a private pilot before changing the distributed framework.

Recommended immediate action:

```text
Create:
.planning-lab/recommendations/active/

Store this recommendation there.
Exclude .planning-lab/ locally.
Collect 3-10 high-quality feedback candidates
from independent projects.

Do not implement shipped template changes yet.
```

After sufficient evidence:

```text
run cross-project synthesis
→ refine this recommendation
→ create one bounded central CHG
→ implement through the normal Planning Lite lifecycle
```

The intended result is not an automatically self-editing framework.

It is a framework that can explain:

```text
what happened
what was learned
why the lesson is reusable
where the rule belongs
which evidence justified it
which release introduced it
```

That is a safer and more useful form of self-improvement.
