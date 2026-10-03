from src.cleanup.dry_run import get_dry_run_targets


def test_dry_run_includes_valid_ebs_target():
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

    targets = get_dry_run_targets(findings)

    assert len(targets) == 1
    assert targets[0]["resource_id"] == "vol-123"


def test_dry_run_includes_valid_elastic_ip_target():
    findings = [
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "region": "us-east-1",
            "status": "unused",
            "reason": "Elastic IP is unassociated",
            "cleanup_action": "Review and release if no longer required",
        }
    ]

    targets = get_dry_run_targets(findings)

    assert len(targets) == 1
    assert targets[0]["resource_id"] == "eipalloc-123"


def test_dry_run_includes_valid_ec2_target():
    findings = [
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "region": "us-east-1",
            "status": "underutilized",
            "reason": "Average CPU utilization is below 5%",
            "cpu_utilization": 2.5,
            "cleanup_action": "Review and consider stopping",
        }
    ]

    targets = get_dry_run_targets(findings)

    assert len(targets) == 1
    assert targets[0]["resource_id"] == "i-123"


def test_dry_run_excludes_normal_ec2_instance():
    findings = [
        {
            "resource_type": "EC2",
            "resource_id": "i-456",
            "region": "us-east-1",
            "status": "normal",
            "reason": "CPU utilization is normal",
            "cpu_utilization": 25.0,
            "cleanup_action": "",
        }
    ]

    targets = get_dry_run_targets(findings)

    assert targets == []


def test_dry_run_excludes_invalid_ebs_target():
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-456",
            "region": "us-east-1",
            "status": "attached",
            "reason": "EBS volume is attached",
            "cleanup_action": "",
        }
    ]

    targets = get_dry_run_targets(findings)

    assert targets == []


def test_dry_run_returns_empty_when_no_findings():
    targets = get_dry_run_targets([])

    assert targets == []