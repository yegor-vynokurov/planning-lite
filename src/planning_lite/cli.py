from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path
from typing import Iterable

import yaml
from packaging.version import InvalidVersion, Version

from . import __version__

ANSWERS_FILE = ".copier-answers.planning-lite.yml"
CONFIG_ENV = "PLANNING_LITE_TEMPLATE"
CONFIG_PATH = Path.home() / ".config" / "planning-lite" / "config.toml"
DEFAULT_TEMPLATE_SOURCE = "https://github.com/yegor-vynokurov/planning-lite"
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

    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if _looks_like_template_repo(candidate):
            return str(candidate)

    configured = _load_user_config().get("template_source")
    if isinstance(configured, str) and configured.strip():
        return configured.strip()

    return DEFAULT_TEMPLATE_SOURCE


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
    print(f"Saved template source override in {CONFIG_PATH}: {args.template_source}")
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


def _version_from_tag(tag: str) -> Version:
    raw = tag.strip()
    if raw.startswith("v"):
        raw = raw[1:]
    try:
        parsed = Version(raw)
    except InvalidVersion as exc:
        raise PlanningLiteError(f"Invalid PEP 440 version tag: {tag}") from exc
    return parsed


def _is_stable_release(version: Version) -> bool:
    return (
        version.epoch == 0
        and len(version.release) == 3
        and not version.is_prerelease
        and not version.is_devrelease
        and not version.is_postrelease
        and version.local is None
    )


def _latest_release_version(target: Path) -> Version:
    output = _git_output(target, "tag", "--list")
    if output is None:
        raise PlanningLiteError("Cannot read Git tags.")

    versions: list[Version] = []
    for tag in output.splitlines():
        try:
            parsed = _version_from_tag(tag)
        except PlanningLiteError:
            continue
        if _is_stable_release(parsed):
            versions.append(parsed)

    if not versions:
        raise PlanningLiteError(
            "No stable release tag was found. Create an initial tag such as v3.0.0 first."
        )
    return max(versions)


def _next_release_version(current: Version, requested: str) -> Version:
    normalized = requested.strip().lower()
    major, minor, patch = current.release
    if normalized == "patch":
        candidate = Version(f"{major}.{minor}.{patch + 1}")
    elif normalized == "minor":
        candidate = Version(f"{major}.{minor + 1}.0")
    elif normalized == "major":
        candidate = Version(f"{major + 1}.0.0")
    else:
        candidate = _version_from_tag(requested)

    if not _is_stable_release(candidate):
        raise PlanningLiteError(
            "Release versions must contain exactly MAJOR.MINOR.PATCH and must not be "
            "pre-, dev-, post-, local-, or epoch versions."
        )
    if candidate <= current:
        raise PlanningLiteError(
            f"Requested version {candidate} must be greater than the latest release {current}."
        )
    return candidate


def _render_released_changelog(text: str, version: Version, *, released_on: date) -> str:
    marker = "## Unreleased"
    marker_index = text.find(marker)
    if marker_index < 0:
        raise PlanningLiteError("CHANGELOG.md must contain a `## Unreleased` section.")

    content_start = marker_index + len(marker)
    next_heading = re.search(r"(?m)^##\s+", text[content_start:])
    content_end = content_start + next_heading.start() if next_heading else len(text)
    unreleased = text[content_start:content_end].strip()
    if not re.search(r"(?m)^-\s+\S", unreleased):
        raise PlanningLiteError(
            "The `## Unreleased` section must contain at least one bullet before release."
        )

    before = text[:marker_index]
    after = text[content_end:].lstrip("\n")
    released = (
        f"## Unreleased\n\n"
        f"## {version} - {released_on.isoformat()}\n\n"
        f"{unreleased}\n"
    )
    if after:
        released += f"\n{after}"
    return before + released


def _validate_release_lockfile(target: Path) -> None:
    lockfile = target / "uv.lock"
    if not lockfile.exists():
        raise PlanningLiteError(
            "uv.lock is missing. Run `uv lock --default-index https://pypi.org/simple` "
            "and commit the lockfile before releasing."
        )
    text = lockfile.read_text(encoding="utf-8")
    forbidden = (
        "packages.applied-caas-gateway1.internal.api.openai.org",
        "applied-caas-gateway",
    )
    found = [value for value in forbidden if value in text]
    if found:
        raise PlanningLiteError(
            "uv.lock contains an environment-specific package index. Regenerate it from "
            "the intended index before releasing."
        )


