from unittest.mock import patch

from typer.testing import CliRunner

from src.cli.main import app


def test_audit_successful_authentication():
    runner = CliRunner()

    session_info = {
        "profile": "cloud-auditor",
        "region": "us-east-1",
    }

    mock_findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "unused",
        },
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "unused",
        },
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "status": "underutilized",
        },
    ]

    with patch(
        "src.cli.main.validate_aws_credentials",
        return_value=True,
    ), patch(
        "src.cli.main.get_aws_session_info",
        return_value=session_info,
    ), patch(
        "src.cli.main.ScannerManager"
    ) as mock_scanner_manager:

        mock_scanner_manager.return_value.run_all.return_value = mock_findings

        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "Starting cloud infrastructure audit..." in result.stdout
    assert "Checking AWS authentication..." in result.stdout
    assert "AWS authentication successful." in result.stdout
    assert "Profile: cloud-auditor" in result.stdout
    assert "Region: us-east-1" in result.stdout
    assert "Infrastructure scan completed." in result.stdout
    assert "Audit Summary" in result.stdout
    assert "Total findings" in result.stdout
    assert "3" in result.stdout

    mock_scanner_manager.return_value.run_all.assert_called_once()


def test_audit_failed_authentication():
    runner = CliRunner()

    with patch(
        "src.cli.main.validate_aws_credentials",
        return_value=False,
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 1
    assert "Starting cloud infrastructure audit..." in result.stdout
    assert "Checking AWS authentication..." in result.stdout
    assert "AWS authentication failed." in result.stdout
    assert "Please check your AWS credentials and configuration." in result.stdout