# REC-PL-CONTEXT-HANDOFF-001 v1 — Governed stage-context handoff, externalized working state, and bounded context inheritance

**Status:** `PROVISIONAL / FIELD-DERIVED / RESEARCH-CORROBORATED / OPEN`
**Date:** `2026-08-20`
**Source:** `PILOT-PL-DIRECTION-002`, Poker `CHG-0009-bayesian-study-harness`, and external review of long-horizon agent context-management practice
**Visibility:** `ACTIVE_DIRECTION` for Planning Lite `PL-V38-05`, `PL-V38-06B`, and `PL-V38-07` design
**Implementation authority:** none; this recommendation records field evidence, external prior art, design constraints, and an eval hypothesis
**Related Planning Lite material:** `REC-PL-DIRECTION-001-v2`, `REC-PL-DIRECTION-002-v1`, `REC-PL-READINESS-001-v1`, legacy `REC-PL-MEMORY-EFFICIENCY.ru.md`

---

## 1. Field observation

During real Poker work, Planning Lite stages such as Planning and Readiness can legitimately require substantial investigation:

```text
inspect governing artifacts
→ inspect code / tests / native seams
→ compare current semantics
→ form and reject hypotheses
→ verify dependencies
→ test whether a planned step is executable
→ revise the plan or emit a gate verdict
```

The problem is not that an agent spends many tool calls or substantial inference effort inside a hard task.

The problem appears when the resulting **observable working trace** is inherited wholesale by the next stage:

```text
necessary stage-local investigation
        ↓
large message/tool/event history
        ↓
next governed stage receives the same history by default
        ↓
higher token cost + latency
        ↓
attention dilution
        ↓
rejected/stale hypotheses compete with current authoritative state
```

This creates a distinction that Planning Lite should make explicit:

```text
required inference work
!=
required downstream context
```

and:

```text
durable trace
!=
active model input
```

Reasoning depth and context inheritance are independent controls.

### Important scope note

Planning Lite does **not** need access to, store, reconstruct, or govern private hidden chain-of-thought.

This recommendation concerns only context the harness can actually observe and control, for example:

- user and agent-visible messages;
- tool calls and tool outputs;
- files read or written;
- explicit scratch notes;
- event logs;
- generated summaries;
- Planning Lite artifacts;
- receipts, hashes, tests, and verification evidence.

---

## 2. External review: the pattern is broader than Anthropic

The field hypothesis is strongly corroborated by independent systems and recent research.

The implementations differ, but several of them converge on the same architectural separation:

```text
broader durable state / history
        ↓
selection, condensation, retrieval, or handoff policy
        ↓
smaller model-visible context
```

### 2.1 OpenAI Agents SDK — stored history and next-agent input are separable

OpenAI Agents SDK handoffs normally expose prior conversation history to the receiving agent, but the SDK supports:

- `input_filter` to alter what the receiving agent sees;
- `input_items` to forward filtered model input while leaving generated items intact for session history;
- `RunConfig.nest_handoff_history` to compact summarizable history;
- `handoff_history_mapper` to construct the exact input list for the next agent;
- common filters such as removing tool calls/results from handoff history;
- `call_model_input_filter` for last-mile shaping of the prepared model input.

This is a direct precedent for:

```text
what is retained for session/audit
!=
what the next model call must receive
```

Relevant sources:

- https://openai.github.io/openai-agents-python/handoffs/
- https://openai.github.io/openai-agents-python/running_agents/
- https://openai.github.io/openai-agents-python/ref/extensions/handoff_filters/

### 2.2 Microsoft AutoGen — model context is a bounded view over broader state/memory

AutoGen separates:

- broader agent state/history;
- `model_context`, which can be unbounded, message-buffered, or token-limited;
- a `Memory` protocol that can store information separately and inject selected material into model context when needed.

Relevant mechanisms include `BufferedChatCompletionContext`, `TokenLimitedChatCompletionContext`, `Memory.query`, and `Memory.update_context`.

This independently supports the principle that active model context is a **view**, not the whole durable state.

