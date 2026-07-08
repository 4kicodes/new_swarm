from datetime import datetime
from typing import Optional
from swarm.planning import ExecutionPlan
from .models import ExecutionSession, ExecutionStatus
from .registry import ExecutionRegistry
from .exceptions import InvalidTransitionError

class ExecutionManager:
    def __init__(self, registry: ExecutionRegistry):
        self.registry = registry

    def create_session(self, session_id: str, plan: ExecutionPlan) -> ExecutionSession:
        session = ExecutionSession(session_id=session_id, execution_plan=plan, status=ExecutionStatus.CREATED)
        self.registry.add(session)
        return session

    def start(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        if session.status != ExecutionStatus.CREATED:
            raise InvalidTransitionError("Cannot start session not in CREATED state.")
        session.status = ExecutionStatus.RUNNING
        session.started_at = datetime.now()

    def pause(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        if session.status != ExecutionStatus.RUNNING:
            raise InvalidTransitionError("Can only pause RUNNING session.")
        session.status = ExecutionStatus.PAUSED

    def resume(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        if session.status != ExecutionStatus.PAUSED:
            raise InvalidTransitionError("Can only resume PAUSED session.")
        session.status = ExecutionStatus.RUNNING

    def cancel(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        session.status = ExecutionStatus.CANCELLED
        session.finished_at = datetime.now()

    def advance(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        if session.status != ExecutionStatus.RUNNING:
            raise InvalidTransitionError("Can only advance RUNNING session.")
        
        session.current_waypoint_index += 1
        if session.current_waypoint_index >= len(session.execution_plan.trajectory):
            self.mark_completed(session_id)

    def mark_completed(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        session.status = ExecutionStatus.COMPLETED
        session.finished_at = datetime.now()

    def mark_failed(self, session_id: str) -> None:
        session = self.registry.get(session_id)
        session.status = ExecutionStatus.FAILED
        session.finished_at = datetime.now()

    def get_status(self, session_id: str) -> ExecutionStatus:
        return self.registry.get(session_id).status
