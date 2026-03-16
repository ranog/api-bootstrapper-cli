from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app
from api_bootstrapper_cli.core.skills_installer import (
    SkillsDistribution,
    SkillsInstallResult,
)


runner = CliRunner()


def strip_ansi_codes(text: str) -> str:
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


@patch("api_bootstrapper_cli.commands.install_agent_skills.install_agentskills")
def test_should_install_agent_skills_with_default_target(
    mock_install: MagicMock, tmp_path: Path
):
    mock_install.return_value = SkillsInstallResult(
        distribution=SkillsDistribution.agentskills,
        source_root=tmp_path / "source",
        target_root=tmp_path / "target",
        installed_skills=("api-bootstrapper-init",),
        overwritten_skills=(),
        skipped_skills=(),
    )

    result = runner.invoke(app, ["install-agent-skills"])
    output = strip_ansi_codes(result.stdout)
    normalized_output = normalize_whitespace(output)

    assert result.exit_code == 0
    assert "Agent Skills installed" in output
    assert "Bundled api-bootstrapper skills in this release: 1" in normalized_output
    assert "System skills are managed separately." in normalized_output
    mock_install.assert_called_once_with(target_root=None, overwrite=True)


@patch("api_bootstrapper_cli.commands.install_agent_skills.install_agentskills")
def test_should_install_agent_skills_with_custom_target(
    mock_install: MagicMock, tmp_path: Path
):
    target_path = tmp_path / "custom-agent-skills"
    mock_install.return_value = SkillsInstallResult(
        distribution=SkillsDistribution.agentskills,
        source_root=tmp_path / "source",
        target_root=target_path,
        installed_skills=("api-bootstrapper-init",),
        overwritten_skills=(),
        skipped_skills=(),
    )

    result = runner.invoke(
        app,
        ["install-agent-skills", "--target", str(target_path), "--no-overwrite"],
    )

    assert result.exit_code == 0
    mock_install.assert_called_once_with(target_root=target_path, overwrite=False)


@patch("api_bootstrapper_cli.commands.install_agent_skills.install_agentskills")
def test_should_show_skipped_agent_skills_when_not_overwriting(
    mock_install: MagicMock, tmp_path: Path
):
    mock_install.return_value = SkillsInstallResult(
        distribution=SkillsDistribution.agentskills,
        source_root=tmp_path / "source",
        target_root=tmp_path / "target",
        installed_skills=("api-bootstrapper-init",),
        overwritten_skills=(),
        skipped_skills=("api-bootstrapper-bootstrap-env",),
    )

    result = runner.invoke(app, ["install-agent-skills", "--no-overwrite"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Skipped skills" in output
    assert "api-bootstrapper-bootstrap-env" in output


@patch("api_bootstrapper_cli.commands.install_agent_skills.install_agentskills")
def test_should_return_error_when_agent_skills_installation_fails(
    mock_install: MagicMock,
):
    mock_install.side_effect = RuntimeError("missing embedded agent skills")

    result = runner.invoke(app, ["install-agent-skills"])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 1
    assert "Error:" in output
    assert "missing embedded agent skills" in output
