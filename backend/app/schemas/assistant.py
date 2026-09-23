from typing import Optional, List
from pydantic import BaseModel

class AssistantQueryRequest(BaseModel):
    user_message: str
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    situation_context: Optional[str] = None

class AssistantQueryResponse(BaseModel):
    response: str
    suggested_actions: List[str]
    call_emergency_services: bool
    quick_tips: List[str]
