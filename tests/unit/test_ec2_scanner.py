from unittest.mock import Mock, patch

from src.scanners.ec2_scanner import EC2Scanner


def test_ec2_scanner_detects_underutilized_instance():
    scanner = EC2Scanner()

    mock_client = Mock()
    mock_client.meta.region_name = "us-east-1"

    mock_client.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-underutilized123",
                        "State": {
                            "Name": "running"
                        },
                    },
                    {
                        "InstanceId": "i-normal123",
                        "State": {
                            "Name": "running"
                        },
                    },
                ]
            }
        ]
    }

    with patch(
        "src.scanners.ec2_scanner.create_aws_client",
        return_value=mock_client,
    ), patch.object(
        scanner,
        "get_cpu_utilization",
        side_effect=[2.5, 25.0],
    ):
        result = scanner.scan()

    assert len(result) == 1
    assert result[0]["resource_type"] == "EC2"
    assert result[0]["resource_id"] == "i-underutilized123"
    assert result[0]["region"] == "us-east-1"
    assert result[0]["status"] == "underutilized"
    assert result[0]["cpu_utilization"] == 2.5
    assert "5%" in result[0]["reason"]


def test_ec2_scanner_ignores_normal_instance():
    scanner = EC2Scanner()

    mock_client = Mock()
    mock_client.meta.region_name = "us-east-1"

    mock_client.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-normal123",
                        "State": {
                            "Name": "running"
                        },
                    }
                ]
            }
        ]
    }

    with patch(
        "src.scanners.ec2_scanner.create_aws_client",
        return_value=mock_client,
    ), patch.object(
        scanner,
        "get_cpu_utilization",
        return_value=25.0,
    ):
        result = scanner.scan()

    assert result == []
def test_get_cpu_utilization_calculates_average():
    scanner = EC2Scanner()

    mock_cloudwatch = Mock()

    mock_cloudwatch.get_metric_statistics.return_value = {
        "Datapoints": [
            {"Average": 2.0},
            {"Average": 4.0},
            {"Average": 6.0},
        ]
    }

    result = scanner.get_cpu_utilization(
        mock_cloudwatch,
        "i-test123",
    )

    assert result == 4.0

    mock_cloudwatch.get_metric_statistics.assert_called_once()