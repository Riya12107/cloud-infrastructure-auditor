from app.cloudwatch_client import get_cpu_utilization
from app.config_loader import load_config


def analyze_cpu_utilization(instance_id, average_cpu, threshold=10):
    if average_cpu is None:
        return {
            "instance_id": instance_id,
            "status": "insufficient_data",
            "average_cpu": None,
        }

    if average_cpu < threshold:
        status = "potentially_underutilized"
    else:
        status = "normal"

    return {
        "instance_id": instance_id,
        "status": status,
        "average_cpu": average_cpu,
        "threshold": threshold,
    }


def check_instance_utilization(instance_id, threshold=None, days=7):
    config = load_config()

    if threshold is None:
        threshold = config.get("thresholds", {}).get("ec2_cpu", 10)

    average_cpu = get_cpu_utilization(instance_id, days)

    return analyze_cpu_utilization(
        instance_id,
        average_cpu,
        threshold,
    )