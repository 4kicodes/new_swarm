from dataclasses import dataclass, field
from typing import List, Optional, Dict
from swarm.planning import Waypoint
from .types import MissionType, MissionStatus

@dataclass(frozen=True)
class MissionGoal:
    goal_id: str
    waypoint: Waypoint
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class MissionPlan:
    goals: List[MissionGoal] = field(default_factory=list)

@dataclass(frozen=True)
class Mission:
    mission_id: str
    name: str
    mission_type: MissionType
    formation_id: Optional[str] = None
    enabled: bool = True
    plan: Optional[MissionPlan] = None

@dataclass(frozen=True)
class MissionProgress:
    current_goal_index: int = 0
    completed_goals: List[str] = field(default_factory=list)
    remaining_goals: List[str] = field(default_factory=list)
    status: MissionStatus = MissionStatus.CREATED
