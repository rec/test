import typer
from typing import List

app = typer.Typer()


@app.command()
def hello(names: List[str] = None):
    typer.echo(f"Hello {names}")


if __name__ == "__main__":
    app()
