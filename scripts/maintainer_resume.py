#!/usr/bin/env python3
"""Read-only central-repository resume helper for Planning Lite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BEGIN = "<!-- PLANNING_LITE_RESUME_CONTRACT_V1:BEGIN -->"
END = "<!-- PLANNING_LITE_RESUME_CONTRACT_V1:END -->"
CURRENT_REL = "docs/design/project-spine/CURRENT.md"
ROADMAP_REL = "docs/design/project-spine/roadmap/ROADMAP.md"

REQUIRED_KEYS = (
    "repository_role",
    "resume_authority",
    "current_roadmap",
    "active_change",
    "lifecycle_gate",
    "implementation_authorized",
    "blockers",
    "next_permitted_action",
    "last_transition_receipt",
    "state_as_of",
)

class ResumeError(RuntimeError):
    pass

def _git(start: Path, *args: str):
    return subprocess.run(
        ["git", "-C", str(start), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

def resolve_git_root(start: Path) -> Path:
    p = _git(start, "rev-parse", "--show-toplevel")
    if p.returncode != 0 or not p.stdout.strip():
        raise ResumeError("NOT A VERIFIED CENTRAL GIT CHECKOUT")
    return Path(p.stdout.strip()).resolve()

def parse_resume_block(text: str) -> dict[str, str]:
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ResumeError("Resume Contract v1 block must occur exactly once")
    start = text.index(BEGIN) + len(BEGIN)
    finish = text.index(END, start)
    body = text[start:finish].strip()
    data: dict[str, str] = {}
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if ":" not in line:
            raise ResumeError(f"Malformed Resume Contract line: {raw}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in data:
            raise ResumeError(f"Duplicate Resume Contract key: {key}")
        if not key or not value:
            raise ResumeError(f"Empty Resume Contract key/value: {raw}")
        data[key] = value
    missing = [k for k in REQUIRED_KEYS if k not in data]
    extra = [k for k in data if k not in REQUIRED_KEYS]
    if missing:
        raise ResumeError("Missing Resume Contract keys: " + ", ".join(missing))
    if extra:
        raise ResumeError("Unknown Resume Contract keys: " + ", ".join(extra))
    if data["implementation_authorized"] not in {"YES", "NO"}:
        raise ResumeError("implementation_authorized must be YES or NO")
    return data

def _inside(root: Path, rel: str) -> Path:
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ResumeError(f"Authority path escapes repository: {rel}") from exc
    return candidate

def load_resume(root: Path) -> dict[str, str]:
    current = root / CURRENT_REL
    if not current.is_file():
        raise ResumeError(f"Missing resume authority: {CURRENT_REL}")
    data = parse_resume_block(current.read_text(encoding="utf-8-sig"))
    if data["repository_role"] != "CENTRAL_SOURCE":
        raise ResumeError("repository_role must be CENTRAL_SOURCE")
    if data["resume_authority"] != CURRENT_REL:
        raise ResumeError(f"resume_authority must be {CURRENT_REL}")
    if data["current_roadmap"] != ROADMAP_REL:
        raise ResumeError(f"current_roadmap must be {ROADMAP_REL}")
    for key in ("resume_authority", "current_roadmap"):
        p = _inside(root, data[key])
        if not p.is_file():
            raise ResumeError(f"Referenced {key} path missing: {data[key]}")
    receipt = data["last_transition_receipt"]
    if receipt != "NONE":
        p = _inside(root, receipt)
        if not p.is_file():
            raise ResumeError(f"Referenced last_transition_receipt missing: {receipt}")
    return data

def git_state(root: Path):
    branch = _git(root, "branch", "--show-current")
    head = _git(root, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise ResumeError("Git checkout has no resolvable HEAD")
    branch_text = branch.stdout.strip() if branch.returncode == 0 else ""
    branch_text = branch_text or "<DETACHED>"
    head_text = head.stdout.strip()

    origin = _git(root, "rev-parse", "--verify", "refs/remotes/origin/main")
    origin_text = origin.stdout.strip() if origin.returncode == 0 else "UNAVAILABLE"
    ahead_behind = "UNAVAILABLE"
    if origin.returncode == 0:
        counts = _git(root, "rev-list", "--left-right", "--count", "origin/main...HEAD")
        if counts.returncode == 0:
            parts = counts.stdout.strip().split()
            if len(parts) == 2:
                behind, ahead = parts
                ahead_behind = f"+{ahead}/-{behind}"

    status = _git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if status.returncode != 0:
        raise ResumeError("Unable to read Git working-tree status")
    rows = [x for x in status.stdout.splitlines() if x.strip()]
    working = "CLEAN" if not rows else f"DIRTY({len(rows)})"
    return branch_text, head_text, origin_text, ahead_behind, working

def render(root: Path, data: dict[str, str]) -> str:
    branch, head, origin, ab, working = git_state(root)
    return "\n".join([
        "Planning Lite CENTRAL SOURCE RESUME",
        "",
        "Git root:", f"  {root}",
        "",
        "branch:", f"  {branch}",
        "",
        "HEAD:", f"  {head}",
        "",
        "origin/main:", f"  {origin}",
        "",
        "ahead/behind:", f"  {ab}",
        "",
        "working tree:", f"  {working}",
        "",
        "resume authority:", f"  {data['resume_authority']}",
        "",
        "current Roadmap:", f"  {data['current_roadmap']}",
        "",
        "active Change:", f"  {data['active_change']}",
        "",
        "lifecycle gate:", f"  {data['lifecycle_gate']}",
        "",
        "implementation authorized:", f"  {data['implementation_authorized']}",
        "",
        "blockers:", f"  {data['blockers']}",
        "",
        "next permitted action:", f"  {data['next_permitted_action']}",
        "",
        "last transition receipt:", f"  {data['last_transition_receipt']}",
        "",
        "state as of:", f"  {data['state_as_of']}",
        "",
        "non-authoritative for current direction:",
        "  .planning-lab/**",
        "  docs/design/project-spine/roadmap/archive/**",
        "  docs/design/project-spine/recommendations/archive/**",
        "  docs/design/project-spine/support/**",
    ])

def main() -> int:
    try:
        script_root = Path(__file__).resolve().parents[1]
        root = resolve_git_root(script_root)
        if root != script_root:
            raise ResumeError(
                f"Helper location is not the Git root scripts directory: resolved {root}"
            )
        data = load_resume(root)
        print(render(root, data))
        return 0
    except ResumeError as exc:
        print(f"Planning Lite resume: BLOCKED\n{exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