Relevant sources:

- https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html
- https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html
- https://microsoft.github.io/autogen/stable/reference/python/autogen_core.model_context.html

### 2.3 LangChain / LangGraph — trim, summarize, checkpoint, and custom-filter context

LangChain/LangGraph explicitly treats long conversation history as something that may need trimming before model calls, summarization, checkpointing, or custom filtering.

This is less specific than a governed Planning Lite stage handoff, but it confirms that message history and the context passed to a model are intentionally separable surfaces.

Relevant source:

- https://docs.langchain.com/oss/python/langchain/short-term-memory

### 2.4 OpenHands — persistent event history, condensed LLM view

OpenHands' Context Condenser is especially relevant because it separates the underlying event stream from the view used for reasoning.

The condenser architecture can:

- detect when context should be reduced;
- preserve selected head/tail events;
- summarize older/middle events;
- emit a `Condensation` event;
- construct a smaller `View` for the next model step while retaining history semantics.

OpenHands reports, on its tested SWE-bench Verified subset, that condensation reduced per-turn API cost to less than half once active while solving 54% versus 53% for the baseline. This is vendor-reported evidence on a subset, not a universal result, but it demonstrates the right kind of evaluation: **quality and efficiency must be measured together**.

Relevant sources:

- https://docs.openhands.dev/sdk/guides/context-condenser
- https://docs.openhands.dev/sdk/arch/condenser
- https://www.openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents

### 2.5 Manus — filesystem as externalized, restorable context

Manus describes a related but stronger production pattern:

- long observations are moved out of active context;
- the filesystem acts as persistent external context;
- compression is designed to be restorable;
- a web page can leave active context if its URL remains;
- a document can leave active context if its path remains;
- `todo.md` is repeatedly updated to keep current objectives near the model's active attention.

This supports two Planning Lite ideas:

```text
compression should preserve a recovery path
```

and:

```text
current objectives/state deserve a small recent anchor
```

Manus also argues that irreversible compression is risky because it is difficult to predict which earlier observation will matter later.

Relevant source:

- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

### 2.6 MemGPT / Letta — virtual context and progressive disclosure

MemGPT introduced an operating-system-inspired model of virtual context management: move information between memory tiers rather than require all useful state to remain in the LLM context window.

Letta's 2026 Context Repositories move this idea toward ordinary software-engineering primitives:

- context copied to a local filesystem;
- Git-backed versioning;
- progressive disclosure;
- file-tree/navigation cues kept visible;
- full files loaded only when needed;
- subagents can work on isolated memory branches and merge them.

Planning Lite should not copy Letta's self-editing memory architecture wholesale, but the relevant lesson is strong:

```text
externalized, versioned, progressively disclosed state
can be easier to govern than a monolithic transcript
```

Relevant sources:

- MemGPT: https://arxiv.org/abs/2310.08560
- Letta Context Repositories: https://www.letta.com/blog/context-repositories/

### 2.7 MAGE (2026 preprint) — memory as execution-state management

`Beyond Semantic Organization: Memory as Execution State Management for Long-Horizon Agents` is unusually close to the Planning Lite problem.

The paper argues that semantic-similarity retrieval can be a poor fit for long-horizon execution because it may fragment decision trajectories, mix valid and erroneous traces, and make coherent execution-state reconstruction harder.

MAGE instead uses a hierarchical execution-state tree. Active state is derived from the current root-to-node path, with operations to grow new traces, compress completed subgoals, validate summaries, and revise from a prior boundary while isolating flawed branches.

The authors report on MemoryArena a 55.1% token reduction and 7.8–20.4 percentage-point task-success improvement over their baselines. This is a recent arXiv preprint and should be treated as promising research evidence, not settled fact.

Its strongest Planning Lite implication is conceptual:

```text
execution state should be reconstructed from valid state lineage,
not from a bag of semantically similar historical fragments
```

Relevant source:

- https://arxiv.org/abs/2606.06090

