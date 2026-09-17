from unittest.mock import Mock, patch

from src.scanners.ebs_scanner import EBSScanner


def test_ebs_scanner_detects_unattached_volume():
    scanner = EBSScanner()

    mock_client = Mock()

    mock_client.describe_volumes.return_value = {
        "Volumes": [
            {
                "VolumeId": "vol-unattached",
                "State": "available",
            },
            {
                "VolumeId": "vol-attached",
                "State": "in-use",
            },
        ]
    }

    with patch(
        "src.scanners.ebs_scanner.create_aws_client",
        return_value=mock_client,
    ):
        result = scanner.scan()

    assert len(result) == 1
    assert result[0]["resource_type"] == "EBS"
    assert result[0]["resource_id"] == "vol-unattached"
    assert result[0]["status"] == "unused"
    assert "unattached" in result[0]["reason"].lower()


def test_ebs_scanner_ignores_attached_volume():
    scanner = EBSScanner()

    mock_client = Mock()

    mock_client.describe_volumes.return_value = {
        "Volumes": [
            {
                "VolumeId": "vol-attached",
                "State": "in-use",
            }
        ]
    }

    with patch(
        "src.scanners.ebs_scanner.create_aws_client",
        return_value=mock_client,
    ):
        result = scanner.scan()

    assert result == []