from typing import Dict, List
from .models import Formation
from .exceptions import FormationNotFoundError, InvalidFormationConfiguration

class FormationRegistry:
    def __init__(self):
        self._formations: Dict[str, Formation] = {}

    def add(self, formation: Formation) -> None:
        if formation.formation_id in self._formations:
            raise InvalidFormationConfiguration(f"Formation {formation.formation_id} already exists.")
        self._formations[formation.formation_id] = formation

    def remove(self, formation_id: str) -> None:
        if formation_id not in self._formations:
            raise FormationNotFoundError(f"Formation {formation_id} not found.")
        del self._formations[formation_id]

    def get(self, formation_id: str) -> Formation:
        if formation_id not in self._formations:
            raise FormationNotFoundError(f"Formation {formation_id} not found.")
        return self._formations[formation_id]

    def list_all(self) -> List[Formation]:
        return list(self._formations.values())