### 2.8 Recent systems work — memory is a lifecycle, not only retrieval

Two 2026 reports further reinforce the systems framing.

`Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads` profiles ten representative memory systems and separates costs of memory construction, retrieval, and generation. This supports measuring the entire context-management lifecycle rather than token count alone.

Oracle's `Agent Memory as an Enterprise Memory Substrate for Long-Horizon AI Agents` describes a lifecycle spanning ingestion, extraction, consolidation, retrieval, summarization, revision/removal and separates an active memory core from a passive store. It reports about 10.7x fewer tokens than flat-history baselines in its evaluation. As a vendor technical report, this should be treated as corroborating rather than independent benchmark authority.

Relevant sources:

- https://arxiv.org/abs/2606.06448
- https://arxiv.org/abs/2607.13157

---

## 3. Synthesis: the useful common pattern

The reviewed systems do **not** converge on one universal compressor.

They converge on a more general architecture:

```text
FULL / DURABLE STATE
    may be large
    may be replayable
    may contain history and evidence
            ↓
CONTEXT POLICY
    select
    filter
    condense
    externalize
    retrieve
    validate
            ↓
ACTIVE MODEL VIEW
    bounded
    task/stage specific
    recent enough for attention
```

Planning Lite already has several compatible ideas:

- archive means "not injected", not "forgotten";
- visibility decay rather than information decay;
- multi-resolution memory;
- lineage-first retrieval;
- future AgentWorkPacket / Context Compiler;
- compact resumable `PL-V38-CURRENT.md`;
- stage-specific context policy planned in `PL-V38-05`.

The new field evidence sharpens these into a narrower missing contract:

> **A governed stage transition should control context inheritance explicitly.**

---

## 4. Recommendation

Planning Lite should introduce and evaluate a **Governed Stage Context Handoff** pattern.

The model should distinguish three information planes.

### Plane A — WORKSPACE / SCRATCH

Purpose:

- temporary hypotheses;
- intermediate calculations;
- exploratory searches;
- rejected approaches;
- verbose tool observations;
- stage-local notes.

Properties:

```text
large is acceptable
not authoritative by default
may be mutable
may be disposable
not inherited by the next stage by default
```

A scratch item that becomes materially relevant must be promoted into durable evidence or an authoritative artifact before the stage closes.

### Plane B — DURABLE EVIDENCE / TRACE

Purpose:

- exact verification results;
- test receipts;
- command outputs that justify a decision;
- hashes and source identities;
- audit findings;
- stable artifacts;
- materially relevant rejected alternatives where they explain a decision or protect against regression.

Properties:

```text
durable
retrievable
citeable
identity/provenance aware
not injected wholesale by default
```

### Plane C — STAGE HANDOFF STATE

Purpose:

Provide the next governed stage with the **minimum current state required to continue correctly**.

Candidate fields:

```yaml
handoff_version: 1

change_id: CHG-...
from_stage: Planning
to_stage: Readiness

stage_result:
  status: approved

authoritative_artifacts:
  - specification.md
  - plan.md
  - tasks.md
  - requirements-checklist.md

decisions:
  - id: ...
    assertion: ...

invariants:
  - ...

blockers: []
open_questions: []

evidence_refs:
  - id: ...
    path_or_receipt: ...
    identity: ...

next_gate:
  workflow: READINESS
  authorization_required: true

context_transport:
  raw_prior_transcript: not_injected_by_default
  evidence_retrieval: allowed_on_demand
```

This is a **candidate semantic shape**, not authorization to add a new Python domain model or mandatory YAML artifact.

The smallest implementation may be a structured Markdown/receipt section and ContextTrace rules.

---

## 5. Recommended semantic units

