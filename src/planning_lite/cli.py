from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Iterable

import yaml

from . import __version__

ANSWERS_FILE = ".copier-answers.planning-lite.yml"
CONFIG_ENV = "PLANNING_LITE_TEMPLATE"
CONFIG_PATH = Path.home() / ".config" / "planning-lite" / "config.toml"
BRIDGE_START = "<!-- planning-lite:start -->"
BRIDGE_END = "<!-- planning-lite:end -->"
BRIDGE_BLOCK = f"""{BRIDGE_START}
This repository uses Planning Lite.

Before acting, read and follow `.planning/control/ROOT_ROUTER.md`.
Also read `.planning/project/PROJECT_INSTRUCTIONS.md` when repository-specific rules are relevant.
Do not preload the entire `.planning/` tree.
{BRIDGE_END}"""


class PlanningLiteError(RuntimeError):
    """User-facing command failure."""


def _run(command: list[str], *, cwd: Path | None = None) -> int:
    completed = subprocess.run(command, cwd=cwd, check=False)
    return completed.returncode


def _git_output(target: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(target), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _is_git_repo(target: Path) -> bool:
    return _git_output(target, "rev-parse", "--show-toplevel") is not None


def _is_dirty(target: Path) -> bool:
    output = _git_output(target, "status", "--porcelain")
    return bool(output)


def _load_user_config() -> dict[str, object]:
    if not CONFIG_PATH.exists():
        return {}
    try:
        with CONFIG_PATH.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise PlanningLiteError(f"Cannot read {CONFIG_PATH}: {exc}") from exc


def _save_template_source(source: str) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    escaped = source.replace("\\", "\\\\").replace('"', '\\"')
    CONFIG_PATH.write_text(
        "# Planning Lite user configuration\n"
        f'template_source = "{escaped}"\n',
        encoding="utf-8",
    )


def _looks_like_template_repo(path: Path) -> bool:
    return (path / "copier.yml").is_file() and (path / "template").is_dir()


def _discover_template_source(explicit: str | None) -> str:
    if explicit:
        return explicit

    environment = os.environ.get(CONFIG_ENV)
    if environment:
        return environment

    configured = _load_user_config().get("template_source")
    if isinstance(configured, str) and configured.strip():
        return configured.strip()

    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if _looks_like_template_repo(candidate):
            return str(candidate)

    raise PlanningLiteError(
        "Template source is not configured. Pass --template-source, set "
        f"{CONFIG_ENV}, or run `planning-lite configure --template-source <path-or-git-url>`."
    )


def _copier_command(*args: str) -> list[str]:
    return [sys.executable, "-m", "copier", *args]


def _ensure_agents_bridge(target: Path) -> str:
    agents = target / "AGENTS.md"
    if not agents.exists():
        agents.write_text(
            "# Repository agent instructions\n\n"
            + BRIDGE_BLOCK
            + "\n\n## Project-specific additions\n",
            encoding="utf-8",
        )
        return "created"

    content = agents.read_text(encoding="utf-8")
    if BRIDGE_START in content:
        return "already-present"

    separator = "" if content.endswith("\n") else "\n"
    agents.write_text(
        content
        + separator
        + "\n"
        + BRIDGE_BLOCK
        + "\n",
        encoding="utf-8",
    )
    return "appended"


def _require_clean_git(target: Path, allow_dirty: bool) -> None:
    if not _is_git_repo(target):
        raise PlanningLiteError(
            f"{target} is not a Git repository. Initialize Git before adopting or updating Planning Lite."
        )
    if not allow_dirty and _is_dirty(target):
        raise PlanningLiteError(
            "The target repository has uncommitted changes. Commit or stash them first, "
            "or pass --allow-dirty for an intentional initial adoption."
        )


def command_configure(args: argparse.Namespace) -> int:
    _save_template_source(args.template_source)
    print(f"Saved template source in {CONFIG_PATH}: {args.template_source}")
    return 0


def command_adopt(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not target.exists() or not target.is_dir():
        raise PlanningLiteError(f"Target directory does not exist: {target}")

    _require_clean_git(target, args.allow_dirty)
    source = _discover_template_source(args.template_source)
    project_name = args.project_name or target.name

    command = _copier_command(
        "copy",
        "--defaults",
        "--answers-file",
        ANSWERS_FILE,
        "--data",
        f"project_name={project_name}",
        "--data",
        f"agent_adapter={args.agent}",
    )
    if args.vcs_ref:
        command.extend(["--vcs-ref", args.vcs_ref])
    command.extend([source, str(target)])

    code = _run(command)
    if code != 0:
        return code

    bridge_result = _ensure_agents_bridge(target)
    print(f"AGENTS.md bridge: {bridge_result}")
    print("Next: review `git status`, run `planning-lite doctor .`, and commit the adoption separately.")
    return 0


def command_update(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    _require_clean_git(target, args.allow_dirty)
    answers = target / ANSWERS_FILE
    if not answers.exists():
        raise PlanningLiteError(
            f"{ANSWERS_FILE} is missing. Adopt Planning Lite before running an update."
        )

    command = _copier_command(
        "update",
        "--answers-file",
        ANSWERS_FILE,
        "--skip-answered",
    )
    if args.dry_run:
        command.append("--pretend")
    if args.vcs_ref:
        command.extend(["--vcs-ref", args.vcs_ref])

    return _run(command, cwd=target)


def _load_yaml(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _iter_required_paths() -> Iterable[str]:
    return (
        "AGENTS.md",
        ANSWERS_FILE,
        ".planning/ACTIVE.md",
        ".planning/CONFIG.yml",
        ".planning/AGENT_PROFILE.yml",
        ".planning/control/ROOT_ROUTER.md",
        ".planning/control/CONFIG_RESOLUTION.md",
        ".planning/framework/defaults.yml",
        ".planning/framework/OWNERSHIP.yml",
        ".planning/project/PROJECT_CHARTER.md",
        ".planning/project/PROJECT_INSTRUCTIONS.md",
        ".planning/skills/planning-checkpoint/SKILL.md",
    )


def command_doctor(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    failures: list[str] = []
    warnings: list[str] = []

    for relative in _iter_required_paths():
        if not (target / relative).exists():
            failures.append(f"missing: {relative}")

    agents = target / "AGENTS.md"
    if agents.exists() and BRIDGE_START not in agents.read_text(encoding="utf-8"):
        failures.append("AGENTS.md does not contain the Planning Lite bridge block")

    answers = target / ANSWERS_FILE
    if answers.exists():
        try:
            data = _load_yaml(answers)
            if not isinstance(data, dict) or "_src_path" not in data:
                failures.append(f"{ANSWERS_FILE} is not a valid Copier answers file")
        except (OSError, yaml.YAMLError) as exc:
            failures.append(f"cannot parse {ANSWERS_FILE}: {exc}")

    unrendered = list(target.rglob("*.jinja"))
    if unrendered:
        failures.append(f"unrendered template files found: {len(unrendered)}")

    if not _is_git_repo(target):
        warnings.append("target is not a Git repository")
    elif _is_dirty(target):
        warnings.append("working tree is not clean")

    version_path = target / ".planning" / "VERSION"
    version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else "unknown"
    print(f"Planning Lite framework version: {version}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for failure in failures:
        print(f"ERROR: {failure}")

    if failures:
        return 1
    print("Doctor: OK")
    return 0


def command_ownership(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    ownership = target / ".planning" / "framework" / "OWNERSHIP.yml"
    if not ownership.exists():
        raise PlanningLiteError(f"Ownership manifest not found: {ownership}")
    print(ownership.read_text(encoding="utf-8"), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="planning-lite",
        description="Adopt and update the Planning Lite repository workflow.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser("configure", help="Store the central template source.")
    configure.add_argument("--template-source", required=True)
    configure.set_defaults(func=command_configure)

    adopt = subparsers.add_parser("adopt", help="Install Planning Lite into an existing Git repository.")
    adopt.add_argument("target", nargs="?", default=".")
    adopt.add_argument("--template-source")
    adopt.add_argument("--vcs-ref", help="Git tag, branch, or commit of the central template.")
    adopt.add_argument("--project-name")
    adopt.add_argument(
        "--agent",
        default="codex",
        choices=("codex", "claude-code", "hermes", "generic"),
    )
    adopt.add_argument("--allow-dirty", action="store_true")
    adopt.set_defaults(func=command_adopt)

    update = subparsers.add_parser("update", help="Update managed files from the central template.")
    update.add_argument("target", nargs="?", default=".")
    update.add_argument("--vcs-ref")
    update.add_argument("--dry-run", action="store_true")
    update.add_argument("--allow-dirty", action="store_true")
    update.set_defaults(func=command_update)

    check = subparsers.add_parser("check", help="Preview a Planning Lite update without writing files.")
    check.add_argument("target", nargs="?", default=".")
    check.add_argument("--vcs-ref")
    check.add_argument("--allow-dirty", action="store_true")
    check.set_defaults(func=command_update, dry_run=True)

    doctor = subparsers.add_parser("doctor", help="Validate a Planning Lite installation.")
    doctor.add_argument("target", nargs="?", default=".")
    doctor.set_defaults(func=command_doctor)

    ownership = subparsers.add_parser("ownership", help="Show managed and project-owned path policies.")
    ownership.add_argument("target", nargs="?", default=".")
    ownership.set_defaults(func=command_ownership)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except PlanningLiteError as exc:
        print(f"planning-lite: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
