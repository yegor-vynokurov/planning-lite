from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

import planning_lite.cli as cli
from planning_lite.local_update import classify_path, load_ownership_policy


ROOT = Path(__file__).resolve().parents[1]
ANSWERS_FILE = ".copier-answers.planning-lite.yml"
BASELINE_TAG = "v0.0.0.dev1"
CANDIDATE_TAG = "v0.0.0.dev2"
CONFLICT_TAG = "v0.0.0.dev3"
ADR_PATTERN = ".planning/decisions/ADR-*.md"


def _run(*args: str, cwd: Path) -> str:
    """Run Git fixture commands with explicit cwd and fail on fixture errors."""
    return subprocess.run(
        args, cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def _candidate_manifest(root: Path) -> dict[str, str]:
    """Hash the exact Copier config and rendered template tree as raw bytes."""
    paths = [root / "copier.yml", *(root / "template").rglob("*")]
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
        if path.is_file()
    }


def _canonical_lf(value: bytes) -> bytes:
    """Normalize platform line endings for managed render comparisons."""
    return value.replace(b"\r\n", b"\n")


def _init_source_repo(source: Path) -> None:
    """Initialize Git only inside the disposable Copier source fixture."""
    source.mkdir(parents=True, exist_ok=True)
    _run("git", "init", cwd=source)
    _run("git", "config", "user.email", "planning-lite-test@example.invalid", cwd=source)
    _run("git", "config", "user.name", "Planning Lite Test", cwd=source)
    _run("git", "config", "core.autocrlf", "false", cwd=source)


def _commit_tag(source: Path, message: str, tag: str) -> str:
    """Commit and annotate one isolated source state, then require a clean tree."""
    _run("git", "add", "-A", cwd=source)
    _run("git", "commit", "-m", message, cwd=source)
    _run("git", "tag", "-a", tag, "-m", message, cwd=source)
    assert _run("git", "cat-file", "-t", tag, cwd=source) == "tag"
    assert _run("git", "status", "--porcelain", cwd=source) == ""
    return _run("git", "rev-parse", f"{tag}^{{commit}}", cwd=source)


def _run_normal_copier_update(consumer: Path, source: Path, ref: str) -> None:
    """Run Copier's real update using the committed explicit source and tag."""
    answers = yaml.safe_load(
        (consumer / ANSWERS_FILE).read_text(encoding="utf-8")
    )
    assert answers["_src_path"] == str(source)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "copier",
            "update",
            "--answers-file",
            ANSWERS_FILE,
            "--skip-answered",
            "--vcs-ref",
            ref,
        ],
        cwd=consumer,
        check=True,
        capture_output=True,
        text=True,
    )


