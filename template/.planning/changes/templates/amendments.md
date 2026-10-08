# Amendments

| Date | Amendment ID | Type | Trigger and evidence | Old approach | New approach | Approval | Readiness impact | Changed dependency fields | Before values | After values |
|---|---|---|---|---|---|---|---|---|---|---|

Types: `Implementation detail`, `Scope`.

Give every record a stable unique Amendment ID and keep rows in governance
order. Encode the three effect cells as compact canonical JSON. `Changed
dependency fields` is a sorted unique array of exact projection-root keys;
`Before values` and `After values` contain the complete JSON value for every
listed key. For a record with no dependency effect, use `[]`, `{}`, `{}`.
Supported effect keys are the six mutable dependent contract/task fields
(`accepted_output_contract_ref`, `produced_artifact_logical_ref`,
`required_input_logical_ref`, `acceptance_contract_ref`,
`evaluation_scope_ref`, `required_verifier_contract_refs`) plus complete
`source_task_semantics`, `target_task_semantics`, task-local
`task_semantics`, or task-local `incoming_dependency_edges` values. Task
semantics values contain the full six-field task projection and therefore
identify their task. Do not add a caller-supplied materiality class: the
resolver derives each amendment's relation to each exact projection from its
complete values.

After the existing approval/reconciliation transition, end this file with the
generated receipt below. Its exact seven fields must match the current Plan,
fixed T-01 -> T-02 projection, amendments semantic hash, and ordered
applicable dependent amendment IDs. The receipt is excluded from the
amendments semantic hash and is not approval or execution authority.

## Dependency reconciliation receipt

```json
{"amendments_semantics_sha256":"0000000000000000000000000000000000000000000000000000000000000000","applicable_dependency_material_amendment_ids":[],"approved_plan_digest":"0000000000000000000000000000000000000000000000000000000000000000","change_id":"CHG-NNNN","dependency_semantic_digest":"0000000000000000000000000000000000000000000000000000000000000000","schema_version":1,"status":"RECONCILED"}
```
