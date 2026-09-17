import typer
from rich.console import Console
from rich.table import Table

from src.auth.aws_auth import get_aws_session_info, validate_aws_credentials
from src.config.settings import AWS_PROFILE, AWS_REGION
from src.scanners.scanner_manager import ScannerManager


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

    if not validate_aws_credentials():
        console.print(
            "[red]AWS authentication failed.[/red]"
        )
        console.print(
            "Please check your AWS credentials and configuration."
        )
        raise typer.Exit(code=1)

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

    console.print(
        "\n[bold]Running infrastructure scanners...[/bold]"
    )

    scanner_manager = ScannerManager()

    findings = scanner_manager.run_all()

    console.print(
        "[green]Infrastructure scan completed.[/green]"
    )

    summary_table = Table(
        title="Audit Summary"
    )

    summary_table.add_column("Metric")
    summary_table.add_column("Count")

    summary_table.add_row(
        "Total findings",
        str(len(findings))
    )

    ebs_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "EBS"
    )

    elastic_ip_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "ElasticIP"
    )

    ec2_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "EC2"
    )

    summary_table.add_row(
        "EBS findings",
        str(ebs_count)
    )

    summary_table.add_row(
        "Elastic IP findings",
        str(elastic_ip_count)
    )

    summary_table.add_row(
        "EC2 findings",
        str(ec2_count)
    )

    console.print(summary_table)


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