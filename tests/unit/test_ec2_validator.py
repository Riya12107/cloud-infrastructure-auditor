from src.cleanup.ec2_validator import (
    validate_ec2_cleanup_target,
)


def test_valid_ec2_cleanup_target():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "underutilized",
        "cpu_utilization": 2.5,
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is True
    assert message == "EC2 cleanup target is valid."


def test_invalid_resource_type():
    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-123",
        "status": "underutilized",
        "cpu_utilization": 2.5,
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "Resource type is not EC2."


def test_missing_ec2_resource_id():
    finding = {
        "resource_type": "EC2",
        "resource_id": "",
        "status": "underutilized",
        "cpu_utilization": 2.5,
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "EC2 cleanup target does not have a resource ID."


def test_ec2_not_underutilized():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "normal",
        "cpu_utilization": 2.5,
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "EC2 resource is not marked as underutilized."


def test_missing_cpu_utilization():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "underutilized",
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "EC2 cleanup target does not have CPU utilization data."


def test_cpu_utilization_at_threshold_is_invalid():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "underutilized",
        "cpu_utilization": 5.0,
        "cleanup_action": "Review and consider stopping",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "EC2 CPU utilization is not below the cleanup threshold."


def test_missing_cleanup_action():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "underutilized",
        "cpu_utilization": 2.5,
        "cleanup_action": "",
    }

    is_valid, message = validate_ec2_cleanup_target(finding)

    assert is_valid is False
    assert message == "EC2 cleanup target does not have a cleanup action."