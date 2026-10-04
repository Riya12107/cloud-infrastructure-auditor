from app.audit_engine import run_audit


def test_run_audit_without_credentials():
    result = run_audit()

    assert "resources" in result
    assert "summary" in result

    assert "ec2" in result["resources"]
    assert "ebs" in result["resources"]
    assert "elastic_ips" in result["resources"]
    assert "s3" in result["resources"]
    assert isinstance(result["findings"], list)