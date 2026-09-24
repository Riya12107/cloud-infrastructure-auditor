from unittest.mock import patch

from app.cloudwatch_client import get_cpu_utilization


@patch("app.cloudwatch_client.create_aws_session")
def test_cpu_utilization_from_cloudwatch(mock_session):
    mock_cloudwatch = mock_session.return_value.client.return_value

    mock_cloudwatch.get_metric_data.return_value = {
        "MetricDataResults": [
            {
                "Values": [5.0, 10.0, 15.0]
            }
        ]
    }

    result = get_cpu_utilization("i-test123")

    assert result == 10.0