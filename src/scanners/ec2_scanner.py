from src.scanners.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):
    """
    Scanner interface for AWS EC2 instances.
    """

    RESULT_FIELDS = [
        "resource_type",
        "resource_id",
        "region",
        "status",
        "reason",
        "cpu_utilization",
        "cleanup_action",
    ]

    def scan(self) -> list[dict]:
        """
        Scan AWS EC2 instances.

        Actual AWS scanning will be implemented in Week 2.
        """
        return []

    def build_finding(
        self,
        resource_id: str,
        region: str,
        status: str,
        reason: str,
        cpu_utilization: float,
        cleanup_action: str,
    ) -> dict:
        """
        Build a standardized EC2 audit finding.
        """

        return {
            "resource_type": "EC2",
            "resource_id": resource_id,
            "region": region,
            "status": status,
            "reason": reason,
            "cpu_utilization": cpu_utilization,
            "cleanup_action": cleanup_action,
        }