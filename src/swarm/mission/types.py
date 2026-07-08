from enum import Enum, auto

class MissionStatus(Enum):
    CREATED = auto()
    PLANNED = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    FAILED = auto()

class MissionType(Enum):
    WAYPOINT = auto()
    PATROL = auto()
    SURVEY = auto()
