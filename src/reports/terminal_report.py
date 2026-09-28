from rich.console import Console
from rich.table import Table


console = Console()


def display_findings(findings: list[dict]) -> None:
    """
    Display audit findings in a Rich terminal table.

    Args:
        findings: List of audit findings returned by scanners.
    """

    table = Table(
        title="Cloud Infrastructure Audit Findings"
    )

    table.add_column("Resource Type")
    table.add_column("Resource ID")
    table.add_column("Region")
    table.add_column("Status")
    table.add_column("Reason")
    table.add_column("Cleanup Action")

    if not findings:
        console.print("[yellow]No audit findings found.[/yellow]")
        return

    for finding in findings:
        table.add_row(
            str(finding.get("resource_type", "")),
            str(finding.get("resource_id", "")),
            str(finding.get("region", "")),
            str(finding.get("status", "")),
            str(finding.get("reason", "")),
            str(finding.get("cleanup_action", "")),
        )

    console.print(table)