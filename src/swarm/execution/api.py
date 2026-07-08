from typing import Optional
from swarm.planning import ExecutionPlan
from .models import ExecutionSession, ExecutionStatus
from .registry import ExecutionRegistry
from .manager import ExecutionManager

# Shared registry and manager
_registry = ExecutionRegistry()
_manager = ExecutionManager(_registry)

def create_execution(session_id: str, plan: ExecutionPlan) -> ExecutionSession:
    return _manager.create_session(session_id, plan)

def start_execution(session_id: str) -> None:
    _manager.start(session_id)

def pause_execution(session_id: str) -> None:
    _manager.pause(session_id)

def resume_execution(session_id: str) -> None:
    _manager.resume(session_id)

def cancel_execution(session_id: str) -> None:
    _manager.cancel(session_id)

def advance_execution(session_id: str) -> None:
    _manager.advance(session_id)

def execution_status(session_id: str) -> ExecutionStatus:
    return _manager.get_status(session_id)
