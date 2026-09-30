# Route B T-01..T-05 Implementation Candidate Review

## Transition

- Change: `CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001`
- Transition: `OWNER_REVIEW_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05_CANDIDATE`
- Review scope: independent review of the prepared implementation candidate; governance recording only.
- Verdict: **REVIEW_FAIL / 2 MATERIAL FINDINGS**
- Material findings: 2
- Nonmaterial advisories: 2
- Entry HEAD: `19217522f3dac695602a8534d7ddb8f9bbee5858`
- Entry index: empty
- Entry authority state: `77d4d92d68d1ebabb77b54245739c57d8052f938f4430bc967e58bb76ac7d434`
- Entry candidate state: `5165b501284cdc06e5b219d4bc1863a104e9147e249a176ceb629f34850a175a`
- Entry unrelated dirt state: `2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a`
- Entry sync state: `9640421549b94558f57c8506b2605f53dc41752970ed010e3d9412b11f01b952`

## Reviewed candidate

Execution receipt: `docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-ROUTE-B-T01-T05-IMPLEMENTATION-EXECUTION-v1.md`

Execution receipt SHA256: `df0f9b4d00343ab9c17b34c88ed4fd89a7edc5b9df05b5d8f541d738e98a9521`

Result: candidate prepared. T-01, T-02, T-03, T-04, and T-05 are complete; T-06 was not executed. The focused suite recorded 117 passed and 0 failed; acceptance recorded 20/20. No authorized implementation surface violation was reported.

Candidate state: preserved exactly as reviewed. Candidate product paths (4):

- `src/planning_lite/telemetry.py`
- `scripts/capture_codex_run_receipts.py`
- `src/planning_lite/codex_work_window.py`
- `src/planning_lite/cli.py`

Candidate test paths (4):

- `tests/test_run_receipts.py`
- `tests/test_codex_run_receipt_capture.py`
- `tests/test_codex_work_window.py`
- `tests/test_cli.py`

The candidate state ID remains `5165b501284cdc06e5b219d4bc1863a104e9147e249a176ceb629f34850a175a`. No candidate product or test bytes were changed by this review transition.

## Material findings

### R5-01 ? `PLANNING_LITE_REF_PROVENANCE_OMITTED`

- Status: **OPEN**
- Classification: material implementation contract deviation
- Affected tasks: T-01 / T-04
- Affected paths: `src/planning_lite/telemetry.py`, `src/planning_lite/cli.py`, `src/planning_lite/codex_work_window.py`, `tests/test_run_receipts.py`, `tests/test_codex_work_window.py`, `tests/test_cli.py`

Active Plan Amendment v5 requires recording `configuration_ref`, provider, model when known, and the installed Planning Lite ref separately. `WorkWindowRegistrationV1` and `ResourceObservationV1` do not carry the Planning Lite ref, so the Work Window open/finalize path cannot persist and bind that independent provenance. Configuration identity and installed framework provenance must remain separate; otherwise observations produced under different installed refs may be indistinguishable on this audit axis.

Required semantics for a separately authorized corrective pass: obtain authoritative `planning_lite_ref` from the existing installed/current Planning Lite project authority mechanism, not arbitrary caller input; persist it prospectively in `WorkWindowRegistrationV1`; copy it unchanged into `ResourceObservationV1`; include it in registration replay/conflict semantics and observation-to-registration binding validation; preserve it through canonical readback; leave legacy RunReceipt v1/v2 semantics unchanged; and do not redefine `configuration_ref`. Do not create a new registry or configuration system. No correction was performed or authorized by this review.

### R5-02 ? `CODEX_SOURCE_ENVELOPE_FAIL_CLOSED_GAP`

- Status: **OPEN**
- Classification: material measurement integrity failure
- Affected tasks: T-03 / T-05
- Affected paths: `src/planning_lite/codex_work_window.py`, `tests/test_codex_work_window.py`

The active Plan requires recognizing the allowlisted current Codex JSONL envelope and failing closed on unknown source shapes that could hide resource usage. `token_usage_record` rows receive full JSON validation, but known non-usage top-level record types receive only structural type scanning. The skip path does not fully validate JSON scalar syntax and does not require the complete current host envelope for every accepted non-usage record.

Independent adversarial reproduction: a measured synthetic segment containing `{"type":"response_item"}` followed by a valid `token_usage_record` finalized with `source_completeness=COMPLETE`, `unavailable_reason=null`, and supported quantities emitted as `DIRECT / COMPLETE_SCOPE_TOTAL`. A second probe showed malformed scalar content in a known non-usage row could also pass the skip path while a later valid usage row still produced a direct complete total. This can overstate completeness when a malformed, corrupted, or incompatible host row occurs inside the measured byte segment.

