from __future__ import annotations

import argparse
from pathlib import Path

SKILLS = (
    "planning-audit",
    "planning-checkpoint",
    "planning-dialogue",
    "planning-execute",
    "planning-git-review",
    "planning-plan",
    "planning-quick-fix",
    "planning-recover",
)


def write_wrapper(path: Path, skill: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {skill}\ndescription: Thin wrapper for canonical Planning Lite skill.\n---\n\n"
        f"Read and follow `.planning/skills/{skill}/SKILL.md` as the authoritative workflow.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--agent", choices=("codex", "claude-code"), required=True)
    args = parser.parse_args()

    root = Path(args.target).resolve()
    base = root / (".agents/skills" if args.agent == "codex" else ".claude/skills")
    for skill in SKILLS:
        write_wrapper(base / skill / "SKILL.md", skill)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
