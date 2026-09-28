from unittest.mock import patch

from src.reports.terminal_report import display_findings


def test_display_findings():
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Review and delete if no longer required",
        },
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "Elastic IP is unassociated",
            "cleanup_action": "Review and release if no longer required",
        },
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "region": "us-east-1",
            "status": "underutilized",
            "reason": "Average CPU utilization is below 5%",
            "cleanup_action": "Review and consider stopping or downsizing",
        },
    ]

    with patch(
        "src.reports.terminal_report.console.print"
    ) as mock_print:

        display_findings(findings)

        mock_print.assert_called_once()

        table = mock_print.call_args[0][0]

        assert table.title == "Cloud Infrastructure Audit Findings"
        assert len(table.rows) == 3


def test_display_findings_empty():

    with patch(
        "src.reports.terminal_report.console.print"
    ) as mock_print:

        display_findings([])

        mock_print.assert_called_once_with(
            "[yellow]No audit findings found.[/yellow]"
        )