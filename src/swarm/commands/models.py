from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Command:
    name: str
    target: Optional[str] = None
    args: List[str] = None

    def __post_init__(self):
        if self.args is None:
            self.args = []
