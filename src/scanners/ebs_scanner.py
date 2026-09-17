from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api, create_aws_client


class EBSScanner(BaseScanner):
    """
    Scanner for AWS EBS volumes.
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
        Scan AWS EBS volumes and identify unattached volumes.
        """

        ec2_client = create_aws_client("ec2")

        response = self.fetch_volumes(ec2_client)

        findings = []

        for volume in response.get("Volumes", []):
            volume_id = volume.get("VolumeId")
            state = volume.get("State")

            if state == "available":
                findings.append(
                    self.build_finding(
                        resource_id=volume_id,
                        region=ec2_client.meta.region_name,
                        status="unused",
                        reason="EBS volume is unattached",
                        cleanup_action="Review and delete if no longer required",
                    )
                )

        return findings

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