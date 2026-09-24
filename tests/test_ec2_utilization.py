from unittest.mock import patch

from analyzers.ec2_utilization import (
    analyze_cpu_utilization,
    check_instance_utilization,
)


def test_underutilized_instance():
    result = analyze_cpu_utilization("i-test123", 5.0)

    assert result["status"] == "potentially_underutilized"
    assert result["average_cpu"] == 5.0


def test_normal_instance():
    result = analyze_cpu_utilization("i-test456", 25.0)

    assert result["status"] == "normal"
    assert result["average_cpu"] == 25.0


def test_missing_cpu_data():
    result = analyze_cpu_utilization("i-test789", None)

    assert result["status"] == "insufficient_data"
    assert result["average_cpu"] is None


@patch("analyzers.ec2_utilization.get_cpu_utilization")
def test_check_instance_utilization(mock_cpu):
    mock_cpu.return_value = 5.0

    result = check_instance_utilization("i-test999")

    assert result["status"] == "potentially_underutilized"
    assert result["average_cpu"] == 5.0
@patch("analyzers.ec2_utilization.get_cpu_utilization")
def test_check_instance_utilization_uses_config(mock_cpu):
    mock_cpu.return_value = 8.0

    result = check_instance_utilization("i-config-test")

    assert result["threshold"] == 10
    assert result["status"] == "potentially_underutilized"