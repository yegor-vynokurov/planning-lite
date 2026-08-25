# Project Spine / Planning Lite development design

**Start here:** `CURRENT.md`

This directory is the tracked development/design control area for Planning Lite
itself. It is separate from the `.planning/` structure installed into consumer
projects.

## Stable layout

```text
project-spine/
├── CURRENT.md
├── roadmap/
│   ├── ROADMAP.md
│   └── archive/
├── recommendations/
│   ├── inbox/
│   ├── active/
│   ├── FUTURE-RESERVE.md
│   └── archive/
├── discoveries/
│   ├── INDEX.md
│   ├── TEMPLATE.md
│   ├── items/
│   └── archive/
├── governance/
│   └── RECOMMENDATION-ABSORPTION.md
└── support/
    ├── code-seeds/
    ├── playbooks/
    ├── field-evidence/
    ├── reviews/
    ├── research/
    └── checkpoints/
```

## Authority

```text
CURRENT.md
→ navigation/current checkpoint

roadmap/ROADMAP.md
→ current development Roadmap

recommendations/FUTURE-RESERVE.md
→ deferred residue, no scheduling authority

recommendations/inbox/ + active/
→ recommendation intake/reconciliation

discoveries/
→ observations/facts, not proposed work

governance/
→ rules for intake/absorption

support/
→ evidence and reusable assets, not direction authority
```

## Important distinctions

```text
Discovery != Recommendation
Recommendation != Roadmap item
Future Reserve != second Roadmap
Contingency Route != active Roadmap
design baseline != released product behavior
archive != forgotten
```

## Historical compatibility

`PL-V38-CURRENT.md` remains at its previous path because maintainer verification
and current field operations still reference it.

Other versioned design sources were moved into semantic archive/support
locations. Normal work should use stable paths above rather than search by the
largest version number in the directory.

## Lab boundary

`.planning-lab/` remains non-canonical experimental/research state. Historical
files there may be referenced as evidence, but new current development Roadmaps,
Discoveries, and Recommendations should use this tracked structure.

<!-- PL_PROJECT_SPINE_RESUME_AUTHORITY_V1:BEGIN -->
## Central resume authority

For a new chat, new agent, or returning maintainer, start with:

```text
docs/design/project-spine/CURRENT.md
```

`CURRENT.md` contains the canonical semantic Resume Contract. Live repository
facts such as Git root, branch, HEAD, `origin/main`, ahead/behind, and working
tree status are derived by:

```text
scripts/maintainer_resume.py
```

Do not infer current authority from similarly named historical files.
`PL-V38-CURRENT.md` is a legacy checkpoint, Roadmap archives are historical,
`support/**` is evidence, and `.planning-lab/**` is non-canonical research state.
<!-- PL_PROJECT_SPINE_RESUME_AUTHORITY_V1:END -->
