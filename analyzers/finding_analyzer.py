from models.finding import Finding
from app.cost_estimator import (
    estimate_monthly_cost,
    estimate_monthly_savings,
)


def analyze_ebs_volume(volume):
    if volume.get("attached"):
        return None

    monthly_cost = estimate_monthly_cost("ebs", volume)
    monthly_savings = estimate_monthly_savings("ebs", volume)

    return Finding(
        resource_id=volume.get("volume_id"),
        resource_type="ebs",
        title="Unattached EBS volume",
        severity="medium",
        description="The EBS volume is not attached to any EC2 instance.",
        recommendation="Review the volume and remove it if it is no longer required.",
        estimated_monthly_cost=monthly_cost,
        estimated_monthly_savings=monthly_savings,
    )


def analyze_elastic_ip(address):
    if address.get("associated"):
        return None

    monthly_cost = estimate_monthly_cost("elastic_ip", address)
    monthly_savings = estimate_monthly_savings("elastic_ip", address)

    return Finding(
        resource_id=address.get("allocation_id"),
        resource_type="elastic_ip",
        title="Unused Elastic IP",
        severity="medium",
        description="The Elastic IP is not associated with any resource.",
        recommendation="Release the Elastic IP if it is no longer required.",
        estimated_monthly_cost=monthly_cost,
        estimated_monthly_savings=monthly_savings,
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
        description=(
            f"Average CPU utilization is {average_cpu}%, "
            f"below the configured threshold of {threshold}%."
        ),
        recommendation=(
            "Review the instance and consider resizing or stopping it "
            "if it is no longer required."
        ),
    )
def analyze_gcp_compute_instance(instance):
    status = instance.details.get("status")

    if status not in {"TERMINATED", "STOPPED"}:
        return None

    return Finding(
        resource_id=instance.resource_id,
        resource_type="gcp_compute",
        title="Stopped GCP Compute instance",
        severity="medium",
        description=(
            f"The GCP Compute instance is currently {status.lower()} "
            "and may no longer be required."
        ),
        recommendation=(
            "Review the instance and delete it if it is no longer needed."
        ),
    )