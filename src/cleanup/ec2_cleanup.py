from typing import Any

from src.cleanup.ec2_validator import validate_ec2_cleanup_target


def terminate_ec2_instance(
    ec2_client: Any,
    instance_id: str,
) -> dict[str, Any]:
    """
    Terminate an EC2 instance.
    """

    ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )

    return {
        "resource_type": "EC2",
        "resource_id": instance_id,
        "action": "terminated",
        "success": True,
    }


def execute_ec2_cleanup_target(
    ec2_client: Any,
    finding: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute cleanup for one validated EC2 target.

    Invalid EC2 findings are skipped.
    """

    is_valid, message = validate_ec2_cleanup_target(finding)

    if not is_valid:
        return {
            "resource_type": finding.get("resource_type"),
            "resource_id": finding.get("resource_id"),
            "action": "skipped",
            "success": False,
            "message": message,
        }

    resource_id = finding.get("resource_id")

    return terminate_ec2_instance(
        ec2_client,
        resource_id,
    )