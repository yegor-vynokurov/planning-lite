# Recommendation: Memory Efficiency and Procedural Learning for Planning Lite

**Suggested ID:** `REC-PL-MEMORY-EFFICIENCY`
**Status:** Draft / Private
**Scope:** Central Planning Lite repository
**Relationship:** Complements `REC-PL-LEARNING-LOOP`
**Implementation status:** Recommendation only. No framework files should be changed yet.
**Source inspiration:** This recommendation emerged from reviewing the `AIAnytime/memrust` project and comparing its memory architecture with Planning Lite.

---

## 1. Summary

Introduce a lightweight memory policy for Planning Lite focused on three outcomes:

1. useful self-learning;
2. token economy;
3. fewer failures and more accurate agent work.

The proposed model is:

```text
project events
→ preserved evidence
→ compact durable memory
→ selective retrieval
→ successful procedure candidate
→ reviewed framework learning
```

This is not a proposal to embed memrust into Planning Lite.

The useful ideas to adapt are:

- distinguish different roles of memory;
- keep active context separate from archived evidence;
- retrieve only the smallest authoritative context needed;
- explain why a historical artifact was selected;
- consolidate completed work into compact durable memory;
- learn successful procedures, not only facts;
- log outcomes and operator corrections, not only skill names;
- preserve privacy and provenance;
- let optional intelligence degrade safely;
- avoid vector databases, embeddings, daemons, and automatic self-modification until real scale requires them.

---

## 2. Why this recommendation exists

Planning Lite already stores:

```text
ACTIVE.md
context.md
progress.md
tasks.md
readiness.md
review.md
decisions
recommendations
completed changes
Git and test evidence
```

But the framework does not yet define a clear memory policy.

As a result, agents may:

- read too much historical material;
- treat all files as equally authoritative;
- confuse provisional notes with approved decisions;
- repeat completed investigation;
- let `context.md` grow like a diary;
- preserve useful procedures only as narrative;
- record that a skill was invoked without recording whether it worked.

The `memrust` project is relevant because it distinguishes:

- working memory;
- episodic memory;
- semantic memory;
- reflection memory;
- procedural memory;
- tool-call memory;

and combines this with selective retrieval, consolidation, visibility, and fail-soft fallbacks.

Planning Lite should adopt the concepts, not the implementation.

---

## 3. Goals

### 3.1. Reduce context cost

Agents should not read all completed changes, progress logs, or recommendations on every turn.

### 3.2. Increase accuracy

Approved decisions and lifecycle-valid specifications should outrank recent but provisional notes.

### 3.3. Improve continuation

A checkpoint should provide one compact current resume packet.

### 3.4. Capture repeatable procedures

Useful learning should include:

- trigger;
- preconditions;
- ordered steps;
- verification;
- failure modes;
- recovery.

### 3.5. Improve framework learning

Project experience should help decide whether the right destination is:

- workflow;
- template;
- deterministic check;
- operator guide;
- discipline;
- skill;
- no framework change.

### 3.6. Stay lightweight

The first implementation should use Markdown, stable IDs, existing lifecycle files, and optional CSV. No memory service is required.

---

## 4. Non-goals

This recommendation does not propose:

- adding memrust as a dependency;
- adding Rust services or MCP memory;
- vector search in every project;
- HNSW or embeddings;
- automatic prompt rewriting;
- deleting historical evidence;
- automatic skill creation;
- cross-project synchronization;
- background self-modification;
- replacing the Planning Lite lifecycle.

---

## 5. Memory roles

Planning Lite should explicitly distinguish six roles.

| Memory role | Meaning | Existing examples | Default reading policy |
|---|---|---|---|
| Working | Current resumable state | `ACTIVE.md`, active `context.md`, current task and gate | Read on every continuation |
| Episodic | What happened | `progress.md`, checkpoints, test runs, amendments | Read for audit, recovery, or relevant investigation |
| Semantic | Durable facts and approved state | `CURRENT_STATE.md`, decisions, project rules, domain language | Read during bootstrap, routing, planning, and affected work |
| Reflection | Evaluations and lessons | `review.md`, findings, learning candidates | Read during completion and learning review |
| Procedural | How to perform repeatable work | workflows, skills, disciplines, operator guide | Load only for the matching operation |
| Tool-call / skill outcome | What was invoked and how it ended | skill usage, retries, operator corrections | Aggregate at checkpoint or completion |

Core rule:

