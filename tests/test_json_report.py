import json

from app.json_report import export_json_report
from models.finding import Finding


def test_export_json_report(tmp_path):
    finding = Finding(
        resource_id="vol-001",
        resource_type="ebs",
        title="Unattached EBS volume",
        severity="medium",
        description="Unused volume",
        recommendation="Remove if no longer required.",
        estimated_monthly_cost=8.0,
        estimated_monthly_savings=8.0,
    )

    result = {
        "summary": {
            "ec2": 2,
            "ebs": 1,
            "elastic_ips": 1,
            "s3": 3,
        },
        "findings": [finding],
    }

    output_file = tmp_path / "audit_report.json"

    export_json_report(result, output_file)

    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["summary"]["ec2"] == 2
    assert data["summary"]["ebs"] == 1
    assert len(data["findings"]) == 1
    assert data["findings"][0]["resource_id"] == "vol-001"
    assert data["findings"][0]["estimated_monthly_savings"] == 8.0