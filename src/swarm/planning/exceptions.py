class PlanningError(Exception):
    """Base exception for all planning domain errors."""
    pass

class InvalidWaypointError(PlanningError):
    """Raised when waypoint coordinates are out of bounds."""
    pass

class InvalidRouteError(PlanningError):
    """Raised when route validation fails."""
    pass

class InvalidExecutionPlanError(PlanningError):
    """Raised when execution plan validation fails."""
    pass
