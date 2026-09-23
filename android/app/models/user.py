from dataclasses import dataclass
from typing import Optional

@dataclass
class UserModel:
    id: int
    email: str
    phone_number: str
    full_name: str
