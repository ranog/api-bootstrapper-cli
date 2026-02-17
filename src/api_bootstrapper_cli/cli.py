import typer


app = typer.Typer(no_args_is_help=True)


@app.command()
def bootstrap_env():
    typer.echo("bootstrap-env: TODO")


def main():
    app()