| Unit | Recommendation | State | Intended destination |
|---|---|---|---|
| `REC-PL-CONTEXT-HANDOFF-001/U1` | Treat **durable history, active model context, and authoritative project state as separate surfaces**. A message/tool trace can remain stored without being inherited by every later stage. | `FIELD_CONFIRMED / RESEARCH_CORROBORATED` | `PL-V38-05` context policy |
| `REC-PL-CONTEXT-HANDOFF-001/U2` | Separate **workspace/scratch**, **durable evidence**, and **stage handoff state**. Scratch is not authority; evidence is durable but normally retrieval-on-demand; handoff is the compact current-state carrier. | `STRONG CANDIDATE` | `PL-V38-05`, later Context Compiler |
| `REC-PL-CONTEXT-HANDOFF-001/U3` | At a material lifecycle boundary, prefer **fresh-context bootstrap from governed handoff + authoritative artifacts** over wholesale prior-transcript inheritance, but only after eval proves no correctness regression. | `TO TEST` | `PL-V38-06B` / `PL-V38-07` |
| `REC-PL-CONTEXT-HANDOFF-001/U4` | A handoff should carry bounded semantics: stage result, authoritative artifacts, current decisions/invariants, blockers/open questions, evidence references, source identities, and exact next gate. It should not carry redundant tool chatter or require hidden chain-of-thought. | `STRONG CANDIDATE` | workflow contract / ContextTrace |
| `REC-PL-CONTEXT-HANDOFF-001/U5` | Context removal should be **recoverable when the omitted material can still matter**. Prefer path/ID/hash/receipt-backed externalization over irreversible summarization for authoritative evidence. | `RESEARCH_CORROBORATED / TO CALIBRATE` | `PL-V38-05`, evidence policy |
| `REC-PL-CONTEXT-HANDOFF-001/U6` | Generic LLM summarization must not become a truth owner. Handoff assertions must be derived from or validated against **authoritative owners/current receipts**. If a summary conflicts with an owner, the owner wins or the transition fails closed. | `FIELD-ALIGNED / STRONG CANDIDATE` | ties to `REC-PL-DIRECTION-002` |
| `REC-PL-CONTEXT-HANDOFF-001/U7` | Preserve rejected/invalid branches as retrievable history when useful, but do not let them compete with the current valid execution path after a stage boundary. **Evidence retention and active-path visibility are separate controls.** | `STRONG CANDIDATE` | ContextTrace / visibility policy |
| `REC-PL-CONTEXT-HANDOFF-001/U8` | Prefer **owner/lineage/exact-reference retrieval first** and semantic retrieval second when reconstructing execution state. Semantic similarity alone may mix stale, rejected, or unrelated branches. | `RESEARCH_CORROBORATED / EXISTING-DIRECTION-ALIGNED` | `PL-V38-05` and `PL-V38-07` |
| `REC-PL-CONTEXT-HANDOFF-001/U9` | Measure stage-boundary context as an engineering surface: input tokens, peak active context, handoff size, evidence retrievals, files reopened, latency, cost where available, and operator corrections. Token reduction alone is not a success criterion. | `STRONG CANDIDATE` | `PL-V38-06B` / eval harness |
| `REC-PL-CONTEXT-HANDOFF-001/U10` | Evaluate **correctness and context efficiency jointly**. Promotion requires no material regression in semantic correctness, authorization correctness, blocker detection, safe deferral, and provenance before token/cost savings count as a win. | `STRONG CANDIDATE` | `PL-V38-06B` / `PL-V38-07` |
| `REC-PL-CONTEXT-HANDOFF-001/U11` | Provider/framework features such as OpenAI handoff filters, AutoGen bounded contexts, or OpenHands condensers should be treated as **adapters**, not Planning Lite semantics. Planning Lite's handoff contract must remain provider-agnostic. | `ARCHITECTURAL GUARD` | `PL-V38-07/08` |
| `REC-PL-CONTEXT-HANDOFF-001/U12` | Do not create a new feature stage, vector database, graph database, parallel workflow engine, or general multi-agent memory layer solely for this finding. First test the smallest stage-handoff/context-policy change on existing fixtures. | `ANTI-OVERREACH` | Roadmap governance |

---

## 6. Important reconciliation: keep useful failures, isolate stale failures

The external evidence contains an apparent tension.

