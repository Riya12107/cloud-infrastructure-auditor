from datetime import datetime, timedelta, timezone

from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api, create_aws_client


class CloudWatchScanner(BaseScanner):
    """
    Scanner for AWS CloudWatch EC2 CPU utilization metrics.
    """

    LOOKBACK_DAYS = 14
    CLOUDWATCH_PERIOD = 86400
    CPU_THRESHOLD = 5.0

    METRIC_NAME = "CPUUtilization"
    NAMESPACE = "AWS/EC2"

    RESULT_FIELDS = [
        "resource_type",
        "resource_id",
        "region",
        "metric_name",
        "metric_value",
        "period",
        "reason",
    ]

    def __init__(self, instance_ids: list[str] | None = None):
        """
        Initialize the CloudWatch scanner.

        Args:
            instance_ids:
                EC2 instance IDs whose CloudWatch CPU metrics
                should be checked.
        """

        self.instance_ids = instance_ids or []

    def scan(self) -> list[dict]:
        """
        Collect average EC2 CPU utilization metrics
        over the previous 14 days.

        Instances with average CPU utilization below 5%
        are returned as findings.
        """

        if not self.instance_ids:
            return []

        cloudwatch_client = create_aws_client("cloudwatch")

        findings = []

        for instance_id in self.instance_ids:
            cpu_utilization = self.get_cpu_utilization(
                cloudwatch_client,
                instance_id,
            )

            if cpu_utilization < self.CPU_THRESHOLD:
                findings.append(
                    self.build_metric(
                        resource_id=instance_id,
                        region=cloudwatch_client.meta.region_name,
                        metric_name=self.METRIC_NAME,
                        metric_value=cpu_utilization,
                        period="14 days",
                        reason=(
                            "Average CPU utilization is below "
                            "5% over the last 14 days"
                        ),
                    )
                )

        return findings

    def get_cpu_utilization(
        self,
        cloudwatch_client,
        instance_id: str,
    ) -> float:
        """
        Retrieve the average CPU utilization for an EC2 instance
        over the previous 14 days.
        """

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=self.LOOKBACK_DAYS)

        response = self.fetch_metric_statistics(
            cloudwatch_client,
            Namespace=self.NAMESPACE,
            MetricName=self.METRIC_NAME,
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id,
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=self.CLOUDWATCH_PERIOD,
            Statistics=["Average"],
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return 0.0

        averages = [
            datapoint["Average"]
            for datapoint in datapoints
            if "Average" in datapoint
        ]

        if not averages:
            return 0.0

        return sum(averages) / len(averages)

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