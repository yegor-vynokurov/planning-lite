from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
import hashlib
from pathlib import Path
import shutil
import tempfile
from typing import Iterable, Literal

import yaml

ANSWERS_FILE = ".copier-answers.planning-lite.yml"
OWNERSHIP_FILE = ".planning/framework/OWNERSHIP.yml"

OwnershipClass = Literal["managed", "project_owned", "installer_metadata", "unknown"]
Action = Literal[
    "ADD_MANAGED",
    "UPDATE_MANAGED",
    "REMOVE_MANAGED",
    "ADD_PROJECT",
    "KEEP_PROJECT",
    "UPDATE_METADATA",
    "KEEP_METADATA",
    "UNCHANGED_MANAGED",
]


@dataclass(frozen=True)
class OwnershipPolicy:
    managed: tuple[str, ...]
    project_owned: tuple[str, ...]
    installer_metadata: tuple[str, ...]


@dataclass(frozen=True)
class Mutation:
    action: Action
    path: str


@dataclass(frozen=True)
class LocalUpdatePlan:
    mutations: tuple[Mutation, ...]

    def changed(self) -> tuple[Mutation, ...]:
        return tuple(
            item
            for item in self.mutations
            if item.action
            not in {"KEEP_PROJECT", "KEEP_METADATA", "UNCHANGED_MANAGED"}
        )

    def count(self, action: Action) -> int:
        return sum(1 for item in self.mutations if item.action == action)


class LocalUpdateError(RuntimeError):
    """Fail-closed local-only update planning/apply failure."""


