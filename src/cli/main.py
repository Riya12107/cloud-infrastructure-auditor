import typer
from rich.console import Console
from rich.table import Table

from src.auth.aws_auth import (
    get_aws_client,
    get_aws_session_info,
    validate_aws_credentials,
)
from src.config.settings import AWS_PROFILE, AWS_REGION

from src.cleanup.dry_run import display_dry_run
from src.cleanup.resource_cleanup import execute_cleanup_target
from src.cleanup.ec2_cleanup import execute_ec2_cleanup_target

from src.reports.terminal_report import display_findings
from src.reports.csv_report import export_findings_to_csv
from src.reports.json_report import export_findings_to_json

from src.scanners.scanner_manager import ScannerManager


# ---------------------------------------------------------
# CLI Application
# ---------------------------------------------------------

app = typer.Typer(
    name="cloud-auditor",
    help="Cloud Infrastructure Auditor & Cost Optimizer",
)

console = Console()


# ---------------------------------------------------------
# Cleanup Execution
# ---------------------------------------------------------

def execute_cleanup_targets(findings: list[dict]) -> list[dict]:
    """
    Execute validated cleanup targets.

    EBS and Elastic IP resources use the general cleanup executor.
    EC2 resources use the EC2-specific cleanup executor.

    Invalid or unsupported resources are safely skipped
    by the cleanup validation logic.
    """

    ec2_client = get_aws_client("ec2")

    results = []

    for finding in findings:

        resource_type = finding.get("resource_type")

        # -------------------------------------------------
        # EBS and Elastic IP
        # -------------------------------------------------

        if resource_type in {"EBS", "ElasticIP"}:

            result = execute_cleanup_target(
                ec2_client,
                finding,
            )

        # -------------------------------------------------
        # EC2
        # -------------------------------------------------

        elif resource_type == "EC2":

            result = execute_ec2_cleanup_target(
                ec2_client,
                finding,
            )

        # -------------------------------------------------
        # Unsupported resource
        # -------------------------------------------------

        else:

            result = {
                "resource_type": resource_type,
                "resource_id": finding.get("resource_id"),
                "action": "skipped",
                "success": False,
                "message": "Unsupported cleanup resource type.",
            }

        results.append(result)

    return results


# ---------------------------------------------------------
# Audit Command
# ---------------------------------------------------------