def command_release(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not _looks_like_template_repo(target):
        raise PlanningLiteError(
            f"{target} does not look like the central Planning Lite template repository."
        )
    _require_clean_git(target, allow_dirty=False)

    branch = _git_output(target, "branch", "--show-current")
    if not branch:
        raise PlanningLiteError("Release cannot run from a detached HEAD.")
    if branch != args.branch and not args.allow_other_branch:
        raise PlanningLiteError(
            f"Release must run from `{args.branch}`; current branch is `{branch}`. "
            "Pass --allow-other-branch only when this is intentional."
        )

    current = _latest_release_version(target)
    version = _next_release_version(current, args.version)
    tag = f"v{version}"
    if _git_output(target, "tag", "--list", tag):
        raise PlanningLiteError(f"Tag already exists: {tag}")

    changelog_path = target / "CHANGELOG.md"
    if not changelog_path.exists():
        raise PlanningLiteError("CHANGELOG.md is missing.")
    changelog = _render_released_changelog(
        changelog_path.read_text(encoding="utf-8"),
        version,
        released_on=date.today(),
    )
    _validate_release_lockfile(target)

    print(f"Latest release: v{current}")
    print(f"Planned release: {tag}")
    if args.dry_run:
        print("Dry run: tests, changelog update, release commit, and tag creation were skipped.")
        return 0

    if not args.skip_tests:
        if shutil.which("uv") is None:
            raise PlanningLiteError(
                "The release workflow requires `uv` for lock validation and the template smoke test."
            )
        checks = [
            ["uv", "lock", "--check"],
            [sys.executable, "-m", "pytest"],
        ]
        template_test = target / "scripts" / "test_template_update.py"
        if template_test.exists():
            checks.append([sys.executable, str(template_test)])
        for command in checks:
            if _run(command, cwd=target) != 0:
                raise PlanningLiteError(
                    f"Release check failed: {' '.join(command)}. No release tag was created."
                )
        if _is_dirty(target):
            raise PlanningLiteError(
                "Release checks modified the working tree. Review and commit or remove those "
                "changes before retrying; no release tag was created."
            )

    changelog_path.write_text(changelog, encoding="utf-8")
    if _run(["git", "add", "CHANGELOG.md"], cwd=target) != 0:
        raise PlanningLiteError("Cannot stage CHANGELOG.md.")
    message = args.message or f"Release {tag}"
    if _run(["git", "commit", "-m", message], cwd=target) != 0:
        _run(["git", "restore", "--staged", "CHANGELOG.md"], cwd=target)
        _run(["git", "restore", "CHANGELOG.md"], cwd=target)
        raise PlanningLiteError("Cannot create the release commit. CHANGELOG.md was restored.")
    if _run(["git", "tag", "-a", tag, "-m", message], cwd=target) != 0:
        raise PlanningLiteError(
            "The release commit was created, but tag creation failed. Inspect Git state before retrying."
        )

    print(f"Created release commit and annotated tag {tag}.")
    print("Nothing was pushed automatically.")
    print("Next:")
    print(f"  git push origin {branch}")
    print(f"  git push origin {tag}")
    return 0


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
    answers_data: dict[str, object] | None = None
    if answers.exists():
        try:
            data = _load_yaml(answers)
            if not isinstance(data, dict) or "_src_path" not in data:
                failures.append(f"{ANSWERS_FILE} is not a valid Copier answers file")
            else:
                answers_data = data
        except (OSError, yaml.YAMLError) as exc:
            failures.append(f"cannot parse {ANSWERS_FILE}: {exc}")

    unrendered = list(target.rglob("*.jinja"))
    if unrendered:
        failures.append(f"unrendered template files found: {len(unrendered)}")

    if not _is_git_repo(target):
        warnings.append("target is not a Git repository")
    elif _is_dirty(target):
        warnings.append("working tree is not clean")

    installed_ref = "unknown"
    if answers_data is not None:
        raw_ref = answers_data.get("_commit") or answers_data.get("_vcs_ref")
        if isinstance(raw_ref, str) and raw_ref.strip():
            installed_ref = raw_ref.strip()
    print(f"Planning Lite framework version: {installed_ref}")

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

    configure = subparsers.add_parser(
        "configure",
        help="Override the built-in central template source for this user.",
    )
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

    release = subparsers.add_parser(
        "release",
        help="Run release checks, finalize CHANGELOG.md, commit, and create a version tag.",
    )
    release.add_argument(
        "version",
        help="One of patch, minor, major, or an explicit MAJOR.MINOR.PATCH version.",
    )
    release.add_argument("--target", default=".", help="Central Planning Lite repository root.")
    release.add_argument("--branch", default="main", help="Expected release branch.")
    release.add_argument("--allow-other-branch", action="store_true")
    release.add_argument("--skip-tests", action="store_true")
    release.add_argument("--dry-run", action="store_true")
    release.add_argument("--message", help="Release commit and annotated tag message.")
    release.set_defaults(func=command_release)

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
