from typer.testing import CliRunner
from src.cli.main import app


runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "v0.1.0" in result.stdout


def test_audit():
    result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "Starting cloud infrastructure audit" in result.stdout