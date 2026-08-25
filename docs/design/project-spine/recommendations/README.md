# Planning Lite development recommendations

Stable structure:

```text
recommendations/
├── inbox/                 new/untriaged proposed actions
├── active/                accepted or actively reconciled, not yet absorbed
├── FUTURE-RESERVE.md      deferred residue + dormant contingency routes
└── archive/
    ├── absorbed/
    ├── superseded/
    └── rejected/
```

Rules:

- Discovery/fact records belong in `../discoveries/`.
- New recommendations may remain unanchored in `inbox/`.
- A recommendation does not become Roadmap work automatically.
- Absorption follows `../governance/RECOMMENDATION-ABSORPTION.md`.
- Fully absorbed source documents move to `archive/absorbed/`.
- Superseded documents are archived only after a residue check.
- `FUTURE-RESERVE.md` is not a second Roadmap and has no scheduling authority.
