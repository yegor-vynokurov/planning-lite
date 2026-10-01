# Architecture Decision Flow

Use this flow only for one material architecture-sensitive question that the owner explicitly asks to resolve, or that an already approved Change explicitly includes. It is optional and does not apply to routine work or every technical/design question. Keep routine implementation choices on their ordinary workflow.

The flow records a bounded decision that can be handed to ordinary Planning Lite Change definition and planning. It does not add decision authority, a new approval status, an ADR subsystem, or runtime behavior. Use the existing project-owned `.planning/project/ARCHITECTURE_OVERVIEW.md` as the compact carrier; record references to evidence and semantic artifacts rather than copying them.

## Establish the question and its evidence

Before comparing designs, record exactly one material decision question for this invocation. Reference the Goal and tier when available, one Critical Flow, relevant facts and constraints, and their sources. Mark project context `GREENFIELD` or `BROWNFIELD`.

For `BROWNFIELD`, describe observed topology only from scoped repository/runtime evidence and reconcile it to cited sources. Label observation, inference, and unknowns; include source and scope. Existing topology is evidence about the as-is system, never authority for Ideal or target architecture. Do not invent historical intent from implementation.

If material authority, provenance, or facts are missing, stop and request the specific missing evidence or owner decision. Do not fill gaps with assumptions.

## State material drivers and scenarios

For each material driver, capture an ID, source reference, affected capability or seam, type (`FUNCTIONAL`, `QUALITY`, `CONSTRAINT`, `RISK`, or `EVOLUTION`), uncertainty, confidence, and a measurable bound when one is known. Keep uncertainty visible; do not present an unsupported estimate as a fact.

Write one to three measurable scenarios. Each scenario identifies its stimulus, context, affected asset, expected response, and response measure. Quality scenarios need a measurable response measure or bound; if a material quality concern cannot be measured well enough to compare, stop and request bounded evidence or clarification.

## Compare alternatives and choose a terminal result

Compare at least two credible alternatives, including a simpler option unless the accepted baseline itself is the decision. For each alternative record its benefit, trade-off, operational burden, reversibility, and evidence. Cite evidence for claims and uncertainty. Do not invent weighted scores or an arbitrary numeric winner; explain the choice against the drivers and scenarios.

Finish with exactly one terminal result: `DECISION_ACCEPTED` or `SPIKE_REQUIRED`.

- For `DECISION_ACCEPTED`, identify the selected alternative and record the bounded decision and its evidence. Do not imply implementation authorization; continue through ordinary Change definition, approval, and planning.
- For `SPIKE_REQUIRED`, state the bounded request, the stop condition, and the evidence or answer that unlocks the decision. Do not silently turn the spike into implementation.

If no credible alternative can be compared, stop rather than fabricating one. A second material question requires a separate record and invocation; it may be listed only as a related future question here.

## Keep the architecture horizons explicit

For an accepted decision, distinguish:

- `TARGET`: the intended architecture outcome and its authority/evidence reference.
- `MVP-REFERENCE`: the smallest useful realization that demonstrates the relevant decision and scenarios.
- `TRANSITION`: the bounded move from observed/current state toward the reference, including sequencing or coexistence when needed.

Keep risk notes local and small: `REPLACEMENT_OR_SCALE_RISK`, `REOPEN_TRIGGER`, and `NEXT_TRANSITION`. Add `CHEAP_REPLACEABILITY_SEAM` only when a concrete seam makes later replacement materially cheaper. For each material selected claim, identify at least one practical evidence/fitness route, such as a measurable check, observed behavior, or a cited source to review during ordinary planning or execution.

## Handoff and stop conditions

Hand an accepted semantic decision to the existing 09-E `plan-compile` workflow through ordinary Change definition, semantic Plan, and tasks. Compiled output never replaces the semantic Plan as decision authority. Keep the decision record as references and a concise rationale; do not duplicate the full 09-B definition or 09-E planning rules here.

Stop this flow when authority, provenance, or material facts are missing; a material quality scenario is unmeasurable; no credible alternative exists; a second question appears; or resolution would require a new schema, decision authority, or runtime mechanism. Capture a bounded `SPIKE_REQUIRED` request when evidence can resolve the issue. Route a second question to a separate record and invocation. This guidance does not introduce 09-G, Context Compiler, SQLite/vector storage, Prompt Garden machinery, or other runtime expansion.
