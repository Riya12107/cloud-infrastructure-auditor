from unittest.mock import patch

from src.scanners.scanner_manager import ScannerManager


def test_scanner_manager_combines_findings():
    """
    Verify that ScannerManager combines findings
    returned by all configured scanners.
    """

    ebs_findings = [
        {
            "resource_type": "EBS",
            "resource_id": "vol-123",
            "status": "unused",
        }
    ]

    elastic_ip_findings = [
        {
            "resource_type": "ElasticIP",
            "resource_id": "eipalloc-123",
            "status": "unused",
        }
    ]

    ec2_findings = [
        {
            "resource_type": "EC2",
            "resource_id": "i-123",
            "status": "underutilized",
        }
    ]

    with patch(
        "src.scanners.scanner_manager.EBSScanner.scan",
        return_value=ebs_findings,
    ), patch(
        "src.scanners.scanner_manager.ElasticIPScanner.scan",
        return_value=elastic_ip_findings,
    ), patch(
        "src.scanners.scanner_manager.EC2Scanner.scan",
        return_value=ec2_findings,
    ):

        manager = ScannerManager()

        findings = manager.run_all()

    assert len(findings) == 3
    assert findings[0]["resource_type"] == "EBS"
    assert findings[1]["resource_type"] == "ElasticIP"
    assert findings[2]["resource_type"] == "EC2"


def test_scanner_manager_returns_empty_when_no_findings():
    """
    Verify that the manager returns an empty list when
    no scanner reports any findings.
    """

    with patch(
        "src.scanners.scanner_manager.EBSScanner.scan",
        return_value=[],
    ), patch(
        "src.scanners.scanner_manager.ElasticIPScanner.scan",
        return_value=[],
    ), patch(
        "src.scanners.scanner_manager.EC2Scanner.scan",
        return_value=[],
    ):

        manager = ScannerManager()

        findings = manager.run_all()

    assert findings == []