from typing import Any


EC2_CPU_THRESHOLD = 5.0


def validate_ec2_cleanup_target(
    finding: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate whether an EC2 finding is a safe cleanup target.

    An EC2 cleanup candidate must be an underutilized instance
    with CPU utilization below the configured threshold.
    """

    resource_type = finding.get("resource_type")
    resource_id = finding.get("resource_id")
    status = finding.get("status")
    cpu_utilization = finding.get("cpu_utilization")
    cleanup_action = finding.get("cleanup_action")

    if resource_type != "EC2":
        return False, "Resource type is not EC2."

    if not resource_id:
        return False, "EC2 cleanup target does not have a resource ID."

    if status != "underutilized":
        return False, "EC2 resource is not marked as underutilized."

    if cpu_utilization is None:
        return False, "EC2 cleanup target does not have CPU utilization data."

    if cpu_utilization >= EC2_CPU_THRESHOLD:
        return False, "EC2 CPU utilization is not below the cleanup threshold."

    if not cleanup_action:
        return False, "EC2 cleanup target does not have a cleanup action."

    return True, "EC2 cleanup target is valid."