class CoordinatorError(Exception):
    """Base exception for all coordinator domain errors."""
    pass

class SessionError(CoordinatorError):
    """Raised when session operations fail."""
    pass

class InvalidOrchestrationError(CoordinatorError):
    """Raised when an orchestration sequence is invalid."""
    pass
