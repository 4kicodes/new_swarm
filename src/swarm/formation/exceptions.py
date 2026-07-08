class FormationError(Exception):
    """Base exception for all formation domain errors."""
    pass

class FormationNotFoundError(FormationError):
    """Raised when a formation cannot be found."""
    pass

class InvalidFormationConfiguration(FormationError):
    """Raised when formation configuration is invalid."""
    pass
