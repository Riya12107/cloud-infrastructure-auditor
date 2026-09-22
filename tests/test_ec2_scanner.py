from scanners.ec2_scanner import get_ec2_instances


def test_ec2_scanner_without_credentials():
    instances = get_ec2_instances()

    assert instances == []