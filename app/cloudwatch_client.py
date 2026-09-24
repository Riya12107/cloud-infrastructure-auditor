from datetime import datetime, timedelta, timezone

from app.aws_connection import create_aws_session


def get_cpu_utilization(instance_id, days=7):
    session = create_aws_session()

    if session is None:
        return None

    cloudwatch = session.client("cloudwatch")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "cpu",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": "CPUUtilization",
                        "Dimensions": [
                            {
                                "Name": "InstanceId",
                                "Value": instance_id,
                            }
                        ],
                    },
                    "Period": 3600,
                    "Stat": "Average",
                },
                "ReturnData": True,
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    results = response.get("MetricDataResults", [])

    if not results or not results[0].get("Values"):
        return None

    values = results[0]["Values"]

    return sum(values) / len(values)