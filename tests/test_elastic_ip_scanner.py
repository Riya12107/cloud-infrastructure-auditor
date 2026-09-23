from scanners.elastic_ip_scanner import get_elastic_ips


def test_elastic_ip_scanner_without_credentials():
    addresses = get_elastic_ips()

    assert addresses == []