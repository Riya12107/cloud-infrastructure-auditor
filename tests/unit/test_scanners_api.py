from unittest.mock import Mock

from src.scanners.ebs_scanner import EBSScanner
from src.scanners.elastic_ip_scanner import ElasticIPScanner


def test_ebs_scanner_fetch_volumes():
    client = Mock()
    client.describe_volumes.return_value = {
        "Volumes": [
            {"VolumeId": "vol-test"}
        ]
    }

    scanner = EBSScanner()

    result = scanner.fetch_volumes(client)

    assert result["Volumes"][0]["VolumeId"] == "vol-test"
    client.describe_volumes.assert_called_once()


def test_elastic_ip_scanner_fetch_addresses():
    client = Mock()
    client.describe_addresses.return_value = {
        "Addresses": [
            {"PublicIp": "54.0.0.1"}
        ]
    }

    scanner = ElasticIPScanner()

    result = scanner.fetch_addresses(client)

    assert result["Addresses"][0]["PublicIp"] == "54.0.0.1"
    client.describe_addresses.assert_called_once()
    