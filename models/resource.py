from dataclasses import dataclass
from typing import Any


@dataclass
class CloudResource:
    provider: str
    resource_type: str
    resource_id: str
    details: dict[str, Any]