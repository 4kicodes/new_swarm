from dataclasses import dataclass

@dataclass(frozen=True)
class ExecutionStarted:
    session_id: str

@dataclass(frozen=True)
class ExecutionPaused:
    session_id: str

@dataclass(frozen=True)
class ExecutionResumed:
    session_id: str

@dataclass(frozen=True)
class WaypointReached:
    session_id: str
    waypoint_index: int

@dataclass(frozen=True)
class ExecutionCompleted:
    session_id: str

@dataclass(frozen=True)
class ExecutionCancelled:
    session_id: str

@dataclass(frozen=True)
class ExecutionFailed:
    session_id: str
    reason: str
