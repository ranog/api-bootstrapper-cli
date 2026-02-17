import typer
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app, main


runner = CliRunner()


def test_should_show_help_with_help_flag():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.stdout
    assert "bootstrap-env" in result.stdout


def test_should_list_bootstrap_env_command():
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "bootstrap-env" in result.stdout or "TODO" in result.stdout


def test_should_show_help_for_bootstrap_env_command():
    result = runner.invoke(app, ["bootstrap-env", "--help"])

    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_should_have_callable_main_function():
    assert callable(main)


def test_should_be_typer_instance():
    assert isinstance(app, typer.Typer)
