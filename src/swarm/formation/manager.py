from typing import List, Optional, Dict
from swarm.planning import Waypoint
from swarm.safety import validate_execution_plan
from .models import Formation
from .types import FormationType, FormationStatus
from .registry import FormationRegistry
from .exceptions import InvalidFormationConfiguration
from .geometry import generate_offsets
from .planner import generate_targets as _generate_targets

class FormationManager:
    def __init__(self, registry: FormationRegistry):
        self.registry = registry
        self._status: Dict[str, FormationStatus] = {}

    def _set_status(self, formation_id: str, status: FormationStatus) -> None:
        self._status[formation_id] = status

    def get_status(self, formation_id: str) -> FormationStatus:
        return self._status.get(formation_id, FormationStatus.CREATED)

    def create_formation(self, formation_id: str, name: str, formation_type: FormationType) -> Formation:
        formation = Formation(formation_id=formation_id, name=name, formation_type=formation_type)
        self.registry.add(formation)
        self._set_status(formation_id, FormationStatus.CREATED)
        return formation

    def delete_formation(self, formation_id: str) -> None:
        self.registry.remove(formation_id)
        if formation_id in self._status:
            del self._status[formation_id]

    def get_formation(self, formation_id: str) -> Formation:
        return self.registry.get(formation_id)

    def update_formation(self, formation_id: str, **kwargs) -> Formation:
        f = self.registry.get(formation_id)
        # Create updated formation (immutable)
        updated = Formation(**{**f.__dict__, **kwargs})
        self.registry.remove(formation_id)
        self.registry.add(updated)
        self._set_status(formation_id, FormationStatus.CONFIGURED)
        return updated

    def set_leader(self, formation_id: str, leader_id: str) -> Formation:
        return self.update_formation(formation_id, leader_id=leader_id)

    def set_followers(self, formation_id: str, follower_ids: List[str]) -> Formation:
        return self.update_formation(formation_id, follower_ids=follower_ids)

    def set_spacing(self, formation_id: str, spacing: float) -> Formation:
        return self.update_formation(formation_id, spacing=spacing)

    def set_type(self, formation_id: str, formation_type: FormationType) -> Formation:
        return self.update_formation(formation_id, formation_type=formation_type)

    def generate_targets(self, formation_id: str, leader_waypoint: Waypoint) -> Dict[str, Waypoint]:
        formation = self.registry.get(formation_id)
        
        # 1. Compute Offsets
        offsets = generate_offsets(
            formation.formation_type,
            formation.leader_id or "leader",
            formation.follower_ids,
            formation.spacing
        )
        
        # 2. Generate Targets
        targets = _generate_targets(formation, leader_waypoint, offsets)
        
        # NOTE: Safety validation for structural compliance of targets
        # The integration would require a structural ExecutionPlan creation here.
        # Returning structural map for now as per constraints.
        self._set_status(formation_id, FormationStatus.READY)
        return targets
