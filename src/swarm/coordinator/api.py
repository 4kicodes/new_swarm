from typing import Optional, Dict, List
from swarm.planning import ExecutionPlan, Waypoint
from swarm.mission import (
    create_mission as _create_mission,
    get_mission as _get_mission,
    attach_plan as _attach_plan,
    MissionType,
)
from swarm.formation import (
    create_formation as _create_formation,
    get_formation as _get_formation,
    set_leader as _set_leader,
    set_followers as _set_followers,
    set_spacing as _set_spacing,
    set_type as _set_type,
    generate_targets,
    FormationType,
)
from swarm.safety import validate_execution_plan, SafetyResult
from swarm.execution import ExecutionSession
from .manager import CoordinatorManager
from .exceptions import SessionError, InvalidOrchestrationError
from .orchestrator import orchestrate_execution

_manager = CoordinatorManager()

def create_session() -> None:
    _manager.clear_session()

def create_mission(mission_id: str, name: str, mission_type: MissionType) -> None:
    _create_mission(mission_id, name, mission_type)

def load_mission(mission_id: str) -> None:
    _get_mission(mission_id)
    _manager.update_session(mission_id=mission_id)

def create_formation(formation_id: str, name: str, formation_type: FormationType) -> None:
    _create_formation(formation_id, name, formation_type)

def load_formation(formation_id: str) -> None:
    _get_formation(formation_id)
    _manager.update_session(formation_id=formation_id)

def set_leader(formation_id: str, leader_id: str) -> None:
    _set_leader(formation_id, leader_id)

def set_followers(formation_id: str, follower_ids: List[str]) -> None:
    _set_followers(formation_id, follower_ids)

def set_spacing(formation_id: str, spacing: float) -> None:
    _set_spacing(formation_id, spacing)

def set_type(formation_id: str, formation_type: FormationType) -> None:
    _set_type(formation_id, formation_type)

def generate_execution_plan(leader_waypoint: Waypoint) -> Optional[ExecutionPlan]:
    session = _manager.get_session()
    if not session.mission_id or not session.formation_id:
        raise InvalidOrchestrationError("Mission or Formation not loaded")
        
    # Orchestrate
    targets = generate_targets(session.formation_id, leader_waypoint)
    
    from swarm.planning import create_route, build_execution_plan, CoordinateFrame
    route = create_route(list(targets.values()))
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    return plan

def validate_plan(plan: ExecutionPlan) -> SafetyResult:
    return validate_execution_plan(plan)

def orchestrate_mission(mission_id: str, leader_waypoint: Waypoint) -> ExecutionSession:
    return orchestrate_execution(mission_id, leader_waypoint)

def get_status() -> Dict:
    session = _manager.get_session()
    return {"mission": session.mission_id, "formation": session.formation_id}
