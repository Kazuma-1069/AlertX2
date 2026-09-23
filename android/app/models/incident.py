from dataclasses import dataclass
from typing import Optional

@dataclass
class IncidentModel:
    incident_uuid: str
    status: str
    initial_latitude: float
    initial_longitude: float
    trigger_type: str
