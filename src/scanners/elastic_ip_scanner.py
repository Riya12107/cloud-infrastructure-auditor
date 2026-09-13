from src.scanners.base_scanner import BaseScanner


class ElasticIPScanner(BaseScanner):
    """
    Scanner for AWS Elastic IP addresses.
    """

    def scan(self) -> list[dict]:
        """
        Find unused Elastic IP addresses.
        """
        raise NotImplementedError(
            "Elastic IP scanner is not implemented yet"
        )