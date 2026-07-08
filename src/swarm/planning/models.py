from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional
from .exceptions import InvalidWaypointError, InvalidRouteError

class CoordinateFrame(Enum):
    GLOBAL = auto()
    LOCAL_NED = auto()
    LOCAL_ENU = auto()

@dataclass(frozen=True)
class Waypoint:
    latitude: float
    longitude: float
    altitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise InvalidWaypointError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise InvalidWaypointError(f"Invalid longitude: {self.longitude}")
        if self.altitude < 0:
            raise InvalidWaypointError(f"Invalid altitude: {self.altitude}")

@dataclass(frozen=True)
class Route:
    waypoints: List[Waypoint]

    def __post_init__(self):
        if not self.waypoints:
            raise InvalidRouteError("Route must contain at least one waypoint.")

@dataclass(frozen=True)
class Position:
    x: float
    y: float
    z: float

@dataclass(frozen=True)
class TrajectoryPoint:
    waypoint: Waypoint
    timestamp: Optional[float] = None

@dataclass(frozen=True)
class ExecutionPlan:
    route: Route
    frame: CoordinateFrame
    trajectory: List[TrajectoryPoint]