Manus reports that keeping recent wrong turns visible can help an agent avoid repeating them **inside an ongoing run**.

MAGE argues that flawed branches should be isolated from the active execution path when reconstructing state.

These are compatible if Planning Lite distinguishes time scale.

### Intra-stage

Recent failure evidence may remain active when it helps immediate recovery:

```text
attempt failed
→ error remains visible
→ agent corrects course
```

### Inter-stage

Once the stage has adjudicated that branch and produced a current decision:

```text
failed/rejected branch
→ durable evidence/history
→ excluded from default next-stage context
→ retrievable if a later question explicitly needs it
```

Therefore the proposed rule is not `delete mistakes`.

It is:

```text
retain evidence
but sanitize the active state view at governed boundaries
```

---

## 7. Interaction with existing Planning Lite architecture

This recommendation should **refine**, not duplicate, existing context/memory work.

### Existing Project Spine direction already establishes

```text
archive != forgotten
visibility decay != information decay
L3/L2 default, L1/L0 on demand
deterministic lineage retrieval first
semantic retrieval second
future AgentWorkPacket
```

`REC-PL-CONTEXT-HANDOFF-001` adds a narrower field-derived question:

```text
what exactly crosses a lifecycle-stage boundary?
```

### Existing `PL-V38-05`

Current roadmap intent already includes stage-specific context depth profiles, least-privilege targeted context, safe insufficient-context deferral, ContextTrace, and visibility tiers.

Recommended refinement:

```text
PL-V38-05
+ explicitly distinguish durable trace from model-visible stage context
+ define stage-boundary handoff semantics
+ record what was inherited, omitted, and retrieved
```

Do not turn `PL-V38-05` into a full Context Compiler.

### Existing `PL-V38-06B`

Add controlled-realistic fixtures for:

1. `Planning → Readiness` fresh-context handoff;
2. `Readiness → Execution` handoff with authorization boundary;
3. stale/rejected hypothesis present in durable history but absent from active handoff;
4. omitted evidence successfully retrieved by exact reference;
5. missing required evidence causes safe deferral rather than invention;
6. handoff conflicts with authoritative owner and fails closed.

Poker `CHG-0009` is a particularly useful real source candidate because it has a previous `Needs revision`, a bounded Planning revision, native-path investigation with a rejected applicability hypothesis, explicit current native disposition, separate Planning and Readiness gates, and rich durable evidence that should not all need to remain in active context.

### Existing `PL-V38-07`

Do not silently conflate two experimental variables.

The current Context Compiler arms:

```text
A raw canonical docs
B status snapshot
C snapshot + authoritative workflow
D Project Spine + workflow compiled AgentWorkPacket
```

primarily compare **source/context compilation strategies**.

Stage-history transport is a separate variable:

```text
T0 full prior observable transcript/history
T1 fresh context + governed StageContextHandoff + on-demand evidence
```

Recommended experiment design:

- first compare `T0` vs `T1` on a small fixed source packet;
- only after that is stable, optionally cross the transport variable with the Context Compiler arm;
- avoid a large combinatorial matrix before the basic effect is known.

### Existing `PL-V38-08`

Safe orchestration should consume governed handoffs only if earlier eval proves the contract.

No automatic material authority should be added.

---

## 8. Proposed evaluation plan

### Phase A — capture a real field fixture

After the current Poker readiness loop is complete:

1. preserve the observable Planning-stage trace as baseline evidence;
2. preserve the approved Planning artifacts;
3. create a compact candidate StageContextHandoff;
4. freeze exact source revision and workflow instructions.

### Phase B — paired comparison

Run the same Readiness task under two context transports:

```text
T0 FULL_HISTORY
  workflow + authoritative artifacts + prior observable trace

T1 GOVERNED_HANDOFF
  fresh model context
  + workflow
  + StageContextHandoff
  + authoritative artifacts
  + evidence retrieval on demand
```

Keep model, source revision, task, and authorization boundary fixed as far as practical.

### Phase C — correctness adjudication

Measure at least:

