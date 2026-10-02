from models.finding import Finding


def analyze_ebs_volume(volume):
    if volume.get("attached"):
        return None

    return Finding(
        resource_id=volume.get("volume_id"),
        resource_type="ebs",
        title="Unattached EBS volume",
        severity="medium",
        description="The EBS volume is not attached to any EC2 instance.",
        recommendation="Review the volume and remove it if it is no longer required.",
    )
def analyze_elastic_ip(address):
    if address.get("associated"):
        return None

    return Finding(
        resource_id=address.get("allocation_id"),
        resource_type="elastic_ip",
        title="Unused Elastic IP",
        severity="medium",
        description="The Elastic IP is not associated with any resource.",
        recommendation="Release the Elastic IP if it is no longer required.",
    )
def analyze_ec2_utilization(instance):
    average_cpu = instance.get("average_cpu")

    if average_cpu is None:
        return None

    threshold = instance.get("threshold", 10)

    if average_cpu >= threshold:
        return None

    return Finding(
        resource_id=instance.get("instance_id"),
        resource_type="ec2",
        title="Underutilized EC2 instance",
        severity="low",
        description=f"Average CPU utilization is {average_cpu}%, below the configured threshold of {threshold}%.",
        recommendation="Review the instance and consider resizing or stopping it if it is no longer required.",
    )