```text
Not all memory belongs in active context.
```

Completed episodic evidence remains on disk but leaves default startup context.

---

## 6. Authority-first retrieval

Recommended priority:

```text
1. Authority
2. Lifecycle validity
3. Explicit relation
4. Exact identifier or canonical term
5. Recency
6. Semantic resemblance
```

Typical authority:

| Artifact | Authority |
|---|---|
| Approved decision / ADR | Very high |
| Active approved specification | Very high |
| `ACTIVE.md` for current lifecycle state | Very high |
| Completion review | High |
| Readiness verdict | High for execution authorization |
| Current-state document | High |
| Progress note | Medium |
| Checkpoint summary | Medium |
| Agent reflection | Low until verified |
| Raw chat observation | Low |

A recent note saying “maybe JSON” must not override an approved decision defining JSON Schema v2.

Recency is useful only after authority and lifecycle validity.

---

## 7. Bounded context selection

At startup or continuation:

```text
1. Read AGENTS.md.
2. Read ACTIVE.md.
3. Read the active change index or relations.
4. Read stage-relevant files of the active change.
5. Select no more than 2-4 related completed changes.
6. Open progress, amendments, or logs only when needed.
```

Suggested reasons:

```text
authoritative
active
dependency
follow-up
superseded-history
decision-constraint
supporting-evidence
recovery-evidence
```

Optional short manifest:

```markdown
## Context selected

- `ACTIVE.md`
  Reason: authoritative current state.

- `CHG-0004/specification.md`
  Reason: active approved specification.

- `CHG-0002/review.md`
  Reason: `CHG-0004` is a follow-up of `CHG-0002`.

- `ADR-0003`
  Reason: constrains the persistence interface.
```

This should remain short and explainable.

---

## 8. Durable memory capsule

After closure:

```text
progress
+ checkpoints
+ amendments
+ verification evidence
+ final review
→ durable memory capsule
```

Suggested `review.md` section:

```markdown
## Durable memory capsule

- Outcome:
- Behavior now guaranteed:
- Decisions introduced or confirmed:
- Interfaces or invariants changed:
- Known limitations:
- Relevant successors or follow-ups:
- Evidence sources:
```

A compact variant may use 2-4 factual sentences.

Suggested compression prompt:

```text
Compress the completed change into durable project memory.

Write 2-4 factual sentences.

Preserve:
- change and decision IDs;
- versions and dates;
- accepted behavior;
- invariants;
- known limitations;
- follow-up obligations.

Remove:
- tool chatter;
- repeated task descriptions;
- abandoned intermediate ideas;
- transient debugging details.

Do not infer facts not supported by the completed change.
Output only the memory capsule.
```

The capsule does not replace evidence. It becomes the default entry point to that evidence.

---

## 9. Deterministic structure before LLM compression

Prefer:

```text
structured extraction
→ optional language compression
```

over:

```text
ask the model to decide what matters
```

The capsule should be assembled from known fields:

```text
change ID
completion verdict
accepted criteria
approved decisions
known limitations
follow-up IDs
test summary
```

The model may compress these fields into prose but should not discover or invent facts.

Principle:

```text
Use code or templates for structure.
Use the model for constrained synthesis.
```

---

## 10. Procedural learning candidates

Add a precise candidate type:

```text
Procedural candidate
```

Suggested structure:

```markdown
## Procedure candidate

- Trigger:
- Preconditions:
- Inputs:
- Steps:
- Verification:
- Failure modes:
- Recovery:
- Successful source changes:
- Failed or corrected attempts:
- Projects where observed:
- Suggested destination:
```

Example:

```text
Trigger:
A pristine Planning Lite project must be initialized.

Steps:
1. Classify each project-owned file.
2. Materialize Missing and Pristine files completely.
3. Merge Existing content.
4. Stop on Ambiguous.
5. Verify that only allowed planning files changed.

Verification:
No pristine markers remain.
No project-owned text was lost.
Program code is unchanged.
```

A validated procedure may become:

- a rule in an existing workflow;
- a template;
- a deterministic check;
- a discipline;
- an operator-guide recipe;
- a skill only when truly independent and reusable.

Skill creation remains the last resort.

---

## 11. Outcome-aware skill logging

Evolve from:

```text
Which skill was invoked?
```

toward:

```text
How did the invocation end?
```

Possible future schema:

```csv
timestamp_utc,skill,invocation,lifecycle_stage,change_id,result,retry,operator_correction
```

