# CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001 — Change Definition

- Status: `APPROVED / CENTRAL DEFINITION / NO IMPLEMENTATION AUTHORITY`
- Date: `2026-09-03`
- Roadmap source: `PL-V39-05 — Project Shaping and Target Reality`
- Slice: `PL-V39-05-C — Consumer Control Topology + Project Policy + Telemetry Baseline`
- Definition baseline: `a40019209c133785a4babe06b5e96dfd4673c4f5`
- Branch at definition creation: `reconcile/current-design-spine-2026-08-25`
- Canonical repository: `D:\documents\planning-lite`
- Implementation authorization: `NO`
- Plan preparation authorization: `YES`
- Plan approval: `NO`
- Live consumer migration authorization: `NO`

## 1. Authority and purpose

This is the single bounded central Change Definition for the owner-accepted
05-C slice. It is governed by:

1. `01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md`;
2. `02_PL_V39_05_C_IMPLEMENTATION_START_CONTRACT.md`;
3. `PL_V39_05_C_INCOMING_ADJUDICATION.md`;
4. the explicit `PL-V39-05-C-02` owner decision of `2026-09-03`.

The named program Roadmap overlay remains non-canonical design/program evidence.
It does not replace `docs/design/project-spine/roadmap/ROADMAP.md`.

This Definition freezes the problem, goal, scope, non-goals, invariants,
acceptance boundary, and authorization boundaries. Detailed decomposition
`T-01` through `T-09` remains owned by the existing Implementation Start
Contract and by a later, separately authorized Plan; it is not copied here.

## 2. Problem

Planning Lite already renders a consumer-local `.planning` control surface and
supports tracked and local-only update behavior, but it does not yet provide one
explicit multi-project foundation that:

- identifies registered projects through a stable Planning Lite home;
- distinguishes product Git from Planning/control Git;
- supports single-repo, split-control, and local-only control-history modes;
- expresses project policy through the existing configuration authority;
- keeps Doctor and update behavior safe across those modes;
- records small raw run receipts without inventing runtime facts or creating a
  semantic-memory system.

Without this bounded foundation, later Context/Memory/Handoff and
Execution/Skills work would inherit ambiguous repository, policy, update-source,
and evidence boundaries. The field consumers also cannot safely prove migration
without risking their live repositories.

## 3. Goal

Extend the existing Planning Lite configuration-home and consumer control
architecture so that a project can be registered and inspected under an explicit
policy, can use one of three control-history modes with deterministic product and
control Git contexts, and can append externally supplied `RunReceipt v1` records.

The result must preserve project-owned state and existing source precedence,
remain compatible with Doctor/update, and be demonstrated only through disposable
Poker and mood proofs plus central completion verification.

## 4. Bound architecture

### 4.1 Existing Planning Lite home extension

Reuse the existing config-home seam. Home resolution is:

```text
explicit --home
→ PLANNING_LITE_HOME
→ Path.home()/.config/planning-lite
```

The home is extended, not replaced, with:

```text
config.toml
projects.yml
control/<project-id>.git/
telemetry/<project-id>/run-receipts.jsonl
```

`projects.yml` stores topology and locators only. It must not copy semantic
project history or become a second Planning Lite product/control authority.

### 4.2 Existing policy authority extension

Reuse:

```text
template/.planning/framework/defaults.yml
template/.planning/CONFIG.yml
template/.planning/project/PROJECT_RULES.md
template/.planning/project/PROJECT_INSTRUCTIONS.md
```

Add the bounded `project_policy` defaults/overrides defined by the Implementation
Start Contract. Do not create `PROJECT_POLICY`, `POLICY`, or another policy file
or database. Project-specific values remain in project-owned `CONFIG.yml`.

### 4.3 Control-history modes and Git contexts

Support exactly:

```text
single-repo
split-control
local-only
```

- `single-repo` may track project-owned Planning state in product Git.
- `split-control` keeps `.planning` as the control work tree, uses a
  `.planning/.git` gitfile, and stores its Git metadata outside both product and
  Planning roots under `<home>/control/<project-id>.git`.
