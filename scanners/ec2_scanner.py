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