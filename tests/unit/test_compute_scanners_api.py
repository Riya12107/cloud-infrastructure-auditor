from unittest.mock import Mock, patch
from unittest.mock import Mock

from src.scanners.cloudwatch_scanner import CloudWatchScanner
from src.scanners.ec2_scanner import EC2Scanner


def test_ec2_scanner_fetch_instances():
    client = Mock()

    client.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {"InstanceId": "i-test123"}
                ]
            }
        ]
    }

    scanner = EC2Scanner()

    result = scanner.fetch_instances(client)

    assert result["Reservations"][0]["Instances"][0]["InstanceId"] == "i-test123"
    client.describe_instances.assert_called_once()


def test_cloudwatch_scanner_fetch_metric_statistics():
    client = Mock()

    client.get_metric_statistics.return_value = {
        "Datapoints": [
            {"Average": 12.5}
        ]
    }

    scanner = CloudWatchScanner()

    result = scanner.fetch_metric_statistics(
        client,
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
    )

    assert result["Datapoints"][0]["Average"] == 12.5
    client.get_metric_statistics.assert_called_once()


def test_ec2_scanner_build_finding():
    scanner = EC2Scanner()

    result = scanner.build_finding(
        resource_id="i-test123",
        region="us-east-1",
        status="underutilized",
        reason="Low CPU utilization",
        cpu_utilization=8.5,
        cleanup_action="Review instance",
    )

    assert result["resource_type"] == "EC2"
    assert result["resource_id"] == "i-test123"
    assert result["region"] == "us-east-1"
    assert result["status"] == "underutilized"
    assert result["cpu_utilization"] == 8.5
    assert result["cleanup_action"] == "Review instance"


def test_cloudwatch_scanner_build_metric():
    scanner = CloudWatchScanner()

    result = scanner.build_metric(
        resource_id="i-test123",
        region="us-east-1",
        metric_name="CPUUtilization",
        metric_value=8.5,
        period="7 days",
        reason="Low average CPU utilization",
    )

    assert result["resource_type"] == "CloudWatch"
    assert result["resource_id"] == "i-test123"
    assert result["region"] == "us-east-1"
    assert result["metric_name"] == "CPUUtilization"
    assert result["metric_value"] == 8.5
    assert result["period"] == "7 days"
def test_cloudwatch_scanner_detects_underutilized_instance():
    scanner = CloudWatchScanner(
        instance_ids=["i-underutilized123", "i-normal123"]
    )

    mock_client = Mock()
    mock_client.meta.region_name = "us-east-1"

    with patch(
        "src.scanners.cloudwatch_scanner.create_aws_client",
        return_value=mock_client,
    ), patch.object(
        scanner,
        "get_cpu_utilization",
        side_effect=[2.5, 25.0],
    ):
        result = scanner.scan()

    assert len(result) == 1
    assert result[0]["resource_type"] == "CloudWatch"
    assert result[0]["resource_id"] == "i-underutilized123"
    assert result[0]["region"] == "us-east-1"
    assert result[0]["metric_name"] == "CPUUtilization"
    assert result[0]["metric_value"] == 2.5
    assert result[0]["period"] == "14 days"
    assert "5%" in result[0]["reason"]


def test_cloudwatch_scanner_returns_empty_without_instances():
    scanner = CloudWatchScanner()

    result = scanner.scan()

    assert result == []


def test_cloudwatch_scanner_calculates_cpu_average():
    scanner = CloudWatchScanner()

    mock_client = Mock()

    mock_client.get_metric_statistics.return_value = {
        "Datapoints": [
            {"Average": 2.0},
            {"Average": 4.0},
            {"Average": 6.0},
        ]
    }

    result = scanner.get_cpu_utilization(
        mock_client,
        "i-test123",
    )

    assert result == 4.0

    mock_client.get_metric_statistics.assert_called_once()