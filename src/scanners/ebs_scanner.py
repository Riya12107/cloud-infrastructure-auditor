from src.scanners.base_scanner import BaseScanner


class EBSScanner(BaseScanner):
    """
    Scanner for AWS EBS volumes.
    """

    def scan(self) -> list[dict]:
        """
        Find unused or relevant EBS volumes.
        """
        raise NotImplementedError("EBS scanner is not implemented yet")