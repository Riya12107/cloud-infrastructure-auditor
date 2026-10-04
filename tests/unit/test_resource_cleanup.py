from unittest.mock import Mock

from src.cleanup.resource_cleanup import (
    delete_ebs_volume,
    release_elastic_ip,
    execute_cleanup_target,
)


def test_delete_ebs_volume():
    ec2_client = Mock()

    result = delete_ebs_volume(
        ec2_client,
        "vol-123",
    )

    ec2_client.delete_volume.assert_called_once_with(
        VolumeId="vol-123"
    )

    assert result["resource_type"] == "EBS"
    assert result["resource_id"] == "vol-123"
    assert result["action"] == "deleted"
    assert result["success"] is True


def test_release_elastic_ip():
    ec2_client = Mock()

    result = release_elastic_ip(
        ec2_client,
        "eipalloc-123",
    )

    ec2_client.release_address.assert_called_once_with(
        AllocationId="eipalloc-123"
    )

    assert result["resource_type"] == "ElasticIP"
    assert result["resource_id"] == "eipalloc-123"
    assert result["action"] == "released"
    assert result["success"] is True


def test_execute_valid_ebs_cleanup():
    ec2_client = Mock()

    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-456",
        "region": "us-east-1",
        "status": "unused",
        "reason": "EBS volume is unattached",
        "cleanup_action": "Review and delete if no longer required",
    }

    result = execute_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.delete_volume.assert_called_once_with(
        VolumeId="vol-456"
    )

    assert result["success"] is True
    assert result["action"] == "deleted"


def test_execute_valid_elastic_ip_cleanup():
    ec2_client = Mock()

    finding = {
        "resource_type": "ElasticIP",
        "resource_id": "eipalloc-456",
        "region": "us-east-1",
        "status": "unused",
        "reason": "Elastic IP is unassociated",
        "cleanup_action": "Review and release if no longer required",
    }

    result = execute_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.release_address.assert_called_once_with(
        AllocationId="eipalloc-456"
    )

    assert result["success"] is True
    assert result["action"] == "released"


def test_execute_invalid_ebs_cleanup_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-invalid",
        "region": "us-east-1",
        "status": "attached",
        "reason": "EBS volume is attached",
        "cleanup_action": "",
    }

    result = execute_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.delete_volume.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"


def test_execute_invalid_elastic_ip_cleanup_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "ElasticIP",
        "resource_id": "eipalloc-invalid",
        "region": "us-east-1",
        "status": "associated",
        "reason": "Elastic IP is associated",
        "cleanup_action": "",
    }

    result = execute_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.release_address.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"


def test_execute_unsupported_resource_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "S3",
        "resource_id": "bucket-123",
        "region": "us-east-1",
        "status": "unused",
        "reason": "Unused resource",
        "cleanup_action": "Delete if no longer required",
    }

    result = execute_cleanup_target(
        ec2_client,
        finding,
    )

    assert result["success"] is False
    assert result["action"] == "skipped"

    ec2_client.delete_volume.assert_not_called()
    ec2_client.release_address.assert_not_called()