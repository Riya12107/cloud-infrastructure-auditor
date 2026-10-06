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
def test_run_audit_with_gcp_provider(monkeypatch):
    config = {
        "provider": "gcp",
        "gcp": {
            "project_id": "test-project",
            "zone": "asia-south1-a",
        },
    }

    monkeypatch.setattr(
        "app.audit_engine.load_config",
        lambda: config,
    )

    monkeypatch.setattr(
        "app.audit_engine.get_gcp_compute_instances",
        lambda project_id, zone: [
            {
                "resource_id": "instance-1",
                "provider": "gcp",
            }
        ],
    )

    result = run_audit()

    assert "gcp_compute" in result["resources"]
    assert len(result["resources"]["gcp_compute"]) == 1