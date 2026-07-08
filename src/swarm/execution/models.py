from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict
from datetime import datetime
from swarm.planning import ExecutionPlan

class ExecutionStatus(Enum):
    CREATED = auto()
    READY = auto()
    RUNNING = auto()
    WAITING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

@dataclass
class ExecutionSession:
    session_id: str
    execution_plan: ExecutionPlan
    current_waypoint_index: int = 0
    status: ExecutionStatus = ExecutionStatus.CREATED
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    retry_counter: int = 0
    metadata: Dict[str, str] = field(default_factory=dict)

