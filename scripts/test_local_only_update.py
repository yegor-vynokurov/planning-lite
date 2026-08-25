"""End-to-end smoke for a v4.2.0 Git-ignored Planning Lite consumer.

Run from the central Planning Lite repository with dependencies installed:

    uv run python scripts/test_local_only_update.py

The smoke creates a temporary consumer, adopts the historical v4.2.0 template,
keeps `.planning` / `.agents` local-only, and updates it to current HEAD through
the ownership-aware updater.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

import yaml


V42_COMMIT = "bd8c422"


def run(*args: str, cwd: Path, capture: bool = False) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=capture,
        text=True,
    )
    return completed.stdout if capture else ""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_zero(plan: str, action: str) -> None:
    pattern = rf"(?m)^\s{{2}}{re.escape(action)}\s+0\s*$"
    if not re.search(pattern, plan):
        raise RuntimeError(f"Expected {action}=0 in local-only plan:\n{plan}")


def main() -> None:
    central = Path.cwd().resolve()
    if not (central / "copier.yml").is_file() or not (central / ".git").exists():
        raise SystemExit("Run from a Git-versioned Planning Lite central repository.")

    run("git", "cat-file", "-e", f"{V42_COMMIT}^{{commit}}", cwd=central)

    with tempfile.TemporaryDirectory(prefix="planning-lite-local-only-smoke-") as temporary:
        target = Path(temporary)
        run("git", "init", "-b", "main", cwd=target)
        run("git", "config", "user.email", "planning-lite@example.invalid", cwd=target)
        run("git", "config", "user.name", "Planning Lite Test", cwd=target)
        (target / "README.md").write_text("# Local-only smoke target\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=target)
        run("git", "commit", "-m", "Initial target", cwd=target)

        run(
            "uv",
            "run",
            "planning-lite",
            "adopt",
            str(target),
            "--template-source",
            str(central),
            "--vcs-ref",
            V42_COMMIT,
            cwd=central,
        )

        (target / ".gitignore").write_text(".planning\n.agents\n", encoding="utf-8")
        run("git", "add", ".gitignore", "AGENTS.md", ".copier-answers.planning-lite.yml", cwd=target)
        run("git", "commit", "-m", "Adopt Planning Lite v4.2.0 local-only", cwd=target)

        sentinels = {
            ".planning/ACTIVE.md": "SMOKE ACTIVE\n",
            ".planning/project/CURRENT_STATE.md": "SMOKE CURRENT STATE\n",
            ".planning/project/ROADMAP.md": "SMOKE ROADMAP\n",
            ".planning/recommendations/INDEX.md": "SMOKE RECOMMENDATIONS\n",
        }
        for relative, content in sentinels.items():
            (target / relative).write_text(content, encoding="utf-8")
        before = {relative: digest(target / relative) for relative in sentinels}

        status = run("git", "status", "--porcelain", cwd=target, capture=True).strip()
        if status:
            raise RuntimeError(f"Local-only smoke consumer must be Git-clean, got:\n{status}")

        preview = run(
            "uv",
            "run",
            "planning-lite",
            "check",
            str(target),
            "--vcs-ref",
            "HEAD",
            cwd=central,
            capture=True,
        )
        if "Detected local-only Planning Lite managed roots" not in preview:
            raise RuntimeError(f"Local-only mode was not detected:\n{preview}")
        require_zero(preview, "REMOVE_MANAGED")

        run(
            "uv",
            "run",
            "planning-lite",
            "update",
            str(target),
            "--vcs-ref",
            "HEAD",
            "--local-only",
            cwd=central,
        )
        run("uv", "run", "planning-lite", "doctor", str(target), cwd=central)

        for relative, expected in before.items():
            actual = digest(target / relative)
            if actual != expected:
                raise RuntimeError(f"Project-owned hash changed: {relative}")

        required = (
            ".planning/control/CHANGE_PLANNING.md",
            ".planning/framework/defaults.yml",
            ".agents/skills/planning-plan/SKILL.md",
            ".planning/control/DIRECTION_INVENTORY.md",
            ".planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md",
            ".planning/project/TARGET_STATE.md",
            ".planning/project/CAPABILITY_MODEL.md",
            ".planning/project/GAP_MAP.md",
        )
        missing = [relative for relative in required if not (target / relative).is_file()]
        if missing:
            raise RuntimeError("Missing expected post-update files: " + ", ".join(missing))

        answers = yaml.safe_load(
            (target / ".copier-answers.planning-lite.yml").read_text(encoding="utf-8")
        )
        if answers.get("_commit") in {None, "v4.2.0", V42_COMMIT}:
            raise RuntimeError("Installer metadata did not advance from v4.2.0")

        second = run(
            "uv",
            "run",
            "planning-lite",
            "check",
            str(target),
            "--vcs-ref",
            "HEAD",
            "--allow-dirty",
            cwd=central,
            capture=True,
        )
        for action in (
            "ADD_MANAGED",
            "UPDATE_MANAGED",
            "REMOVE_MANAGED",
            "ADD_PROJECT",
            "UPDATE_METADATA",
        ):
            require_zero(second, action)

        print("Planning Lite local-only v4.2.0 -> current smoke test passed.")


if __name__ == "__main__":
    main()
