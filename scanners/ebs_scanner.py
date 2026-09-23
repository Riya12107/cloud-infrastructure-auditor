from app.aws_connection import create_aws_session


def get_ebs_volumes():
    session = create_aws_session()

    if session is None:
        return []

    ec2 = session.client("ec2")

    response = ec2.describe_volumes()

    volumes = []

    for volume in response.get("Volumes", []):
        volumes.append({
            "volume_id": volume.get("VolumeId"),
            "volume_type": volume.get("VolumeType"),
            "size": volume.get("Size"),
            "state": volume.get("State"),
            "attached": bool(volume.get("Attachments")),
        })

    return volumes