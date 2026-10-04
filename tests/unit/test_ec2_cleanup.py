from unittest.mock import Mock

from src.cleanup.ec2_cleanup import (
    execute_ec2_cleanup_target,
    terminate_ec2_instance,
)


def test_terminate_ec2_instance():
    ec2_client = Mock()

    result = terminate_ec2_instance(
        ec2_client,
        "i-123456",
    )

    ec2_client.terminate_instances.assert_called_once_with(
        InstanceIds=["i-123456"]
    )

    assert result["resource_type"] == "EC2"
    assert result["resource_id"] == "i-123456"
    assert result["action"] == "terminated"
    assert result["success"] is True


def test_execute_valid_ec2_cleanup():
    ec2_client = Mock()

    finding = {
        "resource_type": "EC2",
        "resource_id": "i-123456",
        "region": "us-east-1",
        "status": "underutilized",
        "reason": "Average CPU utilization is below 5% over the last 14 days",
        "cpu_utilization": 2.5,
        "cleanup_action": (
            "Review and consider stopping, downsizing, "
            "or terminating if no longer required"
        ),
    }

    result = execute_ec2_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.terminate_instances.assert_called_once_with(
        InstanceIds=["i-123456"]
    )

    assert result["resource_type"] == "EC2"
    assert result["resource_id"] == "i-123456"
    assert result["action"] == "terminated"
    assert result["success"] is True


def test_execute_high_cpu_ec2_cleanup_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "EC2",
        "resource_id": "i-highcpu",
        "region": "us-east-1",
        "status": "underutilized",
        "reason": "Average CPU utilization is below threshold",
        "cpu_utilization": 8.5,
        "cleanup_action": "Review EC2 instance",
    }

    result = execute_ec2_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.terminate_instances.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"


def test_execute_non_ec2_cleanup_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "EBS",
        "resource_id": "vol-123",
        "region": "us-east-1",
        "status": "unused",
        "cpu_utilization": 1.0,
        "cleanup_action": "Delete volume",
    }

    result = execute_ec2_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.terminate_instances.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"


def test_execute_ec2_without_cpu_data_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "EC2",
        "resource_id": "i-nocpu",
        "region": "us-east-1",
        "status": "underutilized",
        "reason": "CPU data unavailable",
        "cleanup_action": "Review EC2 instance",
    }

    result = execute_ec2_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.terminate_instances.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"


def test_execute_ec2_without_resource_id_is_skipped():
    ec2_client = Mock()

    finding = {
        "resource_type": "EC2",
        "resource_id": "",
        "region": "us-east-1",
        "status": "underutilized",
        "cpu_utilization": 2.0,
        "cleanup_action": "Review EC2 instance",
    }

    result = execute_ec2_cleanup_target(
        ec2_client,
        finding,
    )

    ec2_client.terminate_instances.assert_not_called()

    assert result["success"] is False
    assert result["action"] == "skipped"