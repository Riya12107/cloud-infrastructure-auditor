from analyzers.finding_analyzer import (
    analyze_ebs_volume,
    analyze_elastic_ip,
    analyze_ec2_utilization,
)


def test_unattached_ebs_volume_creates_finding():
    volume = {
        "volume_id": "vol-test123",
        "volume_type": "gp3",
        "size": 20,
        "state": "available",
        "attached": False,
    }

    finding = analyze_ebs_volume(volume)

    assert finding is not None
    assert finding.resource_id == "vol-test123"
    assert finding.resource_type == "ebs"
    assert finding.title == "Unattached EBS volume"
    assert finding.severity == "medium"


def test_attached_ebs_volume_has_no_finding():
    volume = {
        "volume_id": "vol-test123",
        "volume_type": "gp3",
        "size": 20,
        "state": "in-use",
        "attached": True,
    }

    finding = analyze_ebs_volume(volume)

    assert finding is None



def test_unused_elastic_ip_creates_finding():
    address = {
        "public_ip": "203.0.113.10",
        "allocation_id": "eipalloc-test123",
        "associated": False,
    }

    finding = analyze_elastic_ip(address)

    assert finding is not None
    assert finding.resource_id == "eipalloc-test123"
    assert finding.resource_type == "elastic_ip"
    assert finding.title == "Unused Elastic IP"
    assert finding.severity == "medium"


def test_associated_elastic_ip_has_no_finding():
    address = {
        "public_ip": "203.0.113.10",
        "allocation_id": "eipalloc-test123",
        "associated": True,
    }

    finding = analyze_elastic_ip(address)

    assert finding is None

def test_underutilized_ec2_creates_finding():
    instance = {
        "instance_id": "i-test123",
        "average_cpu": 5.0,
        "threshold": 10,
    }

    finding = analyze_ec2_utilization(instance)

    assert finding is not None
    assert finding.resource_id == "i-test123"
    assert finding.resource_type == "ec2"
    assert finding.title == "Underutilized EC2 instance"
    assert finding.severity == "low"


def test_normal_ec2_has_no_finding():
    instance = {
        "instance_id": "i-test123",
        "average_cpu": 25.0,
        "threshold": 10,
    }

    finding = analyze_ec2_utilization(instance)

    assert finding is None


def test_ec2_without_cpu_data_has_no_finding():
    instance = {
        "instance_id": "i-test123",
        "average_cpu": None,
        "threshold": 10,
    }

    finding = analyze_ec2_utilization(instance)

    assert finding is None