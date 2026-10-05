from typer.testing import CliRunner

from app.main import app


def test_audit_command_exports_json(monkeypatch, tmp_path):
    result_data = {
        "summary": {
            "ec2": 0,
            "ebs": 0,
            "elastic_ips": 0,
            "s3": 0,
        },
        "findings": [],
    }

    monkeypatch.setattr(
        "app.main.run_audit",
        lambda: result_data,
    )

    output_file = tmp_path / "audit_report.json"

    monkeypatch.setattr(
        "app.main.export_json_report",
        lambda result: str(output_file),
    )

    runner = CliRunner()
    result = runner.invoke(app, ["audit"])

    assert result.exit_code == 0
    assert "JSON report saved to" in result.stdout