from unittest.mock import patch

from typer.testing import CliRunner

from src.cli.main import app


def test_audit_successful_authentication():
    runner = CliRunner()

    session_info = {
        "profile": "cloud-auditor",
        "region": "us-east-1",
    }

    with patch(
        "src.cli.main.validate_aws_credentials",
        return_value=True,
    ), patch(
        "src.cli.main.get_aws_session_info",
        return_value=session_info,
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "Starting cloud infrastructure audit..." in result.stdout
    assert "Checking AWS authentication..." in result.stdout
    assert "AWS authentication successful." in result.stdout
    assert "Profile: cloud-auditor" in result.stdout
    assert "Region: us-east-1" in result.stdout


def test_audit_failed_authentication():
    runner = CliRunner()

    with patch(
        "src.cli.main.validate_aws_credentials",
        return_value=False,
    ):
        result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "Starting cloud infrastructure audit..." in result.stdout
    assert "Checking AWS authentication..." in result.stdout
    assert "AWS authentication failed." in result.stdout
    assert "Please check your AWS credentials and configuration." in result.stdout