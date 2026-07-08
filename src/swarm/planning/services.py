from typing import List
from .models import Waypoint, Route, ExecutionPlan, CoordinateFrame, TrajectoryPoint
from .exceptions import InvalidWaypointError, InvalidRouteError, InvalidExecutionPlanError
from .validators import validate_route, validate_execution_plan

def append_waypoint(route: Route, waypoint: Waypoint) -> Route:
    """Returns a new Route with the appended waypoint."""
    new_waypoints = list(route.waypoints)
    new_waypoints.append(waypoint)
    return Route(waypoints=new_waypoints)

def prepend_waypoint(route: Route, waypoint: Waypoint) -> Route:
    """Returns a new Route with the prepended waypoint."""
    new_waypoints = [waypoint] + list(route.waypoints)
    return Route(waypoints=new_waypoints)

def merge_routes(route_a: Route, route_b: Route) -> Route:
    """Returns a new Route merging route_a and route_b."""
    return Route(waypoints=list(route_a.waypoints) + list(route_b.waypoints))

def reverse_route(route: Route) -> Route:
    """Returns a new Route with reversed order."""
    return Route(waypoints=list(reversed(route.waypoints)))

def copy_route(route: Route) -> Route:
    """Returns a copy of the route."""
    return Route(waypoints=list(route.waypoints))

def build_execution_plan(route: Route, frame: CoordinateFrame) -> ExecutionPlan:
    """Service to construct an ExecutionPlan from a Route."""
    validate_route(route)
    
    trajectory = [TrajectoryPoint(waypoint=w) for w in route.waypoints]
    plan = ExecutionPlan(route=route, frame=frame, trajectory=trajectory)
    
    validate_execution_plan(plan)
    return plan
