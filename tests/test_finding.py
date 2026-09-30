from models.finding import Finding


def test_finding_creation():
    finding = Finding(
        resource_id="vol-test123",
        resource_type="ebs",
        title="Unattached EBS volume",
        severity="medium",
        description="The volume is not attached to any EC2 instance.",
        recommendation="Review and remove the volume if it is no longer required.",
    )

    assert finding.resource_id == "vol-test123"
    assert finding.resource_type == "ebs"
    assert finding.severity == "medium"
    assert finding.title == "Unattached EBS volume"