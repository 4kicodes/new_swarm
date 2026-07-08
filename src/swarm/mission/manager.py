from typing import Optional, Dict
from swarm.planning import ExecutionPlan, build_execution_plan, CoordinateFrame
from swarm.formation import generate_targets
from swarm.safety import validate_execution_plan
from .models import Mission, MissionPlan, MissionProgress
from .types import MissionType, MissionStatus
from .registry import MissionRegistry
from .executor import MissionExecutor

class MissionManager:
    def __init__(self, registry: MissionRegistry):
        self.registry = registry
        self._executors: Dict[str, MissionExecutor] = {}

    def create_mission(self, mission_id: str, name: str, mission_type: MissionType) -> Mission:
        mission = Mission(mission_id=mission_id, name=name, mission_type=mission_type)
        self.registry.add(mission)
        return mission

    def delete_mission(self, mission_id: str) -> None:
        self.registry.remove(mission_id)
        if mission_id in self._executors:
            del self._executors[mission_id]

    def attach_plan(self, mission_id: str, plan: MissionPlan) -> Mission:
        mission = self.registry.get(mission_id)
        updated = Mission(
            mission_id=mission.mission_id,
            name=mission.name,
            mission_type=mission.mission_type,
            formation_id=mission.formation_id,
            enabled=mission.enabled,
            plan=plan
        )
        self.registry.remove(mission_id)
        self.registry.add(updated)
        self._executors[mission_id] = MissionExecutor(updated)
        return updated

    def assign_formation(self, mission_id: str, formation_id: str) -> Mission:
        mission = self.registry.get(mission_id)
        updated = Mission(
            mission_id=mission.mission_id,
            name=mission.name,
            mission_type=mission.mission_type,
            formation_id=formation_id,
            enabled=mission.enabled,
            plan=mission.plan
        )
        self.registry.remove(mission_id)
        self.registry.add(updated)
        return updated

    def start(self, mission_id: str) -> Optional[ExecutionPlan]:
        executor = self._executors[mission_id]
        executor.progress = MissionProgress(
            remaining_goals=[g.goal_id for g in (executor.mission.plan.goals if executor.mission.plan else [])],
            status=MissionStatus.RUNNING
        )
        return self.execute_next_goal(mission_id)

    def execute_next_goal(self, mission_id: str) -> Optional[ExecutionPlan]:
        executor = self._executors[mission_id]
        if not executor.has_next_goal():
            return None
            
        goal = executor.current_goal()
        formation_id = executor.mission.formation_id
        
        # 1. Ask Formation for targets
        targets = generate_targets(formation_id, goal.waypoint)
        
        # 2. Build Execution Plan (Simplified: build one per drone or one for swarm?)
        # Let's assume build_execution_plan takes a route (sequence of waypoints)
        # For now, build one ExecutionPlan from the targets mapping.
        # This requires planning to support this, which it does.
        from swarm.planning import create_route
        route = create_route(list(targets.values()))
        plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
        
        # 3. Validate
        result = validate_execution_plan(plan)
        if not result.valid:
            executor.progress = MissionProgress(status=MissionStatus.FAILED)
            return None
            
        # 4. Advance
        executor.advance_goal()
        return plan

    def pause(self, mission_id: str) -> None:
        pass

    def resume(self, mission_id: str) -> None:
        pass

    def cancel(self, mission_id: str) -> None:
        pass
