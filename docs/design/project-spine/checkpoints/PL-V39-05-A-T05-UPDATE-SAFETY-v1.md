# PLANNING LITE / PL-V39-05-A / T-05 CONSUMER UPDATE-SAFETY v1

**Document ID:** `PL-V39-05-A-T05-UPDATE-SAFETY-001`
**Date:** `2026-08-27`
**Change:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001`
**Task:** `T-05`
**Task verdict:** `COMPLETED`
**Implementation authorization:** `YES`
**Push authorization:** `NO`

## Disposable consumer proof

Pre-Survey baseline: `8c9e303cf3cb4a8b3bb000cb9ed02cfb0388bb97`

Candidate/current central: `2fbe27430ec67f23deacb6f774c7b7bd8e66e4cd`

Required split:

```text
managed:       .planning/assessments/PROJECT_SURVEY_TEMPLATE.md
project-owned: .planning/assessments/current/PROJECT_SURVEY.md
```

Preview proved:

```text
ADD_MANAGED  .planning/assessments/PROJECT_SURVEY_TEMPLATE.md
REMOVE_MANAGED = 0
project Survey preview mode = OMITTED_ALLOWED
```

The local-only preview is not required to enumerate every arbitrary ignored project-owned file under a broad ownership glob. The materialized Survey safety contract is therefore proven by absence of unsafe action for that path plus byte-for-byte preservation after apply.

After local-only apply:

```text
managed Survey template = canonical-LF content equals central source
materialized Project Survey = preserved raw-byte-for-byte
consumer Doctor = OK
second preview = zero mutating actions
second apply = ownership/idempotence PASS
```

Project Survey sentinel SHA256: `4b84271decd91a7e840b491231baaa2a35dcd1e6a241f258eaf4e30a8ad61ec9`

Managed central raw SHA256: `c90646f852deb03bea2043df25e34c39dac868303dc77b91ddfdabfb84838d6d`

Managed central canonical-LF SHA256: `c90646f852deb03bea2043df25e34c39dac868303dc77b91ddfdabfb84838d6d`

Managed consumer raw SHA256: `b35e86324c3f93b5c50779f68e3f5c9aaf2aedd2d49f748277c292887e2e83b5`

Managed consumer canonical-LF SHA256: `c90646f852deb03bea2043df25e34c39dac868303dc77b91ddfdabfb84838d6d`

Managed serialization: `LF_SERIALIZATION_ONLY`

The fixture lived only under a temporary directory and was removed automatically. No Poker or other live consumer project was touched.

## Verifier defect adjudication

The first T-05 probe incorrectly required an explicit `KEEP_PROJECT` preview row for `.planning/assessments/current/PROJECT_SURVEY.md`. This consumer path is arbitrary project-owned state inside an ignored local-only subtree and may be omitted from the preview plan. AC-11 requires preservation, not preview enumeration.

A second T-05 verifier assumption required raw-byte identity for a managed file. On Windows the update path may serialize LF as CRLF. Planning Lite's integrity contract already canonicalizes CRLF to LF, so managed-content equality is adjudicated canonically while consumer-owned state remains raw-byte protected.

```text
VERIFIER_DEFECT
preview enumeration assumption = corrected
managed raw-byte assumption = corrected
project-owned byte preservation = strict
product defect = NO
```

## Repository-owned regression

`tests/test_local_only_update.py`: PASS

## Boundary

No product/template/src/copier/ownership file was changed in T-05. Central writes are state/receipt only.

## Next permitted task

`T-06 — completion review`
