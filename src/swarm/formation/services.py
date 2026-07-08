from typing import Dict
from swarm.planning import Position
from .geometry import generate_offsets
from .models import Formation
from .registry import FormationRegistry

class FormationGeometryService:
    def __init__(self, registry: FormationRegistry):
        self.registry = registry

    def recompute(self, formation_id: str) -> Dict[str, Position]:
        formation = self.registry.get(formation_id)
        if not formation.leader_id:
            return {}
        
        return generate_offsets(
            formation.formation_type,
            formation.leader_id,
            formation.follower_ids,
            formation.spacing
        )
