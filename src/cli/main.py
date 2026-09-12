import typer
from rich.console import Console

app = typer.Typer(
    name="cloud-auditor",
    help="Cloud Infrastructure Auditor & Cost Optimizer"
)

console = Console()


@app.command()
def audit():
    """Run a cloud infrastructure audit."""
    console.print("Starting cloud infrastructure audit...")


@app.command()
def version():
    """Display application version."""
    console.print("Cloud Infrastructure Auditor v0.1.0")


if __name__ == "__main__":
    app()