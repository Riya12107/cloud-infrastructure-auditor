from src.scanners.base_scanner import BaseScanner


class EC2Scanner(BaseScanner):
    """
    Scanner for AWS EC2 instances.
    """

    def scan(self) -> list[dict]:
        """
        Find EC2 instances that may be underutilized.
        """
        raise NotImplementedError(
            "EC2 scanner is not implemented yet"
        )