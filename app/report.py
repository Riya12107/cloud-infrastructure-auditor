from rich.console import Console
from rich.table import Table


console = Console()


def display_audit_report(result):
    console.print("\n[bold blue]Cloud Infrastructure Audit[/bold blue]\n")

    summary_table = Table(title="Resource Summary")

    summary_table.add_column("Resource", style="cyan")
    summary_table.add_column("Count", justify="right")

    for resource_type, count in result["summary"].items():
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

    else:
        console.print("\n[green]No findings detected.[/green]")

    console.print("\n[bold green]Audit completed successfully.[/bold green]")