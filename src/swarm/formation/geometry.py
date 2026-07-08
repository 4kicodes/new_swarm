from typing import Dict, List
from swarm.planning import Position
from .types import FormationType
from .exceptions import InvalidFormationConfiguration

def generate_offsets(formation_type: FormationType, leader_id: str, follower_ids: List[str], spacing: float) -> Dict[str, Position]:
    """
    Generates relative offsets based on formation type.
    Followers receive relative offsets, Leader is always (0,0,0).
    """
    if spacing <= 0:
        raise InvalidFormationConfiguration("Spacing must be positive.")
    
    if leader_id in follower_ids:
        raise InvalidFormationConfiguration("Leader cannot be a follower.")
        
    if len(set(follower_ids)) != len(follower_ids):
        raise InvalidFormationConfiguration("Duplicate follower IDs detected.")

    offsets: Dict[str, Position] = {leader_id: Position(0.0, 0.0, 0.0)}
    
    for i, f_id in enumerate(follower_ids):
        idx = i + 1
        if formation_type == FormationType.LINE:
            # LINE: Followers behind leader (y is North/forward in NED, but let's use x/y/z)
            # Assuming LINE is along Y-axis (backward)
            offsets[f_id] = Position(x=0.0, y=-idx * spacing, z=0.0)
            
        elif formation_type == FormationType.COLUMN:
            # COLUMN: Followers beside leader
            offsets[f_id] = Position(x=idx * spacing, y=0.0, z=0.0)
            
        elif formation_type == FormationType.V:
            # V: Symmetric expansion
            side = 1 if i % 2 == 0 else -1
            row = (i // 2) + 1
            offsets[f_id] = Position(x=side * row * spacing, y=-row * spacing, z=0.0)
            
        elif formation_type == FormationType.GRID:
            # GRID: Square grid
            row = i // 2
            col = i % 2
            offsets[f_id] = Position(x=(col - 0.5) * 2 * spacing, y=-row * spacing, z=0.0)
            
    return offsets
