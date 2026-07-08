class MissionError(Exception):
    """Base exception for all mission domain errors."""
    pass

class MissionNotFoundError(MissionError):
    """Raised when a mission cannot be found."""
    pass

class InvalidMissionConfiguration(MissionError):
    """Raised when mission configuration is invalid."""
    pass
