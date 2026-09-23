from dataclasses import dataclass
from typing import Optional

@dataclass
class LocationModel:
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: Optional[str] = None
