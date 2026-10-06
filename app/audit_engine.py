from scanners.ec2_scanner import get_ec2_instances
from scanners.ebs_scanner import get_ebs_volumes
from scanners.elastic_ip_scanner import get_elastic_ips
from scanners.s3_scanner import get_s3_buckets

from analyzers.finding_analyzer import (
    analyze_ebs_volume,
    analyze_elastic_ip,
    analyze_ec2_utilization,
)
from scanners.ec2_scanner import get_cpu_utilizations

from app.config_loader import load_config
from scanners.gcp_compute_scanner import get_gcp_compute_instances












def run_audit():
    config = load_config()
    provider = config.get("provider", "aws")

    resources = {
        "ec2": get_ec2_instances(),
        "ebs": get_ebs_volumes(),
        "elastic_ips": get_elastic_ips(),
        "s3": get_s3_buckets(),
    }

    if provider == "gcp":
        gcp_config = config.get("gcp", {})
        project_id = gcp_config.get("project_id", "")
        zone = gcp_config.get("zone", "")

        if project_id and zone:
            resources["gcp_compute"] = get_gcp_compute_instances(
                project_id=project_id,
                zone=zone,
            )
        else:
            resources["gcp_compute"] = []

    findings = []

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

    summary = {
        resource_type: len(items)
        for resource_type, items in resources.items()
    }

    return {
        "resources": resources,
        "summary": summary,
        "findings": findings,
    }