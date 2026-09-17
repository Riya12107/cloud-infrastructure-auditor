import typer
from rich.console import Console
from rich.table import Table

from src.auth.aws_auth import get_aws_session_info, validate_aws_credentials
from src.config.settings import AWS_PROFILE, AWS_REGION


app = typer.Typer(
    name="cloud-auditor",
    help="Cloud Infrastructure Auditor & Cost Optimizer"
)

console = Console()


@app.command()
def audit():
    """Run a cloud infrastructure audit."""

    console.print(
        "[bold]Starting cloud infrastructure audit...[/bold]"
    )

    console.print("Checking AWS authentication...")

    if validate_aws_credentials():
        session_info = get_aws_session_info()

        console.print(
            "[green]AWS authentication successful.[/green]"
        )
        console.print(
            f"Profile: {session_info['profile']}"
        )
        console.print(
            f"Region: {session_info['region']}"
        )

    else:
        console.print(
            "[red]AWS authentication failed.[/red]"
        )
        console.print(
            "Please check your AWS credentials and configuration."
        )


@app.command()
def version():
    """Display application version."""

    console.print(
        "Cloud Infrastructure Auditor v0.1.0"
    )


@app.command()
def config():
    """Display current cloud auditor configuration."""

    table = Table(title="Cloud Auditor Configuration")

    table.add_column("Setting")
    table.add_column("Value")

    table.add_row(
        "AWS Profile",
        AWS_PROFILE or "Default credential chain"
    )

    table.add_row(
        "AWS Region",
        AWS_REGION
    )

    console.print(table)


if __name__ == "__main__":
    app()