@app.command()
def audit(
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show proposed cleanup actions without modifying cloud resources.",
    ),
    execute: bool = typer.Option(
        False,
        "--execute",
        help="Execute validated cleanup actions.",
    ),
):
    """
    Run a cloud infrastructure audit.
    """

    # -----------------------------------------------------
    # Prevent conflicting options
    # -----------------------------------------------------

    if dry_run and execute:

        console.print(
            "[red]Error: --dry-run and --execute cannot be used together.[/red]"
        )

        raise typer.Exit(code=1)

    # -----------------------------------------------------
    # Start Audit
    # -----------------------------------------------------

    console.print(
        "[bold]Starting cloud infrastructure audit...[/bold]"
    )

    # -----------------------------------------------------
    # AWS Authentication
    # -----------------------------------------------------

    console.print(
        "Checking AWS authentication..."
    )

    if not validate_aws_credentials():

        console.print(
            "[red]AWS authentication failed.[/red]"
        )

        console.print(
            "Please check your AWS credentials and configuration."
        )

        raise typer.Exit(code=1)

    # -----------------------------------------------------
    # AWS Session Information
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Run Infrastructure Scanners
    # -----------------------------------------------------

    console.print(
        "\n[bold]Running infrastructure scanners...[/bold]"
    )

    scanner_manager = ScannerManager()

    findings = scanner_manager.run_all()

    console.print(
        "[green]Infrastructure scan completed.[/green]"
    )

    # -----------------------------------------------------
    # Terminal Report
    # -----------------------------------------------------

    display_findings(findings)

    # -----------------------------------------------------
    # CSV Report
    # -----------------------------------------------------

    csv_output_path = "reports/audit_report.csv"

    export_findings_to_csv(
        findings,
        csv_output_path,
    )

    console.print(
        f"[green]CSV report exported to {csv_output_path}[/green]"
    )

    # -----------------------------------------------------
    # JSON Report
    # -----------------------------------------------------

    json_output_path = "reports/audit_report.json"

    export_findings_to_json(
        findings,
        json_output_path,
    )

    console.print(
        f"[green]JSON report exported to {json_output_path}[/green]"
    )

    # -----------------------------------------------------
    # Week 3 Day 5 - Dry Run
    # -----------------------------------------------------

    if dry_run:

        display_dry_run(
            findings
        )

    # -----------------------------------------------------
    # Week 3 Day 6 - Execute Mode
    # -----------------------------------------------------

    if execute:

        console.print()

        console.print(
            "[bold red]EXECUTE MODE[/bold red]"
        )

        console.print(
            "[red]Cleanup actions will modify cloud resources.[/red]"
        )

        console.print(
            "[yellow]This action cannot be undone easily.[/yellow]"
        )

        console.print()

        # -------------------------------------------------
        # Strict Confirmation
        # -------------------------------------------------

        confirmation = typer.prompt(
            "Type CONFIRM to continue"
        )

        if confirmation != "CONFIRM":

            console.print(
                "[yellow]Cleanup cancelled. "
                "No cloud resources were modified.[/yellow]"
            )

            raise typer.Exit(code=0)

        # -------------------------------------------------
        # Confirmation Accepted
        # -------------------------------------------------

        console.print(
            "[green]Confirmation accepted. "
            "Starting cleanup...[/green]"
        )

        cleanup_results = execute_cleanup_targets(
            findings
        )

        # -------------------------------------------------
        # Cleanup Result Summary
        # -------------------------------------------------

        successful = sum(
            1
            for result in cleanup_results
            if result.get("success") is True
        )

        failed = len(cleanup_results) - successful

        console.print()

        console.print(
            f"[green]Successful cleanup actions: {successful}[/green]"
        )

        if failed:

            console.print(
                f"[red]Failed or skipped cleanup actions: {failed}[/red]"
            )

    # -----------------------------------------------------
    # Audit Summary
    # -----------------------------------------------------

    summary_table = Table(
        title="Audit Summary"
    )

    summary_table.add_column(
        "Metric"
    )

    summary_table.add_column(
        "Count"
    )

    # -----------------------------------------------------
    # Total Findings
    # -----------------------------------------------------

    summary_table.add_row(
        "Total findings",
        str(len(findings)),
    )

    # -----------------------------------------------------
    # EBS Findings
    # -----------------------------------------------------

    ebs_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "EBS"
    )

    summary_table.add_row(
        "EBS findings",
        str(ebs_count),
    )

    # -----------------------------------------------------
    # Elastic IP Findings
    # -----------------------------------------------------

    elastic_ip_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "ElasticIP"
    )

    summary_table.add_row(
        "Elastic IP findings",
        str(elastic_ip_count),
    )

    # -----------------------------------------------------
    # EC2 Findings
    # -----------------------------------------------------

    ec2_count = sum(
        1
        for finding in findings
        if finding.get("resource_type") == "EC2"
    )

    summary_table.add_row(
        "EC2 findings",
        str(ec2_count),
    )

    console.print(
        summary_table
    )


# ---------------------------------------------------------
# Version Command
# ---------------------------------------------------------

@app.command()
def version():
    """
    Display application version.
    """

    console.print(
        "Cloud Infrastructure Auditor v0.1.0"
    )


# ---------------------------------------------------------
# Configuration Command
# ---------------------------------------------------------

@app.command()
def config():
    """
    Display current cloud auditor configuration.
    """

    table = Table(
        title="Cloud Auditor Configuration"
    )

    table.add_column(
        "Setting"
    )

    table.add_column(
        "Value"
    )

    table.add_row(
        "AWS Profile",
        AWS_PROFILE or "Default credential chain",
    )

    table.add_row(
        "AWS Region",
        AWS_REGION,
    )

    console.print(
        table
    )


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    app()