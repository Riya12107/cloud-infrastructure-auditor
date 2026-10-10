
from models.finding import Finding
from app.cleanup_preview import display_cleanup_preview


def test_cleanup_preview_displays_ebs_recommendation(capsys):
    finding = Finding(
        resource_id="vol-test123",
        resource_type="ebs",
        title="Unattached EBS volume",
        severity="medium",
        description="The volume is not attached.",
        recommendation="Review before deleting.",
        estimated_monthly_cost=8.0,
        estimated_monthly_savings=8.0,
    )

    display_cleanup_preview([finding])

    output = capsys.readouterr().out

    assert "Safe Cleanup Preview" in output
    assert "vol-test123" in output
    assert "Unattached EBS volume" in output
    assert "Preview completed" in output
    assert "no resources were modified" in output.lower()


def test_cleanup_preview_handles_no_findings(capsys):
    display_cleanup_preview([])

    output = capsys.readouterr().out

    assert "No cleanup recommendations to preview" in output
    assert "Preview completed" in output
