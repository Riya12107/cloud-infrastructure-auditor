import typer
from rich import print

from utils.logger import get_logger
from app.audit_engine import run_audit
from app.report import display_audit_report
app = typer.Typer()
logger = get_logger()


@app.command()
def start():
    logger.info("Application started")
    print("[bold green]Cloud Infrastructure Auditor is ready![/bold green]")


@app.command()
def info():
    print("[bold blue]Cloud Infrastructure Auditor[/bold blue]")
    print("Version: 1.0.0")
    print("Purpose: Audit cloud resources and identify cost-saving opportunities.")


@app.command()
def version():
    print("Cloud Infrastructure Auditor version 1.0.0")


@app.command()
def audit():
    """Run a cloud infrastructure audit."""
    logger.info("Starting cloud infrastructure audit")

    result = run_audit()

    print("\n[bold blue]Cloud Infrastructure Audit[/bold blue]\n")

    print("[bold]Resource Summary:[/bold]")

    for resource_type, count in result["summary"].items():
        print(f"  {resource_type}: {count}")

    print("\n[bold green]Audit completed successfully.[/bold green]")


if __name__ == "__main__":
    app()