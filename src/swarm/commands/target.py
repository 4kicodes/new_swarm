from typing import List

def resolve_targets(manager, target: str) -> List[str]:
    """Resolves target string to a list of drone IDs."""
    if not target:
        return []
        
    all_drones = list(manager.connections.keys())
    
    if target == "all":
        return all_drones
    
    if target in all_drones:
        return [target]
        
    return []
