from typing import Optional
from swarm.planning import ExecutionPlan, Waypoint
from swarm.mission import get_mission
from swarm.formation import get_formation, generate_targets
from swarm.planning import create_route, build_execution_plan, CoordinateFrame
from swarm.safety import validate_execution_plan, SafetyResult
from swarm.execution import create_execution, ExecutionSession
from .exceptions import InvalidOrchestrationError

def orchestrate_execution(mission_id: str, leader_waypoint: Waypoint) -> ExecutionSession:
    # 1. Retrieve Mission and Formation
    mission = get_mission(mission_id)
    if not mission.formation_id:
        raise InvalidOrchestrationError(f"Mission {mission_id} has no formation assigned.")
    
    # 2. Ask Formation to generate absolute targets
    targets = generate_targets(mission.formation_id, leader_waypoint)
    
    # 3. Ask Planning to build ExecutionPlan
    route = create_route(list(targets.values()))
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    # 4. Ask Safety to validate
    result = validate_execution_plan(plan)
    if not result.valid:
        raise InvalidOrchestrationError(f"Plan validation failed: {result.violations}")
        
    # 5. Create ExecutionSession
    session = create_execution(f"session_{mission_id}", plan)
    
    return session
