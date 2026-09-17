from src.scanners.ebs_scanner import EBSScanner
from src.scanners.elastic_ip_scanner import ElasticIPScanner
from src.scanners.ec2_scanner import EC2Scanner


class ScannerManager:
    """
    Coordinate all cloud infrastructure scanners.

    The manager runs each scanner and combines their
    findings into one list for the CLI audit flow.
    """

    def __init__(self):
        self.scanners = [
            EBSScanner(),
            ElasticIPScanner(),
            EC2Scanner(),
        ]

    def run_all(self) -> list[dict]:
        """
        Run all configured scanners.

        Returns:
            A combined list containing findings from
            all scanners.
        """

        findings = []

        for scanner in self.scanners:
            scanner_findings = scanner.scan()
            findings.extend(scanner_findings)

        return findings