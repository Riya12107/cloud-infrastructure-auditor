from typing import Any

from src.cleanup.validator import validate_cleanup_target
from src.utils.aws_helpers import call_aws_api


def release_elastic_ip(
    ec2_client: Any,
    allocation_id: str,
) -> dict[str, Any]:
    """
    Release an Elastic IP address using the shared AWS API helper.
    """

    call_aws_api(
        ec2_client.release_address,
        AllocationId=allocation_id,
    )

    return {
        "resource_type": "ElasticIP",
        "resource_id": allocation_id,
        "action": "released",
        "success": True,
    }


def delete_ebs_volume(
    ec2_client: Any,
    volume_id: str,
) -> dict[str, Any]:
    """
    Delete an EBS volume using the shared AWS API helper.
    """

    call_aws_api(
        ec2_client.delete_volume,
        VolumeId=volume_id,
    )

    return {
        "resource_type": "EBS",
        "resource_id": volume_id,
        "action": "deleted",
        "success": True,
    }


def execute_cleanup_target(
    ec2_client: Any,
    finding: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute cleanup for one validated EBS or Elastic IP target.

    Invalid or unsupported resources are skipped.
    """

    is_valid, message = validate_cleanup_target(finding)

    if not is_valid:
        return {
            "resource_type": finding.get("resource_type"),
            "resource_id": finding.get("resource_id"),
            "action": "skipped",
            "success": False,
            "message": message,
        }

    resource_type = finding.get("resource_type")
    resource_id = finding.get("resource_id")

    if resource_type == "EBS":
        return delete_ebs_volume(
            ec2_client,
            resource_id,
        )

    if resource_type == "ElasticIP":
        return release_elastic_ip(
            ec2_client,
            resource_id,
        )

    return {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "action": "skipped",
        "success": False,
        "message": "Unsupported cleanup resource type.",
    }