from typing import Dict, Optional
from swarm.planning import ExecutionPlan
from .models import Mission, MissionPlan
from .types import MissionType, MissionStatus
from .registry import MissionRegistry
from .manager import MissionManager

# Shared registry and manager for the API facade
_registry = MissionRegistry()
_manager = MissionManager(_registry)

def create_mission(mission_id: str, name: str, mission_type: MissionType) -> Mission:
    return _manager.create_mission(mission_id, name, mission_type)

def delete_mission(mission_id: str) -> None:
    _manager.delete_mission(mission_id)

def attach_plan(mission_id: str, plan: MissionPlan) -> Mission:
    return _manager.attach_plan(mission_id, plan)

def assign_formation(mission_id: str, formation_id: str) -> Mission:
    return _manager.assign_formation(mission_id, formation_id)

def start(mission_id: str) -> Optional[ExecutionPlan]:
    return _manager.start(mission_id)

def execute_next_goal(mission_id: str) -> Optional[ExecutionPlan]:
    return _manager.execute_next_goal(mission_id)

def pause(mission_id: str) -> None:
    _manager.pause(mission_id)

def resume(mission_id: str) -> None:
    _manager.resume(mission_id)

def cancel(mission_id: str) -> None:
    _manager.cancel(mission_id)

def get_mission(mission_id: str) -> Mission:
    return _registry.get(mission_id)