```text
semantic verdict correctness
authorization correctness
R/E blocker detection
false blocker rate
stale/rejected-branch contamination
safe deferral when evidence is missing
correct evidence/source identity
operator correction required
```

### Phase D — efficiency measurement

Measure at least:

```text
initial input tokens
total input tokens
peak active-context size
handoff size
number of evidence retrievals
files opened/reopened
tool calls
latency
cost when available
```

### Phase E — adversarial context fixtures

Add explicit cases where:

- an old hypothesis conflicts with the final accepted decision;
- an early `Needs revision` finding has already been resolved;
- a tool failure exists in history but no longer constrains the current stage;
- a relevant evidence item is omitted from the handoff but addressable by exact reference;
- a required evidence ref is broken or stale.

The desired behavior is not maximum compression.

The desired behavior is:

```text
small enough context
+
correct current state
+
recoverable evidence
+
safe failure when context is insufficient
```

---

## 9. Promotion criteria

Do not promote fresh-context stage handoff merely because it saves tokens.

Candidate promotion requires:

1. no material semantic-correctness regression;
2. no authorization/gate regression;
3. no increase in missed material blockers;
4. no provenance weakening;
5. safe retrieval or deferral when omitted evidence becomes necessary;
6. measurable reduction in active context burden on at least one representative long-running workflow;
7. no requirement to duplicate authoritative project truth in another large state system.

A practical outcome may be:

```text
QUALITY: non-inferior
CONTEXT: materially smaller
LATENCY/COST: improved or bounded
STALE-CONTEXT ERRORS: reduced
```

If quality regresses, preserve the externalized-evidence idea but do not promote automatic fresh-context reset.

---

## 10. Anti-overreach constraints

This recommendation does **not** imply:

- persistence of hidden chain-of-thought;
- a requirement to expose model-private reasoning;
- deleting durable evidence to save tokens;
- making summaries authoritative;
- vector search as the default reconstruction mechanism;
- a vector database;
- a graph database;
- a new Project Spine domain model;
- a new workflow engine;
- a general multi-agent memory service;
- auto-rewriting canonical planning artifacts;
- automatic stage reset before dependency/evidence references are validated;
- provider-specific Planning Lite semantics;
- replacing current Project Spine lineage with generic conversational memory.

Prefer the smallest mechanism that can prove the hypothesis.

---

## 11. Recommended Roadmap disposition

Do **not** add a new `PL-V38-*` stage solely for this recommendation.

Current sequencing remains field-first.

After the active Poker `CHG-0009` readiness loop is closed:

```text
REC-PL-CONTEXT-HANDOFF-001
        ↓
PL-V38-05
  refine context policy + ContextTrace
        ↓
PL-V38-06B
  qualify handoff/context fixtures
        ↓
PL-V38-07
  test fresh-context transport separately from compiler strategy
        ↓
PL-V38-08
  automate only if evidence supports it
```

This recommendation is therefore an **input to already planned work**, not a justification for roadmap expansion.

---

## 12. Why this matters for Planning Lite specifically

Planning Lite is designed around bounded authority:

```text
one stage
one workflow
one gate
one explicit authority boundary
```

Context inheritance should follow the same philosophy.

A stage should have bounded authority not only over what it may **do**, but also over what it may **inject into the attention of future stages**.

Candidate principle:

> **Bounded authority should imply bounded context propagation.**

Operationally:

```text
think / inspect as much as the stage legitimately needs
        ↓
preserve evidence
        ↓
distill current governed state
        ↓
hand off only what the next stage needs by default
        ↓
retrieve deeper evidence only when demanded
```

This preserves long-horizon capability without making every future model call carry the archaeological layers of every earlier investigation.

---

## 13. External evidence classification

