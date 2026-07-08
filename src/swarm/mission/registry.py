from typing import Dict, List
from .models import Mission
from .exceptions import MissionNotFoundError, InvalidMissionConfiguration

class MissionRegistry:
    def __init__(self):
        self._missions: Dict[str, Mission] = {}

    def add(self, mission: Mission) -> None:
        if mission.mission_id in self._missions:
            raise InvalidMissionConfiguration(f"Mission {mission.mission_id} already exists.")
        self._missions[mission.mission_id] = mission

    def remove(self, mission_id: str) -> None:
        if mission_id not in self._missions:
            raise MissionNotFoundError(f"Mission {mission_id} not found.")
        del self._missions[mission_id]

    def get(self, mission_id: str) -> Mission:
        if mission_id not in self._missions:
            raise MissionNotFoundError(f"Mission {mission_id} not found.")
        return self._missions[mission_id]

    def list_all(self) -> List[Mission]:
        return list(self._missions.values())
