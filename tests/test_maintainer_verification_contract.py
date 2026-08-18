from __future__ import annotations

from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_central_repo_verification_does_not_require_root_doctor() -> None:
    root = _root()
    readme = (root / "README.md").read_text(encoding="utf-8")
    operator = (root / "docs/OPERATOR_WORKFLOW.ru.md").read_text(encoding="utf-8")
    current = (root / "docs/design/project-spine/PL-V38-CURRENT.md").read_text(
        encoding="utf-8"
    )

    required_central_commands = (
        "uv sync",
        "uv run pytest",
        "uv run python scripts/test_template_update.py",
    )
    for command in required_central_commands:
        assert command in readme
        assert command in operator
        assert command in current

    assert "not** a central-repository validation command" in readme
    assert "не запускайте `planning-lite doctor .` в корне центрального репозитория" in operator
    assert "Do **not** run `planning-lite doctor .` at the central repository root" in current


def test_doctor_remains_a_consumer_verification_command() -> None:
    root = _root()
    operator = (root / "docs/OPERATOR_WORKFLOW.ru.md").read_text(encoding="utf-8")
    installation = (root / "docs/UPDATABLE_INSTALLATION.ru.md").read_text(encoding="utf-8")
    smoke = (root / "scripts/test_template_update.py").read_text(encoding="utf-8")

    assert "Выполнить `planning-lite doctor .`" in operator
    assert "adopted/installed consumer-проекта" in installation
    assert '"planning-lite", "doctor", str(target)' in smoke
