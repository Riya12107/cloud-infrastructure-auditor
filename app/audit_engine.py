from scanners.ec2_scanner import get_ec2_instances
from scanners.ebs_scanner import get_ebs_volumes
from scanners.elastic_ip_scanner import get_elastic_ips
from scanners.s3_scanner import get_s3_buckets


def run_audit():
    resources = {
        "ec2": get_ec2_instances(),
        "ebs": get_ebs_volumes(),
        "elastic_ips": get_elastic_ips(),
        "s3": get_s3_buckets(),
    }

    summary = {
        resource_type: len(items)
        for resource_type, items in resources.items()
    }

    return {
        "resources": resources,
        "summary": summary,
    }