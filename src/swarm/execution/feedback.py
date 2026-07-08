from typing import Dict, Any
from swarm.planning import distance, Position
from swarm.execution import advance_execution, execution_status, ExecutionStatus
from .events import ExecutionCompleted

class FeedbackAdapter:
    def __init__(self, bus, registry, acceptance_radius: float = 2.0):
        self.bus = bus
        self.registry = registry
        self.acceptance_radius = acceptance_radius
        self.bus.subscribe("telemetry.position", self._on_position_update)

    def _on_position_update(self, data: Dict[str, Any]):
        # data: {"drone_id": str, "position": Waypoint}
        drone_pos = data["position"]
        
        # Check all active sessions
        for session in self.registry.list_all():
            if session.status != ExecutionStatus.RUNNING:
                continue
                
            # Compare current drone position with current target waypoint
            target_wp = session.execution_plan.trajectory[session.current_waypoint_index].waypoint
            
            if distance(drone_pos, target_wp) < self.acceptance_radius:
                # Reached waypoint
                advance_execution(session.session_id)
                
                # Check for completion
                updated_session = self.registry.get(session.session_id)
                if updated_session.status == ExecutionStatus.COMPLETED:
                    self.bus.publish("execution.completed", ExecutionCompleted(session_id=session.session_id))
