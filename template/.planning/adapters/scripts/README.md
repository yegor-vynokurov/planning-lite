# Adapter materializer

The script creates repository-local thin wrappers from canonical skills:

```bash
python .planning/adapters/scripts/materialize_adapter.py codex --dry-run
python .planning/adapters/scripts/materialize_adapter.py claude-code --dry-run
python .planning/adapters/scripts/materialize_adapter.py claude-code
python .planning/adapters/scripts/materialize_adapter.py hermes
```

Safety properties:

- does not install or launch an agent;
- does not modify project plans or code;
- does not modify user-level Hermes config;
- skips existing files unless `--force` is explicitly supplied;
- canonical skill bodies remain under `.planning/skills/`.

Run from the project root or pass `--root`.
