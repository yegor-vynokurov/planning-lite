# PL-V39-09 Execution Efficiency Bootstrap — Slice A Independent Review v1

## Review identity and authority

```text
Change: CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001
Slice: A — CODEX_TELEMETRY_CAPTURE
Review phase: COMPLETE
Review mode: READ_ONLY
Entry HEAD: 748fbe70dd6f3d5a6d7242df41ace2d573c40d55
Definition SHA-256: 9AA61891CC31C1E784F6A7A7892D4535C5E0E4D1B25343AD995DC79B6D70912C
Approved Plan SHA-256: CFEFD5915BAE7B7C427A343380E0A29C041EE6D52D83FCCEA3AB10E3D9A1BB5A
Formal Readiness SHA-256: 60DDC1F170EA8FB0D4041FCA3ECB45D56DABF0D0F726028BF21639C83979F0C6
Execution Ledger SHA-256: 527CBD1893A17415AF5D86BFAB040D2C4B529072B0595273DBFEB5DCE1CD7840
Entry CURRENT SHA-256: 282220C33CE3610489D2F6A10DB3D4A18588CFF5A5DFD821BA60D29E4C71E4F4
Reviewer model requested: GPT-5.6 Luna / Extra High
Reviewer model confirmed: YES
Reviewer independence: BOUNDED_CHILD
Nested delegation used: NO
```

The reviewer read the required authority, candidate, and RunReceipt owner set
and treated the Execution Ledger as claims to reproduce. The reviewer remained
project-read-only. All independent mutation probes used disposable OS-temporary
Git repositories and were cleaned. The parent wrote this artifact only after
validating the reviewer evidence.

## Frozen candidate and evidence identities

```text
scripts/capture_codex_run_receipts.py SHA-256:
9400EBBE58EAC55E425F38FDCF3CF11C3B04898402132CE27DFE3168A4EEF6D3

tests/test_codex_run_receipt_capture.py SHA-256:
37783ECA5C91BC76EFE890A86ED79C34F222EDCC75004C222B6C4E481DD8223A

src/planning_lite/telemetry.py SHA-256:
CA1F9D32E4E93528A5ED9871763F7E125657C31E11611BA33F6AEC9B9B6030B7

tests/test_run_receipts.py SHA-256:
54ACA4A2324A26C3DEFB43510D5F8DCCAB99576F0685333359E6F0485CAC264B

local real-host receipt stream SHA-256:
D67102B0A69844C041963932581D9943A03087FE197D977AB21A738DD52AFF61
```

Exactly two Slice A implementation paths were present. There were zero staged
paths, zero Slice B candidate paths, and zero unauthorized Slice A project
paths. `telemetry.py`, `workspace.py`, `cli.py`, the existing owner tests, and
all template paths remained read-only.

## Reproduced evidence

```text
focused Slice A tests: 20 passed
RunReceipt owner regression: 5 passed
original RED reconstruction: 1 passed, 2 expected failures
RED failure marker: CAPTURE_CAPABILITY_MISSING
production-equivalent Walking Skeleton: PASS / expected 2 / actual 2
real-host proof: PASS for the frozen H1 operation / expected 2 / actual 2
real-host identical replay: PASS / count and stream SHA unchanged
structured metadata only: YES
explicit host binding: YES
git diff --check: PASS (line-ending warning only)
```

The reviewer independently recomputed the normative receipt-ID vector and the
two real-host IDs:

```text
normative child vector:
codex-run-v1:8a5db46c63972343069db409940828848164a22cfaf297126c072e8bc8795283

real-host parent:
codex-run-v1:351af9f27978a186858dff2b410b688a5221b961c41a79bd9893cea3d6cfb3ce

real-host child:
codex-run-v1:d07b403553bddb75dabcabd2486acfa8c2353bc97dd3f357e77e0a680ea6f5e3
```

The frozen real-host proof remains valid for its initially empty H1 operation
stream: exact parent `gpt-5.6-sol / high`, child `gpt-5.6-luna / xhigh`, direct
session/turn linkage, null `model_tier`, exact counter mapping, and unchanged
two-record read-back were independently confirmed without content inspection.
That proof does not exercise either blocking stream-state scenario below.

## Rubric

