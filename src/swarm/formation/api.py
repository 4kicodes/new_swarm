from typing import List, Dict
from swarm.planning import Waypoint
from .types import FormationType, FormationStatus
from .registry import FormationRegistry
from .manager import FormationManager
from .models import Formation

# Shared registry and manager for the API facade
_registry = FormationRegistry()
_manager = FormationManager(_registry)

def create_formation(formation_id: str, name: str, formation_type: FormationType) -> Formation:
    return _manager.create_formation(formation_id, name, formation_type)

def delete_formation(formation_id: str) -> None:
    _manager.delete_formation(formation_id)

def set_leader(formation_id: str, leader_id: str) -> Formation:
    return _manager.set_leader(formation_id, leader_id)

def set_followers(formation_id: str, follower_ids: List[str]) -> Formation:
    return _manager.set_followers(formation_id, follower_ids)

def set_spacing(formation_id: str, spacing: float) -> Formation:
    return _manager.set_spacing(formation_id, spacing)

def set_type(formation_id: str, formation_type: FormationType) -> Formation:
    return _manager.set_type(formation_id, formation_type)

def generate_targets(formation_id: str, leader_waypoint: Waypoint) -> Dict[str, Waypoint]:
    return _manager.generate_targets(formation_id, leader_waypoint)

def get_formation(formation_id: str) -> Formation:
    return _manager.get_formation(formation_id)

def get_status(formation_id: str) -> FormationStatus:
    return _manager.get_status(formation_id)
