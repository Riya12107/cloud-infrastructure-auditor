
from rich.console import Console
from rich.table import Table

console = Console()


def display_cleanup_preview(findings):
    """Display suggested cleanup actions without changing cloud resources."""

    console.print(
        "\n[bold yellow]Safe Cleanup Preview[/bold yellow]"
    )
    console.print(
        "[yellow]Preview only: no cloud resources will be changed.[/yellow]\n"
    )

    table = Table(title="Recommended Actions")
    table.add_column("Resource ID", style="cyan")
    table.add_column("Issue")
    table.add_column("Recommended Action")
    table.add_column("Severity")

    action_count = 0

    for finding in findings:
        if finding.resource_type == "ebs":
            action = "Review; delete only if unneeded"
        elif finding.resource_type == "elastic_ip":
            action = "Review; release only if unneeded"
        elif finding.resource_type == "ec2":
            action = "Review utilization; consider resizing"
        elif finding.resource_type == "gcp_compute":
            action = "Review; delete only if unneeded"
        else:
            continue

        table.add_row(
            str(finding.resource_id or "Unknown"),
            finding.title,
            action,
            finding.severity.upper(),
        )
        action_count += 1

    console.print(table)

    if action_count == 0:
        console.print(
            "[green]No cleanup recommendations to preview.[/green]"
        )
    else:
        console.print(
            f"\nRecommendations requiring review: {action_count}"
        )

    console.print(
        "\n[bold green]Preview completed. No resources were modified.[/bold green]"
    )