Suggested values:

```text
result:
success
partial
blocked
failed

retry:
0
1
2+

operator_correction:
no
routing
scope
format
lifecycle
technical
```

To reduce noise, record at:

- checkpoint;
- completion review;
- meaningful failure;
- operator correction;
- repeated retry.

Prompt-level telemetry is approximate. Exact telemetry would require a hook or wrapper and belongs to a later phase.

---

## 12. Explained recall

When historical information is used, the agent should know:

1. why it was retrieved;
2. how authoritative it is.

Example:

```text
Artifact:
CHG-0002 progress note

Retrieved because:
exact term match

Authority:
working hypothesis

Use:
supporting context only
```

Versus:

```text
Artifact:
ADR-0005

Retrieved because:
explicit informed-by relation

Authority:
approved decision

Use:
binding constraint
```

Principle:

```text
Similarity explains relevance.
Authority determines whether the memory may constrain action.
```

---

## 13. Two-stage retrieval

For larger projects:

### Stage 1: deterministic candidate selection

Use:

- stable IDs;
- relations;
- lifecycle stage;
- exact terms;
- index entries;
- recency as a secondary signal.

### Stage 2: optional model-assisted relevance pass

Only for 3-8 candidates.

Suggested prompt:

```text
Task:
[current task]

Candidate project artifacts:
[ID, title, one-line summary]

Classify each artifact:

- MUST_READ
- SUPPORTING
- SKIP

Use MUST_READ only when the artifact directly constrains
the current action, scope, interface, gate, or acceptance criteria.

Return JSON only.
```

Do not add a reranker until relation-based selection becomes insufficient in real projects.

---

## 14. Fail-soft behavior

Optional intelligence may degrade. Safety gates may not.

```text
Semantic retrieval unavailable
→ use IDs, relations, index, and text search

Learning classifier uncertain
→ Reusable lesson: None

Skill telemetry unavailable
→ continue the workflow

Capsule compression fails
→ preserve structured fields

Readiness evidence missing
→ prohibit execution

Completion evidence missing
→ prohibit closure
```

Principle:

```text
Optional intelligence may fall back.
Authorization and evidence gates must fail closed.
```

---

## 15. Visibility for cross-project learning

Suggested values:

```text
private
exportable
central
```

### Private

Contains sensitive or project-specific material.

### Exportable

Passed privacy review and may be copied manually into the central private inbox.

### Central

Reviewed in the Planning Lite repository and usable as evidence for a central recommendation or change.

Rule:

```text
A central synthesis may be published only when it does not require disclosure of any private source.
```

This extends `REC-PL-LEARNING-LOOP`.

---

## 16. Checkpoint as compact snapshot

A checkpoint should be a replaceable snapshot, not an accumulating diary.

Suggested fields:

```text
checkpoint ID
active change
lifecycle stage
stage status
last completed task
next permitted action
blockers
approved amendments
Git state
verification state
recommended next skill
```

Repeated checkpoint must not:

- duplicate completed tasks;
- duplicate blockers;
- advance lifecycle stage;
- invent a new next action;
- append repeated narrative;
- create competing resume packets.

---

## 17. Relationship to `REC-PL-LEARNING-LOOP`

The earlier recommendation proposes:

```text
change evidence
→ reusable-learning candidate
→ feedback packet
→ central review
→ central CHG
→ release
```

This recommendation adds:

```text
memory roles
authority-first retrieval
bounded context
durable capsules
procedural candidates
outcome-aware logging
visibility
compact checkpoints
fail-soft behavior
```

The two recommendations should remain separate during the pilot and may later be merged.

---

## 18. Proposed future framework changes

Candidates for a future central `CHG`:

1. Add memory-role policy to `STATE_OWNERSHIP.md`.
2. Add authority-first context selection to startup and resume workflows.
3. Add bounded related-change reading.
4. Add `Durable memory capsule` to `review.md`.
5. Add `Procedural candidate` to the feedback template.
6. Add visibility classification.
7. Extend skill logging with outcome and correction fields.
8. Make checkpoint resume state compact and idempotent.
9. Add fail-soft rules for optional memory features.
10. Keep evidence archived but outside default context.
11. Preserve provenance to source changes.
12. Measure prompt growth before accepting new runtime instructions.

---

## 19. Minimal rollout plan

### Phase 1: Private recommendation

Store this file in:

```text
.planning-lab/recommendations/active/
```

Do not change distributed templates.

