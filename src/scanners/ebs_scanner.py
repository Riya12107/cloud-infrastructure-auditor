from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api


class EBSScanner(BaseScanner):
    """
    Scanner interface for AWS EBS volumes.
    """

    RESULT_FIELDS = [
        "resource_type",
        "resource_id",
        "region",
        "status",
        "reason",
        "cleanup_action",
    ]

    def scan(self) -> list[dict]:
        """
        Scan AWS EBS volumes.

        Actual AWS resource scanning will be implemented
        in Week 2.
        """
        return []

    def fetch_volumes(self, ec2_client) -> dict:
        """
        Fetch EBS volume information through the shared
        AWS API retry and rate-limit handler.
        """

        return call_aws_api(
            ec2_client.describe_volumes
        )

    def build_finding(
        self,
        resource_id: str,
        region: str,
        status: str,
        reason: str,
        cleanup_action: str,
    ) -> dict:
        """
        Build a standardized EBS audit finding.
        """

        return {
            "resource_type": "EBS",
            "resource_id": resource_id,
            "region": region,
            "status": status,
            "reason": reason,
            "cleanup_action": cleanup_action,
        }