- `local-only` requires no control Git and does not make a false history claim.

Every Git-sensitive operation must select an explicit product or control context.
It must not infer the repository merely from current working directory. Product
and control HEAD/status/dirt remain independently addressable.

Topology creation and update must preserve project-owned files and topology
metadata, avoid `.git` traversal and root escape, and perform no automatic Git
history operation or product `.gitignore` edit.

### 4.4 Doctor, update, and source rebind

Doctor and update must recognize all three modes without confusing product and
control repositories. Existing Copier ownership and local-only preservation
semantics remain authoritative.

An update-source change is explicit. A migration may rebind only through the
accepted explicit source override/repair path; successful rebind must update the
rendered installer metadata. No silent source rebind is allowed, and existing
source-precedence tests remain owners of that invariant.

### 4.5 Product/control linkage policy

Ordinary product commit messages require no Planning vocabulary. A Change may
record zero, one, or many product and control commit SHAs. A public changelog
reference to a Planning Change ID is optional. No hook or automatic changelog
generation is introduced.

### 4.6 Raw externally-fed telemetry

`RunReceipt v1` is an append-only, externally supplied raw receipt stored at:

```text
<home>/telemetry/<project-id>/run-receipts.jsonl
```

Collection validates the exact schema in the Implementation Start Contract. It
does not invoke a model/runtime and does not infer model, token, cost, or other
runtime facts. Required-but-unknown facts remain present as `null`/`unavailable`
with their provenance. Registry entries and receipts are not semantic memory
authorities, analytics, or interpreted evaluation conclusions.

## 5. In scope

This Change contains one integrated foundation, not separate registry, Git, and
telemetry Changes:

- extension of the existing Planning Lite home;
- topology-only project registry;
- extension of existing `CONFIG.yml`/defaults/project-rules policy authority;
- `single-repo`, `split-control`, and `local-only` modes;
- explicit product/control Git contexts;
- external split-control gitdir plus `.planning/.git` gitfile;
- Doctor and update compatibility;
- explicit update-source rebind required for migration safety;
- product commit/control commit/public changelog linkage policy;
- raw externally-fed `RunReceipt v1`;
- disposable Poker brownfield migration proof;
- disposable mood unborn/early-adoption migration proof;
- central completion verification.

The expected product write surface and its exact file-level constraints are
owned by Section 8 of the Implementation Start Contract. Any expansion beyond
that surface requires Definition amendment before implementation.

## 6. Explicitly out of scope

- semantic memory or a new memory authority;
- context retrieval or compilation;
- handoff redesign beyond the linkage fields strictly needed by 05-C;
- model routing or model-tier selection;
- agent scheduling;
- skills or checklists implementation;
- Pre-Readiness Closure Sweep implementation;
- task-verifier baseline implementation;
- governed exception/failure lifecycle work;
- analytics, dashboarding, metric interpretation, or recommendation semantic
  aggregation;
- daemon, service, or database;
- remote backup or sync;
- secret-management subsystem;
- automatic product `.gitignore` edits;
- automatic Git add, commit, tag, push, merge, rebase, reset, clean, or stash;
- live Poker migration;
- live mood migration;
- release.

## 7. Frozen invariants

### Roadmap invariant

No new major Roadmap phase is created. After 05-C the next major block remains
`PL-V39-06`. This Definition does not edit or replace the canonical Roadmap.

### Reuse invariant

Reuse existing `.planning`, `.agents`, Copier ownership/update behavior,
`CONFIG.yml`, defaults, and project-rule/instruction authorities. Do not create a
parallel project-policy authority.

### Home invariant

Reuse and extend the existing Planning Lite config-home seam. Do not create a
second Planning Lite source/control product.

### Memory invariant

The registry and receipts are locator/raw-evidence surfaces, not semantic memory
or direction authorities.

### Telemetry invariant

