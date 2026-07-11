#!/usr/bin/env python3
"""Materialize thin Planning Lite adapter files from canonical skills.

The script intentionally does not install clients, change user-level config, or
modify project planning state. It only creates repository-local adapter files.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillMeta:
    name: str
    description: str


def parse_skill_meta(skill_file: Path) -> SkillMeta:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter: {skill_file}")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"Malformed frontmatter: {skill_file}") from exc

    name_match = re.search(r"(?m)^name:\s*(.+?)\s*$", frontmatter)
    desc_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)
    if not name_match or not desc_match:
        raise ValueError(f"Missing name or description: {skill_file}")
    return SkillMeta(
        name=name_match.group(1).strip().strip('"\''),
        description=desc_match.group(1).strip().strip('"\''),
    )


def write_file(path: Path, content: str, *, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        print(f"SKIP existing: {path}")
        return
    print(f"WRITE: {path}")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def wrapper(meta: SkillMeta, adapter: str) -> str:
    return f'''---
name: {meta.name}
description: {meta.description}
metadata:
  adapter: {adapter}
  canonical-skill: .planning/skills/{meta.name}/SKILL.md
---

This is a thin {adapter} adapter. Read and follow `.planning/skills/{meta.name}/SKILL.md` as the authoritative workflow.

Do not duplicate or silently override the canonical instructions here. Client-specific behavior belongs under `.planning/adapters/{adapter}/`.
'''


def materialize_codex(root: Path, skills: list[SkillMeta], *, force: bool, dry_run: bool) -> None:
    target = root / ".agents" / "skills"
    for meta in skills:
        write_file(target / meta.name / "SKILL.md", wrapper(meta, "codex"), force=force, dry_run=dry_run)


def materialize_claude(root: Path, skills: list[SkillMeta], *, force: bool, dry_run: bool) -> None:
    claude_source = root / ".planning" / "adapters" / "claude-code" / "templates" / "CLAUDE.md"
    if not claude_source.exists():
        raise FileNotFoundError(f"Missing Claude template: {claude_source}")
    write_file(
        root / "CLAUDE.md",
        claude_source.read_text(encoding="utf-8"),
        force=force,
        dry_run=dry_run,
    )
    target = root / ".claude" / "skills"
    for meta in skills:
        write_file(target / meta.name / "SKILL.md", wrapper(meta, "claude-code"), force=force, dry_run=dry_run)


def show_hermes(root: Path) -> None:
    skills_dir = (root / ".planning" / "skills").resolve()
    print("Hermes should use the canonical skills directory directly.")
    print("Merge this into the active Hermes profile config:")
    print("skills:")
    print("  external_dirs:")
    print(f"    - {skills_dir}")
    print("No user-level Hermes configuration was modified.")


def discover_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".planning" / "skills").is_dir() and (candidate / "AGENTS.md").is_file():
            return candidate
    raise FileNotFoundError("Could not find a Planning Lite root containing AGENTS.md and .planning/skills/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=("codex", "claude-code", "hermes"))
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root or a path inside it")
    parser.add_argument("--force", action="store_true", help="Overwrite existing adapter files")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    try:
        root = discover_root(args.root)
        skill_files = sorted((root / ".planning" / "skills").glob("*/SKILL.md"))
        skills = [parse_skill_meta(path) for path in skill_files]
        if not skills:
            raise RuntimeError("No canonical skills found")

        if args.agent == "codex":
            materialize_codex(root, skills, force=args.force, dry_run=args.dry_run)
        elif args.agent == "claude-code":
            materialize_claude(root, skills, force=args.force, dry_run=args.dry_run)
        else:
            show_hermes(root)
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
