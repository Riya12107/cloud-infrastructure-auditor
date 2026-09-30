from dataclasses import dataclass


@dataclass
class Finding:
    resource_id: str
    resource_type: str
    title: str
    severity: str
    description: str
    recommendation: str