| Rubric | Result | Independent review evidence |
|---|---|---|
| R-01 Authority/scope | PASS | Exact authority hashes; two implementation paths; no Slice B or owner mutation |
| R-02 Code contract | BLOCKED | Existing-operation preflight can write before count failure; historical valid refs make the shared stream unusable at a new HEAD |
| R-03 Privacy | PASS | Discriminator-first metadata projection and hostile opaque-content test; no content used by real-host verification |
| R-04 RED evidence | PASS | Reconstructed pre-adapter state reached the intended missing-capability seam: one pass and two expected failures |
| R-05 Focused GREEN | PASS | `20 passed` |
| R-06 RunReceipt regression | PASS | `5 passed` |
| R-07 Discriminator coverage | BLOCKED | No test covers a valid alien same-operation ID below expected count or valid historical receipts from another HEAD |
| R-08 Receipt identity | PASS | Normative SHA-256 vector recomputed; stable identity, token exclusion, role/session/turn/index participation confirmed |
| R-09 Preappend atomicity | BLOCKED | Independent same-operation alien-ID probe wrote two new receipts before returning `RECEIPT_COUNT_MISMATCH` |
| R-10 Replay | PASS | Ordinary identical replay, canonical conflict, and interrupted-prefix recovery pass |
| R-11 Production-equivalent Walking Skeleton | PASS | Actual CLI → parser → existing validator/append → JSONL → deterministic read-back, 2/2 |
| R-12 Real-host proof | PASS | Frozen explicit H1 parent/child binding, mappings, IDs, 2/2 count, and unchanged idempotent replay independently verified |
| R-13 No false done | BLOCKED | Happy-path A-04/A-05 evidence exists, but it did not expose two material append-stream defects |
| R-14 Non-blocking finding audit | PASS | Two verifier repairs and one external child usage-limit interruption remain non-blocking |
| R-15 Scope/Git audit | PASS | Exact two-path implementation surface; no staged, Slice B, owner, or unauthorized mutation |

## Blocking findings

### BR-A-01 — operation-count preflight is not zero-write

The independent disposable probe created one structurally valid existing
receipt with the same operation keys but a different unique opaque
`receipt_id`, then invoked the two-candidate parent/child capture:

```text
before_count: 1
command result: RECEIPT_COUNT_MISMATCH
after_count: 3
NEW_RECEIPTS_WRITTEN: 2
```

`capture()` checks only whether the number of existing operation records is
greater than the candidate count. It does not prove before append that every
existing operation receipt ID belongs to the candidate set. Both candidates
are appended and the exact-count mismatch is detected only during read-back.
This violates the approved Plan's requirement that existing-stream
classification and expected-count validation finish before the first append,
and that a preappend validation failure write zero new receipts.

Required repair direction: classify the complete existing same-operation ID
set against the candidate ID set before append and add the nearest-wrong
zero-write regression. Exact repair remains owner-gated; this review does not
authorize or implement it.

### BR-A-02 — valid historical HEAD receipts block later capture

The independent disposable probe captured two receipts at H1, committed the
fixture repository to H2, and attempted a different valid operation at H2
against the same project receipt stream:

```text
H1 receipt count: 2
H2 command result: RECEIPT_STREAM_INVALID
final receipt count: 2
H2 receipts written: 0
```

`_read_existing()` supplies the current `binding.expected_head` when validating
every historical receipt. A valid H1 receipt therefore becomes invalid merely
because capture now runs at H2. The existing RunReceipt append owner was
independently checked and supports valid records carrying different
`planning_lite_ref` values. The defect is adapter-local and prevents the
append-only normal-work stream from continuing after the next Git commit.

Required repair direction: structurally validate each historical receipt using
its own exact stored `planning_lite_ref`, while still requiring new candidates
to match the current verified HEAD; add a cross-HEAD append regression. Exact
repair remains owner-gated; this review does not authorize or implement it.

## Non-blocking finding audit

1. The original missing-counter test mutation accidentally duplicated a
   completion. The verifier-only repair removed both counters without changing
   the product contract; the node now reaches `MISSING_FINAL_COUNTER`.
2. The original direct import depended on pytest namespace-path behavior. The
   verifier-only repair uses an explicit script-path import seam; receipt-ID
   assertions remain substantive.
3. The earlier bounded child stopped because of an external usage limit after
   confirmed `GPT-5.6 Luna / Extra High` dispatch. Partial work remained inside
   the exact two-path surface, the parent continuation was authorized, and no
   nested delegation occurred.

No skip, xfail, assertion deletion, broader implementation write, or stronger
child substitution was used. These three findings remain non-blocking and are
independent of the two blocking product defects.

## Verdict and authority boundary

```text
SLICE_A_REVIEW_PHASE: COMPLETE
OVERALL: BLOCKED
MATERIAL_FINDING_COUNT: 2
BLOCKING_FINDING_COUNT: 2
NON_BLOCKING_FINDING_COUNT: 3
PRODUCTION_EQUIVALENT_WALKING_SKELETON: PASS
REAL_HOST_PROOF: PASS
SLICE_A_FIELD_PROOF: PROVEN
ALL_CANDIDATES_PREVALIDATED: FAIL
SLICE_A_FALSE_DONE_BLOCKED: YES
SLICE_A_OWNER_ACCEPTED: NO
SLICE_A_COMMIT_AUTHORIZED: NO
SLICE_B_EXECUTION_AUTHORIZED: NO
STAGE_PERFORMED: NO
COMMIT_PERFORMED: NO
NEXT_SINGLE_GATE: OWNER_ADJUDICATION_PL_V39_09_EXECUTION_EFFICIENCY_BOOTSTRAP_SLICE_A_REVIEW_REPAIR
```

The review is evidence only. It grants no repair, acceptance, commit, Slice B,
Roadmap sequencing, recommendation absorption, or release authority.