### Phase 2: Manual pilot

Across poker, labeling, and mathematical-exercise projects:

- observe unnecessary historical reads;
- note authority mistakes;
- write 3-10 durable capsules manually;
- identify 2-5 procedural candidates;
- record skill failures and operator corrections;
- inspect checkpoint duplication.

### Phase 3: Cross-project synthesis

Compare:

- repeated retrieval failures;
- successful procedures;
- token-heavy continuation;
- ambiguous authority;
- recurring operator corrections.

### Phase 4: Bounded central change

Suggested first subset:

```text
memory roles
+ authority-first retrieval
+ durable memory capsule
+ compact checkpoint
```

Keep outcome telemetry and procedural promotion separate if needed.

### Phase 5: Evaluate

Compare before and after:

- files read to resume work;
- repeated investigation;
- operator corrections;
- lifecycle mistakes;
- context size;
- completion-review quality;
- failed or blocked execution attempts.

---

## 20. Evaluation questions

1. Does bounded selection reduce files read without losing necessary context?
2. Does authority-first retrieval prevent provisional notes from overriding decisions?
3. Are durable capsules accurate enough as the default entry point?
4. Can agents create capsules without unsupported claims?
5. Do compact checkpoints improve `/new` continuation?
6. Are procedural candidates more useful than generic lessons?
7. Does outcome-aware logging reveal routing or prompt weaknesses?
8. Does the added policy save more tokens than it adds?
9. Are relations and indexes sufficient without semantic search?
10. At what project size does deterministic retrieval stop being enough?

---

## 21. Risks and mitigations

### Memory taxonomy becomes bureaucracy

Keep roles conceptual. Do not create six new directory trees.

### Context selection omits history

Make active specification, decisions, relations, and lifecycle-valid artifacts mandatory.

### Capsule distorts the record

Build from structured fields, retain source IDs, preserve original evidence.

### Procedural candidates multiply

Use no-op by default and require repeated evidence.

### Logging adds noise

Aggregate only at checkpoint, correction, failure, or completion.

### Optional retrieval creates a new failure point

Keep deterministic selection canonical and model reranking optional.

### Private details leak centrally

Use visibility, privacy review, and manual export.

---

## 22. Acceptance criteria for a future implementation change

A central implementation change should not close unless:

1. memory roles map to existing files without unnecessary duplication;
2. startup and resume workflows specify bounded selection;
3. authority outranks recency;
4. historical context selection is explainable;
5. completed evidence remains stored;
6. durable capsules point to evidence;
7. capsule generation is constrained against inference;
8. checkpoint output is compact and repeatable;
9. checkpoint does not advance lifecycle stage;
10. procedural candidates include trigger, steps, verification, and failure modes;
11. visibility distinguishes private, exportable, and central;
12. optional intelligence fails softly;
13. approval and evidence gates fail closed;
14. no vector database or background service is introduced without separate evidence;
15. runtime prompt growth is measured;
16. central private learning material is not copied into installed projects;
17. existing lifecycle semantics remain intact.

---

## 23. Open decisions

Before implementation, decide:

1. whether the durable capsule belongs only in `review.md` or also in the change index;
2. whether context-selection reasons should be persisted or only reported;
3. whether skill outcome fields belong in the existing CSV;
4. whether checkpoints need stable IDs;
5. how many related completed changes may be opened by default;
6. whether procedural and semantic candidates share one feedback template;
7. whether authority is explicit metadata or inferred from artifact type;
8. whether capsule extraction needs a helper script;
9. which pilot metrics are practical;
10. whether this recommendation should later merge with `REC-PL-LEARNING-LOOP`.

---

## 24. Recommendation

Proceed with a manual pilot before changing Planning Lite.

Recommended immediate action:

```text
Store this recommendation privately.

Use three active projects as field tests.

Collect:
- unnecessary context reads;
- authority mistakes;
- continuation failures;
- useful durable capsules;
- successful repeatable procedures;
- skill retries and operator corrections.

Do not add embeddings, SQLite, or a new memory service.

After sufficient evidence:
→ compare both recommendations
→ merge overlapping concepts
→ create one bounded central CHG
→ implement through the normal Planning Lite lifecycle
```

The intended result is a Planning Lite that remembers less by default, retrieves better, and learns only from procedures that proved useful.

```text
preserve evidence
compress durable truth
retrieve selectively
explain retrieval
learn successful procedures
promote only through reviewed central changes
```
