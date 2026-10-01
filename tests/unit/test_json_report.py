import json

from src.reports.json_report import export_findings_to_json


def test_export_findings_to_json(tmp_path):
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "EBS volume is unattached",
            "cleanup_action": "Review and delete if no longer required",
        }
    ]

    output_path = tmp_path / "audit_report.json"

    export_findings_to_json(
        findings,
        output_path,
    )

    assert output_path.exists()

    with output_path.open(
        mode="r",
        encoding="utf-8",
    ) as json_file:
        data = json.load(json_file)

    assert len(data) == 1
    assert data[0]["resource_type"] == "EBS"
    assert data[0]["resource_id"] == "vol-123"
    assert data[0]["region"] == "us-east-1"
    assert data[0]["status"] == "unused"


def test_export_empty_findings_to_json(tmp_path):
    output_path = tmp_path / "empty_report.json"

    export_findings_to_json(
        [],
        output_path,
    )

    assert output_path.exists()

    with output_path.open(
        mode="r",
        encoding="utf-8",
    ) as json_file:
        data = json.load(json_file)

    assert data == []