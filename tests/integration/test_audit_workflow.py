from unittest.mock import patch

from typer.testing import CliRunner

from src.cli.main import app


runner = CliRunner()


@patch("src.cli.main.export_findings_to_json")
@patch("src.cli.main.export_findings_to_csv")
@patch("src.cli.main.ScannerManager")
@patch("src.cli.main.get_aws_session_info")
@patch("src.cli.main.validate_aws_credentials")
def test_complete_audit_workflow(
    mock_validate_credentials,
    mock_session_info,
    mock_scanner_manager,
    mock_export_csv,
    mock_export_json,
):
    """
    Test the complete audit workflow:
    authentication -> scanning -> report export -> summary.

    AWS operations are mocked, so no real AWS resources are accessed.
    """

    # 1. Mock successful AWS authentication
    mock_validate_credentials.return_value = True

    # 2. Mock AWS session information
    mock_session_info.return_value = {
        "profile": "test-profile",
        "region": "us-east-1",
    }

    # 3. Create sample findings
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Delete volume",
        },
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "Elastic IP is not associated",
            "cleanup_action": "Release Elastic IP",
        },
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "region": "us-east-1",
            "status": "underutilized",
            "reason": "EC2 instance is underutilized",
            "cleanup_action": "Review instance",
        },
    ]

    # 4. Mock the scanner
    mock_scanner_manager.return_value.run_all.return_value = findings

    # 5. Run the complete audit command
    result = runner.invoke(app, ["audit"])

    # 6. Verify successful execution
    assert result.exit_code == 0, result.output

    assert "Starting cloud infrastructure audit" in result.output
    assert "AWS authentication successful" in result.output
    assert "Infrastructure scan completed" in result.output
    assert "Audit Summary" in result.output
    assert "Total findings" in result.output

    # 7. Verify authentication and scanning
    mock_validate_credentials.assert_called_once()
    mock_session_info.assert_called_once()
    mock_scanner_manager.return_value.run_all.assert_called_once()

    # 8. Verify CSV report export
    mock_export_csv.assert_called_once_with(
        findings,
        "reports/audit_report.csv",
    )

    # 9. Verify JSON report export
    mock_export_json.assert_called_once_with(
        findings,
        "reports/audit_report.json",
    )


@patch("src.cli.main.display_dry_run")
@patch("src.cli.main.ScannerManager")
@patch("src.cli.main.get_aws_session_info")
@patch("src.cli.main.validate_aws_credentials")
def test_dry_run_workflow(
    mock_validate_credentials,
    mock_session_info,
    mock_scanner_manager,
    mock_display_dry_run,
):
    """
    Verify that dry-run mode completes without executing cleanup.
    """

    # 1. Mock successful authentication
    mock_validate_credentials.return_value = True

    # 2. Mock AWS session information
    mock_session_info.return_value = {
        "profile": "test-profile",
        "region": "us-east-1",
    }

    # 3. Create a sample finding
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Delete volume",
        }
    ]

    # 4. Mock scanner results
    mock_scanner_manager.return_value.run_all.return_value = findings

    # 5. Run dry-run mode and prevent real cleanup
    with patch("src.cli.main.execute_cleanup_targets") as mock_execute:
        result = runner.invoke(app, ["audit", "--dry-run"])

    # 6. Verify successful execution
    assert result.exit_code == 0, result.output
    assert "Starting cloud infrastructure audit" in result.output
    assert "Audit Summary" in result.output

    # 7. Verify dry-run was called with the findings
    mock_display_dry_run.assert_called_once_with(findings)

    # 8. Verify cleanup was never executed
    mock_execute.assert_not_called()

    # 9. Verify authentication and scanning
    mock_validate_credentials.assert_called_once()
    mock_session_info.assert_called_once()
    mock_scanner_manager.return_value.run_all.assert_called_once()