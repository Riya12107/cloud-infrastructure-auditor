from typing import Any

from rich.console import Console
from rich.table import Table

from src.cleanup.validator import validate_cleanup_targets
from src.cleanup.ec2_validator import validate_ec2_cleanup_target


console = Console()


def get_dry_run_targets(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Return only findings that are valid cleanup candidates.

    Dry-run mode does not modify any cloud resources.
    It only identifies resources that would be considered
    for cleanup.
    """

    cleanup_targets = []

    general_targets = validate_cleanup_targets(findings)

    cleanup_targets.extend(general_targets)

    for finding in findings:
        if finding.get("resource_type") != "EC2":
            continue

        is_valid, _ = validate_ec2_cleanup_target(finding)

        if is_valid:
            cleanup_targets.append(finding)

    return cleanup_targets


def display_dry_run(
    findings: list[dict[str, Any]],
) -> None:
    """
    Display the cleanup actions that would be proposed.

    This function is read-only and does not perform
    any AWS cleanup operation.
    """

    cleanup_targets = get_dry_run_targets(findings)

    console.print()
    console.print(
        "[bold yellow]DRY-RUN MODE[/bold yellow]"
    )

    console.print(
        "[yellow]No cloud resources will be modified.[/yellow]"
    )

    if not cleanup_targets:
        console.print(
            "[green]No cleanup actions are proposed.[/green]"
        )
        return

    table = Table(
        title="Proposed Cleanup Actions",
        show_header=True,
        header_style="bold",
        show_lines=True,
    )

    table.add_column("Resource Type", no_wrap=True)
    table.add_column("Resource ID", no_wrap=True)
    table.add_column("Region", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Reason", overflow="fold")
    table.add_column("Proposed Action", overflow="fold")

    for finding in cleanup_targets:
        table.add_row(
            str(finding.get("resource_type", "")),
            str(finding.get("resource_id", "")),
            str(finding.get("region", "")),
            str(finding.get("status", "")),
            str(finding.get("reason", "")),
            str(finding.get("cleanup_action", "")),
        )

    console.print(table)

    console.print()
    console.print(
        f"[yellow]{len(cleanup_targets)} cleanup target(s) "
        "would be considered.[/yellow]"
    )

    console.print(
        "[green]Dry-run complete. No resources were modified.[/green]"
    )