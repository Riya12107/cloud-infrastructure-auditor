from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api


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

    def fetch_metric_statistics(
        self,
        cloudwatch_client,
        **kwargs,
    ) -> dict:
        """
        Fetch CloudWatch metric statistics through the shared
        AWS API retry and rate-limit handler.
        """

        return call_aws_api(
            cloudwatch_client.get_metric_statistics,
            **kwargs,
        )

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