from pathlib import Path
import tomllib


def test_campaign_cli_is_opt_in_and_template_is_untouched() -> None:
    root = Path(__file__).resolve().parents[1]
    with (root / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)
    assert pyproject["project"]["scripts"]["planning-lite"] == "planning_lite.cli:main"
    assert pyproject["project"]["scripts"]["planning-lite-campaign"] == "planning_lite.campaign.cli:main"
    assert not (root / "template/.planning/campaign").exists()
    assert not (root / "template/.planning/experiments").exists()


def test_main_cli_remains_separate_from_campaign_cli() -> None:
    root = Path(__file__).resolve().parents[1]
    main_cli = (root / "src/planning_lite/cli.py").read_text(encoding="utf-8")
    assert "planning_lite.campaign" not in main_cli
    assert "planning-lite-campaign" not in main_cli


def test_campaign_cli_uses_distribution_version() -> None:
    from planning_lite import __version__
    from planning_lite.campaign.cli import build_parser

    parser = build_parser()
    version_action = next(action for action in parser._actions if "--version" in action.option_strings)
    assert version_action.version == f"%(prog)s {__version__}"
