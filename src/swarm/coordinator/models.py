from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CoordinatorSession:
    mission_id: Optional[str] = None
    formation_id: Optional[str] = None
    active: bool = False
