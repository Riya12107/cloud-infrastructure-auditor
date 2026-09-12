import typer
from rich import print

app = typer.Typer()

@app.command()
def start():
    print("[bold green]Cloud Infrastructure Auditor is ready![/bold green]")

if __name__ == "__main__":
    app()