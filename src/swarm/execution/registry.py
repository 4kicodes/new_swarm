from typing import Dict, List
from .models import ExecutionSession
from .exceptions import SessionNotFoundError

class ExecutionRegistry:
    def __init__(self):
        self._sessions: Dict[str, ExecutionSession] = {}

    def add(self, session: ExecutionSession) -> None:
        self._sessions[session.session_id] = session

    def remove(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Session {session_id} not found.")
        del self._sessions[session_id]

    def get(self, session_id: str) -> ExecutionSession:
        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Session {session_id} not found.")
        return self._sessions[session_id]

    def list_all(self) -> List[ExecutionSession]:
        return list(self._sessions.values())
