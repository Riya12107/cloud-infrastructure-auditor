from dataclasses import dataclass
from typing import Optional


@dataclass
class Finding:
    resource_id: str
    resource_type: str
    title: str
    severity: str
    description: str
    recommendation: str
    estimated_monthly_cost: Optional[float] = None
    estimated_monthly_savings: Optional[float] = None