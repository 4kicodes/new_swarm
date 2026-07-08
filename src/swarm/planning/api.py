from typing import List, Tuple
from .models import Waypoint, Route, TrajectoryPoint, ExecutionPlan, CoordinateFrame, Position
from .exceptions import InvalidWaypointError, InvalidRouteError, InvalidExecutionPlanError
from .math import (
    distance,
    bearing,
    offset_waypoint,
    relative_position,
    route_length,
    route_bounding_box,
    convert_frame,
)
from .services import (
    append_waypoint,
    prepend_waypoint,
    merge_routes,
    reverse_route,
    copy_route,
    build_execution_plan,
)

def create_waypoint(lat: float, lon: float, alt: float) -> Waypoint:
    """Factory to create and validate a Waypoint."""
    try:
        return Waypoint(latitude=lat, longitude=lon, altitude=alt)
    except Exception as e:
        raise InvalidWaypointError(f"Failed to create waypoint: {e}")

def create_route(waypoints: List[Waypoint]) -> Route:
    """Factory to create and validate a Route."""
    try:
        return Route(waypoints=waypoints)
    except Exception as e:
        raise InvalidRouteError(f"Failed to create route: {e}")
