import typer

from api_bootstrapper_cli.commands.add_alembic import add_alembic
from api_bootstrapper_cli.commands.add_docker import add_docker
from api_bootstrapper_cli.commands.add_mypy import add_mypy
from api_bootstrapper_cli.commands.add_pre_commit import add_pre_commit
from api_bootstrapper_cli.commands.bootstrap_env import bootstrap_env
from api_bootstrapper_cli.commands.init import init
from api_bootstrapper_cli.commands.install_agent_skills import install_agent_skills
from api_bootstrapper_cli.commands.install_skills import install_skills


app = typer.Typer(
    no_args_is_help=True,
    help="CLI to bootstrap and manage Python API projects.",
    epilog="💡 Tip: Use 'api-bootstrapper COMMAND --help' to see options for each command.",
    add_completion=True,
    rich_markup_mode="rich",
)

# ── Sub-app groups ─────────────────────────────────────────────────────────────
env_app = typer.Typer(
    no_args_is_help=True,
    help="[cyan]Manage Python environment[/cyan] (pyenv + Poetry + VSCode).",
    rich_markup_mode="rich",
)

hooks_app = typer.Typer(
    no_args_is_help=True,
    help="[cyan]Manage git hooks[/cyan] and code-quality tools.",
    rich_markup_mode="rich",
)

db_app = typer.Typer(
    no_args_is_help=True,
    help="[cyan]Manage database migrations[/cyan] (Alembic).",
    rich_markup_mode="rich",
)

env_app.command("bootstrap")(bootstrap_env)
hooks_app.command("add-pre-commit")(add_pre_commit)
hooks_app.command("add-mypy")(add_mypy)
db_app.command("add-alembic")(add_alembic)

app.add_typer(env_app, name="env")
app.add_typer(hooks_app, name="hooks")
app.add_typer(db_app, name="db")

# ── Top-level commands (kept for backward compatibility) ───────────────────────
app.command("init")(init)
app.command("bootstrap-env")(bootstrap_env)
app.command("add-alembic")(add_alembic)
app.command("add-docker")(add_docker)
app.command("add-pre-commit")(add_pre_commit)
app.command("add-mypy")(add_mypy)
app.command("install-skills")(install_skills)
app.command("install-agent-skills")(install_agent_skills)


def main() -> None:
    app()
