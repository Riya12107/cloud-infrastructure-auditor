
from scanners.ec2_scanner import get_ec2_instances
from scanners.ebs_scanner import get_ebs_volumes
from scanners.elastic_ip_scanner import get_elastic_ips
from scanners.s3_scanner import get_s3_buckets
from scanners.ec2_scanner import get_cpu_utilizations
from scanners.gcp_compute_scanner import get_gcp_compute_instances

from analyzers.finding_analyzer import (
    analyze_ebs_volume,
    analyze_elastic_ip,
    analyze_ec2_utilization,
    analyze_gcp_compute_instance,
)

from app.config_loader import load_config


def run_audit():
    config = load_config()
    provider = config.get("provider", "aws")

    # Collect resources from the selected cloud provider
    if provider == "aws":
        resources = {
            "ec2": get_ec2_instances(),
            "ebs": get_ebs_volumes(),
            "elastic_ips": get_elastic_ips(),
            "s3": get_s3_buckets(),
        }

    elif provider == "gcp":
        gcp_config = config.get("gcp", {})
        project_id = gcp_config.get("project_id", "")
        zone = gcp_config.get("zone", "")

        resources = {"gcp_compute": []}

        if project_id and zone:
            resources["gcp_compute"] = get_gcp_compute_instances(
                project_id=project_id,
                zone=zone,
            )

    else:
        raise ValueError(
            f"Unsupported cloud provider: {provider}"
        )

    # Analyze resources and generate findings
    findings = []

    if provider == "aws":
        for volume in resources["ebs"]:
            finding = analyze_ebs_volume(volume)
            if finding:
                findings.append(finding)

        for address in resources["elastic_ips"]:
            finding = analyze_elastic_ip(address)
            if finding:
                findings.append(finding)

        instance_ids = [
            instance["instance_id"]
            for instance in resources["ec2"]
            if instance.get("instance_id")
        ]

        cpu_utilizations = get_cpu_utilizations(instance_ids)

        for instance in resources["ec2"]:
            instance_id = instance.get("instance_id")
            average_cpu = cpu_utilizations.get(instance_id)
            instance["average_cpu"] = average_cpu

            finding = analyze_ec2_utilization(instance)
            if finding:
                findings.append(finding)

    elif provider == "gcp":
        for instance in resources["gcp_compute"]:
            finding = analyze_gcp_compute_instance(instance)
            if finding:
                findings.append(finding)

    # Summarize the collected resources
    summary = {
        resource_type: len(items)
        for resource_type, items in resources.items()
    }

    return {
        "resources": resources,
        "summary": summary,
        "findings": findings,
    }
