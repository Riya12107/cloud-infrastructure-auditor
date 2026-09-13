from src.scanners.base_scanner import BaseScanner


class CloudWatchScanner(BaseScanner):
    """
    Scanner for AWS CloudWatch metrics.
    """

    def scan(self) -> list[dict]:
        """
        Collect CloudWatch metrics used for utilization analysis.
        """
        raise NotImplementedError(
            "CloudWatch scanner is not implemented yet"
        )