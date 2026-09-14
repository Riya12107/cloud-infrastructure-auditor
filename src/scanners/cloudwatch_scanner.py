from src.scanners.base_scanner import BaseScanner


class CloudWatchScanner(BaseScanner):
    """
    Scanner interface for AWS CloudWatch metrics.
    """

    RESULT_FIELDS = [
        "resource_type",
        "resource_id",
        "region",
        "metric_name",
        "metric_value",
        "period",
        "reason",
    ]

    def scan(self) -> list[dict]:
        """
        Collect CloudWatch metrics.

        Actual CloudWatch metric collection will be implemented
        in Week 2.
        """
        return []

    def build_metric(
        self,
        resource_id: str,
        region: str,
        metric_name: str,
        metric_value: float,
        period: str,
        reason: str,
    ) -> dict:
        """
        Build a standardized CloudWatch metric result.
        """

        return {
            "resource_type": "CloudWatch",
            "resource_id": resource_id,
            "region": region,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "period": period,
            "reason": reason,
        }