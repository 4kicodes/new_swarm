from dataclasses import dataclass, field
from typing import List, Optional
from swarm.planning import Position
from .types import FormationType

@dataclass(frozen=True)
class FormationAssignment:
    drone_id: str
    role: str
    offset: Optional[Position] = None

@dataclass(frozen=True)
class Formation:
    formation_id: str
    name: str
    formation_type: FormationType
    leader_id: Optional[str] = None
    follower_ids: List[str] = field(default_factory=list)
    spacing: float = 5.0
    enabled: bool = True
