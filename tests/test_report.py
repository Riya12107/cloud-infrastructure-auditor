from app.report import display_audit_report
from models.finding import Finding


def test_display_audit_report(capsys):
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

    display_audit_report(result)

    output = capsys.readouterr().out

    assert "Resource Summary" in output
    assert "Unattached EBS volume" in output
    assert "MEDIUM" in output
    assert "$8.00" in output
    assert "Total potential monthly savings" in output