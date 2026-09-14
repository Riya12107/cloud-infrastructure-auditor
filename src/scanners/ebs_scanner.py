from src.scanners.base_scanner import BaseScanner


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

        Actual AWS scanning will be implemented in Week 2.
        """
        return []

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