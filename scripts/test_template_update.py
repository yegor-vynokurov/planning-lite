"""Manual end-to-end smoke test for maintainers.

This script creates a temporary Git repository, adopts the current central
repository HEAD, and verifies the installation. Run it from a clean,
Git-versioned central repository before creating a release tag.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    central = Path.cwd().resolve()
    if not (central / "copier.yml").exists() or not (central / ".git").exists():
        raise SystemExit("Run from a Git-versioned Planning Lite central repository.")

    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary)
        run("git", "init", cwd=target)
        run("git", "config", "user.email", "planning-lite@example.invalid", cwd=target)
        run("git", "config", "user.name", "Planning Lite Test", cwd=target)
        (target / "README.md").write_text("# Smoke target\n", encoding="utf-8")
        run("git", "add", ".", cwd=target)
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
            "HEAD",
        )
        run("uv", "run", "planning-lite", "doctor", str(target), cwd=central)
        print("Planning Lite smoke test passed.")


if __name__ == "__main__":
    main()
