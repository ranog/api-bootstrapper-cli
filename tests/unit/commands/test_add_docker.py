from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app


runner = CliRunner()


def strip_ansi_codes(text: str) -> str:
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


@patch("api_bootstrapper_cli.commands.add_docker.create_dockerfile")
def test_should_create_dockerfile(mock_create: MagicMock, tmp_path: Path):
    dockerfile_path = tmp_path / "Dockerfile"
    mock_create.return_value = dockerfile_path

    result = runner.invoke(app, ["add-docker", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "Adding Docker support" in output
    assert "Created Dockerfile" in output
    mock_create.assert_called_once_with(tmp_path, python_version="3.13")


@patch("api_bootstrapper_cli.commands.add_docker.create_dockerfile")
def test_should_use_custom_python_version(mock_create: MagicMock, tmp_path: Path):
    dockerfile_path = tmp_path / "Dockerfile"
    mock_create.return_value = dockerfile_path

    result = runner.invoke(
        app, ["add-docker", "--path", str(tmp_path), "--python", "3.12"]
    )

    assert result.exit_code == 0
    mock_create.assert_called_once_with(tmp_path, python_version="3.12")


def test_should_skip_if_dockerfile_exists(tmp_path: Path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM ubuntu:latest\n")

    result = runner.invoke(app, ["add-docker", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert result.exit_code == 0
    assert "already exists" in output
    assert "Skipping creation" in output


def test_should_work_in_current_directory(tmp_path: Path):
    with runner.isolated_filesystem():
        isolated_cwd = Path.cwd().resolve()
        result = runner.invoke(app, ["add-docker"])
        output = strip_ansi_codes(result.stdout)

        assert result.exit_code == 0
        assert "Adding Docker support" in output
        assert (isolated_cwd / "Dockerfile").exists()


def test_should_show_next_steps(tmp_path: Path):
    result = runner.invoke(app, ["add-docker", "--path", str(tmp_path)])
    output = strip_ansi_codes(result.stdout)

    assert "Next steps:" in output
    assert "requirements.txt" in output
    assert "docker build" in output
    assert "docker run" in output
