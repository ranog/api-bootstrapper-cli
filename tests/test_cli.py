import pytest
import typer
from typer.testing import CliRunner

from api_bootstrapper_cli.cli import app, main


runner = CliRunner()


@pytest.mark.parametrize(
    "args",
    [
        ["--help"],
        ["bootstrap-env", "--help"],
    ],
)
def test_should_show_help(args):
    result = runner.invoke(app, args)

    assert result.exit_code == 0
    assert "Usage: bootstrap-env" in result.stdout


def test_should_list_bootstrap_env_command():
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert result.stdout == "bootstrap-env: TODO\n"


def test_should_have_callable_main_function():
    assert callable(main)


def test_should_be_typer_instance():
    assert isinstance(app, typer.Typer)