Unknown runtime facts stay `null`/`unavailable`. Model/token/cost facts are never
inferred from adapters, filenames, defaults, or surrounding context.

### Consumer invariant

Central implementation mutates no live Poker or mood checkout. Only disposable
byte/snapshot fixtures are part of this Change. Any live migration is a later
owner decision.

### Ownership and update invariant

Project-owned goals, plans, recommendations, decisions, active state,
configuration overrides, and completed work records remain byte-preserved except
for narrowly and explicitly initialized topology keys in a disposable proof.

### Git safety invariant

Product and control roots are explicit and non-overlapping. Scans do not descend
into `.git` directories or escape through links/reparse points. No Planning Lite
command in this Change performs a Git history operation.

### Expansion invariant

Newly discovered useful mechanisms route to recommendations/backlog unless they
strictly block an already approved 05-C acceptance criterion. They do not expand
this Change by convenience.

## 8. Acceptance boundary

The Change may be considered complete only when all of the following are proven:

1. Home resolution, project-policy merge/validation, and topology-only registry
   behavior are deterministic, bounded, and backward-compatible.
2. All three control-history modes work with explicit product/control contexts;
   split-control uses an external gitdir and `.planning/.git` gitfile, and no
   operation silently mutates Git history or product ignore policy.
3. Doctor and update select the correct topology, preserve project-owned bytes
   and topology metadata, avoid Git internals/root escapes, and remain idempotent.
4. An update source changes only through explicit rebind and installer metadata
   records the selected source without changing established precedence silently.
5. Product/control SHA linkage and optional public changelog linkage work without
   requiring Change IDs in ordinary product commits.
6. `RunReceipt v1` validates and appends exact externally supplied raw records;
   nullable unknowns and provenance are preserved, corruption fails closed, and
   no runtime fact is inferred.
7. Registry/receipt schemas contain no secret fields and control Git is explicitly
   documented as not being a secret store.
8. Disposable Poker and mood proofs satisfy their distinct migration/adoption
   contracts from the Implementation Start Contract without changing either live
   checkout.
9. Focused owner tests, central ownership/write-boundary checks, `uv sync`, the
   full test suite, clean temporary adoption, consumer Doctor, and applicable
   update smoke evidence pass at the completion gate.
10. No out-of-scope feature, parallel authority, new major Roadmap phase, or
    material unresolved product defect remains in the candidate.

Exact test selection, task sequencing, and intermediate gates remain Plan-owned.
The accepted T-01 through T-09 contract is referenced, not duplicated.

## 9. Authorization boundaries

The owner explicitly approved this Definition in its current draft revision on
`2026-09-03`. Canonical central activation is recorded separately; approval of
the Definition permits Plan preparation only.

```text
Change Definition: APPROVED
Central active Change: YES, through the canonical activation receipt
Plan preparation: AUTHORIZED
Plan approval: NOT GRANTED
Implementation: NOT AUTHORIZED
Poker live migration: NOT AUTHORIZED
mood live migration: NOT AUTHORIZED
Commit/tag/push/merge/release: NOT AUTHORIZED
```

The canonical activation updates `CURRENT.md` only to the Planning boundary.
Neither Definition approval nor activation authorizes product/template/test
implementation.

## 10. Definition verdict and next gate

```text
PL_V39_05_C_CHANGE_DEFINITION: APPROVED
next gate: prepare and obtain owner approval of the bounded Plan
```

After the bounded Plan is prepared, stop for owner approval. Do not begin
implementation automatically.

## Owner approval record

```text
Approval authority: USER / EXPLICIT
Approval date: 2026-09-03
Approved source draft SHA256:
2b8f6b910cd6079fa0d3a7e86cf919e471ad70d526a57531890452d538296597

Definition: APPROVED
Plan preparation: AUTHORIZED
Implementation: NOT AUTHORIZED
Live Poker/mood migration: NOT AUTHORIZED
Commit/tag/push/merge/release: NOT AUTHORIZED
```
