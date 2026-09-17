from datetime import datetime, timedelta, timezone

from src.scanners.base_scanner import BaseScanner
from src.utils.aws_helpers import call_aws_api, create_aws_client


class EC2Scanner(BaseScanner):
    """
    Scanner for AWS EC2 instances.

    Identifies running instances with average CPU utilization
    below 5% over the previous 14 days.
    """

    CPU_THRESHOLD = 5.0
    LOOKBACK_DAYS = 14
    CLOUDWATCH_PERIOD = 86400

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
        Scan EC2 instances and identify underutilized instances.
        """

        ec2_client = create_aws_client("ec2")
        cloudwatch_client = create_aws_client("cloudwatch")

        response = self.fetch_instances(ec2_client)

        findings = []

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):

                instance_id = instance.get("InstanceId")
                state = instance.get("State", {}).get("Name")

                # Only running instances are evaluated for
                # CPU-based underutilization.
                if state != "running":
                    continue

                cpu_utilization = self.get_cpu_utilization(
                    cloudwatch_client,
                    instance_id,
                )

                if cpu_utilization < self.CPU_THRESHOLD:
                    findings.append(
                        self.build_finding(
                            resource_id=instance_id,
                            region=ec2_client.meta.region_name,
                            status="underutilized",
                            reason=(
                                "Average CPU utilization is below "
                                "5% over the last 14 days"
                            ),
                            cpu_utilization=cpu_utilization,
                            cleanup_action=(
                                "Review and consider stopping, "
                                "downsizing, or terminating if no longer required"
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
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
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

    def fetch_instances(self, ec2_client) -> dict:
        """
        Fetch EC2 instance information through the shared
        AWS API retry and rate-limit handler.
        """

        return call_aws_api(
            ec2_client.describe_instances
        )

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