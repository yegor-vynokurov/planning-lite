# Mode router

Modes are selected per user turn, not permanently. This prevents a stale execution state from surviving a topic change, a new session, or context compaction.


## Explicit commands

The user may write an equivalent natural-language instruction or invoke the logical skill name through the active adapter:

- `Mode: dialogue` / `planning-dialogue`
- `Mode: plan` / `planning-plan`
- `Mode: execute` / `planning-execute`
- `Mode: quick fix` / `planning-quick-fix`
- `Mode: audit` / `planning-audit`
- `Mode: recover` / `planning-recover`
- `Make checkpoint` / `planning-checkpoint`
- `Make Git review` / `planning-git-review`

The adapter determines whether a logical skill is invoked with `$name`, `/name`, a menu, an external skill directory, or a direct file read. An explicit mode applies to the current request. It does not authorize actions forbidden by approval gates.

## Automatic routing

### Dialogue / critic

Use when the user:

- asks a question or requests an explanation;
- asks for ideas, options, trade-offs, criticism, or analysis;
- says “what do you think”, “is this sensible”, “compare”, “explain”, or “challenge this”;
- corrects or negotiates a plan without asking to update files;
- introduces an idea whose scope is not yet agreed.

### Planning

Use when the user asks to:

- analyze a proposed change and structure it;
- create or revise proposal, specification, acceptance criteria, plan, or tasks;
- convert accepted recommendations into one or more changes;
- amend an approved plan;
- prepare work but not write production code.

Planning may edit `.planning/` artifacts but not production code.

### Execution

Use only when the user directly asks to:

- implement an approved change;
- write or modify code according to the approved plan;
- execute named tasks or a named milestone;
- continue implementation already in progress.

Words such as “согласна”, “идея подходит”, “рекомендацию принимаю”, or “план выглядит хорошо” do not alone authorize code. A direct action verb is required, such as “выполняй”, “реализуй”, “пиши код”, or “сделай T003–T006”.

### Quick fix

Use when the user directly asks for a tiny edit and the request passes every criterion in `DRIFT_POLICY.md`.

Examples:

- fix capitalization in generated labels;
- correct a typo or one inaccurate error message;
- rename a private local variable without behavior change;
- add a missing narrow regression assertion.

If risk or scope is uncertain, route to Planning.

### Recovery

Use when the user says planning or code began without the right authorization, or asks to stop and reconcile accidental work. Follow `RECOVERY.md` and prompt `13`. Do not revert automatically.

### Audit

Use when the user asks to:

- assess current state;
- review code or a plan;
- find omissions or contradictions;
- check implementation against specification;
- measure drift from an approved plan;
- inspect unplanned changes.

Audit may update assessments, reviews, recommendations, and drift reports, but not production code.

## Mixed requests

When a message mixes discussion and implementation:

1. Separate the discussion decision from the executable instruction.
2. If the implementation target is already approved and unambiguous, execution may proceed.
3. Otherwise, answer or plan first and stop before code.

When a user asks a question during active execution, pause edits for that turn. Answer the question. Resume only on a new direct implementation instruction or when the same message explicitly says to answer and continue.

## Mode announcement

Do not clutter every response with a mode label. State the selected mode only when:

- intent is ambiguous;
- the mode changes an approval boundary;
- a requested quick fix is rejected and promoted to planning;
- execution must stop because the plan no longer fits reality.

## Control workflows

Checkpoint and Git review are bounded control workflows rather than persistent modes.

- Checkpoint stops production-code edits, writes durable state, and reports readiness for operator context compaction or a new session.
- Git review is read-only and escalates from summaries to targeted patches only when evidence requires it.

After either workflow, select the next mode again from the user's next request.
