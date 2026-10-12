
from rich.console import Console
from rich.table import Table

console = Console()


def display_audit_report(result):
    """Display an audit report with an accurate execution status."""

    status = result.get("status", "success")
    errors = result.get("errors", [])

    console.print("\n[bold blue]Cloud Infrastructure Audit[/bold blue]\n")

    summary_table = Table(title="Resource Summary")
    summary_table.add_column("Resource", style="cyan")
    summary_table.add_column("Count", justify="right")

    for resource_type, count in result.get("summary", {}).items():
        summary_table.add_row(
            resource_type.replace("_", " ").title(),
            str(count),
        )

    console.print(summary_table)

    findings = result.get("findings", [])

    if findings:
        findings_table = Table(title="Findings")
        findings_table.add_column("Resource")
        findings_table.add_column("Severity")
        findings_table.add_column("Finding")
        findings_table.add_column("Savings / Month", justify="right")

        total_savings = 0.0

        for finding in findings:
            savings = finding.estimated_monthly_savings or 0.0
            total_savings += savings

            findings_table.add_row(
                finding.resource_id,
                finding.severity.upper(),
                finding.title,
                f"${savings:.2f}",
            )

        console.print(findings_table)
        console.print(
            f"\n[bold green]Total potential monthly savings: "
            f"${total_savings:.2f}[/bold green]"
        )

    elif status == "success":
        console.print("\n[green]No findings detected.[/green]")

    elif status == "incomplete":
        console.print(
            "\n[yellow]No findings were returned for the scanned "
            "resources. The audit was incomplete.[/yellow]"
        )

    else:
        console.print(
            "\n[red]The audit failed. Results may be unavailable.[/red]"
        )

    if errors:
        console.print("\n[bold red]Errors and warnings:[/bold red]")
        for error in errors:
            console.print(f"[red]- {error}[/red]")

    if status == "success":
        console.print("\n[bold green]Audit completed successfully.[/bold green]")
    elif status == "incomplete":
        console.print("\n[bold yellow]Audit completed with errors.[/bold yellow]")
    else:
        console.print("\n[bold red]Audit failed.[/bold red]")
