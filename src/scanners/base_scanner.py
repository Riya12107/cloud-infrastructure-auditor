from abc import ABC, abstractmethod


class BaseScanner(ABC):
    """
    Base interface for all cloud infrastructure scanners.
    """

    @abstractmethod
    def scan(self) -> list[dict]:
        """
        Scan the cloud resource and return audit findings.
        """
        raise NotImplementedError