def _normalize(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _pattern_specificity(pattern: str) -> tuple[int, int, int]:
    """Prefer exact paths, then fewer wildcards, then longer patterns."""
    wildcard_count = pattern.count("*") + pattern.count("?") + pattern.count("[")
    exact = 1 if wildcard_count == 0 else 0
    return (exact, -wildcard_count, len(pattern))


def _best_match(path: str, patterns: Iterable[str]) -> str | None:
    matches = [pattern for pattern in patterns if fnmatchcase(path, pattern)]
    if not matches:
        return None
    return max(matches, key=_pattern_specificity)


def load_ownership_policy(root: Path) -> OwnershipPolicy:
    path = root / OWNERSHIP_FILE
    if not path.exists():
        raise LocalUpdateError(f"Ownership manifest not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise LocalUpdateError(f"Cannot parse ownership manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LocalUpdateError(f"Ownership manifest is not a mapping: {path}")

    values: dict[str, tuple[str, ...]] = {}
    for key in ("managed", "project_owned", "installer_metadata"):
        raw = data.get(key)
        if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
            raise LocalUpdateError(f"Ownership manifest field `{key}` must be a list of paths")
        values[key] = tuple(raw)
    return OwnershipPolicy(**values)


def classify_path(path: str, policy: OwnershipPolicy) -> OwnershipClass:
    normalized = _normalize(path)
    matches = {
        "managed": _best_match(normalized, policy.managed),
        "project_owned": _best_match(normalized, policy.project_owned),
        "installer_metadata": _best_match(normalized, policy.installer_metadata),
    }
    present = {key: value for key, value in matches.items() if value is not None}
    if not present:
        return "unknown"
    if len(present) == 1:
        return next(iter(present))  # type: ignore[return-value]

    # Installer metadata is always installer-owned when explicitly listed.
    if present.get("installer_metadata") is not None:
        return "installer_metadata"

    # Exact framework files beat broad project-owned globs. This allows a
    # reserved TEMPLATE.md to live inside an otherwise project-owned runtime dir.
    managed = present.get("managed")
    project = present.get("project_owned")
    if managed is not None and project is not None:
        if _pattern_specificity(managed) > _pattern_specificity(project):
            return "managed"
        if _pattern_specificity(project) > _pattern_specificity(managed):
            return "project_owned"

    raise LocalUpdateError(
        f"Ambiguous ownership for `{normalized}`: "
        + ", ".join(f"{key}={value}" for key, value in sorted(present.items()))
    )


def iter_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in root.rglob("*"):
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path
    return files


def _same_bytes(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    return hashlib.sha256(left.read_bytes()).digest() == hashlib.sha256(right.read_bytes()).digest()


def _classify_candidate(
    candidate_files: dict[str, Path],
    policy: OwnershipPolicy,
) -> dict[str, OwnershipClass]:
    classified: dict[str, OwnershipClass] = {}
    unknown: list[str] = []
    for relative in sorted(candidate_files):
        ownership = classify_path(relative, policy)
        classified[relative] = ownership
        if ownership == "unknown":
            unknown.append(relative)
    if unknown:
        raise LocalUpdateError(
            "Candidate template contains unclassified files; update stopped:\n"
            + "\n".join(f"- {path}" for path in unknown)
        )
    return classified


def build_local_update_plan(target: Path, candidate: Path) -> LocalUpdatePlan:
    target = target.resolve()
    candidate = candidate.resolve()
    old_policy = load_ownership_policy(target)
    new_policy = load_ownership_policy(candidate)
    target_files = iter_files(target)
    candidate_files = iter_files(candidate)
    candidate_classes = _classify_candidate(candidate_files, new_policy)

    mutations: list[Mutation] = []

    # Candidate-driven writes/preservation.
    for relative in sorted(candidate_files):
        ownership = candidate_classes[relative]
        source = candidate_files[relative]
        destination = target / relative
        exists = destination.is_file()

        if ownership == "managed":
            if exists:
                old_class = classify_path(relative, old_policy)
                if old_class == "project_owned":
                    raise LocalUpdateError(
                        f"Unsafe ownership transition for `{relative}`: "
                        "project_owned -> managed. Reconcile ownership explicitly before updating."
                    )
                if old_class == "unknown" and not _same_bytes(destination, source):
                    raise LocalUpdateError(
                        f"Unsafe ownership transition for `{relative}`: unknown -> managed with "
                        "different bytes. Reconcile ownership explicitly before updating."
                    )
            if not exists:
                mutations.append(Mutation("ADD_MANAGED", relative))
            elif _same_bytes(destination, source):
                mutations.append(Mutation("UNCHANGED_MANAGED", relative))
            else:
                mutations.append(Mutation("UPDATE_MANAGED", relative))
        elif ownership == "project_owned":
            mutations.append(Mutation("KEEP_PROJECT" if exists else "ADD_PROJECT", relative))
        elif ownership == "installer_metadata":
            if exists and _same_bytes(destination, source):
                mutations.append(Mutation("KEEP_METADATA", relative))
            else:
                mutations.append(Mutation("UPDATE_METADATA", relative))
        else:  # pragma: no cover - guarded above
            raise LocalUpdateError(f"Unknown candidate ownership: {relative}")

    # Files that were managed by the previous framework and intentionally no
    # longer exist in the new candidate may be removed. Unknown/project-owned
    # extras are never deleted by this updater.
    candidate_paths = set(candidate_files)
    for relative, path in sorted(target_files.items()):
        if relative in candidate_paths:
            continue
        old_class = classify_path(relative, old_policy)
        if old_class != "managed":
            continue
        new_class = classify_path(relative, new_policy)
        if new_class == "project_owned":
            continue
        if path.is_file():
            mutations.append(Mutation("REMOVE_MANAGED", relative))

    mutations.sort(key=lambda item: (item.path, item.action))
    return LocalUpdatePlan(tuple(mutations))


def _project_owned_hashes(target: Path, policy: OwnershipPolicy) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative, path in iter_files(target).items():
        if classify_path(relative, policy) == "project_owned":
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _verify_applied_plan(target: Path, candidate: Path, plan: LocalUpdatePlan) -> None:
    for mutation in plan.mutations:
        destination = target / mutation.path
        source = candidate / mutation.path
        if mutation.action in {"ADD_MANAGED", "UPDATE_MANAGED", "UPDATE_METADATA", "ADD_PROJECT"}:
            if not destination.is_file() or not _same_bytes(destination, source):
                raise LocalUpdateError(f"Post-apply verification failed for {mutation.path}")
        elif mutation.action == "REMOVE_MANAGED" and destination.exists():
            raise LocalUpdateError(f"Removed managed path still exists: {mutation.path}")


def apply_local_update_plan(target: Path, candidate: Path, plan: LocalUpdatePlan) -> None:
    target = target.resolve()
    candidate = candidate.resolve()
    new_policy = load_ownership_policy(candidate)
    before_project = _project_owned_hashes(target, new_policy)
    changed = plan.changed()

    with tempfile.TemporaryDirectory(prefix="planning-lite-local-update-backup-") as temporary:
        backup = Path(temporary)
        existed: set[str] = set()
        touched: set[str] = set()
        try:
            for mutation in changed:
                destination = target / mutation.path
                source = candidate / mutation.path
                touched.add(mutation.path)
                if destination.is_file():
                    existed.add(mutation.path)
                    backup_path = backup / mutation.path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(destination, backup_path)

                if mutation.action == "REMOVE_MANAGED":
                    if destination.exists():
                        destination.unlink()
                    continue

                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

            _verify_applied_plan(target, candidate, plan)
            after_project = _project_owned_hashes(target, new_policy)
            for relative, digest in before_project.items():
                if after_project.get(relative) != digest:
                    raise LocalUpdateError(
                        f"Project-owned file changed during local-only update: {relative}"
                    )
        except Exception as exc:
            # Roll back every planned mutation before surfacing the failure.
            for relative in sorted(touched, reverse=True):
                destination = target / relative
                backup_path = backup / relative
                if relative in existed:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_path, destination)
                elif destination.exists():
                    destination.unlink()
            if isinstance(exc, LocalUpdateError):
                raise
            raise LocalUpdateError(f"Local-only update failed and was rolled back: {exc}") from exc


def format_local_update_plan(plan: LocalUpdatePlan) -> str:
    visible = [item for item in plan.mutations if item.action != "UNCHANGED_MANAGED"]
    lines = ["Planning Lite local-only update plan:"]
    for item in visible:
        lines.append(f"{item.action:<18} {item.path}")
    lines.append("")
    lines.append("Summary:")
    for action in (
        "ADD_MANAGED",
        "UPDATE_MANAGED",
        "REMOVE_MANAGED",
        "ADD_PROJECT",
        "KEEP_PROJECT",
        "UPDATE_METADATA",
        "KEEP_METADATA",
        "UNCHANGED_MANAGED",
    ):
        lines.append(f"  {action:<18} {plan.count(action)}")
    return "\n".join(lines)
