from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api, create_aws_client


class ElasticIPScanner(BaseScanner):
    """
    Scanner for AWS Elastic IP addresses.
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
        Scan AWS Elastic IP addresses and identify
        unassociated Elastic IPs.
        """

        ec2_client = create_aws_client("ec2")

        response = self.fetch_addresses(ec2_client)

        findings = []

        for address in response.get("Addresses", []):
            allocation_id = address.get("AllocationId")

            # An Elastic IP without an AssociationId
            # is currently not associated with a resource.
            if not address.get("AssociationId"):
                findings.append(
                    self.build_finding(
                        resource_id=allocation_id,
                        region=ec2_client.meta.region_name,
                        status="unused",
                        reason="Elastic IP is unassociated",
                        cleanup_action="Review and release if no longer required",
                    )
                )

        return findings

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