def _create_two_tag_source(source: Path) -> tuple[str, dict[str, str]]:
    """Build a synthetic pre-T08 baseline and exact candidate in a disposable source.

    The baseline is derived only inside this fixture: managed decision guidance
    is replaced with older content and the T08 ADR/INDEX ownership and skip rules
    are removed. The candidate tag is then copied from the current source and
    checked byte-for-byte. Neither tag depends on the shared repository HEAD.
    """
    candidate_manifest = _candidate_manifest(ROOT)
    source.mkdir(parents=True)
    shutil.copytree(ROOT / "template", source / "template")
    shutil.copy2(ROOT / "copier.yml", source / "copier.yml")

    baseline_copier = yaml.safe_load((source / "copier.yml").read_text(encoding="utf-8"))
    baseline_skip = baseline_copier.get("_skip_if_exists", [])
    index_path = ".planning/decisions/INDEX.md"
    assert baseline_skip.count(ADR_PATTERN) == 1
    assert baseline_skip.count(index_path) == 1
    baseline_copier["_skip_if_exists"] = [
        pattern for pattern in baseline_skip if pattern not in {ADR_PATTERN, index_path}
    ]
    (source / "copier.yml").write_text(
        yaml.safe_dump(baseline_copier, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )

    ownership_path = source / "template/.planning/framework/OWNERSHIP.yml"
    baseline_ownership = yaml.safe_load(ownership_path.read_text(encoding="utf-8"))
    expected_ownership_rows = {
        "project_owned": {ADR_PATTERN, index_path},
        "managed": {
            ".planning/decisions/README.md",
            ".planning/decisions/TEMPLATE.md",
        },
    }
    for section, rows in expected_ownership_rows.items():
        for row in rows:
            assert baseline_ownership[section].count(row) == 1
        baseline_ownership[section] = [
            row for row in baseline_ownership[section] if row not in rows
        ]
    ownership_path.write_text(
        yaml.safe_dump(baseline_ownership, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )
    (source / "template/.planning/decisions/README.md").write_bytes(
        b"# Baseline decision guidance\n\nPre-T08 decision records guidance.\n"
    )
    (source / "template/.planning/decisions/TEMPLATE.md").write_bytes(
        b"# Baseline decision record\n\nPre-T08 decision record form.\n"
    )

    _init_source_repo(source)
    _commit_tag(source, "synthetic pre-T08 decision template baseline", BASELINE_TAG)

    shutil.rmtree(source / "template")
    shutil.copytree(ROOT / "template", source / "template")
    shutil.copy2(ROOT / "copier.yml", source / "copier.yml")
    assert _candidate_manifest(source) == candidate_manifest

    candidate_commit = _commit_tag(source, "exact T-08 template candidate", CANDIDATE_TAG)
    for relative, expected_sha in candidate_manifest.items():
        committed = subprocess.check_output(
            ["git", "show", f"{candidate_commit}:{relative}"], cwd=source
        )
        assert hashlib.sha256(committed).hexdigest() == expected_sha
    return candidate_commit, candidate_manifest


def _init_consumer_repo(consumer: Path) -> None:
    """Create an independent clean consumer for real Copier adoption/update."""
    consumer.mkdir(parents=True)
    _run("git", "init", cwd=consumer)
    _run("git", "config", "user.email", "planning-lite-test@example.invalid", cwd=consumer)
    _run("git", "config", "user.name", "Planning Lite Test", cwd=consumer)
    _run("git", "config", "core.autocrlf", "false", cwd=consumer)
    (consumer / "README.md").write_bytes(b"# disposable consumer\n")
    _run("git", "add", "README.md", cwd=consumer)
    _run("git", "commit", "-m", "initial consumer", cwd=consumer)


def test_normal_copier_update_preserves_decisions_and_refreshes_managed_guidance(
    tmp_path: Path, capsys
) -> None:
    """Prove exact ownership and real tagged update behavior without issuing authority.

    The disposable source commits the clean central baseline and exact current
    copier.yml/template candidate under annotated tags; its Git tree is checked
    against every candidate byte. A separate clean consumer adopts the baseline,
    then adds project-owned ADR and INDEX bytes. A normal Copier update refreshes
    only managed decision guidance/form. A third adversarial fixture tag carries
    same-name conflicting ADR/INDEX inputs to prove the narrow skip rules retain
    the project bytes. No fixture commit changes the central checkout, and no
    update path issues Authorization or supplies V1 evidence. Managed guidance
    comparisons normalize Copier's platform line endings; project-owned ADR and
    INDEX preservation remains an exact raw-byte assertion.
    """
    policy = load_ownership_policy(ROOT / "template")
    assert classify_path(".planning/decisions/ADR-0001-local-choice.md", policy) == "project_owned"
    assert classify_path(".planning/decisions/README.md", policy) == "managed"
    assert classify_path(".planning/decisions/TEMPLATE.md", policy) == "managed"
    assert classify_path(".planning/decisions/INDEX.md", policy) == "project_owned"
    assert classify_path(".planning/decisions/meeting-notes.md", policy) == "unknown"

    ownership = yaml.safe_load(
        (ROOT / "template/.planning/framework/OWNERSHIP.yml").read_text(encoding="utf-8")
    )
    copier = yaml.safe_load((ROOT / "copier.yml").read_text(encoding="utf-8"))
    assert ownership["project_owned"].count(ADR_PATTERN) == 1
    assert ownership["managed"].count(".planning/decisions/README.md") == 1
    assert ownership["managed"].count(".planning/decisions/TEMPLATE.md") == 1
    assert ownership["project_owned"].count(".planning/decisions/INDEX.md") == 1
    assert copier["_skip_if_exists"].count(ADR_PATTERN) == 1
    assert copier["_skip_if_exists"].count(".planning/decisions/INDEX.md") == 1
    assert not any(
        pattern in ownership["project_owned"] or pattern in copier["_skip_if_exists"]
        for pattern in ("*.md", ".planning/decisions/*.md", ".planning/decisions/**")
    )
    assert not copier.get("_tasks")
    assert not copier.get("_migrations")

    source = tmp_path / "source"
    candidate_commit, candidate_manifest = _create_two_tag_source(source)
    assert _run("git", "status", "--porcelain", cwd=source) == ""
    assert candidate_commit
    assert len(candidate_manifest) > 1

    consumer = tmp_path / "consumer"
    _init_consumer_repo(consumer)
    assert cli.main(
        [
            "adopt",
            str(consumer),
            "--template-source",
            str(source),
            "--vcs-ref",
            BASELINE_TAG,
        ]
    ) == 0
    capsys.readouterr()
    answers_path = consumer / ANSWERS_FILE
    answers_data = yaml.safe_load(answers_path.read_text(encoding="utf-8"))
    assert answers_data["_src_path"] == str(source)
    _run("git", "add", "-A", cwd=consumer)
    _run("git", "commit", "-m", "adopt committed baseline template", cwd=consumer)

    decisions = consumer / ".planning/decisions"
    adr = decisions / "ADR-0001-local-choice.md"
    index = decisions / "INDEX.md"
    adr_raw = (
        b"# ADR-0001: Local choice\n\n- Status: `Proposed`\n"
        b"- Date: 2026-10-07\n- Deciders: Project owner\n"
        b"- Related changes: None\n\n## Context\nLocal decision.\n"
    )
    index_raw = b"# Decision index\n\n- ADR-0001-local-choice.md\n"
    adr.write_bytes(adr_raw)
    index.write_bytes(index_raw)
    _run("git", "add", ".planning/decisions/ADR-0001-local-choice.md", ".planning/decisions/INDEX.md", cwd=consumer)
    _run("git", "commit", "-m", "add project-owned decision records", cwd=consumer)
    assert _run("git", "status", "--porcelain", cwd=consumer) == ""

    managed_paths = (
        ".planning/decisions/README.md",
        ".planning/decisions/TEMPLATE.md",
    )
    managed_before = {rel: (consumer / rel).read_bytes() for rel in managed_paths}
    authorization_root = consumer / ".planning/project/authorizations"
    authorization_json_before = (
        {p.relative_to(consumer).as_posix(): p.read_bytes() for p in authorization_root.rglob("*.json")}
        if authorization_root.exists()
        else {}
    )
    _run_normal_copier_update(consumer, source, CANDIDATE_TAG)

    assert adr.read_bytes() == adr_raw
    assert index.read_bytes() == index_raw
    for relative in managed_paths:
        candidate = source / "template" / relative
        assert _canonical_lf((consumer / relative).read_bytes()) == candidate.read_bytes()
        assert (consumer / relative).read_bytes() != managed_before[relative]
    answers = yaml.safe_load((consumer / ANSWERS_FILE).read_text(encoding="utf-8"))
    assert answers["_commit"] == CANDIDATE_TAG
    authorization_json_after = (
        {p.relative_to(consumer).as_posix(): p.read_bytes() for p in authorization_root.rglob("*.json")}
        if authorization_root.exists()
        else {}
    )
    assert authorization_json_after == authorization_json_before
    # Add deliberately conflicting same-name inputs only to the disposable
    # follow-up source tag; this tests Copier skip behavior without changing the
    # exact candidate v2 bytes bound above.
    incoming_adr = source / "template/.planning/decisions/ADR-0001-local-choice.md"
    incoming_adr.write_bytes(b"# conflicting upstream ADR\n")
    incoming_index = source / "template/.planning/decisions/INDEX.md"
    incoming_index.write_bytes(b"# conflicting upstream INDEX\n")
    _commit_tag(source, "adversarial same-name project-file candidates", CONFLICT_TAG)
    _run("git", "add", "-A", cwd=consumer)
    _run("git", "commit", "-m", "accept exact T-08 candidate", cwd=consumer)
    assert _run("git", "status", "--porcelain", cwd=consumer) == ""
    assert cli.main(["doctor", str(consumer)]) == 0
    capsys.readouterr()

    _run_normal_copier_update(consumer, source, CONFLICT_TAG)
    assert adr.read_bytes() == adr_raw
    assert index.read_bytes() == index_raw
    for relative in managed_paths:
        assert _canonical_lf((consumer / relative).read_bytes()) == (
            source / "template" / relative
        ).read_bytes()
    assert _run("git", "status", "--porcelain", cwd=source) == ""
