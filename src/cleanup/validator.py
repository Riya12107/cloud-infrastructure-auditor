from typing import Any


SUPPORTED_CLEANUP_TYPES = {
    "EBS",
    "ElasticIP",
}


def validate_cleanup_target(
    finding: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate whether an audit finding is a safe cleanup target.

    Cleanup is allowed only for supported resource types that
    have a resource ID and are explicitly marked as unused.
    """

    resource_type = finding.get("resource_type")
    resource_id = finding.get("resource_id")
    status = finding.get("status")

    if resource_type not in SUPPORTED_CLEANUP_TYPES:
        return False, "Resource type is not supported for cleanup."

    if not resource_id:
        return False, "Cleanup target does not have a resource ID."

    if status != "unused":
        return False, "Resource is not marked as unused."

    return True, "Cleanup target is valid."


def validate_cleanup_targets(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Validate multiple audit findings and return only valid
    cleanup targets.
    """

    valid_targets = []

    for finding in findings:
        is_valid, _ = validate_cleanup_target(finding)

        if is_valid:
            valid_targets.append(finding)

    return valid_targets