Required semantics for a separately authorized corrective pass: preserve the privacy/content boundary?do not decode, persist, separately hash, semantically inspect, or echo prompt, assistant, tool-payload, or reasoning bodies. Syntactically validate every bounded JSONL line; require the current accepted top-level envelope structure; retain strict usage validation for `token_usage_record`; permit content bodies to remain opaque only under a structurally valid accepted envelope; fail closed on unknown or incompatible envelope/discriminator shapes that could conceal changed resource semantics; make a stable bounded malformed/incompatible segment yield one terminal `UNAVAILABLE` observation rather than `DIRECT / COMPLETE_SCOPE_TOTAL`; and add deterministic adversarial tests for incomplete/malformed known envelopes and unknown usage-adjacent envelope/discriminator variants. Do not expand into provider research or a generic JSON/event framework. No correction was performed or authorized by this review.

## Nonmaterial advisories

- **N5-A01 ? observation identity derivation:** the producer deterministically uses `work-window-observation-v1:<SHA256(window_id UTF-8)>`, but the generic `ResourceObservationV1` validator does not independently enforce the derivation. Status: nonmaterial hardening only; not a blocker for the bounded corrective pass.
- **N5-A02 ? timestamps:** the shared timestamp validator accepts parseable timezone-naive ISO timestamps, while the Route B producer emits UTC `Z` timestamps. Status: nonmaterial hardening only; do not expand corrective scope solely for this advisory.

## Positive closures

Independent source review found no material issue in these 21 areas:

1. legacy RunReceipt v1/v2 separation;
2. separate typed identity namespaces;
3. lock-protected scan/check/append replay;
4. prospective registration;
5. binary start/end byte boundaries;
6. source identity and prefix-anchor checks;
7. fixed captured end boundary;
8. bounded double-read digest stability;
9. `token_usage_record.usage` as primary source;
10. response deduplication by `(thread_id, response_id)`;
11. conflicting duplicate failure;
12. provider-native arithmetic checks;
13. optional metric absence semantics;
14. `DIRECT / COMPLETE_SCOPE_TOTAL` per supported complete quantity;
15. exact persisted readback;
16. no Attempt bridge;
17. no second persistence store;
18. no T-06 execution;
19. no efficiency judgment;
20. no 09-G behavior;
21. authorized implementation surface compliance.

Provider-neutral serialization note: **not material; not a third finding.** Definition v6 freezes provider-neutral semantic meaning rather than persisted field names, and active Plan v5 permits rollout identity, byte offsets, segment digest, response count, and response-identity digest as first-adapter provenance. Later provider adapters may need additive schema evolution; that is not a blocker for this first slice.

## Governance disposition

- `T01_T05_IMPLEMENTATION`: EXECUTED / CANDIDATE PRESERVED / REVIEW FAIL
- `IMPLEMENTATION_CANDIDATE`: PRESERVED / DO NOT COMMIT
- `ADDITIONAL_IMPLEMENTATION_MUTATION_AUTHORIZED`: NO
- `CORRECTIVE_IMPLEMENTATION_AUTHORIZED`: NO
- `T06_FIELD_PROOF_AUTHORIZED`: NO
- `T00_REEXECUTION_AUTHORIZED`: NO
- `09_G_STARTED`: NO
- `ROADMAP_CHANGED`: NO
- `SOURCE_CHANGED`: NO
- `TESTS_CHANGED`: NO

This receipt records the review findings only. It does not authorize corrective implementation, T-06 field proof, T00 re-execution, a real measured Work Window, or 09-G. The next single gate is `OWNER_AUTHORIZE_CHANGE_3_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION`.

## Entry evidence rechecked before recording

- Definition v6 SHA256: `aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74`
- Plan v5 SHA256: `b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db`
- Formal Readiness SHA256: `09aa37a64832948f02f8451fa0a20c9e09a4b03832a58d0c04f11dfd7925a439`
- Implementation authorization SHA256: `2ce7ca510631182c705286d92f3ab344dbc3daefe43aea3af2a3371593593b9c`
- Candidate disposition/archive record SHA256: `ed9919a02123a65d4bdb06fc7a9be598616c7c7a757471e7ac90630dca58c7cc`
- Candidate archive manifest SHA256: `96fcef0094cb0fb41a73f6d40d49f323f55f1c20ba2a79ce73ec4d9be79f1aff`; the manifest sidecar and all listed archive artifact lengths and hashes matched at entry.
- Roadmap SHA256: `4682e29322a574ef77040ea173e06352a99b3da18b527a8b22f3a8c9ffc7d1b0`
- Index was empty; unrelated dirt matched its entry state ID.
