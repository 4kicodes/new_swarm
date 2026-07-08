from enum import Enum, auto

class FormationType(Enum):
    LINE = auto()
    COLUMN = auto()
    V = auto()
    GRID = auto()

class FormationStatus(Enum):
    CREATED = auto()
    CONFIGURED = auto()
    READY = auto()
    ACTIVE = auto()
    PAUSED = auto()
    STOPPED = auto()
