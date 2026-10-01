from src.cleanup.validator import (
    validate_cleanup_target,
    validate_cleanup_targets,
)


def test_valid_ebs_cleanup_target():
    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-123",
        "status": "unused",
    }

    is_valid, message = validate_cleanup_target(finding)

    assert is_valid is True
    assert message == "Cleanup target is valid."


def test_valid_elastic_ip_cleanup_target():
    finding = {
        "resource_type": "ElasticIP",
        "resource_id": "eipalloc-123",
        "status": "unused",
    }

    is_valid, message = validate_cleanup_target(finding)

    assert is_valid is True
    assert message == "Cleanup target is valid."


def test_invalid_resource_type():
    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123",
        "status": "unused",
    }

    is_valid, message = validate_cleanup_target(finding)

    assert is_valid is False
    assert message == "Resource type is not supported for cleanup."


def test_missing_resource_id():
    finding = {
        "resource_type": "EBS",
        "resource_id": "",
        "status": "unused",
    }

    is_valid, message = validate_cleanup_target(finding)

    assert is_valid is False
    assert message == "Cleanup target does not have a resource ID."


def test_resource_not_unused():
    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-123",
        "status": "active",
    }

    is_valid, message = validate_cleanup_target(finding)

    assert is_valid is False
    assert message == "Resource is not marked as unused."


def test_validate_multiple_cleanup_targets():
    findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "unused",
        },
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "unused",
        },
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "status": "underutilized",
        },
    ]

    valid_targets = validate_cleanup_targets(findings)

    assert len(valid_targets) == 2
    assert valid_targets[0]["resource_id"] == "vol-123"
    assert valid_targets[1]["resource_id"] == "eipalloc-123"