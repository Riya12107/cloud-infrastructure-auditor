from scanners.ebs_scanner import get_ebs_volumes


def test_ebs_scanner_without_credentials():
    volumes = get_ebs_volumes()

    assert volumes == []