class ExecutionError(Exception):
    """Base exception for all execution domain errors."""
    pass

class SessionNotFoundError(ExecutionError):
    """Raised when an execution session cannot be found."""
    pass

class InvalidTransitionError(ExecutionError):
    """Raised when an invalid lifecycle transition is attempted."""
    pass
