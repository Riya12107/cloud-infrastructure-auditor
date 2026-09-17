import typer
from rich import print
from utils.logger import get_logger

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


if __name__ == "__main__":
    app()