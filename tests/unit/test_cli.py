from unittest.mock import patch

from typer.testing import CliRunner

from src.cli.main import app


runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "v0.1.0" in result.stdout


@patch("src.cli.main.ScannerManager")
@patch("src.cli.main.get_aws_session_info")
@patch("src.cli.main.validate_aws_credentials")
def test_audit(
    mock_validate_credentials,
    mock_session_info,
    mock_scanner_manager,
):
    """
    Verify that the audit command authenticates with AWS,
    runs the scanner manager, and displays the audit summary.
    """

    mock_validate_credentials.return_value = True

    mock_session_info.return_value = {
        "profile": "test-profile",
        "region": "us-east-1",
    }

    mock_scanner_manager.return_value.run_all.return_value = [
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

    result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0

    assert "Starting cloud infrastructure audit" in result.stdout
    assert "AWS authentication successful" in result.stdout
    assert "Infrastructure scan completed" in result.stdout
    assert "Audit Summary" in result.stdout
    assert "Total findings" in result.stdout
    assert "3" in result.stdout

    mock_validate_credentials.assert_called_once()
    mock_scanner_manager.return_value.run_all.assert_called_once()


@patch("src.cli.main.validate_aws_credentials")
def test_audit_authentication_failure(mock_validate_credentials):
    """
    Verify that the audit command stops when AWS authentication fails.
    """

    mock_validate_credentials.return_value = False

    result = runner.invoke(app, ["audit"])

    assert result.exit_code == 1
    assert "AWS authentication failed" in result.stdout
@patch("src.cli.main.execute_cleanup_targets")
@patch("src.cli.main.ScannerManager")
@patch("src.cli.main.get_aws_session_info")
@patch("src.cli.main.validate_aws_credentials")
def test_execute_wrong_confirmation_cancels_cleanup(
    mock_validate_credentials,
    mock_session_info,
    mock_scanner_manager,
    mock_execute_cleanup_targets,
):
    mock_validate_credentials.return_value = True

    mock_session_info.return_value = {
        "profile": "test-profile",
        "region": "us-east-1",
    }

    mock_scanner_manager.return_value.run_all.return_value = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Delete volume",
        }
    ]

    result = runner.invoke(
        app,
        ["audit", "--execute"],
        input="NO\n",
    )

    assert result.exit_code == 0

    assert "EXECUTE MODE" in result.stdout

    assert "Type CONFIRM to continue" in result.stdout

    assert "Cleanup cancelled" in result.stdout

    assert "No cloud resources were modified" in result.stdout

    mock_execute_cleanup_targets.assert_not_called()
@patch("src.cli.main.execute_cleanup_targets")
@patch("src.cli.main.ScannerManager")
@patch("src.cli.main.get_aws_session_info")
@patch("src.cli.main.validate_aws_credentials")
def test_execute_correct_confirmation_runs_cleanup(
    mock_validate_credentials,
    mock_session_info,
    mock_scanner_manager,
    mock_execute_cleanup_targets,
):
    mock_validate_credentials.return_value = True

    mock_session_info.return_value = {
        "profile": "test-profile",
        "region": "us-east-1",
    }

    mock_scanner_manager.return_value.run_all.return_value = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Delete volume",
        }
    ]

    mock_execute_cleanup_targets.return_value = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "action": "deleted",
            "success": True,
        }
    ]

    result = runner.invoke(
        app,
        ["audit", "--execute"],
        input="CONFIRM\n",
    )

    assert result.exit_code == 0

    assert "EXECUTE MODE" in result.stdout

    assert "Type CONFIRM to continue" in result.stdout

    assert "Confirmation accepted" in result.stdout

    assert "Successful cleanup actions: 1" in result.stdout

    mock_execute_cleanup_targets.assert_called_once_with(
        mock_scanner_manager.return_value.run_all.return_value
    )