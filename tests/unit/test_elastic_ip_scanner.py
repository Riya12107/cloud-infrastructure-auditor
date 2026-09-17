from unittest.mock import Mock, patch

from src.scanners.elastic_ip_scanner import ElasticIPScanner


def test_elastic_ip_scanner_detects_unassociated_ip():
    scanner = ElasticIPScanner()

    mock_client = Mock()
    mock_client.meta.region_name = "us-east-1"

    mock_client.describe_addresses.return_value = {
        "Addresses": [
            {
                "AllocationId": "eipalloc-unassociated",
                "PublicIp": "203.0.113.10",
            },
            {
                "AllocationId": "eipalloc-associated",
                "PublicIp": "203.0.113.20",
                "AssociationId": "eipassoc-test123",
                "InstanceId": "i-test123",
            },
        ]
    }

    with patch(
        "src.scanners.elastic_ip_scanner.create_aws_client",
        return_value=mock_client,
    ):
        result = scanner.scan()

    assert len(result) == 1
    assert result[0]["resource_type"] == "ElasticIP"
    assert result[0]["resource_id"] == "eipalloc-unassociated"
    assert result[0]["region"] == "us-east-1"
    assert result[0]["status"] == "unused"
    assert "unassociated" in result[0]["reason"].lower()


def test_elastic_ip_scanner_ignores_associated_ip():
    scanner = ElasticIPScanner()

    mock_client = Mock()
    mock_client.meta.region_name = "us-east-1"

    mock_client.describe_addresses.return_value = {
        "Addresses": [
            {
                "AllocationId": "eipalloc-associated",
                "PublicIp": "203.0.113.20",
                "AssociationId": "eipassoc-test123",
                "InstanceId": "i-test123",
            }
        ]
    }

    with patch(
        "src.scanners.elastic_ip_scanner.create_aws_client",
        return_value=mock_client,
    ):
        result = scanner.scan()

    assert result == []