from src.scanners.ebs_scanner import EBSScanner
from src.scanners.elastic_ip_scanner import ElasticIPScanner


EXPECTED_REPORT_FIELDS = {
    "resource_type",
    "resource_id",
    "region",
    "status",
    "reason",
    "cleanup_action",
}


def test_ebs_finding_is_report_compatible():
    scanner = EBSScanner()

    finding = scanner.build_finding(
        resource_id="vol-123",
        region="us-east-1",
        status="unused",
        reason="EBS volume is unattached",
        cleanup_action="Review and delete if no longer required",
    )

    assert EXPECTED_REPORT_FIELDS.issubset(finding.keys())


def test_elastic_ip_finding_is_report_compatible():
    scanner = ElasticIPScanner()

    finding = scanner.build_finding(
        resource_id="eipalloc-123",
        region="us-east-1",
        status="unused",
        reason="Elastic IP is unassociated",
        cleanup_action="Review and release if no longer required",
    )

    assert EXPECTED_REPORT_FIELDS.issubset(finding.keys())

from src.scanners.ec2_scanner import EC2Scanner
from src.scanners.cloudwatch_scanner import CloudWatchScanner


def test_ec2_finding_is_report_compatible():
    scanner = EC2Scanner()

    finding = scanner.build_finding(
        resource_id="i-123",
        region="us-east-1",
        status="underutilized",
        reason="Average CPU utilization is below 5%",
        cpu_utilization=2.5,
        cleanup_action=(
            "Review and consider stopping, downsizing, "
            "or terminating if no longer required"
        ),
    )

    assert EXPECTED_REPORT_FIELDS.issubset(finding.keys())

    assert finding["resource_type"] == "EC2"
    assert finding["resource_id"] == "i-123"
    assert finding["cpu_utilization"] == 2.5


def test_cloudwatch_metric_is_report_compatible():
    scanner = CloudWatchScanner()

    metric = scanner.build_metric(
        resource_id="i-123",
        region="us-east-1",
        metric_name="CPUUtilization",
        metric_value=2.5,
        period="14 days",
        reason="Average CPU utilization is below 5%",
    )

    expected_fields = {
        "resource_type",
        "resource_id",
        "region",
        "metric_name",
        "metric_value",
        "period",
        "reason",
    }

    assert expected_fields.issubset(metric.keys())

    assert metric["resource_type"] == "CloudWatch"
    assert metric["metric_name"] == "CPUUtilization"
    assert metric["metric_value"] == 2.5