class SafetyError(Exception):
    """Base exception for all safety domain errors."""
    pass

class ConstraintViolationError(SafetyError):
    """Raised when a safety constraint is violated."""
    pass

class InvalidSafetyConfigurationError(SafetyError):
    """Raised when a safety constraint configuration is invalid."""
    pass
