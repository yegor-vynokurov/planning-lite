# Brownfield Recovery

- Status: `DRAFT`
- Reflects revision:
- Recovery trigger:
- Recovery decision:
- Direction authority ceiling:
- Evidence scope:
- Refresh condition:

This is bounded direction/provenance recovery evidence.

It is not a second Target, Current State, Gap Map, Roadmap, or project-history archive.

## Recovery decisions

Use exactly one current decision:

```text
REUSE_CURRENT_ACCEPTED_DIRECTION
RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL
BLOCKED_DIRECTION_CONFLICT
INSUFFICIENT_DIRECTION_EVIDENCE
```

Rules:

- `REUSE_CURRENT_ACCEPTED_DIRECTION`: sufficient accepted direction already exists; stop historical recovery except for material provenance/conflict.
- `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`: bounded evidence supports a usable candidate, but recovery alone does not accept Target intent.
- `BLOCKED_DIRECTION_CONFLICT`: materially different live authorities remain and existing rules cannot order them safely.
- `INSUFFICIENT_DIRECTION_EVIDENCE`: bounded available evidence cannot establish a safe direction candidate.

## Authority / provenance notation

Every material direction claim must use one of:

```text
CURRENT_ACCEPTED_AUTHORITY
EXPLICIT_USER_DECISION
PRIOR_ACCEPTED_AUTHORITY
EXISTING_DIRECTION
HISTORICAL_RESIDUE
CONFLICTED_AUTHORITY
UNKNOWN
```

Recovery may preserve or lower confidence/authority. It must not silently raise authority.

```text
historical/project evidence
→ may support a recovered candidate

recovered candidate
→ does NOT become accepted Target intent without acceptance authority
```

## Current usable direction

Record only the material direction needed for downstream shaping.

For `REUSE_CURRENT_ACCEPTED_DIRECTION`, cite the accepted authority and do not restate it as a replacement Target.

For `RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`, state the candidate compactly and mark it provisional.

## Material authority / provenance table

| Direction claim | Authority class | Source evidence | Current use |
|---|---|---|---|

## Material historical conflicts

Record only conflicts that could materially change downstream project outcomes.

Do not silently merge conflicting authorities.

## Historical residue excluded from current authority

Record stale/superseded material only when excluding it prevents downstream ambiguity.

## Unresolved blocking questions

Record only questions that block safe downstream direction shaping.

Route unresolved Target-boundary authority questions to clarification/user decision.

## Bounded evidence references

List only evidence actually used for the recovery decision.

Do not load full project history by default.

## Stop rule reached

Use one:

```text
BR-STOP-01 / sufficient current authority
BR-STOP-02 / bounded provenance sufficient
BR-STOP-03 / material unresolved conflict
BR-STOP-04 / evidence exhaustion
```

## Freshness / reuse decision

State when this recovery result can be reused and what material change would invalidate it.

History volume, file age, or minor unrelated drift do not by themselves invalidate a bounded recovery result.