| Source | Evidence type | Planning Lite relevance | Caution |
|---|---|---|---|
| OpenAI Agents SDK | current framework documentation | filtered/compacted handoff while retaining session history | framework mechanism, not governance semantics |
| Microsoft AutoGen | current framework documentation | bounded model-context view + separate memory protocol | generic agent framework |
| LangChain/LangGraph | current framework documentation | trim/summarize/filter/checkpoint active context | message-centric, less stage-governed |
| OpenHands | open-source architecture + vendor benchmark | durable event semantics + condensed model view; paired quality/efficiency evaluation | benchmark is vendor-reported and subset-specific |
| Manus | production engineering report | filesystem externalization, restorable compression, current-goal recitation | engineering experience, not controlled academic benchmark |
| MemGPT | research lineage / arXiv | virtual context / hierarchical memory | broader conversational/document memory problem |
| Letta Context Repositories | 2026 product/research engineering | Git-backed external memory, progressive disclosure | broader self-managed memory design |
| MAGE | 2026 arXiv preprint | execution-state lineage, completed-subgoal compression, flawed-branch isolation | fresh preprint |
| Agent Memory characterization | 2026 arXiv preprint | system-level lifecycle/cost measurement | broad memory systems study |
| Oracle Agent Memory | 2026 vendor technical report | active/passive memory separation, lifecycle, token measurement | vendor report |

---

## 14. Canonical placement and follow-through

Canonical location:

```text
docs/design/project-spine/REC-PL-CONTEXT-HANDOFF-001-v1.md
```

Why this location:

- the finding is cross-cutting Project Spine/context-governance design evidence;
- current field-derived recommendations such as `REC-PL-DIRECTION-002-v1.md` and `REC-PL-READINESS-001-v1.md` live in the same design area;
- it should inform the current v3.8 direction track;
- it should not be buried only inside legacy `.planning-lab` recommendation history.

After the current Poker readiness loop finishes, add references from the then-current:

```text
docs/design/project-spine/PL-V38-CURRENT.md
docs/design/project-spine/PLANNING-LITE-ROADMAP-v3.8.x.ru.md
docs/design/project-spine/README.md
```

Do not rewrite or supersede legacy `REC-PL-MEMORY-EFFICIENCY.ru.md` merely to add this finding.

At `PL-V38-06A`, reconcile the relationship between this recommendation and the preserved Lab memory/context recommendations as part of the already-planned research-asset lineage work.

---

## 15. Current evidence state

### Already field-observed in Planning Lite / Poker

- long Planning/Readiness work can accumulate substantial observable context;
- `PL-V38-CURRENT.md` already acts as a compact resumable state primitive;
- current Project Spine design already favors visibility decay, lineage-first retrieval, and bounded context;
- Poker `CHG-0009` contains a realistic rejected-hypothesis case: existing native acceleration was investigated, verified in its own seam, then adjudicated `NOT_APPLICABLE_FALLBACK_REQUIRED`;
- subsequent Readiness should need the adjudicated disposition and evidence reference, not every exploratory native-inspection message.

### Externally corroborated

- next-agent input can be filtered independently from retained history;
- model context can be a bounded view over broader state;
- event histories can remain durable while a condensed view is presented to the model;
- filesystem/external memory can make compression recoverable;
- progressive disclosure is used in production/research systems;
- execution-state-aware memory may outperform similarity-first history retrieval on long-horizon tasks;
- meaningful efficiency claims are possible only when paired with correctness measurement.

### Still to test in Planning Lite

- whether fresh-context stage bootstrap is non-inferior to full-history inheritance;
- the minimum handoff schema that preserves correct Readiness behavior;
- whether stale/rejected hypothesis contamination measurably decreases;
- the retrieval cost of omitted evidence;
- whether a deterministic owner-derived handoff is better than generic LLM summarization;
- whether the benefit survives outside research-heavy Poker work.

---

## 16. Provisional conclusion

The original field intuition is supported, but the strongest version is not:

```text
"agents should summarize more"
```

It is:

```text
Planning Lite should govern the boundary
between durable execution history
and the bounded context view inherited by the next stage.
```

The target is not to make agents think less.

The target is to let a stage perform deep work, preserve what must remain inspectable, and then hand the next stage a clean, authoritative, recoverable state instead of an ever-growing transcript.
