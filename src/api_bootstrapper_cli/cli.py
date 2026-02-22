import typer

from api_bootstrapper_cli.commands.add_alembic import add_alembic
from api_bootstrapper_cli.commands.add_precommit import add_precommit
from api_bootstrapper_cli.commands.bootstrap_env import bootstrap_env
from api_bootstrapper_cli.commands.init import init


app = typer.Typer(
    no_args_is_help=True,
    help="CLI to bootstrap and manage Python API projects.",
    epilog="💡 Tip: Use 'api-bootstrapper COMMAND --help' to see options for each command.",
    add_completion=True,
    rich_markup_mode="rich",
)

app.command("init")(init)
app.command("bootstrap-env")(bootstrap_env)
app.command("add-alembic")(add_alembic)
app.command("add-precommit")(add_precommit)


def main():
    app()
