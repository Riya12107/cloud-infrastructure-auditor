from types import SimpleNamespace

from scanners.gcp_compute_scanner import get_gcp_compute_instances


class FakeGCPClient:
    def list(self, request):
        return [
            SimpleNamespace(
                name="instance-1",
                machine_type="e2-medium",
                status="RUNNING",
            ),
            SimpleNamespace(
                name="instance-2",
                machine_type="e2-small",
                status="TERMINATED",
            ),
        ]


def test_get_gcp_compute_instances(monkeypatch):
    monkeypatch.setattr(
        "scanners.gcp_compute_scanner.create_gcp_compute_client",
        lambda: FakeGCPClient(),
    )

    resources = get_gcp_compute_instances(
        project_id="test-project",
        zone="asia-south1-a",
    )

    assert len(resources) == 2
    assert resources[0].provider == "gcp"
    assert resources[0].resource_type == "compute_instance"
    assert resources[0].resource_id == "instance-1"
    assert resources[0].details["machine_type"] == "e2-medium"
    assert resources[0].details["status"] == "RUNNING"


def test_get_gcp_compute_instances_without_client(monkeypatch):
    monkeypatch.setattr(
        "scanners.gcp_compute_scanner.create_gcp_compute_client",
        lambda: None,
    )

    resources = get_gcp_compute_instances(
        project_id="test-project",
        zone="asia-south1-a",
    )

    assert resources == []