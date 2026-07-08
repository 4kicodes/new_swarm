from typing import Dict
from swarm.planning import Waypoint, Position, offset_waypoint
from .models import Formation
from .exceptions import FormationError

def generate_targets(formation: Formation, leader_waypoint: Waypoint, offsets: Dict[str, Position]) -> Dict[str, Waypoint]:
    """
    Computes absolute waypoints for all drones in the formation.
    
    Workflow:
    Leader Waypoint -> Geometry Engine -> Relative Offsets -> Planning.offset_waypoint() -> Absolute Waypoints
    """
    targets = {}
    
    for drone_id, offset in offsets.items():
        # Delegate coordinate transformation to the Planning domain
        targets[drone_id] = offset_waypoint(leader_waypoint, offset)
        
    return targets
