
import typer
from rich import print

from utils.logger import get_logger
from app.audit_engine import run_audit
from app.report import display_audit_report
from app.json_report import export_json_report
from app.cleanup_preview import display_cleanup_preview

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
    logger.info("Starting a cloud infrastructure audit")

    result = run_audit()
    display_audit_report(result)

    output_file = export_json_report(result)
    print(f"\n[bold green]JSON report saved to: {output_file}[/bold green]")


@app.command("cleanup-preview")
def cleanup_preview():
    """Preview recommended cleanup actions without modifying resources."""
    logger.info("Generating safe cleanup preview")

    result = run_audit()
    display_cleanup_preview(result.get("findings", []))


if __name__ == "__main__":
    app()
