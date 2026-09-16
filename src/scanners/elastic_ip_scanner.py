from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api


class ElasticIPScanner(BaseScanner):
    """
    Scanner interface for AWS Elastic IP addresses.
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
        Scan AWS Elastic IP addresses.

        Actual AWS resource scanning will be implemented
        in Week 2.
        """
        return []

    def fetch_addresses(self, ec2_client) -> dict:
        """
        Fetch Elastic IP information through the shared
        AWS API retry and rate-limit handler.
        """

        return call_aws_api(
            ec2_client.describe_addresses
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
        Build a standardized Elastic IP audit finding.
        """

        return {
            "resource_type": "ElasticIP",
            "resource_id": resource_id,
            "region": region,
            "status": status,
            "reason": reason,
            "cleanup_action": cleanup_action,
        }