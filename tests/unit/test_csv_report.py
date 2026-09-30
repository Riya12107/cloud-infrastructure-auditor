import csv

from src.reports.csv_report import export_findings_to_csv


def test_export_findings_to_csv(tmp_path):
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

    output_path = tmp_path / "audit_report.csv"

    export_findings_to_csv(
        findings,
        output_path,
    )

    assert output_path.exists()

    with output_path.open(
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 1
    assert rows[0]["resource_type"] == "EBS"
    assert rows[0]["resource_id"] == "vol-123"
    assert rows[0]["region"] == "us-east-1"
    assert rows[0]["status"] == "unused"


def test_export_empty_findings_to_csv(tmp_path):
    output_path = tmp_path / "empty_report.csv"

    export_findings_to_csv(
        [],
        output_path,
    )

    assert output_path.exists()

    with output_path.open(
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows == []