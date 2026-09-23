from dataclasses import dataclass
from typing import List

@dataclass
class GuideModel:
    category: str
    title: str
    summary: str
    steps: List[str]
