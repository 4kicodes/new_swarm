from dataclasses import dataclass

@dataclass(frozen=True)
class MissionCreated:
    mission_id: str

@dataclass(frozen=True)
class MissionStarted:
    mission_id: str

@dataclass(frozen=True)
class MissionPaused:
    mission_id: str

@dataclass(frozen=True)
class MissionCompleted:
    mission_id: str

@dataclass(frozen=True)
class MissionCancelled:
    mission_id: str
