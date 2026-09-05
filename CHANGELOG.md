# Changelog

## Unreleased

- Add a bounded read-only consumer `planning-lite resume` projection with
  authority-first selection, exact expansion guards, freshness outcomes, and
  in-memory HandoffV1 validation; no context store or consumer writes are
  introduced.

- Add bounded project-policy, topology registry, explicit split-control Git
  contexts, topology-aware local updates, source rebind, and external RunReceipt
  v1 collection while preserving project-owned state and separate authorization
  gates.

- Add the Field Control Pack foundations: a non-executable Discovery lifecycle and durable registry; manual Recommendation Absorption with exhaustive residue accounting; conditional Contract Closure plus exhaustive Readiness and bounded Execution controls; managed Discovery README/TEMPLATE with project-owned INDEX/items preserved across updates; and deterministic foundation/integrity coverage. Independent Task Closure Review, user-invoked bounded CONVERGE, and controlled-realistic behavioral fixtures remain pilot-only pending bounded validation.

- Added a read-only central repository resume contract and maintainer helper that verifies Git identity, makes `CURRENT.md` the canonical session-handoff authority, fails closed for non-Git snapshots, and keeps consumer/runtime behavior unchanged.

- Add fail-closed ownership-aware updates for consumers that keep `.planning/` / `.agents/` Git-ignored, including file-level preview, atomic `--local-only` apply, project-owned hash preservation, and a v4.2.0 migration regression fixture.

- Clarified maintainer verification: central source repos use pytest + template-update smoke; `planning-lite doctor .` is consumer-only.

- Add Project Spine Roadmap outcome synthesis, credible-alternative qualitative prioritization, explicit human Roadmap acceptance, and exact Roadmap/Gap/Recommendation lineage handoff into bounded Change definition (`PW-DIR-007`), without auto-creating Changes or auto-closing outcomes/Gaps.
- Add Project Spine recommendation semantic-unit residue and historical Roadmap reconciliation (`PW-DIR-006`), preserving future/carry-forward meaning, separating lifecycle status from reconciliation state, and preventing completed Changes or historical ordering from silently collapsing current direction.
- Add Project Spine Current Capability Assessment and causal Gap derivation workflows, separating Coverage from EvidenceConfidence, preserving evidence uncertainty, and adding a project-owned Gap Map with human baseline authority.
- Add the first Project Spine Direction Foundation workflows, project-owned Target/Capability artifacts, stage-specific context rules, and Doctor coverage.

- Preserve the Project Spine v3.8.2 design track, including Poker-derived workflow commands and explicit reuse/ownership boundaries for `planning-lite-lab` and the Context Pilot/Eval Harness research assets.
- Add append-only reconciliation for legacy completed Campaign attempts that have sealed balanced-suite evidence but no native suite projection, without rewriting historical journal events or accounting.
- Add optional strict attempt budget admission so new governed attempts reserve projected token and wall-clock cost before `attempt_started`, while preserving backward compatibility for historical manifests and truthful sunk-cost completion.

## 4.3.0 - 2026-08-10

- Add the opt-in `planning-lite-campaign` CLI and `planning_lite.campaign` package for bounded experiment campaigns.
- Add immutable campaign manifests, frozen-input verification, append-only hash-linked journals, deterministic resume state, budgets, and stop gates.
- Bind balanced evaluation suites to campaign attempts with sealed evidence hashes and idempotent resume.
- Add deterministic candidate review, review receipts and handoff capsules, independent reviewer decisions, and tamper detection.
- Add campaign completion seals and bounded release handoffs while keeping release promotion explicitly separate.
- Keep the existing `planning-lite` CLI, Copier template, `AGENTS.md`, and target-project managed files unchanged.
- Bind `planning-lite-campaign --version` to the same Git-tag-derived Planning Lite distribution version.

## 4.2.0 - 2026-07-22

- state machine:

Discovery
→ Definition
→ Planning
→ Readiness
→ Execution
→ Verification
→ Closure

- every stage has:

Lifecycle stage
Stage status
Next gate
Next permitted action

- new chain of aproving:

proposal approved
→ plan drafted
→ plan approved
→ readiness audit
→ direct execution authorization

- also added
Facts vs Decisions в critic mode;
WAYFINDING.md for big tasks;
CODEBASE_DESIGN.md;
DELIVERY_SLICES.md;
DOMAIN_MODELING.md;
CODE_REVIEW.md;
tracer bullet, expand-contract, blocking edge, verification seam, blast radius;
separate runnings spec conformance and standards conformance;
prompt-quality checklist с completion criterion и no-op test;
new version of project glossary for canonical terms of the project (autho filling).

## 4.1.0 - 2026-07-20

- ready templates for all main actions.
- now agents may do not overwrite task.md or like document but go to templates and fill the template

## 4.0.0 - 2026-07-16

- big update to avoide duplications in the control prompts
- to clarify functional procedures for agents such as closure.

## 3.1.2 - 2026-07-15

- change cirillic symbols to eng descriptions

## 3.1.1 - 2026-07-14

- Add a caveman prompt parts to the control root_router.md as soft rules
- Add a caveman prompt parts to the skills depend role of the agent in the skill

## 3.1.0 - 2026-07-13

- Add a simple one-command installation mode using `uvx`.
- Add `planning-lite install` for users who only need repository-local agent prompts.
- Move persistent CLI installation and template updates to `docs/UPDATABLE_INSTALLATION.ru.md`.

## 3.0.3 - 2026-07-11

- Use the official GitHub repository as the built-in template source so new computers can run `adopt` immediately after installing the CLI.
- Keep `planning-lite configure` as an optional override for forks and local development copies.
- Add regression tests for template-source precedence and fallback behavior.

## 3.0.2 - 2026-07-11

- Derive package versions from Git tags through `hatch-vcs`.
- Add `planning-lite release` for checked patch, minor, major, and explicit releases.
- Read installed template versions from Copier metadata instead of `.planning/VERSION`.
- Add regression tests for package metadata, version duplication, release numbering, and changelog finalization.

## 3.0.0

- Converted Planning Lite into a centrally versioned Copier template.
- Added an install/update/doctor CLI.
- Split framework defaults from project overrides.
- Added explicit managed and project-owned path policies.
- Moved the full router into a managed control file while preserving project-local `AGENTS.md`.
