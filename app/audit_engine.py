
import logging

from scanners.ec2_scanner import (
    get_ec2_instances,
    get_cpu_utilizations,
)
from scanners.ebs_scanner import get_ebs_volumes
from scanners.elastic_ip_scanner import get_elastic_ips
from scanners.s3_scanner import get_s3_buckets
from scanners.gcp_compute_scanner import get_gcp_compute_instances

from analyzers.finding_analyzer import (
    analyze_ebs_volume,
    analyze_elastic_ip,
    analyze_ec2_utilization,
    analyze_gcp_compute_instance,
)

from app.config_loader import load_config
from app.aws_connection import create_aws_session

logger = logging.getLogger(__name__)


def run_audit():
    """Scan the selected cloud provider and return an audit result."""

    config = load_config()

    empty_result = {
        "resources": {},
        "summary": {},
        "findings": [],
        "status": "failed",
        "errors": [],
    }

    if not config:
        empty_result["errors"].append(
            "Configuration is missing or invalid."
        )
        return empty_result

    provider = str(config.get("provider", "aws")).lower()
    errors = []
    findings = []

    if provider == "aws":
        resources = {
            "ec2": [],
            "ebs": [],
            "elastic_ips": [],
            "s3": [],
        }

        # Stop early when AWS credentials are unavailable.
        if create_aws_session(region_name=config.get("region")) is None:
            empty_result["resources"] = resources
            empty_result["summary"] = {
                resource_type: 0
                for resource_type in resources
            }
            empty_result["errors"].append(
                "AWS credentials were not found. "
                "Configure AWS credentials and run the audit again."
            )
            return empty_result

        scanners = {
            "ec2": get_ec2_instances,
            "ebs": get_ebs_volumes,
            "elastic_ips": get_elastic_ips,
            "s3": get_s3_buckets,
        }

        # Continue scanning other resource types if one scan fails.
        for resource_type, scanner in scanners.items():
            try:
                result = scanner()
                if result is None:
                    raise RuntimeError(
                        "Scanner returned no result."
                    )
                resources[resource_type] = result
            except Exception as exc:
                logger.exception(
                    "Failed to scan AWS resource type: %s",
                    resource_type,
                )
                errors.append(
                    f"Failed to scan {resource_type}: {exc}"
                )

        for volume in resources["ebs"]:
            try:
                finding = analyze_ebs_volume(volume)
                if finding:
                    findings.append(finding)
            except Exception as exc:
                logger.exception("Failed to analyze EBS volume")
                errors.append(f"Failed to analyze an EBS volume: {exc}")

        for address in resources["elastic_ips"]:
            try:
                finding = analyze_elastic_ip(address)
                if finding:
                    findings.append(finding)
            except Exception as exc:
                logger.exception("Failed to analyze Elastic IP")
                errors.append(f"Failed to analyze an Elastic IP: {exc}")

        instance_ids = [
            instance["instance_id"]
            for instance in resources["ec2"]
            if instance.get("instance_id")
        ]

        cpu_utilizations = {}

        if instance_ids:
            try:
                cpu_utilizations = get_cpu_utilizations(instance_ids)
            except Exception as exc:
                logger.exception("Failed to retrieve EC2 CPU metrics")
                errors.append(
                    f"Failed to retrieve EC2 CPU metrics: {exc}"
                )

        for instance in resources["ec2"]:
            instance_id = instance.get("instance_id")
            instance["average_cpu"] = cpu_utilizations.get(instance_id)

            try:
                finding = analyze_ec2_utilization(instance)
                if finding:
                    findings.append(finding)
            except Exception as exc:
                logger.exception("Failed to analyze EC2 instance")
                errors.append(
                    f"Failed to analyze EC2 instance {instance_id}: {exc}"
                )

    elif provider == "gcp":
        gcp_config = config.get("gcp", {})
        project_id = gcp_config.get("project_id", "")
        zone = gcp_config.get("zone", "")

        resources = {"gcp_compute": []}

        if not project_id or not zone:
            errors.append(
                "GCP project_id and zone must be configured."
            )
        else:
            try:
                result = get_gcp_compute_instances(
                    project_id=project_id,
                    zone=zone,
                )
                if result is None:
                    raise RuntimeError(
                        "GCP scanner returned no result."
                    )
                resources["gcp_compute"] = result
            except Exception as exc:
                logger.exception("Failed to scan GCP compute instances")
                errors.append(
                    f"Failed to scan GCP compute instances: {exc}"
                )

            for instance in resources["gcp_compute"]:
                try:
                    finding = analyze_gcp_compute_instance(instance)
                    if finding:
                        findings.append(finding)
                except Exception as exc:
                    logger.exception(
                        "Failed to analyze GCP compute instance"
                    )
                    errors.append(
                        f"Failed to analyze a GCP compute instance: {exc}"
                    )

    else:
        empty_result["errors"].append(
            f"Unsupported cloud provider: {provider}"
        )
        return empty_result

    summary = {
        resource_type: len(items)
        for resource_type, items in resources.items()
    }

    if errors and any(summary.values()):
        status = "incomplete"
    elif errors:
        status = "failed"
    else:
        status = "success"

    return {
        "resources": resources,
        "summary": summary,
        "findings": findings,
        "status": status,
        "errors": errors,
    }
