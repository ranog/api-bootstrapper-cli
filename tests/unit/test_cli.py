import typer
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app, main


runner = CliRunner(env={"NO_COLOR": "1"})


def test_should_show_main_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "bootstrap-env" in result.stdout
    assert "CLI to bootstrap and manage Python API projects" in result.stdout


def test_should_show_bootstrap_env_help(expected_bootstrap_help):
    result = runner.invoke(app, ["bootstrap-env", "--help"])

    assert result.exit_code == 0
    print(result.stdout)
    assert result.stdout == expected_bootstrap_help


def test_should_require_command():
    result = runner.invoke(app, [])

    assert result.exit_code == 2
    assert "Usage:" in result.stdout or "Commands" in result.stdout


def test_should_have_callable_main_function():
    assert callable(main)


def test_should_be_typer_instance():
    assert isinstance(app, typer.Typer)
