from dataclasses import dataclass
from typing import Optional

@dataclass
class ContactModel:
    id: Optional[int]
    name: str
    phone_number: str
    relationship: str = "Friend"
    is_primary: bool = False
