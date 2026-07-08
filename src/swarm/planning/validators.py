from .models import Waypoint, Route, ExecutionPlan
from .exceptions import InvalidRouteError, InvalidExecutionPlanError

def validate_route(route: Route) -> None:
    """Validates the route structure."""
    if not route.waypoints:
        raise InvalidRouteError("Route has no waypoints.")
    # Add other validations here if necessary

def validate_waypoint_sequence(route: Route) -> None:
    """Validates sequence properties if required."""
    validate_route(route)

def validate_execution_plan(plan: ExecutionPlan) -> None:
    """Validates the structure of the execution plan."""
    if not plan.trajectory:
        raise InvalidExecutionPlanError("Execution plan trajectory is empty.")
    if len(plan.route.waypoints) != len(plan.trajectory):
        raise InvalidExecutionPlanError("Route length and trajectory length mismatch.")
