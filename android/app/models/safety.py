from dataclasses import dataclass

@dataclass
class SafetyTimerModel:
    id: int
    title: str
    duration_minutes: int
    is_active: bool
