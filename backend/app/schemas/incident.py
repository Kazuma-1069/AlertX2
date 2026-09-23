from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class IncidentSummary(BaseModel):
    total_incidents: int
    active_incidents: int
    resolved_incidents: int
    last_incident_time: Optional[datetime] = None
