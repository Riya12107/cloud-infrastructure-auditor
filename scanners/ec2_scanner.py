from app.aws_connection import create_aws_session


def get_ec2_instances():
    session = create_aws_session()

    if session is None:
        return []

    ec2 = session.client("ec2")

    response = ec2.describe_instances()

    instances = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instances.append({
                "instance_id": instance.get("InstanceId"),
                "instance_type": instance.get("InstanceType"),
                "state": instance.get("State", {}).get("Name"),
            })

    return instances


def get_cpu_utilizations(instance_ids, cloudwatch_client=None):
    if not instance_ids:
        return {}

    if cloudwatch_client is None:
        session = create_aws_session()

        if session is None:
            return {}

        cloudwatch_client = session.client("cloudwatch")

    metric_queries = []

    for index, instance_id in enumerate(instance_ids):
        metric_queries.append({
            "Id": f"cpu_{index}",
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
        })

    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=None,
        EndTime=None,
    )

    results = {}

    for index, instance_id in enumerate(instance_ids):
        result_id = f"cpu_{index}"

        for metric_result in response.get("MetricDataResults", []):
            if metric_result.get("Id") == result_id:
                values = metric_result.get("Values", [])

                if values:
                    results[instance_id] = sum(values) / len(values)

                break

    return results